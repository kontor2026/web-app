"""3D-Modell: newspaper. Erzeugt tools/kategorien/modelle/newspaper.json.

Typische Tageszeitung, einmal gefaltet (29 × 40 cm, Falz hinten bei y = 0): drei ineinandergelegte Bücher
(Titelbuch, Lokalteil, Sport) und ein Werbeprospekt aus gestrichenem Papier. Die Lagen werden nach oben abgehoben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, explodiere, schreibe  # noqa: E402

PAPIER = '#ECE8DF'
TEXT = '#9A9890'
ZEITUNG = [['papier', 97], ['druck', 3]]


def spalten(y0, y1, n=5, x0=12, breite=266):
    """Textspalten als graue Streifen."""
    b = (breite - (n - 1) * 6) / n
    return [mark('box', round(x0 + i * (b + 6), 1), y0, round(b, 1), y1 - y0, 0, TEXT) for i in range(n)]


teile = [
    teil('titelbuch', 'paper_sheets', 'Titelbuch (Mantel)', 'Titelbuch', 'box',
         x=0, y=0, w=290, d=400, z=7, h=3, r=0, mass=70, materials=ZEITUNG,
         info='Zeitungspapier aus fast 100 % Altpapier, mit schwarzer und farbiger Druckfarbe bedruckt. '
              'Gelesen kommt es wieder ins Altpapier und wird daraus neue Zeitung.',
         color=PAPIER, marks=[mark('box', 12, 12, 266, 34, 0, '#2A2E31'), mark('box', 12, 56, 266, 14, 0, '#5A5F63'),
                              mark('box', 12, 80, 160, 110, 0, '#7E9BB2')]
                             + [mark('box', 182, 80 + i * 22, 96, 12, 0, TEXT) for i in range(5)]
                             + spalten(200, 388)),
    teil('prospekt', 'paper_sheets', 'Werbeprospekt (Beilage)', 'Prospekt', 'box',
         x=40, y=50, w=210, d=297, z=5, h=2, r=0, mass=40, materials=[['papier', 93], ['druck', 7]],
         info='Glänzendes, gestrichenes Papier mit mehr Druckfarbe. Darf auch ins Altpapier. Ist er in Folie '
              'eingeschweißt, die Folie in die Gelbe Tonne.',
         color='#F7F5F0', marks=[mark('box', 10, 10, 190, 30, 0, '#C8423A'), mark('box', 10, 50, 90, 90, 0, '#E3B23C'),
                                 mark('box', 110, 50, 90, 90, 0, '#5C9E5A'), mark('box', 10, 150, 90, 90, 0, '#4C7FB5'),
                                 mark('box', 110, 150, 90, 90, 0, '#E3B23C'), mark('box', 10, 255, 190, 30, 0, '#C8423A')]),
    teil('lokalteil', 'paper_sheets', 'Lokalteil', 'Lokalteil', 'box',
         x=0, y=0, w=290, d=400, z=3, h=2, r=0, mass=50, materials=ZEITUNG,
         info='Zweites Buch, lose eingelegt. Zeitungen sind nicht geklebt oder geheftet, nur gefaltet.',
         color=PAPIER, marks=[mark('box', 12, 12, 266, 24, 0, '#3E6E9E'), mark('box', 12, 46, 120, 90, 0, '#9DB27A')]
                             + spalten(146, 388, 4)),
    teil('sportteil', 'paper_sheets', 'Sportteil', 'Sport', 'box',
         x=0, y=0, w=290, d=400, z=0, h=3, r=0, mass=48, materials=ZEITUNG,
         info='Unterstes Buch. Zeitungen sauber und trocken ins Altpapier, nicht in Plastiktüten.',
         color=PAPIER, marks=[mark('box', 12, 12, 266, 24, 0, '#5C9E5A'), mark('box', 150, 46, 128, 100, 0, '#C9B48A')]
                             + spalten(156, 388, 4)),
]
explodiere(teile, abstand=110)
skaliere_masse(teile, oid='newspaper')
schreibe('newspaper', teile)
