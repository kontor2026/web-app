"""3D-Modell: remote_control. Erzeugt tools/kategorien/modelle/remote_control.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Typische TV-Fernbedienung, 45 × 180 × 20 mm, Tasten oben, Infrarot-LED hinten (y = 0), Batteriefach unten.
tasten = (
    [mark('cyl', 3, 3, 7, fill='#C9302C')]                              # Ein/Aus
    + raster(4, 15, 3, 4, 8, 6, 12, 9, r=2)                             # Ziffern 1–9, 0
    + [mark('cyl', 9, 54, 21), mark('cyl', 15, 60, 9, fill='#2B2F33')]  # Steuerkreuz mit OK
    + raster(3, 81, 2, 3, 6, 8, 25, 10, r=2)                            # Lautstärke / Programm
    + raster(4, 113, 4, 1, 6, 5, 8, r=2, fill='#5F8F4E')               # Farbtasten
)

teile = [
    teil('oberschale', 'plastic_housing', 'Oberschale', 'Oberschale', 'box',
         x=0, y=0, w=45, d=180, z=10, h=7, r=10, mass=24,
         info='Hat Löcher für die Gummitasten. Meist nur mit Rastnasen verklipst: mit einem Plektrum an der Fuge entlang aufhebeln.',
         marks=[mark('box', 4, 18, 37, 128, 6, '#2B2F33')]),
    teil('tastenmatte', 'silicone_keypad', 'Silikon-Tastenmatte', 'Tastenmatte', 'box',
         x=4, y=18, w=37, d=128, z=7.6, h=12.4, r=6, mass=14, color='#4A5258',
         info='Alle Tasten sind eine einzige Silikonmatte. Unter jeder Taste klebt eine schwarze Kohle-Pille, die den Kontakt schließt.',
         marks=tasten),
    teil('chip', 'circuit_board', 'Steuer-Chip', 'Chip', 'box',
         material_id='pcb', x=17, y=150, w=10, d=8, z=7.6, h=1.4, r=0.5, mass=0.4, materials=[['chip', 100]],
         color='#2B2F33', info='Erkennt die gedrückte Taste und schaltet die Infrarot-LED in einem bestimmten Blinkmuster an und aus.'),
    teil('quarz', 'circuit_board', 'Keramik-Resonator', 'Resonator', 'box',
         material_id='mixed_electronics', x=29, y=150, w=7, d=4, z=7.6, h=3, r=1, mass=0.3,
         materials=[['keramik', 70], ['kupfer', 30]], color='#3E7FB6',
         info='Gibt den Takt vor, mit dem die LED blinkt (meist 38.000-mal pro Sekunde).'),
    teil('ir_led', 'circuit_board', 'Infrarot-LED', 'IR-LED', 'cyl',
         material_id='mixed_electronics', x=18, y=0, w=5, z=9, h=5, mass=0.3, materials=[['led', 50], ['kupfer', 50]],
         color='#5A5F8C', opacity=0.85,
         info='Sendet für unser Auge unsichtbares Licht zum Fernseher. Mit einer Handykamera sieht man sie beim Drücken leuchten.'),
    teil('platine', 'circuit_board', 'Leiterplatte mit Kontaktfeldern', 'Platine', 'box',
         x=4, y=4, w=37, d=158, z=6, h=1.6, r=4, mass=9, color='#2E6B45',
         info='Unter den Tasten liegen kammartige Kontaktfelder. Meist nur eingelegt, Platine in die Elektro-Sammlung geben.',
         marks=raster(4, 16, 3, 4, 7, 6, 12, 9, r=1, fill='#D9D2B8') + raster(4, 80, 2, 3, 6, 6, 25, 10, r=1, fill='#D9D2B8')),
    teil('kontakte', 'circuit_board', 'Batteriekontakte und Federn', 'Batteriefedern', 'box',
         material_id='steel', x=6, y=112, w=33, d=4, z=1.5, h=9, r=1, mass=1.5, materials=[['stahl', 85], ['kupfer', 15]],
         color='#B9BEC2', info='Vernickelter Federstahl, verbindet die Batterien. Ausgelaufene Batterien hinterlassen hier weißen Belag.'),
    teil('unterschale', 'plastic_housing', 'Unterschale mit Batteriefach', 'Unterschale', 'box',
         x=0, y=0, w=45, d=180, z=0, h=10, r=10, mass=28,
         info='Trägt Platine und Batteriefach. Kunststoffe ohne Elektronik ließen sich gut recyceln, sind aber oft dunkel und schwer sortierbar.',
         marks=[mark('box', 6, 108, 33, 66, 4, '#2B2F33')]),
    teil('batterie_l', 'alkaline_cell', 'Alkaline-Batterie AAA', 'Batterien', 'box',
         x=10, y=118, w=10.5, d=44.5, z=1.5, h=10.5, r=5, mass=11.5, explode=[60, 0, 20], color='#3A6EA5',
         info='Zwei AAA-Zellen mit je 1,5 V. Herausnehmen und in die Batterie-Sammelbox geben, nie in den Restmüll.',
         marks=[mark('box', 1, 1, 8.5, 6, 3, '#C9A227')]),
    teil('batterie_r', 'alkaline_cell', 'Alkaline-Batterie AAA', 'Batterie', 'box',
         x=24.5, y=118, w=10.5, d=44.5, z=1.5, h=10.5, r=5, mass=11.5, explode=[60, 0, 20], color='#3A6EA5', label=False,
         info='Zweite AAA-Zelle, eingelegt mit umgekehrter Polung. Batterien können auslaufen, darum bei längerer Pause herausnehmen.',
         marks=[mark('box', 1, 37.5, 8.5, 6, 3, '#C9A227')]),
    teil('deckel', 'plastic_housing', 'Batteriefachdeckel', 'Batteriedeckel', 'box',
         x=6, y=110, w=33, d=64, z=0, h=1.5, r=4, mass=4, explode=[60, 0, 0],
         info='Wird aufgeschoben und rastet mit einer Nase ein. Zum Öffnen auf die Rillen drücken und schieben.',
         marks=raster(10, 52, 1, 3, 13, 1.5, 0, 3, r=0.5)),
]

explodiere(teile, abstand=30)
skaliere_masse(teile, oid='remote_control')
schreibe('remote_control', teile)
