"""3D-Modell: blister_pack. Erzeugt tools/kategorien/modelle/blister_pack.json.

Typischer Tabletten-Blister 10 Stück (100 × 60 mm): PVC-Folie mit 2 × 5 einzelnen tiefgezogenen Näpfen, unten die
aufgesiegelte, bedruckte Aluminium-Durchdrückfolie. Die PVC-Folie hebt nach oben ab.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

PVC = '#E4EBEF'
TABLETTE = '#FFFFFF'
# 2 × 5 Näpfe für ovale Tabletten (14 × 8 mm), Napf 16 × 12 mm, 5,3 mm hoch
NAEPFE = [(round(5 + i * 18.5, 2), y0) for y0 in (12, 36) for i in range(5)]
naepfe = [teil(f'napf{n}', 'pvc_blister', 'Tablettennapf', 'Napf', 'cyl',
               x=x, y=y, w=16, d=12, z=0.4, h=5.3, mass=0.12, opacity=0.55, color=PVC, label=(n == 0),
               info='Tiefgezogene Mulde, je eine pro Tablette. Alle Tabletten herausdrücken; Medikamentenreste '
                    'gehören in die Apotheke oder den Restmüll, nicht in die Gelbe Tonne.' if n == 0 else
                    'Napf aus PVC, gehört zur Blisterfolie.',
               marks=[mark('cyl', 1.5, 2, 13, 8, fill=TABLETTE), mark('box', 7.6, 3, 0.6, 6, 0, '#D5D9DC')])
          for n, (x, y) in enumerate(NAEPFE)]
teile = naepfe + [
    teil('pvc_folie', 'pvc_blister', 'PVC-Trägerfolie', 'PVC-Folie', 'box',
         x=0, y=0, w=100, d=60, z=0.1, h=0.3, r=3, mass=2.4, opacity=0.6,
         info='Glasklares PVC, etwa 0,25 mm dick, mit der Alufolie verschweißt. PVC und Alu lassen sich nicht '
              'trennen; der leere Blister kommt als Ganzes in die Gelbe Tonne.',
         color=PVC, marks=[mark('box', 2.5, 29.5, 95, 1, 0, '#BFC8CE')]
         + [mark('box', round(22.2 + i * 18.5, 1), 2, 0.6, 56, 0, '#BFC8CE') for i in range(4)]
         + [mark('box', 3, 3, 6, 6, 1.5, '#D2DADE')]),
    teil('siegellack', 'aluminium_lid_foil', 'Heißsiegellack', 'Siegellack', 'box',
         x=0, y=0, w=100, d=60, z=0.08, h=0.02, r=3, mass=0.1, materials=[['klebstoff', 100]],
         color='#E8E2C8', opacity=0.8,
         info='Hauchdünne Lackschicht auf der Alufolie. Beim Erhitzen schmilzt sie und klebt die PVC-Folie fest.'),
    teil('alufolie', 'aluminium_lid_foil', 'Durchdrückfolie', 'Alufolie', 'box',
         x=0, y=0, w=100, d=60, z=0, h=0.08, r=3, explode=[0, 0, 0], mass=0.7,
         materials=[['alu', 92], ['druck', 8]],
         info='Hauchdünne Aluminiumfolie (0,02 mm) mit Aufdruck. Die Tablette drückt man durch sie hindurch.',
         color='#D2D6DA', marks=[mark('cyl', x + 1, y, 14, 12, fill='#B5BBC0') for x, y in NAEPFE]
                                + [mark('box', 2.5, 29.5, 95, 1, 0, '#A9B0B6'), mark('box', 4, 52, 92, 5, 0, '#4A6FA5'),
                                   mark('box', 4, 2, 40, 4, 0, '#7C8790')]),
]
explodiere(teile, abstand=22, gruppen=[[p['id'] for p in naepfe] + ['pvc_folie']])
skaliere_masse(teile, oid='blister_pack')
schreibe('blister_pack', teile)
