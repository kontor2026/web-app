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
    teil('mine', 'lipstick_bullet', 'Lippenstiftmine', 'Mine', 'cyl',
         x=4, y=4, w=12, z=42, h=30, mass=3.8, materials=[['wachs', 100]],
         info='Wachs, Öle und Farbpigmente, schräg angeschnitten. Reste mit einem Wattestäbchen auskratzen und in den '
              'Restmüll geben.',
         color='#B3263E', marks=[mark('cyl', 1, 1, 10, 7, fill='#C93A52')]),
    teil('becher', 'lipstick_case', 'Minenbecher', 'Becher', 'cyl',
         x=3.5, y=3.5, w=13, z=34, h=12, mass=0.8,
         info='Kleiner Becher, in dem die Mine steckt. Zwei Zapfen greifen in die Spirale.',
         color=GOLD, marks=[mark('cyl', 0.5, 0.5, 12, fill='#B3263E')]),
    teil('spiralhuelse', 'lipstick_case', 'Spiralhülse (Drehmechanik)', 'Spiralhülse', 'cyl',
         x=3, y=3, w=14, z=8, h=40, mass=3.5,
         info='Innenrohr mit Längsschlitz und Spirale: Dreht man das Unterteil, schraubt sich der Becher nach oben.',
         color='#D8D6CE', marks=[mark('cyl', 1, 1, 12, fill='#B8B4AA')]),
    teil('unterteil', 'lipstick_case', 'Unterteil', 'Unterteil', 'cyl',
         x=0.5, y=0.5, w=19, z=0, h=40, mass=7, materials=[['pp', 90], ['alu', 10]],
         info='Drehbarer Fuß der Hülse. Kunststoff mit dünner Metallschicht, Gelbe Tonne. Echte Metallhülsen '
              'gehören auch hinein.',
         color=GOLD, marks=[mark('cyl', 2, 2, 15, fill='#B8963A')]),
]
explodiere(teile, abstand=10, nach_liste=True)
skaliere_masse(teile, oid='lipstick')
schreibe('lipstick', teile)
