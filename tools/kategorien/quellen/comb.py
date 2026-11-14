"""3D-Modell: comb. Erzeugt tools/kategorien/modelle/comb.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

# Taschenkamm flach liegend (laut CSV 30 × 180 × 4 mm), Rücken links (x = 0), Zinken zeigen nach rechts (+x).
# Ein einziges Spritzgussteil: dicker Rücken, hinten (y klein) grobe, vorne feine Zinken, jede Zinke ein eigener
# schmaler Quader mit echten Lücken. Explodiert: die beiden Zinkenreihen als Gruppen zur Seite.
ABS = '#4A3B33'

GROB = [teil(f'grob_{k}', 'plastic_comb', 'Grobe Zinken', 'Grobe Zinken', 'box',
             x=9, y=2 + k * 4.4, w=20, d=2.2, z=0.3, h=3.2, r=0.8, explode=[14, -8, 0], mass=0.16,
             color=ABS, label=(k == 0),
             info='Weit auseinanderstehende Zinken zum Entwirren. Der Kamm ist aus einem Kunststoff gespritzt '
                  'und lässt sich nicht weiter zerlegen.' if k == 0 else 'Eine der groben Zinken.')
        for k in range(20)]
FEIN = [teil(f'fein_{k}', 'plastic_comb', 'Feine Zinken', 'Feine Zinken', 'box',
             x=9, y=92 + k * 2.4, w=18, d=1.2, z=0.3, h=3.2, r=0.4, explode=[14, 8, 0], mass=0.08,
             color=ABS, label=(k == 0),
             info='Eng stehende Zinken zum Glätten und Scheiteln. Zwischen ihnen sammeln sich Haare und Talg, '
                  'deshalb den Kamm ab und zu mit Seifenwasser reinigen.' if k == 0 else 'Eine der feinen Zinken.')
        for k in range(36)]

teile = [
    teil('ruecken', 'plastic_comb', 'Kammrücken', 'Rücken', 'box',
         x=0, y=0, w=9, d=180, z=0, h=4, r=3, explode=[0, 0, 0], mass=4,
         info='Der dicke Rücken macht den Kamm stabil. Ein Kamm hält viele Jahre; abgebrochene Zinken '
              'machen ihn noch nicht unbrauchbar.',
         color=ABS, marks=[mark('box', 1.5, 6, 6, 168, 2, '#5C4A40')]),
    *GROB,
    *FEIN,
]

skaliere_masse(teile, oid='comb', stellen=2)
schreibe('comb', teile)
