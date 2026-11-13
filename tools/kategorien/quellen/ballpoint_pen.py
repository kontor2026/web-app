"""3D-Modell: ballpoint_pen. Erzeugt tools/kategorien/modelle/ballpoint_pen.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Kugelschreiber mit Kappe, aufrecht wie im Stifteköcher (Spitze oben), Ø 10 mm, 145 mm hoch (laut CSV stehend).
# Schaft unten, Griffstück aufgeschraubt, Kappe mit Clip oben. Mine mit Messingspitze und Feder wird seitlich
# (dx > 0) herausgezogen, Griffstück und Kappe schweben über dem Schaft.
BLAU = '#2F5FA8'
MINE = 22  # seitlicher Versatz der Mine

teile = [
    teil('kappe', 'pen_cap', 'Kappe', 'Kappe', 'cyl',
         x=-0.5, y=-0.5, w=11, z=106, h=39, explode=[0, 0, 45], mass=1.4,
         info='Schützt die Spitze vor dem Austrocknen. Das kleine Loch oben ist Absicht: Verschluckt man die Kappe, '
              'kann man trotzdem atmen.',
         color=BLAU, marks=[mark('cyl', 4, 4, 3, fill='#1E3F73')]),
    teil('clip', 'pen_cap', 'Clip', 'Clip', 'box',
         x=10.5, y=3.5, w=1.5, d=3, z=112, h=30, r=0.5, explode=[6, 0, 45], mass=0.3,
         info='Federnder Kunststoffclip, an die Kappe angespritzt. Hält den Stift in der Hemdtasche.',
         color=BLAU),
    teil('feder', 'steel_spring', 'Druckfeder', 'Feder', 'cyl',
         x=2.75, y=2.75, w=4.5, z=100, h=10, explode=[MINE, 0, 45], mass=0.2,
         info='Kleine Stahlfeder um die Mine. Sie drückt die Mine nach vorne, damit sie beim Schreiben nicht wackelt. '
              'Mit einer Pinzette abziehen; sie gehört nicht in die Gelbe Tonne.',
         color='#B8BEC4', marks=[mark('cyl', 0.75, 0.75, 3)]),
    teil('spitze', 'ink_refill', 'Schreibspitze mit Kugel', 'Spitze', 'cyl', material_id='steel',
         x=3.75, y=3.75, w=2.5, z=122, h=8, explode=[MINE, 0, 8], mass=0.3, materials=[['messing', 95], ['stahl', 5]],
         info='Messinghülse mit einer winzigen Kugel aus Hartmetall. Die Kugel rollt über das Papier und nimmt dabei Tinte mit.',
         color='#C9A24A', marks=[mark('cyl', 0.75, 0.75, 1, fill='#8E969A')]),
    teil('mine', 'ink_refill', 'Mine (Tintenröhrchen)', 'Mine', 'cyl',
         x=3.5, y=3.5, w=3, z=8, h=114, explode=[MINE, 0, 0], mass=1.1, materials=[['pp', 80], ['tinte', 20]],
         info='Polypropylen-Röhrchen mit zäher Kugelschreiberpaste. Lieber nur die Mine wechseln als den ganzen Stift wegwerfen.',
         color='#E4E8EA', marks=[mark('cyl', 0.6, 0.6, 1.8, fill='#2F5FA8')]),
    teil('griffstueck', 'pen_barrel', 'Griffstück', 'Griffstück', 'cyl',
         x=0.25, y=0.25, w=9.5, z=75, h=37, explode=[0, 0, 14], mass=1.3,
         info='Vorderer Teil des Schafts, oft mit gummierter Griffzone. Abschrauben, dann lässt sich die Mine herausnehmen.',
         materials=[['pp', 85], ['tpe', 15]], color='#2A2E31', marks=[mark('cyl', 3, 3, 3.5, fill='#C9A24A')]),
    teil('schaft', 'pen_barrel', 'Schaft', 'Schaft', 'cyl',
         x=0, y=0, w=10, z=0, h=75, explode=[0, 0, 0], mass=2.6,
         info='Hülse aus Polypropylen mit Gewinde oben. Leer gehört der Stift in den Restmüll, weil Mine, Feder und Kunststoff '
              'zu klein zum Sortieren sind.',
         color=BLAU, marks=[mark('cyl', 2, 2, 6, fill='#E4E8EA')]),
]

explodiere(teile, abstand=12)
skaliere_masse(teile, oid='ballpoint_pen', stellen=2)
schreibe('ballpoint_pen', teile)
