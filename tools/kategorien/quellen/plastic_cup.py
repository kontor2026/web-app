"""3D-Modell: plastic_cup. Erzeugt tools/kategorien/modelle/plastic_cup.json.

Typischer Einweg-Trinkbecher 0,2 l aus PP (75 mm oben, 50 mm unten, 100 mm hoch): gerollter Rand, konische Wand
aus fünf Ringen, Standring. Ein einziges Material; der Rand hebt zur Erklärung leicht ab.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

PP = '#EEF1F3'
INNEN = '#D3D9DD'
SCHATTEN = '#BCC4CA'
# Konische Wand: oben Ø 72, unten Ø 52, in fünf Ringen (je 19 mm hoch)
RINGE = [(72, 78, 19), (67, 59, 19), (62, 40, 19), (57, 22, 18), (52, 3, 19)]
teile = [
    teil('rand', 'pp_cup_body', 'Rollrand', 'Rand', 'cyl',
         x=0, y=0, w=75, z=97, h=3, explode=[0, 0, 30], mass=0.6, opacity=0.6,
         info='Der gerollte Rand macht den dünnen Becher steif und angenehm zum Trinken.',
         color=PP, wand=2.5, boden=0, marks=[mark('cyl', 2.5, 2.5, 70, fill=INNEN, zeichnung=True), mark('cyl', 13, 15, 50, 46, fill=SCHATTEN, zeichnung=True)]),
]
for i, (w, z, h) in enumerate(RINGE):
    o = (75 - w) / 2
    teile.append(teil(f'wand{i}', 'pp_cup_body', 'Becherwand', 'Wand', 'cyl',
                      x=o, y=o, w=w, z=z, h=h, explode=[0, 0, 0], mass=0.9, opacity=0.6, label=(i == 0), color=PP, wand=round(0.8 + 0.05 * i, 2), boden=0,
                      info='PP, Recyclingcode 5, tiefgezogen aus einer dünnen Folie (etwa 0,2 mm). Weil der Becher '
                           'nach unten schmaler wird, lassen sich viele ineinander stapeln.' if i == 0 else
                           'Gehört zur Becherwand aus PP. Leicht geriffelt, damit der Becher besser in der Hand liegt.',
                      marks=[mark('cyl', 1.5, 1.5, w - 3, fill=INNEN, zeichnung=True)] if i == 0 else None))
teile.append(teil('boden', 'pp_cup_body', 'Boden mit Standring', 'Boden', 'cyl',
                  x=12.5, y=12.5, w=50, z=0, h=3, explode=[0, 0, 0], mass=0.6, opacity=0.6, color=PP,
                  info='Hier steht das Recyclingzeichen 5. Leer gemacht kommt der ganze Becher in die Gelbe Tonne, '
                       'Becher nicht ineinanderstecken, sonst sortiert die Anlage sie schlechter.',
                  wand=0.8, marks=[mark('cyl', 4, 4, 42, fill=INNEN, zeichnung=True)]))
skaliere_masse(teile, oid='plastic_cup')
schreibe('plastic_cup', teile)
