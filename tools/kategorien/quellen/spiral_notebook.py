"""3D-Modell: spiral_notebook. Erzeugt tools/kategorien/modelle/spiral_notebook.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# A4-Spiralblock (Collegeblock) flach auf dem Tisch, Spirale links (x = 0). 210 × 297 × 10 mm laut CSV.
# Rückpappe, Papierblock mit Lochrand, bedruckter Kartondeckel; die Drahtspirale wird nach links herausgezogen,
# die Lagen schweben übereinander.
PAPIER = '#F7F5F0'
LINIE = '#B9CBE0'


def lochung(fill):
    """Vierfach-Abheftlochung (Lochabstand 80 mm) neben der Perforation."""
    return [mark('cyl', 16, 148.5 + k * 40 - 3, 6, fill=fill) for k in (-3, -1, 1, 3)]


teile = [
    teil('deckel', 'cardboard_cover', 'Deckblatt (Karton)', 'Deckblatt', 'box',
         x=6, y=0, w=204, d=297, z=8.1, h=0.4, r=2, mass=19, materials=[['papier', 95], ['druck', 5]],
         info='Bedruckter Karton als Schutzumschlag. Ins Altpapier, wenn er nicht mit Folie beschichtet ist.',
         color='#3E8E7E', marks=[mark('box', 40, 60, 130, 40, 3, '#F3F1EC'), mark('box', 50, 72, 90, 3, 0, '#9AA3A8'),
                                         mark('box', 50, 84, 70, 3, 0, '#9AA3A8'), mark('box', 40, 250, 130, 14, 3, '#2F7062')]
         + raster(2, 4, 1, 36, 3, 3, 0, 8, 'cyl', fill='#E8EEF0') + lochung('#E8EEF0')),
    teil('papier', 'paper_sheets', 'Papierblock (50 Blatt)', 'Papier', 'box',
         x=6, y=0, w=204, d=297, z=2.5, h=5.6, r=1, mass=190, materials=[['papier', 98], ['druck', 2]],
         info='50 linierte Blätter, am Rand gelocht und perforiert. Beschriebenes Papier gehört ins Altpapier.',
         color=PAPIER, marks=raster(2, 4, 1, 36, 3, 3, 0, 8, 'cyl', fill='#C9CDD0')
         + [mark('box', 10, 0, 0.6, 297, 0, '#D8D4CA'), mark('box', 30, 15, 1, 275, 0, '#E3A5A0')]
         + [mark('box', 30, 25 + 8.5 * i, 165, 0.6, 0, LINIE) for i in range(31)] + lochung('#C9CDD0')),
    teil('rueckpappe', 'cardboard_cover', 'Rückpappe', 'Rückpappe', 'box',
         x=6, y=0, w=204, d=297, z=1.5, h=1, r=2, mass=30,
         info='Steife Graupappe als Schreibunterlage. Reine Pappe aus Altpapier.',
         color='#8C8A84', marks=raster(2, 4, 1, 36, 3, 3, 0, 8, 'cyl', fill='#6E6C66') + lochung('#6E6C66')),
    teil('spirale', 'steel_spiral', 'Drahtspirale', 'Spirale', 'box',
         x=0, y=2, w=12, d=293, z=0, h=10, r=3, explode=[-170, 0, 0], mass=9,
         info='Lackierter Stahldraht, durch die Löcher gefädelt. Ein Ende aufbiegen und herausdrehen, '
              'dann darf der Block ins Altpapier und der Draht zum Metall.',
         color='#8E969A', marks=raster(1, 1.5, 1, 36, 10, 1.2, 0, 8, r=0.6, fill='#5A6268')),
]

explodiere(teile, abstand=100)
skaliere_masse(teile, oid='spiral_notebook')
schreibe('spiral_notebook', teile)
