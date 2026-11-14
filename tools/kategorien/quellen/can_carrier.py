"""3D-Modell: can_carrier. Erzeugt tools/kategorien/modelle/can_carrier.json.

Typischer Sixpack-Ringträger für sechs 0,33-l-Dosen (25 × 17 cm, ca. 0,5 mm LDPE-Folie mit verstärkten Rändern,
hier 1,5 mm dick gezeichnet). Die sechs Ringe sind ein gestanztes Stück; für die Explosion werden sie entlang
der Stanzlinien vom Mittelsteg weg nach außen gezogen, so wie man sie aufschneiden soll.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

FOLIE = '#E6ECEE'
LOCH = '#EDE9E1'  # Tischfarbe: man schaut durch das Loch
AUS = 25
teile = [
    teil('mittelsteg', 'ldpe_rings', 'Mittelsteg', 'Mittelsteg', 'box',
         x=0, y=78, w=250, d=14, z=0, h=1.6, r=3, explode=[0, 0, 0], mass=0.8, color=FOLIE, opacity=0.85,
         info='Der Steg zwischen den beiden Ringreihen hält alles zusammen. Hier greift man den Sixpack.',
         marks=[mark('box', 4, 6, 242, 2, 0, '#D3DBDE'), *[mark('box', 82 + i * 84, 2, 2, 10, 0, '#B9C4C8') for i in range(2)]]),
]
nr = 0
for j, (y, dy) in enumerate(((0, -AUS), (90, AUS))):
    for i, (x, dx) in enumerate(((0, -AUS), (84, 0), (168, AUS))):
        nr += 1
        erster = nr == 1
        teile.append(teil(f'ring_{nr}', 'ldpe_rings', 'Haltering' if erster else f'Haltering {nr}', 'Ring', 'box',
                          x=x, y=y, w=82, d=80, r=30, z=0, h=1.5, explode=[dx, dy, 0], mass=0.7, color=FOLIE,
                          wand=8, boden=0,
                          opacity=0.85, label=erster,
                          info='Dehnbarer LDPE-Ring, der sich um den Dosenrand spannt. Jeden Ring vor dem Wegwerfen '
                               'durchschneiden, damit sich keine Tiere darin verfangen. Dann in die Gelbe Tonne.'
                          if erster else 'Gleicher Ring wie Ring 1, ebenfalls aufschneiden.',
                          marks=[mark('box', 3, 3, 76, 74, 20, '#D3DBDE', zeichnung=True),
                                 mark('box', 5, 5, 72, 70, 19, FOLIE, zeichnung=True),
                                 mark('cyl', 9, 8, 64, 64, fill='#C4CDD1', zeichnung=True),
                                 mark('cyl', 11, 10, 60, 60, fill=LOCH, zeichnung=True),
                                 mark('box', 38, 1 if j == 0 else 73, 6, 6, 3, '#C4CDD1')]))
skaliere_masse(teile, oid='can_carrier', stellen=2)
schreibe('can_carrier', teile)
