"""3D-Modell: hairbrush. Erzeugt tools/kategorien/modelle/hairbrush.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Paddle-Haarbürste flach liegend, Borsten nach oben (laut CSV 70 × 230 × 45 mm), Bürstenkopf hinten (y = 0).
# Körper aus ABS (Kopfschale und Griff aus einem Stück) mit Soft-Touch-Einlage im Griff. In der Kopfschale sitzt
# ein Gummikissen, durch das die Nylonborsten mit Kugelspitzen gesteckt sind. Explodiert: Ebenen nach oben.
ABS = '#3A3F44'

# Stiftpositionen: 6 × 10 Raster im Kissen, Ecken (außerhalb des abgerundeten Kissens) ausgelassen
POS = []
for j in range(10):
    for i in range(6):
        px, py = 12.7 + i * 9, 13.5 + j * 9
        dx, dy = abs(px + 1.3 - 35) / 30, abs(py + 1.3 - 53) / 48
        if not (dx > 0.65 and dy > 0.75):
            POS.append((px, py))

PINS = [teil(f'borste_{k}', 'nylon_bristles', 'Nylonborste mit Kugelspitze', 'Borsten', 'cyl',
             x=px, y=py, w=2.6, z=17, h=23.5, mass=0.22, materials=[['nylon', 100]],
             color='#7A8288', label=(k == 0), marks=[mark('cyl', 0, 0, 2.6, fill='#D9473A', zeichnung=True)],
             info='Dicker Nylonstift mit aufgesetzter Kunststoffkugel, die die Kopfhaut schont. Der Fuß steckt im '
                  'Gummikissen; mit einer Zange lassen sich die Stifte herausziehen.' if k == 0 else
                  'Eine von vielen Nylonborsten mit Kugelspitze.')
        for k, (px, py) in enumerate(POS)]
KUGELN = [teil(f'kugel_{k}', 'nylon_bristles', 'Kugelspitze', 'Kugelspitzen', 'cyl', form='kugel',
               x=px - 0.95, y=py - 0.95, w=4.5, z=40.5, h=4.5, mass=0.03, materials=[['pp', 100]],
               color='#D9473A', label=False, info='Aufgesetzte Kunststoffkugel, schont die Kopfhaut.')
          for k, (px, py) in enumerate(POS)]
LOECHER = [mark('cyl', px - 6 - 0.2, py - 6 - 0.2, 3, fill='#3A3F44') for px, py in POS]

teile = [
    *KUGELN,
    *PINS,
    teil('kissen', 'rubber_cushion', 'Gummikissen', 'Kissen', 'box',
         x=6, y=6, w=58, d=94, z=12, h=5, r=25, mass=10,
         info='Elastisches Luftkissen aus Gummi, das beim Bürsten nachgibt. Mit einem flachen Werkzeug '
              'am Rand aus der Schale hebeln, dann sind Gummi und Kunststoff getrennt.',
         color='#1E2022', marks=LOECHER + [mark('cyl', 26, 88, 5, fill='#000000')]),
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
         x=21, y=106, w=28, d=124, z=1, h=11, r=12, form='liegend_y', mass=23,
         info='Griff aus ABS, in einem Stück mit der Kopfschale gespritzt.',
         color=ABS, marks=[mark('box', 5, 34, 18, 70, 8, '#6E747A', zeichnung=True), mark('cyl', 9, 110, 10, fill='#1E2022', zeichnung=True)]),
]

explodiere(teile, abstand=28, gruppen=[['kopfschale', 'griff'], [p['id'] for p in PINS + KUGELN]])
skaliere_masse(teile, oid='hairbrush')
schreibe('hairbrush', teile)
