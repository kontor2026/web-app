"""Belegte Bauideen aus data/rezepte (dieselben wie auf der Werkbank der Website).

Ein Rezept passt, wenn der Gegenstand eine Komponente hat, die das Rezept braucht (component_id oder
eine Alternative aus "oder"). Die Komponenten stehen an den Bauteilen der Kategorie-Modelle und in
data/classifier.json. Passende Rezepte kommen vor die Ideen der KI."""
import json
from functools import cache

from . import config

QUELLE = config.ROOT / 'data'

WERKZEUG = {
    'shredding_bike_shredder': 'Fahrrad-Schredder', 'shredding_granulator': 'Granulator', 'injection_molding': 'Spritzguss',
    'extrusion': 'Extruder', '3d_printing': '3D-Drucker', 'laser_processing': 'Laser', 'drilling': 'Bohren', 'sawing': 'Sägen',
    'filing': 'Feilen', 'milling': 'Fräsen', 'screwing': 'Schrauben', 'soldering': 'Löten', 'gluing_hot_glue': 'Heißkleber',
    'gluing_super_glue': 'Sekundenkleber', 'gluing_two_component': '2K-Kleber', 'gluing_wood_glue': 'Holzleim',
    'gluing_double_sided_tape': 'Klebeband',
}
# Einordnung nach § 6 KrWG wie in data/rezepte/README.md: neu geformter Kunststoff ist Recycling.
FORMEN = {'shredding_bike_shredder', 'shredding_granulator', 'injection_molding', 'extrusion'}


def _json(name):
    p = QUELLE / name
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


@cache
def alle():
    ordner = QUELLE / 'rezepte'
    if not ordner.exists():
        return []
    return [{'id': f.stem, **json.loads(f.read_text(encoding='utf-8'))} for f in sorted(ordner.glob('*.json'))]


@cache
def _namen():
    return _json('bauteile_de.json')


@cache
def _objekt_komponenten():
    return {oid: set(o.get('components', [])) for oid, o in _json('classifier.json').get('objects', {}).items()}


def _komponenten(obj):
    ids = {p['component_id'] for p in obj.get('parts', []) if p.get('component_id')}
    return ids | _objekt_komponenten().get(obj['id'], set())


def _projekt(r, eigene, obj):
    name = lambda c: _namen().get(c, c.replace('_', ' '))
    nutzt = []
    for b in r['braucht']:
        treffer = next((c for c in [b['component_id'], *b.get('oder', [])] if c in eigene), None)
        if treffer and not any(u.get('neu') for u in nutzt):
            nutzt.append({'neu': True, 'name': name(treffer)})
        else:
            nutzt.append({'extra': name(b['component_id']), 'menge': b.get('menge', 1)})
    recycling = bool(FORMEN & set(r['werkzeug']))
    return {
        'titel': r['titel'], 'kurz': r['kurz'], 'stufe': r['stufe'], 'dauer': r['dauer'],
        'lernziel': ('Recycling: Kunststoff wird zerkleinert und neu geformt, statt im Müll zu landen.' if recycling
                     else 'Wiederverwendung: Ein ausgebautes Bauteil bekommt eine neue Aufgabe.'),
        'nutzt': nutzt, 'werkzeug': [WERKZEUG.get(w, w) for w in r['werkzeug']] or ['Schere', 'Nadel und Faden'],
        'schritte': r['schritte'], 'sicherheit': r.get('sicherheit'), 'quelle': r.get('quelle'), 'rezept': r['id'],
    }


def passend(obj):
    """Rezepte, die ein Bauteil dieses Gegenstands nutzen, im App-Format. Leichte zuerst."""
    eigene = _komponenten(obj)
    treffer = [r for r in alle()
               if any(c in eigene for b in r['braucht'] for c in [b['component_id'], *b.get('oder', [])])]
    return [_projekt(r, eigene, obj) for r in sorted(treffer, key=lambda r: r['stufe'])]


def als_beispiel():
    """Kurzliste für den Prompt der KI: so sehen geprüfte Ideen der Werkstatt aus."""
    return '; '.join(f'{r["titel"]} ({r["kurz"]})' for r in alle())
