"""3D-Modell: ice_cube_tray. Erzeugt tools/kategorien/modelle/ice_cube_tray.json.

Typische Silikon-Eiswürfelform für 14 Würfel (2 × 7, 110 × 250 × 30 mm) mit aufgestecktem PP-Deckel.
Die Form ist ein Stück (Rand, Mulden, Boden bewegen sich gemeinsam), der Deckel schwebt darüber.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

SILIKON = '#4FB3BF'
teile = [
    teil('deckel', 'silicone_tray', 'Deckel', 'Deckel', 'box',
         material_id='pp', x=0, y=0, w=110, d=250, z=26, h=4, r=10, mass=22, materials=[['pp', 100]],
         info='Durchsichtiger PP-Deckel, schützt das Eis vor Gerüchen aus dem Gefrierfach. Kunststoff, aber '
              'keine Verpackung: kaputt in den Restmüll.',
         color='#E4F1F3', opacity=0.7, marks=[mark('box', 4, 4, 102, 242, 8, '#D3E6E9')]),
    teil('rand', 'silicone_tray', 'Rand', 'Rand', 'box',
         x=0, y=0, w=110, d=250, z=22, h=4, r=10, mass=14,
         info='Steifer Rand zum Festhalten. Die Form ist aus einem Stück Silikon gegossen.',
         color=SILIKON, marks=raster(8, 8, 2, 7, 44, 30, 50, 33, r=6, fill='#2F7F89')),
    teil('mulden', 'silicone_tray', 'Mulden für 14 Würfel', 'Mulden', 'box',
         x=4, y=4, w=102, d=242, z=3, h=19, r=8, mass=40,
         info='Weiches Silikon, das Eis löst sich durch Biegen. Silikon gehört nicht in die Gelbe Tonne, '
              'sondern in den Restmüll. Lange haltbar: lieber weiterverwenden.',
         color=SILIKON, marks=raster(4, 4, 2, 7, 44, 30, 50, 33, r=6, fill='#3C9AA5')),
    teil('boden', 'silicone_tray', 'Boden mit Noppen', 'Boden', 'box',
         x=8, y=8, w=94, d=234, z=0, h=3, r=6, mass=6, label=False,
         info='Unterseite der Mulden, kleine Noppen verhindern das Rutschen.', color=SILIKON),
]
explodiere(teile, abstand=50, nach_liste=True, gruppen=[['rand', 'mulden', 'boden']])
skaliere_masse(teile, oid='ice_cube_tray')
schreibe('ice_cube_tray', teile)
