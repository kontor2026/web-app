"""3D-Modell: paper_coffee_cup. Erzeugt tools/kategorien/modelle/paper_coffee_cup.json.

Typischer 0,3-l-Coffee-to-go-Becher: konische Wand aus PE-beschichtetem Karton (oben 80 mm, unten 60 mm),
eingesetzte Bodenscheibe, gerollter Rand, PS-Trinkdeckel mit Kuppel und Papp-Banderole. Deckel hebt nach oben ab,
Banderole wird seitlich abgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

BECHER = '#F4F1EA'
DECKEL = '#F7F7F5'
PAPIER_PE = [['papier', 94], ['ldpe', 6]]
teile = [
    teil('kuppel', 'ps_cup_lid', 'Deckelkuppel mit Trinköffnung', 'Kuppel', 'cyl',
         x=4, y=4, w=72, z=105, h=6, mass=1.2,
         info='Gewölbtes Oberteil des Deckels aus PS (Recyclingcode 6). Die kleine Öffnung zum Trinken ist vorne, '
              'ein Loch dahinter lässt Luft nach.',
         color=DECKEL, marks=[mark('box', 26, 58, 20, 7, 3.5, '#3A3F44'), mark('cyl', 34, 10, 4, fill='#3A3F44'),
                              mark('cyl', 8, 8, 56, fill='#ECECE8')]),
    teil('deckelrand', 'ps_cup_lid', 'Deckelrand zum Aufdrücken', 'Deckelrand', 'cyl',
         x=-2, y=-2, w=84, z=99, h=6, mass=1.6,
         info='Rastet über den gerollten Becherrand. Zum Entsorgen abziehen: Der Deckel ist reiner Kunststoff und '
              'kommt getrennt in die Gelbe Tonne.',
         color=DECKEL, marks=[mark('cyl', 6, 6, 72, fill='#E6E6E2')]),
    teil('rollrand', 'coated_paper_cup', 'Gerollter Becherrand', 'Rollrand', 'cyl',
         x=0, y=0, w=80, z=97, h=3, mass=0.5, materials=PAPIER_PE,
         info='Der obere Rand ist eingerollt, damit der Becher stabil ist und der Deckel einrasten kann.',
         color=BECHER, marks=[mark('cyl', 3, 3, 74, fill='#5A3A22')]),
    teil('wand_oben', 'coated_paper_cup', 'Becherwand oben', 'Becherwand', 'cyl',
         x=2, y=2, w=76, z=66, h=31, mass=2.2, materials=PAPIER_PE,
         info='Karton mit einer dünnen Polyethylen-Schicht innen, damit der Kaffee nicht durchweicht. '
              'Wegen dieser Schicht gehört der Becher nicht ins Altpapier.',
         color=BECHER),
    teil('wand_mitte', 'coated_paper_cup', 'Becherwand Mitte mit Klebenaht', 'Wand', 'cyl',
         x=5, y=5, w=70, z=36, h=30, mass=2.0, materials=PAPIER_PE, label=False,
         info='Die Wand ist aus einem Zuschnitt gerollt und an einer senkrechten Naht heiß verschweißt.',
         color=BECHER),
    teil('wand_unten', 'coated_paper_cup', 'Becherwand unten', 'Wand unten', 'cyl',
         x=8, y=8, w=64, z=5, h=31, mass=1.9, materials=PAPIER_PE, label=False,
         info='Unten ist die Wand nach innen um die Bodenscheibe gebördelt und dicht verpresst.',
         color=BECHER),
    teil('boden', 'coated_paper_cup', 'Eingesetzte Bodenscheibe', 'Boden', 'cyl',
         x=10, y=10, w=60, z=0, h=5, mass=0.8, materials=PAPIER_PE,
         info='Runde Kartonscheibe, ein paar Millimeter hochgesetzt. Becher ausleeren und mit dem Deckel '
              'getrennt in die Gelbe Tonne geben.',
         color=BECHER, marks=[mark('cyl', 4, 4, 52, fill='#E9E4DA')]),
    teil('banderole', 'cardboard_sleeve', 'Papp-Banderole (Hitzeschutz)', 'Banderole', 'box',
         x=80, y=15, w=0.5, d=50, z=30, h=55, r=0, explode=[55, 0, 0], mass=3.5,
         materials=[['papier', 98], ['druck', 2]],
         info='Wellpappe-Manschette, damit man sich nicht die Finger verbrennt. Abstreifen: Sie ist reines Papier '
              'und gehört ins Altpapier.',
         color='#B5835A', sortBias=100),
]
explodiere(teile, abstand=22, fest=('wand_oben', 'wand_mitte', 'wand_unten', 'boden', 'rollrand'),
           gruppen=[['kuppel', 'deckelrand']])
skaliere_masse(teile, oid='paper_coffee_cup')
schreibe('paper_coffee_cup', teile)
