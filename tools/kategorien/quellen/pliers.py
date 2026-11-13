"""3D-Modell: pliers. Erzeugt tools/kategorien/modelle/pliers.json.

Kombizange 180 mm, geschlossen flach auf dem Tisch, Backen hinten (y 0), Griffe vorn. Zwei geschmiedete Stahlhälften
überlappen im Gelenk und sind mit einem Niet verbunden; jede Hälfte besteht aus Backe, Gelenkplatte und Schenkel
(gemeinsam bewegt) und kreuzt im Gelenk. Explodiert: untere Hälfte bleibt, obere Hälfte und Niet schweben darüber,
die Griffhüllen werden seitlich abgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

STAHL = '#5E666C'
BLANK = '#AEB5BA'
ROT = '#C8322B'
GELB = '#E9B92D'
A = ['spitze_links', 'backe_links', 'gelenk_oben', 'schenkel_rechts']
B = ['spitze_rechts', 'backe_rechts', 'gelenk_unten', 'schenkel_links']

teile = [
    teil('niet', 'steel_pliers_jaws', 'Gelenkniet', 'Niet', 'cyl',
         x=25, y=59, w=10, z=14, h=1, explode=[0, 0, 60], mass=2,
         info='Hält beide Hälften zusammen und ist die Drehachse. Ist vernietet und lässt sich nicht lösen.',
         color='#8C949A', marks=[mark('cyl', 2, 2, 6, fill='#A9B0B5')]),
    teil('niet_schaft', 'steel_pliers_jaws', 'Nietschaft', 'Niet', 'cyl',
         x=26, y=60, w=8, z=1.5, h=12, explode=[0, 0, 60], mass=4, label=False,
         info='Schaft des Niets, unten breitgeschlagen.', color='#8C949A'),
    teil('spitze_links', 'steel_pliers_jaws', 'Backenspitze der oberen Hälfte', 'Spitze A', 'box',
         x=22, y=0, w=8, d=20, z=3, h=9, r=2, mass=6, label=False,
         info='Schmale Spitze zum Greifen kleiner Teile.',
         color=STAHL, marks=raster(3.5, 3, 1, 4, 3.5, 2, 0, 4, r=0.5, fill=BLANK)),
    teil('spitze_rechts', 'steel_pliers_jaws', 'Backenspitze der unteren Hälfte', 'Spitze B', 'box',
         x=30, y=0, w=8, d=20, z=3, h=9, r=2, mass=6, label=False,
         info='Schmale Spitze zum Greifen kleiner Teile.',
         color=STAHL, marks=raster(0.5, 3, 1, 4, 3.5, 2, 0, 4, r=0.5, fill=BLANK)),
    teil('backe_links', 'steel_pliers_jaws', 'Backe der oberen Hälfte', 'Backe A', 'box',
         x=19, y=20, w=11, d=30, z=1.5, h=12, r=2, mass=16,
         info='Gehärteter Chrom-Vanadium-Stahl mit Riffelung zum Greifen und Schneide zum Drahtschneiden.',
         color=STAHL, marks=raster(7, 2, 1, 3, 3.5, 2, 0, 4, r=0.5, fill=BLANK) + [mark('cyl', 5, 13, 6, 4, fill='#3F464B'), mark('box', 9, 20, 2, 9, 0.5, BLANK)]),
    teil('gelenk_oben', 'steel_pliers_jaws', 'Gelenk der oberen Hälfte', 'Gelenk A', 'box',
         x=16, y=50, w=28, d=28, z=7.5, h=6.5, r=10, mass=24,
         info='Am Gelenk ist jede Hälfte auf halbe Dicke abgeflacht, so liegen beide Hälften übereinander.',
         color=STAHL, label=False, marks=[mark('cyl', 10, 10, 8, fill=BLANK)]),
    teil('schenkel_rechts', 'steel_pliers_jaws', 'Schenkel der oberen Hälfte', 'Schenkel A', 'box',
         x=38, y=78, w=10, d=97, z=3, h=9, r=3, mass=34,
         info='Die Hälfte kreuzt im Gelenk: Die linke Backe gehört zum rechten Griff.',
         color=STAHL, label=False),
    teil('backe_rechts', 'steel_pliers_jaws', 'Backe der unteren Hälfte', 'Backe B', 'box',
         x=30, y=20, w=11, d=30, z=1.5, h=12, r=2, mass=16,
         info='Gegenstück mit Riffelung. Der Stahl ist wertvoller Schrott für den Wertstoffhof.',
         color=STAHL, marks=raster(0.5, 2, 1, 3, 3.5, 2, 0, 4, r=0.5, fill=BLANK) + [mark('cyl', 0, 13, 6, 4, fill='#3F464B'), mark('box', 0, 20, 2, 9, 0.5, BLANK)]),
    teil('gelenk_unten', 'steel_pliers_jaws', 'Gelenk der unteren Hälfte', 'Gelenk B', 'box',
         x=16, y=50, w=28, d=28, z=1, h=6.5, r=10, mass=24,
         info='Untere Gelenkplatte mit Bohrung für den Niet.', color=STAHL, label=False,
         marks=[mark('cyl', 10, 10, 8, fill=BLANK)]),
    teil('schenkel_links', 'steel_pliers_jaws', 'Schenkel der unteren Hälfte', 'Schenkel B', 'box',
         x=12, y=78, w=10, d=97, z=3, h=9, r=3, mass=34,
         info='Stahlkern des linken Griffs, unter der Kunststoffhülle.', color=STAHL, label=False),
    teil('griff_links', 'plastic_handles', 'Griffhülle links', 'Griff links', 'box',
         x=4, y=86, w=24, d=94, z=0, h=15, r=10, explode=[-42, 0, 0], mass=16, materials=[['pp', 60], ['tpe', 40]],
         info='Zwei-Komponenten-Griff aus PP und weichem TPE. Abziehen oder aufschneiden, dann Kunststoff '
              'in den Restmüll und Stahl zum Altmetall.',
         color=ROT, marks=[mark('box', 4, 12, 16, 70, 7, GELB)]),
    teil('griff_rechts', 'plastic_handles', 'Griffhülle rechts', 'Griff rechts', 'box',
         x=32, y=86, w=24, d=94, z=0, h=15, r=10, explode=[42, 0, 0], mass=16, materials=[['pp', 60], ['tpe', 40]],
         info='Isoliert nicht gegen Strom, wenn kein VDE-Zeichen draufsteht.',
         color=ROT, marks=[mark('box', 4, 12, 16, 70, 7, GELB)]),
]

for p in teile:
    if p['id'] in A:
        p['explode'] = [0, 0, 30]
    elif p['id'] in B:
        p['explode'] = [0, 0, 0]
skaliere_masse(teile, oid='pliers')
schreibe('pliers', teile)
