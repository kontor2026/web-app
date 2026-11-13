"""3D-Modell: paint_bucket. Erzeugt tools/kategorien/modelle/paint_bucket.json.

Typischer 5-l-Farbeimer aus PP (Ø 200 mm, 220 mm hoch mit Deckel) mit leicht konischer Wand, verstärktem Rand
mit Ösen, Schnappdeckel mit Originalitätslaschen, Drahtbügel mit Kunststoff-Griffstück und In-Mould-Etikett.
Eimerabschnitte bewegen sich gemeinsam, Deckel und Bügel stapeln darüber, das Etikett wird seitlich gezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

EIMER = '#F4F4F1'
teile = [
    teil('griffstueck', 'steel_handle', 'Griffstück', 'Griffstück', 'box',
         material_id='pp', x=80, y=93, w=40, d=14, z=215, h=5, r=6, mass=6, materials=[['pp', 100]],
         info='Kunststoffrolle auf dem Bügel, damit der Draht nicht in die Hand schneidet.',
         color='#2F6DB5', marks=raster(6, 5, 7, 1, 2, 4, 4.5, fill='#285E9C')),
    teil('buegel', 'steel_handle', 'Drahtbügel', 'Bügel', 'box',
         x=2, y=98, w=196, d=4, z=212, h=3, r=1.5, mass=30,
         info='Verzinkter Stahldraht, in die Ösen am Rand eingehängt. Zum Trennen aushaken: Er gehört zum '
              'Metallschrott oder in die Gelbe Tonne.',
         color='#9DA4AA'),
    teil('deckel', 'pp_lid', 'Schnappdeckel', 'Deckel', 'cyl',
         x=0, y=0, w=200, z=196, h=16, mass=85,
         info='Schnappt über den Rand, Originalitätslaschen zeigen, dass der Eimer noch zu ist. Laschen abreißen '
              'und den Deckel mit einem Schraubendreher aufhebeln.',
         color=EIMER, marks=[mark('cyl', 10, 10, 180, fill='#E6E6E1'), mark('cyl', 50, 50, 100, fill='#DADAD4')]
         + raster(94, 2, 2, 1, 6, 6, 6, fill='#2F6DB5')),
    teil('rand', 'pp_bucket_body', 'Rand mit Ösen', 'Rand', 'cyl',
         x=0, y=0, w=200, z=186, h=14, mass=45,
         info='Verstärkter Rand mit Rastwulst für den Deckel und zwei Ösen für den Bügel.',
         color=EIMER, marks=[mark('cyl', 6, 6, 188, fill='#E2E2DD')]),
    teil('wand_oben', 'pp_bucket_body', 'Eimerwand oben', 'Wand', 'cyl',
         x=2, y=2, w=196, z=96, h=90, mass=110,
         info='Spritzgegossenes PP, Recyclingcode 5. Nur ganz leere Eimer mit trockenen Resten in die Gelbe '
              'Tonne. Flüssige Farbreste sind Sondermüll (Schadstoffmobil, Wertstoffhof).',
         color=EIMER),
    teil('wand_unten', 'pp_bucket_body', 'Eimerwand unten', 'Wand', 'cyl',
         x=6, y=6, w=188, z=8, h=88, mass=95,
         info='Die Wand wird nach unten etwas enger, so lassen sich leere Eimer ineinanderstapeln.',
         color=EIMER, label=False),
    teil('boden', 'pp_bucket_body', 'Eimerboden', 'Boden', 'cyl',
         x=9, y=9, w=182, z=0, h=8, mass=30,
         info='Boden mit Standring und Recyclingzeichen 5.', color=EIMER, label=False),
    teil('etikett', 'pp_bucket_body', 'In-Mould-Etikett', 'Etikett', 'box',
         x=198, y=50, w=0.3, d=100, z=30, h=150, r=0, explode=[70, 0, 0], mass=4,
         materials=[['pp', 92], ['druck', 8]],
         info='Bedruckte PP-Folie, die beim Spritzgießen mit der Wand verschmolzen wird. Nicht ablösbar, '
              'muss aber auch nicht: Sie ist aus demselben Kunststoff.',
         color='#2F6DB5', sortBias=100),
]
explodiere(teile, abstand=40, nach_liste=True, gruppen=[['griffstueck', 'buegel'], ['rand', 'wand_oben', 'wand_unten', 'boden']])
skaliere_masse(teile, oid='paint_bucket')
schreibe('paint_bucket', teile)
