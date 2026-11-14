"""3D-Modell: headphones. Erzeugt tools/kategorien/modelle/headphones.json.

Typischer kabelgebundener Over-Ear-Kopfhörer, flach hingelegt: Ohrmuscheln vorn links und rechts mit den
Polstern nach oben, Kopfbügel nach hinten (y = 0). 180 × 175 × 75 mm. Das Kabel kommt aus der linken Muschel
und liegt aufgerollt zwischen den Muscheln. Die linke Muschel wird ganz zerlegt, die rechte nur bis zum Lautsprecher.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

POLSTER = [['kunstleder', 25], ['schaum', 75]]   # PU-Schaum mit Kunstleder-Bezug
TREIBER = [['folien', 25], ['kupfer', 35], ['pcabs', 40]]
MAGNET = [['ndfeb', 55], ['stahl', 45]]
SCHWARZ = '#2F3338'
POLSTERFARBE = '#3A3F44'


def schrauben(x0, y0):
    """Vier Schraubenköpfe auf der Schallwand (relativ zum Teil)."""
    return [mark('cyl', x0 + dx, y0 + dy, 3.5, fill='#8A9095') for dx, dy in ((4, 36), (52, 36), (26, 4), (26, 70))]


teile = [
    teil('polster_l', 'ear_cushions', 'Ohrpolster links', 'Ohrpolster', 'cyl',
         x=2, y=78, w=70, d=90, z=48, h=24, mass=14, materials=POLSTER, color=POLSTERFARBE, wand=16, boden=0,
         info='Schaumstoff mit Kunstleder-Bezug. Meist nur eingeklipst oder eingedreht: am Rand greifen und abziehen. '
              'Ersatzpolster gibt es günstig.',
         marks=[mark('cyl', 5, 6, 60, 78, fill='#33383C', zeichnung=True), mark('cyl', 15, 19, 40, 52, fill='#25292C', zeichnung=True)]),
    teil('polster_r', 'ear_cushions', 'Ohrpolster rechts', 'Ohrpolster', 'cyl',
         x=108, y=78, w=70, d=90, z=48, h=24, mass=14, materials=POLSTER, color=POLSTERFARBE, label=False, wand=16, boden=0,
         info='Gleiches Polster für das rechte Ohr. Verschlissene Polster lieber tauschen als den ganzen Kopfhörer wegwerfen.',
         marks=[mark('cyl', 5, 6, 60, 78, fill='#33383C', zeichnung=True), mark('cyl', 15, 19, 40, 52, fill='#25292C', zeichnung=True)]),
    teil('stoff_l', 'ear_cushions', 'Staubschutz-Stoff', 'Staubschutz', 'cyl', material_id='polyester',
         x=12, y=93, w=50, d=60, z=46.5, h=1, mass=0.5, materials=[['textil', 100]], color='#45494D',
         info='Dünner Stoff vor dem Lautsprecher. Lässt den Schall durch und hält Staub und Haare fern.',
         marks=[mark('cyl', 5, 6, 40, 48, fill='#4E5357')]),
    teil('membran_l', 'speaker_driver', 'Lautsprecher-Membran mit Schwingspule', 'Membran', 'cyl',
         material_id='mixed_electronics', x=17, y=103, w=40, z=41, h=5, mass=4, materials=TREIBER, color='#C9CDD1',
         info='40-mm-Membran aus dünner Kunststofffolie. Hinten klebt eine Kupferspule, die im Magnetfeld hin und her schwingt.',
         marks=[mark('cyl', 3, 3, 34, fill='#B9BEC2'), mark('cyl', 6, 6, 28), mark('cyl', 13, 13, 14, fill='#C98F62')]),
    teil('schallwand_l', 'plastic_housing', 'Schallwand mit Schrauben', 'Schallwand', 'cyl',
         x=7, y=84, w=60, d=78, z=40, h=4, mass=8, color='#3A3F44',
         info='Trägt den Lautsprecher und ist mit vier kleinen Kreuzschrauben in der Muschel verschraubt.',
         marks=[mark('cyl', 8, 17, 44, fill='#25292C')] + schrauben(0, 0)),
    teil('magnet_l', 'speaker_driver', 'Neodym-Magnet mit Polplatte', 'Magnet', 'cyl',
         material_id='mixed_electronics', x=24, y=110, w=26, z=30, h=9, mass=10, materials=MAGNET, color='#8A9095',
         info='Starker Neodym-Magnet in einem Stahltopf. Von Bankkarten und Handys fernhalten, er kann Finger einklemmen.',
         marks=[mark('cyl', 3, 3, 20, fill='#9BA3A8'), mark('cyl', 8, 8, 10, fill='#5A6066')]),
    teil('litzen_innen', 'cable_copper_core', 'Innenverkabelung', 'Innenkabel', 'box',
         x=8, y=124, w=16, d=3, z=30, h=2, r=1, mass=0.5, materials=[['kupfer', 60], ['pvc', 40]], color='#C98F62',
         info='Dünne Kupferlitzen, an den Lautsprecher gelötet. Ein Kabel läuft durch den Bügel zur rechten Seite.'),
    teil('treiber_r', 'speaker_driver', 'Lautsprecher rechts', 'Lautsprecher', 'cyl',
         material_id='mixed_electronics', x=123, y=103, w=40, z=32, h=14, mass=14,
         materials=[['ndfeb', 30], ['stahl', 25], ['kupfer', 15], ['folien', 10], ['pcabs', 20]], color='#C9CDD1',
         info='Kompletter Lautsprecher der rechten Seite mit Magnet, Spule und Membran. Gehört mit dem Magneten '
              'in die Elektro-Sammlung.',
         marks=[mark('cyl', 3, 3, 34, fill='#B9BEC2'), mark('cyl', 6, 6, 28), mark('cyl', 13, 13, 14, fill='#C98F62')]),
    teil('kopfpolster', 'plastic_housing', 'Kopfpolster', 'Kopfpolster', 'box',
         material_id='pu_foam', x=50, y=14, w=80, d=12, z=2, h=24, r=6, mass=10, materials=POLSTER, color=POLSTERFARBE,
         info='Polstert den Bügel oben am Kopf. Meist mit Klettband oder Klebstoff befestigt.',
         marks=raster(6, 4, 7, 1, 6, 4, 10, r=2, fill='#33383C')),
    teil('schale_l', 'plastic_housing', 'Ohrmuschel links', 'Ohrmuschel', 'cyl',
         x=2, y=78, w=70, d=90, z=0, h=48, mass=42, color=SCHWARZ, wand=3,
         info='Gehäuse aus ABS. Die Schrauben liegen unter dem Ohrpolster. Erst Lautsprecher und Kabel entfernen, '
              'dann ist die Schale sortenreiner Kunststoff.',
         marks=[mark('cyl', 4, 5, 62, 80, fill='#272B2F', zeichnung=True)]),
    teil('schale_r', 'plastic_housing', 'Ohrmuschel rechts', 'Ohrmuschel', 'cyl',
         x=108, y=78, w=70, d=90, z=0, h=48, mass=45, label=False, color=SCHWARZ, wand=3,
         info='Rechte Ohrmuschel, gleich aufgebaut. Hier kommt das Kabel innen von links über den Bügel an.',
         marks=[mark('cyl', 4, 5, 62, 80, fill='#272B2F', zeichnung=True),
                mark('cyl', 14, 22, 42, 46, fill='#25292C', zeichnung=True)]
         + [dict(m, zeichnung=True) for m in schrauben(7, 6)]),
    teil('buegel', 'plastic_housing', 'Kopfbügel mit Federstahl', 'Kopfbügel', 'box',
         material_id='abs', x=30, y=0, w=120, d=14, z=0, h=30, r=7, mass=40, materials=[['pcabs', 55], ['stahl', 45]],
         color=SCHWARZ,
         info='Kunststoffbügel mit eingelegtem Federstahlband, das die Muscheln an den Kopf drückt. '
              'Mit einem Magneten findet man den Stahl.', marks=[mark('box', 3, 3, 114, 8, 4, '#3A3F44')]),
    teil('gleiter_l', 'plastic_housing', 'Verstellbarer Gleitarm links', 'Gleitarm', 'box',
         material_id='steel', x=31, y=14, w=12, d=64, z=6, h=20, r=4, mass=12, explode=[0, 0, 0], label=False, materials=[['stahl', 70], ['pcabs', 30]],
         color='#B9BEC2', info='Ausziehbarer Stahlbügel zum Anpassen der Größe. Innen läuft das Kabel zur Ohrmuschel.',
         marks=raster(4, 6, 1, 6, 4, 2, 0, 8, r=1, fill='#8A9095')),
    teil('gleiter_r', 'plastic_housing', 'Verstellbarer Gleitarm rechts', 'Gleitarm', 'box',
         material_id='steel', x=137, y=14, w=12, d=64, z=6, h=20, r=4, mass=12, explode=[45, 0, 0], materials=[['stahl', 70], ['pcabs', 30]],
         color='#B9BEC2', info='Rechter Gleitarm. Bricht er, gibt es für viele Modelle Ersatzteile.',
         marks=raster(4, 6, 1, 6, 4, 2, 0, 8, r=1, fill='#8A9095')),
    teil('tuelle', 'cable_insulation', 'Knickschutz-Tülle', 'Knickschutz', 'box',
         x=72, y=150, w=6, d=8, z=6, h=8, r=2, mass=1, color='#25292C', materials=[['tpe', 100]],
         info='Weiche Gummitülle, wo das Kabel aus der Muschel kommt. Verhindert, dass die Adern dort brechen.'),
    teil('kabel', 'cable_insulation', 'Kabelmantel (aufgerollt)', 'Kabel', 'cyl', form='torus',
         x=76, y=120, w=28, z=0, h=8, mass=11, explode=[130, 0, 0], color='#25292C',
         info='Etwa 1,2 m PVC-Kabel. Mit einer Abisolierzange lässt sich der Mantel vom Kupfer trennen.',
         marks=[mark('cyl', 3, 3, 22), mark('cyl', 6, 6, 16), mark('cyl', 9, 9, 10, fill='#3A3F44', zeichnung=True)]),
    teil('litzen', 'cable_copper_core', 'Kupferlitzen', 'Kupferlitzen', 'cyl', form='torus',
         x=79, y=123, w=22, z=1, h=6, mass=5, explode=[160, 0, 0], color='#C98F62',
         info='Drei sehr dünne lackierte Kupferlitzen für links, rechts und Masse. Kupfer ist fast beliebig oft recycelbar.',
         marks=[mark('cyl', 3, 3, 16), mark('cyl', 6, 6, 10, fill='#B9805A', zeichnung=True)]),
    teil('stecker', 'cable_copper_core', 'Klinkenstecker 3,5 mm', 'Klinkenstecker', 'box', form='liegend_y',
         material_id='mixed_electronics', x=84, y=150, w=6, d=24, z=0, h=6, r=3, mass=3, explode=[150, 0, 0],
         materials=[['messing', 60], ['pcabs', 30], ['kontakte', 10]], color='#B9BEC2',
         info='Vergoldeter Messingstift mit drei Kontakten. Zum Recyceln einfach am Kabel lassen.',
         marks=[mark('box', 0.5, 0, 5, 12, 2.5, '#25292C'), mark('box', 1.5, 15, 3, 1, 0.5, '#2B2F33'),
                mark('box', 1.5, 19, 3, 1, 0.5, '#2B2F33')]),
]

explodiere(teile, abstand=34, abstaende={'stoff_l': 22, 'litzen_innen': 14})
skaliere_masse(teile, oid='headphones')
for p in teile:   # Foto-Ansicht: echte Formen (form) tragen keine aufgemalten Details
    if p.get('form') and p.get('marks'):
        p['marks'] = [dict(k, zeichnung=True) for k in p['marks']]
schreibe('headphones', teile)
