"""3D-Modell: bag_in_box. Erzeugt tools/kategorien/modelle/bag_in_box.json.

Typische Bag-in-Box 5 l für Saft oder Wein (25 × 16 × 30 cm, stehend): Wellpappkarton mit Tragegriff in den
Deckellaschen und perforierter Zapfklappe vorne unten, innen ein metallisierter Mehrschichtbeutel mit
eingeschweißtem Ausgießstutzen und aufgestecktem PP-Zapfhahn. Deckellaschen heben ab, die Zapfklappe klappt nach
vorne, Beutel mit Stutzen und Hahn wird seitlich herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

PAPPE = '#C49A6C'
BEUTEL = '#B8BEC4'
WELLE = [['papier', 100]]
teile = [
    teil('deckel', 'cardboard_box_body', 'Deckellaschen mit Tragegriff', 'Deckel', 'box',
         x=0, y=0, w=250, d=160, z=294, h=6, r=1, mass=32, materials=[['papier', 97], ['druck', 3]],
         info='Vier verklebte Laschen. Die Grifflöcher sind ausgestanzt; zum Flachmachen die Laschen aufreißen.',
         color=PAPPE, marks=[mark('box', 0, 78, 250, 4, 0, '#9E7A52'), mark('box', 95, 60, 60, 14, 7, '#3A3F44'),
                             mark('box', 95, 86, 60, 14, 7, '#3A3F44')]),
    teil('mantel', 'cardboard_box_body', 'Karton', 'Karton', 'box',
         x=0, y=0, w=250, d=160, z=6, h=288, r=1, mass=175, materials=[['papier', 97], ['druck', 2], ['klebstoff', 1]],
         info='Bedruckte Wellpappe, schützt den weichen Beutel. Leer flach gefaltet ins Altpapier.',
         color=PAPPE, marks=[mark('box', 4, 4, 242, 152, 0, '#8E6B45')]),
    teil('klappe', 'cardboard_box_body', 'Zapfklappe', 'Zapfklappe', 'box',
         x=95, y=159.7, w=60, d=0.3, z=15, h=60, r=0, explode=[0, 50, 0], mass=2, materials=WELLE,
         info='Perforiertes Fenster vorne unten. Herausdrücken und den Zapfhahn hindurchziehen.',
         color='#B98D5F', sortBias=100),
    teil('boden', 'cardboard_box_body', 'Bodenlaschen', 'Boden', 'box',
         x=0, y=0, w=250, d=160, z=0, h=6, r=1, explode=[0, 0, 0], mass=32, materials=WELLE,
         info='Verklebte Bodenlaschen, tragen das Gewicht der Flüssigkeit.',
         color=PAPPE),
    teil('beutel', 'multilayer_bag', 'Innenbeutel', 'Innenbeutel', 'box',
         x=10, y=10, w=230, d=140, z=8, h=270, r=20, explode=[290, 0, 0], mass=38,
         info='Mehrschichtfolie aus PE und metallisiertem PET, hält Luft fern. Die Schichten lassen sich nicht trennen: '
              'leer in die Gelbe Tonne.',
         color=BEUTEL, marks=[mark('box', 0, 0, 230, 6, 3, '#9AA1A8'), mark('box', 0, 134, 230, 6, 3, '#9AA1A8')]),
    teil('stutzen', 'multilayer_bag', 'Ausgießstutzen', 'Stutzen', 'cyl',
         material_id='ldpe', x=110, y=150, w=30, d=9, z=20, h=30, explode=[290, 25, 0], mass=5, materials=[['ldpe', 100]],
         info='In den Beutel eingeschweißter Stutzen aus PE. Bleibt am Beutel.',
         color='#F2F0EA'),
    teil('hahn', 'pp_tap', 'Zapfhahn', 'Zapfhahn', 'box',
         x=107, y=135, w=36, d=24, z=15, h=42, r=6, explode=[290, 60, 0], mass=14,
         info='PP-Hahn mit Drucktaste, auf den Stutzen gesteckt. Abziehen und ebenfalls in die Gelbe Tonne.',
         color='#2E5E8C', marks=[mark('cyl', 8, 4, 20, 16, fill='#E8EEF2')]),
]
explodiere(teile, abstand=60)
skaliere_masse(teile, oid='bag_in_box')
schreibe('bag_in_box', teile)
