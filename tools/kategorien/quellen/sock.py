"""3D-Modell: sock. Erzeugt tools/kategorien/modelle/sock.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Eine Socke flach hingelegt, Bündchen hinten (y = 0), Spitze vorne (y = 250). 90 × 250 × 5 mm.
# Eine Socke ist ein nahtlos gestrickter Schlauch; die Abschnitte werden explodiert entlang der Länge
# auseinandergezogen, die Ferse nach rechts.
STOFF = '#5B6770'
VERST = '#3F484F'
GARN = [['baumwolle', 80], ['nylon', 17], ['polyester', 3]]

teile = [
    teil('bund', 'cotton_fabric', 'Bündchen', 'Bündchen', 'box',
         x=5, y=0, w=80, d=45, z=0, h=5, r=3, mass=7, materials=GARN, color=VERST, explode=[0, -45, 0],
         info='Doppelt gestrickter Rand mit eingestricktem Gummifaden (Elasthan), damit die Socke nicht rutscht.',
         marks=raster(4, 2, 10, 1, 4, 41, 8, fill='#2F363B')),
    teil('schaft', 'cotton_fabric', 'Schaft', 'Schaft', 'box',
         x=5, y=45, w=80, d=80, z=0, h=3.5, r=2, mass=9, materials=GARN, color=STOFF, explode=[0, -15, 0],
         info='Rundgestrickter Schlauch aus Baumwolle mit etwas Polyamid. Tragbare Socken paarweise in die Altkleidersammlung.'),
    teil('ferse', 'cotton_fabric', 'Verstärkte Ferse', 'Ferse', 'box',
         x=55, y=112, w=35, d=55, z=0.5, h=4.5, r=14, mass=5, materials=[['baumwolle', 70], ['nylon', 30]],
         color=VERST, explode=[60, 0, 0],
         info='Die Ferse ist als Käppchen eingestrickt und mit mehr Polyamid verstärkt, weil sie am stärksten reibt.'),
    teil('fuss', 'cotton_fabric', 'Fußteil', 'Fuß', 'box',
         x=5, y=125, w=80, d=95, z=0, h=3.5, r=2, mass=13, materials=GARN, color=STOFF, explode=[0, 15, 0],
         info='Unter der Sohle oft als Frottee gestrickt (kleine Schlaufen), das polstert. Löcher lassen sich stopfen.',
         marks=raster(10, 10, 4, 4, 10, 10, 18, 19, shape='cyl', fill='#66737C')),
    teil('spitze', 'cotton_fabric', 'Spitze mit Naht', 'Spitze', 'box',
         x=8, y=220, w=74, d=30, z=0, h=4.5, r=13, mass=6, materials=[['baumwolle', 70], ['nylon', 30]],
         color=VERST, explode=[0, 45, 0],
         info='Verstärkte Zehenpartie. Die Spitze wird zuletzt zugenäht oder flach zusammengekettelt.',
         marks=[mark('box', 6, 4, 62, 2, 1, '#2F363B')]),
]

skaliere_masse(teile, oid='sock')
schreibe('sock', teile)
