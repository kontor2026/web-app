"""Bausteine für handgebaute 3D-Modelle (siehe docs/3d-modelle.md).

Ein Modell entsteht als kleines Skript in tools/kategorien/quellen/<id>.py:

    from bau import teil, raster, explodiere, skaliere_masse, schreibe

    teile = [
        teil('deckel', 'hdpe_screw_cap', 'Schraubdeckel', 'Deckel', 'cyl', x=17.5, y=17.5, w=30, z=208, h=22,
             mass=1.8, info='...'),
        ...
    ]
    explodiere(teile, abstand=25)
    schreibe('pet_bottle', teile)

Aufruf (Projektordner):  python tools/kategorien/quellen/<id>.py
schreibe() legt tools/kategorien/modelle/<id>.json an und prüft das Modell sofort mit pruefe.py.
Nur Standardbibliothek. Koordinaten in mm, x = Breite, y = Tiefe (hinten = 0), z = Höhe.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'tools' / 'kategorien'
sys.path.insert(0, str(SRC))

from build import MATERIAL  # noqa: E402  (main() von build.py läuft beim Import nicht)
import pruefe as _pruefe  # noqa: E402

CLS = json.loads((ROOT / 'data' / 'classifier.json').read_text(encoding='utf-8'))
KATALOG = json.loads((ROOT / 'backend' / 'seed' / 'catalog.json').read_text(encoding='utf-8'))['materials']
ZEILEN = {r['id']: r for r in csv.DictReader((SRC / 'kategorien.csv').open(encoding='utf-8'), delimiter=';')}

# Reihenfolge der Felder wie in den Vorlagen
REIHENFOLGE = ('id', 'component_id', 'material_id', 'name', 'short', 'shape', 'x', 'y', 'w', 'd', 'z', 'h', 'r',
               'explode', 'mass', 'materials', 'info', 'color', 'opacity', 'label', 'sortBias', 'wand', 'boden', 'marks')


def masse(oid):
    """Maße und Gewicht aus kategorien.csv: dict mit breite, tiefe, hoehe, gramm, form, name."""
    z = ZEILEN[oid]
    return {'breite': float(z['breite']), 'tiefe': float(z['tiefe']), 'hoehe': float(z['hoehe']),
            'gramm': float(z['gramm']), 'form': z['form'], 'name': z['name']}


def komponenten(oid):
    """Komponenten-IDs des Objekts laut classifier.json."""
    return list(CLS['objects'][oid]['components'])


def teil(id, component_id, name, short, shape, *, x, y, w, z, h, d=None, r=None, mass, info,
         material_id=None, materials=None, explode=None, **extra):
    """Ein Bauteil. material_id kommt aus der Komponente, materials aus build.MATERIAL, beides überschreibbar.

    extra: color, opacity, label, sortBias, marks, wand, boden.
    wand (mm): Teil ist in der Foto-Ansicht hohl mit dieser Wandstärke, oben offen; boden (mm): Bodendicke
    (Standard = wand, 0 = auch unten offen, z. B. Ring, Reifen). Die Station zeichnet es weiter massiv."""
    if component_id not in CLS['components']:
        raise ValueError(f'{id}: unbekannte component_id {component_id}')
    mid = material_id or CLS['components'][component_id]['material_id']
    if mid not in CLS['materials']:
        raise ValueError(f'{id}: unbekannte material_id {mid}')
    mats = [list(m) for m in (materials or MATERIAL[mid])]
    if abs(sum(v for _, v in mats) - 100) > 0.01:
        raise ValueError(f'{id}: materials ergeben {sum(v for _, v in mats)} %')
    for m, _ in mats:
        if m not in KATALOG:
            raise ValueError(f'{id}: Katalog-Material {m} fehlt in backend/seed/catalog.json')
    if shape == 'box' and d is None:
        d = w
    p = dict(id=id, component_id=component_id, material_id=mid, name=name, short=short, shape=shape,
             x=x, y=y, w=w, d=d, z=z, h=h, r=r, explode=list(explode) if explode else None,
             mass=mass, materials=mats, info=info, **extra)
    unbekannt = set(p) - set(REIHENFOLGE)
    if unbekannt:
        raise ValueError(f'{id}: unbekannte Felder {unbekannt}')
    return p


def mark(shape, x, y, w, d=None, r=None, fill=None, lift=None, zeichnung=False):
    """Ein Detail auf der Oberseite eines Teils, Koordinaten relativ zum Teil.

    lift: mm über der Oberseite (Station). zeichnung=True: nur in der Zeichnung (Station, Foto aus), nicht in der
    Foto-Ansicht, z. B. aufgemalte Öffnungen, die dort ein hohles Teil (wand) ersetzt."""
    m = {'shape': shape, 'x': x, 'y': y, 'w': w}
    if lift is not None:
        m['lift'] = lift
    if zeichnung:
        m['zeichnung'] = True
    if d is not None:
        m['d'] = d
    if r is not None:
        m['r'] = r
    if fill:
        m['fill'] = fill
    return m


def raster(x0, y0, nx, ny, w, d, abstand_x, abstand_y=None, shape='box', r=None, fill=None):
    """nx × ny gleiche marks (Tasten, Lüftungsschlitze, Akkuzellen). abstand = Mittenabstand."""
    abstand_y = abstand_x if abstand_y is None else abstand_y
    return [mark(shape, round(x0 + i * abstand_x, 2), round(y0 + j * abstand_y, 2), w, d, r, fill)
            for j in range(ny) for i in range(nx)]


def _box(p, dz=None):
    dx, dy, ez = p['explode'] or (0, 0, 0)
    dz = ez if dz is None else dz
    d = p['d'] if p['d'] is not None else p['w']
    return (p['x'] + dx, p['y'] + dy, p['z'] + dz, p['x'] + dx + p['w'], p['y'] + dy + d, p['z'] + dz + p['h'])


def _schnitt_xy(a, b, tol=0.05):
    return all(min(a[i + 3], b[i + 3]) - max(a[i], b[i]) > tol for i in range(2))


def explodiere(teile, abstand, fest=(), abstaende=None, gruppen=(), nach_liste=False):
    """Setzt dz für alle Teile ohne explode, so dass explodiert nichts überlappt.

    Arbeitet von unten nach oben: jedes Teil schwebt mindestens `abstand` mm über der explodierten Oberkante
    aller Teile darunter, deren Grundriss es überlappt. Teile mit eigenem explode (z. B. seitlich herausgezogen)
    und IDs in `fest` bleiben, wo sie sind. Teile in der Liste weiter oben (Index klein) liegen weiter oben.
    `abstaende` = {id: mm} gibt einzelnen Teilen einen eigenen Abstand, z. B. Chips knapp über der Platine.
    `gruppen` = [[id, id, ...], ...]: diese Teile bekommen denselben Versatz (z. B. Segmente eines Körpers).
    `nach_liste=True`: Stapelreihenfolge folgt der Liste (letztes Teil unten) statt der Höhe im Zusammenbau,
    z. B. damit eine Haube, die tief beginnt, trotzdem über dem Innenleben schwebt."""
    abstaende = abstaende or {}
    platziert = [p for p in teile if p['explode'] is not None or p['id'] in fest]
    for p in teile:
        if p['id'] in fest and p['explode'] is None:
            p['explode'] = [0, 0, 0]
    gruppe_von = {i: n for n, g in enumerate(gruppen) for i in g}
    einheiten, gesehen = [], set()
    for p in reversed(teile):  # von unten (Listenende) nach oben
        if p['explode'] is not None or p['id'] in gesehen:
            continue
        g = gruppe_von.get(p['id'])
        e = [q for q in teile if q['explode'] is None and gruppe_von.get(q['id'], -1) == g] if g is not None else [p]
        gesehen.update(q['id'] for q in e)
        einheiten.append(e)
    if not nach_liste:  # stabil: bei gleichem z bleibt das untere Listenende unten
        einheiten.sort(key=lambda e: min(q['z'] for q in e))
    for e in einheiten:
        dz = 0.0
        for p in e:
            ab = abstaende.get(p['id'], abstand)
            for q in platziert:
                a, b = _box(p, 0), _box(q)
                if _schnitt_xy(a, b) and b[5] + ab > a[2] + dz:
                    dz = b[5] + ab - a[2]
        for p in e:
            p['explode'] = [0, 0, round(dz, 1)]
        platziert.extend(e)
    return teile


def skaliere_masse(teile, ziel=None, oid=None, stellen=1):
    """Skaliert alle Massen so, dass die Summe `ziel` g ergibt (oder das CSV-Gewicht von `oid`)."""
    ziel = ziel if ziel is not None else masse(oid)['gramm']
    summe = sum(p['mass'] for p in teile)
    for p in teile:
        p['mass'] = max(round(p['mass'] * ziel / summe, stellen), 10 ** -stellen)
    return teile


def _sauber(p):
    out = {}
    for k in REIHENFOLGE:
        if k in p and p[k] is not None and p[k] != []:
            v = p[k]
            if isinstance(v, float) and v.is_integer():
                v = int(v)
            out[k] = v
    return out


def schreibe(oid, teile, pruefen=True):
    """Schreibt modelle/<oid>.json und prüft es. Exit-Code 1 bei Fehlern."""
    if oid not in CLS['objects']:
        raise ValueError(f'unbekannte Kategorie {oid}')
    ids = [p['id'] for p in teile]
    doppelt = {i for i in ids if ids.count(i) > 1}
    if doppelt:
        raise ValueError(f'doppelte ids: {doppelt}')
    ohne = [p['id'] for p in teile if p['explode'] is None]
    if ohne:
        raise ValueError(f'Teile ohne explode (explodiere() aufrufen oder explode setzen): {ohne}')
    ziel = SRC / 'modelle' / f'{oid}.json'
    ziel.write_text(json.dumps({'parts': [_sauber(p) for p in teile]}, ensure_ascii=False, indent=1) + '\n',
                    encoding='utf-8')
    if not pruefen:
        return
    katalog = json.loads((ROOT / 'backend' / 'seed' / 'catalog.json').read_text(encoding='utf-8'))['materials']
    fehler, warn = _pruefe.pruefe(oid, CLS, katalog, ZEILEN)
    print(f'{oid}: {"FEHLER" if fehler else "ok"}, {len(teile)} Teile, {sum(p["mass"] for p in teile):g} g '
          f'(CSV {masse(oid)["gramm"]:g} g)' + (f', {len(warn)} Warnungen' if warn else ''))
    for f in fehler:
        print(f'  ✗ {f}')
    for w in warn:
        print(f'  ! {w}')
    if fehler:
        sys.exit(1)
