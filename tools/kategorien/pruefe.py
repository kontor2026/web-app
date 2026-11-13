"""Prüft die handgebauten Modelle in tools/kategorien/modelle/ gegen docs/3d-modelle.md.

Aufruf (Projektordner):  python tools/kategorien/pruefe.py [id ...]
Ohne Argument werden alle Dateien in modelle/ geprüft. Exit-Code 1 bei Fehlern, Warnungen brechen nicht ab.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'tools' / 'kategorien'
PFLICHT = ('id', 'name', 'shape', 'x', 'y', 'w', 'z', 'h', 'explode', 'mass', 'materials', 'info')


def box(p, explodiert):
    dx, dy, dz = p['explode'] if explodiert else (0, 0, 0)
    d = p.get('d', p['w'])
    return (p['x'] + dx, p['y'] + dy, p['z'] + dz, p['x'] + dx + p['w'], p['y'] + dy + d, p['z'] + dz + p['h'])


def schnitt(a, b, tol=0.05):
    return all(min(a[i + 3], b[i + 3]) - max(a[i], b[i]) > tol for i in range(3))


def pruefe(oid, cls, katalog, zeilen):
    fehler, warn = [], []
    parts = json.loads((SRC / 'modelle' / f'{oid}.json').read_text(encoding='utf-8'))['parts']
    if oid not in cls['objects']:
        return [f'unbekannte Kategorie {oid}'], warn
    ids = set()
    for p in parts:
        pid = p.get('id', '?')
        for f in PFLICHT:
            if f not in p:
                fehler.append(f'{pid}: Feld {f} fehlt')
        if pid in ids:
            fehler.append(f'{pid}: doppelte id')
        ids.add(pid)
        if p.get('shape') not in ('box', 'cyl'):
            fehler.append(f'{pid}: shape {p.get("shape")}')
        if p.get('shape') == 'box' and 'd' not in p:
            fehler.append(f'{pid}: box ohne d')
        if 'short' not in p:
            warn.append(f'{pid}: ohne short')
        elif len(p['short']) > 18:
            warn.append(f'{pid}: short länger als 18 Zeichen')
        if 'component_id' not in p:
            warn.append(f'{pid}: ohne component_id')
        elif p['component_id'] not in cls['components']:
            fehler.append(f'{pid}: component_id {p["component_id"]} unbekannt')
        if 'material_id' in p and p['material_id'] not in cls['materials']:
            fehler.append(f'{pid}: material_id {p["material_id"]} unbekannt')
        mats = p.get('materials', [])
        if abs(sum(v for _, v in mats) - 100) > 0.01:
            fehler.append(f'{pid}: materials ergeben {sum(v for _, v in mats)} %')
        for m, _ in mats:
            if m not in katalog:
                fehler.append(f'{pid}: Katalog-Material {m} fehlt')
        for m in p.get('marks', []):
            mw, md = m['w'], m.get('d', m['w'])
            if m['x'] < -0.01 or m['y'] < -0.01 or m['x'] + mw > p['w'] + 0.01 or m['y'] + md > p.get('d', p['w']) + 0.01:
                warn.append(f'{pid}: mark ragt über das Teil hinaus')

    fehlt = set(cls['objects'][oid]['components']) - {p.get('component_id') for p in parts}
    if fehlt:
        (fehler if any('component_id' in p for p in parts) else warn).append(f'Komponenten ohne Teil: {sorted(fehlt)}')

    z = zeilen[oid]
    W, D, H, g = (float(z[k]) for k in ('breite', 'tiefe', 'hoehe', 'gramm'))
    masse = sum(p.get('mass', 0) for p in parts)
    if abs(masse - g) > max(0.15 * g, 1):
        fehler.append(f'Masse {masse:g} g, CSV {g:g} g')
    boxes = [box(p, False) for p in parts]
    ext = [max(b[i + 3] for b in boxes) - min(b[i] for b in boxes) for i in range(3)]
    for name, ist, soll in zip('BTH', ext, (W, D, H)):
        if ist > soll * 1.1 + 3 or ist < soll * 0.85 - 3:
            warn.append(f'zusammengebaut {name} = {ist:g} mm, CSV {soll:g} mm')

    ex = [box(p, True) for p in parts]
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            if schnitt(ex[i], ex[j]):
                fehler.append(f'explodiert überlappen {parts[i]["id"]} und {parts[j]["id"]}')
    return fehler, warn


def main():
    cls = json.loads((ROOT / 'data' / 'classifier.json').read_text(encoding='utf-8'))
    katalog = json.loads((ROOT / 'backend' / 'seed' / 'catalog.json').read_text(encoding='utf-8'))['materials']
    zeilen = {r['id']: r for r in csv.DictReader((SRC / 'kategorien.csv').open(encoding='utf-8'), delimiter=';')}
    ids = sys.argv[1:] or sorted(f.stem for f in (SRC / 'modelle').glob('*.json'))
    schlecht = 0
    for oid in ids:
        fehler, warn = pruefe(oid, cls, katalog, zeilen)
        schlecht += bool(fehler)
        status = 'FEHLER' if fehler else 'ok'
        print(f'{oid}: {status}' + (f' ({len(warn)} Warnungen)' if warn else ''))
        for f in fehler:
            print(f'  ✗ {f}')
        for w in warn:
            print(f'  ! {w}')
    sys.exit(1 if schlecht else 0)


if __name__ == '__main__':
    main()
