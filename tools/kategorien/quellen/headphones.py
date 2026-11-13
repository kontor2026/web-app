"""3D-Modell: headphones. Erzeugt tools/kategorien/modelle/headphones.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Typischer kabelgebundener Over-Ear-Kopfhörer, flach hingelegt: Ohrmuscheln vorn links und rechts mit den
# Polstern nach oben, Kopfbügel als Bogen nach hinten (y = 0). 180 × 170 × 75 mm. Kabel liegt aufgerollt im Bügel.
POLSTER = [['schaum', 75], ['kunstleder', 25]]   # PU-Schaum mit Kunstleder-Bezug
TREIBER = [['folien', 25], ['kupfer', 35], ['pcabs', 40]]
MAGNET = [['ndfeb', 55], ['stahl', 45]]

teile = [
    teil('polster_l', 'ear_cushions', 'Ohrpolster links', 'Ohrpolster', 'cyl',
         x=2, y=78, w=70, d=90, z=48, h=27, mass=14, materials=POLSTER, color='#3A3F44',
         info='Schaumstoff mit Kunstleder-Bezug. Meist nur eingeklipst oder eingedreht: am Rand greifen und abziehen. Ersatzpolster gibt es günstig.',
         marks=[mark('cyl', 17, 22, 36, 46, fill='#2B2F33')]),
    teil('polster_r', 'ear_cushions', 'Ohrpolster rechts', 'Ohrpolster', 'cyl',
         x=108, y=78, w=70, d=90, z=48, h=27, mass=14, materials=POLSTER, color='#3A3F44', label=False,
         info='Gleiches Polster für das rechte Ohr. Verschlissene Polster lieber tauschen als den ganzen Kopfhörer wegzuwerfen.',
         marks=[mark('cyl', 17, 22, 36, 46, fill='#2B2F33')]),
    teil('membran_l', 'speaker_driver', 'Lautsprecher-Membran mit Schwingspule', 'Membran', 'cyl',
         material_id='mixed_electronics', x=17, y=103, w=40, z=42, h=5, mass=4, materials=TREIBER, color='#C9CDD1',
         info='40-mm-Membran aus dünner Kunststofffolie. Hinten klebt eine Kupferspule, die im Magnetfeld hin und her schwingt.',
         marks=[mark('cyl', 5, 5, 30), mark('cyl', 13, 13, 14, fill='#C98F62')]),
    teil('magnet_l', 'speaker_driver', 'Neodym-Magnet mit Polplatte', 'Magnet', 'cyl',
         material_id='mixed_electronics', x=24, y=110, w=26, z=32, h=9, mass=10, materials=MAGNET, color='#8A9095',
         info='Starker Neodym-Magnet in einem Stahltopf. Von Bankkarten und Handys fernhalten, er kann Finger einklemmen.',
         marks=[mark('cyl', 8, 8, 10, fill='#5A6066')]),
    teil('treiber_r', 'speaker_driver', 'Lautsprecher rechts', 'Lautsprecher', 'cyl',
         material_id='mixed_electronics', x=123, y=103, w=40, z=32, h=15, mass=14,
         materials=[['ndfeb', 30], ['stahl', 25], ['kupfer', 15], ['folien', 10], ['pcabs', 20]], color='#C9CDD1',
         info='Kompletter Lautsprecher der rechten Seite mit Magnet, Spule und Membran. Gehört mit dem Magneten in die Elektro-Sammlung.',
         marks=[mark('cyl', 5, 5, 30), mark('cyl', 13, 13, 14, fill='#C98F62')]),
    teil('kopfpolster', 'plastic_housing', 'Kopfpolster', 'Kopfpolster', 'box',
         material_id='pu_foam', x=50, y=14, w=80, d=12, z=0, h=26, r=6, mass=10, materials=POLSTER, color='#3A3F44',
         info='Polstert den Bügel oben am Kopf. Meist mit Klettband oder Klebstoff befestigt.'),
    teil('schale_l', 'plastic_housing', 'Ohrmuschel links', 'Ohrmuschel', 'cyl',
         x=2, y=78, w=70, d=90, z=0, h=48, mass=45,
         info='Gehäuse mit Schallwand für den Lautsprecher. Die Schrauben liegen unter dem Ohrpolster.',
         marks=[mark('cyl', 10, 12, 50, 66, fill='#2B2F33')]),
    teil('schale_r', 'plastic_housing', 'Ohrmuschel rechts', 'Ohrmuschel', 'cyl',
         x=108, y=78, w=70, d=90, z=0, h=48, mass=45, label=False,
         info='Rechte Ohrmuschel, gleich aufgebaut. Hier kommt das Kabel innen von links über den Bügel an.',
         marks=[mark('cyl', 10, 12, 50, 66, fill='#2B2F33')]),
    teil('buegel', 'plastic_housing', 'Kopfbügel mit Federstahl', 'Kopfbügel', 'box',
         material_id='abs', x=30, y=0, w=120, d=14, z=0, h=30, r=6, mass=40, materials=[['pcabs', 55], ['stahl', 45]],
         info='Kunststoffbügel mit eingelegtem Federstahlband, das die Muscheln an den Kopf drückt. Mit einem Magneten findet man den Stahl.'),
    teil('gleiter_l', 'plastic_housing', 'Verstellbarer Gleitarm links', 'Gleitarm', 'box',
         material_id='abs', x=30, y=14, w=14, d=64, z=4, h=24, r=4, mass=12, materials=[['pcabs', 70], ['stahl', 30]],
         info='Lässt sich herausziehen, um die Größe anzupassen. Innen läuft das Kabel zur Ohrmuschel.',
         marks=raster(3, 6, 1, 6, 8, 2, 0, 8, r=1)),
    teil('gleiter_r', 'plastic_housing', 'Verstellbarer Gleitarm rechts', 'Gleitarm', 'box',
         material_id='abs', x=136, y=14, w=14, d=64, z=4, h=24, r=4, mass=12, materials=[['pcabs', 70], ['stahl', 30]],
         label=False, info='Rechter Gleitarm. Bricht er, gibt es für viele Modelle Ersatzteile.',
         marks=raster(3, 6, 1, 6, 8, 2, 0, 8, r=1)),
    teil('kabel', 'cable_insulation', 'Kabelmantel (aufgerollt)', 'Kabel', 'cyl',
         x=62, y=30, w=46, z=0, h=6, mass=11, explode=[150, 0, 0], color='#2B2F33',
         info='Etwa 1,2 m PVC-Kabel mit 3,5-mm-Stecker. Mit einer Abisolierzange lässt sich der Mantel vom Kupfer trennen.',
         marks=[mark('cyl', 5, 5, 36), mark('cyl', 10, 10, 26), mark('cyl', 15, 15, 16, fill='#F2EFE8')]),
    teil('litzen', 'cable_copper_core', 'Kupferlitzen', 'Kupferlitzen', 'cyl',
         x=67, y=35, w=36, z=1, h=4, mass=5, explode=[150, 0, 30], color='#C98F62',
         info='Drei sehr dünne lackierte Kupferlitzen für links, rechts und Masse. Kupfer ist fast beliebig oft recycelbar.',
         marks=[mark('cyl', 5, 5, 26), mark('cyl', 10, 10, 16, fill='#F2EFE8')]),
    teil('stecker', 'cable_copper_core', 'Klinkenstecker 3,5 mm', 'Klinkenstecker', 'box',
         material_id='mixed_electronics', x=112, y=38, w=24, d=6, z=0, h=6, r=3, mass=3, explode=[150, 0, 0],
         materials=[['messing', 60], ['pcabs', 30], ['kontakte', 10]], color='#B9BEC2',
         info='Vergoldeter Messingstift mit drei Kontakten. Zum Recyceln einfach am Kabel lassen.',
         marks=[mark('box', 13, 1.5, 1, 3, 0.5, '#2B2F33'), mark('box', 17, 1.5, 1, 3, 0.5, '#2B2F33')]),
]

explodiere(teile, abstand=40)
skaliere_masse(teile, oid='headphones')
schreibe('headphones', teile)
