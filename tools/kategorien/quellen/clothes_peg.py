"""3D-Modell: clothes_peg. Erzeugt tools/kategorien/modelle/clothes_peg.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Kunststoff-Wäscheklammer auf der Seite liegend (laut CSV 10 × 75 × 15 mm): die beiden Hälften liegen übereinander,
# Klemmbacken hinten (y = 0), Griffenden vorne. Die Stahlfeder sitzt mit ihrer Windung in einer Kerbe bei y ≈ 38,
# ihre Schenkel liegen in Rillen auf den Außenseiten der Griffenden. Explodiert: Ebenen nach oben.
PP = '#E86A92'
STAHL = '#B8BEC4'

teile = [
    teil('schenkel_oben', 'steel_spring', 'Federschenkel oben', 'Schenkel', 'box',
         x=4.4, y=42, w=1.2, d=28, z=14, h=1.2, r=0.6, mass=0.15,
         info='Gerader Drahtschenkel, der auf das obere Griffende drückt.', color=STAHL),
    teil('haelfte_oben', 'peg_halves', 'Obere Klammerhälfte', 'Hälfte oben', 'box',
         x=0.5, y=0, w=9, d=75, z=7.5, h=6.5, r=2, mass=2.5,
         info='Polypropylen, wird mit der Zeit in der Sonne spröde und bricht. Zum Trennen die Hälften '
              'gegeneinander verdrehen, dann springt die Feder heraus.',
         color=PP, marks=[mark('box', 1, 3, 7, 18, 1, '#D45780'), mark('box', 3.9, 42, 2.2, 30, 1, '#C04A72')]
         + raster(1.5, 50, 1, 4, 6, 1, 0, 4, fill='#D45780')),
    teil('feder', 'steel_spring', 'Federwindung', 'Feder', 'box',
         x=0, y=34, w=10, d=8, z=4.5, h=6, r=3, mass=0.5,
         info='Gewickelte Torsionsfeder aus verzinktem Stahldraht. Mit einer Zange herausziehen; '
              'sie gehört zum Altmetall oder taugt als Ersatzfeder.',
         color=STAHL, marks=raster(0.5, 0.5, 6, 1, 1, 7, 1.6, r=0.5, fill='#7E868C')),
    teil('haelfte_unten', 'peg_halves', 'Untere Klammerhälfte', 'Hälfte unten', 'box',
         x=0.5, y=0, w=9, d=75, z=1, h=6.5, r=2, mass=2.5, label=False,
         info='Gegenstück zur oberen Hälfte, baugleich. Die Riffelung an den Backen hält die Wäsche fest.',
         color=PP, marks=[mark('box', 1, 3, 7, 18, 1, '#D45780'), mark('box', 3.9, 42, 2.2, 30, 1, '#C04A72')]),
    teil('schenkel_unten', 'steel_spring', 'Federschenkel unten', 'Schenkel', 'box',
         x=4.4, y=42, w=1.2, d=28, z=0, h=1, r=0.6, mass=0.15, label=False,
         info='Zweiter Schenkel der Feder unter dem unteren Griffende.', color=STAHL),
]

explodiere(teile, abstand=6, nach_liste=True)
skaliere_masse(teile, oid='clothes_peg', stellen=2)
schreibe('clothes_peg', teile)
