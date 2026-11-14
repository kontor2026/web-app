"""3D-Modell: keyboard. Erzeugt tools/kategorien/modelle/keyboard.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Typische Folientastatur (Rubber Dome) mit Ziffernblock, 440 × 135 × 25 mm, Stahlplatte als Versteifung.
# Tastenfeld relativ zum Kappen-Teil (x = 10, y = 10, 420 × 115 mm), Rastermaß 19 mm.
U = 19
kappen = (
    raster(0, 0, 1, 1, 17, 17, U)                                    # Esc
    + raster(38, 0, 4, 1, 17, 17, U) + raster(123.5, 0, 4, 1, 17, 17, U) + raster(209, 0, 4, 1, 17, 17, U)  # F1–F12
    + raster(0, 22, 13, 1, 17, 17, U) + [mark('box', 247, 22, 36, 17, 2)]                                 # Zahlenreihe, Rück
    + [mark('box', 0, 41, 26, 17, 2)] + raster(28.5, 41, 12, 1, 17, 17, U) + [mark('box', 257, 41, 26, 17, 2)]
    + [mark('box', 0, 60, 31, 17, 2)] + raster(33, 60, 12, 1, 17, 17, U) + [mark('box', 262, 60, 21, 17, 2)]
    + [mark('box', 0, 79, 41, 17, 2)] + raster(43, 79, 10, 1, 17, 17, U) + [mark('box', 233, 79, 50, 17, 2)]
    + raster(0, 98, 3, 1, 21, 17, 24) + [mark('box', 72, 98, 115, 17, 2)] + raster(190, 98, 4, 1, 21, 17, 23.5)
    + raster(290, 0, 3, 1, 17, 17, U) + raster(290, 22, 3, 2, 17, 17, U) + raster(309, 79, 1, 1, 17, 17, U)
    + raster(290, 98, 3, 1, 17, 17, U)                               # Navigationsblock und Pfeiltasten
    + raster(345, 22, 4, 1, 17, 17, U) + raster(345, 41, 3, 3, 17, 17, U)
    + [mark('box', 402, 41, 17, 36, 2), mark('box', 402, 79, 17, 36, 2), mark('box', 345, 98, 36, 17, 2),
       mark('box', 383, 98, 17, 17, 2)]                              # Ziffernblock
)

TASTE = '#454A4F'
for m in kappen:
    m['fill'] = TASTE
SCHWARZ = '#2B2F33'

teile = [
    teil('tastenkappen', 'keycaps', 'Tastenkappen (105 Stück)', 'Tastenkappen', 'box',
         x=10, y=10, w=420, d=115, z=14, h=10.5, r=3, mass=110, color='#30343A',
         info='Die Kappen sind nur aufgesteckt und lassen sich mit einem Tastenzieher oder einer gebogenen Büroklammer senkrecht abziehen.',
         marks=kappen),
    teil('stabilisator', 'keycaps', 'Stabilisatoren aus Stahldraht', 'Stabilisatoren', 'box',
         material_id='steel', x=82, y=111, w=115, d=4, z=12.5, h=1.5, r=0.75, mass=6, color='#B9BEC2',
         info='Gebogene Stahldrähte unter Leertaste, Shift und Enter. Sie sorgen dafür, dass lange Tasten nicht kippen.'),
    teil('oberschale', 'plastic_housing', 'Oberschale (Tastenrahmen)', 'Oberschale', 'box',
         x=0, y=0, w=440, d=135, z=10, h=6, r=8, mass=130, color=SCHWARZ,
         info='Rahmen mit den Führungen der Tasten. Mit vielen kleinen Schrauben von unten befestigt, manche stecken unter Aufklebern.',
         marks=[mark('box', 9, 9, 290, 117, 3, '#1F2225'), mark('box', 353, 9, 78, 117, 3, '#1F2225'),
                mark('box', 302, 30, 48, 96, 3, '#1F2225')]
               + [mark('box', 376, 0.8, 50, 7, 2, '#24272A')] + raster(380, 2.5, 3, 1, 4, 4, 15, shape='cyl', fill='#7FD36B')),
    teil('gummimatte', 'circuit_board', 'Gummimatte mit Tastenkuppeln', 'Gummimatte', 'box',
         material_id='silicone', x=10, y=10, w=420, d=115, z=7, h=4, r=3, mass=28, color='#4A5258', opacity=0.85,
         info='Unter jeder Taste sitzt eine kleine Gummikuppel. Sie federt die Taste zurück und drückt beim Tippen auf die Folie.',
         marks=raster(4, 4, 15, 6, 10, 10, U, shape='cyl') + raster(298, 23, 3, 5, 10, 10, U, shape='cyl')
         + raster(353, 23, 4, 5, 10, 10, U, shape='cyl')),
    teil('chip', 'circuit_board', 'Tastatur-Controller (Chip)', 'Controller', 'box',
         material_id='pcb', x=394, y=3, w=10, d=5, z=8.2, h=1.2, r=0.5, mass=0.5, materials=[['chip', 100]],
         color='#2B2F33', info='Fragt die Tasten-Matrix tausendmal pro Sekunde ab und schickt die gedrückten Tasten per USB zum Computer.'),
    teil('platine', 'circuit_board', 'Controller-Platine mit LEDs', 'Platine', 'box',
         x=370, y=1, w=60, d=9, z=6.6, h=1.6, r=1, mass=7, color='#2E6B45',
         info='Kleine Leiterplatte mit Chip, Status-LEDs und Kabelanschluss. Die Tastenfolie steckt in einem Klemmstecker.',
         marks=raster(11, 2, 3, 1, 4, 4, 15, shape='cyl', fill='#7FD36B')),
    teil('folie_oben', 'circuit_board', 'Obere Kontaktfolie', 'Folie oben', 'box',
         material_id='multilayer_plastic', x=10, y=10, w=420, d=115, z=6.2, h=0.3, r=2, mass=8,
         materials=[['folien', 90], ['kontakte', 10]], color='#D9DEE2', opacity=0.85,
         info='PET-Folie mit aufgedruckten Silberbahnen. Drückt eine Gummikuppel darauf, berührt sie die untere Folie.',
         marks=raster(9, 9, 15, 6, 3, 3, U, shape='cyl', fill='#A8AEB3')),
    teil('folie_mitte', 'circuit_board', 'Abstandsfolie mit Löchern', 'Abstandsfolie', 'box',
         material_id='multilayer_plastic', x=10, y=10, w=420, d=115, z=5.9, h=0.3, r=2, mass=6,
         materials=[['folien', 100]], color='#EEF0F1', opacity=0.8,
         info='Mittlere Folie mit einem Loch unter jeder Taste. Sie hält die beiden Kontaktfolien auf Abstand.',
         marks=raster(8.5, 8.5, 15, 6, 4, 4, U, shape='cyl', fill='#C9CED2')),
    teil('folie_unten', 'circuit_board', 'Untere Kontaktfolie', 'Folie unten', 'box',
         material_id='multilayer_plastic', x=10, y=10, w=420, d=115, z=5.6, h=0.3, r=2, mass=8,
         materials=[['folien', 90], ['kontakte', 10]], color='#D9DEE2', opacity=0.85,
         info='Zweite Folie mit Silberbahnen. Die Leiterbahnen beider Folien bilden zusammen ein Gitter (Matrix) '
              'und enden an der Controller-Platine.',
         marks=raster(9, 9, 15, 6, 3, 3, U, shape='cyl', fill='#A8AEB3') + [mark('box', 365, 0, 40, 6, 1, '#A8AEB3')]),
    teil('stahlplatte', 'steel_backplate', 'Stahlplatte', 'Stahlplatte', 'box',
         x=8, y=8, w=424, d=119, z=4.5, h=0.8, r=3, mass=190, color='#9BA3A8',
         info='Dünnes verzinktes Stahlblech, macht die Tastatur steif und schwer. Mit einem Magneten erkennt man es leicht.',
         marks=raster(20, 15, 8, 3, 30, 6, 50, 40, r=3)),
    teil('unterschale', 'plastic_housing', 'Unterschale mit Klappfüßen', 'Unterschale', 'box',
         x=0, y=0, w=440, d=135, z=0, h=10, r=8, mass=150, color='#24272A', wand=2.5,
         info='Bodenwanne aus ABS mit Schraubdomen. Nach dem Ausbau von Stahlplatte und Elektronik ist sie '
              'sortenreiner Kunststoff.',
         marks=[dict(m, zeichnung=True) for m in [mark('box', 4, 4, 432, 127, 6, '#2B2F33'),
                mark('box', 25, 5, 50, 12, 3, '#1F2225'), mark('box', 365, 5, 50, 12, 3, '#1F2225')]
               + raster(60, 60, 6, 1, 6, 6, 64, shape='cyl', fill='#3A3F44')]),
    teil('schrauben', 'plastic_housing', 'Gehäuseschrauben (12 Stück)', 'Schrauben', 'cyl', material_id='steel',
         x=124, y=60, w=4, z=1, h=8, mass=6, explode=[0, 100, 0], materials=[['stahl', 100]], color='#9BA3A8',
         info='Kleine Kreuzschlitzschrauben von unten. Manche verstecken sich unter Aufklebern oder Gummifüßen.',
         marks=[mark('box', 1.6, 0.6, 0.8, 2.8, fill='#3A3F44'), mark('box', 0.6, 1.6, 2.8, 0.8, fill='#3A3F44')]),
    teil('klappfuss_l', 'plastic_housing', 'Klappfuß', 'Klappfüße', 'box',
         x=27, y=6, w=46, d=10, z=1, h=3, r=2, mass=4, color='#1F2225', explode=[0, 150, 0],
         info='Ausklappbare Füße hinten, stellen die Tastatur schräg. Sie rasten nur ein und brechen leicht ab.'),
    teil('klappfuss_r', 'plastic_housing', 'Klappfuß rechts', 'Klappfuß', 'box',
         x=367, y=6, w=46, d=10, z=1, h=3, r=2, mass=4, color='#1F2225', explode=[0, 150, 0], label=False,
         info='Zweiter Klappfuß. Gleich gebaut wie der linke.'),
    teil('kabel', 'cable_insulation', 'Kabelmantel mit Knickschutz', 'Kabel', 'box', form='liegend_y',
         x=216, y=-14, w=8, d=14, z=3, h=6, r=3, mass=26, explode=[260, -30, 0], color='#2B2F33',
         info='Etwa 1,5 m PVC-Kabel. Mantel und Kupferadern lassen sich mit einer Abisolierzange trennen.'),
    teil('litzen', 'cable_copper_core', 'Kupferlitzen', 'Kupferlitzen', 'box', form='liegend_y',
         x=218, y=-14, w=4, d=14, z=4, h=4, r=2, mass=8, explode=[280, -30, 0], color='#C98F62',
         info='Vier Kupferadern für Strom und Daten. Kupfer lässt sich ohne Qualitätsverlust immer wieder einschmelzen.'),
    teil('usb', 'cable_copper_core', 'USB-Stecker', 'USB-Stecker', 'box',
         material_id='mixed_electronics', x=216, y=-14, w=8, d=14, z=1, h=9, r=1, mass=5,
         materials=[['stahl', 40], ['pcabs', 35], ['kupfer', 20], ['kontakte', 5]], explode=[300, -30, 0],
         info='Am anderen Kabelende. Blechhülle aus Stahl, darin vergoldete Kontakte im Kunststoffträger.',
         marks=[mark('box', 2, 1, 4, 12, 0.5, '#B9BEC2')]),
]

explodiere(teile, abstand=50, abstaende={'folie_mitte': 30, 'folie_oben': 30, 'chip': 12})
skaliere_masse(teile, oid='keyboard')
for p in teile:   # Foto-Ansicht: echte Formen (form) tragen keine aufgemalten Details
    if p.get('form') and p.get('marks'):
        p['marks'] = [dict(k, zeichnung=True) for k in p['marks']]
schreibe('keyboard', teile)
