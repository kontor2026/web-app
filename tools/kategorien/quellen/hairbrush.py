"""3D-Modell: hairbrush. Erzeugt tools/kategorien/modelle/hairbrush.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Paddle-Haarbürste flach liegend, Borsten nach oben (laut CSV 70 × 230 × 45 mm), Bürstenkopf hinten (y = 0).
# Körper aus ABS (Kopfschale und Griff aus einem Stück) mit Soft-Touch-Einlage im Griff. In der Kopfschale sitzt
# ein Gummikissen, durch das die Nylonborsten mit Kugelspitzen gesteckt sind. Explodiert: Ebenen nach oben.
ABS = '#3A3F44'
PINS = raster(3, 4.5, 9, 15, 2, 2, 5.6, 5.6, shape='cyl', fill='#B8BEC4')

teile = [
    teil('kugelspitzen', 'nylon_bristles', 'Kugelspitzen', 'Kugelspitzen', 'box', material_id='pp',
         x=9, y=9, w=52, d=88, z=42, h=3, r=22, mass=3, materials=[['pp', 100]],
         info='Kleine Kunststoffkugeln auf den Borstenenden. Sie schonen die Kopfhaut beim Bürsten.',
         color='#D9473A', marks=raster(3, 4.5, 9, 15, 2.6, 2.6, 5.6, 5.6, shape='cyl', fill='#B5372C')),
    teil('borsten', 'nylon_bristles', 'Nylonborsten', 'Borsten', 'box',
         x=9, y=9, w=52, d=88, z=17, h=25, r=22, mass=12,
         info='Rund 130 dicke Nylonstifte, mit dem Fuß im Gummikissen verankert. Mit einer Zange lassen sie sich herausziehen.',
         color='#2B2D2F', opacity=0.85, marks=PINS),
    teil('kissen', 'rubber_cushion', 'Gummikissen', 'Kissen', 'box',
         x=6, y=6, w=58, d=94, z=12, h=5, r=25, mass=10,
         info='Elastisches Luftkissen aus Gummi, das beim Bürsten nachgibt. Mit einem flachen Werkzeug '
              'am Rand aus der Schale hebeln, dann sind Gummi und Kunststoff getrennt.',
         color='#1E2022', marks=raster(6, 7.5, 9, 15, 2, 2, 5.6, 5.6, shape='cyl', fill='#3A3F44') + [mark('cyl', 26, 87, 6, fill='#000000')]),
    teil('griffeinlage', 'hairbrush_body', 'Soft-Touch-Einlage', 'Griffeinlage', 'box', material_id='rubber',
         x=26, y=140, w=18, d=70, z=12, h=1, r=8, mass=2, materials=[['tpe', 100]],
         info='Weiche, rutschfeste Einlage aus TPE im Griff. Sie ist eingeklebt oder angespritzt.',
         color='#6E747A'),
    teil('kopfschale', 'hairbrush_body', 'Kopfschale', 'Kopfschale', 'box',
         x=0, y=0, w=70, d=106, z=0, h=13, r=30, mass=30,
         info='Schale aus ABS mit einem kleinen Luftloch, damit das Kissen federn kann. '
              'Ohne Kissen und Borsten ist der Körper sortenreiner Kunststoff.',
         color=ABS, marks=[mark('box', 4, 4, 62, 98, 27, '#2B2D2F')]),
    teil('griff', 'hairbrush_body', 'Griff', 'Griff', 'box',
         x=21, y=106, w=28, d=124, z=1, h=11, r=12, mass=23,
         info='Griff aus ABS, in einem Stück mit der Kopfschale gespritzt.',
         color=ABS, marks=[mark('box', 5, 34, 18, 70, 8, '#6E747A'), mark('cyl', 9, 110, 10, fill='#1E2022')]),
]

explodiere(teile, abstand=28, gruppen=[['kopfschale', 'griff']])
skaliere_masse(teile, oid='hairbrush')
schreibe('hairbrush', teile)
