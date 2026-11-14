"""3D-Modell: bucket. Erzeugt tools/kategorien/modelle/bucket.json.

Typischer 12-l-Haushaltseimer aus PP (Ø 300 mm, 270 mm hoch, Bügel umgelegt 300 mm) mit konischer Wand,
Literskala, verstärktem Rand mit Ausguss und zwei Ösen, Drahtbügel mit Kunststoff-Griffstück.
Eimerabschnitte bewegen sich gemeinsam, Bügel und Griffstück stapeln darüber.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

EIMER = '#3C7DC4'
INNEN = '#2F6AA8'


def nur_zeichnung(ms):
    """marks nur für die Zeichnung (in der Foto-Ansicht ist der Eimer hohl bzw. der Griff rund)."""
    return [{**m, 'zeichnung': True} for m in ms]


teile = [
    teil('griffstueck', 'steel_handle', 'Griffstück', 'Griffstück', 'box',
         material_id='pp', x=110, y=140, w=80, d=20, z=274, h=18, r=8, mass=12, materials=[['pp', 100]],
         info='Kunststoffgriff auf dem Bügel, damit der Draht nicht in die Hand schneidet. Lässt sich meist '
              'nur abschneiden; kleine Kunststoffreste stören beim Metallrecycling nicht.',
         color='#2B2E31', form='liegend_x', marks=nur_zeichnung(raster(8, 4, 8, 1, 4, 12, 9, fill='#1E2022'))),
    teil('buegel', 'steel_handle', 'Drahtbügel', 'Bügel', 'box',
         x=4, y=148, w=292, d=4, z=270, h=4, r=2, mass=35,
         info='Verzinkter Stahldraht, in die Ösen am Rand eingehängt. Zum Trennen aus den Ösen biegen und zum '
              'Metallschrott geben.',
         color='#B5BBC0', form='liegend_x'),
    teil('rand', 'pp_bucket_body', 'Rand mit Ausguss und Ösen', 'Rand', 'cyl',
         x=0, y=0, w=300, z=255, h=15, mass=70,
         info='Verstärkter Wulstrand, vorn mit Ausguss, seitlich zwei Ösen für den Bügel.',
         color=EIMER, wand=3, marks=nur_zeichnung([mark('cyl', 8, 8, 284, fill='#24548A'),  # Innenwand, von oben gesehen
                             mark('cyl', 80, 80, 200, fill='#1E4877'),  # Schatten tief im Eimer
                             mark('box', 135, 286, 30, 12, 5, '#5893D1')]
         + [mark('box', round(150 + 128 * math.cos(math.radians(a)) - 5, 1), round(150 + 128 * math.sin(math.radians(a)) - 1, 1),
                10, 2, 1, '#6FA3DB') for a in range(205, 250, 9)])),  # Literskala auf der Innenwand
    teil('wand_oben', 'pp_bucket_body', 'Eimerwand oben mit Literskala', 'Wand', 'cyl',
         x=5, y=5, w=290, z=135, h=120, mass=170,
         info='PP, Recyclingcode 5. Innen eine eingeprägte Literskala. Ein Eimer ist keine Verpackung: '
              'kaputte Eimer zum Wertstoffhof. Farb- und Gipsreste vorher ganz austrocknen lassen.',
         color=EIMER, wand=3, marks=[mark('box', 140, 8, 4, 30, 1, '#5893D1', zeichnung=True)]),
    teil('wand_unten', 'pp_bucket_body', 'Eimerwand unten', 'Wand', 'cyl',
         x=15, y=15, w=270, z=10, h=125, mass=150, label=False,
         info='Die Wand wird nach unten enger, so lassen sich Eimer ineinanderstapeln.', color=EIMER, wand=3),
    teil('boden', 'pp_bucket_body', 'Boden mit Standring', 'Boden', 'cyl',
         x=25, y=25, w=250, z=0, h=10, mass=60, label=False,
         info='Boden mit Standring und eingeprägtem Recyclingzeichen.', color=EIMER, wand=3),
]
explodiere(teile, abstand=50, abstaende={'griffstueck': 110, 'buegel': 110}, nach_liste=True, gruppen=[['griffstueck', 'buegel'],
                                                       ['rand', 'wand_oben', 'wand_unten', 'boden']])
skaliere_masse(teile, oid='bucket')
schreibe('bucket', teile)
