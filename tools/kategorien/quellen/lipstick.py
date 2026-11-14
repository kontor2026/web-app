"""3D-Modell: lipstick. Erzeugt tools/kategorien/modelle/lipstick.json.

Typischer Lippenstift (Ø 20 mm, 80 mm lang, geschlossen): Kappe, Lippenstiftmine, Becher, Spiralhülse
(Drehmechanik) und Unterteil. Die Kappe wird seitlich abgezogen, der Mechanismus stapelt nach oben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

GOLD = '#C9A646'
teile = [
    teil('kappe', 'lipstick_case', 'Kappe', 'Kappe', 'cyl',
         x=0, y=0, w=20, z=38, h=42, explode=[35, 0, 0], mass=5, materials=[['pp', 90], ['alu', 10]],
         info='Aufgesteckte Kappe, oft aus PP mit Metallic-Beschichtung. Kommt in die Gelbe Tonne.',
         color='#8E1B2C', marks=[mark('cyl', 2, 2, 16, fill='#A3263A')]),
    *[teil(f'spitze{i}', 'lipstick_bullet', 'Schräge Spitze der Mine', 'Mine', 'cyl',
           x=4, y=4 + (12 - dd), w=12, d=dd, z=66 + 2 * i, h=2, mass=0.15, materials=[['wachs', 100]], label=False,
           color='#B3263E', info='Die Spitze ist schräg angeschnitten, damit man die Lippenränder genau trifft.',
           marks=[mark('cyl', 0.8, 0.6, 10.4, dd - 1.2, fill='#C93A52')] if i == 3 else None)
      for i, dd in reversed(list(enumerate([10.5, 8.5, 6.5, 4.5])))],
    teil('mine', 'lipstick_bullet', 'Lippenstiftmine', 'Mine', 'cyl',
         x=4, y=4, w=12, z=42, h=24, mass=3.2, materials=[['wachs', 100]],
         info='Wachs, Öle und Farbpigmente. Reste mit einem Wattestäbchen auskratzen und in den Restmüll geben.',
         color='#B3263E', marks=[mark('cyl', 0.8, 0.8, 10.4, fill='#C93A52')]),
    teil('becher', 'lipstick_case', 'Minenbecher', 'Becher', 'cyl',
         x=3.5, y=3.5, w=13, z=34, h=12, mass=0.8,
         info='Kleiner Becher, in dem die Mine steckt. Zwei Zapfen greifen in die Spirale.',
         color=GOLD, marks=[mark('cyl', 0.5, 0.5, 12, fill='#B3263E'), mark('box', 0, 5.5, 1.5, 2, 0.5, '#8F7530'),
                           mark('box', 11.5, 5.5, 1.5, 2, 0.5, '#8F7530')], sortBias=-15),
    teil('spiralhuelse', 'lipstick_case', 'Spiralhülse (Drehmechanik)', 'Spiralhülse', 'cyl',
         x=3, y=3, w=14, z=8, h=40, mass=3.5,
         info='Innenrohr mit Längsschlitz und Spirale: Dreht man das Unterteil, schraubt sich der Becher nach oben.',
         color='#D8D6CE', wand=1, marks=[mark('cyl', 1, 1, 12, fill='#B8B4AA', zeichnung=True)], sortBias=-15),
    teil('feder', 'lipstick_case', 'Klemmfeder', 'Klemmfeder', 'cyl',
         x=2.5, y=2.5, w=15, z=40, h=3, mass=0.4, material_id='steel', materials=[['stahl', 100]], color='#9EA3A8',
         sortBias=-5,
         info='Kleiner Federring aus Stahl, der die Kappe festklemmt. Er ist magnetisch und wird in der Sortieranlage '
              'mit dem Magneten aussortiert.',
         wand=1.2, boden=0,
         marks=[mark('cyl', 1.2, 1.2, 12.6, fill='#D8D6CE', zeichnung=True), mark('box', 6.5, 0, 2, 1.5, 0, '#6E7378')]),
    teil('zierring', 'lipstick_case', 'Zierring', 'Zierring', 'cyl',
         x=0.3, y=0.3, w=19.4, z=36, h=4, mass=0.6, material_id='aluminium', materials=[['alu', 100]],
         color='#F0DC9A', wand=1.5, boden=0,
         info='Glänzender Ring aus Aluminium als Schmuck und Anschlag für die Kappe. Er ist aufgepresst.',
         marks=[mark('cyl', 1.5, 1.5, 16.4, fill='#C9A646', zeichnung=True)]),
    teil('unterteil', 'lipstick_case', 'Unterteil', 'Unterteil', 'cyl',
         x=0.5, y=0.5, w=19, z=0, h=36, mass=6.5, materials=[['pp', 90], ['alu', 10]],
         info='Drehbarer Fuß der Hülse. Kunststoff mit dünner Metallschicht, Gelbe Tonne. Echte Metallhülsen '
              'gehören auch hinein.',
         color='#D4B04E', wand=2, marks=[mark('cyl', 2, 2, 15, fill='#B8963A', zeichnung=True)]),
]
explodiere(teile, abstand=10, nach_liste=True, gruppen=[['mine', 'spitze0', 'spitze1', 'spitze2', 'spitze3']])
skaliere_masse(teile, oid='lipstick')
schreibe('lipstick', teile)
