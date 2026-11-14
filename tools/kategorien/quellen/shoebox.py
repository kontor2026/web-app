"""3D-Modell: shoebox. Erzeugt tools/kategorien/modelle/shoebox.json.

Typischer Schuhkarton (33 × 20 × 12 cm) aus bedrucktem Graukarton: Unterteil, übergestülpter Stülpdeckel,
Seidenpapier über den Schuhen, Größenetikett an der Stirnseite. Seidenpapier und Deckel heben nach oben ab,
das Etikett wird seitlich herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

KARTON = '#D9D4CB'
DRUCK = '#3F5C78'
teile = [
    teil('deckel', 'cardboard_box_body', 'Stülpdeckel', 'Deckel', 'box',
         x=0, y=0, w=330, d=200, z=95, h=25, r=2, mass=95, materials=[['papier', 97], ['druck', 3]],
         info='Wird über das Unterteil gestülpt. An den Ecken geklammert oder geklebt; zum Flachmachen dort aufreißen.',
         color=DRUCK, marks=[mark('box', 115, 70, 100, 60, 4, '#F2F0EA'), mark('box', 130, 88, 70, 24, 2, DRUCK),
                             mark('box', 0, 0, 330, 4, 0, '#33495F')]),
    teil('seidenpapier', 'tissue_paper', 'Seidenpapier', 'Seidenpapier', 'box',
         x=8, y=6, w=314, d=188, z=104, h=2, r=2, mass=6, opacity=0.85,
         info='Dünnes Papier, das die Schuhe schützt. Wiederverwenden zum Einpacken oder ins Altpapier.',
         color='#FBFAF7', marks=[mark('box', 155, 0, 4, 188, 0, '#ECE9E2')]),
    teil('unterteil', 'cardboard_box_body', 'Unterteil', 'Unterteil', 'box',
         x=2, y=2, w=326, d=196, z=0, h=118, r=2, mass=145, materials=[['papier', 98], ['druck', 2]],
         info='Graukarton aus Altpapier, außen bedruckt. Sauber und flach gefaltet ins Altpapier.',
         color=KARTON, marks=[mark('box', 2, 2, 322, 192, 1, '#A8A196')]),
    teil('etikett', 'cardboard_box_body', 'Größenetikett', 'Etikett', 'box',
         material_id='paper', x=328, y=40, w=0.3, d=120, z=15, h=70, r=0, explode=[70, 0, 0], mass=1,
         materials=[['papier', 85], ['druck', 8], ['klebstoff', 7]],
         info='Aufkleber mit Größe, Farbe und Barcode. Darf beim Altpapier am Karton bleiben.',
         color='#F4F2EE', sortBias=100),
]
explodiere(teile, abstand=100, nach_liste=True)
skaliere_masse(teile, oid='shoebox')
schreibe('shoebox', teile)
