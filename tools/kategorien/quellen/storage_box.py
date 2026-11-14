"""3D-Modell: storage_box. Erzeugt tools/kategorien/modelle/storage_box.json.

Stapelbare Aufbewahrungsbox (etwa 20 l) aus PP mit aufgelegtem Deckel und zwei Klappverschlüssen an den Schmalseiten.
Die Wand verjüngt sich nach unten (Stapeln ineinander). Box-Abschnitte bewegen sich gemeinsam, der Deckel schwebt
darüber, die Klappverschlüsse werden seitlich, das Papieretikett auf dem Deckel hebt nach oben ab.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

BOX = '#E8ECEE'
BLAU = '#2F6DB5'

teile = [
    teil('etikett', 'pp_storage_box', 'Papieretikett', 'Etikett', 'box',
         material_id='paper', x=120, y=110, w=150, d=70, z=220, h=0.3, r=2, mass=4,
         materials=[['papier', 85], ['druck', 5], ['klebstoff', 10]],
         info='Aufgeklebtes Verkaufsetikett auf dem Deckel. Vor dem Abgeben abziehen, es stört beim Kunststoffrecycling.',
         color='#F7F3E6', marks=[mark('box', 10, 10, 130, 12, 1, '#2F6DB5'), mark('box', 10, 32, 90, 6, 1, '#8A9298'),
                                 mark('box', 10, 46, 60, 6, 1, '#8A9298'), mark('box', 112, 40, 28, 22, 1, '#22272B')]),
    teil('deckel', 'pp_lid', 'Deckel', 'Deckel', 'box',
         x=2, y=2, w=386, d=286, z=204, h=16, r=18, mass=300,
         info='Spritzgegossenes PP mit Versteifungsrippen und Stapelrand. Einfach abheben; '
              'sauber und ohne Etikett zum Wertstoffhof (Hartkunststoff).',
         color=BLAU, opacity=0.9,
         marks=[mark('box', 16, 16, 354, 254, 12, '#2A62A3')] + raster(40, 40, 6, 1, 4, 206, 60, r=2, fill='#3A79C2')),
    teil('clip_links', 'pp_lid', 'Klappverschluss links', 'Verschluss', 'box', label=False,
         x=0, y=95, w=7, d=100, z=150, h=62, r=2, explode=[-45, 0, 0], mass=25,
         info='Klappt über den Deckelrand und hält ihn fest. Er hängt mit Zapfen am Rand und lässt sich '
              'mit etwas Kraft aushebeln.',
         color=BLAU, marks=[mark('box', 1, 10, 5, 80, 2, '#2A62A3')]),
    teil('clip_rechts', 'pp_lid', 'Klappverschluss rechts', 'Verschluss', 'box',
         x=383, y=95, w=7, d=100, z=150, h=62, r=2, explode=[45, 0, 0], mass=25,
         info='Zweiter Verschluss an der anderen Schmalseite. Auch er ist aus PP und darf mit der Box zusammenbleiben.',
         color=BLAU, marks=[mark('box', 1, 10, 5, 80, 2, '#2A62A3')]),
    teil('rand', 'pp_storage_box', 'Rand mit Griffleisten', 'Rand', 'box',
         x=0, y=0, w=390, d=290, z=188, h=16, r=20, mass=180,
         info='Verstärkter Rand mit Griffmulden an den Schmalseiten. Hier sind die Verschlüsse eingehängt.',
         color=BOX, opacity=0.8, wand=3, marks=[mark('box', 8, 8, 374, 274, 16, '#D5DADD', zeichnung=True)]),
    teil('wand_oben', 'pp_storage_box', 'Boxwand oben', 'Box', 'box',
         x=8, y=8, w=374, d=274, z=100, h=88, r=18, mass=260,
         info='Durchsichtiges PP, Recyclingcode 5. Große Hartkunststoffteile gehören zum Wertstoffhof, '
              'nicht in die Gelbe Tonne: Sie sind keine Verpackung.',
         color=BOX, opacity=0.8, label=True, wand=3),
    teil('wand_unten', 'pp_storage_box', 'Boxwand unten', 'Box unten', 'box',
         x=14, y=14, w=362, d=262, z=12, h=88, r=16, mass=240,
         info='Die Wand wird nach unten schmaler, so passen leere Boxen ineinander.',
         color=BOX, opacity=0.8, label=False, wand=3),
    teil('boden', 'pp_storage_box', 'Boden mit Standfüßen', 'Boden', 'box',
         x=20, y=20, w=350, d=250, z=0, h=12, r=14, mass=150,
         info='Boden mit Stapelnoppen und Recyclingzeichen 5.', color=BOX, opacity=0.8, label=False, wand=3,
         marks=raster(20, 20, 2, 2, 30, 30, 280, 180, r=6, fill='#CDD3D6')),
]

explodiere(teile, abstand=60, abstaende={'deckel': 110, 'etikett': 90}, gruppen=[['rand', 'wand_oben', 'wand_unten', 'boden']])
skaliere_masse(teile, oid='storage_box')
schreibe('storage_box', teile)
