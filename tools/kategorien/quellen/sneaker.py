"""3D-Modell: sneaker. Erzeugt tools/kategorien/modelle/sneaker.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, schreibe  # noqa: E402

# Ein Sportschuh (Größe ca. 42), Ferse hinten (y = 0), Spitze vorne (y = 290). 110 × 290 × 118 mm.
OBER = '#E8E6E1'
teile = [
    teil('senkel', 'shoelaces', 'Schnürsenkel', 'Schnürsenkel', 'box',
         x=38, y=100, w=34, d=88, z=104, h=4, r=3, mass=10, materials=[['polyester', 100]], color='#F4F2EE',
         explode=[130, 0, 40],
         info='Geflochtenes Polyester mit Kunststoffenden. Ausfädeln: Sie lassen sich weiterverwenden oder mit dem Textil abgeben.',
         marks=[mark('box', 0, 6 + i * 14, 34, 3, 1.5, '#C9C6BF') for i in range(6)]),
    teil('zunge', 'textile_upper', 'Zunge', 'Zunge', 'box',
         x=30, y=95, w=50, d=100, z=80, h=24, r=20, mass=16, materials=[['polyester', 70], ['schaum', 30]], color=OBER,
         info='Gepolsterte Lasche unter den Schnürsenkeln, oben am Schaft angenäht. Im Inneren steckt Schaumstoff.',
         marks=[mark('box', 15, 6, 20, 10, 2, '#5E656A')]),
    teil('ferse', 'textile_upper', 'Fersenteil mit Kragen', 'Fersenteil', 'box',
         x=8, y=0, w=94, d=95, z=32, h=86, r=40, mass=50, materials=[['polyester', 65], ['schaum', 25], ['tpu', 10]],
         color=OBER,
         info='Gepolsterter Schaft rund um Knöchel und Ferse. Mit dem Vorderschaft vernäht und an die Sohle geklebt.',
         marks=[mark('cyl', 17, 20, 60, 70, fill='#C9C6BF'), mark('box', 40, 0, 14, 8, 3, '#5E656A')]),
    teil('vorfuss', 'textile_upper', 'Obermaterial Vorfuß', 'Obermaterial', 'box',
         x=5, y=95, w=100, d=195, z=32, h=48, r=45, mass=62, materials=[['polyester', 80], ['tpu', 15], ['schaum', 5]],
         color=OBER,
         info='Atmungsaktives Polyester-Netzgewebe mit aufgeschweißten Kunststoff-Verstärkungen. Mit dem Messer entlang der '
              'Sohlennaht abtrennen.',
         marks=raster(26, 10, 5, 2, 4, 4, 12, 10, shape='cyl') + [mark('box', 8, 130, 84, 50, 35, '#D6D3CC')]),
    teil('fersenkappe', 'textile_upper', 'Fersenkappe', 'Fersenkappe', 'box',
         material_id='polyurethane', x=12, y=3, w=86, d=40, z=36, h=55, r=34, mass=14, materials=[['tpu', 100]],
         color='#B8BCC0', explode=[-130, 0, 0],
         info='Feste Kunststoffschale zwischen Futter und Obermaterial. Sie hält die Ferse im Schuh stabil.'),
    teil('einlegesohle', 'foam_midsole', 'Einlegesohle', 'Einlegesohle', 'box',
         material_id='pu_foam', x=12, y=6, w=86, d=276, z=32, h=4, r=40, mass=22,
         materials=[['schaum', 85], ['polyester', 15]], color='#5E656A',
         info='Weicher Schaumstoff mit Stoffbezug. Lose eingelegt: einfach herausziehen.',
         marks=[mark('box', 10, 4, 66, 60, 30, '#6E7579')]),
    teil('zwischensohle', 'foam_midsole', 'Zwischensohle (EVA)', 'Zwischensohle', 'box',
         x=3, y=0, w=104, d=290, z=10, h=22, r=48, mass=108, materials=[['schaum', 100]], color='#F4F2EE',
         info='Leichter EVA-Schaum, der beim Laufen federt. Mit der Laufsohle verklebt: nur mit Heißluft und Messer trennbar.'),
    teil('laufsohle', 'rubber_outsole', 'Laufsohle', 'Laufsohle', 'box',
         x=0, y=0, w=110, d=290, z=0, h=10, r=50, mass=118, materials=[['gummi', 100]], color='#3A3F44',
         info='Abriebfester Gummi mit Profil für Halt. Nach Erwärmen des Klebers von der Zwischensohle abziehen.',
         marks=raster(14, 14, 6, 18, 10, 6, 14, 14.5, r=2, fill='#262B2F')),
]

explodiere(teile, abstand=40, fest=('laufsohle',))
schreibe('sneaker', teile)
