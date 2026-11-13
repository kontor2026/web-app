"""3D-Modell: smartwatch. Erzeugt tools/kategorien/modelle/smartwatch.json.

Typische eckige Smartwatch (Gehäuse 37 × 38 × 11 mm, Aluminium), liegt mit dem Display nach oben.
Innen von oben nach unten: Deckglas, OLED, Akku, Platine mit SoC, Vibrationsmotor, Ladespule, Rückdeckel mit
Pulssensor. Krone und Seitentaste werden nach rechts (dx positiv) gezogen, die Armbandansätze nach vorne und hinten.
Das Armband ist nur mit seinen Ansätzen am Gehäuse modelliert (sonst passt die Uhr nicht in die CSV-Maße).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

ALU = '#C3C8CC'
CHIP = '#22272B'
BAND = '#3A4A5C'
ZELLE = [['lco', 40], ['graphit', 20], ['elektrolyt', 15], ['alu', 15], ['kupfer', 10]]

teile = [
    teil('deckglas', 'smartwatch_display', 'Deckglas', 'Deckglas', 'box',
         x=1, y=6, w=35, d=36, z=10, h=1, r=9, mass=2.5, materials=[['glas', 100]], color='#C9DEDF', opacity=0.6,
         info='Gehärtetes, leicht gewölbtes Glas, zugleich Touch-Fläche. Mit Wärme lösen und mit einer dünnen Klinge '
              'anheben: Direkt darunter liegt der Akku.'),
    teil('display', 'smartwatch_display', 'OLED-Display', 'Display', 'box',
         x=1.5, y=6.5, w=34, d=35, z=9.2, h=0.8, r=8, mass=2,
         materials=[['displayglas', 55], ['folien', 25], ['chip', 10], ['kupfer', 10]], color='#31373B',
         info='Selbstleuchtende OLED-Anzeige, braucht kein Hintergrundlicht. Ein schmales Flachbandkabel führt zur Platine.',
         marks=[mark('box', 2, 2, 30, 31, 7, '#3D464C')]),
    teil('krone', 'aluminium_housing', 'Drehkrone', 'Krone', 'box', material_id='steel',
         x=37, y=17, w=3.5, d=7, z=4.5, h=4, r=1.5, explode=[18, 0, 0], mass=0.6, materials=[['stahl', 85], ['gummi', 15]],
         info='Edelstahlrädchen mit Dichtring zum Scrollen. Sitzt mit einer Achse im Gehäuse, ein Sensor erkennt die Drehung.',
         color='#B7BCC0'),
    teil('taste', 'aluminium_housing', 'Seitentaste', 'Taste', 'box', material_id='steel',
         x=37, y=29, w=2.5, d=8, z=5, h=3, r=1, explode=[18, 0, 0], mass=0.3, materials=[['stahl', 80], ['gummi', 20]],
         info='Kleine Drucktaste mit Gummidichtung, damit kein Wasser eindringt.', color='#B7BCC0'),
    teil('akku', 'li_ion_battery', 'Lithium-Ionen-Akku', 'Akku', 'box',
         x=6, y=10, w=25, d=24, z=5.6, h=3.4, r=3, mass=5, materials=ZELLE, color='#9DA6AD',
         info='Etwa 300 mAh, flach in einer Folientasche. Klebt fest: nicht mit Metall hebeln, '
              'Pole abkleben und zur Batterie-Sammelstelle bringen.',
         marks=[mark('box', 2, 2, 21, 20, 2), mark('box', 4, 4, 9, 5, 1, '#C8423A')]),
    teil('soc', 'circuit_board', 'Prozessor mit Speicher (SiP)', 'Prozessor', 'box',
         x=12, y=16, w=12, d=12, z=4.6, h=1, r=0.5, mass=0.5, materials=[['chip', 100]], color=CHIP,
         info='Rechenkern, Arbeitsspeicher und Speicher in einem Baustein. Hier liegen auch Gesundheitsdaten: '
              'Uhr vorher zurücksetzen.',
         marks=[mark('cyl', 1, 1, 1.5)]),
    teil('platine', 'circuit_board', 'Hauptplatine', 'Platine', 'box',
         x=4, y=9, w=29, d=30, z=3.6, h=1, r=6, mass=2.5, color='#2E6B45',
         info='Kleine, dicht bestückte Leiterplatte mit Funkchips für Bluetooth und WLAN. Mit Gold und Kupfer: ab zur E-Schrott-Sammlung.',
         marks=raster(3, 3, 3, 1, 4, 3, 6, fill=CHIP) + [mark('box', 22, 22, 5, 5, 0.5, '#B7BCC0')]),
    teil('motor', 'circuit_board', 'Vibrationsmotor', 'Vibration', 'box', material_id='mixed_electronics',
         x=26, y=34, w=8, d=6, z=2.2, h=1.6, r=1, mass=1, materials=[['stahl', 40], ['ndfeb', 30], ['kupfer', 30]],
         info='Ein kleiner Magnet wird von einer Spule hin und her bewegt, so spürt man Benachrichtigungen am Handgelenk.',
         color='#9BA3A8'),
    teil('ladespule', 'circuit_board', 'Ladespule', 'Ladespule', 'cyl', material_id='mixed_electronics',
         x=8.5, y=13.5, w=20, z=2.2, h=0.6, mass=0.8, materials=[['kupfer', 60], ['ferrit', 30], ['klebstoff', 10]],
         info='Flache Kupferspule auf einer Ferritfolie. Nimmt die Energie der magnetischen Ladeschale kabellos auf.',
         color='#C5803D', marks=[mark('cyl', 3, 3, 14, fill='#B06F33'), mark('cyl', 6, 6, 8, fill='#3A3F44')]),
    teil('gehaeuse', 'aluminium_housing', 'Aluminium-Gehäuse', 'Gehäuse', 'box',
         x=0, y=5, w=37, d=38, z=1.5, h=8.5, r=10, mass=9, materials=[['alu', 100]], color=ALU,
         info='Gefräster Aluminiumrahmen. Erst alle Teile ausbauen, dann ist die leere Schale reines Aluminium.',
         marks=[mark('box', 1.5, 1.5, 34, 35, 9, '#9DA4A9')]),
    teil('rueckdeckel', 'aluminium_housing', 'Rückdeckel', 'Rückdeckel', 'box', material_id='pc',
         x=3.5, y=8.5, w=30, d=31, z=0.6, h=1.4, r=9, mass=2.5, materials=[['pcabs', 80], ['glas', 20]],
         info='Kunststoffboden mit Glasfenster für den Pulssensor, verklebt oder verschraubt. Er liegt beim Tragen auf der Haut.',
         color='#2F3438', marks=[mark('cyl', 7, 7.5, 16, fill='#454C52')]),
    teil('sensor', 'circuit_board', 'Pulssensor (LEDs und Fotodioden)', 'Pulssensor', 'cyl', material_id='mixed_electronics',
         x=12.5, y=18, w=12, z=0, h=1.2, mass=0.4, materials=[['led', 30], ['chip', 30], ['glas', 25], ['kupfer', 15]],
         info='Grüne LEDs leuchten in die Haut, Fotodioden messen, wie viel Licht das Blut zurückwirft. Daraus wird der Puls.',
         color='#3A3F44', marks=[mark('cyl', 2, 5, 2.5, fill='#5FBF6A'), mark('cyl', 7.5, 5, 2.5, fill='#5FBF6A'),
                                mark('cyl', 4.5, 1.5, 3, fill='#262B2F'), mark('cyl', 4.5, 7.5, 3, fill='#262B2F')]),
    teil('band_oben', 'silicone_strap', 'Armband oben (Ansatz)', 'Armband', 'box',
         x=7.5, y=-1, w=22, d=6, z=2.5, h=4, r=2, explode=[0, -16, 0], mass=5, color=BAND,
         info='Silikonarmband, mit einem Schnellverschluss-Stift im Gehäuse eingehakt. Stift drücken und herausschieben.',
         marks=[mark('box', 2, 1, 18, 2, 1, '#2C3947')]),
    teil('band_unten', 'silicone_strap', 'Armband unten (Ansatz)', 'Armband', 'box',
         x=7.5, y=43, w=22, d=6, z=2.5, h=4, r=2, explode=[0, 16, 0], mass=5, color=BAND, label=False,
         info='Zweite Bandhälfte mit Löchern für die Schließe. Silikon ist kein Elektroschrott und kann abgetrennt werden.',
         marks=[mark('box', 2, 3, 18, 2, 1, '#2C3947')]),
]

explodiere(teile, abstand=18, abstaende={'soc': 6})
skaliere_masse(teile, oid='smartwatch')
schreibe('smartwatch', teile)
