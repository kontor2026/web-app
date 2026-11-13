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
         color=TOPF, marks=[mark('cyl', 3, 3, 124, fill='#3B3D40'), mark('cyl', 6, 6, 118, fill='#1C1D1F'),
                            # Blick ins Innere: Boden mit Abzugslöchern und Stapelnocken
                            mark('cyl', 20, 26, 90, 86, fill='#252628'),
                            mark('cyl', 60, 64, 10, fill='#0E0F10'), mark('cyl', 38, 64, 8, fill='#0E0F10'),
                            mark('cyl', 84, 64, 8, fill='#0E0F10'), mark('cyl', 61, 42, 8, fill='#0E0F10'),
                            mark('cyl', 61, 86, 8, fill='#0E0F10'),
                            *[mark('box', x0, y0, 5, 5, 1.5, '#3B3D40') for x0, y0 in ((62, 9), (62, 116), (9, 62), (116, 62))]]),
    teil('wand0', 'pp_plant_pot', 'Topfwand', 'Wand', 'cyl',
         x=3, y=3, w=124, z=92, h=20, mass=5.5, label=True,
         info='PP, Recyclingcode 5. Erde ausklopfen, dann in die Gelbe Tonne. Die Wand wird nach unten enger, so '
              'rutscht der Wurzelballen leicht heraus.',
         color=TOPF),
    teil('wand1', 'pp_plant_pot', 'Topfwand', 'Wand', 'cyl',
         x=6, y=6, w=118, z=72, h=20, mass=5.5, label=False,
         info='PP, Recyclingcode 5. Erde ausklopfen, dann in die Gelbe Tonne. Die Wand wird nach unten enger, so '
              'rutscht der Wurzelballen leicht heraus.',
         color=TOPF),
    teil('wand2', 'pp_plant_pot', 'Topfwand', 'Wand', 'cyl',
         x=9, y=9, w=112, z=52, h=20, mass=5.5, label=False,
         info='PP, Recyclingcode 5. Erde ausklopfen, dann in die Gelbe Tonne. Die Wand wird nach unten enger, so '
              'rutscht der Wurzelballen leicht heraus.',
         color=TOPF),
    teil('wand3', 'pp_plant_pot', 'Topfwand', 'Wand', 'cyl',
         x=12, y=12, w=106, z=32, h=20, mass=5.5, label=False,
         info='PP, Recyclingcode 5. Erde ausklopfen, dann in die Gelbe Tonne. Die Wand wird nach unten enger, so '
              'rutscht der Wurzelballen leicht heraus.',
         color=TOPF),
    teil('wand4', 'pp_plant_pot', 'Topfwand', 'Wand', 'cyl',
         x=15, y=15, w=100, z=5, h=27, mass=5.5, label=False,
         info='PP, Recyclingcode 5. Erde ausklopfen, dann in die Gelbe Tonne. Die Wand wird nach unten enger, so '
              'rutscht der Wurzelballen leicht heraus.',
         color=TOPF),
    teil('boden', 'pp_plant_pot', 'Boden mit Abzugslöchern', 'Boden', 'cyl',
         x=17, y=17, w=96, z=0, h=5, mass=6, label=False,
         info='Mehrere Löcher lassen überschüssiges Gießwasser ablaufen, damit die Wurzeln nicht faulen. Schwarze '
              'Töpfe erkennt die Sortieranlage oft nicht, besser sind graue, braune oder bunte.',
         color=TOPF),
    teil('etikett', 'pp_plant_pot', 'Preisetikett', 'Etikett', 'box',
         material_id='paper', x=124, y=53, w=0.3, d=24, z=60, h=22, r=0, explode=[40, 0, 0], mass=0.3,
         materials=[['papier', 80], ['druck', 8], ['klebstoff', 12]],
         info='Aufkleber aus Papier. Darf dranbleiben, er stört das Recycling kaum.',
         color='#F4E04D', sortBias=100,
         marks=[mark('box', 0, 3, 0.3, 18, 0, '#3A3F44')]),
]
explodiere(teile, abstand=30, gruppen=[['rand', 'wand0', 'wand1', 'wand2', 'wand3', 'wand4', 'boden']])
skaliere_masse(teile, oid='plant_pot')
schreibe('plant_pot', teile)
