"""3D-Modell: squeeze_bottle. Erzeugt tools/kategorien/modelle/squeeze_bottle.json.

Typische 250-ml-Quetschflasche für Ketchup oder Senf: ovaler PP-Körper (60 × 45 mm), PP-Klappdeckel aus
Unterteil und Klappe mit Silikon-Dosierventil, PP-Etiketten. Flaschenabschnitte bewegen sich gemeinsam,
Ventil und Deckelteile stapeln über dem Hals, die Etiketten werden seitlich abgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

FLASCHE = '#E9E2D8'
DECKEL = '#C8302C'
teile = [
    teil('klappe', 'pp_flip_cap', 'Deckelklappe', 'Klappe', 'cyl',
         x=14, y=6.5, w=32, z=170, h=10, mass=2,
         info='Klappe mit Filmscharnier, ein kleiner Stöpsel innen verschließt die Öffnung.',
         color=DECKEL, marks=[mark('box', 10, 0, 12, 3, 1.5, '#A82623'), mark('cyl', 4, 4, 24, fill='#D43A35')]),
    teil('ventil', 'pp_flip_cap', 'Silikon-Dosierventil', 'Ventil', 'cyl',
         material_id='silicone', x=21, y=13.5, w=18, z=164, h=2, mass=0.5,
         info='Weiche Membran mit Kreuzschlitz: Sie öffnet sich nur beim Drücken, danach tropft nichts nach. '
              'Bleibt im Deckel.',
         color='#E4E0D2', marks=[mark('box', 8.5, 4, 1, 10, 0, '#8A8478'), mark('box', 4, 8.5, 10, 1, 0, '#8A8478')]),
    teil('deckel_unterteil', 'pp_flip_cap', 'Deckel-Unterteil', 'Unterteil', 'cyl',
         x=14, y=6.5, w=32, z=152, h=18, mass=4,
         info='Wird auf den Hals geschraubt. Der Deckel darf zum Entsorgen auf der Flasche bleiben.',
         color=DECKEL, marks=[mark('cyl', 8, 8, 16, fill='#A82623'), mark('cyl', 13, 13, 6, fill='#1F2A33')]),
    teil('siegel', 'squeeze_bottle_body', 'Siegelfolie', 'Siegelfolie', 'cyl',
         material_id='aluminium', x=19, y=11.5, w=22, z=164, h=0.4, mass=0.2,
         materials=[['alu', 60], ['pet', 25], ['klebstoff', 15]], color='#D5D9DD', sortBias=-8,
         info='Aufgesiegelte Folie unter dem Deckel, die die Flasche bis zum ersten Öffnen dicht hält. Abziehen '
              'und in die Gelbe Tonne.',
         marks=[mark('cyl', 3, 3, 16, fill='#C3C8CD'), mark('box', 15.5, 9, 5, 4, 1, '#AEB4BA')]),
    teil('hals', 'squeeze_bottle_body', 'Flaschenhals mit Gewinde', 'Hals', 'cyl',
         x=17, y=9.5, w=26, z=150, h=14, mass=1.5,
         info='Kurzer Gewindehals. Unter dem Deckel klebt beim Kauf oft eine Siegelfolie.',
         color=FLASCHE, marks=[mark('cyl', 4, 4, 18, fill='#CFC6B8')]),
    teil('schulter', 'squeeze_bottle_body', 'Flaschenschulter', 'Schulter', 'cyl',
         x=8, y=6, w=44, d=33, z=140, h=10, mass=2,
         info='Übergang vom ovalen Körper zum runden Hals.', color=FLASCHE, label=False),
    teil('rumpf_oben', 'squeeze_bottle_body', 'Flaschenkörper oben', 'Flasche', 'cyl',
         x=0, y=0, w=60, d=45, z=120, h=20, mass=2.5, label=False,
         info='Oberer Teil des Körpers über dem Etikett.', color=FLASCHE),
    teil('etikett', 'plastic_label', 'Etiketten vorne und hinten', 'Etikett', 'cyl',
         x=-0.4, y=-0.4, w=60.8, d=45.8, z=28, h=92, explode=[80, 0, 0], mass=1.8, sortBias=1,
         materials=[['pp', 92], ['druck', 5], ['klebstoff', 3]], color=DECKEL,
         info='Bedruckte PP-Folie mit Name, Zutaten und Nährwerten. Gleicher Kunststoff wie die Flasche, darf '
              'also dranbleiben.',
         marks=[mark('cyl', 0.4, 0.4, 60, 45, fill=FLASCHE)]),
    teil('rumpf', 'squeeze_bottle_body', 'Flaschenkörper', 'Flasche', 'cyl',
         x=0, y=0, w=60, d=45, z=6, h=114, mass=12.5,
         info='Weiches PP, damit man sie gut drücken kann. Reste mit einem Löffelstiel herauskratzen, '
              'ausspülen ist nicht nötig. Mit Deckel in die Gelbe Tonne.',
         color=FLASCHE),
    teil('boden', 'squeeze_bottle_body', 'Flaschenboden', 'Boden', 'cyl',
         x=3, y=2, w=54, d=41, z=0, h=6, mass=2.5,
         info='Standboden mit Recyclingzeichen 5 für PP.', color=FLASCHE, label=False),
]
explodiere(teile, abstand=14, nach_liste=True, gruppen=[['hals', 'schulter', 'rumpf_oben', 'rumpf', 'boden']])
skaliere_masse(teile, oid='squeeze_bottle')
schreibe('squeeze_bottle', teile)
