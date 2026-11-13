"""3D-Modell: pill_bottle. Erzeugt tools/kategorien/modelle/pill_bottle.json.

Typische Tablettendose aus HDPE (etwa 60 ml, Ø 38 mm) mit zweiteiligem kindersicherem Deckel (Außen- und
Innenkappe), Siegelscheibe auf dem Hals und Papieretikett. Flaschenabschnitte bewegen sich gemeinsam,
Siegel und Deckelteile stapeln darüber, das Etikett wird seitlich abgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

DOSE = '#F4F2EC'
DECKEL = '#E9E7E0'
teile = [
    teil('kappe_aussen', 'child_safe_cap', 'Außenkappe (Kindersicherung)', 'Außenkappe', 'cyl',
         x=0, y=0, w=40, z=52, h=18, mass=3.2,
         info='Die Außenkappe dreht sich frei, bis man sie herunterdrückt. Erst dann greifen Zähne in die Innenkappe: '
              'Drücken und gleichzeitig drehen.',
         color=DECKEL, marks=[mark('cyl', 4, 4, 32, fill='#DCDAD2'), mark('box', 17, 8, 6, 16, 2, '#8A9096')]),
    teil('kappe_innen', 'child_safe_cap', 'Innenkappe mit Gewinde', 'Innenkappe', 'cyl',
         x=3, y=3, w=34, z=54, h=15.5, mass=1.6,
         info='Trägt das Gewinde und die Zähne, in die die Außenkappe beim Drücken einrastet. '
              'Beide Kappen sind aus PP und bleiben zusammen.',
         color='#FFFFFF', marks=[mark('cyl', 3, 3, 28, fill='#EFEFEA')] + raster(6, 15.5, 7, 1, 1.6, 3, 3.6, fill='#C8C6BE')),
    teil('siegel', 'child_safe_cap', 'Siegelscheibe', 'Siegel', 'cyl',
         material_id='aluminium', x=7, y=7, w=26, z=67, h=0.4, mass=0.2,
         materials=[['alu', 40], ['ldpe', 35], ['papier', 25]],
         info='Aluminium-Kunststoff-Folie, die beim Abfüllen auf den Hals gesiegelt wird. Zeigt, dass die Dose noch '
              'nicht geöffnet war. Abziehen und in die Gelbe Tonne.',
         color='#C9CED3'),
    teil('hals', 'hdpe_bottle_body', 'Hals mit Gewinde', 'Hals', 'cyl',
         x=6.5, y=6.5, w=27, z=53, h=14, mass=0.8,
         info='Weite Öffnung, damit man die Tabletten gut herausschütten kann.',
         color=DOSE, marks=[mark('cyl', 3, 3, 21, fill='#D6D3CA')]),
    teil('schulter', 'hdpe_bottle_body', 'Schulter', 'Schulter', 'cyl',
         x=4, y=4, w=32, z=48, h=5, mass=0.6, info='Übergang vom Rumpf zum Hals.', color=DOSE, label=False),
    teil('rumpf', 'hdpe_bottle_body', 'Dosenrumpf', 'Dose', 'cyl',
         x=1, y=1, w=38, z=3, h=45, mass=3.5,
         info='Weißes HDPE schützt die Tabletten vor Licht und Feuchtigkeit. Leer mit Deckel in die Gelbe Tonne, '
              'Medikamentenreste gehören nicht hinein.',
         color=DOSE),
    teil('boden', 'hdpe_bottle_body', 'Boden', 'Boden', 'cyl',
         x=2, y=2, w=36, z=0, h=3, mass=0.8,
         info='Am Boden steht das Recyclingzeichen 2 für HDPE.', color=DOSE, label=False),
    teil('etikett', 'paper_label', 'Papieretikett', 'Etikett', 'cyl',
         x=0.5, y=0.5, w=39, z=8, h=40, explode=[58, 0, 0], mass=0.3,
         materials=[['papier', 92], ['druck', 5], ['klebstoff', 3]],
         info='Papier mit Name, Dosierung und Haltbarkeit, rundum geklebt. Darf beim Recycling dranbleiben.',
         color='#CFE0EE', sortBias=1, marks=[mark('cyl', 0.8, 0.8, 37.4, fill=DOSE)]),
]
explodiere(teile, abstand=16, nach_liste=True, gruppen=[['hals', 'schulter', 'rumpf', 'boden']])
skaliere_masse(teile, oid='pill_bottle')
schreibe('pill_bottle', teile)
