"""3D-Modell: cereal_box. Erzeugt tools/kategorien/modelle/cereal_box.json.

Typische Müslipackung 375 g (19 × 7 × 29 cm, stehend): Faltschachtel aus bedrucktem Frischfaserkarton,
oben und unten verklebte Laschen, innen ein verschweißter PE-Beutel. Die oberen Laschen heben ab, der
Beutel wird seitlich herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

KARTON = '#D8A440'
teile = [
    teil('laschen_oben', 'cardboard_box_body', 'Verschlusslaschen oben', 'Laschen oben', 'box',
         x=0, y=0, w=190, d=70, z=284, h=6, r=0.5, mass=8, materials=[['papier', 96], ['druck', 4]],
         info='Zwei lange und zwei kurze Laschen, mit Heißleim verklebt. Zum Öffnen an der Lasche aufziehen.',
         color=KARTON, marks=[mark('box', 0, 33, 190, 4, 0, '#B3842E'), mark('box', 80, 33, 30, 4, 1, '#3A3F44')]),
    teil('mantel', 'cardboard_box_body', 'Faltschachtel', 'Schachtel', 'box',
         x=0, y=0, w=190, d=70, z=6, h=278, r=0.5, mass=54, materials=[['papier', 95], ['druck', 4], ['klebstoff', 1]],
         info='Bedruckter Karton, an einer Seitenkante verklebt. Leer flach drücken und ins Altpapier.',
         color=KARTON, marks=[mark('box', 2, 2, 186, 66, 0, '#8E6B45')]),
    teil('laschen_unten', 'cardboard_box_body', 'Bodenlaschen', 'Boden', 'box',
         x=0, y=0, w=190, d=70, z=0, h=6, r=0.5, explode=[0, 0, 0], mass=10, materials=[['papier', 97], ['klebstoff', 3]],
         info='Wie oben, nur fest verklebt. Hier sitzt meist der Code fürs Altpapier.',
         color=KARTON),
    teil('beutel', 'ldpe_film', 'Innenbeutel', 'Innenbeutel', 'box',
         x=8, y=5, w=174, d=60, z=8, h=270, r=6, explode=[230, 0, 0], mass=7, opacity=0.6,
         info='PE-Beutel, hält das Müsli frisch und trocken. Gehört nicht ins Altpapier: leer in die Gelbe Tonne.',
         color='#E8EEF2', marks=[mark('box', 0, 26, 174, 8, 0, '#C9D0D5')] + raster(10, 28, 12, 1, 6, 4, 13.5, fill='#B5BEC5')),
]
explodiere(teile, abstand=60)
skaliere_masse(teile, oid='cereal_box')
schreibe('cereal_box', teile)
