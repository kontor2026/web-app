"""3D-Modell: door_key. Erzeugt tools/kategorien/modelle/door_key.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Zylinderschlüssel flach liegend (laut CSV 23 × 55 × 3 mm), Reide (Griff) hinten (y = 0), Spitze vorne.
# Ein Stück vernickeltes Messing; zur Erklärung in Reide, Anschlag, Halm mit Profilrillen und Bart mit Einschnitten
# geteilt. Explodiert: die Bereiche in der Ebene auseinandergezogen.
MESSING = [['messing', 97], ['nickel', 3]]
NICKEL = '#C9CDD0'

teile = [
    teil('reide', 'brass_key', 'Reide (Griff)', 'Reide', 'cyl',
         x=0, y=0, w=23, d=22, z=0, h=3, explode=[0, -10, 0], mass=3.6, materials=MESSING,
         info='Der Griff mit Loch für den Schlüsselring. Hier ist oft die Schlüsselnummer eingeprägt, '
              'mit der man einen Nachschlüssel bestellen kann.',
         color=NICKEL, marks=[mark('cyl', 8.5, 3, 6, fill='#4A4F54'), mark('box', 5, 12, 13, 3, 1, '#A9AFB4')]),
    teil('anschlag', 'brass_key', 'Anschlag', 'Anschlag', 'box',
         x=4, y=22, w=15, d=4, z=0, h=2.6, r=1, explode=[0, -4, 0], mass=0.8, materials=MESSING,
         info='Die Schulter stößt vorne am Zylinder an, so steckt der Schlüssel immer gleich tief.',
         color=NICKEL),
    teil('halm', 'brass_key', 'Halm mit Profil', 'Halm', 'box',
         x=6, y=26, w=7, d=29, z=0, h=2.4, r=1, explode=[0, 0, 0], mass=1.8, materials=MESSING,
         info='Die Längsrillen passen nur in das Profil des eigenen Schließzylinders.',
         color=NICKEL, marks=[mark('box', 1.5, 0, 1.2, 27, 0.5, '#A9AFB4'), mark('box', 4, 0, 1.2, 25, 0.5, '#A9AFB4')]),
    teil('bart', 'brass_key', 'Bart mit Einschnitten', 'Bart', 'box',
         x=13, y=26, w=4, d=27, z=0, h=2.4, r=1, explode=[8, 0, 0], mass=1.0, materials=MESSING,
         info='Die unterschiedlich tiefen Einschnitte heben die Stifte im Schloss genau auf die Trennlinie. '
              'Alte Schlüssel sind wertvolles Messing für die Metallsammlung.',
         color=NICKEL, marks=[mark('box', 2.2, 2, 1.8, 3, 0.5, '#4A4F54'), mark('box', 1, 7, 3, 3, 0.5, '#4A4F54'),
                              mark('box', 2.8, 12, 1.2, 3, 0.5, '#4A4F54'), mark('box', 1.6, 17, 2.4, 3, 0.5, '#4A4F54'),
                              mark('box', 2, 22, 2, 4, 0.5, '#4A4F54')]),
]

skaliere_masse(teile, oid='door_key', stellen=2)
schreibe('door_key', teile)
