"""Die drei KI-Schritte mit Prüfung, Wiederholung, Cache und Vorausrechnen.

Reihenfolge pro Scan:
  1. Qualitätscheck (Helligkeit, Schärfe)           ohne KI
  2. Foto-Abgleich mit bekannten Fotos (dHash)       ohne KI, sofort
  3. Erkennung mit Vision-Modell                     KI, Ausgabe nach Schema
  4. Steckbrief: Cache nach Modellname, sonst KI     KI liefert Struktur, Code rechnet Geometrie
  5. Bauideen: Lagerbestand + KI, Lager-IDs im Schema erzwungen

Vorausrechnen: Mit Claude starten Steckbrief (4) und Bauideen (5) schon beim Upload parallel zur
Erkennung (3), denn beide brauchen nur das Bild. Beim lokalen Modell (eine Anfrage nach der anderen)
laufen die Bauideen im Hintergrund direkt nach dem Steckbrief, während die Zeichnung angeschaut wird.
"""
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from . import config, db, images, llm, schemas
from .layout import build_object, slug

SYSTEM = ('Du arbeitest an einer Scan-Station in einer offenen Upcycling-Werkstatt für Schülerinnen und Schüler. '
          'Antworte auf Deutsch, in kurzen, klaren Sätzen ohne Fachjargon. Erfinde keine genauen Zahlen: '
          'Schätzungen kennzeichnest du mit "≈". Wenn du etwas nicht sicher weißt, sag es.')


class PipelineError(Exception):
    pass


# Kleine Modelle kennen die IDs nicht: Liste mit Klarnamen in den Prompt.
MATERIAL_LISTE = 'Erlaubte Material-IDs: ' + '; '.join(
    f'{mid} = {m["name"]}' for mid, m in schemas.CATALOG['materials'].items())


def _with_retry(call, validate, repair=None):
    """Ein Versuch, bei Prüffehlern ein zweiter mit der Fehlerliste als Hinweis.
    Schlägt auch der fehl, repariert repair() die Antwort deterministisch, sofern möglich."""
    fehler = None
    for _ in range(2):
        data, info = call(fehler)
        fehler = validate(data)
        if not fehler:
            return data, info
    if repair:
        return repair(data), info
    raise PipelineError('Die KI-Antwort hat die Prüfung zweimal nicht bestanden: ' + '; '.join(fehler))


# ---------------------------------------------------------------- Hintergrund-Jobs

_pool = ThreadPoolExecutor(max_workers=6, thread_name_prefix='ki')
_jobs = {}                       # scan_id -> {'steckbrief': Future, 'ideen': Future}
_jobs_lock = threading.Lock()


def vorausrechnen():
    return config.VORAUSRECHNEN == 'an' or (config.VORAUSRECHNEN == 'auto' and config.LLM_PROVIDER != 'lokal')


def _start(scan_id, art, fn, *args):
    with _jobs_lock:
        _jobs.setdefault(scan_id, {})[art] = _pool.submit(fn, *args)
        for alt in sorted(_jobs)[:-50]:          # nur die letzten 50 Scans merken
            _jobs.pop(alt, None)


def _job(scan_id, art):
    with _jobs_lock:
        return _jobs.get(scan_id, {}).get(art)


def jobs(scan_id):
    """Stand der Hintergrund-Jobs eines Scans: aus, laeuft, fertig oder fehler."""
    out = {}
    for art in ('steckbrief', 'ideen'):
        f = _job(scan_id, art)
        out[art] = 'aus' if f is None else 'laeuft' if not f.done() else 'fehler' if f.exception() else 'fertig'
    return out


def _warte(f):
    try:
        return f.result(timeout=config.LLM_TIMEOUT)
    except Exception:  # noqa: BLE001 - ein gescheiterter Vorlauf wird einfach neu gerechnet
        return None


# ---------------------------------------------------------------- 1–3 Scan

SCAN_PROMPT = ('Was für ein Gegenstand liegt auf diesem Foto? Bewerte nur den Gegenstand selbst, '
               'nicht den Untergrund (Tisch, Boden) und nicht den Hintergrund.\n'
               '- objekt: was für ein Gegenstand es ist, als allgemeiner Begriff ohne Marke.\n'
               '- kandidaten: bis zu drei konkrete Modelle oder Produkte mit Marke, mit deiner Sicherheit (0 bis 1).\n'
               '- sichtbarer_text: abgelesener Text wie Marke oder Typenschild.\n'
               '- material_vermutung: die Hauptmaterialien, jedes nur einmal. Achte auf Glas gegenüber Kunststoff.\n'
               '- ist_gegenstand: false, wenn kein Gegenstand zu sehen ist.\n' + MATERIAL_LISTE)


def scan(data_url):
    t0 = time.perf_counter()
    img = images.decode(data_url)
    q = images.quality(img)
    h = images.dhash(img)
    # Gegenstand freistellen: Die KI sieht dann nur das Objekt, nicht Tisch oder Hintergrund.
    box = images.find_object(img)
    obj_img = images.crop(img, box) if box else img
    sid = db.save_scan({'status': 'laeuft'}, h, img, obj_img if box else None)

    hit = db.find_photo(h)
    if hit:
        o = db.get_object(hit[1])
        result = {
            'quelle': 'foto-abgleich', 'objekt': o['name'], 'kategorie': o['klasse'], 'conf': o['erkennung']['conf'],
            'kandidaten': [{'name': n, 'conf': c, 'object_id': o['id']} for n, c in o['erkennung']['modelle']],
            'hinweis': o['erkennung'].get('hinweis'), 'material_vermutung': [], 'sichtbarer_text': '',
            'schritte': [{'name': 'Qualität geprüft', 'ms': 0}, {'name': f'Foto-Abgleich: Treffer (Abstand {hit[0]})', 'ms': 0}],
        }
    elif config.LLM_MODE == 'mock':
        objs = db.list_objects()
        result = {
            'quelle': 'mock', 'objekt': 'Unbekannt', 'kategorie': 'Sonstiges', 'conf': 0.0,
            'kandidaten': [{'name': o['name'], 'conf': None, 'object_id': o['id']} for o in objs][:4],
            'hinweis': 'KI ist gerade abgeschaltet. Bitte Gegenstand aus der Liste wählen.',
            'material_vermutung': [], 'sichtbarer_text': '', 'schritte': [{'name': 'Foto-Abgleich: kein Treffer', 'ms': 0}],
        }
    else:
        if vorausrechnen():
            # Steckbrief und Bauideen brauchen nur das Bild: sofort parallel zur Erkennung starten.
            _start(sid, 'steckbrief', _steckbrief_ki, sid, None)
            _start(sid, 'ideen', _ideen_ki, None, sid)
        data, info = _with_retry(
            lambda f: llm.chat_json(model=config.VISION_MODEL, system=SYSTEM,
                                    user=SCAN_PROMPT + (f'\nKorrigiere: {f}' if f else ''),
                                    schema=schemas.SCAN, name='scan', images=[images.to_data_url(obj_img)], max_tokens=600),
            lambda d: [] if d.get('kandidaten') else ['mindestens ein Kandidat'])
        kands = sorted(data['kandidaten'], key=lambda k: -k['sicherheit'])
        result = {
            'quelle': 'ki', 'objekt': data['objekt'], 'kategorie': data['kategorie'], 'conf': data['sicherheit'],
            'ist_gegenstand': data['ist_gegenstand'],
            'kandidaten': [{'name': k['name'], 'conf': round(k['sicherheit'], 2),
                            'object_id': db.find_alias(k['name'])} for k in kands],
            'hinweis': 'Die Sicherheit ist eine Selbsteinschätzung des Modells. Bitte prüfen.',
            'material_vermutung': list(dict.fromkeys(data['material_vermutung'])), 'sichtbarer_text': data['sichtbarer_text'],
            'schritte': [{'name': 'Qualität geprüft', 'ms': 0}, {'name': 'Foto-Abgleich: kein Treffer', 'ms': 0},
                         {'name': 'Gegenstand freigestellt' if box else 'Freistellen: ganzes Bild', 'ms': 0},
                         {'name': f'Erkennung mit {info["modell"]}', 'ms': info['ms']}],
        }
    result['qualitaet'] = q
    result['bbox'] = [round(v, 3) for v in box] if box else None
    result['dauer_ms'] = round((time.perf_counter() - t0) * 1000)
    result['scan_id'] = sid
    db.update_scan(sid, result)
    result['vorbereitung'] = jobs(sid)
    return result


# ---------------------------------------------------------------- 4 Steckbrief

def _check_steckbrief(d):
    f = []
    m = d.get('masse_mm', {})
    if min(m.get('breite', 0), m.get('tiefe', 0), m.get('hoehe', 0)) <= 0:
        f.append('alle Maße müssen größer als 0 sein')
    namen = [t['name'] for t in d.get('bauteile', [])]
    if len(set(namen)) < len(namen):
        f.append('jedes Bauteil braucht einen eigenen Namen')
    teile = d.get('bauteile', [])
    if not any(t['breite_anteil'] > 0.8 and t['tiefe_anteil'] > 0.8 for t in teile):
        f.append('mindestens ein Bauteil muss die ganze Grundfläche einnehmen (Gehäuse, Körper oder Platte)')
    if len(teile) >= 3 and len({t['ebene'] for t in teile}) < 3:
        f.append('verteile die Bauteile auf mindestens 3 Ebenen: Unterteil unten, Innenteile in der Mitte, Deckel oben')
    for t in teile:
        if sum(m['anteil'] for m in t['materialien']) < 50:
            f.append(f'Materialanteile von {t["name"]} müssen zusammen etwa 100 ergeben')
    return f


STECKBRIEF_REGELN = (
    'Erstelle einen Material-Steckbrief für diesen Gegenstand. Das Feld name ist nur der Gegenstand, ohne Zusätze.\n'
    'Zerlege den Gegenstand gedanklich in 4 bis 10 Bauteile, wie bei einer Explosionszeichnung:\n'
    '- ebene 0 ist ganz unten, höhere Ebenen liegen darüber. Teile auf derselben Ebene liegen nebeneinander.\n'
    '- Teile das Gehäuse in Unterteil (ebene 0) und Deckel oder Oberteil (oberste Ebene). '
    'Innenteile wie Akku, Platine, Magnete liegen auf den Ebenen dazwischen.\n'
    '- form: "platte" für flache, durchgehende Schichten, "block" für Kästen, "rund" für Zylinder.\n'
    '- breite_anteil und tiefe_anteil: Anteil an der Grundfläche (1 = ganze Breite).\n'
    '- materialien nur aus der erlaubten Liste, anteil in Prozent.\n'
    '- masse_mm in Millimetern für den ganzen Gegenstand, liegend wie auf dem Foto.\n'
    + MATERIAL_LISTE + '\n'
    'Nenne bei Entsorgung, wohin der Gegenstand in Deutschland gehört. Geräte mit Akku nie selbst öffnen oder den Akku ausbauen, '
    'sondern als Elektroaltgerät abgeben. Schreibe jede Warnung nur einmal. '
    'rohstoffwert, gebrauchtwert und co2_kg als kurze Schätzung mit "≈".')


def _steckbrief_ki(scan_id, name, objekt=None):
    """Steckbrief mit KI erzeugen und als Entwurf speichern. name=None: Die KI bestimmt den
    Gegenstand selbst aus dem Bild (Vorausrechnen, bevor die Erkennung fertig ist)."""
    row, img = db.get_scan(scan_id) if scan_id else (None, None)
    scan_res = row['result'] if row else {}
    if name:
        kopf = (f'Gegenstand: {name}\nAllgemein: {scan_res.get("objekt") or objekt or "unbekannt"}\n'
                f'Sichtbarer Text auf dem Foto: {scan_res.get("sichtbarer_text") or "keiner"}\n')
    else:
        kopf = ('Bestimme zuerst selbst, welcher Gegenstand auf dem Foto liegt, möglichst mit Marke und Modell, '
                'und trage das in name ein.\n')
    imgs = [images.to_data_url(img)] if img else []
    data, info = _with_retry(
        lambda f: llm.chat_json(model=config.VISION_MODEL if imgs else config.TEXT_MODEL, system=SYSTEM,
                                user=kopf + STECKBRIEF_REGELN + (f'\nDeine letzte Antwort hatte Fehler, korrigiere: {f}' if f else ''),
                                schema=schemas.STECKBRIEF, name='steckbrief', images=imgs, max_tokens=3500),
        _check_steckbrief)

    name = name or data['name']
    oid = slug(name)
    if db.get_object(oid):
        oid = f'{oid}-{int(time.time()) % 100000}'
    quelle = f'KI-Entwurf mit {info["modell"]}, noch nicht von der Werkstatt geprüft. Werte sind Schätzungen.'
    obj = build_object(data, oid=oid, modell=name, scan=scan_res, quelle=quelle)
    obj['scan_id'] = scan_id
    db.put_object(obj, 'entwurf', info['modell'], aliases=[name], photo_hash=row['hash'] if row else None)
    obj['status'] = 'entwurf'
    if scan_id and not _job(scan_id, 'ideen'):
        # Lokales Modell: Bauideen im Hintergrund, während die Explosionszeichnung angeschaut wird.
        _start(scan_id, 'ideen', _ideen_ki, obj['id'], scan_id)
    return obj


def steckbrief(scan_id, modell, objekt=None):
    t0 = time.perf_counter()
    cached = db.find_alias(modell) if modell else None
    if cached:
        return {'object': db.get_object(cached), 'quelle': 'cache', 'dauer_ms': 0}
    if config.LLM_MODE == 'mock':
        raise PipelineError('Die KI ist gerade abgeschaltet. Für neue Gegenstände ist kein Steckbrief möglich.')

    row, _ = db.get_scan(scan_id) if scan_id else (None, None)
    scan_res = row['result'] if row else {}
    kands = scan_res.get('kandidaten') or []
    vorlauf = _job(scan_id, 'steckbrief') if scan_id else None
    # Der Vorlauf passt, wenn der wahrscheinlichste Kandidat oder "weiß ich nicht" gewählt wurde.
    passt = not modell or modell in (scan_res.get('objekt'), objekt) or (kands and modell == kands[0]['name'])
    if vorlauf and passt:
        obj = _warte(vorlauf)
        if obj:
            obj['erkennung'] = {
                'conf': scan_res.get('conf', 0.5),
                'modelle': [[k['name'], k['conf']] for k in kands] or obj['erkennung']['modelle'],
                'hinweis': obj['erkennung']['hinweis'],
            }
            status = obj.pop('status', 'entwurf')
            db.put_object(obj, status, 'vorlauf', aliases=[modell] if modell else [])
            obj['status'] = status
            return {'object': obj, 'quelle': 'vorausberechnet', 'dauer_ms': round((time.perf_counter() - t0) * 1000)}
    obj = _steckbrief_ki(scan_id, modell or scan_res.get('objekt') or objekt or 'Gegenstand', objekt)
    return {'object': obj, 'quelle': 'ki', 'dauer_ms': round((time.perf_counter() - t0) * 1000)}


# ---------------------------------------------------------------- 5 Bauideen

WERKZEUG = ('Säge, Akkuschrauber, Bohrer, Cutter, Heißklebepistole, Lötkolben, Abisolierzange, Schleifpapier, '
            'Fahrrad-Schredder für Kunststoff, Spritzgussmaschine mit Karabinerform, Plattenpresse')


def _bestand(ausser=None):
    return {i['id']: i for i in db.inventory() if i['menge'] > 0 and (ausser is None or i['object_id'] != ausser)}


def _ideen_ki(object_id, scan_id=None):
    """Drei Bauideen erzeugen. Mit object_id aus den Bauteilen des Steckbriefs, sonst nur aus dem Bild
    (Vorausrechnen parallel zum Steckbrief). Rückgabe: Rohdaten nach Schema."""
    obj = db.get_object(object_id) if object_id else None
    bestand = _bestand(object_id)
    beispiele = [p for f in sorted((config.SEED / 'objects').glob('*.json'))
                 for p in json.loads(f.read_text(encoding='utf-8')).get('projekte', [])][:2]
    imgs = []
    if obj:
        teile = '; '.join(f"{p['name']} ({', '.join(schemas.CATALOG['materials'][m]['name'] for m, _ in p['materials'])})"
                          for p in obj['parts'])
        kopf = f'Ein Schüler hat gerade abgegeben: {obj["name"]}. Bauteile: {teile}.\n'
    else:
        _, img = db.get_scan(scan_id)
        imgs = [images.to_data_url(img)] if img else []
        kopf = ('Ein Schüler hat gerade den Gegenstand auf dem Foto abgegeben. Erkenne ihn und seine wahrscheinlichen '
                'Bauteile selbst. neu_teil ist ein Bauteil dieses Gegenstands mit einem gängigen Namen.\n')
    user = (kopf + 'Lager der Werkstatt (id: Name, Bestand): '
            + '; '.join(f"{i['id']}: {i['name']}, {i['menge']:g} {i['einheit']}" for i in bestand.values()) + '\n'
            f'Werkzeug in der Werkstatt: {WERKZEUG}.\n'
            'Schlage genau drei unterschiedliche Upcycling-Projekte vor, die Schüler in einer Werkstattstunde bauen können. '
            'Jedes Projekt verwendet ein Teil des neuen Gegenstands (neu_teil) und kann Material aus dem Lager nutzen, '
            'höchstens 10 Stück je Lagerartikel. '
            'Keine Projekte, bei denen Akkus geöffnet werden oder an Netzspannung gearbeitet wird. '
            'Ein Projekt soll leicht sein (stufe 1). lernziel: was man über Material oder Kreislauf lernt.\n'
            f'Beispiele für Stil und Umfang: {json.dumps(beispiele, ensure_ascii=False)}')

    def check(d):
        f = []
        if len({p['titel'] for p in d['projekte']}) < 3:
            f.append('drei verschiedene Projekte')
        for p in d['projekte']:
            if p['neu_teil'].lower() in bestand:
                f.append(f'"{p["titel"]}": neu_teil muss ein Bauteil des abgegebenen Gegenstands sein, kein Lagerartikel')
        return f

    schema = schemas.projekte_schema(list(bestand) or ['keins'])
    data, _ = _with_retry(
        lambda f: llm.chat_json(model=config.VISION_MODEL if imgs else config.TEXT_MODEL, system=SYSTEM,
                                user=user + (f'\nKorrigiere: {f}' if f else ''), schema=schema, name='projekte',
                                images=imgs, max_tokens=2500, temperature=0.5),
        check, lambda d: d)
    return data


def _projekte(data, obj):
    """Rohdaten in das Format der App bringen, gegen Objekt und aktuellen Lagerbestand geprüft."""
    bestand = _bestand(obj['id'])
    projekte = []
    for p in data['projekte']:
        neu = p['neu_teil']
        if neu.lower() in bestand:
            neu = f'{obj["name"]} (ganzer Gegenstand)'
        lager = {}
        for u in p['lager']:
            if u['id'] in bestand:
                lager[u['id']] = min(lager.get(u['id'], 0) + u['menge'], 10, int(bestand[u['id']]['menge']))
        projekte.append({
            'titel': p['titel'], 'kurz': p['kurz'], 'stufe': p['stufe'], 'dauer': p['dauer'], 'lernziel': p['lernziel'],
            'nutzt': [{'neu': True, 'name': neu}] + [{'inv': k, 'menge': max(1, v)} for k, v in lager.items()],
            'werkzeug': p['werkzeug'], 'schritte': p['schritte'],
        })
    return projekte


def ideen(object_id, neu=False):
    t0 = time.perf_counter()
    obj = db.get_object(object_id)
    if not obj:
        raise PipelineError('Unbekanntes Objekt')
    if obj.get('projekte') and not neu:
        return {'projekte': obj['projekte'], 'quelle': 'cache', 'dauer_ms': 0}
    if config.LLM_MODE == 'mock':
        raise PipelineError('Die KI ist gerade abgeschaltet. Bauideen sind nur für bekannte Gegenstände da.')

    vorlauf = _job(obj.get('scan_id'), 'ideen') if not neu else None
    data = _warte(vorlauf) if vorlauf else None
    quelle = 'vorausberechnet' if data else 'ki'
    if not data:
        data = _ideen_ki(object_id)
    projekte = _projekte(data, obj)
    obj['projekte'] = projekte
    status = obj.pop('status', 'entwurf')
    db.put_object(obj, status, 'ideen')
    return {'projekte': projekte, 'quelle': quelle, 'dauer_ms': round((time.perf_counter() - t0) * 1000)}
