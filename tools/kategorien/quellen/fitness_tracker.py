"""3D-Modell: fitness_tracker. Erzeugt tools/kategorien/modelle/fitness_tracker.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Typisches Fitnessarmband: Kapsel 19 × 38 × 11 mm mit OLED-Display oben und Pulssensor unten.
# Das Armband ist nur als kurze Ansätze an beiden Enden dargestellt (gekürzt, damit das Modell den Maßen
# der Kapsel entspricht); die Masse ist die des ganzen Bandes. Ansätze werden nach hinten und vorne abgezogen.
GEH = '#25292D'
CHIP = '#3F4547'
teile = [
    teil('deckglas', 'plastic_housing', 'Deckglas', 'Deckglas', 'box', material_id='special_glass',
         x=0.5, y=4, w=19, d=38, z=10, h=1, r=9, mass=1.2, materials=[['glas', 100]], color='#C9DEDF', opacity=0.6,
         info='Gehärtetes, gewölbtes Glas über dem Display. Mit dem Rahmen verklebt.'),
    teil('display', 'circuit_board', 'OLED-Display', 'Display', 'box', material_id='special_glass',
         x=3, y=8, w=14, d=30, z=9.2, h=0.8, r=2, mass=1, materials=[['displayglas', 60], ['folien', 25], ['kupfer', 15]],
         color='#1F2326',
         info='Leuchtende Pixel ohne Hintergrundlicht. Mit einem winzigen Flachbandkabel an der Platine angesteckt.',
         marks=[mark('box', 2, 6, 10, 6, 1, '#7FC8F0'), mark('box', 3, 14, 8, 2, 0.5, '#5F8F4E'),
                mark('box', 3, 18, 6, 2, 0.5, '#C9A227')]),
    teil('oberschale', 'plastic_housing', 'Gehäuse-Oberteil', 'Oberteil', 'box',
         x=0.5, y=4, w=19, d=38, z=5, h=5, r=9, mass=2.5, color=GEH,
         info='Rahmen aus Kunststoff, oft mit dem Glas und dem Unterteil verklebt. Nur mit Wärme zu öffnen.',
         marks=[mark('box', 2.5, 4, 14, 30, 2, '#1E2226')]),
    teil('motor', 'circuit_board', 'Vibrationsmotor', 'Vibration', 'cyl', material_id='mixed_electronics',
         x=13.5, y=12, w=4.5, z=4.8, h=2.7, mass=0.4, materials=[['stahl', 40], ['kupfer', 30], ['ndfeb', 30]],
         color='#B7BCC0', info='Münzgroßer Motor mit Unwucht. Brummt bei Nachrichten und Weckalarm.'),
    teil('akku', 'li_ion_battery', 'Lithium-Polymer-Akku', 'Akku', 'box',
         x=3, y=10, w=10, d=20, z=4.8, h=3.5, r=1.5, mass=3,
         materials=[['lco', 40], ['graphit', 20], ['elektrolyt', 15], ['alu', 15], ['kupfer', 10]], color='#9DA6AD',
         info='Kleine Zelle mit etwa 120 mAh. Fest verklebt: nicht aufbiegen, Kontakte abkleben und zur Batterie-Sammelstelle bringen.',
         marks=[mark('box', 1.5, 2, 7, 14, 1)]),
    teil('soc', 'circuit_board', 'Prozessor mit Bluetooth', 'Prozessor', 'box',
         x=4, y=31, w=6, d=6, z=4.8, h=0.8, r=0.3, mass=0.15, materials=[['chip', 100]], color=CHIP,
         info='Wertet die Sensoren aus und funkt die Daten per Bluetooth ans Handy.'),
    teil('sensorchip', 'circuit_board', 'Bewegungssensor', 'Sensor', 'box',
         x=11.5, y=32, w=4, d=4, z=4.8, h=0.8, r=0.3, mass=0.05, materials=[['chip', 100]], color=CHIP,
         info='Misst jede Bewegung des Arms und zählt so die Schritte.'),
    teil('platine', 'circuit_board', 'Platine', 'Platine', 'box',
         x=2.5, y=7, w=15, d=32, z=4, h=0.8, r=2, mass=1, color='#2E6B45',
         info='Winzige, mehrlagige Leiterplatte. Mit den anderen Teilen in die Elektro-Sammlung.'),
    teil('unterschale', 'plastic_housing', 'Gehäuse-Unterteil', 'Unterteil', 'box',
         x=0.5, y=4, w=19, d=38, z=1, h=4, r=9, mass=2, color=GEH,
         info='Boden mit Fenster für den Pulssensor und zwei Ladekontakten aus Edelstahl.',
         marks=[mark('box', 5, 13, 9, 12, 3, '#1E2226'), mark('cyl', 6, 31, 2.5, fill='#C9A227'),
                mark('cyl', 10.5, 31, 2.5, fill='#C9A227')]),
    teil('pulssensor', 'circuit_board', 'Optischer Pulssensor', 'Pulssensor', 'box', material_id='mixed_electronics',
         x=5.5, y=17, w=9, d=12, z=0, h=1.5, r=3, mass=0.5, materials=[['pcabs', 40], ['led', 30], ['chip', 30]],
         color='#3A3F44',
         info='Grüne LEDs leuchten in die Haut, eine Fotodiode misst, wie viel Licht zurückkommt. Daraus wird der Puls berechnet.',
         marks=[mark('cyl', 1, 4, 3, fill='#5FBF6E'), mark('cyl', 5, 4, 3, fill='#5FBF6E'), mark('box', 2.5, 8, 4, 2.5, 0.5, '#22272B')]),
    teil('armband_hinten', 'silicone_strap', 'Armband, hinteres Teil (gekürzt)', 'Armband', 'box',
         x=2, y=0, w=16, d=4, z=2, h=3, r=1, mass=7, explode=[0, -25, 0], color='#3A4148',
         info='Silikonband, hier gekürzt gezeigt. Mit dem Schnellverschluss abziehen; reines Silikon gehört in den Restmüll.',
         marks=[mark('box', 2, 0.5, 12, 1.5, 0.5, '#2B3035')]),
    teil('armband_vorne', 'silicone_strap', 'Armband, vorderes Teil mit Löchern (gekürzt)', 'Armband vorne', 'box',
         x=2, y=42, w=16, d=4, z=2, h=3, r=1, mass=8, explode=[0, 25, 0], color='#3A4148', label=False,
         info='Zweite Bandhälfte mit Lochreihe und Schließe. Ein Band wiegt zusammen etwa 15 g.',
         marks=[mark('cyl', 6.5, 1, 3, fill='#2B3035')]),
]

explodiere(teile, abstand=18, abstaende={'soc': 6, 'sensorchip': 6, 'motor': 6}, nach_liste=True)
skaliere_masse(teile, oid='fitness_tracker', stellen=2)
schreibe('fitness_tracker', teile)
