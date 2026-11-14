"""3D-Modell: picture_frame. Erzeugt tools/kategorien/modelle/picture_frame.json.

Typischer Bilderrahmen 13 × 18 cm Bildmaß (außen 180 × 230 mm, 20 mm hoch) mit Holzleiste, Glasscheibe,
Passepartout, Foto, Rückwand aus Hartpappe, vier Drehklammern und Zackenaufhänger. Liegt mit der Vorderseite
nach oben; explodiert schwebt der Rahmen über Glas, Passepartout, Foto und Rückwand, Klammern und Aufhänger
liegen unten.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

HOLZ = '#B98A57'
METALL = '#A9AFB4'
KLAMMER_INFO = 'Drehklammer aus Federstahl. Zur Seite drehen, dann lässt sich die Rückwand herausnehmen.'

teile = [
    teil('rahmen', 'wooden_frame', 'Holzrahmen', 'Rahmen', 'box',
         x=0, y=0, w=180, d=230, z=0, h=20, r=2, mass=170,
         info='Leiste aus Kiefernholz, lackiert und an den Ecken auf Gehrung verleimt. Hinten hat sie einen Falz, '
              'in dem Glas, Bild und Rückwand liegen. Ohne Glas und Metall kann sie zum Altholz.',
         color=HOLZ, marks=[mark('box', 6, 6, 168, 218, 1, '#A37548'), mark('box', 20, 20, 140, 190, 0.5, '#E9EEF0')]),
    teil('glas', 'frame_glass', 'Glasscheibe', 'Glas', 'box',
         x=15, y=15, w=150, d=200, z=6.8, h=2, r=0.5, mass=150,
         info='Dünnes Flachglas, 2 mm dick. Gehört nicht in den Altglascontainer: in Zeitungspapier wickeln und in '
              'den Restmüll geben. Vorsicht, die Kanten sind scharf.',
         color='#CFE3EA', opacity=0.6),
    teil('passepartout', 'cardboard_backing', 'Passepartout', 'Passepartout', 'box',
         material_id='cardboard', x=15, y=15, w=150, d=200, z=5.3, h=1.5, r=0.5, mass=18,
         info='Karton mit ausgeschnittenem Fenster, er setzt das Bild vom Glas ab. Sauber ins Altpapier.',
         color='#F3F0E8', marks=[mark('box', 25, 25, 100, 150, 0, '#DCD7CB')]),
    teil('foto', 'cardboard_backing', 'Fotoabzug', 'Foto', 'box',
         material_id='paper', x=25, y=30, w=130, d=170, z=5, h=0.3, r=0, mass=4,
         materials=[['papier', 90], ['druck', 10]],
         info='Fotopapier mit Kunststoffbeschichtung. Herausnehmen und behalten, das Bild gehört nicht zum Müll.',
         color='#7FA6C4', marks=[mark('box', 10, 10, 110, 70, 0, '#A9C9DF'), mark('box', 10, 85, 110, 75, 0, '#5E8A5A')]),
    teil('rueckwand', 'cardboard_backing', 'Rückwand aus Hartpappe', 'Rückwand', 'box',
         x=15, y=15, w=150, d=200, z=2.5, h=2.5, r=0.5, mass=55,
         info='Graue Hartpappe mit einem Aufsteller zum Hinstellen. Nach dem Lösen der Klammern herausheben, '
              'dann ins Altpapier.',
         color='#8C8478', marks=[mark('box', 60, 90, 30, 100, 2, '#7A7266')]),
    teil('klammer_l', 'wooden_frame', 'Drehklammer', 'Klammer', 'box',
         material_id='steel', x=9, y=108, w=14, d=14, z=1.5, h=1, r=1, mass=1,
         info=KLAMMER_INFO, color=METALL, marks=[mark('cyl', 4, 4, 6, fill='#7D858B')]),
    teil('klammer_r', 'wooden_frame', 'Drehklammer', 'Klammer', 'box',
         material_id='steel', x=157, y=108, w=14, d=14, z=1.5, h=1, r=1, mass=1, label=False,
         info=KLAMMER_INFO, color=METALL, marks=[mark('cyl', 4, 4, 6, fill='#7D858B')]),
    teil('klammer_u', 'wooden_frame', 'Drehklammer', 'Klammer', 'box',
         material_id='steel', x=83, y=208, w=14, d=14, z=1.5, h=1, r=1, mass=1, label=False,
         info=KLAMMER_INFO, color=METALL, marks=[mark('cyl', 4, 4, 6, fill='#7D858B')]),
    teil('aufhaenger', 'wooden_frame', 'Zackenaufhänger', 'Aufhänger', 'box',
         material_id='steel', x=75, y=4, w=30, d=8, z=0, h=1.5, r=0.5, mass=3,
         info='Gezacktes Blech, mit zwei kleinen Nägeln auf die Leiste genagelt. Mit einer Zange abziehen, '
              'dann zum Metallschrott.',
         color=METALL, marks=raster(2, 1, 9, 1, 2, 3, 3, fill='#7D858B')),
]
explodiere(teile, abstand=80, nach_liste=True, gruppen=[['klammer_l', 'klammer_r', 'klammer_u']])
skaliere_masse(teile, oid='picture_frame')
schreibe('picture_frame', teile)
