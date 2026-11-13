"""3D-Modell: usb_stick. Erzeugt tools/kategorien/modelle/usb_stick.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Typischer USB-A-Stick mit Schutzkappe, 20 × 55 × 8 mm. Stecker hinten (y = 0), von der Kappe bedeckt.
# Explosion: Kappe und Steckerblech nach hinten abgezogen, Gehäusehälften und Platine nach oben.
GEH = '#2F3438'
CHIP = '#3F4547'
teile = [
    teil('kappe', 'plastic_housing', 'Schutzkappe', 'Kappe', 'box',
         x=1, y=0, w=18, d=17, z=0.5, h=7, r=2, mass=1.5, explode=[0, -40, 0], color=GEH,
         info='Schützt den Stecker vor Staub. Geht leicht verloren, ist aber reiner Kunststoff.'),
    teil('oberschale', 'plastic_housing', 'Gehäuse-Oberteil', 'Oberteil', 'box',
         x=0, y=15, w=20, d=40, z=4, h=4, r=3, mass=2.2, color=GEH,
         info='Zwei Kunststoffhälften, verklipst oder verschweißt. Mit einem Messer an der Naht vorsichtig aufhebeln.',
         marks=[mark('cyl', 7, 33, 6, fill='#1E2226')]),
    teil('led', 'circuit_board', 'Status-LED', 'LED', 'box', material_id='mixed_electronics',
         x=8.5, y=45, w=3, d=2, z=3.5, h=0.8, r=0.2, mass=0.02, materials=[['led', 60], ['kupfer', 40]],
         color='#7FC8F0', info='Blinkt, während Daten geschrieben oder gelesen werden. Leuchtet durch das Gehäuse.'),
    teil('controller', 'circuit_board', 'Controller-Chip', 'Controller', 'box',
         x=6.5, y=17, w=7, d=7, z=3.5, h=0.9, r=0.2, mass=0.15, materials=[['chip', 100]], color=CHIP,
         info='Übersetzt zwischen USB und Speicher und verteilt die Daten gleichmäßig auf die Speicherzellen.'),
    teil('quarz', 'circuit_board', 'Quarz', 'Quarz', 'box', material_id='mixed_electronics',
         x=14.5, y=18, w=2.5, d=5, z=3.5, h=1, r=0.5, mass=0.05, materials=[['stahl', 50], ['keramik', 50]],
         color='#B7BCC0', info='Gibt den genauen Takt für die USB-Übertragung vor.'),
    teil('flash', 'circuit_board', 'Flash-Speicherchip', 'Speicher', 'box',
         x=4, y=26, w=12, d=17, z=3.5, h=1.2, r=0.3, mass=0.4, materials=[['chip', 100]], color=CHIP,
         info='Hier liegen die Daten, auch ohne Strom. Vor dem Wegwerfen löschen oder den Chip zerstören.',
         marks=[mark('cyl', 1, 1, 1.2, fill='#5E656A')]),
    teil('platine', 'circuit_board', 'Platine mit Steckerkontakten', 'Platine', 'box',
         x=4, y=4, w=12, d=46, z=2.5, h=1, r=1, mass=0.8, color='#2E6B45',
         info='Der vordere Teil der Platine steckt im Stecker, vier vergoldete Kontaktflächen berühren die Buchse.',
         marks=raster(1.5, 1, 4, 1, 1.5, 7, 2.6, r=0.2, fill='#D4AF37')),
    teil('stecker', 'circuit_board', 'USB-A-Steckerblech', 'Stecker', 'box', material_id='steel',
         x=4, y=2, w=12, d=13, z=1.75, h=4.5, r=0.5, mass=1.8, explode=[0, -22, 0],
         materials=[['stahl', 95], ['nickel', 5]], color='#C9CED2',
         info='Vernickeltes Stahlblech um die Platine. Ist an der Platine angelötet.',
         marks=[mark('box', 2.5, 3, 2, 2, 0.2, '#2A2E31'), mark('box', 7.5, 3, 2, 2, 0.2, '#2A2E31')]),
    teil('unterschale', 'plastic_housing', 'Gehäuse-Unterteil', 'Unterteil', 'box',
         x=0, y=15, w=20, d=40, z=0, h=4, r=3, mass=2.2, color=GEH,
         info='Trägt die Platine und hat oft eine Öse für den Schlüsselring.',
         marks=[mark('box', 4, 0, 12, 35, 1, '#1E2226'), mark('cyl', 7, 33, 6, fill='#1E2226')]),
]

explodiere(teile, abstand=14, abstaende={'led': 6, 'controller': 6, 'quarz': 6, 'flash': 6}, nach_liste=True)
skaliere_masse(teile, oid='usb_stick', stellen=2)
schreibe('usb_stick', teile)
