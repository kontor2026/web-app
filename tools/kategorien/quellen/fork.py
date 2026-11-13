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
         x=i * 7, y=0, w=4, d=40, z=10, h=3, r=2, explode=[0, -24, 0], mass=2, label=i == 0,
         info='Vier gestanzte Zinken, die Spitzen sind leicht abgerundet. Sie sind aus demselben Stück Stahl wie die '
              'ganze Gabel.',
         color=STAHL, marks=[mark('box', 1.5, 3, 1, 34, 0.5, GLANZ)])
    for i in range(4)
]
teile += [
    teil('ansatz', 'steel_cutlery', 'Zinkenansatz', 'Ansatz', 'box',
         x=0, y=36, w=25, d=20, z=7, h=4, r=5, explode=[0, -12, 0], mass=7,
         info='Breiteste Stelle der Gabel, hier ist das Blech nach oben gewölbt, damit Essen nicht herunterrutscht.',
         color=STAHL, marks=[mark('box', 3, 4, 19, 10, 4, GLANZ)]),
    teil('hals', 'steel_cutlery', 'Hals', 'Hals', 'box',
         x=8, y=56, w=9, d=44, z=3, h=5, r=3, explode=[0, 0, 0], mass=8,
         info='Schmale, gebogene Stelle zwischen Griff und Zinken. Durch die Biegung liegt die Gabel nur hinten '
              'und vorne auf.',
         color=STAHL),
    teil('griff', 'steel_cutlery', 'Griff', 'Griff', 'box',
         x=2, y=100, w=21, d=100, z=0, h=3.5, r=10, explode=[0, 12, 0], mass=22,
         info='Rostfreier Edelstahl (18/10: mit Chrom und Nickel). Besteck hält ewig: gut erhaltenes spenden, '
              'kaputtes als Metallschrott zum Wertstoffhof, nicht in die Gelbe Tonne.',
         color=STAHL, marks=[mark('box', 3, 10, 15, 80, 7, GLANZ), mark('cyl', 7.5, 88, 6, fill='#A9B0B5')]),
]
skaliere_masse(teile, oid='fork')
schreibe('fork', teile)
