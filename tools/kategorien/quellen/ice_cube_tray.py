"""3D-Modell: ice_cube_tray. Erzeugt tools/kategorien/modelle/ice_cube_tray.json.

Typische Silikon-Eiswürfelform für 14 Würfel (2 × 7, 110 × 250 × 30 mm) mit aufgestecktem PP-Deckel.
Die Form ist ein Stück; die Mulden sind als Marks gezeichnet (dunkle Innenwand, Boden um die Tiefe versetzt).\nExplodiert wird der Deckel nach links oben abgehoben, damit man in die Mulden sieht.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

SILIKON = '#4FB3BF'
WAND = '#2F7F89'     # Innenwand der Mulde (im Schatten)
GRUND = '#3E9EAA'    # Muldenboden, um die Tiefe nach vorn versetzt sichtbar
T = 12               # sichtbarer Versatz des Muldenbodens (Iso: Tiefe = Versatz in x und y)

mulden = []
for j in range(7):
    for i in range(2):
        x0, y0 = 8 + i * 50, 9 + j * 33.5
        mulden += [mark('box', x0, y0, 44, 30, 5, WAND), mark('box', x0 + T * 0.7, y0 + T * 0.7, 44 - T * 0.7, 30 - T * 0.7, 4, GRUND)]

teile = [
    teil('deckel', 'silicone_tray', 'Deckel', 'Deckel', 'box',
         material_id='pp', x=0, y=0, w=110, d=250, z=26, h=4, r=10, mass=22, materials=[['pp', 100]],
         explode=[-125, 0, 30],
         info='Durchsichtiger PP-Deckel, schützt das Eis vor Gerüchen aus dem Gefrierfach. Kunststoff, aber '
              'keine Verpackung: kaputt in den Restmüll.',
         color='#E4F1F3', opacity=0.4,
         marks=[mark('box', 40, 2, 30, 6, 2, '#C3DADE'),
                mark('box', 40, 242, 30, 6, 2, '#C3DADE')]),
    teil('form', 'silicone_tray', 'Silikonform für 14 Würfel', 'Silikonform', 'box',
         x=0, y=0, w=110, d=250, z=0, h=26, r=10, mass=60, explode=[0, 0, 0],
         info='Aus einem Stück Silikon gegossen, mit steifem Rand zum Festhalten. Das Eis löst sich durch Biegen. '
              'Silikon gehört nicht in die Gelbe Tonne, sondern in den Restmüll. Lange haltbar: lieber weiterverwenden.',
         color=SILIKON, marks=mulden),
]
skaliere_masse(teile, oid='ice_cube_tray')
schreibe('ice_cube_tray', teile)
