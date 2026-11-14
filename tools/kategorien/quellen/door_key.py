"""3D-Modell: door_key. Erzeugt tools/kategorien/modelle/door_key.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

# Zylinderschlüssel flach liegend (laut CSV 23 × 55 × 3 mm), Reide (Griff) hinten (y = 0), Spitze vorne.
# Ein Stück vernickeltes Messing; zur Erklärung in Reide, Anschlag, Halm mit Profilrillen und Bart geteilt.
# Der Bart besteht aus fünf Zähnen unterschiedlicher Tiefe (das ist die Schließung). Ringloch in Tischfarbe.
# Explodiert: die Bereiche in der Ebene auseinandergezogen, Bart nach rechts.
MESSING = [['messing', 97], ['nickel', 3]]
NICKEL = '#C9CDD0'
RILLE = '#A9AFB4'
LOCH = '#EEECE5'
ZAEHNE = [4.0, 2.0, 3.5, 1.5, 3.0]  # Zahntiefe in mm, von der Reide zur Spitze
ZAHN_D = 5.0

teile = [
    teil('reide', 'brass_key', 'Reide (Griff)', 'Reide', 'cyl',
         x=0, y=0, w=23, d=21, z=0, h=3, explode=[0, -10, 0], mass=3.6, materials=MESSING,
         info='Der Griff mit Loch für den Schlüsselring. Hier ist oft die Schlüsselnummer eingeprägt, '
              'mit der man einen Nachschlüssel bestellen kann.',
         color=NICKEL, marks=[mark('cyl', 6.5, 1, 10, fill='#B8BDC1'), mark('cyl', 8, 2.5, 7, fill=LOCH),
                              mark('box', 5, 13, 13, 1.2, 0.5, RILLE), mark('box', 7, 16, 9, 1.2, 0.5, RILLE)]),
    teil('anschlag', 'brass_key', 'Anschlag', 'Anschlag', 'box',
         x=4, y=21, w=15, d=4, z=0, h=2.6, r=1, explode=[0, -4, 0], mass=0.8, materials=MESSING,
         info='Die Schulter stößt vorne am Zylinder an, so steckt der Schlüssel immer gleich tief.',
         color=NICKEL),
    teil('halm', 'brass_key', 'Halm mit Profil', 'Halm', 'box',
         x=5, y=25, w=9, d=30, z=0, h=2.4, r=1.5, explode=[0, 0, 0], mass=1.8, materials=MESSING,
         info='Die Längsrillen passen nur in das Profil des eigenen Schließzylinders. So passt der Schlüssel '
              'nicht in fremde Schlösser.',
         color=NICKEL, marks=[mark('box', 1.5, 0, 1.2, 28, 0.5, RILLE), mark('box', 4, 0, 1.2, 26, 0.5, RILLE),
                              mark('box', 6.5, 0, 1, 24, 0.5, RILLE)]),
    *[teil('bart' if i == 0 else f'bart_{i + 1}', 'brass_key', 'Bart mit Einschnitten', 'Bart', 'box',
           x=14, y=26 + i * ZAHN_D, w=t, d=ZAHN_D, z=0, h=2.4, r=0.3, explode=[9, 0, 0], mass=0.2 * t,
           materials=MESSING, label=i == 0,
           info=('Die unterschiedlich tiefen Zähne heben die Stifte im Schloss genau auf die Trennlinie. '
                 'Alte Schlüssel sind wertvolles Messing für die Metallsammlung.') if i == 0
           else 'Ein Zahn des Barts. Seine Tiefe gehört zur Schließung.',
           color=NICKEL) for i, t in enumerate(ZAEHNE)],
]

skaliere_masse(teile, oid='door_key', stellen=2)
schreibe('door_key', teile)
