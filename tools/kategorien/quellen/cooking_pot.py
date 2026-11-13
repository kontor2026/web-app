"""3D-Modell: cooking_pot. Erzeugt tools/kategorien/modelle/cooking_pot.json.

Typischer Edelstahl-Kochtopf (Ø 18 cm, ca. 2,5 l) mit Kapselboden (Aluminiumkern in Stahlkappe), Glasdeckel mit
Edelstahlrand, Dampfloch und Kunststoffknauf, zwei angenieteten Seitengriffen. Deckelteile schweben über dem Topf,
der Kapselboden liegt unten; Griffe und Nieten werden seitlich herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

STAHL = '#C9CED2'
GRIFF = '#2E3338'
GLAS = '#D6E4E6'

teile = [
    teil('knauf', 'pot_lid_glass', 'Deckelknauf', 'Knauf', 'cyl', material_id='phenolic_resin',
         x=90, y=90, w=40, z=120, h=10, mass=25,
         info='Hitzefester Kunststoff (Bakelit). Von unten mit einer Schraube gehalten: Schraube lösen, dann kann man '
              'Knauf, Glas und Metall getrennt entsorgen.',
         color=GRIFF, marks=[mark('cyl', 6, 6, 28, fill='#3E444A')]),
    teil('glasdeckel', 'pot_lid_glass', 'Glasdeckel', 'Glasdeckel', 'cyl',
         x=18, y=18, w=184, z=113, h=7, mass=330,
         info='Gehärtetes, hitzefestes Glas. Es schmilzt anders als Flaschenglas und gehört deshalb nicht in den '
              'Glascontainer, sondern in den Restmüll oder zum Wertstoffhof.',
         color=GLAS, opacity=0.65,
         marks=[mark('cyl', 72, 72, 40, fill='#C4D4D6'), mark('cyl', 150, 89, 6, fill='#9AA8AA')]),
    teil('deckelrand', 'pot_lid_glass', 'Edelstahlrand mit Dampfloch', 'Deckelrand', 'cyl', material_id='steel',
         x=17, y=17, w=186, z=111, h=3, mass=40,
         info='Schmaler Edelstahlring um das Glas. Die Kerbe darin ist das Dampfloch, damit der Deckel nicht klappert.',
         color=STAHL, marks=[mark('cyl', 4, 4, 178, fill='#D6E4E6'), mark('box', 176, 89, 8, 8, 2, fill='#5A6268')]),
    teil('knaufschraube', 'pot_lid_glass', 'Knaufschraube', 'Schraube', 'cyl', material_id='steel',
         x=107, y=107, w=6, z=110, h=14, mass=3,
         info='Edelstahlschraube mit Unterlegscheibe, steckt von unten durch das Loch im Glas in den Knauf.',
         color='#9AA2A6', marks=[mark('box', 0.5, 2.5, 5, 1, fill='#5A6268')]),
    teil('koerper', 'stainless_steel_body', 'Topfkörper', 'Topfkörper', 'cyl',
         x=20, y=20, w=180, z=6, h=106, mass=650,
         info='Tiefgezogener Edelstahl mit Chrom und Nickel. Ohne Griffe und Deckel ist er reiner Metallschrott für den '
              'Wertstoffhof.',
         color=STAHL, marks=[mark('cyl', 2, 2, 176, fill='#B5BBC0'), mark('cyl', 30, 30, 120, fill='#A9B0B5')]),
    teil('alukern', 'stainless_steel_body', 'Aluminiumkern', 'Alu-Kern', 'cyl', material_id='aluminium',
         x=32, y=32, w=156, z=1, h=5, mass=150,
         info='Dicke Aluminiumscheibe im Kapselboden. Aluminium leitet Wärme sehr gut und verteilt sie gleichmäßig. '
              'Sie ist fest eingepresst und lässt sich zu Hause nicht herauslösen.',
         color='#D5D9DC', marks=[mark('cyl', 8, 8, 140, fill='#C8CDD1')]),
    teil('kapsel', 'stainless_steel_body', 'Bodenkapsel (magnetischer Stahl)', 'Bodenkapsel', 'cyl', material_id='steel',
         x=30, y=30, w=160, z=0, h=6, mass=130,
         info='Kappe aus magnetischem Edelstahl, die den Aluminiumkern umschließt. Sie macht den Topf '
              'induktionstauglich: Ein Magnet bleibt hier haften.',
         color='#B5BBC0', marks=[mark('cyl', 20, 20, 120, fill='#A9B0B5')]),
    teil('griff_links', 'plastic_handle', 'Seitengriff links', 'Griff links', 'box', material_id='phenolic_resin',
         x=0, y=88, w=24, d=44, z=88, h=16, r=8, explode=[-70, 0, 0], mass=40,
         info='Bakelit-Griff auf einem Stahlwinkel, mit zwei Nieten am Topf befestigt. Nieten mit einem Metallbohrer '
              'aufbohren, dann Griff (Restmüll) und Topf (Metall) trennen.',
         color=GRIFF, marks=[mark('box', 4, 6, 12, 32, 5, fill='#3E444A')]),
    teil('griff_rechts', 'plastic_handle', 'Seitengriff rechts', 'Griff rechts', 'box', material_id='phenolic_resin',
         x=196, y=88, w=24, d=44, z=88, h=16, r=8, explode=[70, 0, 0], mass=40,
         info='Gegenstück zum linken Griff. Bakelit wird beim Erhitzen nicht weich und kann nicht recycelt werden.',
         color=GRIFF, marks=[mark('box', 8, 6, 12, 32, 5, fill='#3E444A')]),
    teil('nieten_links', 'plastic_handle', 'Nieten links (2 Stück)', 'Nieten', 'box', material_id='steel',
         x=17, y=96, w=6, d=28, z=93, h=6, r=2, explode=[-35, 0, 0], mass=5,
         info='Zwei Edelstahlnieten, die den Griffwinkel durch die Topfwand halten. Innen sieht man ihre flachen Köpfe.',
         color='#9AA2A6', marks=[mark('cyl', 1, 1, 4, fill='#5A6268'), mark('cyl', 1, 23, 4, fill='#5A6268')]),
    teil('nieten_rechts', 'plastic_handle', 'Nieten rechts (2 Stück)', 'Nieten', 'box', material_id='steel',
         x=197, y=96, w=6, d=28, z=93, h=6, r=2, explode=[35, 0, 0], mass=5, label=False,
         info='Zwei Edelstahlnieten für den rechten Griff.',
         color='#9AA2A6', marks=[mark('cyl', 1, 1, 4, fill='#5A6268'), mark('cyl', 1, 23, 4, fill='#5A6268')]),
]
explodiere(teile, abstand=22, nach_liste=True)
skaliere_masse(teile, oid='cooking_pot')
schreibe('cooking_pot', teile)
