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
    teil('aufdruck', 'cardboard_box_body', 'Bedruckte Vorderseite', 'Aufdruck', 'box',
         x=20, y=160, w=210, d=0.3, z=110, h=170, r=0, mass=1, materials=[['druck', 70], ['papier', 30]],
         color='#7A1F33', sortBias=200, label=False,
         info='Farbe direkt auf der Wellpappe. Sie stört das Papierrecycling nicht.'),
    teil('klappe', 'cardboard_box_body', 'Zapfklappe', 'Zapfklappe', 'box',
         x=95, y=159.7, w=60, d=0.3, z=15, h=60, r=0, explode=[0, 50, 0], mass=2, materials=WELLE,
         info='Perforiertes Fenster vorne unten. Herausdrücken und den Zapfhahn hindurchziehen.',
         color='#B98D5F', sortBias=260),
    teil('boden', 'cardboard_box_body', 'Bodenlaschen', 'Boden', 'box',
         x=0, y=0, w=250, d=160, z=0, h=6, r=1, explode=[0, 0, 0], mass=32, materials=WELLE,
         info='Verklebte Bodenlaschen, tragen das Gewicht der Flüssigkeit.',
         color=PAPPE),
    teil('beutel', 'multilayer_bag', 'Innenbeutel', 'Innenbeutel', 'box',
         x=10, y=10, w=230, d=140, z=8, h=270, r=20, explode=[220, -220, 0], mass=38,
         info='Mehrschichtfolie aus PE und metallisiertem PET, hält Luft fern. Die Schichten lassen sich nicht trennen: '
              'leer in die Gelbe Tonne.',
         color=BEUTEL, marks=[mark('box', 0, 0, 230, 6, 3, '#9AA1A8'), mark('box', 0, 134, 230, 6, 3, '#9AA1A8')]),
    teil('stutzen', 'multilayer_bag', 'Ausgießstutzen', 'Stutzen', 'cyl',
         material_id='ldpe', x=110, y=150, w=30, d=9, z=20, h=30, explode=[220, -190, 0], mass=5, materials=[['ldpe', 100]],
         info='In den Beutel eingeschweißter Stutzen aus PE. Bleibt am Beutel.',
         color='#F2F0EA'),
    teil('taste', 'pp_tap', 'Drucktaste', 'Drucktaste', 'cyl',
         x=113, y=137, w=24, d=20, z=57, h=5, explode=[220, -110, 30], mass=3, material_id='rubber', materials=[['tpe', 100]],
         color='#5C8FC2', sortBias=5,
         info='Weiche Taste mit Membran: Drückt man sie, öffnet sich das Ventil im Hahn. Kommt mit dem Hahn in die Gelbe Tonne.',
         marks=[mark('cyl', 4, 3, 16, 14, fill='#7AA6D2')]),
    teil('hahn', 'pp_tap', 'Zapfhahn', 'Zapfhahn', 'box',
         x=107, y=135, w=36, d=24, z=15, h=42, r=6, explode=[220, -110, 0], mass=11,
         info='PP-Hahn mit Drucktaste, auf den Stutzen gesteckt. Abziehen und ebenfalls in die Gelbe Tonne.',
         color='#2E5E8C', marks=[mark('cyl', 6, 2, 24, 20, fill='#24507A')]),
]
explodiere(teile, abstand=60)
skaliere_masse(teile, oid='bag_in_box')
schreibe('bag_in_box', teile)
