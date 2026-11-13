"""3D-Modell: plant_pot. Erzeugt tools/kategorien/modelle/plant_pot.json.

Typischer Kunststoff-Pflanztopf Ø 13 cm aus dünnwandigem PP (tiefgezogen, 40 g), konisch, mit Stapelrand und
Abzugslöchern im Boden. Der Topf ist ein Stück: Rand, Wandabschnitte und Boden bewegen sich gemeinsam, das
Preisetikett wird seitlich gezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

TOPF = '#2E2F31'
teile = [
    teil('rand', 'pp_plant_pot', 'Stapelrand', 'Rand', 'cyl',
         x=0, y=0, w=130, z=112, h=8, mass=6,
         info='Umgebogener Rand, der den dünnen Topf stabil macht. Leere Töpfe stapeln sich ineinander und '
              'lassen sich in der Gärtnerei zurückgeben.',
         color=TOPF, marks=[mark('cyl', 3, 3, 124, fill='#3B3D40'), mark('cyl', 6, 6, 118, fill='#5A4636')]),
    teil('wand_oben', 'pp_plant_pot', 'Topfwand oben', 'Wand', 'cyl',
         x=3, y=3, w=124, z=60, h=52, mass=14,
         info='PP, Recyclingcode 5. Erde ausklopfen, dann in die Gelbe Tonne. Schwarze Töpfe erkennt die '
              'Sortieranlage oft nicht, besser sind graue, braune oder bunte Töpfe.',
         color=TOPF),
    teil('wand_unten', 'pp_plant_pot', 'Topfwand unten', 'Wand', 'cyl',
         x=10, y=10, w=110, z=5, h=55, mass=13, label=False,
         info='Die Wand wird nach unten enger, so rutscht der Wurzelballen beim Umtopfen leicht heraus.',
         color=TOPF),
    teil('boden', 'pp_plant_pot', 'Boden mit Abzugslöchern', 'Boden', 'cyl',
         x=17, y=17, w=96, z=0, h=5, mass=6,
         info='Mehrere Löcher lassen überschüssiges Gießwasser ablaufen, damit die Wurzeln nicht faulen.',
         color=TOPF, marks=[mark('cyl', 43, 43, 10, fill='#151617'), mark('cyl', 20, 43, 8, fill='#151617'),
                            mark('cyl', 68, 43, 8, fill='#151617'), mark('cyl', 44, 20, 8, fill='#151617'),
                            mark('cyl', 44, 68, 8, fill='#151617')]),
    teil('etikett', 'pp_plant_pot', 'Preisetikett', 'Etikett', 'box',
         material_id='paper', x=127, y=50, w=0.3, d=30, z=70, h=25, r=0, explode=[40, 0, 0], mass=0.3,
         materials=[['papier', 80], ['druck', 8], ['klebstoff', 12]],
         info='Aufkleber aus Papier. Darf dranbleiben, er stört das Recycling kaum.',
         color='#F4E04D', sortBias=100),
]
explodiere(teile, abstand=30, gruppen=[['rand', 'wand_oben', 'wand_unten', 'boden']])
skaliere_masse(teile, oid='plant_pot')
schreibe('plant_pot', teile)
