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

LEISTE_INFO = 'Rahmenleiste aus Kiefernholz, lackiert.'
PROFIL = '#A87A4A'


def leiste(id, x, y, w, d, mass, **kw):
    """Eine der vier Rahmenleisten; die Marks zeichnen die Profilkanten auf der Vorderseite."""
    lang = d > w
    marks = ([mark('box', 3, 3, w - 6, d - 6, 1, '#C39565'), mark('box', w - 5, 5, 2, d - 10, 0.5, PROFIL)] if lang else
             [mark('box', 0, 3, w, d - 6, 1, '#C39565'), mark('box', 0, d - 5, w, 2, 0.5, PROFIL)])
    if id == 'leiste_r':
        marks[1] = mark('box', 3, 5, 2, d - 10, 0.5, PROFIL)
    if id == 'leiste_o':
        marks[1] = mark('box', 0, 3, w, 2, 0.5, PROFIL)
    return teil(id, 'wooden_frame', 'Holzrahmen', 'Rahmen', 'box', x=x, y=y, w=w, d=d, z=0, h=20, r=1,
                mass=mass, color=HOLZ, marks=marks, **kw)


FOTO = [mark('box', 0, 0, 100, 60, 0, '#A9C9DF'), mark('cyl', 70, 8, 16, fill='#F4E3A1'),
        mark('box', 0, 60, 100, 90, 0, '#6E9A5E'), mark('box', 0, 60, 100, 6, 0, '#5A8650'),
        mark('cyl', 18, 40, 30, 26, fill='#4F7A47')]

teile = [
    leiste('leiste_l', 0, 0, 20, 230, 50,
           info='Leiste aus Kiefernholz, lackiert und an den Ecken auf Gehrung verleimt. Hinten hat sie einen Falz, '
                'in dem Glas, Bild und Rückwand liegen. Ohne Glas und Metall kann sie zum Altholz.'),
    leiste('leiste_r', 160, 0, 20, 230, 50, label=False, info=LEISTE_INFO),
    leiste('leiste_o', 20, 0, 140, 20, 35, label=False, info=LEISTE_INFO),
    leiste('leiste_u', 20, 210, 140, 20, 35, label=False, info=LEISTE_INFO),
    teil('glas', 'frame_glass', 'Glasscheibe', 'Glas', 'box',
         x=15, y=15, w=150, d=200, z=8, h=2, r=0.5, mass=150,
         info='Dünnes Flachglas, 2 mm dick. Gehört nicht in den Altglascontainer: in Zeitungspapier wickeln und in '
              'den Restmüll geben. Vorsicht, die Kanten sind scharf.',
         color='#D6E8EE', opacity=0.35),
    teil('passepartout', 'cardboard_backing', 'Passepartout', 'Passepartout', 'box',
         material_id='cardboard', x=15, y=15, w=150, d=200, z=6.5, h=1.5, r=0.5, mass=18,
         info='Karton mit ausgeschnittenem Fenster, er setzt das Bild vom Glas ab. Sauber ins Altpapier.',
         color='#F3F0E8', marks=[mark('box', 24, 24, 102, 152, 0, '#DCD7CB')]
         + [dict(m, x=m['x'] + 25, y=m['y'] + 25) for m in FOTO]),
    teil('foto', 'cardboard_backing', 'Fotoabzug', 'Foto', 'box',
         material_id='paper', x=25, y=30, w=130, d=170, z=6.2, h=0.3, r=0, mass=4,
         materials=[['papier', 90], ['druck', 10]],
         info='Fotopapier mit Kunststoffbeschichtung. Herausnehmen und behalten, das Bild gehört nicht zum Müll.',
         color='#F7F7F4', marks=[dict(m, x=m['x'] + 15, y=m['y'] + 10) for m in FOTO]),
    teil('rueckwand', 'cardboard_backing', 'Rückwand aus Hartpappe', 'Rückwand', 'box',
         x=15, y=15, w=150, d=200, z=3.2, h=3, r=0.5, mass=55,
         info='Graue Hartpappe mit einem Aufsteller zum Hinstellen. Nach dem Aufdrehen der Klammern herausheben, '
              'dann ins Altpapier.',
         color='#8C8478', marks=[mark('box', 60, 70, 30, 120, 2, '#7A7266'), mark('box', 70, 72, 10, 3, 1, '#5F584E')]),
    teil('klammer_l', 'wooden_frame', 'Drehklammer', 'Klammer', 'box',
         material_id='steel', x=9, y=108, w=14, d=14, z=1.5, h=1.5, r=1, mass=1, explode=[0, 130, 0],
         info=KLAMMER_INFO, color=METALL, marks=[mark('cyl', 4, 4, 6, fill='#7D858B')]),
    teil('klammer_r', 'wooden_frame', 'Drehklammer', 'Klammer', 'box',
         material_id='steel', x=157, y=108, w=14, d=14, z=1.5, h=1.5, r=1, mass=1, label=False, explode=[0, 130, 0],
         info=KLAMMER_INFO, color=METALL, marks=[mark('cyl', 4, 4, 6, fill='#7D858B')]),
    teil('klammer_u', 'wooden_frame', 'Drehklammer', 'Klammer', 'box',
         material_id='steel', x=83, y=208, w=14, d=14, z=1.5, h=1.5, r=1, mass=1, label=False, explode=[0, 30, 0],
         info=KLAMMER_INFO, color=METALL, marks=[mark('cyl', 4, 4, 6, fill='#7D858B')]),
    teil('aufhaenger', 'wooden_frame', 'Zackenaufhänger', 'Aufhänger', 'box',
         material_id='steel', x=75, y=4, w=30, d=8, z=0, h=1.5, r=0.5, mass=3, explode=[0, 256, 0],
         info='Gezacktes Blech, mit zwei kleinen Nägeln auf die Leiste genagelt. Mit einer Zange abziehen, '
              'dann zum Metallschrott.',
         color=METALL, marks=raster(2, 1, 9, 1, 2, 3, 3, fill='#7D858B')),
]
explodiere(teile, abstand=40, nach_liste=True, gruppen=[['leiste_l', 'leiste_r', 'leiste_o', 'leiste_u']])
skaliere_masse(teile, oid='picture_frame')
schreibe('picture_frame', teile)
