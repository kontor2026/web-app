"""3D-Modell: felt_tip_marker. Erzeugt tools/kategorien/modelle/felt_tip_marker.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Filzstift mit Kappe, aufrecht (laut CSV 15 × 15 × 140 mm), Spitze oben. Schaft Ø 12 mm, Kappe mit Clip.
# Unten Endstopfen, darüber Schaft und Spitzenhalter; Fasertank und Faserspitze werden seitlich (dx > 0) herausgezogen,
# Kappe und Spitzenhalter schweben über dem Schaft.
FARBE = '#C8423A'
WEISS = '#F3F1EC'
TANK = 24

teile = [
    teil('kappe', 'pen_cap', 'Kappe', 'Kappe', 'cyl',
         x=1, y=1, w=13, z=84, h=56, mass=2.4,
         info='Hält die Spitze feucht. Immer gleich wieder aufstecken, sonst trocknet der Stift aus. Das Luftloch oben ist Absicht.',
         color=FARBE, marks=[mark('cyl', 5, 5, 3, fill='#8E2E28')]),
    teil('clip', 'pen_cap', 'Clip', 'Clip', 'box',
         x=14, y=6, w=1.5, d=3, z=100, h=36, r=0.5, mass=0.3,
         info='An die Kappe angespritzter Kunststoffclip, gleiches Material wie die Kappe.',
         color=FARBE),
    teil('innenkappe', 'pen_cap', 'Innenkappe', 'Innenkappe', 'cyl',
         x=3.5, y=3.5, w=8, z=100, h=24, mass=0.3,
         info='Kleiner Becher in der Kappe, der sich luftdicht über die Spitze schiebt. Er sorgt dafür, dass der '
              'Stift auch nach Wochen nicht austrocknet.',
         color='#E9E6DF', marks=[mark('cyl', 1.5, 1.5, 5, fill='#C9CDD0')]),
    teil('spitze', 'marker_nib', 'Faserspitze', 'Spitze', 'cyl',
         x=5.5, y=5.5, w=4, z=96, h=22, explode=[TANK, 0, 10], mass=0.3,
         info='Gepresste Polyesterfasern, durch die die Tinte wie in einem Docht nach vorne läuft. Mit einer Zange herausziehen.',
         color=FARBE, marks=[mark('cyl', 1, 1, 2, fill='#8E2E28')]),
    teil('spitzenhalter', 'pen_barrel', 'Spitzenhalter', 'Spitzenhalter', 'cyl',
         x=2, y=2, w=11, z=90, h=10, mass=0.8,
         info='Konisches Vorderteil, in dem die Spitze steckt. Es ist in den Schaft gedrückt.',
         color=WEISS, marks=[mark('cyl', 3.5, 3.5, 4, fill='#C9CDD0')]),
    teil('tank', 'marker_ink_reservoir', 'Fasertank mit Tinte', 'Tank', 'cyl',
         x=3, y=3, w=9, z=8, h=82, explode=[TANK, 0, 0], mass=2.2, materials=[['polyester', 75], ['pp', 15], ['druck', 10]],
         info='Polyesterwatte in einer Folienhülle, mit wasserbasierter Tinte getränkt. Viele Marker lassen sich nachfüllen, '
              'das spart den ganzen Stift.',
         color='#E8C9C6', marks=[mark('cyl', 1.5, 1.5, 6, fill=FARBE)]),
    teil('schaft', 'pen_barrel', 'Schaft', 'Schaft', 'cyl',
         x=1.5, y=1.5, w=12, z=4, h=86, mass=4.5,
         info='Hülse aus Polypropylen, bedruckt. Leer gehört der Stift in den Restmüll, weil die Teile zu klein zum Sortieren sind.',
         color=WEISS, marks=[mark('cyl', 2, 2, 8, fill='#C9CDD0')]),
    teil('endstopfen', 'pen_barrel', 'Endstopfen', 'Endstopfen', 'cyl',
         x=2, y=2, w=11, z=0, h=4, mass=0.6,
         info='Verschließt den Schaft hinten. Herausziehen, dann gleitet der Tank heraus.',
         color=FARBE),
]

explodiere(teile, abstand=10, nach_liste=True, gruppen=[['kappe', 'clip']])
skaliere_masse(teile, oid='felt_tip_marker', stellen=2)
schreibe('felt_tip_marker', teile)
