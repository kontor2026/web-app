"""3D-Modell: screwdriver. Erzeugt tools/kategorien/modelle/screwdriver.json.

Schlitz-Schraubendreher 6,5 mm, flach auf dem Tisch: Griff hinten (y 0), Klinge vorn (y groß). Griff aus PP mit
TPE-Weichzone, Rundschaft aus Chrom-Vanadium-Stahl, im Griff mit angestauchten Flügeln gegen Verdrehen gesichert.
Explodiert: Griffteile bleiben liegen, Schaft mit Flügeln und Klinge schwebt als Einheit darüber.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

ROT = '#C8322B'
GELB = '#F1C232'
STAHL = '#B5BCC1'

teile = [
    teil('klinge', 'steel_shaft', 'Schlitzklinge', 'Klinge', 'box',
         x=11.75, y=203, w=6.5, d=17, z=14, h=2, r=0.3, mass=3,
         info='Flach geschmiedete, gehärtete Spitze, schwarz brüniert. Sie greift in den Schlitz der Schraube.',
         color='#33383C'),
    teil('schaft', 'steel_shaft', 'Rundschaft', 'Schaft', 'box',
         x=12, y=60, w=6, d=143, z=12, h=6, r=3, mass=36,
         info='Chrom-Vanadium-Stahl, verchromt. Ist fest in den Griff gespritzt: Zum Trennen den Griff '
              'mit einer Säge aufschneiden. Der Stahl gehört zum Altmetall.',
         color=STAHL, marks=[mark('box', 1.5, 50, 3, 80, 1.5, '#DCE1E4')]),
    teil('fluegel', 'steel_shaft', 'Verdrehsicherung (Flügel)', 'Flügel', 'box',
         x=9, y=46, w=12, d=14, z=14, h=2, r=1, mass=3,
         info='Angestauchte Flügel am Schaftende. Sie verhindern, dass sich der Schaft im Griff dreht.',
         color=STAHL),
    teil('griff_kappe', 'plastic_handle', 'Griffkappe', 'Kappe', 'box',
         x=1, y=0, w=28, d=18, z=1, h=28, r=12, mass=8,
         info='Hartes Polypropylen mit Aufhängeloch. Der Griff ist in einem Stück um den Schaft gespritzt.',
         color=ROT, marks=[mark('cyl', 10, 5, 8, fill='#7E1E19')]),
    teil('griff_weich', 'plastic_handle', 'Weichgriff', 'Weichgriff', 'box',
         material_id='rubber', x=0, y=18, w=30, d=72, z=0, h=30, r=14, mass=22, materials=[['tpe', 70], ['pp', 30]],
         info='Weiche TPE-Zone auf dem harten Kern, damit die Hand nicht abrutscht. Lässt sich nicht vom Kern trennen.',
         color=GELB, marks=raster(13, 4, 1, 8, 4, 6, 0, 8.5, r=2, fill='#C99A1E')),
    teil('griff_hals', 'plastic_handle', 'Griffhals', 'Griffhals', 'box',
         x=3, y=90, w=24, d=15, z=3, h=24, r=10, mass=6,
         info='Verjüngter Übergang zum Schaft, hier tritt der Stahl aus dem Griff.',
         color=ROT, marks=[mark('cyl', 9, 4, 6, fill='#7E1E19')]),
]

explodiere(teile, abstand=18, gruppen=[['klinge', 'schaft', 'fluegel']])
skaliere_masse(teile, oid='screwdriver')
schreibe('screwdriver', teile)
