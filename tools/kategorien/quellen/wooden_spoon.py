"""3D-Modell: wooden_spoon. Erzeugt tools/kategorien/modelle/wooden_spoon.json.

Typischer Kochlöffel aus Buchenholz (30 cm) flach auf dem Tisch, Laffe hinten (y = 0), Stielende vorne.
Der Löffel ist aus einem Stück gedrechselt; explodiert rücken Laffe, Hals und Stiel etwas auseinander.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

HOLZ = '#D9B48A'

teile = [
    teil('laffe', 'wooden_spoon_body', 'Laffe', 'Laffe', 'cyl',
         x=0, y=0, w=60, d=82, z=0, h=15, explode=[0, -16, 0], mass=14,
         info='Die flache Mulde zum Rühren und Abschmecken. Dunkle, rissige Stellen sind verbranntes Holz: Dann ist '
              'es Zeit für einen neuen Löffel.',
         color=HOLZ, marks=[mark('cyl', 6, 7, 48, 66, fill='#CFA97E'), mark('cyl', 14, 16, 32, 46, fill='#C69F73')]),
    teil('hals', 'wooden_spoon_body', 'Hals', 'Hals', 'box',
         x=21, y=78, w=18, d=32, z=2, h=11, r=6, explode=[0, 0, 0], mass=4,
         info='Übergang von der Laffe zum Stiel, hier ist der Löffel am stärksten belastet.',
         color='#D3AE84'),
    teil('stiel', 'wooden_spoon_body', 'Stiel', 'Stiel', 'box',
         x=23, y=110, w=14, d=190, z=3, h=10, r=6, explode=[0, 16, 0], mass=22,
         info='Unbehandeltes oder nur mit Speiseöl eingeriebenes Buchenholz. Es darf in die Biotonne oder in den '
              'Restmüll; lackierte Löffel nur in den Restmüll.',
         color=HOLZ, marks=[mark('cyl', 3.5, 172, 7, fill='#8E6B47'), mark('box', 5, 10, 4, 150, 2, '#CFA97E')]),
]
skaliere_masse(teile, oid='wooden_spoon')
schreibe('wooden_spoon', teile)
