"""3D-Modell: towel. Erzeugt tools/kategorien/modelle/towel.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Frottee-Handtuch (50 × 100 cm) gefaltet zu 300 × 250 × 40 mm, Aufhänger hinten (y = 0).
# Explodiert schieben sich die vier Faltlagen treppenartig nach hinten oben, der Aufhänger schwebt über der
# obersten Lage, das Etikett wird nach rechts gezogen.
FROTTEE = '#A8433B'
BORTE = '#8C3129'
BW = [['baumwolle', 100]]
SCHLINGEN = [dict(m, zeichnung=True) for m in raster(15, 15, 14, 11, 4, 4, 20, 20, shape='cyl', fill='#B34C42')]  # Foto: Stoffstruktur
KANTEN = [mark('box', 0, 0, 5, 250, 0, BORTE, zeichnung=True), mark('box', 295, 0, 5, 250, 0, BORTE, zeichnung=True)]  # umgenähte Webkanten

teile = [
    teil('aufhaenger', 'cotton_fabric', 'Aufhänger', 'Aufhänger', 'box',
         x=140, y=0, w=12, d=45, z=40, h=2, r=2, mass=3, materials=BW, color=BORTE, explode=[0, -260, 175],
         info='Gewebtes Baumwollband als Schlaufe in den Saum genäht, zum Aufhängen am Haken.'),
    teil('etikett', 'care_label', 'Pflegeetikett', 'Etikett', 'box',
         x=160, y=4, w=25, d=32, z=40, h=0.3, r=1, mass=1, explode=[260, 0, 0], color='#F4F2EE',
         info='Polyester-Etikett mit Waschsymbolen (bis 60 °C). Vor dem Recycling abschneiden.',
         marks=[mark('box', 4, 5, 17, 3, 0, '#8E969A'), mark('box', 4, 12, 17, 3, 0, '#8E969A'),
                mark('box', 4, 19, 11, 3, 0, '#8E969A')]),
    teil('lage_1', 'cotton_fabric', 'Oberste Faltlage mit Bordüre', 'Oberste Lage', 'box',
         x=0, y=0, w=300, d=250, z=30, h=10, r=8, mass=110, materials=BW, color=FROTTEE,
         info='Frottee: Auf einem Grundgewebe stehen tausende kleine Baumwollschlingen, die viel Wasser aufsaugen.',
         explode=[0, -210, 165], marks=SCHLINGEN + KANTEN + [mark('box', 6, 200, 288, 22, 0, BORTE), mark('box', 6, 206, 288, 2, 0, '#E0B04A'), mark('box', 6, 214, 288, 2, 0, '#E0B04A')]),
    teil('lage_2', 'cotton_fabric', 'Faltlage 2', 'Faltlage', 'box',
         x=0, y=0, w=300, d=250, z=20, h=10, r=8, mass=110, materials=BW, color=FROTTEE,
         info='Gut erhaltene Handtücher in die Altkleidersammlung, alte als Putzlappen oder für das Tierheim.',
         explode=[0, -140, 110], marks=SCHLINGEN + KANTEN),
    teil('lage_3', 'cotton_fabric', 'Faltlage 3', 'Faltlage', 'box',
         x=0, y=0, w=300, d=250, z=10, h=10, r=8, mass=110, materials=BW, color=FROTTEE, label=False,
         info='Reine Baumwolle: ohne Etikett und Aufhänger lässt sich das Tuch komplett zu Fasern reißen.',
         explode=[0, -70, 55], marks=SCHLINGEN + KANTEN),
    teil('lage_4', 'cotton_fabric', 'Unterste Faltlage mit Bordüre', 'Unterste Lage', 'box',
         x=0, y=0, w=300, d=250, z=0, h=10, r=8, mass=110, materials=BW, color=FROTTEE,
         info='Die glatt gewebte Bordüre und die umgenähten Kanten verhindern, dass sich Schlingen herausziehen.',
         explode=[0, 0, 0], marks=SCHLINGEN + KANTEN + [mark('box', 6, 28, 288, 22, 0, BORTE), mark('box', 6, 34, 288, 2, 0, '#E0B04A'), mark('box', 6, 42, 288, 2, 0, '#E0B04A')]),
]

skaliere_masse(teile, oid='towel')
schreibe('towel', teile)
