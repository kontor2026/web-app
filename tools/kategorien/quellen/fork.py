"""3D-Modell: fork. Erzeugt tools/kategorien/modelle/fork.json.

Typische Tafelgabel aus Edelstahl (20 cm) flach auf dem Tisch, Zinken hinten (y = 0), Griff vorne. Die Gabel ist
aus einem Blech gestanzt und gebogen: Griff liegt auf, Hals steigt an, Zinken stehen leicht hoch. Explodiert
rücken Zinken, Zinkenansatz, Hals und Griff entlang der Längsachse auseinander.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

STAHL = '#C3C9CE'
GLANZ = '#E3E7EA'

teile = [
    teil(f'zinke_{i + 1}', 'steel_cutlery', f'Zinke {i + 1}', 'Zinken', 'box',
         x=i * 7, y=0, w=4, d=38, z=8.5, h=2.5, r=2, explode=[0, -26, 0], mass=2, label=i == 0,
         info='Vier gestanzte Zinken, die Spitzen sind leicht abgerundet. Sie sind aus demselben Stück Stahl wie die '
              'ganze Gabel.',
         color=STAHL, marks=[mark('box', 1.5, 4, 1, 30, 0.5, GLANZ, zeichnung=True)])
    for i in range(4)
]
teile += [
    teil('ansatz', 'steel_cutlery', 'Zinkenansatz', 'Ansatz', 'box',
         x=0, y=34, w=25, d=20, z=7.5, h=3.5, r=7, explode=[0, -14, 0], mass=6,
         info='Breiteste Stelle der Gabel, hier ist das Blech nach oben gewölbt, damit Essen nicht herunterrutscht.',
         color=STAHL, marks=[mark('box', 3, 3, 19, 12, 5, GLANZ, zeichnung=True)]),
    teil('schulter', 'steel_cutlery', 'Schulter', 'Schulter', 'box',
         x=5, y=50, w=15, d=14, z=5, h=3.5, r=6, explode=[0, -6, 0], mass=3, label=False,
         info='Hier verjüngt sich die Gabel vom Kopf zum Hals.',
         color=STAHL, marks=[mark('box', 3, 2, 9, 9, 4, GLANZ, zeichnung=True)]),
    teil('hals', 'steel_cutlery', 'Hals', 'Hals', 'box',
         x=8, y=60, w=9, d=46, z=2.5, h=3.5, r=4, explode=[0, 0, 0], mass=7,
         info='Schmale, gebogene Stelle zwischen Griff und Zinken. Durch die Biegung liegt die Gabel nur hinten '
              'und vorne auf.',
         color=STAHL, marks=[mark('box', 3, 4, 3, 38, 1.5, GLANZ, zeichnung=True)]),
    teil('griff', 'steel_cutlery', 'Griff', 'Griff', 'box',
         x=2, y=102, w=21, d=98, z=0, h=3, r=10, explode=[0, 12, 0], mass=22,
         info='Rostfreier Edelstahl (18/10: mit Chrom und Nickel). Besteck hält ewig: gut erhaltenes spenden, '
              'kaputtes als Metallschrott zum Wertstoffhof, nicht in die Gelbe Tonne.',
         color=STAHL, marks=[mark('box', 2, 2, 17, 94, 8, '#B3BABF', zeichnung=True), mark('box', 4, 12, 13, 74, 6, GLANZ, zeichnung=True)]),
]
skaliere_masse(teile, oid='fork')
schreibe('fork', teile)
