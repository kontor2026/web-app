"""3D-Modell: incandescent_bulb. Erzeugt tools/kategorien/modelle/incandescent_bulb.json.

Klassische Glühbirne A60, E27, 60 W, stehend auf dem Sockel. Glaskolben aus fünf Scheiben (bewegen sich gemeinsam),
innen der Tellerfuß aus Glas mit Quetschung, zwei Zuleitungsdrähte, Haltedrähte und die Wolframwendel.
Explodiert: Fußkontakt, Sockel, Kitt, Tellerfuß und Kolben senkrecht gestapelt, Drähte und Wendel rechts (dx > 0).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

GLAS = '#E9F1F4'
GLASM = [['behaelterglas', 100]]

teile = [
    teil('kolben_kuppe', 'bulb_glass', 'Glaskolben (Kuppe)', 'Kolben', 'cyl',
         x=14, y=14, w=32, z=100, h=5, mass=1.5, materials=GLASM,
         info='Dünnes Kalk-Natron-Glas, nur etwa 0,5 mm dick. Innen Vakuum oder Edelgas, damit die Wendel '
              'nicht verbrennt. Glühbirnen gehören in den Restmüll, nicht ins Altglas.',
         color=GLAS, opacity=0.6),
    teil('kolben_oben', 'bulb_glass', 'Glaskolben (oben)', 'Kolben oben', 'cyl',
         x=4, y=4, w=52, z=88, h=12, mass=3.5, materials=GLASM, color=GLAS, opacity=0.6, label=False,
         info='Gewölbter oberer Teil des Kolbens.'),
    teil('kolben_mitte', 'bulb_glass', 'Glaskolben (Mitte)', 'Kolben Mitte', 'cyl',
         x=0, y=0, w=60, z=60, h=28, mass=6, materials=GLASM, color=GLAS, opacity=0.6, label=False,
         info='Breiteste Stelle, 60 mm. Zerbricht leicht: Scherben mit Handschuhen aufsammeln.'),
    teil('kolben_unten', 'bulb_glass', 'Glaskolben (unten)', 'Kolben unten', 'cyl',
         x=5, y=5, w=50, z=42, h=18, mass=4, materials=GLASM, color=GLAS, opacity=0.6, label=False,
         info='Der Kolben verjüngt sich zum Hals.'),
    teil('kolben_hals', 'bulb_glass', 'Glaskolben (Hals)', 'Kolbenhals', 'cyl',
         x=14, y=14, w=32, z=22, h=20, mass=3, materials=GLASM, color=GLAS, opacity=0.6, label=False,
         info='Der Hals steckt im Sockel und ist dort mit Kitt eingeklebt.'),
    teil('tellerfuss', 'bulb_glass', 'Tellerfuß mit Quetschung', 'Tellerfuß', 'cyl',
         x=24, y=24, w=12, z=26, h=36, mass=2.5, materials=[['behaelterglas', 90], ['nickel', 10]],
         info='Glasröhrchen, mit dem Kolben verschmolzen. In der flachen Quetschung sind die Drähte luftdicht eingeschmolzen.',
         color='#DCE8EC', opacity=0.75, marks=[mark('box', 1, 4.5, 10, 3, 1, '#C7D6DC')]),
    teil('wendel', 'bulb_filament', 'Glühwendel (Wolfram)', 'Glühwendel', 'box',
         x=21, y=29.4, w=18, d=1.2, z=76.5, h=1.2, r=0.5, explode=[55, 0, 22], mass=0.02,
         materials=[['nichrom', 100]],
         info='Doppelt gewendelter Wolframdraht, dünner als ein Haar. Glüht bei etwa 2.500 Grad; nur 5 % '
              'der Energie werden Licht, der Rest Wärme. Ist sie durchgebrannt, ist die Birne kaputt.',
         color='#3D3A36', marks=raster(0.5, 0.1, 9, 1, 1, 1, 1.9, shape='cyl', fill='#F2B33D')),
    teil('haltedraehte', 'bulb_filament', 'Haltedrähte (Molybdän)', 'Haltedrähte', 'box',
         x=19, y=29.5, w=22, d=1, z=64, h=12, r=0.3, explode=[55, 0, 12], mass=0.1,
         materials=[['nickel', 100]],
         info='Feine Molybdänhaken im Glasknopf halten die Wendel, damit sie nicht durchhängt.',
         color='#8D949A', marks=raster(0.5, 0.1, 4, 1, 0.8, 0.8, 6.8, fill='#5A6268')),
    teil('zuleitungen', 'bulb_filament', 'Zuleitungsdrähte', 'Zuleitungen', 'box',
         x=25, y=29.5, w=10, d=1, z=16, h=60, r=0.3, explode=[55, 0, 0], mass=0.3,
         materials=[['kupfer', 60], ['nickel', 40]],
         info='Kupfer- und Nickeldrähte führen den Strom vom Sockel zur Wendel. Einer ist an den Fußkontakt, '
              'einer an das Gewinde gelötet.',
         color='#B87333'),
    teil('kitt', 'bulb_screw_base', 'Sockelkitt', 'Kitt', 'cyl',
         material_id='ceramic', x=15, y=15, w=30, z=20, h=6, mass=1.5, materials=[['keramik', 80], ['phenolharz', 20]],
         info='Harzkitt verklebt Glas und Sockel. Nicht lösen: Die Birne bleibt im Ganzen.',
         color='#C9B98F', marks=[mark('cyl', 7, 7, 16, fill='#B5A57C')]),
    teil('sockel', 'bulb_screw_base', 'Schraubsockel E27', 'Sockel', 'cyl',
         x=16.5, y=16.5, w=27, z=3, h=23, mass=2.5,
         info='Gerolltes Aluminiumblech mit Gewinde, passt in jede normale Lampenfassung.',
         color='#C2C6C9', marks=[mark('cyl', 1.5, 1.5, 24, fill='#B0B5B8'), mark('cyl', 3, 3, 21)]),
    teil('fusskontakt', 'bulb_screw_base', 'Fußkontakt mit Isolierglas', 'Fußkontakt', 'cyl',
         material_id='copper', x=22, y=22, w=16, z=0, h=3, mass=2,
         materials=[['behaelterglas', 70], ['messing', 15], ['lot', 15]],
         info='Schwarzes Glas trennt das Gewinde vom Lötkontakt in der Mitte. Hier fließt der Strom hinein.',
         color='#2A2B2D', marks=[mark('cyl', 5, 5, 6, fill='#C9CDD0')]),
]

explodiere(teile, abstand=12, nach_liste=True,
           gruppen=[['kolben_kuppe', 'kolben_oben', 'kolben_mitte', 'kolben_unten', 'kolben_hals']])
skaliere_masse(teile, oid='incandescent_bulb', stellen=2)
schreibe('incandescent_bulb', teile)
