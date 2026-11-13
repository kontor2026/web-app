"""3D-Modell: towel. Erzeugt tools/kategorien/modelle/towel.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Frottee-Handtuch (50 × 100 cm) gefaltet zu 300 × 250 × 40 mm, Aufhänger hinten (y = 0).
# Explodiert heben sich vier Faltlagen nach oben ab, Aufhänger und Etikett werden nach rechts gezogen.
FROTTEE = '#C2554A'
BORTE = '#A8443B'
BW = [['baumwolle', 100]]
SCHLINGEN = raster(15, 15, 14, 11, 4, 4, 20, 20, shape='cyl', fill='#B34C42')

teile = [
    teil('aufhaenger', 'cotton_fabric', 'Aufhänger', 'Aufhänger', 'box',
         x=140, y=0, w=12, d=45, z=40, h=2, r=2, mass=3, materials=BW, color=BORTE, explode=[230, 0, 0],
         info='Gewebtes Baumwollband als Schlaufe in den Saum genäht, zum Aufhängen am Haken.'),
    teil('etikett', 'care_label', 'Pflegeetikett', 'Etikett', 'box',
         x=160, y=4, w=25, d=32, z=40, h=0.3, r=1, mass=1, explode=[200, 60, 0], color='#F4F2EE',
         info='Polyester-Etikett mit Waschsymbolen (bis 60 °C). Vor dem Recycling abschneiden.',
         marks=[mark('box', 4, 5, 17, 3, 0, '#8E969A'), mark('box', 4, 12, 17, 3, 0, '#8E969A'),
                mark('box', 4, 19, 11, 3, 0, '#8E969A')]),
    teil('lage_1', 'cotton_fabric', 'Oberste Faltlage mit Bordüre', 'Faltlage oben', 'box',
         x=0, y=0, w=300, d=250, z=30, h=10, r=8, mass=110, materials=BW, color=FROTTEE,
         info='Frottee: Auf einem Grundgewebe stehen tausende kleine Baumwollschlingen, die viel Wasser aufsaugen.',
         marks=SCHLINGEN + [mark('box', 0, 200, 300, 22, 0, BORTE)]),
    teil('lage_2', 'cotton_fabric', 'Faltlage 2', 'Faltlage', 'box',
         x=0, y=0, w=300, d=250, z=20, h=10, r=8, mass=110, materials=BW, color=FROTTEE,
         info='Gut erhaltene Handtücher in die Altkleidersammlung, alte als Putzlappen oder für das Tierheim.',
         marks=SCHLINGEN),
    teil('lage_3', 'cotton_fabric', 'Faltlage 3', 'Faltlage', 'box',
         x=0, y=0, w=300, d=250, z=10, h=10, r=8, mass=110, materials=BW, color=FROTTEE, label=False,
         info='Reine Baumwolle: ohne Etikett und Aufhänger lässt sich das Tuch komplett zu Fasern reißen.',
         marks=SCHLINGEN),
    teil('lage_4', 'cotton_fabric', 'Unterste Faltlage mit Bordüre', 'Faltlage unten', 'box',
         x=0, y=0, w=300, d=250, z=0, h=10, r=8, mass=110, materials=BW, color=FROTTEE,
         info='Die glatt gewebte Bordüre und die umgenähten Kanten verhindern, dass sich Schlingen herausziehen.',
         marks=SCHLINGEN + [mark('box', 0, 28, 300, 22, 0, BORTE)]),
]

explodiere(teile, abstand=90)
skaliere_masse(teile, oid='towel')
schreibe('towel', teile)
