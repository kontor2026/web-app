"""3D-Modell: highlighter. Erzeugt tools/kategorien/modelle/highlighter.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Textmarker mit Keilspitze, aufrecht (laut CSV 20 × 20 × 120 mm), Spitze oben. Ovaler Schaft 17 × 15 mm,
# Kappe mit Clip. Fasertank und Keilspitze werden seitlich (dx > 0) herausgezogen, Kappe und Spitzenhalter schweben oben.
GELB = '#F2E23A'
GRAU = '#3A3F44'
TANK = 30

teile = [
    teil('kappe', 'pen_cap', 'Kappe', 'Kappe', 'cyl',
         x=0, y=1.5, w=18, d=17, z=84, h=36, mass=2.6,
         info='Hält die Spitze feucht. Die neonfarbene Tinte trocknet offen in wenigen Stunden ein.',
         color=GRAU, marks=[mark('cyl', 7, 6.5, 4, fill='#2A2E31')]),
    teil('clip', 'pen_cap', 'Clip', 'Clip', 'box',
         x=18, y=8.5, w=2, d=3, z=90, h=28, r=0.6, mass=0.4,
         info='Angespritzter Clip aus Polypropylen, wie die Kappe.',
         color=GRAU),
    teil('spitze', 'marker_nib', 'Keilspitze', 'Keilspitze', 'box',
         x=7, y=8, w=5, d=4, z=90, h=20, r=0.5, explode=[TANK, 0, 10], mass=0.4,
         info='Schräg geschnittene Polyesterfaser: breit für Zeilen, schmal für feine Striche. Mit einer Zange herausziehen.',
         color=GELB, marks=[mark('box', 0.5, 0.5, 4, 1, 0.3, '#E0CC20')]),
    teil('spitzenhalter', 'pen_barrel', 'Spitzenhalter', 'Spitzenhalter', 'cyl',
         x=1.5, y=2.5, w=16, d=15, z=88, h=10, mass=1.0,
         info='Vorderteil mit Schlitz für die Keilspitze, in den Schaft eingepresst.',
         color=GELB, marks=[mark('box', 5.5, 5.5, 5, 4, 0.5, '#B8A817')]),
    teil('tank', 'marker_ink_reservoir', 'Fasertank mit Leuchttinte', 'Tank', 'cyl',
         x=3.5, y=4, w=12, d=12, z=6, h=80, explode=[TANK, 0, 0], mass=3.2, materials=[['polyester', 75], ['pp', 15], ['druck', 10]],
         info='Polyesterwatte mit fluoreszierender Tinte. Nachfüllbare Textmarker sparen viel Kunststoff.',
         color='#F7F09A', marks=[mark('cyl', 2, 2, 8, fill=GELB)]),
    teil('schaft', 'pen_barrel', 'Schaft', 'Schaft', 'cyl',
         x=1, y=2, w=17, d=16, z=4, h=84, mass=5.6,
         info='Ovaler Polypropylen-Schaft, damit der Stift nicht wegrollt. Ausgetrocknet in den Restmüll.',
         color=GELB, marks=[mark('cyl', 2.5, 2.5, 12, 11, fill='#E0CC20')]),
    teil('endstopfen', 'pen_barrel', 'Endstopfen', 'Endstopfen', 'cyl',
         x=1.5, y=2.5, w=16, d=15, z=0, h=4, mass=0.8,
         info='Hinterer Stopfen. Abziehen, dann lässt sich der Tank nachfüllen oder herausnehmen.',
         color=GRAU),
]

explodiere(teile, abstand=10, gruppen=[['kappe', 'clip']])
skaliere_masse(teile, oid='highlighter', stellen=2)
schreibe('highlighter', teile)
