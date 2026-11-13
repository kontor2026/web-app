"""3D-Modell: webcam. Erzeugt tools/kategorien/modelle/webcam.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Typische Full-HD-Webcam (Balkenform), auf den Rücken gelegt: Linse zeigt nach oben.
# Körper 92 × 30 mm, unten der eingeklappte Monitor-Clip. Das Kabel kommt rechts heraus
# (gekürzt dargestellt, Masse des ganzen 1,5-m-Kabels) und wird nach rechts gezogen.
GEH = '#25292D'
CHIP = '#3F4547'
teile = [
    teil('frontblende', 'plastic_housing', 'Frontblende', 'Frontblende', 'box', material_id='pc',
         x=0, y=0, w=92, d=30, z=26, h=2, r=12, mass=6, color='#1C1F22',
         info='Glänzende Kunststoffblende mit Fenster für Linse, Mikrofone und Status-LED. Meist eingeclipst und verklebt.',
         marks=[mark('cyl', 34, 3, 24, fill='#0F1113'), mark('cyl', 64, 12.5, 3, fill='#5FBF6E'),
                mark('box', 8, 13.5, 4, 1.5, 0.5, '#0F1113'), mark('box', 80, 13.5, 4, 1.5, 0.5, '#0F1113')]),
    teil('linse', 'webcam_lens', 'Objektiv mit Linsen', 'Objektiv', 'cyl',
         x=37, y=6, w=18, z=20, h=6, mass=2, materials=[['pcabs', 70], ['glas', 30]], color='#3A3F44',
         info='Mehrere kleine Kunststofflinsen in einem Gewinderohr. Lässt sich vom Sensor abschrauben.',
         marks=[mark('cyl', 3, 3, 12, fill='#2E4A6B'), mark('cyl', 6, 6, 6, fill='#4A6E96')]),
    teil('bildsensor', 'circuit_board', 'Bildsensor', 'Bildsensor', 'box',
         x=40, y=9, w=12, d=12, z=18.6, h=1.4, r=0.5, mass=0.5, materials=[['chip', 80], ['glas', 20]], color=CHIP,
         info='Lichtempfindlicher Chip mit Millionen Pixeln. Er wandelt das Bild in elektrische Signale um.',
         marks=[mark('box', 2, 2, 8, 8, 0.3, '#5A4E7A')]),
    teil('steuerchip', 'circuit_board', 'Bildprozessor mit USB', 'Prozessor', 'box',
         x=62, y=10, w=9, d=9, z=18.6, h=1, r=0.3, mass=0.4, materials=[['chip', 100]], color=CHIP,
         info='Komprimiert das Video und schickt es über USB an den Computer.'),
    teil('mikrofon_l', 'circuit_board', 'Mikrofon links', 'Mikrofon', 'box', material_id='mixed_electronics',
         x=8, y=12.5, w=4, d=3, z=18.6, h=1.2, r=0.3, mass=0.1, materials=[['stahl', 50], ['chip', 30], ['kupfer', 20]],
         color='#B7BCC0', info='Winzige MEMS-Mikrofone. Zwei davon filtern Hintergrundgeräusche heraus.'),
    teil('mikrofon_r', 'circuit_board', 'Mikrofon rechts', 'Mikrofon', 'box', material_id='mixed_electronics',
         x=80, y=12.5, w=4, d=3, z=18.6, h=1.2, r=0.3, mass=0.1, materials=[['stahl', 50], ['chip', 30], ['kupfer', 20]],
         color='#B7BCC0', label=False, info='Zweites Mikrofon für Stereo-Ton.'),
    teil('platine', 'circuit_board', 'Platine', 'Platine', 'box',
         x=4, y=3, w=84, d=24, z=17, h=1.6, r=3, mass=6, color='#2E6B45',
         info='Leiterplatte mit Sensor, Prozessor und Mikrofonen. Mit zwei Schrauben in der Rückschale; in die Elektro-Sammlung geben.',
         marks=raster(18, 4, 4, 1, 3, 2, 4, r=0.3, fill='#22272B')),
    teil('rueckschale', 'plastic_housing', 'Rückschale', 'Rückschale', 'box',
         x=0, y=0, w=92, d=30, z=8, h=18, r=12, mass=18, color=GEH,
         info='Hinterer Gehäuseteil mit Kabeldurchführung. Nach Lösen der Schrauben unter dem Clip-Gelenk abnehmbar.',
         marks=[mark('box', 3, 3, 86, 24, 10, '#1E2226')]),
    teil('clip', 'plastic_housing', 'Monitor-Clip', 'Clip', 'box',
         x=21, y=2, w=50, d=26, z=0, h=8, r=4, mass=14, color=GEH,
         info='Klappbarer Halter für den Bildschirmrand, mit Gummiauflage und Stativgewinde. Am Gelenk abschraubbar.',
         marks=[mark('box', 3, 3, 44, 20, 3, '#3A3F44'), mark('cyl', 21, 9, 7, fill='#9BA3A8')]),
    teil('kabelmantel', 'cable_insulation', 'Kabelmantel (gekürzt)', 'Kabelmantel', 'box',
         x=92, y=12.5, w=14, d=5, z=14, h=5, r=2.5, mass=18, explode=[40, 0, 0], color='#1E2226',
         info='PVC-Hülle des 1,5 m langen USB-Kabels, hier gekürzt gezeigt. Mit einem Abisolierwerkzeug längs aufschlitzen.',
         marks=[mark('box', 0, 1, 4, 3, 1, '#3A3F44')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=92, y=13.5, w=14, d=3, z=15, h=3, r=1.5, mass=9, explode=[40, 0, 15], color='#C5803D',
         info='Vier dünne Kupferlitzen für Strom und Daten mit Abschirmgeflecht. Sortenreines Kupfer ist wertvoll.',
         marks=raster(1, 0.3, 4, 1, 2.5, 2.4, 3.3, r=1, fill='#D9954F')),
]

explodiere(teile, abstand=18, abstaende={'bildsensor': 8, 'steuerchip': 8, 'mikrofon_l': 8, 'mikrofon_r': 8}, nach_liste=True)
skaliere_masse(teile, oid='webcam')
schreibe('webcam', teile)
