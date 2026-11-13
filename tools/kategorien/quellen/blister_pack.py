"""3D-Modell: blister_pack. Erzeugt tools/kategorien/modelle/blister_pack.json.

Typischer Tabletten-Blister 10 Stück (100 × 60 mm): PVC-Folie mit 2 × 5 tiefgezogenen Näpfen, unten die
aufgesiegelte, bedruckte Aluminium-Durchdrückfolie. Die PVC-Folie hebt nach oben ab.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

PVC = '#E4EBEF'
teile = [
    teil('naepfe', 'pvc_blister', 'Tablettennäpfe', 'Näpfe', 'box',
         x=4, y=6, w=92, d=48, z=0.4, h=6, r=4, mass=1.2, opacity=0.6,
         info='Tiefgezogene Mulden, je eine pro Tablette. Alle Tabletten herausdrücken; Reste von Medikamenten '
              'gehören in die Apotheke, nicht in den Müll.',
         color=PVC, marks=raster(4, 3, 5, 2, 12, 18, 18.5, 25, shape='cyl', fill='#FFFFFF')),
    teil('pvc_folie', 'pvc_blister', 'PVC-Trägerfolie', 'PVC-Folie', 'box',
         x=0, y=0, w=100, d=60, z=0.1, h=0.3, r=3, mass=3.0, opacity=0.6,
         info='Glasklares PVC, etwa 0,25 mm dick, auf die Alufolie gesiegelt. Der leere Blister kommt '
              'als Ganzes in die Gelbe Tonne.',
         color=PVC, marks=raster(1, 30, 5, 1, 18.5, 0.5, 18.5, fill='#BFC8CE')),
    teil('alufolie', 'aluminium_lid_foil', 'Durchdrückfolie', 'Alufolie', 'box',
         x=0, y=0, w=100, d=60, z=0, h=0.1, r=3, explode=[0, 0, 0], mass=0.7,
         materials=[['alu', 88], ['klebstoff', 8], ['druck', 4]],
         info='Hauchdünne Aluminiumfolie mit Siegellack und Aufdruck. Die Tablette drückt man durch sie hindurch.',
         color='#D2D6DA', marks=raster(7, 11, 5, 2, 14, 14, 18.5, 25, shape='cyl', fill='#B5BBC0')
                                + [mark('box', 4, 52, 92, 5, 0, '#4A6FA5')]),
]
explodiere(teile, abstand=25, gruppen=[['naepfe', 'pvc_folie']])
skaliere_masse(teile, oid='blister_pack')
schreibe('blister_pack', teile)
