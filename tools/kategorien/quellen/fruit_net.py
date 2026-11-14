"""3D-Modell: fruit_net. Erzeugt tools/kategorien/modelle/fruit_net.json.

Typisches leeres Obstnetz (Raschelnetz aus LDPE für 1 kg Orangen oder Zwiebeln, flach 15 × 25 cm), oben mit einer
bedruckten Etikett-Banderole verschweißt (hinten bei y = 0), unten zugeschweißt. Das Netz ist ein Schlauch und
liegt doppelt. Die Lagen werden nach oben abgehoben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

NETZ = '#E2672E'
FADEN = '#C24F1E'


def maschen(w, y0, y1, schritt=12):
    """Netzfäden als dünne Längs- und Querstreifen."""
    m = [mark('box', round(x, 1), y0, 1.2, y1 - y0, 0, FADEN) for x in range(4, int(w) - 2, schritt)]
    m += [mark('box', 0, round(y, 1), w, 1.2, 0, FADEN) for y in range(y0 + 4, y1 - 2, schritt)]
    return m


teile = [
    teil('etikett_vorne', 'plastic_label', 'Etikett-Banderole (Vorderseite)', 'Etikett', 'box',
         x=0, y=0, w=150, d=40, z=4.2, h=0.3, r=1, mass=0.6, materials=[['pp', 94], ['druck', 6]], color='#F4F1EA',
         info='Bedruckter PP-Streifen mit Sorte, Herkunft und Gewicht, um das Netz herum verschweißt. Mit der Schere '
              'abschneiden oder an der Naht aufreißen.',
         marks=[mark('box', 6, 5, 60, 30, 3, '#E2672E'), mark('box', 74, 6, 66, 6, 0, '#3A3F44'),
                mark('box', 74, 16, 50, 5, 0, '#3A3F44'), mark('box', 74, 26, 66, 9, 0, '#22272B')]),
    teil('netz_oben', 'fruit_net_mesh', 'Netz (obere Lage)', 'Netz', 'box',
         x=0, y=30, w=150, d=220, z=2.2, h=2, r=2, mass=1.5, color=NETZ, opacity=0.35,
         info='Gewirkter Schlauch aus dünnen LDPE-Fäden. Leer in die Gelbe Tonne. Sind Metallklammern dran, '
              'diese vorher abschneiden.',
         marks=maschen(150, 0, 220)),
    teil('netz_unten', 'fruit_net_mesh', 'Netz (untere Lage)', 'Netz unten', 'box',
         x=0, y=30, w=150, d=220, z=0.2, h=2, r=2, mass=1.5, color=NETZ, opacity=0.35, label=False,
         info='Rückseite desselben Netzschlauchs. Netze können sich in Maschinen verfangen, deshalb nicht in '
              'andere Verpackungen stopfen.',
         marks=maschen(150, 0, 220)),
    teil('bodennaht', 'fruit_net_mesh', 'Bodennaht (verschweißt)', 'Bodennaht', 'box',
         x=0, y=244, w=150, d=6, z=4.2, h=0.6, r=1, mass=0.3, color=FADEN,
         info='Unten sind beide Netzlagen zu einer festen Kante verschmolzen.'),
    teil('etikett_hinten', 'plastic_label', 'Etikett-Banderole (Rückseite)', 'Etikett hinten', 'box',
         x=0, y=0, w=150, d=40, z=0, h=0.3, r=1, mass=0.5, materials=[['pp', 97], ['druck', 3]], color='#F4F1EA',
         label=False,
         info='Rückseite der Banderole mit Barcode. Netz und Etikett sind verschiedene Kunststoffe, kommen aber '
              'beide in die Gelbe Tonne.',
         marks=[mark('box', 10, 8, 60, 24, 0, '#22272B')]),
]
explodiere(teile, abstand=100)
skaliere_masse(teile, oid='fruit_net')
schreibe('fruit_net', teile)
