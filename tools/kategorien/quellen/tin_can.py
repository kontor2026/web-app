"""3D-Modell: tin_can. Erzeugt tools/kategorien/modelle/tin_can.json.

Typische Konservendose 425 ml (73 × 110 mm, dreiteilig aus Weißblech): Rumpf mit Sicken und Längsnaht, Boden
und Aufreißdeckel mit Ring sind aufgefalzt. Deckel, Ring und Boden werden gestapelt, das Etikett seitlich gezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

BLECH = '#C3C8CC'
WB = [['weissblech', 97], ['druck', 3]]
teile = [
    teil('ring', 'steel_can_lid', 'Aufreißring', 'Ring', 'box',
         x=26.5, y=8, w=20, d=26, z=109.4, h=0.6, r=9, mass=1.5, materials=[['weissblech', 100]],
         info='Mit einer Niete am Deckel befestigt. Hochziehen, dann reißt der Deckel entlang der Ritzlinie ab.',
         color='#B9BFC4', marks=[mark('box', 4, 4, 12, 12, 6, fill='#8E959B')]),
    teil('deckel', 'steel_can_lid', 'Aufreißdeckel', 'Deckel', 'cyl',
         x=0, y=0, w=73, z=107, h=3, mass=9, materials=WB,
         info='Weißblech mit eingeprägter Ritzlinie. Die Kante ist scharf: in die leere Dose drücken '
              'und mit ihr in die Gelbe Tonne geben.',
         color=BLECH, marks=[mark('cyl', 3, 3, 67), mark('cyl', 5, 5, 63, fill='#B3B9BE'),
                             mark('cyl', 33.5, 22, 6, fill='#9DA4AA')]),
    teil('rumpf', 'steel_can_body', 'Dosenrumpf', 'Rumpf', 'cyl',
         x=0.5, y=0.5, w=72, z=3, h=104, mass=36, materials=WB,
         info='Stahlblech, dünn verzinnt (Weißblech), zu einem Rohr gerollt und verschweißt. Die Sicken machen ihn '
              'stabil. Ein Magnet bleibt daran hängen, so erkennt man Stahl.',
         color=BLECH, marks=[mark('cyl', 2, 2, 68, fill='#E6E2D6')]),
    teil('boden', 'steel_can_lid', 'Dosenboden', 'Boden', 'cyl',
         x=0, y=0, w=73, z=0, h=3, mass=7, materials=WB,
         info='Wie der Deckel auf den Rumpf gefalzt, aber ohne Aufreißlinie. Bleibt an der Dose.',
         color=BLECH, marks=[mark('cyl', 3, 3, 67), mark('cyl', 12, 12, 49, fill='#B3B9BE')]),
    teil('etikett', 'paper_label', 'Papierbanderole', 'Etikett', 'box',
         x=73, y=11.5, w=0.3, d=50, z=10, h=90, r=0, explode=[50, 0, 0], mass=2,
         info='Rundum geklebtes Papier. Darf dranbleiben, beim Einschmelzen verbrennt es.',
         color='#D9503F', sortBias=100),
]
explodiere(teile, abstand=25, nach_liste=True)
skaliere_masse(teile, oid='tin_can')
schreibe('tin_can', teile)
