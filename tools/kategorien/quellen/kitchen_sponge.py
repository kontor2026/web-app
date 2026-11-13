"""3D-Modell: kitchen_sponge. Erzeugt tools/kategorien/modelle/kitchen_sponge.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Haushaltsschwamm flach liegend (laut CSV 70 × 100 × 30 mm), grünes Scheuervlies oben, gelber Schaum unten.
# Das Vlies ist mit einer dünnen Klebeschicht auf den Schaum kaschiert; der Schaum hat seitliche Griffmulden.
# Explodiert: Vlies, Klebeschicht und Schaum übereinander abgehoben.
teile = [
    teil('vlies', 'scrub_pad', 'Scheuervlies', 'Scheuervlies', 'box',
         x=0, y=0, w=70, d=100, z=24, h=6, r=6, mass=3,
         materials=[['nylon', 70], ['phenolharz', 30]],
         info='Wirrfaservlies aus Nylon, mit Harz und feinem Schleifkorn getränkt. Es kratzt Angebranntes ab, '
              'zerkratzt aber auch beschichtete Pfannen.',
         color='#3E8E4A', marks=raster(5, 6, 6, 8, 6, 6, 11, 11.5, shape='cyl', fill='#2F7039')),
    teil('kleber', 'scrub_pad', 'Klebeschicht', 'Kleber', 'box', material_id='polyurethane',
         x=0.5, y=0.5, w=69, d=99, z=23.7, h=0.3, r=6, mass=0.4, materials=[['klebstoff', 100]],
         info='Dünner Kleberfilm, der Vlies und Schaum fest verbindet. Deshalb lassen sich die beiden Schichten nicht trennen.',
         color='#E8E1C8'),
    teil('schaum', 'sponge_foam', 'Schaumstoffkörper', 'Schaum', 'box',
         x=0, y=0, w=70, d=100, z=0, h=23.7, r=6, mass=6.6,
         info='Offenporiger Polyurethan-Schaum, der viel Wasser aufsaugt. Alte Schwämme gehören in den Restmüll; '
              'regelmäßig wechseln, weil sich im feuchten Schaum Keime vermehren.',
         color='#F2CF3B', marks=[mark('box', 0, 30, 4, 40, 2, '#D9B42A'), mark('box', 66, 30, 4, 40, 2, '#D9B42A')]
         + raster(10, 10, 4, 6, 3, 3, 15, 15, shape='cyl', fill='#E0BC2C')),
]

explodiere(teile, abstand=35)
skaliere_masse(teile, oid='kitchen_sponge')
schreibe('kitchen_sponge', teile)
