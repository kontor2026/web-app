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
A = ['backe_links', 'gelenk_oben', 'schenkel_rechts']
B = ['backe_rechts', 'gelenk_unten', 'schenkel_links']

teile = [
    teil('niet', 'steel_pliers_jaws', 'Gelenkniet', 'Niet', 'cyl',
         x=26, y=60, w=8, z=0, h=15, mass=6,
         info='Hält beide Hälften zusammen und ist die Drehachse. Ist vernietet und lässt sich nicht lösen.',
         color='#8C949A', marks=[mark('cyl', 2, 2, 4, fill='#6C747A')]),
    teil('backe_links', 'steel_pliers_jaws', 'Backe der oberen Hälfte', 'Backe A', 'box',
         x=19, y=0, w=11, d=50, z=1.5, h=12, r=2, mass=22,
         info='Gehärteter Chrom-Vanadium-Stahl mit Riffelung zum Greifen und Schneide zum Drahtschneiden.',
         color=STAHL, marks=raster(7, 3, 1, 6, 3.5, 2, 0, 4, r=0.5, fill=BLANK) + [mark('box', 9, 30, 2, 16, 0.5, BLANK)]),
    teil('gelenk_oben', 'steel_pliers_jaws', 'Gelenk der oberen Hälfte', 'Gelenk A', 'box',
         x=16, y=50, w=28, d=28, z=7.5, h=6.5, r=10, mass=24,
         info='Am Gelenk ist jede Hälfte auf halbe Dicke abgeflacht, so liegen beide Hälften übereinander.',
         color=STAHL, label=False, marks=[mark('cyl', 10, 10, 8, fill=BLANK)]),
    teil('schenkel_rechts', 'steel_pliers_jaws', 'Schenkel der oberen Hälfte', 'Schenkel A', 'box',
         x=38, y=78, w=10, d=97, z=3, h=9, r=3, mass=34,
         info='Die Hälfte kreuzt im Gelenk: Die linke Backe gehört zum rechten Griff.',
         color=STAHL, label=False),
    teil('backe_rechts', 'steel_pliers_jaws', 'Backe der unteren Hälfte', 'Backe B', 'box',
         x=30, y=0, w=11, d=50, z=1.5, h=12, r=2, mass=22,
         info='Gegenstück mit Riffelung. Der Stahl ist wertvoller Schrott für den Wertstoffhof.',
         color=STAHL, marks=raster(0.5, 3, 1, 6, 3.5, 2, 0, 4, r=0.5, fill=BLANK) + [mark('box', 0, 30, 2, 16, 0.5, BLANK)]),
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

explodiere(teile, abstand=20, nach_liste=True, gruppen=[A, B])
skaliere_masse(teile, oid='pliers')
schreibe('pliers', teile)
