"""HTTP-Schnittstelle der Station. Liefert auch das Frontend aus, die Station braucht nur diesen Prozess.

Start (aus dem Projektordner):  uvicorn backend.app.main:app --port 8000
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import config, db, llm, pipeline

app = FastAPI(title='Kreislauf-Station')


class ScanIn(BaseModel):
    image: str                     # data:image/jpeg;base64,...


class SteckbriefIn(BaseModel):
    scan_id: int | None = None
    modell: str | None = None      # bestätigter Kandidat
    objekt: str | None = None      # Gattung als Rückfall


class StoreIn(BaseModel):
    object_id: str
    modell: str | None = None


class StartIn(BaseModel):
    object_id: str
    projekt: int


def _run(fn, *args, **kw):
    try:
        return fn(*args, **kw)
    except (pipeline.PipelineError, llm.LLMError) as e:
        raise HTTPException(502, str(e)) from e


@app.get('/api/health')
def health():
    return {**llm.health(), 'objekte': len(db.list_objects())}


@app.post('/api/scan')
def scan(body: ScanIn):
    return _run(pipeline.scan, body.image)


@app.post('/api/steckbrief')
def steckbrief(body: SteckbriefIn):
    return _run(pipeline.steckbrief, body.scan_id, body.modell, body.objekt)


@app.get('/api/objects')
def objects(status: str | None = None):
    return db.list_objects(status)


@app.get('/api/objects/{oid}')
def get_object(oid: str):
    o = db.get_object(oid)
    if not o:
        raise HTTPException(404, 'Unbekanntes Objekt')
    return o


@app.post('/api/objects/{oid}/freigeben')
def approve(oid: str):
    """Werkstatt hat den KI-Entwurf geprüft."""
    db.set_status(oid, 'geprueft')
    return {'ok': True}


@app.delete('/api/objects/{oid}')
def discard(oid: str):
    """Werkstatt verwirft einen KI-Entwurf. Geprüfte Objekte bleiben geschützt."""
    o = db.get_object(oid)
    if not o:
        raise HTTPException(404, 'Unbekanntes Objekt')
    if o['status'] != 'entwurf':
        raise HTTPException(409, 'Nur Entwürfe können verworfen werden')
    db.delete_object(oid)
    return {'ok': True}


@app.post('/api/objects/{oid}/ideen')
def ideas(oid: str, neu: bool = False):
    return _run(pipeline.ideen, oid, neu)


@app.get('/api/inventory')
def inventory():
    return db.inventory()


@app.post('/api/inventory/einlagern')
def store(body: StoreIn):
    o = db.get_object(body.object_id)
    if not o:
        raise HTTPException(404, 'Unbekanntes Objekt')
    return db.store_item(o, body.modell)


@app.post('/api/projekte/start')
def start(body: StartIn):
    o = db.get_object(body.object_id)
    if not o or body.projekt >= len(o.get('projekte', [])):
        raise HTTPException(404, 'Unbekanntes Projekt')
    res = db.book(body.object_id, o['projekte'][body.projekt])
    if not res['ok']:
        raise HTTPException(409, 'Nicht genug im Lager: ' + ', '.join(res['fehlt']))
    return res


# Frontend mitausliefern, wenn vorhanden (Entwicklung, ein Prozess). Im Docker-Betrieb
# übernimmt das der Frontend-Container (nginx), dort fehlt index.html im Backend-Image.
if (config.ROOT / 'index.html').exists():
    for d in ['css', 'js', 'vendor', 'assets']:
        app.mount(f'/{d}', StaticFiles(directory=config.ROOT / d), name=d)

    @app.get('/')
    def index():
        return FileResponse(config.ROOT / 'index.html')
