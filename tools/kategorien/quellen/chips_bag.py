"""3D-Modell: chips_bag. Erzeugt tools/kategorien/modelle/chips_bag.json.

Typische 150-g-Chipstüte als Schlauchbeutel, flach hingelegt (20 × 28 cm, prall mit Schutzgas ca. 3 cm hoch):
bedruckte Vorderseite, Rückseite mit Längsnaht, gezackte Kopf- und Bodennaht. Die Vorderseite hebt mit den
Quernähten nach oben ab, die Längsnaht wird seitlich herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

DRUCK = '#D8342C'
SILBER = '#C9CDD0'
FOLIE = [['verbundfolie', 97], ['druck', 2], ['alu', 1]]  # OPP/PP-Verbund, mit Aluminium bedampft
teile = [
    teil('kopfnaht', 'multilayer_film', 'Kopfnaht (Aufreißkante)', 'Kopfnaht', 'box',
         x=0, y=0, w=200, d=15, z=14, h=2, r=0, mass=0.6, materials=FOLIE,
         info='Beide Folienlagen sind hier heiß verschweißt. Die Zacken helfen beim Aufreißen.',
         color=DRUCK, marks=raster(2, 2, 25, 1, 4, 11, 8, fill='#A82822')),
    teil('vorderseite', 'multilayer_film', 'Vorderseite (bedruckt)', 'Vorderseite', 'box',
         x=0, y=15, w=200, d=250, z=15, h=15, r=20, mass=3.0, materials=FOLIE,
         info='Mehrschichtfolie aus Polypropylen, innen hauchdünn mit Aluminium bedampft. Die Schichten lassen sich '
              'nicht trennen. Tüte ausschütteln und in die Gelbe Tonne geben.',
         color=DRUCK, marks=[mark('cyl', 30, 50, 140, 110, fill='#E3B23C'), mark('box', 25, 175, 150, 26, 6, '#FFFFFF'),
                             mark('box', 60, 212, 80, 14, 4, '#7A1B17')]),
    teil('bodennaht', 'multilayer_film', 'Bodennaht', 'Bodennaht', 'box',
         x=0, y=265, w=200, d=15, z=14, h=2, r=0, mass=0.6, materials=FOLIE,
         info='Zweite Quernaht. Sie wird erst verschweißt, wenn Chips und Stickstoff in der Tüte sind.',
         color=DRUCK, marks=raster(2, 2, 25, 1, 4, 11, 8, fill='#A82822')),
    teil('rueckseite', 'multilayer_film', 'Rückseite (innen silbern)', 'Rückseite', 'box',
         x=0, y=15, w=200, d=250, z=1, h=14, r=20, mass=2.6, materials=FOLIE,
         info='Die silberne Innenseite ist eine Aluminiumschicht von etwa 0,00004 mm. Sie hält Licht und '
              'Sauerstoff ab, damit die Chips nicht ranzig werden.',
         color=SILBER, marks=[mark('box', 10, 10, 180, 230, 16, '#DDE0E2'), mark('box', 20, 200, 160, 30, 4, '#8E969A')]),
    teil('laengsnaht', 'multilayer_film', 'Längsnaht (Flossennaht)', 'Längsnaht', 'box',
         x=92, y=15, w=16, d=250, z=0, h=1, r=0, explode=[140, 0, 0], mass=0.5, materials=FOLIE,
         info='Hier wurde die Folie zum Schlauch geschlossen und flach umgelegt. Sie liegt auf der Rückseite.',
         color=SILBER, marks=[mark('box', 3, 0, 10, 250, 0, '#AEB3B7')]),
]
explodiere(teile, abstand=90, gruppen=[['kopfnaht', 'vorderseite', 'bodennaht']])
skaliere_masse(teile, oid='chips_bag')
schreibe('chips_bag', teile)
