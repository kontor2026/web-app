"""3D-Modell: coffee_bag. Erzeugt tools/kategorien/modelle/coffee_bag.json.

Typische 250-g-Kaffeeverpackung als Blockbodenbeutel (10 × 6 cm Boden, 22 cm hoch), leer, aufgestellt:
Mantel aus Verbundfolie mit Längsnaht hinten, gefalteter Blockboden, zusammengedrückter Kopf mit Siegelnaht,
Aromaventil vorne. Kopf und Siegelnaht schweben über dem Mantel, Ventil und Längsnaht werden nach vorne bzw.
hinten herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

DRUCK = '#3B2A22'
SILBER = '#C9CDD0'
VERBUND = [['verbundfolie', 96], ['druck', 3], ['alu', 1]]  # PET/Alu/PE-Verbund, bedruckt
teile = [
    teil('siegelnaht', 'multilayer_film', 'Siegelnaht (Kopf)', 'Siegelnaht', 'box',
         x=0, y=27, w=100, d=6, z=205, h=15, r=0, mass=0.6, materials=VERBUND, color=DRUCK,
         info='Oben sind alle Folienlagen heiß verschweißt. Zum Öffnen unterhalb der Naht abschneiden.',
         marks=raster(1, 1, 33, 1, 2, 4, 3, fill='#5A4436')),
    teil('kopf', 'multilayer_film', 'Kopfteil (zusammengelegt)', 'Kopf', 'box',
         x=0, y=12, w=100, d=36, z=190, h=15, r=6, mass=1.0, materials=VERBUND, color=DRUCK,
         info='Beim Verschließen werden die Seitenfalten nach innen gelegt, so wird der Beutel oben flach.',
         marks=[mark('box', 0, 17, 100, 2, 0, '#5A4436')]),
    teil('ventil', 'degassing_valve', 'Aromaschutzventil', 'Ventil', 'box',
         x=39, y=60, w=22, d=2.5, z=150, h=22, r=1.2, mass=0.6, materials=[['ldpe', 85], ['pp', 10], ['klebstoff', 5]],
         color='#E9E6DF',
         info='Kleines Einwegventil: Frisch gerösteter Kaffee gibt Kohlendioxid ab, das hier entweicht, ohne dass '
              'Luft hineinkommt. Mit der Schere herausschneiden.',
         marks=[mark('cyl', 7, 0.5, 8, 1.5, fill='#9C968A')]),
    teil('mantel', 'multilayer_film', 'Mantel aus Verbundfolie', 'Mantel', 'box',
         x=0, y=0, w=100, d=60, z=3, h=187, r=3, mass=7.6, materials=VERBUND, color=DRUCK,
         info='Mehrere fest verklebte Schichten aus Kunststoff und Aluminium halten Licht, Sauerstoff und Feuchte ab. '
              'Sie lassen sich nicht trennen: leer schütteln und in die Gelbe Tonne.',
         marks=[mark('box', 1.5, 1.5, 97, 57, 2, SILBER), mark('box', 47, 0, 6, 1.5, 0, '#5A4436')]),
    teil('laengsnaht', 'multilayer_film', 'Längsnaht (hinten)', 'Längsnaht', 'box',
         x=44, y=-2, w=12, d=2, z=3, h=187, r=0, mass=0.5, materials=VERBUND, color=DRUCK,
         info='Hier ist die Folienbahn zum Schlauch verschweißt und flach umgelegt.'),
    teil('boden', 'multilayer_film', 'Blockboden', 'Boden', 'box',
         x=0, y=0, w=100, d=60, z=0, h=3, r=3, mass=1.7, materials=VERBUND, color=DRUCK,
         info='Das untere Schlauchende ist zu einem rechteckigen Boden gefaltet und versiegelt, darum steht '
              'der Beutel von allein.',
         marks=[mark('box', 2, 2, 96, 56, 2, SILBER), mark('box', 2, 28, 96, 4, 0, '#8E969A'),
                mark('box', 2, 2, 20, 56, 0, '#B5BBBF'), mark('box', 78, 2, 20, 56, 0, '#B5BBBF')]),
]
seitlich = {'ventil': (0, 50), 'laengsnaht': (0, -45)}
explodiere([p for p in teile if p['id'] not in seitlich], abstand=35)
dz_mantel = next(p for p in teile if p['id'] == 'mantel')['explode'][2]
for p in teile:
    if p['id'] in seitlich:
        p['explode'] = [seitlich[p['id']][0], seitlich[p['id']][1], dz_mantel]
skaliere_masse(teile, oid='coffee_bag')
schreibe('coffee_bag', teile)
