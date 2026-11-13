"""3D-Modell: yoga_mat. Erzeugt tools/kategorien/modelle/yoga_mat.json.

Yogamatte 183 × 61 cm, 6 mm dick, aufgerollt und hochkant: Rolle Ø 150 mm, 610 mm hoch, ca. 1 kg.
Die Rolle ist ein Zylinder, die Wicklung ist als Spirale auf der Stirnseite markiert. Dazu ein Tragegurt aus
Polyester mit zwei Schlaufen. Explodiert: Gurt und Schlaufen seitlich abgenommen, Rolle steht.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

MATTE, MATTE_D, MATTE_H = '#7A9E8E', '#5F8273', '#93B6A6'
GURT = '#3B4250'

wicklung = []
for i, dm in enumerate(range(150, 20, -12)):
    o = (150 - dm) / 2
    wicklung.append(mark('cyl', o, o, dm, fill=MATTE_D if i % 2 else MATTE_H))
wicklung.append(mark('cyl', 66, 66, 18, fill='#2E3530'))

teile = [
    teil('gurt', 'foam_mat', 'Tragegurt', 'Tragegurt', 'box',
         material_id='polyester', x=150, y=60, w=3, d=30, z=120, h=395, r=1, mass=20,
         materials=[['polyester', 100]], color=GURT, explode=[230, 0, 0],
         info='Gewebtes Polyesterband zum Umhängen. Es wird nur abgestreift und kann weiterbenutzt werden.'),
    teil('schlaufe_oben', 'foam_mat', 'Gurtschlaufe oben', 'Schlaufe', 'cyl',
         material_id='polyester', x=-3, y=-3, w=156, z=470, h=25, mass=10,
         materials=[['polyester', 85], ['pp', 15]], color=GURT, explode=[190, 0, 30],
         info='Schlaufe mit Kunststoff-Schiebeschnalle, die die Rolle zusammenhält.',
         marks=[mark('cyl', 3, 3, 150, fill=MATTE)]),
    teil('matte', 'foam_mat', 'Matte, aufgerollt', 'Matte', 'cyl',
         x=0, y=0, w=150, z=0, h=610, mass=960, color=MATTE,
         info='Geschäumter Kunststoff (EVA oder TPE) mit rutschfester Struktur. Nicht recycelbar: lieber in Stücke '
              'schneiden und als Knieschoner oder Schubladeneinlage weiternutzen, sonst Restmüll.',
         marks=wicklung),
    teil('schlaufe_unten', 'foam_mat', 'Gurtschlaufe unten', 'Schlaufe', 'cyl',
         material_id='polyester', x=-3, y=-3, w=156, z=110, h=25, mass=10,
         materials=[['polyester', 85], ['pp', 15]], color=GURT, explode=[190, 0, -30], label=False,
         info='Zweite Schlaufe am anderen Ende der Rolle.',
         marks=[mark('cyl', 3, 3, 150, fill=MATTE)]),
]
explodiere(teile, abstand=20, fest=('matte',))
skaliere_masse(teile, oid='yoga_mat')
schreibe('yoga_mat', teile)
