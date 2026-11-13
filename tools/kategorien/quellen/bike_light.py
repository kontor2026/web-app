"""3D-Modell: bike_light. Erzeugt tools/kategorien/modelle/bike_light.json.

Typisches USB-aufladbares LED-Frontlicht (Lichtaustritt nach vorne, y groß), liegt auf der Gummihalterung.
Innen: Lithium-Polymer-Akku, Platine mit Ladebuchse hinten, senkrechte LED-Platine mit Reflektor und Streuscheibe vorne.
Explosion: Streuscheibe, Reflektor und LED nach vorne (dy > 0) herausgezogen, der Rest in Ebenen nach oben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

GEH = '#2B2E31'
teile = [
    teil('oberschale', 'plastic_housing', 'Gehäuse-Oberschale mit Taster', 'Oberschale', 'box',
         x=1, y=0, w=38, d=74, z=24, h=16, r=10, mass=12,
         info='Kunststoffschale aus PC/ABS, meist mit zwei kleinen Schrauben oder Clips am Unterteil befestigt. '
              'Durch die Gummikappe oben wird das Licht ein- und ausgeschaltet.',
         color=GEH, marks=[mark('cyl', 12, 26, 14, fill='#4A4F54'), mark('cyl', 16, 30, 6, fill='#7FD36B'),
                           mark('box', 6, 4, 26, 6, 3, '#3A3D40')]),
    teil('usb_buchse', 'circuit_board', 'USB-C-Ladebuchse', 'USB-Buchse', 'box',
         material_id='steel', x=15.5, y=3, w=9, d=7, z=23.2, h=3.2, r=1.5, mass=1,
         materials=[['stahl', 70], ['kontakte', 15], ['pcabs', 15]],
         info='Hinten unter einer Gummiklappe. Hier wird das Licht mit einem USB-Kabel aufgeladen.',
         color='#B7BCC0', marks=[mark('box', 1.5, 0.5, 6, 1.6, 0.8, '#2A2E31')]),
    teil('ladechip', 'circuit_board', 'Lade- und LED-Treiberchip', 'Chip', 'box',
         material_id='pcb', x=10, y=24, w=6, d=6, z=23.2, h=1, r=0.3, mass=0.3, materials=[['chip', 100]],
         info='Lädt den Akku sicher auf und regelt den Strom für die LED, auch im Blinkmodus.',
         color='#22272B', marks=[mark('cyl', 0.6, 0.6, 1)]),
    teil('platine', 'circuit_board', 'Platine', 'Platine', 'box',
         x=4, y=2, w=32, d=50, z=22, h=1.2, r=2, mass=4,
         info='Leiterplatte mit Taster, Ladechip und Anzeige-LED. Mit dem Akku über zwei Drähte verlötet.',
         color='#2E6B45', marks=[mark('cyl', 12, 26, 8, fill='#B7BCC0'), mark('box', 24, 40, 4, 6, 0.5, '#E8E8E2')]),
    teil('akku', 'li_ion_battery', 'Lithium-Polymer-Akku', 'Akku', 'box',
         x=5, y=6, w=30, d=48, z=12, h=9, r=2, mass=28,
         materials=[['lco', 40], ['graphit', 20], ['elektrolyt', 15], ['alu', 15], ['kupfer', 10]],
         info='Etwa 1.500 mAh in einer Folientasche. Nicht knicken oder durchstechen, Drähte abschneiden, '
              'Enden abkleben und zur Batteriesammlung bringen.',
         color='#9DA6AD', marks=[mark('box', 3, 4, 24, 38, 2), mark('box', 6, 8, 18, 10, 1, '#C8423A')]),
    teil('led_platine', 'led_module', 'LED-Platine (Aluminiumkern)', 'LED-Platine', 'box',
         material_id='mixed_electronics', x=10, y=56, w=20, d=1.6, z=14, h=20, r=0.3, explode=[0, 18, 0], mass=1.5,
         materials=[['alu', 75], ['kupfer', 10], ['fr4', 10], ['lot', 5]],
         info='Steht senkrecht hinter dem Reflektor. Das Aluminium leitet die Wärme der LED ab.',
         color='#ECECE6'),
    teil('led', 'led_module', 'Hochleistungs-LED', 'LED', 'box',
         material_id='mixed_electronics', x=16, y=57.6, w=8, d=3, z=20, h=8, r=0.5, explode=[0, 26, 0], mass=0.3,
         materials=[['led', 60], ['keramik', 25], ['kupfer', 10], ['lot', 5]],
         info='Eine einzige sehr helle Leuchtdiode auf Keramik, gelber Leuchtstoff macht das Licht weiß.',
         color='#F6D86B'),
    teil('reflektor', 'led_module', 'Reflektor', 'Reflektor', 'box',
         material_id='pc', x=6, y=60.6, w=28, d=10, z=13, h=22, r=4, explode=[0, 38, 0], mass=3,
         materials=[['pcabs', 95], ['alu', 5]],
         info='Kunststoff, innen hauchdünn mit Aluminium bedampft. Bündelt das Licht nach vorne auf die Straße.',
         color='#D6DADD', marks=[mark('box', 4, 1, 20, 8, 3, '#EEF0F1')]),
    teil('streuscheibe', 'plastic_housing', 'Streuscheibe', 'Streuscheibe', 'box',
         material_id='pc', x=2, y=72, w=36, d=6, z=12, h=26, r=3, explode=[0, 56, 0], mass=4,
         materials=[['pcabs', 100]],
         info='Klares Polycarbonat, schlagfest. Mit dem Gehäuse verklebt oder verrastet, lässt sich nach vorne abhebeln.',
         color='#DDEFF7', opacity=0.6, marks=[mark('box', 4, 1, 28, 4, 2)]),
    teil('unterschale', 'plastic_housing', 'Gehäuse-Unterschale', 'Unterschale', 'box',
         x=1, y=0, w=38, d=74, z=10, h=14, r=10, mass=12,
         info='Wanne für Akku und Platine, unten mit Schiene für die Halterung.', color=GEH,
         marks=[mark('box', 3, 4, 32, 52, 6, '#34383C')]),
    teil('schiene', 'rubber_mount', 'Halteschiene', 'Halteschiene', 'box',
         material_id='nylon', x=8, y=18, w=24, d=34, z=6, h=4, r=3, mass=4, materials=[['nylon', 100]],
         info='Harter Kunststoff-Schlitten, in den das Licht einrastet. Zum Abnehmen den Riegel drücken.',
         color='#3A3D40', marks=[mark('box', 4, 2, 16, 30, 2, '#2B2E31')]),
    teil('gummihalter', 'rubber_mount', 'Gummi-Halteband', 'Gummiband', 'box',
         x=6, y=16, w=28, d=38, z=0, h=6, r=6, mass=9,
         info='Dehnbares Silikon- oder Gummiband, das um den Lenker gespannt und in einen Haken gehängt wird. '
              'Einfach abziehen, es gehört in den Restmüll.',
         color='#1F2224', marks=raster(4, 6, 1, 4, 20, 3, 8, 8, r=1, fill='#34383C')),
]
explodiere(teile, abstand=26, abstaende={'ladechip': 10, 'usb_buchse': 10})
skaliere_masse(teile, oid='bike_light')
schreibe('bike_light', teile)
