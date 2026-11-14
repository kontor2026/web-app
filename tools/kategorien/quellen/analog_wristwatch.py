"""3D-Modell: analog_wristwatch. Erzeugt tools/kategorien/modelle/analog_wristwatch.json.

Analoge Quarzuhr mit Edelstahlgehäuse (Ø 36 mm) und Lederarmband, liegt mit dem Glas nach oben, 12 Uhr hinten (y = 0).
Das Armband ist wie bei der Smartwatch nur mit seinen Ansätzen modelliert (sonst passt die Uhr nicht in die CSV-Maße).
Explodiert: Gehäusemittelteil nach links, Krone nach rechts, Armbandansätze nach hinten und vorne; Boden, Dichtung,
Knopfzelle, Werk, Zifferblatt, Zeiger, Lünette und Glas stapeln sich in der Mitte nach oben.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

STAHL = '#DADDE0'
LEDER = '#6B4226'
ZEIGER = '#2A2E31'
# Mittelpunkt der Uhr
CX, CY = 19, 23
INDEX = [mark('cyl' if i % 3 else 'box', round(15 + 12.5 * math.sin(i * math.pi / 6) - (1 if i % 3 else 0.75), 2),
              round(15 - 12.5 * math.cos(i * math.pi / 6) - (1 if i % 3 else 1.5), 2),
              2 if i % 3 else 1.5, None if i % 3 else 3, 0.3 if i % 3 == 0 else None, '#3A3F44') for i in range(12)]

teile = [
    teil('glas', 'watch_glass', 'Mineralglas', 'Glas', 'cyl',
         x=3, y=7, w=32, z=10.5, h=1.5, mass=2, color='#F2F6F7', opacity=0.5,
         info='Gehärtetes Mineralglas, in die Lünette eingepresst. Nicht herausdrücken: Es gehört mit zum Gehäuse.'),
    teil('luenette', 'steel_watch_case', 'Lünette', 'Lünette', 'cyl',
         x=1, y=5, w=36, z=10, h=1.5, mass=5, materials=[['stahl', 100]], color=STAHL, wand=2, boden=0,
         info='Polierter Edelstahlring um das Glas, auf das Gehäuse gepresst.',
         marks=[mark('cyl', 2, 2, 32, fill='#9DA4A9', zeichnung=True)]),
    teil('sekundenzeiger', 'watch_movement', 'Sekundenzeiger', 'Sekundenzeiger', 'box', material_id='copper',
         x=CX - 0.4, y=CY - 13, w=0.8, d=16, z=9.6, h=0.2, r=0.3, mass=0.05, materials=[['messing', 100]],
         color='#C8423A', info='Dünner Messingzeiger, springt jede Sekunde einen Schritt weiter.'),
    teil('minutenzeiger', 'watch_movement', 'Minutenzeiger', 'Minutenzeiger', 'box', material_id='copper',
         x=CX - 0.8, y=CY - 13, w=1.6, d=14, z=9.3, h=0.2, r=0.6, mass=0.08, materials=[['messing', 100]],
         color=ZEIGER, info='Langer Zeiger, auf das Minutenrohr gesteckt. Mit einem Zeigerheber vorsichtig abziehen.'),
    teil('stundenzeiger', 'watch_movement', 'Stundenzeiger', 'Stundenzeiger', 'box', material_id='copper',
         x=CX - 1, y=CY - 1, w=10, d=2, z=9.0, h=0.2, r=0.8, mass=0.07, materials=[['messing', 100]],
         color=ZEIGER, info='Kurzer, breiter Zeiger. Er dreht sich in 12 Stunden einmal herum (hier auf 3 Uhr).'),
    teil('zifferblatt', 'watch_movement', 'Zifferblatt', 'Zifferblatt', 'cyl', material_id='copper',
         x=4, y=8, w=30, z=8.6, h=0.4, mass=1.2, materials=[['messing', 90], ['druck', 10]], color='#F4F2EE',
         info='Bedrucktes Messingblech mit Stundenmarken, mit zwei Füßchen am Werk eingesteckt.',
         marks=INDEX + [mark('cyl', 14, 14, 2, fill='#2A2E31')]),
    teil('werk', 'watch_movement', 'Quarzwerk', 'Uhrwerk', 'cyl',
         x=6, y=10, w=26, z=3.6, h=5, mass=4.5,
         materials=[['pcabs', 35], ['messing', 25], ['stahl', 15], ['kupfer', 10], ['chip', 10], ['ferrit', 5]],
         color='#9BA3A8',
         info='Kunststoffplatine mit Zahnrädern aus Messing. Ein Schwingquarz gibt 32.768 Schwingungen pro Sekunde vor. '
              'Herausheben, nachdem die Aufzugswelle gezogen ist.',
         marks=[mark('cyl', 9, 9, 8, fill='#B7BCC0'), mark('cyl', 3, 6, 5, fill='#C9A24A'),
                mark('cyl', 17, 13, 4, fill='#C9A24A')]),
    teil('spule', 'watch_movement', 'Schrittmotor mit Spule', 'Spule', 'box',
         x=17, y=28, w=10, d=4, z=1.6, h=2, r=1, mass=0.5, materials=[['kupfer', 60], ['stahl', 30], ['ndfeb', 10]],
         color='#C5803D',
         info='Eine Kupferspule bewegt jede Sekunde einen kleinen Magnetrotor. Über Zahnräder treibt er die Zeiger an.',
         marks=[mark('box', 2, 0.8, 6, 2.4, 1, '#B06F33')]),
    teil('quarz', 'watch_movement', 'Schwingquarz und Steuerchip', 'Quarz', 'box',
         x=10, y=27, w=6, d=3, z=1.6, h=1.5, r=1, mass=0.2, materials=[['chip', 50], ['glas', 20], ['stahl', 30]],
         color='#B7BCC0',
         info='Der winzige Quarz im Metallröhrchen schwingt sehr gleichmäßig, der Chip zählt die Schwingungen.'),
    teil('knopfzelle', 'button_cell', 'Knopfzelle SR626SW', 'Knopfzelle', 'cyl',
         x=12, y=15, w=6.8, z=1.5, h=2.6, mass=0.4, color='#B7BCC0',
         info='Silberoxid-Knopfzelle, hält zwei bis drei Jahre. Deckel öffnen, Zelle abkleben und zur Batteriesammlung bringen.',
         marks=[mark('cyl', 1, 1, 4.8, fill='#9DA6AD')]),
    teil('gehaeuse', 'steel_watch_case', 'Gehäusemittelteil mit Bandanstößen', 'Gehäuse', 'cyl',
         x=1, y=5, w=36, z=1.5, h=8.5, mass=22, materials=[['stahl', 100]], color=STAHL, explode=[-55, 0, 0], wand=3, boden=0,
         info='Edelstahlgehäuse aus einem Stück mit den Hörnern für die Federstege. Leer ist es reiner Stahlschrott.',
         marks=[mark('cyl', 3, 3, 30, fill='#9DA4A9', zeichnung=True)]),
    teil('krone', 'steel_watch_case', 'Krone mit Aufzugswelle', 'Krone', 'box',
         x=34, y=21.5, w=6, d=3, z=4.6, h=3, r=1, form='liegend_x', mass=0.8, materials=[['stahl', 90], ['gummi', 10]], color='#B7BCC0',
         explode=[20, 0, 0],
         info='Ziehen, um die Uhrzeit zu stellen. Zum Ausbau des Werks die Welle nach Drücken eines Hebelchens herausziehen.'),
    teil('dichtung', 'steel_watch_case', 'Dichtungsring', 'Dichtung', 'cyl', material_id='rubber',
         x=4.5, y=8.5, w=29, z=1.3, h=0.3, mass=0.1, materials=[['gummi', 100]], color='#22272B', wand=1, boden=0,
         info='Gummiring zwischen Boden und Gehäuse, hält Wasser und Staub fern.',
         marks=[mark('cyl', 1, 1, 27, fill='#3A3F44', zeichnung=True)]),
    teil('boden', 'steel_watch_case', 'Gehäuseboden', 'Boden', 'cyl',
         x=4, y=8, w=30, z=0, h=1.3, mass=6, materials=[['stahl', 100]], color=STAHL,
         info='Eingedrückter Stahlboden. Mit einem Gehäusemesser an der kleinen Kerbe aufhebeln.',
         marks=[mark('box', 28, 13, 2, 4, 0.5, '#8E969A'), mark('cyl', 7, 7, 16, fill='#B0B6BA')]),
    teil('band_oben', 'leather_strap', 'Lederarmband oben (Ansatz)', 'Armband', 'box',
         x=9, y=0, w=20, d=6, z=3, h=4, r=2, explode=[0, -18, 0], mass=7,
         materials=[['leder', 85], ['stahl', 15]], color=LEDER,
         info='Rindslederband mit Dornschließe, mit Federstegen an den Hörnern befestigt. Federsteg eindrücken, '
              'dann löst sich das Band.',
         marks=[mark('box', 1, 1, 18, 1, 0.5, '#4F301B')]),
    teil('band_unten', 'leather_strap', 'Lederarmband unten (Ansatz)', 'Armband', 'box',
         x=9, y=40, w=20, d=6, z=3, h=4, r=2, explode=[0, 18, 0], mass=7, materials=[['leder', 90], ['stahl', 10]],
         color=LEDER, label=False,
         info='Zweite Bandhälfte mit Löchern. Leder kommt nicht in den Elektroschrott: vorher abnehmen.',
         marks=[mark('box', 1, 4, 18, 1, 0.5, '#4F301B')]),
]

explodiere(teile, abstand=10, abstaende={'sekundenzeiger': 4, 'minutenzeiger': 4, 'stundenzeiger': 4,
                                          'spule': 5, 'quarz': 5, 'knopfzelle': 5, 'dichtung': 5}, nach_liste=True)
skaliere_masse(teile, oid='analog_wristwatch')
for p in teile:  # gerundete Formen (form): marks nur in der Zeichnung, oben flach würden sie schweben
    if p.get('form'):
        p['marks'] = [dict(m, zeichnung=True) for m in p.get('marks') or []]
schreibe('analog_wristwatch', teile)
