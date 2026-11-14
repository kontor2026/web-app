"""3D-Modell: ceramic_mug. Erzeugt tools/kategorien/modelle/ceramic_mug.json.

Typischer Kaffeebecher aus Steingut (ca. 300 ml, Ø 78 mm) mit angarniertem Henkel und unglasiertem Standring.
Der Becher ist ein Stück: Die Abschnitte bewegen sich gemeinsam, die Glasur schwebt als Schicht darüber, der
Henkel wird seitlich herausgezogen, um zu zeigen, wo er angesetzt wurde.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

FARBE = '#3F7FA6'
INNEN = '#F1EEE6'
SCHERBEN = '#D8CBB4'

teile = [
    teil('glasur', 'ceramic_body', 'Glasur', 'Glasur', 'cyl',
         x=4, y=4, w=70, z=8, h=0.4, mass=18, materials=[['glas', 70], ['keramik', 30]],
         info='Glasartige Schicht, die beim zweiten Brand auf den Ton schmilzt. Sie macht den Becher wasserdicht und '
              'lässt sich nicht abtrennen.',
         color=INNEN, opacity=0.8, marks=[mark('cyl', 15, 15, 40, fill='#E6E1D6')]),
    teil('rand', 'ceramic_body', 'Trinkrand', 'Rand', 'cyl',
         x=0, y=0, w=78, z=85, h=10, mass=35,
         info='Abgerundete Lippe, rundum glasiert. Hier platzen oft kleine Stücke ab: dann lieber nicht mehr daraus '
              'trinken.',
         color=FARBE, wand=4, boden=0, marks=[mark('cyl', 4, 4, 70, fill=INNEN, zeichnung=True)]),
    teil('wand', 'ceramic_body', 'Becherwand', 'Wand', 'cyl',
         x=0, y=0, w=78, z=6, h=79, mass=200,
         info='Gebrannter Ton (Steingut), etwa 5 mm dick. Keramik gehört nicht ins Altglas, weil sie dort die neue '
              'Glasschmelze verdirbt. Ganze Becher spenden, Scherben in den Restmüll.',
         color=FARBE, wand=5, boden=0),
    teil('standring', 'ceramic_body', 'Standring (unglasiert)', 'Standring', 'cyl',
         x=4, y=4, w=70, z=0, h=6, mass=45,
         info='Unten bleibt ein Ring ohne Glasur, damit der Becher beim Brennen nicht am Ofen festklebt. Man sieht '
              'dort die helle Farbe des Tons.',
         color=SCHERBEN, marks=[mark('cyl', 6, 6, 58, fill='#CBBDA4')]),
    teil('henkel_oben', 'ceramic_body', 'Henkel', 'Henkel', 'box',
         x=76, y=33, w=19, d=12, z=68, h=10, r=4, explode=[35, 0, 0], mass=10, sortBias=40,
         info='Separat geformt und vor dem Brennen mit flüssigem Ton (Schlicker) angesetzt. Nach dem Brand ist er fest '
              'mit dem Becher verbunden.',
         color=FARBE, marks=[mark('box', 2, 2, 15, 8, 3, fill='#4A8DB5')]),
    teil('henkel_griff', 'ceramic_body', 'Henkel (Griffbogen)', 'Henkel', 'box',
         x=86, y=33, w=9.5, d=12, z=26, h=42, r=4, explode=[35, 0, 0], mass=14, sortBias=40, label=False,
         info='Der senkrechte Bogen, an dem man den Becher hält.', color=FARBE),
    teil('henkel_unten', 'ceramic_body', 'Henkel (unterer Ansatz)', 'Henkel', 'box',
         x=76, y=33, w=10, d=12, z=26, h=10, r=4, explode=[35, 0, 0], mass=8, sortBias=40, label=False,
         info='Unterer Ansatzpunkt des Henkels. Hier bricht ein Henkel am häufigsten ab.', color=FARBE),
]
explodiere(teile, abstand=18, nach_liste=True, gruppen=[['rand', 'wand', 'standring']])
skaliere_masse(teile, oid='ceramic_mug')
schreibe('ceramic_mug', teile)
