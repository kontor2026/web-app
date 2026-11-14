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

RAND = 8             # breiter Rand rundum
MW, MD = 47, 234 / 7  # Mulden füllen die Fläche innerhalb des Rands
mulden = []
for j in range(7):
    for i in range(2):
        n = len(mulden)
        mulden.append(teil(
            f'mulde_{n + 1}', 'silicone_tray', 'Mulden (14 Stück)' if n == 0 else f'Mulde {n + 1}', 'Mulden', 'box',
            x=RAND + i * MW, y=round(RAND + j * MD, 2), w=MW, d=round(MD, 2), z=0, h=26, r=5, mass=48 / 14,
            explode=[0, 0, 0], wand=1.6, boden=1.6, label=None if n == 0 else False,
            info='Jede Mulde ist ein dünnwandiger Silikonbecher, der beim Biegen nachgibt und den Würfel freigibt.'
            if n == 0 else 'Weitere Mulde.',
            color=SILIKON,
            marks=[mark('box', 0.8, 0.8, MW - 1.6, round(MD - 1.6, 2), 5, WAND, zeichnung=True),
                   mark('box', 0.8 + T * 0.7, 0.8 + T * 0.7, round(MW - 1.6 - T * 0.7, 2), round(MD - 1.6 - T * 0.7, 2), 4,
                        GRUND, zeichnung=True)]))
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
         x=0, y=0, w=RAND, d=250, z=22, h=4, r=3, mass=4, explode=[0, 0, 0],
         info='Aus einem Stück Silikon gegossen, mit steifem Rand zum Festhalten. Das Eis löst sich durch Biegen. '
              'Silikon gehört nicht in die Gelbe Tonne, sondern in den Restmüll. Lange haltbar: lieber weiterverwenden.',
         color=SILIKON),
    teil('rand_rechts', 'silicone_tray', 'Rand', 'Rand', 'box',
         x=110 - RAND, y=0, w=RAND, d=250, z=22, h=4, r=3, mass=4, explode=[0, 0, 0], label=False,
         info='Steifer Rand der Silikonform.', color=SILIKON),
    teil('rand_hinten', 'silicone_tray', 'Rand', 'Rand', 'box',
         x=RAND, y=0, w=110 - 2 * RAND, d=RAND, z=22, h=4, r=1, mass=2, explode=[0, 0, 0], label=False,
         info='Steifer Rand der Silikonform.', color=SILIKON),
    teil('rand_vorne', 'silicone_tray', 'Rand', 'Rand', 'box',
         x=RAND, y=250 - RAND, w=110 - 2 * RAND, d=RAND, z=22, h=4, r=1, mass=2, explode=[0, 0, 0], label=False,
         info='Steifer Rand der Silikonform.', color=SILIKON),
    *mulden,
]
skaliere_masse(teile, oid='ice_cube_tray')
schreibe('ice_cube_tray', teile)
