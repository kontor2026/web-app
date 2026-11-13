"""3D-Modell: computer_mouse. Erzeugt tools/kategorien/modelle/computer_mouse.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Typische kabelgebundene Büromaus, 63 × 115 × 38 mm, Kabel hinten (y = 0) herausgeführt.
teile = [
    teil('oberschale', 'plastic_housing', 'Oberschale mit Tasten', 'Oberschale', 'box',
         x=0, y=0, w=63, d=115, z=10, h=28, r=26, mass=24,
         info='Die beiden Maustasten sind federnde Zungen der Oberschale. Sie ist mit einer Schraube unter dem Gleitfuß und vorn mit Rastnasen befestigt.',
         marks=[mark('box', 4, 4, 26, 40, 10), mark('box', 33, 4, 26, 40, 10), mark('box', 27.5, 18, 8, 24, 4, '#2B2F33')]),
    teil('mausrad', 'rubber_scroll_wheel', 'Mausrad mit Gummiring', 'Mausrad', 'box',
         x=28, y=19, w=7, d=22, z=16, h=22, r=3.5, mass=3, materials=[['gummi', 45], ['pcabs', 40], ['stahl', 15]],
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
         x=0, y=0, w=63, d=115, z=0, h=10, r=26, mass=20,
         info='Bodenplatte mit Sensoröffnung. Unter den Gleitfüßen aus Teflon versteckt sich oft die Schraube.',
         marks=[mark('box', 10, 4, 43, 8, 4, '#E8E8E8'), mark('box', 10, 101, 43, 8, 4, '#E8E8E8'),
                mark('cyl', 28, 56, 8, fill='#1A1D20')]),
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

explodiere(teile, abstand=26)
skaliere_masse(teile, oid='computer_mouse')
schreibe('computer_mouse', teile)
