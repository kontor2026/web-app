"""3D-Modell: coffee_capsule. Erzeugt tools/kategorien/modelle/coffee_capsule.json.

Typische Aluminium-Kaffeekapsel (Kegelstumpf mit Kuppe, Kragen 37 mm, Höhe 28 mm). Steht auf der Kuppe, die
Deckelfolie zeigt nach oben. Kapselkörper und Kragen sind ein Stück (Gruppe), die Folie schwebt darüber,
der Farblack wird seitlich herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

FARBE = '#7A4B8C'
teile = [
    teil('folie', 'aluminium_lid_foil', 'Deckelfolie', 'Deckelfolie', 'cyl',
         x=0, y=0, w=37, z=27.8, h=0.2, mass=0.15,
         info='Dünne Aluminiumfolie, auf den Kragen gesiegelt. In der Maschine wird sie durchstochen. '
              'Ganz abziehen und mit der Kapsel in die Gelbe Tonne geben.',
         color='#D3D7DA', marks=[mark('cyl', 4, 4, 29), mark('cyl', 15.5, 15.5, 6, fill='#B9BFC4')]),
    teil('kragen', 'aluminium_capsule', 'Kragen (Bördelrand)', 'Kragen', 'cyl',
         x=0, y=0, w=37, z=26.8, h=1, mass=0.25,
         info='Umgebogener Rand, auf dem die Folie klebt. Die Maschine klemmt die Kapsel hier dicht ein.',
         color=FARBE, marks=[mark('cyl', 3.5, 3.5, 30, fill='#5C3A2A')]),
    teil('koerper_oben', 'aluminium_capsule', 'Kapselkörper', 'Kapsel', 'cyl',
         x=3.5, y=3.5, w=30, z=14, h=12.8, mass=1.0,
         info='Aus einer Aluminiumscheibe tiefgezogen. Darin stecken etwa 5 g Kaffeepulver: '
              'den Kaffeesatz in den Bio-Müll leeren, dann wird das Aluminium recycelt.',
         color=FARBE),
    teil('koerper_unten', 'aluminium_capsule', 'Kapselkörper (unten)', 'Kapsel unten', 'cyl',
         x=6, y=6, w=25, z=5, h=9, mass=0.6,
         info='Verjüngt sich nach unten, damit die Kapsel in die Brühkammer passt.', color=FARBE, label=False),
    teil('kuppe', 'aluminium_capsule', 'Kuppe mit Einstichstelle', 'Kuppe', 'cyl',
         x=11, y=11, w=15, z=0, h=5, mass=0.25,
         info='Hier sticht die Maschine Löcher hinein, durch die heißes Wasser mit Druck einströmt.',
         color=FARBE),
    teil('lack', 'aluminium_capsule', 'Farblack', 'Farblack', 'box',
         x=33.5, y=8.5, w=0.3, d=20, z=6, h=19, r=0, explode=[30, 0, 0], mass=0.05,
         materials=[['druck', 100]],
         info='Die Farbe zeigt die Kaffeesorte. Der Lack verbrennt beim Einschmelzen, das Aluminium bleibt übrig.',
         color=FARBE, sortBias=100),
]
explodiere(teile, abstand=10, gruppen=[['kragen', 'koerper_oben', 'koerper_unten', 'kuppe']])
skaliere_masse(teile, oid='coffee_capsule', stellen=2)
schreibe('coffee_capsule', teile)
