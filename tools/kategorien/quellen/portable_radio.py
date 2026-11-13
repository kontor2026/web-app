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
OBEN = 50  # Griff, Knöpfe und Antenne heben so weit ab
C_ZELLE = [['zinkmangan', 80], ['stahl', 20]]

teile = [
    teil('griff', 'plastic_housing', 'Tragegriff', 'Griff', 'box',
         x=40, y=30, w=140, d=20, z=112, h=18, r=8, explode=[0, 0, OBEN], mass=30,
         info='Kunststoffbügel, innen mit zwei Schrauben am Gehäuse befestigt. Zuerst abschrauben.',
         color='#2B2E31', marks=[mark('box', 10, 6, 120, 8, 4, '#3A3D40')]),
    teil('antenne', 'telescopic_antenna', 'Teleskopantenne', 'Antenne', 'box',
         x=30, y=4, w=170, d=8, z=112, h=8, r=4, explode=[40, 0, OBEN], mass=25,
         materials=[['stahl', 85], ['messing', 10], ['pcabs', 5]],
         info='Ineinandergeschobene Röhrchen aus verchromtem Stahl für den UKW-Empfang. Innen im Gehäuse mit '
              'einer Mutter festgeschraubt.',
         color='#C9CDD0', marks=raster(30, 1.5, 4, 1, 1.5, 5, 35, r=0.5, fill='#8A939A')),
    teil('knoepfe', 'plastic_housing', 'Drehknöpfe (Sender und Lautstärke)', 'Drehknöpfe', 'box',
         x=150, y=52, w=56, d=22, z=112, h=8, r=3, explode=[0, 30, OBEN], mass=8,
         info='Gerändelte Kunststoffknöpfe, nur auf die Achsen gesteckt. Lassen sich mit den Fingern abziehen.',
         color='#2B2E31', marks=[mark('cyl', 2, 2, 18, fill='#4A4F54'), mark('cyl', 34, 2, 18, fill='#4A4F54'),
                                 mark('box', 10, 3, 2, 6, 1, '#E35A4E')]),
    teil('frontschale', 'plastic_housing', 'Frontschale mit Lautsprechergitter', 'Frontschale', 'box',
         x=0, y=52, w=220, d=28, z=0, h=112, r=10, explode=[0, 70, 0], mass=125,
         info='Vorderes Gehäuseteil aus ABS mit Lochgitter vor dem Lautsprecher und Senderskala. '
              'Hinten sitzen 4 bis 6 Schrauben, oft im Batteriefach versteckt.',
         color=GEH, marks=[mark('box', 6, 6, 208, 16, 6, '#34383C'), mark('box', 130, 8, 80, 10, 2, '#E8E2C8')]),
    teil('lautsprecher', 'speaker_driver', 'Lautsprecher (100 mm)', 'Lautsprecher', 'box',
         x=15, y=40, w=100, d=12, z=6, h=100, r=6, mass=55,
         materials=[['stahl', 50], ['papier', 25], ['kupfer', 10], ['gummi', 10], ['pcabs', 5]],
         info='Membran aus Pappe in einem Stahlkorb. Sie schwingt und erzeugt den Ton, angetrieben von der '
              'Schwingspule. Mit vier Schrauben an der Frontschale.',
         color='#3B3B3B', marks=[mark('box', 6, 2, 88, 8, 4, '#55493C')]),
    teil('magnet', 'speaker_driver', 'Ferritmagnet des Lautsprechers', 'Magnet', 'cyl',
         material_id='mixed_electronics', x=45, y=26, w=40, d=14, z=36, h=40, mass=95,
         materials=[['ferrit', 80], ['stahl', 15], ['kupfer', 5]],
         info='Schwerer Ringmagnet aus Ferrit hinter der Membran. Zieht Schrauben und Büroklammern an.',
         color='#4A4F54', marks=[mark('cyl', 8, 3, 24, 8, fill='#8A939A')]),
    teil('ferritstab', 'circuit_board', 'Ferritstab-Antenne (Mittelwelle)', 'Ferritantenne', 'box',
         material_id='mixed_electronics', x=20, y=14, w=110, d=10, z=92, h=10, r=4, mass=18,
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
    teil('batterien', 'alkaline_cell', 'Vier Babyzellen (C)', 'Batterien C', 'box',
         x=10, y=3, w=200, d=26, z=4, h=26, r=8, mass=264, materials=C_ZELLE,
         info='Vier 1,5-Volt-Zellen in Reihe ergeben 6 Volt. Sie sind der schwerste Teil des Radios: '
              'herausnehmen und in die Batteriesammlung geben.',
         color='#C8423A', marks=raster(0, 0, 4, 1, 50, 26, 50, r=8, fill='#C8423A')
                              + raster(44, 6, 4, 1, 6, 14, 50, r=2, fill='#B7BCC0')),
    teil('rueckschale', 'plastic_housing', 'Rückschale mit Batteriefach', 'Rückschale', 'box',
         x=0, y=0, w=220, d=52, z=0, h=112, r=10, explode=[0, -75, 0], mass=140,
         info='Hinteres Gehäuseteil mit Batteriefach-Deckel und Typenschild. Nach Lösen der Schrauben nach '
              'hinten abziehen.',
         color=GEH, marks=[mark('box', 8, 4, 204, 44, 8, '#34383C')]),
]
for p in teile:
    if p['explode'] is None:
        p['explode'] = [0, 0, 0]
skaliere_masse(teile, oid='portable_radio')
schreibe('portable_radio', teile)
