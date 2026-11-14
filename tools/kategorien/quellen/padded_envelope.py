"""3D-Modell: padded_envelope. Erzeugt tools/kategorien/modelle/padded_envelope.json.

Typischer Luftpolsterumschlag Größe D (18 × 26 cm außen, Kraftpapier mit eingeklebter Luftpolsterfolie), leer,
Vorderseite oben, Verschlussklappe offen nach hinten (y = 0). Unter der Vorderseite liegen die beiden Lagen des
Luftpolster-Futters, darunter die Rückseite mit Klappe, Haftklebestreifen und Abdeckstreifen. Lagen werden nach
oben abgehoben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

KRAFT = '#C9A46F'
POLSTER = '#E4EEF1'
NOPPEN = raster(3, 4, 17, 20, 8, 8, 10, 10.8, shape='cyl', fill='#CFE0E6')
teile = [
    teil('vorderseite', 'paper_envelope_body', 'Vorderseite (Kraftpapier)', 'Vorderseite', 'box',
         x=0, y=35, w=180, d=225, z=9.6, h=0.4, r=1, mass=3.8, materials=[['papier', 97], ['druck', 3]],
         color=KRAFT,
         info='Braunes Kraftpapier, an drei Rändern mit der Rückseite verklebt. Nur wenn das Futter sauber '
              'herausgeht, darf das Papier ins Altpapier, sonst kommt der ganze Umschlag in den Restmüll.',
         marks=[mark('box', 50, 80, 100, 55, 2, '#F4F1EA'), mark('box', 58, 92, 70, 5, 0, '#3A3F44'),
                mark('box', 58, 104, 60, 5, 0, '#3A3F44'), mark('box', 58, 116, 75, 5, 0, '#3A3F44'),
                mark('box', 145, 10, 25, 30, 1, '#D8342C'), mark('box', 0, 219, 180, 6, 0, '#B48E5C')]),
    teil('polster_oben', 'bubble_lining', 'Luftpolsterfutter (vorne)', 'Polster vorne', 'box',
         x=4, y=37, w=172, d=221, z=5, h=4.6, r=1, mass=2.2, color=POLSTER, opacity=0.6,
         info='LDPE-Noppenfolie, innen an das Papier geklebt. Papier an der Naht aufreißen und die Folie '
              'herausziehen, sie gehört in die Gelbe Tonne.',
         marks=NOPPEN),
    teil('polster_unten', 'bubble_lining', 'Luftpolsterfutter (hinten)', 'Polster hinten', 'box',
         x=4, y=37, w=172, d=221, z=0.4, h=4.6, r=1, mass=2.2, color=POLSTER, opacity=0.6, label=False,
         info='Zweite Lage des Futters. Vorne und hinten sind an den Rändern zu einem Beutel verschweißt.',
         marks=NOPPEN),
    teil('abdeckstreifen', 'paper_envelope_body', 'Abdeckstreifen (silikonisiert)', 'Abdeckpapier', 'box',
         x=8, y=8, w=164, d=18, z=0.5, h=0.1, r=0, explode=[0, -70, 40], mass=0.3, sortBias=100, materials=[['papier', 92], ['pet', 8]],
         color='#F2EFE6',
         info='Silikonbeschichtetes Papier, das den Kleber schützt. Abziehen und in den Restmüll, die Beschichtung '
              'stört im Altpapier.',
         marks=[mark('box', 0, 7, 164, 4, 0, '#E1DCCF')]),
    teil('klebestreifen', 'paper_envelope_body', 'Haftklebestreifen', 'Kleber', 'box',
         x=10, y=10, w=160, d=14, z=0.4, h=0.1, r=0, explode=[0, -70, 15], mass=0.2, sortBias=100, materials=[['klebstoff', 100]], color='#E8DDB5',
         info='Druckempfindlicher Kleber auf der Klappe. Klappe umlegen und fest andrücken, dann ist der Umschlag zu.'),
    teil('rueckseite', 'paper_envelope_body', 'Rückseite mit Verschlussklappe', 'Rückseite', 'box',
         x=0, y=0, w=180, d=260, z=0, h=0.4, r=1, mass=4.4, materials=[['papier', 96], ['klebstoff', 4]],
         color=KRAFT,
         info='Ein Stück mit der Klappe. An den Rändern sieht man die Klebenähte, mit denen Futter und Papier '
              'verbunden sind.',
         marks=[mark('box', 0, 33, 180, 4, 0, '#A98652'), mark('box', 0, 35, 4, 225, 0, '#B48E5C'),
                mark('box', 176, 35, 4, 225, 0, '#B48E5C')]),
]
explodiere(teile, abstand=100)
skaliere_masse(teile, oid='padded_envelope')
schreibe('padded_envelope', teile)
