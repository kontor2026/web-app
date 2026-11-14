"""JSON-Schemas für die drei KI-Schritte.

Feste Aufzählungen (Material-IDs, Lager-IDs, Kategorien) stehen direkt im Schema. Das Modell kann
dadurch nichts erfinden, was die App nicht kennt. Die Schemas sind bewusst flach (keine $ref),
damit jeder Modellserver sie in eine Grammatik übersetzen kann."""
import json

from . import config

CATALOG = json.loads((config.SEED / 'catalog.json').read_text(encoding='utf-8'))
MATERIAL_IDS = list(CATALOG['materials'])

KATEGORIEN = [
    'Elektroschrott · Kleingerät', 'Elektroschrott · Bildschirmgerät', 'Elektroschrott · Großgerät',
    'Verpackung · Kunststoff', 'Verpackung · Glas', 'Verpackung · Metall', 'Verpackung · Papier',
    'Textil', 'Holz', 'Sonstiges',
]
POSITIONEN = ['hinten-links', 'hinten', 'hinten-rechts', 'links', 'mitte', 'rechts', 'vorne-links', 'vorne', 'vorne-rechts']

# The 201 category models (backend/seed/kategorien, built by tools/kategorien/build.py). Recognition only picks
# from these names, so the data sheet always comes straight from the database. Without the seed folder the list
# is empty and any candidate name is allowed again.
_KATEGORIE_INDEX = config.SEED / 'kategorien' / 'index.json'
KATEGORIE_NAMEN = ([k['name'] for k in json.loads(_KATEGORIE_INDEX.read_text(encoding='utf-8'))]
                   if _KATEGORIE_INDEX.exists() else [])

S = lambda maxlen=200: {'type': 'string', 'maxLength': maxlen}


def obj(props, required=None):
    return {'type': 'object', 'properties': props, 'required': required or list(props), 'additionalProperties': False}


SCAN = obj({
    'ist_gegenstand': {'type': 'boolean'},
    'objekt': S(60),
    'sicherheit': {'type': 'number', 'minimum': 0, 'maximum': 1},
    'kandidaten': {'type': 'array', 'minItems': 1, 'maxItems': 3,
                   'items': obj({'name': {'type': 'string', 'enum': KATEGORIE_NAMEN} if KATEGORIE_NAMEN else S(80),
                                 'sicherheit': {'type': 'number', 'minimum': 0, 'maximum': 1}})},
    'sichtbarer_text': S(200),
    'material_vermutung': {'type': 'array', 'maxItems': 4, 'items': {'type': 'string', 'enum': MATERIAL_IDS}},
})

STECKBRIEF = obj({
    'name': S(60),
    'kategorie': {'type': 'string', 'enum': KATEGORIEN},
    'masse_mm': obj({'breite': {'type': 'number'}, 'tiefe': {'type': 'number'}, 'hoehe': {'type': 'number'}}),
    'gewicht_g': {'type': 'number'},
    'rohstoffwert': S(30), 'gebrauchtwert': S(30), 'co2_kg': S(30),
    'wertvoll': S(400),
    'kreislauf': obj({k: S(120) for k in ['rohstoffe', 'herstellung', 'nutzung', 'heute_oft', 'besser']}),
    'entsorgung': obj({'wo': S(160), 'nicht': S(120), 'warnung': S(160)}),
    'bauteile': {'type': 'array', 'minItems': 3, 'maxItems': 12, 'items': obj({
        'name': S(50), 'kurz': S(16),
        'ebene': {'type': 'integer', 'minimum': 0, 'maximum': 7},
        'form': {'type': 'string', 'enum': ['platte', 'block', 'rund']},
        'breite_anteil': {'type': 'number', 'minimum': 0.05, 'maximum': 1},
        'tiefe_anteil': {'type': 'number', 'minimum': 0.05, 'maximum': 1},
        'dicke_mm': {'type': 'number', 'minimum': 0.2},
        'position': {'type': 'string', 'enum': POSITIONEN},
        'masse_g': {'type': 'number', 'minimum': 0},
        'materialien': {'type': 'array', 'minItems': 1, 'maxItems': 4, 'items': obj({
            'id': {'type': 'string', 'enum': MATERIAL_IDS},
            'anteil': {'type': 'integer', 'minimum': 1, 'maximum': 100}})},
        'info': S(220),
    })},
})


def projekte_schema(inventory_ids):
    return obj({'projekte': {'type': 'array', 'minItems': 3, 'maxItems': 3, 'items': obj({
        'titel': S(50), 'kurz': S(160),
        'stufe': {'type': 'integer', 'minimum': 1, 'maximum': 3},
        'dauer': S(20), 'lernziel': S(140),
        'neu_teil': S(60),
        'lager': {'type': 'array', 'maxItems': 4, 'items': obj({
            'id': {'type': 'string', 'enum': inventory_ids},
            'menge': {'type': 'integer', 'minimum': 1, 'maximum': 50}})},
        'werkzeug': {'type': 'array', 'minItems': 1, 'maxItems': 4, 'items': S(30)},
        'schritte': {'type': 'array', 'minItems': 3, 'maxItems': 4, 'items': S(140)},
    })}})
