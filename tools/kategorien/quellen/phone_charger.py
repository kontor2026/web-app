"""3D-Modell: phone_charger. Erzeugt tools/kategorien/modelle/phone_charger.json.

Typisches 5-V-USB-A-Steckernetzteil (Euro-Stecker), auf die Seite gelegt: Stifte zeigen nach hinten (y = 0),
die Platine liegt waagerecht, darüber Trafo und Kondensatoren.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, schreibe  # noqa: E402

GEH = '#F1F2F0'
teile = [
    teil('oberschale', 'plastic_housing', 'Gehäuse-Oberschale', 'Oberschale', 'box',
         x=0, y=19, w=45, d=26, z=14, h=14, r=4, mass=12,
         info='Schwer entflammbares PC/ABS. Die beiden Schalen sind meist verschweißt, nicht verschraubt. '
              'Nur mit Werkzeug und Erwachsenen öffnen.',
         color=GEH, marks=[mark('box', 6, 5, 33, 16, 2), mark('box', 9, 8, 12, 4, 1, '#C9CCCA')]),
    teil('elko', 'circuit_board', 'Elektrolytkondensator (Eingang)', 'Elko', 'cyl',
         material_id='mixed_electronics', x=26, y=23, w=10, z=4.6, h=16, mass=3.2,
         materials=[['alu', 55], ['papier', 20], ['pcabs', 10], ['gummi', 5], ['kupfer', 10]],
         info='Glättet die gleichgerichtete Netzspannung. Kann auch ausgesteckt noch kurz geladen sein, '
              'darum die Beinchen nicht berühren.',
         color='#2F4F7A', marks=[mark('cyl', 2, 2, 6, fill='#B9C0C6')]),
    teil('trafo', 'circuit_board', 'Übertrager (Trafo)', 'Trafo', 'box',
         material_id='mixed_electronics', x=6, y=23.5, w=16, d=14.5, z=4.6, h=15, r=1, mass=15,
         materials=[['ferrit', 55], ['kupfer', 35], ['pcabs', 10]],
         info='Ferritkern mit Kupferwicklungen. Trennt die Netzspannung sicher vom USB-Ausgang und wandelt sie '
              'auf 5 Volt um.',
         color='#3A3F44', marks=[mark('box', 2, 2, 12, 11, 1, '#C5803D'), mark('box', 4, 4, 8, 7, 1),
                                 mark('box', 6, 6, 4, 3, 0.5)]),
    teil('elko_aus', 'circuit_board', 'Ausgangskondensator', 'Elko Ausgang', 'cyl',
         material_id='mixed_electronics', x=33, y=35, w=6, z=4.6, h=9, mass=0.8,
         materials=[['alu', 55], ['papier', 20], ['pcabs', 10], ['gummi', 5], ['kupfer', 10]],
         info='Glättet die 5-Volt-Ausgangsspannung für das Handy.', color='#3B3B3B'),
    teil('y_kondensator', 'circuit_board', 'Y-Kondensator', 'Y-Kondensator', 'box',
         material_id='mixed_electronics', x=23.5, y=35, w=7, d=3, z=4.6, h=8, r=1, mass=0.4,
         materials=[['keramik', 80], ['kupfer', 10], ['pcabs', 10]],
         info='Blaue Keramikscheibe zwischen Netz- und Ausgangsseite. Unterdrückt Funkstörungen.',
         color='#3D6FB6'),
    teil('regler', 'circuit_board', 'Regler-Chip', 'Chip', 'box',
         material_id='pcb', x=8, y=40, w=6, d=4, z=4.6, h=1.6, r=0.3, mass=0.3, materials=[['chip', 100]],
         info='Schaltet den Strom durch den Trafo viele tausend Mal pro Sekunde ein und aus.',
         color='#22272B', marks=[mark('cyl', 0.6, 0.6, 1)]),
    teil('usb_buchse', 'circuit_board', 'USB-A-Buchse', 'USB-Buchse', 'box',
         material_id='steel', x=16.5, y=38.5, w=13, d=6.5, z=4.6, h=6, r=0.5, mass=2,
         materials=[['stahl', 70], ['kontakte', 15], ['pcabs', 15]],
         info='Vernickeltes Stahlblech mit vergoldeten Kontakten. Hier steckt das Ladekabel.',
         color='#B7BCC0', marks=[mark('box', 1.5, 2, 10, 3, 0.3, '#2A2E31')]),
    teil('platine', 'circuit_board', 'Platine', 'Platine', 'box',
         x=1.5, y=20.5, w=42, d=23, z=3, h=1.6, r=1, mass=7,
         info='Leiterplatte aus Glasfaser-Epoxid mit Kupferbahnen. Ein Schlitz in der Mitte trennt '
              'Netz- und Niederspannungsseite.',
         color='#2E6B45', marks=[mark('box', 22.3, 2, 1.2, 12, 0.5, '#1E3F2A')]),
    teil('unterschale', 'plastic_housing', 'Gehäuse-Unterschale', 'Unterschale', 'box',
         x=0, y=19, w=45, d=26, z=0, h=14, r=4, mass=12,
         info='Hält Stifte und Platine. Auf dem Typenschild stehen Ausgangsspannung und Stromstärke.',
         color=GEH, marks=[mark('box', 16, 21, 13, 5, 0.5, '#2A2E31')]),
    teil('stift_l', 'plug_pins', 'Steckerstift links', 'Stift', 'box',
         x=10.5, y=0, w=4, d=19, z=12, h=4, r=2, explode=[0, -22, 0], mass=2.2,
         materials=[['messing', 100]],
         info='Vernickeltes Messing (Kupfer und Zink). In die Schale eingepresst, kommt nur beim Aufbrechen heraus.',
         color='#C9CDD0'),
    teil('stift_r', 'plug_pins', 'Steckerstift rechts', 'Stift', 'box',
         x=30.5, y=0, w=4, d=19, z=12, h=4, r=2, explode=[0, -22, 0], mass=2.2,
         materials=[['messing', 100]], info='Zweiter Stift des Euro-Steckers, 19 mm Abstand zum ersten.',
         color='#C9CDD0', label=False),
]
explodiere(teile, abstand=18)
schreibe('phone_charger', teile)
