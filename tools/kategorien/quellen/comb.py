"""3D-Modell: comb. Erzeugt tools/kategorien/modelle/comb.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Taschenkamm flach liegend (laut CSV 30 × 180 × 4 mm), Rücken links (x = 0), Zinken zeigen nach rechts (+x).
# Ein einziges Spritzgussteil: dicker Rücken, vorne grobe, hinten feine Zinken. Die Zinken sind als marks gezeichnet
# (Lücken dunkel). Explodiert: die beiden Zinkenbereiche zur Seite, damit man Rücken und Zinkenformen sieht.
ABS = '#4A3B33'
LUECKE = '#2A211C'

teile = [
    teil('ruecken', 'plastic_comb', 'Kammrücken', 'Rücken', 'box',
         x=0, y=0, w=9, d=180, z=0, h=4, r=3, explode=[0, 0, 0], mass=4,
         info='Der dicke Rücken macht den Kamm stabil. Ein Kamm hält viele Jahre; abgebrochene Zinken '
              'machen ihn noch nicht unbrauchbar.',
         color=ABS, marks=[mark('box', 1.5, 6, 6, 168, 2, '#5C4A40')]),
    teil('zinken_grob', 'plastic_comb', 'Grobe Zinken', 'Grobe Zinken', 'box',
         x=9, y=2, w=21, d=88, z=0, h=3.5, r=1, explode=[14, -8, 0], mass=3.2,
         info='Weit auseinanderstehende Zinken zum Entwirren. Der Kamm ist aus einem Kunststoff gespritzt '
              'und lässt sich nicht weiter zerlegen.',
         color=ABS, marks=raster(3, 1.5, 1, 22, 18, 1.8, 0, 3.9, r=0.5, fill=LUECKE)),
    teil('zinken_fein', 'plastic_comb', 'Feine Zinken', 'Feine Zinken', 'box',
         x=9, y=90, w=21, d=88, z=0, h=3.5, r=1, explode=[14, 8, 0], mass=2.8,
         info='Eng stehende Zinken zum Glätten und Scheiteln. Zwischen ihnen sammeln sich Haare und Talg, '
              'deshalb den Kamm ab und zu mit Seifenwasser reinigen.',
         color=ABS, marks=raster(3, 1, 1, 44, 18, 0.9, 0, 1.98, fill=LUECKE)),
]

skaliere_masse(teile, oid='comb')
schreibe('comb', teile)
