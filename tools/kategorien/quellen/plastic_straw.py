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
teile = [
    teil('mundstueck', 'pp_straw', 'Mundstück', 'Mundstück', 'cyl',
         x=0, y=0, w=6, z=160, h=40, mass=0.2, color=FARBE, marks=LOCH,
         info='Kurzes oberes Rohrstück aus Polypropylen. Einweg-Trinkhalme aus Kunststoff sind in der EU seit 2021 '
              'verboten, Reste bitte in den Restmüll.'),
    teil('gelenk', 'pp_straw', 'Faltenbalg (Knickgelenk)', 'Knickgelenk', 'cyl',
         x=0, y=0, w=6, z=140, h=20, mass=0.12, color='#F07A83',
         marks=[mark('cyl', 0.3, 0.3, 5.4, fill='#D64550')] + LOCH,
         info='Eingeprägte Rillen wie bei einer Ziehharmonika. Dadurch lässt sich der Halm knicken, ohne dass er '
              'zusammenfällt.'),
    teil('rohr', 'pp_straw', 'Unterrohr', 'Rohr', 'cyl',
         x=0, y=0, w=6, z=0, h=140, mass=0.68, color=FARBE, marks=LOCH,
         info='Dünnwandiges Rohr. Für die Sortieranlage ist es zu klein und leicht, es landet meist im Restmüll. '
              'Besser: Halme aus Glas oder Edelstahl wiederverwenden.'),
]
explodiere(teile, abstand=15)
skaliere_masse(teile, oid='plastic_straw', stellen=2)
schreibe('plastic_straw', teile)
