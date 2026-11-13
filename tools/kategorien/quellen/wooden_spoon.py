"""3D-Modell: wooden_spoon. Erzeugt tools/kategorien/modelle/wooden_spoon.json.

Typischer Kochlöffel aus Buchenholz (30 cm) flach auf dem Tisch, Laffe hinten (y = 0), Stielende vorne.
Der Löffel ist aus einem Stück gedrechselt und gefräst: flache Laffe, schmaler Hals, Stiel, der zum Griffende hin
etwas breiter wird, mit Aufhängeloch. Explodiert rücken die Abschnitte in Stielrichtung auseinander.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

HOLZ = '#DDB88D'
MASER = '#CBA478'


def maserung(w, d, n, x0=2.5):
    """Feine Holzmaserung längs des Stiels."""
    s = (w - 2 * x0) / max(n - 1, 1)
    return [mark('box', round(x0 + i * s - 0.4, 2), 4 + (i % 2) * 6, 0.8, d - 8 - (i % 2) * 12, 0.4, MASER)
            for i in range(n)]


teile = [
    teil('laffe', 'wooden_spoon_body', 'Laffe', 'Laffe', 'cyl',
         x=0, y=0, w=60, d=82, z=0, h=13, explode=[0, -24, 0], mass=13,
         info='Die flache Mulde zum Rühren und Abschmecken. Dunkle, rissige Stellen sind verbranntes Holz: Dann ist '
              'es Zeit für einen neuen Löffel.',
         color=HOLZ, marks=[mark('cyl', 4, 5, 52, 72, fill='#D2AC80'), mark('cyl', 9, 11, 42, 58, fill='#C8A174'),
                            mark('cyl', 16, 20, 28, 36, fill='#BF976A')]),
    teil('hals', 'wooden_spoon_body', 'Hals', 'Hals', 'box',
         x=23, y=76, w=14, d=44, z=1.5, h=10, r=5, explode=[0, -8, 0], mass=4,
         info='Schmaler Übergang von der Laffe zum Stiel. Hier ist der Löffel am stärksten belastet und bricht, '
              'wenn man ihn als Hebel benutzt.',
         color=HOLZ, marks=maserung(14, 44, 3)),
    teil('stiel', 'wooden_spoon_body', 'Stiel', 'Stiel', 'box',
         x=22, y=120, w=16, d=100, z=2, h=10, r=6, explode=[0, 8, 0], mass=10,
         info='Unbehandeltes oder nur mit Speiseöl eingeriebenes Buchenholz. Es leitet Wärme schlecht, deshalb wird '
              'der Stiel im heißen Topf nicht warm.',
         color=HOLZ, marks=maserung(16, 100, 4)),
    teil('griff', 'wooden_spoon_body', 'Griffende mit Loch', 'Griff', 'box',
         x=20.5, y=220, w=19, d=80, z=2, h=10, r=8, explode=[0, 24, 0], mass=9,
         info='Breiteres Griffende mit Loch zum Aufhängen. Holz darf in die Biotonne oder in den Restmüll; '
              'lackierte Löffel nur in den Restmüll.',
         color=HOLZ, marks=maserung(19, 56, 4) + [mark('cyl', 6, 62, 7, fill='#7E5C3A'),
                                                   mark('box', 4, 20, 11, 4, 1, '#B98F62')]),
]
skaliere_masse(teile, oid='wooden_spoon')
schreibe('wooden_spoon', teile)
