"""3D-Modell: toothpaste_tube. Erzeugt tools/kategorien/modelle/toothpaste_tube.json.

Typische 75-ml-Zahnpastatube, liegend (Deckel hinten bei y = 0): ovaler Klappdeckel, angeschweißter Tubenkopf
mit Schulter und Gewinde, Tubenschlauch aus Mehrschichtlaminat, der zur flach gepressten Endnaht hin flacher wird.
Deckel und Kopf werden nach hinten abgezogen, der Schlauch bleibt liegen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

DECKEL = '#F4F4F2'
TUBE = '#FFFFFF'
LAMINAT = [['verbundfolie', 90], ['alu', 7], ['druck', 3]]  # PE-Laminat, oft mit Aluminium-Sperrschicht
teile = [
    teil('klappdeckel', 'pp_flip_cap', 'Klappdeckel', 'Klappdeckel', 'box',
         x=4.5, y=0, w=36, d=18, z=0, h=30, r=8, explode=[0, -65, 0], mass=2.6,
         info='PP-Klappdeckel, auf den Tubenkopf geschraubt. Darauf kann die Tube stehen. Er darf an der Tube '
              'bleiben, beides kommt in die Gelbe Tonne.',
         color=DECKEL, marks=[mark('box', 4, 13, 28, 3, 1.5, '#D9D9D4'), mark('box', 12, 2, 12, 4, 2, '#D9D9D4')]),
    teil('tubenkopf', 'toothpaste_tube_body', 'Tubenkopf mit Schulter und Gewinde', 'Tubenkopf', 'box',
         material_id='hdpe', x=6.5, y=18, w=32, d=14, z=2, h=26, r=10, explode=[0, -30, 0], mass=1.6,
         materials=[['hdpe', 100]],
         info='Gespritzter Kopf aus HDPE mit der kleinen Austrittsöffnung, an den Schlauch angeschweißt. '
              'Er lässt sich nicht abtrennen.',
         color='#E9E9E4', marks=[mark('cyl', 11, 2, 10, 10, fill='#D0D0CA')]),
    teil('schlauch_vorn', 'toothpaste_tube_body', 'Tubenschlauch (rund)', 'Schlauch', 'box',
         x=3, y=32, w=39, d=60, z=2, h=26, r=12, mass=2.0, materials=LAMINAT,
         info='Mehrschichtfolie aus Polyethylen, oft mit einer dünnen Aluminiumschicht gegen Austrocknen. '
              'Leer drücken reicht, ausspülen ist nicht nötig.',
         color=TUBE, marks=[mark('box', 4, 6, 31, 22, 4, '#2F6DB5'), mark('box', 4, 34, 31, 10, 3, '#C8423A')]),
    teil('schlauch_mitte', 'toothpaste_tube_body', 'Tubenschlauch (flacher)', 'Schlauch Mitte', 'box',
         x=1.5, y=92, w=42, d=58, z=6, h=18, r=10, mass=1.8, materials=LAMINAT, label=False,
         info='Zum Ende hin wird der Schlauch flacher. Von hinten nach vorne aufrollen, dann kommt auch der Rest heraus.',
         color=TUBE, marks=[mark('box', 4, 6, 34, 40, 6, '#2F6DB5'), mark('box', 6, 50, 30, 4, 1, '#8E969A')]),
    teil('schlauch_ende', 'toothpaste_tube_body', 'Tubenschlauch (flach)', 'Schlauch Ende', 'box',
         x=0.5, y=150, w=44, d=27, z=10, h=10, r=6, mass=0.8, materials=LAMINAT, label=False,
         info='Fast flach gedrückt. Die Farbstreifen dienen der Maschine als Markierung zum Abfüllen.',
         color=TUBE, marks=[mark('box', 4, 4, 36, 14, 4, '#2F6DB5'), mark('box', 36, 20, 5, 5, 0, '#22272B')]),
    teil('endnaht', 'toothpaste_tube_body', 'Gepresste Endnaht', 'Endnaht', 'box',
         x=0, y=177, w=45, d=13, z=14, h=2, r=0, mass=0.6, materials=LAMINAT,
         info='Nach dem Befüllen von hinten heiß zusammengepresst. Darin ist das Herstelldatum geprägt.',
         color='#ECECE8', marks=[mark('box', 2, 2, 41, 1, 0, '#C9C9C2'), mark('box', 2, 5, 41, 1, 0, '#C9C9C2'),
                                 mark('box', 2, 8, 41, 1, 0, '#C9C9C2')]),
]
explodiere(teile, abstand=10, fest=('schlauch_vorn', 'schlauch_mitte', 'schlauch_ende', 'endnaht'))
skaliere_masse(teile, oid='toothpaste_tube')
schreibe('toothpaste_tube', teile)
