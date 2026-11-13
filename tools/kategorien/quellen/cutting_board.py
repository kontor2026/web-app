"""3D-Modell: cutting_board. Erzeugt tools/kategorien/modelle/cutting_board.json.

Typisches Küchenbrett aus Buchen-Leimholz (25 × 38 cm, 16 mm dick) mit Saftrille und vier Gummifüßen.
Das Brett besteht aus vier verleimten Holzleisten; explodiert schweben die Leisten über den Füßen und rücken
leicht auseinander, damit man die Leimfugen sieht.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

HOLZ = ('#D9B48A', '#CFA97E', '#DDBA92', '#D3AE84')
RILLE = '#B88E62'
MASER = '#C49A6C'
B, T, LW = 250, 380, 62.5


def rille(i):
    """Saftrille (6 mm breit, 12 mm vom Rand) als marks auf Leiste i."""
    x0 = i * LW
    a, e = max(12 - x0, 0), min(238 - x0, LW)
    m = [mark('box', a, 12, e - a, 6, fill=RILLE), mark('box', a, T - 18, e - a, 6, fill=RILLE)]
    if i == 0:
        m.append(mark('box', 12, 12, 6, T - 24, fill=RILLE))
    if i == 3:
        m.append(mark('box', 232 - x0, 12, 6, T - 24, fill=RILLE))
    # Maserung: feine Linien längs der Leiste, innerhalb der Saftrille
    for k, gx in enumerate((14, 31, 47)):
        x = gx + (i * 5) % 9
        if 22 - x0 <= x <= 226 - x0 or i in (1, 2):
            m.append(mark('box', x, 26 + 9 * k, 0.8, T - 52 - 18 * k, fill=MASER))
    return m


INFO = [
    'Massive Buchenleiste. Holz wirkt leicht keimhemmend. Ein abgenutztes Brett kann man abschleifen, neu einölen '
    'und weiter benutzen.',
    'Die Leisten sind mit wasserfestem Leim verbunden. Deshalb gehört ein altes Brett nicht in den Kompost, '
    'sondern zum Altholz am Wertstoffhof oder in den Restmüll.',
    'Die Jahresringe der Leisten liegen abwechselnd, damit sich das Brett nicht verzieht.',
    'Die umlaufende Saftrille fängt Fleisch- und Obstsaft auf.',
]
teile = [
    teil(f'leiste_{i + 1}', 'wooden_board', f'Holzleiste {i + 1}', 'Holzleiste' if i == 0 else f'Leiste {i + 1}', 'box',
         x=i * LW, y=0, w=LW, d=T, z=4, h=16, r=6 if i in (0, 3) else 0, explode=[(i - 1.5) * 16, 0, 75],
         mass=270, materials=[['holz', 98], ['klebstoff', 2]], info=INFO[i], color=HOLZ[i], marks=rille(i),
         label=i in (0, 1))
    for i in range(4)
]
for n, (fx, fy) in enumerate([(15, 20), (217, 20), (15, 342), (217, 342)]):
    teile.append(teil(f'fuss_{n + 1}', 'wooden_board', 'Gummifuß', 'Gummifuß', 'cyl', material_id='rubber',
                      x=fx, y=fy, w=18, z=0, h=4, explode=[0, 0, 0], mass=3, label=n == 3,
                      info='Rutschfester Gummipuffer, mit einer kleinen Edelstahlschraube festgeschraubt. Vor dem '
                           'Entsorgen abschrauben: Gummi kommt in den Restmüll.',
                      materials=[['gummi', 85], ['stahl', 15]], color='#3A3D40',
                      marks=[mark('cyl', 6.5, 6.5, 5, fill='#9AA2A6')]))
for n, (fx, fy) in enumerate([(15, 20), (217, 20), (15, 342), (217, 342)]):
    teile.append(teil(f'schraube_{n + 1}', 'wooden_board', 'Edelstahlschraube', 'Schraube', 'cyl',
                      material_id='steel', x=fx + 7, y=fy + 7, w=4, z=1, h=12, explode=[0, 0, 28], mass=0.8,
                      label=n == 2, materials=[['stahl', 100]], color='#9DA4AA',
                      marks=[mark('cyl', 0.5, 0.5, 3, fill='#6E757B')],
                      info='Kleine Edelstahlschraube, die den Gummifuß von unten ins Holz hält. Sie rostet nicht, '
                           'auch wenn das Brett oft nass wird.'))
skaliere_masse(teile, oid='cutting_board')
schreibe('cutting_board', teile)
