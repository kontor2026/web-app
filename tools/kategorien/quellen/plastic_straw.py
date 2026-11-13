"""3D-Modell: plastic_straw. Erzeugt tools/kategorien/modelle/plastic_straw.json.

Typischer Knick-Trinkhalm aus PP (6 mm Durchmesser, 20 cm lang, Wand ca. 0,2 mm), aufrecht stehend:
langes Unterrohr, Faltenbalg-Gelenk, kurzes Mundstück. Die drei Abschnitte sind ein extrudiertes Rohr und werden
zur Erklärung übereinander abgehoben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

FARBE = '#E8505B'
LOCH = [mark('cyl', 0.6, 0.6, 4.8, fill='#7A2A30')]
RILLEN = []
for i in range(10):  # Faltenbalg: abwechselnd Wulst (breit) und Rille (schmal), je 2 mm
    breit = i % 2 == 0
    w = 6.8 if breit else 5.6
    RILLEN.append(teil(f'gelenk_{i}', 'pp_straw', 'Faltenbalg (Knickgelenk)', 'Knickgelenk', 'cyl',
                       x=(6 - w) / 2, y=(6 - w) / 2, w=w, z=158 - 2 * i, h=2, mass=0.012,
                       color='#F07A83' if breit else '#D64550', label=(i == 0),
                       marks=[mark('cyl', (w - 4.8) / 2, (w - 4.8) / 2, 4.8, fill='#7A2A30')] if i == 0 else None,
                       info='Eingeprägte Rillen wie bei einer Ziehharmonika. Dadurch lässt sich der Halm knicken, '
                            'ohne dass er zusammenfällt.' if i == 0 else 'Eine Falte des Knickgelenks.'))

teile = [
    teil('mundstueck', 'pp_straw', 'Mundstück', 'Mundstück', 'cyl',
         x=0, y=0, w=6, z=160, h=40, mass=0.2, color=FARBE, marks=LOCH,
         info='Kurzes oberes Rohrstück aus Polypropylen. Einweg-Trinkhalme aus Kunststoff sind in der EU seit 2021 '
              'verboten, Reste bitte in den Restmüll.'),
    *RILLEN,
    teil('rohr', 'pp_straw', 'Unterrohr', 'Rohr', 'cyl',
         x=0, y=0, w=6, z=0, h=140, mass=0.68, color=FARBE, marks=LOCH,
         info='Dünnwandiges Rohr. Für die Sortieranlage ist es zu klein und leicht, es landet meist im Restmüll. '
              'Besser: Halme aus Glas oder Edelstahl wiederverwenden.'),
]
explodiere(teile, abstand=15, gruppen=[[p['id'] for p in RILLEN]])
skaliere_masse(teile, oid='plastic_straw', stellen=3)
schreibe('plastic_straw', teile)
