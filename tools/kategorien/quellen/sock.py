"""3D-Modell: sock. Erzeugt tools/kategorien/modelle/sock.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Sportsocke flach hingelegt (seitlich), Bündchen hinten (y = 0), Spitze vorne (y = 250). 90 × 250 × 5 mm.
# Schaft und Fuß sind ein 72 mm breiter Schlauch, die Ferse wölbt sich rechts heraus.
# Explodiert werden die Abschnitte entlang der Länge auseinandergezogen, die Ferse nach rechts,
# der Gummifaden schwebt über dem Bündchen.
STOFF = '#9AA3AA'
RIPPE = '#8A939A'
VERST = '#4A535A'
STREIFEN = '#B8433A'
GARN = [['baumwolle', 80], ['nylon', 17], ['tpu', 3]]
VERST_GARN = [['baumwolle', 70], ['nylon', 30]]


def rippen(w, d, fill=RIPPE, abstand=6):
    """Feine Maschenrippen in Längsrichtung (y)."""
    n = int((w - 4) // abstand)
    return raster(3, 1, n, 1, 1.2, d - 2, abstand, fill=fill)


teile = [
    teil('gummifaden', 'cotton_fabric', 'Elasthan-Gummifaden', 'Gummifaden', 'box', material_id='polyester',
         x=4, y=4, w=64, d=32, z=1.5, h=1, r=2, mass=1, materials=[['tpu', 100]], color='#E4DED0',
         explode=[0, -55, 22],
         info='Im Bündchen läuft ein umsponnener Elasthanfaden rundherum mit. Er hält die Socke am Bein und '
              'lässt sich nicht heraustrennen.',
         marks=raster(0, 3, 1, 6, 64, 1.5, 0, 5, fill='#B9B2A2')),
    teil('bund', 'cotton_fabric', 'Rippenbündchen', 'Bündchen', 'box',
         x=0, y=0, w=72, d=40, z=0, h=4.5, r=3, mass=6, materials=GARN, color=STOFF, explode=[0, -55, 0],
         info='Doppelt gestrickter Rand im Rippenmuster. Rippen und Gummifaden machen ihn dehnbar.',
         marks=raster(2, 1, 12, 1, 3, 38, 6, fill=RIPPE)),
    teil('schaft', 'cotton_fabric', 'Schaft mit Ringeln', 'Schaft', 'box',
         x=0, y=40, w=72, d=80, z=0, h=4, r=2, mass=9, materials=GARN, color=STOFF, explode=[0, -22, 0],
         info='Rundgestrickter Schlauch aus Baumwolle mit etwas Polyamid, die Ringel sind mit eingestrickt. '
              'Tragbare Socken paarweise in die Altkleidersammlung.',
         marks=rippen(72, 80) + [mark('box', 0, 8, 72, 5, 0, STREIFEN), mark('box', 0, 17, 72, 5, 0, STREIFEN)]),
    teil('ferse', 'cotton_fabric', 'Verstärkte Ferse', 'Ferse', 'cyl',
         x=38, y=102, w=52, d=68, z=0, h=4.3, mass=5, materials=VERST_GARN, color=VERST, explode=[75, 0, 0],
         info='Die Ferse ist als Käppchen eingestrickt und mit mehr Polyamid verstärkt, weil sie am stärksten reibt.',
         marks=[mark('cyl', 7, 8, 38, 52, fill='#424A50')]),
    teil('fuss', 'cotton_fabric', 'Fußteil mit Frotteesohle', 'Fuß', 'box',
         x=0, y=120, w=72, d=100, z=0, h=4, r=2, mass=13, materials=GARN, color=STOFF, explode=[0, 18, 0],
         info='Innen unter der Sohle als Frottee gestrickt (kleine Schlaufen), das polstert. Löcher lassen sich stopfen.',
         marks=rippen(72, 100)),
    teil('spitze', 'cotton_fabric', 'Spitze mit Kettelnaht', 'Spitze', 'box',
         x=0, y=205, w=72, d=45, z=0, h=4.4, r=20, mass=6, materials=VERST_GARN, color=VERST, explode=[0, 55, 0],
         info='Verstärkte Zehenpartie. Sie wird zuletzt flach zusammengekettelt, die Naht drückt so kaum.',
         marks=[mark('box', 2, 30, 68, 1.5, 0.5, '#2F363B')]),
]

skaliere_masse(teile, oid='sock')
schreibe('sock', teile)
