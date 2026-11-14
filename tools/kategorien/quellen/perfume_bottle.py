"""3D-Modell: perfume_bottle. Erzeugt tools/kategorien/modelle/perfume_bottle.json.

Typischer 50-ml-Parfümflakon: dickwandiger rechteckiger Glaskörper (60 × 40 mm) mit schwerem Boden,
aufgecrimpte Sprühpumpe (Aluminium-Kragen, Sprühkopf, Pumpenkörper, Stahlfeder, Steigrohr) und
aufgesteckte Kunststoffkappe. Glas bleibt stehen, Pumpenteile und Kappe stapeln darüber, das Steigrohr
wird seitlich gezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

GLAS = '#E6EEF0'
OP = 0.65
GOLD = '#E6CC80'
teile = [
    teil('kappe', 'perfume_cap', 'Kappe', 'Kappe', 'box',
         x=15, y=5, w=30, d=30, z=72, h=28, r=4, mass=12,
         info='Schwere Kunststoffkappe, nur aufgesteckt. Abziehen und in die Gelbe Tonne geben.',
         color='#1F2328', marks=[mark('box', 3, 3, 24, 24, 3, '#2C3238')]),
    teil('spruehkopf', 'perfume_pump', 'Sprühkopf', 'Sprühkopf', 'cyl',
         material_id='pp', x=24, y=14, w=12, z=82, h=10, mass=1, materials=[['pp', 70], ['alu', 30]],
         info='Kunststoffknopf mit Alu-Hülle und feiner Düse. Er wird nur auf den Pumpenstift gesteckt.',
         color=GOLD, marks=[mark('cyl', 2, 2, 8, fill='#B8963A'), mark('cyl', 5, 10, 2, fill='#2A2E31')]),
    teil('kragen', 'perfume_pump', 'Crimp-Kragen', 'Kragen', 'cyl',
         x=21.5, y=11.5, w=17, z=72, h=10, mass=1.5, materials=[['alu', 90], ['gummi', 10]],
         info='Aluminiumkappe, die mit einer Gummidichtung fest um den Glashals gepresst ist. Nur mit einer Zange '
              'abhebeln, dann kann das Glas ins Altglas.',
         color=GOLD, marks=[mark('cyl', 4, 4, 9, fill='#B8963A')]),
    teil('dichtung', 'perfume_pump', 'Halsdichtung', 'Dichtung', 'cyl',
         material_id='rubber', x=22.5, y=12.5, w=15, z=74, h=1, mass=0.1, materials=[['gummi', 100]],
         info='Dünner Gummiring zwischen Glasrand und Kragen. Er hält den Flakon dicht, damit kein Duft verdunstet.',
         color='#3A3D40', marks=[mark('cyl', 4, 4, 7, fill='#E6EEF0')]),
    teil('feder', 'perfume_pump', 'Pumpenfeder', 'Feder', 'cyl',
         material_id='steel', x=28, y=18, w=4, z=60, h=10, mass=0.2, materials=[['stahl', 100]],
         info='Winzige Edelstahlfeder, die den Sprühkopf zurückdrückt.',
         color='#9DA4AA', marks=[mark('cyl', 1, 1, 2, fill='#6E757B')], sortBias=-40),
    teil('pumpe', 'perfume_pump', 'Pumpenkörper', 'Pumpe', 'cyl',
         material_id='pp', x=26.5, y=16.5, w=7, z=50, h=26, mass=1.2, materials=[['pp', 70], ['ldpe', 20], ['gummi', 10]],
         info='Kleiner Kolben mit Ventil, der bei jedem Druck eine genau abgemessene Menge zerstäubt.',
         color='#ECECE8', marks=[mark('cyl', 2, 2, 3, fill='#C9CED3')], sortBias=-40),
    teil('hals', 'glass_container', 'Glashals', 'Hals', 'cyl',
         x=22.5, y=12.5, w=15, z=66, h=8, mass=3,
         info='Kurzer Hals mit Wulst, unter den der Kragen gepresst wird.', color=GLAS, opacity=OP,
         wand=3.5, boden=0, marks=[mark('cyl', 4, 4, 7, fill='#C8D6DA', zeichnung=True)]),
    teil('koerper', 'glass_container', 'Glaskörper', 'Flakon', 'box',
         x=0, y=0, w=60, d=40, z=10, h=56, r=6, mass=100,
         info='Dickes Glas, Recyclingcode GL 70. Leer, mit Pumpe nach Möglichkeit entfernt, ins Weißglas. '
              'Parfüm ist brennbar, Reste nicht in den Ausguss kippen.',
         color=GLAS, opacity=OP, wand=5, boden=0, marks=[mark('box', 4, 4, 52, 32, 4, zeichnung=True)]),
    teil('boden', 'glass_container', 'Glasboden', 'Boden', 'box',
         x=0, y=0, w=60, d=40, z=0, h=10, r=6, mass=30,
         info='Massiver Glasboden, er macht den Flakon schwer und standfest.', color=GLAS, opacity=0.75, label=False),
    teil('steigrohr', 'perfume_pump', 'Steigrohr', 'Steigrohr', 'cyl',
         material_id='ldpe', x=29, y=19, w=2, z=11, h=40, explode=[62, 0, 0], mass=0.2, materials=[['ldpe', 100]],
         info='Dünner Schlauch, durch den die Pumpe das Parfüm vom Boden ansaugt.', color='#EDEDE8', sortBias=-40),
]
explodiere(teile, abstand=18, nach_liste=True, gruppen=[['hals', 'koerper', 'boden']])
skaliere_masse(teile, oid='perfume_bottle')
schreibe('perfume_bottle', teile)
