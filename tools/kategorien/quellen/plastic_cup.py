"""3D-Modell: plastic_cup. Erzeugt tools/kategorien/modelle/plastic_cup.json.

Typischer Einweg-Trinkbecher 0,2 l aus PP (75 mm oben, 50 mm unten, 100 mm hoch): gerollter Rand, konische Wand
aus drei Segmenten, Standring. Ein einziges Material; der Rand hebt zur Erklärung leicht ab.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

PP = '#EEF1F3'
teile = [
    teil('rand', 'pp_cup_body', 'Rollrand', 'Rand', 'cyl',
         x=0, y=0, w=75, z=97, h=3, explode=[0, 0, 25], mass=0.6, opacity=0.8,
         info='Der gerollte Rand macht den dünnen Becher steif und angenehm zum Trinken.',
         color=PP, marks=[mark('cyl', 3, 3, 69, fill='#C9D0D5')]),
    teil('oben', 'pp_cup_body', 'Becherwand oben', 'Wand', 'cyl',
         x=1.5, y=1.5, w=72, z=65, h=32, explode=[0, 0, 0], mass=1.6, opacity=0.8,
         info='PP, Recyclingcode 5, tiefgezogen aus einer dünnen Folie. Darum ist der Becher oben breiter und stapelbar.',
         color=PP, marks=[mark('cyl', 2, 2, 68, fill='#C9D0D5')]),
    teil('mitte', 'pp_cup_body', 'Becherwand Mitte', 'Wand Mitte', 'cyl',
         x=5.5, y=5.5, w=64, z=33, h=32, explode=[0, 0, 0], mass=1.3, opacity=0.8, label=False,
         info='Die Wand ist hier nur etwa 0,2 mm dünn.',
         color=PP),
    teil('unten', 'pp_cup_body', 'Becherwand unten', 'Wand unten', 'cyl',
         x=9.5, y=9.5, w=56, z=3, h=30, explode=[0, 0, 0], mass=1.0, opacity=0.8, label=False,
         info='Leicht geriffelt, damit der Becher besser in der Hand liegt.',
         color=PP),
    teil('boden', 'pp_cup_body', 'Boden mit Standring', 'Boden', 'cyl',
         x=12.5, y=12.5, w=50, z=0, h=3, explode=[0, 0, 0], mass=0.6, opacity=0.8,
         info='Hier steht das Recyclingzeichen. Leer gemacht kommt der ganze Becher in die Gelbe Tonne.',
         color=PP),
]
skaliere_masse(teile, oid='plastic_cup')
schreibe('plastic_cup', teile)
