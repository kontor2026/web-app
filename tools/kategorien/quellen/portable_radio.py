"""3D-Modell: portable_radio. Erzeugt tools/kategorien/modelle/portable_radio.json.

Typisches UKW/MW-Kofferradio für Batterien (220 × 80 × 130 mm), steht aufrecht, Lautsprecher vorne (y groß).
Oben Tragegriff, Drehknöpfe und eingeklappte Teleskopantenne. Innen: Lautsprecher mit Magnet, senkrechte
Platine mit Drehkondensator, Ferritstab-Antenne für Mittelwelle, unten hinten vier Babyzellen (C).
Explosion: Frontschale nach vorne (dy > 0), Rückschale nach hinten (dy < 0), Griff, Knöpfe und Antenne nach oben,
die Antenne zusätzlich nach rechts (dx > 0). Das Innenleben bleibt an seinem Platz.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

GEH = '#3A3D40'
FRONT = [-50, 140, 0]  # Frontschale nach vorne links, damit das Innenleben frei liegt
GITTER = [-50, 185, 0]
OBEN = 50  # Griff, Knöpfe und Antenne heben so weit ab
C_ZELLE = [['zinkmangan', 80], ['stahl', 20]]

teile = [
    teil('griff', 'plastic_housing', 'Tragegriff', 'Griff', 'box',
         x=40, y=30, w=140, d=20, z=112, h=18, r=8, explode=[0, 0, OBEN], mass=30,
         info='Kunststoffbügel, innen mit zwei Schrauben am Gehäuse befestigt. Zuerst abschrauben.',
         color='#2B2E31', marks=[mark('box', 10, 6, 120, 8, 4, '#3A3D40')]),
    teil('antenne', 'telescopic_antenna', 'Teleskopantenne', 'Antenne', 'box',
         x=30, y=4, w=170, d=8, z=112, h=8, r=4, explode=[40, 0, OBEN], form='liegend_x', mass=25,
         materials=[['stahl', 85], ['messing', 10], ['pcabs', 5]],
         info='Ineinandergeschobene Röhrchen aus verchromtem Stahl für den UKW-Empfang. Innen im Gehäuse mit '
              'einer Mutter festgeschraubt.',
         color='#E2E5E7', marks=raster(30, 1.5, 4, 1, 1.5, 5, 35, r=0.5, fill='#8A939A')),
    teil('knoepfe', 'plastic_housing', 'Drehknöpfe (Sender und Lautstärke)', 'Drehknöpfe', 'box',
         x=150, y=52, w=56, d=22, z=112, h=8, r=3, explode=[0, 30, OBEN], mass=8,
         info='Gerändelte Kunststoffknöpfe, nur auf die Achsen gesteckt. Lassen sich mit den Fingern abziehen.',
         color='#2B2E31', marks=[mark('cyl', 2, 2, 18, fill='#4A4F54'), mark('cyl', 34, 2, 18, fill='#4A4F54'),
                                 mark('box', 10, 3, 2, 6, 1, '#E35A4E')]),
    *[teil(f'gitter{i}', 'plastic_housing', 'Lautsprechergitter (Metallstreben)', 'Gitter', 'box',
           material_id='steel', x=14, y=80, w=104, d=1.5, z=12 + i * 11.5, h=7, r=0.5, mass=3,
           materials=[['stahl', 100]], explode=GITTER, sortBias=150, label=i == 0, color='#A7ADB2',
           info='Gelochtes Stahlblech schützt die Membran. In die Frontschale geklipst, mit einem Schraubendreher '
                'heraushebeln. Wertvoll als Stahlschrott.') for i in range(8)],
    teil('skala', 'plastic_housing', 'Senderskala mit Fenster', 'Skala', 'box',
         material_id='pc', x=132, y=80, w=78, d=1, z=58, h=38, r=1, mass=6, materials=[['pcabs', 90], ['druck', 10]],
         explode=FRONT, sortBias=150, color='#E8E2C8',
         info='Bedruckte Skala mit Frequenzen hinter einem Klarsichtfenster. Der Zeiger zeigt den eingestellten Sender.'),
    teil('zeiger', 'plastic_housing', 'Senderzeiger', 'Zeiger', 'box',
         x=168, y=81, w=1.5, d=1, z=60, h=34, mass=0.5, explode=FRONT, sortBias=160, color='#E35A4E',
         info='Roter Kunststoffzeiger, wird über einen Seilzug vom Senderknopf bewegt.'),
    *[teil(f'strich{i}', 'plastic_housing', 'Skalenstrich', 'Strich', 'box',
           x=138 + i * 9, y=81, w=0.8, d=0.5, z=84, h=8, mass=0.1, explode=FRONT, sortBias=155, label=False,
           color='#55493C', info='Aufgedruckter Skalenstrich.') for i in range(8)],
    teil('frontschale', 'plastic_housing', 'Frontschale mit Lautsprechergitter', 'Frontschale', 'box',
         x=0, y=52, w=220, d=28, z=0, h=112, r=10, mass=125,
         info='Vorderes Gehäuseteil aus ABS mit Lochgitter vor dem Lautsprecher und Senderskala. '
              'Hinten sitzen 4 bis 6 Schrauben, oft im Batteriefach versteckt.',
         explode=FRONT, color=GEH,
         marks=[mark('box', 6, 6, 208, 16, 6, '#34383C'), mark('box', 18, 8, 40, 8, 3, '#2B2E31'),
                mark('box', 30, 9, 10, 6, 2, '#B7BCC0'), mark('cyl', 112, 9, 5, fill='#4CC26A')]),
    teil('poti', 'circuit_board', 'Lautstärkeregler (Potentiometer)', 'Poti', 'cyl',
         material_id='mixed_electronics', x=186, y=56, w=14, z=94, h=14, mass=4,
         materials=[['pcabs', 40], ['stahl', 30], ['messing', 15], ['kupfer', 10], ['graphit', 5]],
         info='Drehwiderstand unter dem Lautstärkeknopf. Eine Kohlebahn ändert den Widerstand und damit die Lautstärke.',
         explode=[0, 30, 30], color='#5A6066', marks=[mark('cyl', 4, 4, 6, fill='#C9CDD0')]),
    teil('schrauben', 'plastic_housing', 'Gehäuseschrauben (6 Stück)', 'Schrauben', 'cyl',
         material_id='steel', x=8, y=60, w=6, z=100, h=10, mass=6, materials=[['stahl', 100]],
         info='Halten Front- und Rückschale zusammen. Kreuzschlitz, oft unter dem Batteriedeckel versteckt.',
         explode=[0, 0, 40], color='#9AA0A6', marks=[mark('cyl', 1, 1, 4, fill='#5F666C')]),
    teil('lautsprecher', 'speaker_driver', 'Lautsprecher (100 mm)', 'Lautsprecher', 'box',
         x=15, y=40, w=100, d=12, z=6, h=100, r=6, mass=55,
         materials=[['papier', 25], ['stahl', 50], ['kupfer', 10], ['gummi', 10], ['pcabs', 5]],
         info='Membran aus Pappe in einem Stahlkorb. Sie schwingt und erzeugt den Ton, angetrieben von der '
              'Schwingspule. Mit vier Schrauben an der Frontschale.',
         color='#2E2B28', marks=[mark('box', 6, 2, 88, 8, 4, '#3E3830')]),
    teil('magnet', 'speaker_driver', 'Ferritmagnet des Lautsprechers', 'Magnet', 'cyl',
         material_id='mixed_electronics', x=45, y=26, w=40, d=14, z=36, h=40, form='liegend_y', mass=95,
         materials=[['ferrit', 80], ['stahl', 15], ['kupfer', 5]],
         info='Schwerer Ringmagnet aus Ferrit hinter der Membran. Zieht Schrauben und Büroklammern an.',
         color='#4A4F54', marks=[mark('cyl', 8, 3, 24, 8, fill='#8A939A')]),
    teil('ferritstab', 'circuit_board', 'Ferritstab-Antenne (Mittelwelle)', 'Ferritantenne', 'box',
         material_id='mixed_electronics', x=20, y=14, w=110, d=10, z=92, h=10, r=4, form='liegend_x', mass=18,
         materials=[['ferrit', 75], ['kupfer', 20], ['pcabs', 5]],
         info='Stab aus Ferrit mit Kupferwicklung. Empfängt Mittelwelle, deshalb funktioniert MW auch ohne '
              'ausgezogene Antenne.',
         color='#3A3F44', marks=[mark('box', 30, 1, 22, 8, 2, '#C5803D'), mark('box', 62, 1, 12, 8, 2, '#C5803D')]),
    teil('drehko', 'circuit_board', 'Drehkondensator (Senderwahl)', 'Drehko', 'box',
         material_id='mixed_electronics', x=150, y=32, w=22, d=12, z=60, h=22, r=1, mass=10,
         materials=[['alu', 45], ['pcabs', 40], ['stahl', 10], ['kupfer', 5]],
         info='Plattenpaket, das beim Drehen am Senderknopf ineinander greift. So wird der Sender eingestellt.',
         color='#E8E8E2', marks=[mark('cyl', 6, 1, 10, fill='#B7BCC0')]),
    teil('chip', 'circuit_board', 'Radio-Chip', 'Chip', 'box',
         material_id='pcb', x=180, y=32, w=12, d=4, z=40, h=12, r=0.3, mass=2, materials=[['chip', 100]],
         info='Ein einziger Chip empfängt, verstärkt und dekodiert das Radiosignal.', color='#22272B'),
    teil('platine', 'circuit_board', 'Platine', 'Platine', 'box',
         x=125, y=30, w=85, d=2, z=10, h=95, r=0.3, mass=45,
         info='Senkrecht stehende Leiterplatte hinter der Senderskala. Mit Lautsprecher, Antennen und Batteriefach '
              'über Drähte verlötet.',
         color='#2E6B45'),
    *[teil(f'batterie{i}' if i else 'batterien', 'alkaline_cell', 'Vier Babyzellen (C)' if i == 0 else 'Babyzelle (C)',
           'Batterien C', 'box', x=10 + i * 50, y=3, w=37, d=26, z=4, h=26, r=8, explode=[0, -45, 0], mass=55,
           materials=C_ZELLE, label=i == 0, form='liegend_x', color='#2A2C2E',
           info='Vier 1,5-Volt-Zellen in Reihe ergeben 6 Volt. Sie sind der schwerste Teil des Radios: '
                'herausnehmen und in die Batteriesammlung geben.' if i == 0 else 'Eine der vier Zellen.')
      for i in range(4)],
    *[teil(f'batteriekappe{i}', 'alkaline_cell', 'Babyzelle (C), Pluspol-Ende', 'Batterien C', 'box',
           x=47 + i * 50, y=3, w=13, d=26, z=4, h=26, r=8, explode=[0, -45, 0], mass=11, materials=C_ZELLE,
           label=False, form='liegend_x', color='#B8862E',
           info='Kupferfarben bedrucktes Ende der Zelle mit dem Pluspol.') for i in range(4)],
    teil('rueckschale', 'plastic_housing', 'Rückschale mit Batteriefach', 'Rückschale', 'box',
         x=0, y=0, w=220, d=52, z=0, h=112, r=10, explode=[0, -110, 0], mass=140,
         info='Hinteres Gehäuseteil mit Batteriefach-Deckel und Typenschild. Nach Lösen der Schrauben nach '
              'hinten abziehen.',
         color=GEH, marks=[mark('box', 8, 4, 204, 44, 8, '#34383C')]),
]
for p in teile:
    if p['explode'] is None:
        p['explode'] = [0, 0, 0]
skaliere_masse(teile, oid='portable_radio')
for p in teile:  # gerundete Formen (form): marks nur in der Zeichnung, oben flach würden sie schweben
    if p.get('form'):
        p['marks'] = [dict(m, zeichnung=True) for m in p.get('marks') or []]
schreibe('portable_radio', teile)
