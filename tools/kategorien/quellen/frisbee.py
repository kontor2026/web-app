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


def ring(aussen, innen, fill=INNEN):
    o = (aussen - innen) / 2
    return mark('cyl', o, o, innen, fill=fill)


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
    teil('schulter', 'pp_disc', 'Schulter', 'Schulter', 'cyl',
         x=0, y=0, w=D, z=22, h=5, mass=40, color='#E6E7E2',
         info='Gewölbter Übergang zwischen Platte und Rand. Hier ist die Scheibe am stabilsten.',
         marks=[ring(D, 250)]),
    teil('rand', 'pp_disc', 'Rand (Lippe)', 'Rand', 'cyl',
         x=0, y=0, w=D, z=0, h=22, mass=65, color=FARBE,
         info='Der nach unten gezogene, verdickte Rand. Er gibt Gewicht nach außen, so stabilisiert die Drehung den Flug, '
              'und man kann gut greifen. Kaputte Scheiben in den Restmüll, sie sind keine Verpackung.',
         marks=[ring(D, 258), ring(D, 250, '#B5B8B4')]),
]

explodiere(teile, abstand=80, abstaende={'aufdruck': 40})
skaliere_masse(teile, oid='frisbee')
schreibe('frisbee', teile)
