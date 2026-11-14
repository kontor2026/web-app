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

# Kolben (A60) aus Scheiben: (z, h, Durchmesser), oben zuerst
KOLBEN = [(100, 5, 30), (94, 6, 46), (84, 10, 56), (58, 26, 60), (48, 10, 54), (38, 10, 44), (22, 16, 31)]
KOLBEN_INFO = ('Dünnes Kalk-Natron-Glas, nur etwa 0,5 mm dick. Innen Vakuum oder Edelgas, damit die Wendel '
               'nicht verbrennt. Glühbirnen gehören in den Restmüll, nicht ins Altglas.')
# Gewinde E27 als abwechselnd breite und schmale Ringe (z, h, Durchmesser)
GEWINDE = [(21, 5, 27), (18, 3, 25), (14, 4, 27), (11, 3, 25), (7, 4, 27), (4, 3, 25)]

kolben = [teil(f'kolben_{i}', 'bulb_glass', 'Glaskolben', 'Kolben', 'cyl',
               x=30 - w / 2, y=30 - w / 2, w=w, z=z, h=h, mass=round(w * h / 100, 2), materials=GLASM,
               color=GLAS, opacity=0.55, label=None if i == 0 else False,
               info=KOLBEN_INFO if i == 0 else 'Teil des Glaskolbens. Zerbricht leicht: Scherben mit Handschuhen aufsammeln.')
          for i, (z, h, w) in enumerate(KOLBEN)]
sockel = [teil(f'sockel_{i}', 'bulb_screw_base', 'Schraubsockel E27', 'Sockel', 'cyl',
               x=30 - w / 2, y=30 - w / 2, w=w, z=z, h=h, mass=0.45, color='#C2C6C9' if w > 26 else '#A9AFB3',
               label=None if i == 0 else False,
               marks=[mark('cyl', 1.5, 1.5, 24, fill='#B0B5B8'), mark('cyl', 3, 3, 21)] if i == 0 else None,
               info='Gerolltes Aluminiumblech mit Gewinde, passt in jede normale Lampenfassung.' if i == 0
               else 'Gewindegang des Sockels.')
          for i, (z, h, w) in enumerate(GEWINDE)]
draht = dict(d=0.8, r=0.3, color='#B87333', materials=[['kupfer', 60], ['nickel', 40]])
halte = dict(d=0.6, r=0.2, color='#8D949A', materials=[['nickel', 100]])

teile = kolben + [
    teil('tellerfuss', 'bulb_glass', 'Tellerfuß mit Quetschung', 'Tellerfuß', 'cyl',
         x=24, y=24, w=12, z=26, h=36, mass=2.5, materials=[['behaelterglas', 90], ['nickel', 10]],
         info='Glasröhrchen, mit dem Kolben verschmolzen. In der flachen Quetschung sind die Drähte luftdicht eingeschmolzen.',
         color='#DCE8EC', opacity=0.75, marks=[mark('box', 1, 4.5, 10, 3, 1, '#C7D6DC'), mark('cyl', 4.5, 4.5, 3, fill='#C7D6DC')]),
    teil('wendel', 'bulb_filament', 'Glühwendel (Wolfram)', 'Glühwendel', 'box',
         x=21, y=29.4, w=18, d=1.2, z=76.5, h=1.2, r=0.5, explode=[55, 0, 30], mass=0.02,
         materials=[['nichrom', 100]],
         info='Doppelt gewendelter Wolframdraht, dünner als ein Haar. Glüht bei etwa 2.500 Grad; nur 5 % '
              'der Energie werden Licht, der Rest Wärme. Ist sie durchgebrannt, ist die Birne kaputt.',
         color='#3D3A36', marks=raster(0.5, 0.1, 9, 1, 1, 1, 1.9, shape='cyl', fill='#F2B33D')),
    teil('haltedraht_1', 'bulb_filament', 'Haltedrähte (Molybdän)', 'Haltedrähte', 'box',
         x=26, y=29.7, w=0.6, z=62, h=14.5, explode=[55, 0, 15], mass=0.05,
         info='Feine Molybdänhaken im Glasknopf halten die Wendel, damit sie nicht durchhängt.', **halte),
    teil('haltedraht_2', 'bulb_filament', 'Haltedraht', 'Haltedraht', 'box', label=False,
         x=33.4, y=29.7, w=0.6, z=62, h=14.5, explode=[55, 0, 15], mass=0.05, info='Zweiter Haltedraht.', **halte),
    teil('zuleitung_1', 'bulb_filament', 'Zuleitungsdrähte', 'Zuleitungen', 'box',
         x=21, y=29.6, w=0.8, z=28, h=48.5, explode=[55, 0, 0], mass=0.15,
         info='Kupfer- und Nickeldrähte führen den Strom vom Sockel zur Wendel. Einer ist an den Fußkontakt, '
              'einer an das Gewinde gelötet.', **draht),
    teil('zuleitung_2', 'bulb_filament', 'Zuleitungsdraht', 'Zuleitung', 'box', label=False,
         x=38.2, y=29.6, w=0.8, z=28, h=48.5, explode=[55, 0, 0], mass=0.15,
         info='Zweiter Zuleitungsdraht, im Sockel mit einer dünnen Sicherung.', **draht),
    teil('kitt', 'bulb_screw_base', 'Sockelkitt', 'Kitt', 'cyl',
         material_id='ceramic', x=15.5, y=15.5, w=29, z=26, h=2, mass=1.5, materials=[['keramik', 80], ['phenolharz', 20]],
         info='Harzkitt verklebt Glas und Sockel. Nicht lösen: Die Birne bleibt im Ganzen.',
         color='#C9B98F', marks=[mark('cyl', 7, 7, 15, fill='#B5A57C')]),
] + sockel + [
    teil('fusskontakt', 'bulb_screw_base', 'Fußkontakt mit Isolierglas', 'Fußkontakt', 'cyl',
         material_id='copper', x=20, y=20, w=20, z=0, h=4, mass=2,
         materials=[['behaelterglas', 70], ['messing', 15], ['lot', 15]],
         info='Schwarzes Glas trennt das Gewinde vom Lötkontakt in der Mitte. Hier fließt der Strom hinein.',
         color='#2A2B2D', marks=[mark('cyl', 6, 6, 8, fill='#C9CDD0'), mark('cyl', 8, 8, 4, fill='#9EA4A8')]),
]

explodiere(teile, abstand=12, nach_liste=True,
           gruppen=[[p['id'] for p in kolben], [p['id'] for p in sockel]])
skaliere_masse(teile, oid='incandescent_bulb', stellen=2)
schreibe('incandescent_bulb', teile)
