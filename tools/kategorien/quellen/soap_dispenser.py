"""3D-Modell: soap_dispenser. Erzeugt tools/kategorien/modelle/soap_dispenser.json.

Typischer 300-ml-Flüssigseifenspender: ovale HDPE-Flasche (60 × 48 mm) mit PP-Pumpe aus Pumpkopf und
Auslauf, Kolbenschaft, Stahlfeder, Pumpenzylinder mit Kugelventil, Verschlussring und Steigrohr.
Die Flasche bleibt stehen, die Pumpenteile stapeln darüber, Steigrohr und Etikett werden seitlich gezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

FLASCHE = '#F5F1E8'
PUMPE = '#FFFFFF'
teile = [
    teil('pumpkopf', 'pump_dispenser', 'Pumpkopf', 'Pumpkopf', 'cyl',
         x=17, y=12, w=26, z=152, h=28, mass=4,
         info='Darauf drückt man mit der Hand. Zum Entsorgen die ganze Pumpe abschrauben: Sie enthält eine '
              'Stahlfeder und kommt als Ganzes in die Gelbe Tonne.',
         color=PUMPE, marks=[mark('cyl', 3, 3, 20, fill='#ECECE8')]),
    teil('auslauf', 'pump_dispenser', 'Auslauf', 'Auslauf', 'box',
         x=43, y=21, w=27, d=8, z=168, h=8, r=3, mass=1,
         info='Rohr, aus dem die Seife kommt. Zum Verriegeln für den Transport dreht man den Kopf.',
         color=PUMPE, marks=[mark('cyl', 21, 2, 4, fill='#2A2E31')]),
    teil('schaft', 'pump_dispenser', 'Kolbenschaft', 'Schaft', 'cyl',
         x=26.5, y=21.5, w=7, z=136, h=16, mass=1,
         info='Hohler Schaft mit Kolben am unteren Ende. Durch ihn steigt die Seife in den Kopf.',
         color='#E6E9EC', marks=[mark('cyl', 2, 2, 3, fill='#2A2E31')]),
    teil('feder', 'pump_dispenser', 'Rückstellfeder', 'Feder', 'cyl',
         material_id='steel', x=25, y=20, w=10, z=100, h=30, mass=0.8, materials=[['stahl', 100]],
         info='Edelstahlfeder, die den Pumpkopf nach dem Drücken wieder hochschiebt. Sie bleibt in der Pumpe, '
              'Sortieranlagen holen das Metall später heraus.',
         color='#9DA4AA', marks=[mark('cyl', 2.5, 2.5, 5, fill='#6E757B')]),
    teil('zylinder', 'pump_dispenser', 'Pumpenzylinder mit Kugelventil', 'Zylinder', 'cyl',
         x=23, y=18, w=14, z=85, h=52, mass=2.5, materials=[['pp', 85], ['stahl', 10], ['ldpe', 5]],
         info='Hier saugt der Kolben die Seife an. Eine kleine Kugel unten wirkt als Ventil, damit nichts '
              'zurückläuft.',
         color='#ECECE8', marks=[mark('cyl', 3, 3, 8, fill='#C9CED3')]),
    teil('verschlussring', 'pump_dispenser', 'Verschlussring', 'Verschluss', 'cyl',
         x=15, y=10, w=30, z=127, h=14, mass=3,
         info='Schraubring mit Gewinde, der die Pumpe auf der Flasche hält.',
         color=PUMPE, marks=[mark('cyl', 7, 7, 16, fill='#E2E2DC')]),
    teil('hals', 'hdpe_bottle_body', 'Flaschenhals mit Gewinde', 'Hals', 'cyl',
         x=17, y=12, w=26, z=125, h=14, mass=2.5,
         info='Gewindehals für die Pumpe. Darum lässt sich der Spender auch nachfüllen.',
         color=FLASCHE, marks=[mark('cyl', 4, 4, 18, fill='#DCD7CB')]),
    teil('schulter', 'hdpe_bottle_body', 'Flaschenschulter', 'Schulter', 'cyl',
         x=10, y=7, w=40, d=36, z=115, h=10, mass=3,
         info='Übergang vom ovalen Körper zum Hals.', color=FLASCHE, label=False),
    teil('rumpf', 'hdpe_bottle_body', 'Flaschenkörper', 'Flasche', 'cyl',
         x=0, y=1, w=60, d=48, z=5, h=110, mass=18,
         info='HDPE, Recyclingcode 2. Leer machen, kurz ausspülen und mit Pumpe in die Gelbe Tonne. '
              'Besser: nachfüllen statt neu kaufen.',
         color=FLASCHE),
    teil('boden', 'hdpe_bottle_body', 'Flaschenboden', 'Boden', 'cyl',
         x=3, y=3, w=54, d=44, z=0, h=5, mass=3,
         info='Standboden mit Recyclingzeichen.', color=FLASCHE, label=False),
    teil('steigrohr', 'pump_dispenser', 'Steigrohr', 'Steigrohr', 'cyl',
         material_id='ldpe', x=28, y=23, w=4, z=6, h=80, explode=[50, 0, 0], mass=0.6, materials=[['ldpe', 100]],
         info='Schlauch bis zum Boden, durch den die Pumpe die Seife ansaugt. Steckt unten am Zylinder.',
         color='#EDEDE8'),
    teil('etikett', 'plastic_label', 'Etikett', 'Etikett', 'box',
         x=60, y=10, w=0.3, d=30, z=20, h=80, r=0, explode=[60, 0, 0], mass=1,
         materials=[['pp', 92], ['druck', 5], ['klebstoff', 3]],
         info='Bedruckte PP-Folie. Passt zum Kunststoffrecycling und darf dranbleiben.',
         color='#C98BB9', sortBias=100),
]
explodiere(teile, abstand=15, nach_liste=True,
           gruppen=[['pumpkopf', 'auslauf'], ['hals', 'schulter', 'rumpf', 'boden']])
skaliere_masse(teile, oid='soap_dispenser')
schreibe('soap_dispenser', teile)
