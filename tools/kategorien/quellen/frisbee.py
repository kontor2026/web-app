"""3D-Modell: frisbee. Erzeugt tools/kategorien/modelle/frisbee.json.

Wurfscheibe (Ultimate-Größe, Ø 270 mm, 175 g), mit der Wölbung nach oben liegend. Ein Spritzgussteil,
hier in seine Zonen zerlegt: Aufdruck, flache Flugplatte, gewölbte Schulter und der nach unten gezogene Rand (Lippe).
Ringe sind gefüllte Ellipsen, die Hohlseite unten ist als dunklere Innenfläche markiert.
Explosion: Zonen nach oben abgehoben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

D = 270
FARBE = '#F0F0EA'
INNEN = '#C9CCC8'


def mitte(w):
    return (D - w) / 2


def ring(aussen, innen, fill=INNEN, zeichnung=False):
    o = (aussen - innen) / 2
    return mark('cyl', o, o, innen, fill=fill, zeichnung=zeichnung)


teile = [
    teil('aufdruck', 'pp_disc', 'Aufdruck', 'Aufdruck', 'cyl',
         x=mitte(170), y=mitte(170), w=170, z=30, h=0.05, mass=0.2, materials=[['druck', 100]], color='#3E6FA8',
         info='Farbe, direkt auf die Scheibe gedruckt. Sie lässt sich nicht abtrennen und stört beim Wiederverwenden nicht.',
         marks=[mark('cyl', 25, 25, 120, fill='#F2E6C8'), mark('box', 45, 75, 80, 20, 4, '#C8423A')]),
    teil('flugplatte', 'pp_disc', 'Flugplatte', 'Flugplatte', 'cyl',
         x=mitte(250), y=mitte(250), w=250, z=27, h=3, mass=70, color=FARBE,
         info='Die flache Oberseite. Ihre Fläche erzeugt beim Fliegen Auftrieb wie ein Flügel; '
              'die feinen Rillen (Flugringe) beruhigen die Luftströmung.',
         marks=[ring(250, 230, '#E2E3DE'), ring(250, 220, FARBE), ring(250, 206, '#E2E3DE'), ring(250, 196, FARBE)]),
    teil('schulter_oben', 'pp_disc', 'Schulter oben', 'Schulter', 'cyl', label=False,
         x=mitte(262), y=mitte(262), w=262, z=25, h=2, mass=14, color=FARBE,
         info='Oberer, stärker gewölbter Teil der Schulter.', marks=[ring(262, 250, zeichnung=True)]),
    teil('schulter', 'pp_disc', 'Schulter', 'Schulter', 'cyl',
         x=0, y=0, w=D, z=22, h=3, mass=26, color=FARBE,
         info='Gewölbter Übergang zwischen Platte und Rand. Hier ist die Scheibe am stabilsten.',
         marks=[ring(D, 250, zeichnung=True)]),
    teil('rand', 'pp_disc', 'Rand (Lippe)', 'Rand', 'cyl',
         x=0, y=0, w=D, z=0, h=22, mass=65, color=FARBE,
         info='Der nach unten gezogene, verdickte Rand. Er gibt Gewicht nach außen, so stabilisiert die Drehung den Flug, '
              'und man kann gut greifen. Kaputte Scheiben in den Restmüll, sie sind keine Verpackung.',
         wand=6, boden=0, marks=[ring(D, 258, zeichnung=True), ring(D, 250, '#B5B8B4', zeichnung=True)]),
]

explodiere(teile, abstand=80, abstaende={'aufdruck': 40}, gruppen=[['flugplatte', 'schulter_oben', 'schulter']])
skaliere_masse(teile, oid='frisbee')
schreibe('frisbee', teile)
