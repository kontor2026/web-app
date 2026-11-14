"""3D-Modell: pencil_case. Erzeugt tools/kategorien/modelle/pencil_case.json.

Schlampermäppchen 80 × 210 × 40 mm, flach liegend, Reißverschluss längs (y) mittig oben. Außenstoff aus Nylon-Gewebe
in zwei Schalen (unten mit Boden, oben mit den Reißverschluss-Kanten), innen ein Polyesterfutter. Reißverschluss:
Messing-Zahnreihe auf Polyesterband, Schieber aus Zinkdruckguss, Zuglasche aus Stoff. Explodiert: Lagen nach oben, Schieber und
Zuglasche obenauf.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

STOFF = '#2E5A88'
teile = [
    teil('zuglasche', 'metal_zipper', 'Zuglasche (Stoffschlaufe)', 'Zuglasche', 'box',
         x=34, y=196, w=12, d=26, z=38, h=2, r=5, mass=1.5, material_id='polyester', color='#E4572E',
         info='Stoffschlaufe am Schieber, damit man den Reißverschluss gut greift. Mit der Schere abschneiden.',
         marks=[mark('box', 3, 3, 6, 18, 3, '#C94524')]),
    teil('schieber', 'metal_zipper', 'Reißverschluss-Schieber', 'Schieber', 'box',
         x=34, y=180, w=12, d=20, z=37, h=3, r=3, mass=4, material_id='copper', materials=[['zink', 100]],
         color='#B89A5C',
         info='Druckguss aus Zinklegierung, oft vermessingt. Gehört mit der Zahnreihe zum Metallschrott.',
         marks=[mark('box', 3, 3, 6, 12, 2, '#9C7F45')]),
    teil('reissverschluss', 'metal_zipper', 'Reißverschluss (Zahnreihe auf Band)', 'Reißverschluss', 'box',
         x=32, y=6, w=16, d=198, z=36, h=1.5, r=2, mass=12, materials=[['messing', 65], ['polyester', 35]],
         color='#1F2A36',
         info='Zwei Polyesterbänder mit Messingzähnen, an die Stoffkanten genäht. Zum Trennen links und rechts '
              'neben den Zähnen entlang schneiden.',
         marks=[mark('box', 6, 0, 4, 198, 0, '#C2A564')] + raster(5, 2, 1, 49, 6, 1.2, 0, 4, fill='#A88A4C')),
    teil('oberteil', 'nylon_fabric', 'Oberschale (Außenstoff)', 'Oberschale', 'box',
         x=6, y=6, w=68, d=198, z=31, h=5, r=22, mass=6,
         info='Nylon-Gewebe mit Beschichtung, an der Kante mit dem Unterteil vernäht. Saubere Mäppchen in die '
              'Altkleidersammlung oder weitergeben, kaputte in den Restmüll.',
         color=STOFF, marks=[mark('box', 46, 14, 22, 12, 2, '#E9E6DF'), mark('box', 27, 0, 14, 198, 2, '#1A2430')]),
    # Die Oberschale ist gewölbt: Scheiben werden in der Foto-Ansicht zu einer weichen Hülle verbunden
    teil('oberteil_mitte', 'nylon_fabric', 'Oberschale (Wölbung)', 'Oberschale', 'box',
         x=2, y=2, w=76, d=206, z=26, h=5, r=18, mass=10, label=False,
         info='Gewölbter Teil der Oberschale.', color=STOFF),
    teil('oberteil_rand', 'nylon_fabric', 'Oberschale (Rand)', 'Oberschale', 'box',
         x=0, y=0, w=80, d=210, z=20, h=6, r=14, mass=12, label=False,
         info='Unterer Rand der Oberschale an der Naht.', color=STOFF),
    teil('futter', 'nylon_fabric', 'Innenfutter', 'Futter', 'box',
         x=7, y=7, w=66, d=196, z=4, h=30, r=12, mass=14, material_id='polyester', color='#B9C4CC',
         info='Dünnes Polyesterfutter, an der Reißverschlussnaht mit eingenäht. Lässt sich nur mit der Schere lösen.',
         marks=[mark('box', 4, 30, 58, 80, 4, '#A9B5BE')]),
    teil('unterteil', 'nylon_fabric', 'Unterschale mit Boden', 'Unterschale', 'box',
         x=0, y=0, w=80, d=210, z=12, h=8, r=14, mass=16,
         info='Boden und Seitenwände, innen mit einer dünnen Versteifung, damit das Mäppchen die Form hält.',
         color=STOFF, marks=[mark('box', 3, 3, 74, 204, 12, '#21436A', zeichnung=True)]),
    teil('unterteil_mitte', 'nylon_fabric', 'Unterschale (Wölbung)', 'Unterschale', 'box',
         x=2, y=2, w=76, d=206, z=5, h=7, r=18, mass=12, label=False,
         info='Gewölbter Teil der Unterschale.', color=STOFF),
    teil('unterteil_boden', 'nylon_fabric', 'Unterschale (Boden)', 'Unterschale', 'box',
         x=7, y=7, w=66, d=196, z=0, h=5, r=22, mass=8, label=False,
         info='Flacher Boden, auf dem das Mäppchen liegt.', color=STOFF),
]
explodiere(teile, abstand=25, abstaende={'zuglasche': 12, 'schieber': 18, 'reissverschluss': 50},
           gruppen=[['oberteil', 'oberteil_mitte', 'oberteil_rand'], ['unterteil', 'unterteil_mitte', 'unterteil_boden']])
skaliere_masse(teile, oid='pencil_case')
schreibe('pencil_case', teile)
