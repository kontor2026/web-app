"""3D-Modell: stapler. Erzeugt tools/kategorien/modelle/stapler.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Bürotacker (Heftgerät) flach auf dem Tisch, 40 × 150 × 60 mm laut CSV. Scharnier hinten (y = 0), Heftkopf vorne.
# Von unten: Gummifuß, Kunststoff-Unterteil mit Stahl-Amboss, Scharnierfeder, Stahlmagazin mit Klammerstreifen,
# Schieber und Schieberfeder, Eintreiber, Stahlbügel (Arm) und Kunststoffkappe. Explodiert stapeln sich die Teile
# nach oben, der Scharnierstift wird seitlich herausgezogen.
STAHL = '#B8BEC4'
CHROM = '#D5DADE'
KUNST = '#2A2E31'

teile = [
    teil('kappe', 'plastic_base', 'Griffkappe', 'Kappe', 'box',
         x=6, y=40, w=28, d=106, z=52, h=6, r=10, mass=10, material_id='abs',
         info='Kunststoffkappe auf dem Bügel, hier drückt man drauf. Meist nur eingeklipst: mit einem Schraubendreher abhebeln.',
         color=KUNST, marks=[mark('box', 6, 20, 20, 60, 8, '#3A3F44')]),
    teil('arm', 'steel_stapler_body', 'Bügel (Oberarm)', 'Bügel', 'box',
         x=3, y=0, w=34, d=150, z=36, h=16, r=8, mass=85,
         info='Gebogenes, verchromtes Stahlblech. Es trägt vorne den Eintreiber und ist hinten mit dem Scharnierstift gelagert.',
         color=CHROM, marks=[mark('box', 4, 4, 26, 30, 6, '#AEB4B9'), mark('cyl', 14, 8, 6, fill='#9AA2A6')]),
    teil('treiber', 'steel_stapler_body', 'Eintreiber (Messer)', 'Eintreiber', 'box',
         x=13, y=136, w=14, d=2, z=23, h=12, r=0, mass=3,
         info='Dünne Stahlklinge im Kopf des Bügels. Sie drückt beim Heften genau eine Klammer aus dem Magazin durchs Papier.',
         color=STAHL),
    teil('klammern', 'steel_stapler_body', 'Heftklammerstreifen', 'Klammern', 'box',
         x=13.6, y=60, w=12.8, d=74, z=29, h=6, r=0, mass=4,
         info='Etwa 100 verzinkte Stahlklammern, leicht aneinandergeklebt. Vor dem Entsorgen herausnehmen und weiterverwenden.',
         color='#CBD1D5', marks=raster(0.4, 2, 1, 36, 12, 0.8, 0, 2, fill='#9AA2A6')),
    teil('schieber', 'steel_spring', 'Klammerschieber', 'Schieber', 'box',
         x=14, y=40, w=12, d=18, z=28, h=8, r=1, mass=3, material_id='abs', materials=[['pcabs', 100]],
         info='Kunststoffschlitten, der die Klammern nach vorne zum Eintreiber schiebt.',
         color='#C8423A'),
    teil('schieberfeder', 'steel_spring', 'Schieberfeder', 'Schieberfeder', 'box',
         x=17.5, y=12, w=5, d=28, z=30, h=4, r=2, mass=2,
         info='Lange Schraubenfeder aus Federstahl, die den Schieber gegen die Klammern drückt. Mit einer Zange aushängen.',
         color=STAHL, marks=raster(0.5, 1, 1, 13, 4, 0.8, 0, 2, fill='#8E969A')),
    teil('magazin', 'steel_stapler_body', 'Magazin', 'Magazin', 'box',
         x=8, y=10, w=24, d=134, z=22, h=14, r=2, mass=35,
         info='U-förmige Stahlschiene, in die man die Klammern legt. Sie ist hinten mit dem Scharnier verbunden.',
         color=STAHL, marks=[mark('box', 5, 30, 14, 100, 1, '#8E969A')]),
    teil('scharnierfeder', 'steel_spring', 'Rückstellfeder', 'Rückstellfeder', 'box',
         x=15, y=18, w=10, d=60, z=13, h=8, r=2, mass=6,
         info='Blattfeder zwischen Unterteil und Magazin. Sie drückt den Tacker nach dem Heften wieder auf.',
         color='#8E969A'),
    teil('stift', 'steel_stapler_body', 'Scharnierstift', 'Scharnierstift', 'box',
         x=5, y=8, w=30, d=4, z=22, h=4, r=2, explode=[60, 0, 0], mass=2,
         info='Stahlstift, um den sich Bügel und Magazin drehen. Mit Hammer und Durchschlag heraustreiben, '
              'dann zerfällt der Tacker in seine Teile.',
         color='#9AA2A6'),
    teil('amboss', 'steel_stapler_body', 'Amboss (Biegeplatte)', 'Amboss', 'box',
         x=12, y=118, w=16, d=24, z=13, h=2, r=1, mass=5,
         info='Gehärtetes Stahlplättchen mit zwei Mulden. Darin biegen sich die Klammerbeine um; gedreht heftet er zum Lösen.',
         color=CHROM, marks=[mark('box', 4, 8, 3, 8, 1, '#8E969A'), mark('box', 9, 8, 3, 8, 1, '#8E969A')]),
    teil('scharnierbock', 'plastic_base', 'Scharnierbock', 'Scharnierbock', 'box',
         x=4, y=2, w=32, d=22, z=13, h=15, r=4, mass=8, material_id='abs',
         info='Hinterer Aufbau des Unterteils mit der Bohrung für den Scharnierstift.',
         color=KUNST, marks=[mark('box', 3, 3, 26, 16, 3, '#363B3F')]),
    teil('unterteil', 'plastic_base', 'Unterteil', 'Unterteil', 'box',
         x=0, y=0, w=40, d=150, z=3, h=10, r=8, mass=40,
         info='Fuß aus ABS-Kunststoff, mit dem Amboss vernietet. Vom Stahl abhebeln: Kunststoff und Metall getrennt entsorgen.',
         color=KUNST, marks=[mark('box', 3, 30, 34, 115, 6, '#33383C')]),
    teil('fuss', 'plastic_base', 'Gummifuß', 'Gummifuß', 'box',
         x=2, y=4, w=36, d=142, z=0, h=3, r=7, mass=5, material_id='rubber',
         info='Rutschfeste Gummisohle, nur eingeklebt. Sie lässt sich mit den Fingern abziehen.',
         color='#3A3F44'),
]

explodiere(teile, abstand=26)
skaliere_masse(teile, oid='stapler')
schreibe('stapler', teile)
