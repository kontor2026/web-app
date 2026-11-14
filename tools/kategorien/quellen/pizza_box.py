"""3D-Modell: pizza_box. Erzeugt tools/kategorien/modelle/pizza_box.json.

Typischer Pizzakarton 33 × 33 × 4 cm aus brauner Wellpappe, aus einem Zuschnitt gefaltet: Boden, doppelt gelegte
Seitenwände, Rückwand mit Deckelscharnier, Vorderwand, bedruckter Deckel mit Einstecklasche. In der Mitte steht ein
Pizza-Retter aus PP (Tischchen mit drei Beinen), der den Deckel stützt.
Deckel (mit Lasche) hebt hoch ab, Pizza-Retter schwebt darunter, die Wände klappen nach außen weg.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

PAPPE = '#B8946A'
KANTE = '#9E7A52'
WELLE = [['papier', 100]]
ROT, GRUEN, CREME = '#B3423A', '#3F7D4A', '#F1E4C8'
AUS = 110  # Wände nach außen
DECKEL = [0, 0, 330]

# Deckeldruck: Pizza mit Rand, Käse, Salami und Basilikum, darunter Schriftzug-Balken, Italien-Streifen, Luftlöcher
druck = [mark('cyl', 85, 40, 160, fill='#D9A55B'), mark('cyl', 95, 50, 140, fill=ROT),
         mark('cyl', 102, 57, 126, fill='#E8C65A')]
druck += [mark('cyl', 165 + dx - 11, 120 + dy - 11, 22, fill='#A3352E')
          for dx, dy in ((-35, -30), (25, -38), (40, 10), (-5, 5), (-42, 22), (12, 42), (-15, -60), (50, -12))]
druck += [mark('cyl', 165 + dx - 6, 120 + dy - 4, 12, 8, fill=GRUEN) for dx, dy in ((10, -15), (-25, 0), (28, 28))]
druck += [mark('box', 65, 222, 200, 30, 4, ROT), mark('box', 75, 230, 180, 14, 2, CREME),
          mark('box', 105, 264, 120, 8, 2, '#3A3F44'),
          mark('box', 125, 284, 26, 8, 0, GRUEN), mark('box', 152, 284, 26, 8, 0, CREME), mark('box', 179, 284, 26, 8, 0, ROT)]
druck += raster(18, 18, 2, 1, 10, 10, 284, shape='cyl', fill='#6E5236')

teile = [
    teil('deckel', 'cardboard_box_body', 'Deckel', 'Deckel', 'box',
         x=0, y=0, w=330, d=330, z=37, h=3, r=2, explode=DECKEL, mass=62,
         materials=[['papier', 98], ['druck', 2]],
         info='Bedruckte Wellpappe. Ist der Deckel sauber, kommt er ins Altpapier. Ist nur der Boden fettig, '
              'den Deckel an der Knickkante abreißen und getrennt entsorgen.',
         color=PAPPE, marks=druck),
    teil('lasche', 'cardboard_box_body', 'Einstecklasche des Deckels', 'Deckellasche', 'box',
         x=30, y=321, w=270, d=4, z=12, h=25, r=0, explode=DECKEL, mass=8, materials=WELLE,
         info='Vorne am Deckel angeknickt. Sie wird in die doppelte Vorderwand gesteckt und hält den Karton zu.',
         color=PAPPE),
    teil('pizzaretter', 'cardboard_box_body', 'Pizza-Retter (Tischchen)', 'Pizza-Retter', 'cyl',
         material_id='pp', x=150, y=150, w=30, z=34, h=2, explode=[0, 0, 70], mass=1.2,
         info='Kleines Kunststoff-Tischchen aus PP. Es hält den Deckel vom Käse fern. Gehört nicht ins Altpapier, '
              'sondern in die Gelbe Tonne.',
         color='#F2F0EA', marks=[mark('cyl', 9, 9, 12, fill='#DAD7CF')]),
]
for n, (bx, by) in enumerate(((161, 152), (152, 168), (170, 168))):
    teile.append(teil(f'bein_{n + 1}', 'cardboard_box_body', 'Bein des Pizza-Retters', 'Bein', 'cyl',
                      material_id='pp', x=bx, y=by, w=6, z=3, h=31, explode=[0, 0, 70], mass=0.3, label=False,
                      info='Eines von drei Beinen, aus einem Stück mit dem Tischchen gespritzt.', color='#E6E3DB'))
teile += [
    teil('wand_hinten', 'cardboard_box_body', 'Rückwand mit Deckelscharnier', 'Rückwand', 'box',
         x=4, y=0, w=322, d=4, z=3, h=34, r=0, explode=[0, -AUS, 0], mass=12, materials=WELLE,
         info='Hier ist der Deckel nur eingeknickt, nicht geklebt. Pizzakartons kommen ganz ohne Klebstoff aus.',
         color=PAPPE, marks=[mark('box', 0, 1.5, 322, 1, 0, KANTE)]),
    teil('wand_links', 'cardboard_box_body', 'Seitenwand links (doppelt gelegt)', 'Seitenwand', 'box',
         x=0, y=0, w=4, d=330, z=3, h=34, r=0, explode=[-AUS, 0, 0], mass=24, materials=WELLE,
         info='Die Seitenwand ist doppelt gefaltet und mit Laschen im Boden verriegelt. Das macht den Karton stapelbar.',
         color=PAPPE, marks=[mark('box', 1.5, 0, 1, 330, 0, KANTE)]),
    teil('wand_rechts', 'cardboard_box_body', 'Seitenwand rechts (doppelt gelegt)', 'Seitenwand', 'box',
         x=326, y=0, w=4, d=330, z=3, h=34, r=0, explode=[AUS, 0, 0], mass=24, materials=WELLE, label=False,
         info='Gegenstück zur linken Seitenwand.',
         color=PAPPE, marks=[mark('box', 1.5, 0, 1, 330, 0, KANTE)]),
    teil('wand_vorne', 'cardboard_box_body', 'Vorderwand (doppelt)', 'Vorderwand', 'box',
         x=4, y=326, w=322, d=4, z=3, h=34, r=0, explode=[0, AUS, 0], mass=20, materials=WELLE,
         info='Doppelte Wand mit Schlitz, in den die Deckellasche gesteckt wird. Zum Flachmachen alle Wände aufklappen.',
         color=PAPPE, marks=[mark('box', 26, 1.5, 270, 1, 0, '#6E5236'), mark('box', 141, 0, 40, 4, 1, '#3A3F44')]),
    teil('boden', 'cardboard_box_body', 'Boden', 'Boden', 'box',
         x=0, y=0, w=330, d=330, z=0, h=3, r=2, explode=[0, 0, 0], mass=62, materials=WELLE,
         info='Hier liegt die Pizza. Stark fettige oder verklebte Stellen abreißen und in den Restmüll geben, '
              'der saubere Rest kommt ins Altpapier.',
         color=PAPPE, marks=[mark('cyl', 40, 40, 250, fill='#B98C5C'), mark('cyl', 90, 120, 70, 50, fill='#8E6B45'),
                             mark('cyl', 190, 200, 55, 40, fill='#8E6B45'), mark('cyl', 210, 80, 30, 22, fill='#9C764C'),
                             mark('box', 0, 4, 330, 1, 0, KANTE), mark('box', 0, 325, 330, 1, 0, KANTE)]),
]
skaliere_masse(teile, oid='pizza_box')
schreibe('pizza_box', teile)
