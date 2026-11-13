"""3D-Modell: computer_mouse. Erzeugt tools/kategorien/modelle/computer_mouse.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Typische kabelgebundene Büromaus, 63 × 115 × 38 mm, Kabel hinten (y = 0) herausgeführt.
SCHALE = '#34383C'
NAHT = '#1C1F22'
# Oberschale als gestapelte Scheiben (gewölbter Rücken), höchster Punkt hinten über dem Handballen
SCHEIBEN = [  # x, y, w, d, z, h, r  (unten nach oben)
    (0, 0, 63, 115, 10, 10, 26), (1.5, 2, 60, 110, 20, 6, 25), (4, 6, 55, 100, 26, 4, 23),
    (7, 11, 49, 88, 30, 3, 20), (11, 20, 41, 72, 33, 3, 17), (17, 44, 29, 42, 36, 2, 13)]
TASTE_Y = 45          # Trennfuge Tasten / Rücken
RAD = (28, 19, 7, 22)  # x, y, w, d des Mausrads


def fugen(x, y, w, d, oben):
    """Mittelfuge zwischen den Tasten und Querfuge, relativ zur Scheibe; auf der obersten Scheibe am Rad den Schlitz."""
    m = []
    lang = TASTE_Y - y
    if lang > 0:
        m.append(mark('box', 31 - x, 0, 1, lang, 0.4, NAHT))
        m.append(mark('box', 0, lang, w, 0.8, 0.4, NAHT))
    if oben:
        ry = max(RAD[1] - 1.5 - y, 0)
        m.append(mark('box', RAD[0] - 1 - x, ry, RAD[2] + 2, RAD[1] + RAD[3] + 1.5 - y - ry, 3, NAHT))
    return m


teile = []
for i, (x, y, w, d, z, h, r) in reversed(list(enumerate(SCHEIBEN))):
    teile.append(teil('oberschale' if i == 0 else f'oberschale_{i + 1}', 'plastic_housing',
                      'Oberschale mit Tasten', 'Oberschale', 'box', x=x, y=y, w=w, d=d, z=z, h=h, r=r, mass=5,
                      color=SCHALE, label=None if i == 0 else False,
                      info=('Die beiden Maustasten sind federnde Zungen der Oberschale. Sie ist mit einer Schraube '
                            'unter dem Gleitfuß und vorn mit Rastnasen befestigt.'),
                      marks=fugen(x, y, w, d, i == 4) + ([mark('box', 9, 22, 11, 6, 3, '#3C4146')] if i == 5 else [])))
teile += [
    teil('mausrad', 'rubber_scroll_wheel', 'Mausrad mit Gummiring', 'Mausrad', 'box',
         x=28, y=19, w=7, d=22, z=14, h=23.5, r=3.5, mass=3, sortBias=-1.6, materials=[['gummi', 45], ['pcabs', 40], ['stahl', 15]],
         color='#3A3F44', info='Kunststoffrad mit aufgezogenem Gummiring und Stahlachse. Lässt sich nach dem Öffnen einfach aus der Halterung heben.',
         marks=[mark('box', 1, 2, 5, 18, 2, '#2B2F33')]),
    teil('taster_l', 'circuit_board', 'Mikroschalter links', 'Mikroschalter', 'box',
         material_id='mixed_electronics', x=12, y=24, w=6, d=13, z=5.6, h=6, r=1, mass=1,
         materials=[['pcabs', 55], ['kupfer', 25], ['stahl', 15], ['kontakte', 5]], color='#2F3236',
         info='Kleiner Schalter unter der Taste, der hörbar klickt. Innen schnappt eine Kupferfeder mit silbernem Kontakt um.',
         marks=[mark('box', 2, 2, 2, 3, 0.5, '#C9302C')]),
    teil('taster_r', 'circuit_board', 'Mikroschalter rechts', 'Mikroschalter', 'box',
         material_id='mixed_electronics', x=45, y=24, w=6, d=13, z=5.6, h=6, r=1, mass=1,
         materials=[['pcabs', 55], ['kupfer', 25], ['stahl', 15], ['kontakte', 5]], color='#2F3236', label=False,
         info='Gleicher Mikroschalter für die rechte Taste. Geht er kaputt, lässt er sich mit dem Lötkolben tauschen.',
         marks=[mark('box', 2, 2, 2, 3, 0.5, '#C9302C')]),
    teil('encoder', 'circuit_board', 'Drehgeber für das Mausrad', 'Drehgeber', 'box',
         material_id='mixed_electronics', x=37, y=22, w=6, d=14, z=5.6, h=8, r=1, mass=1,
         materials=[['pcabs', 50], ['kupfer', 25], ['stahl', 25]], color='#5A6066',
         info='Zählt die Rastungen des Mausrads mit kleinen Schleifkontakten und meldet sie dem Sensor-Chip.'),
    teil('sensor', 'circuit_board', 'Optischer Sensor-Chip', 'Sensor', 'box',
         material_id='pcb', x=25, y=52, w=13, d=16, z=5.6, h=3, r=1, mass=1, materials=[['chip', 80], ['kupfer', 20]],
         color='#2B2F33',
         info='Eine winzige Kamera, die tausende Bilder pro Sekunde vom Tisch macht und daraus die Bewegung berechnet.',
         marks=[mark('cyl', 4.5, 6, 4, fill='#1A1D20')]),
    teil('led', 'circuit_board', 'Leuchtdiode (LED)', 'LED', 'box',
         material_id='mixed_electronics', x=40, y=56, w=4, d=6, z=5.6, h=5, r=1, mass=0.2,
         materials=[['led', 60], ['kupfer', 40]], color='#D63C3C',
         info='Beleuchtet die Tischfläche schräg von der Seite, damit der Sensor die feine Struktur erkennt.'),
    teil('platine', 'circuit_board', 'Leiterplatte', 'Platine', 'box',
         x=8, y=16, w=47, d=78, z=4, h=1.6, r=4, mass=6, color='#2E6B45',
         info='Trägt Schalter, Sensor und den Kabelanschluss. Mit einer Schraube befestigt, gehört in die Elektro-Sammlung.',
         marks=[mark('box', 18, 70, 11, 5, 1, '#D9D2B8')]),
    teil('linse', 'plastic_housing', 'Linse und Lichtleiter', 'Linse', 'box',
         material_id='pc', x=22, y=48, w=24, d=24, z=1.5, h=2.5, r=3, mass=1, color='#C9DEDF', opacity=0.7,
         info='Klares Polycarbonat. Bündelt das LED-Licht auf den Tisch und das Bild zurück auf den Sensor.',
         marks=[mark('cyl', 6, 7, 7), mark('cyl', 15, 8, 6)]),
    teil('unterschale', 'plastic_housing', 'Unterschale mit Gleitfüßen', 'Unterschale', 'box',
         x=0, y=0, w=63, d=115, z=0, h=10, r=26, mass=20, color='#26292C',
         info='Bodenplatte mit Sensoröffnung und Schraubendom. Nach dem Ausbau der Elektronik ist sie reiner Kunststoff.',
         marks=[mark('box', 4, 4, 55, 107, 22, '#2F3336'), mark('cyl', 28, 56, 8, fill='#1A1D20'),
                mark('cyl', 28.5, 94.5, 6, fill='#3A3F44')]),
    teil('schraube', 'plastic_housing', 'Gehäuseschraube', 'Schraube', 'cyl', material_id='steel',
         x=29.5, y=95.5, w=4, z=1, h=12, mass=0.5, materials=[['stahl', 100]], color='#9BA3A8',
         info='Kreuzschlitzschraube, die Ober- und Unterschale zusammenhält. Sie steckt unter dem hinteren Gleitfuß.',
         marks=[mark('cyl', 0.5, 0.5, 3, fill='#7A8288'), mark('box', 1.6, 0.8, 0.8, 2.4, fill='#3A3F44'),
                mark('box', 0.8, 1.6, 2.4, 0.8, fill='#3A3F44')]),
    teil('gleitfuss_v', 'plastic_housing', 'Gleitfüße (PTFE)', 'Gleitfüße', 'box', material_id='pp',
         x=10, y=4, w=43, d=8, z=0, h=0.6, r=4, mass=0.3, materials=[['ptfe', 85], ['klebstoff', 15]], color='#ECECE8',
         info='Glatte Teflon-Aufkleber, damit die Maus leicht gleitet. Mit dem Fingernagel abziehen, darunter sitzt die Schraube.'),
    teil('gleitfuss_h', 'plastic_housing', 'Gleitfuß hinten', 'Gleitfuß', 'box', material_id='pp',
         x=10, y=92, w=43, d=12, z=0, h=0.6, r=5, mass=0.4, materials=[['ptfe', 85], ['klebstoff', 15]], color='#ECECE8',
         label=False, info='Hinterer Gleitfuß, verdeckt die Gehäuseschraube.'),
    teil('kabel', 'cable_insulation', 'Kabelmantel mit Knickschutz', 'Kabel', 'box',
         x=29, y=-13, w=5, d=13, z=3, h=5, r=2.5, mass=22, explode=[60, -20, 0], color='#2B2F33',
         info='Etwa 1,8 m PVC-Kabel. Zum Recycling lassen sich Mantel und Kupfer mit einer Abisolierzange trennen.'),
    teil('litzen', 'cable_copper_core', 'Kupferlitzen', 'Kupferlitzen', 'box',
         x=30, y=-13, w=3, d=13, z=4, h=3, r=1.5, mass=6, explode=[75, -20, 0], color='#C98F62',
         info='Vier dünne Kupferadern für Strom und Daten. Kupfer ist wertvoll und fast beliebig oft recycelbar.'),
    teil('usb', 'cable_copper_core', 'USB-Stecker', 'USB-Stecker', 'box',
         material_id='mixed_electronics', x=28, y=-13, w=7, d=13, z=1, h=9, r=1, mass=5,
         materials=[['stahl', 40], ['pcabs', 35], ['kupfer', 20], ['kontakte', 5]], explode=[90, -20, 0],
         info='Am anderen Kabelende. Blechhülle aus Stahl, darin vergoldete Kontakte im Kunststoffträger.',
         marks=[mark('box', 1.5, 1, 4, 11, 0.5, '#B9BEC2')]),
]

explodiere(teile, abstand=26, gruppen=[['oberschale'] + [f'oberschale_{i}' for i in range(2, 7)]],
           abstaende={'schraube': 14, **{p['id']: 65 for p in teile if p['id'].startswith('oberschale')}})
skaliere_masse(teile, oid='computer_mouse')
schreibe('computer_mouse', teile)
