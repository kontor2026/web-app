"""3D-Modell: pizza_box. Erzeugt tools/kategorien/modelle/pizza_box.json.

Typischer Pizzakarton 33 × 33 × 4 cm aus brauner Wellpappe, aus einem Zuschnitt gefaltet: Boden, doppelt gelegte
Seitenwände, Rückwand mit Deckelscharnier, Vorderwand mit eingesteckter Deckellasche, bedruckter Deckel.
Deckel hebt nach oben ab, die Wände klappen nach außen weg.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

PAPPE = '#C49A6C'
WELLE = [['papier', 100]]
teile = [
    teil('deckel', 'cardboard_box_body', 'Deckel', 'Deckel', 'box',
         x=0, y=0, w=330, d=330, z=37, h=3, r=2, explode=[0, 0, 150], mass=62,
         materials=[['papier', 98], ['druck', 2]],
         info='Bedruckte Wellpappe. Ist der Deckel sauber, kommt er ins Altpapier. Meist kann man ihn an der '
              'Knickkante abreißen, wenn der Boden fettig ist.',
         color=PAPPE, marks=[mark('cyl', 95, 70, 140, fill='#B3423A'), mark('cyl', 115, 90, 100, fill='#C49A6C'),
                             mark('box', 85, 240, 160, 18, 4, '#3A3F44'), mark('box', 115, 268, 100, 10, 3, '#3A3F44')]
                            + raster(20, 20, 2, 1, 8, 8, 282, shape='cyl', fill='#9E7A52')),
    teil('wand_hinten', 'cardboard_box_body', 'Rückwand mit Deckelscharnier', 'Rückwand', 'box',
         x=4, y=0, w=322, d=4, z=3, h=34, r=0, explode=[0, -70, 0], mass=12, materials=WELLE,
         info='Hier ist der Deckel nur eingeknickt, nicht geklebt. Pizzakartons kommen ganz ohne Klebstoff aus.',
         color=PAPPE),
    teil('wand_links', 'cardboard_box_body', 'Seitenwand links (doppelt gelegt)', 'Seitenwand', 'box',
         x=0, y=0, w=4, d=330, z=3, h=34, r=0, explode=[-70, 0, 0], mass=24, materials=WELLE,
         info='Die Seitenwand ist doppelt gefaltet und mit Laschen im Boden verriegelt. Das macht den Karton stapelbar.',
         color=PAPPE, marks=[mark('box', 1.5, 0, 1, 330, 0, '#9E7A52')]),
    teil('wand_rechts', 'cardboard_box_body', 'Seitenwand rechts (doppelt gelegt)', 'Seitenwand', 'box',
         x=326, y=0, w=4, d=330, z=3, h=34, r=0, explode=[70, 0, 0], mass=24, materials=WELLE, label=False,
         info='Gegenstück zur linken Seitenwand.',
         color=PAPPE, marks=[mark('box', 1.5, 0, 1, 330, 0, '#9E7A52')]),
    teil('wand_vorne', 'cardboard_box_body', 'Vorderwand mit Einstecklasche', 'Vorderwand', 'box',
         x=4, y=326, w=322, d=4, z=3, h=34, r=0, explode=[0, 70, 0], mass=20, materials=WELLE,
         info='Doppelte Wand, in die die Lasche des Deckels gesteckt wird. Zum Flachmachen alle Wände aufklappen.',
         color=PAPPE, marks=[mark('box', 0, 1.5, 322, 1, 0, '#9E7A52'), mark('box', 141, 0, 40, 4, 1, '#3A3F44')]),
    teil('boden', 'cardboard_box_body', 'Boden', 'Boden', 'box',
         x=0, y=0, w=330, d=330, z=0, h=3, r=2, explode=[0, 0, 0], mass=62, materials=WELLE,
         info='Hier liegt die Pizza. Stark fettige oder verklebte Stellen abreißen und in den Restmüll geben, '
              'der saubere Rest kommt ins Altpapier.',
         color=PAPPE, marks=[mark('cyl', 40, 40, 250, fill='#B98C5C'), mark('cyl', 90, 120, 70, 50, fill='#8E6B45'),
                             mark('cyl', 180, 190, 55, 40, fill='#8E6B45')]),
]
skaliere_masse(teile, oid='pizza_box')
schreibe('pizza_box', teile)
