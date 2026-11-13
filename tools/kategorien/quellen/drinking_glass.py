"""3D-Modell: drinking_glass. Erzeugt tools/kategorien/modelle/drinking_glass.json.

Typisches Wasserglas (Becherglas, ca. 250 ml) aus Kalk-Natron-Glas, nach oben leicht konisch, mit dickem Boden.
Das Glas ist ein Stück; die Abschnitte schweben mit kleinem Abstand übereinander, damit man Rand, Wand und den
dicken Boden einzeln anklicken kann.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

GLAS = '#DCE8E4'
OP = 0.65

teile = [
    teil('rand', 'drinking_glass_body', 'Trinkrand', 'Rand', 'cyl',
         x=0, y=0, w=75, z=98, h=12, mass=22,
         info='Feuerpolierter Rand, nur etwa 1,5 mm dick. Angeschlagene Gläser nicht mehr benutzen: Die Kante ist '
              'scharf.',
         color=GLAS, opacity=OP, marks=[mark('cyl', 2, 2, 71, fill='#EEF4F2')]),
    teil('wand_oben', 'drinking_glass_body', 'Glaswand oben', 'Wand', 'cyl',
         x=1.5, y=1.5, w=72, z=55, h=43, mass=60,
         info='Gepresstes oder geblasenes Trinkglas. Es hat eine andere Zusammensetzung und einen höheren '
              'Schmelzpunkt als Flaschenglas.',
         color=GLAS, opacity=OP),
    teil('wand_unten', 'drinking_glass_body', 'Glaswand unten', 'Wand unten', 'cyl',
         x=3.5, y=3.5, w=68, z=14, h=41, mass=60, label=False,
         info='Unterer, schmalerer Teil der leicht konischen Wand.', color=GLAS, opacity=OP),
    teil('boden', 'drinking_glass_body', 'Dicker Glasboden', 'Boden', 'cyl',
         x=5.5, y=5.5, w=64, z=0, h=14, mass=110,
         info='Massiver Boden, damit das Glas nicht umkippt. Kaputte Trinkgläser kommen in Zeitungspapier gewickelt in '
              'den Restmüll, nicht in den Altglascontainer.',
         color=GLAS, opacity=0.75, marks=[mark('cyl', 4, 4, 56, fill='#CFDDD8')]),
]
explodiere(teile, abstand=12, nach_liste=True)
skaliere_masse(teile, oid='drinking_glass')
schreibe('drinking_glass', teile)
