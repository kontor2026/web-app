"""3D-Modell: plastic_ruler. Erzeugt tools/kategorien/modelle/plastic_ruler.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# 30-cm-Lineal aus glasklarem Polystyrol flach auf dem Tisch, 30 × 320 × 3 mm laut CSV, Länge entlang y.
# Lineal-Körper und abgesetzte Tuschekante (ein Spritzgussteil, als zwei Segmente), darüber die aufgedruckte Skala.
KLAR = '#D7E6EE'
SKALA = '#2A2E31'

ticks = [mark('box', 14 - (6 if i % 10 == 0 else 4 if i % 5 == 0 else 2.5), round(9.7 + i * 1.0, 1),
              6 if i % 10 == 0 else 4 if i % 5 == 0 else 2.5, 0.3, 0, SKALA) for i in range(0, 301, 5)]
ticks += [mark('box', 0.5, round(9.7 + i * 10.0 - 1.5, 1), 3, 3, 0.5, '#5A6268') for i in range(1, 30)]

teile = [
    teil('skala', 'ps_ruler', 'Aufgedruckte Skala', 'Skala', 'box',
         x=12, y=0, w=14, d=320, z=2.5, h=0.1, r=0, mass=0.1, materials=[['druck', 100]],
         info='Millimeterskala im Siebdruck. Die Farbe ist fest mit dem Kunststoff verbunden und lässt sich nicht abtrennen.',
         color=KLAR, opacity=0.25, marks=ticks),
    teil('koerper', 'ps_ruler', 'Lineal (Polystyrol)', 'Lineal', 'box',
         x=0, y=0, w=26, d=320, z=0, h=2.5, r=2, mass=26,
         info='Glasklares, sprödes Polystyrol. Zerbrochen in den Restmüll; ganz bleibt es lange nutzbar, also lieber weitergeben.',
         color=KLAR, opacity=0.7, marks=[mark('cyl', 4, 302, 8)]),
    teil('kante', 'ps_ruler', 'Tuschekante', 'Tuschekante', 'box',
         x=26, y=0, w=4, d=320, z=0, h=1.2, r=1, mass=3.9,
         info='Abgeflachte Kante am Rand, damit Tinte beim Linienziehen nicht unter das Lineal läuft. Gehört zum selben Spritzgussteil.',
         color=KLAR, opacity=0.7),
]

explodiere(teile, abstand=14, gruppen=[['koerper', 'kante']])
skaliere_masse(teile, oid='plastic_ruler', stellen=2)
schreibe('plastic_ruler', teile)
