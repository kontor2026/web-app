"""3D-Modell: building_brick. Erzeugt tools/kategorien/modelle/building_brick.json.

Klemmbaustein 2 × 4 (31,8 × 15,8 × 9,6 mm plus 1,7 mm Noppen, Raster 8 mm), aus ABS gespritzt, ein Teil.
Zerlegt in seine Zonen: acht Noppen, Deckplatte, drei Hohlröhren unten in der Mitte und die vier Außenwände.
Explosion: Wände unten, darüber Röhren, Deckplatte und Noppen (Noppen und Röhren jeweils als Gruppe).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

ROT = '#C8302A'
DUNKEL = '#8E1E1A'
B, T, WAND, DECKE, HK = 31.8, 15.8, 1.2, 1.0, 8.6  # HK = Höhe der Wände unter der Deckplatte
NOPPE, ROHR = 4.8, 6.51

noppen = []
for j in range(2):
    for i in range(4):
        n = len(noppen)
        noppen.append(teil(
            f'noppe_{n + 1}', 'abs_brick', 'Noppen (8 Stück)' if n == 0 else f'Noppe {n + 1}', 'Noppen', 'cyl',
            x=round(3.9 + 8 * i - NOPPE / 2, 2), y=round(3.9 + 8 * j - NOPPE / 2, 2), w=NOPPE, z=HK + DECKE, h=1.7,
            mass=0.04, color=ROT, label=None if n == 0 else False,
            info='Die Noppen klemmen in die Röhren und Wände des nächsten Steins. Die Maße stimmen auf '
                 'Hundertstel Millimeter, deshalb halten die Steine so gut.' if n == 0 else 'Weitere Noppe.',
            marks=[mark('cyl', 0.9, 0.9, 3, fill='#B52924')]))

roehren = []
for i in range(3):
    roehren.append(teil(
        f'rohr_{i + 1}', 'abs_brick', 'Hohlröhren (3 Stück)' if i == 0 else f'Röhre {i + 1}', 'Röhren', 'cyl',
        x=round(7.9 + 8 * i - ROHR / 2, 2), y=round(T / 2 - ROHR / 2, 2), w=ROHR, z=0, h=HK, mass=0.12,
        color=ROT, label=None if i == 0 else False,
        info='Röhren an der Unterseite, zwischen die die Noppen eines anderen Steins greifen.' if i == 0
        else 'Weitere Röhre.',
        marks=[mark('cyl', (ROHR - NOPPE) / 2, (ROHR - NOPPE) / 2, NOPPE, fill=DUNKEL)]))

teile = noppen + [
    teil('deckplatte', 'abs_brick', 'Deckplatte', 'Deckplatte', 'box',
         x=0, y=0, w=B, d=T, z=HK, h=DECKE, r=0.2, mass=0.55, color=ROT,
         info='Die geschlossene Oberseite, mit Wänden, Röhren und Noppen in einem Stück gespritzt. ABS hält '
              'Jahrzehnte: Steine weitergeben statt wegwerfen, im Restmüll werden sie verbrannt.'),
] + roehren + [
    teil('waende', 'abs_brick', 'Außenwände', 'Wände', 'box',
         x=0, y=0, w=B, d=T, z=0, h=HK, r=0.2, mass=1.1, color=ROT,
         info='Vier dünne Wände, unten offen. Gemeinsam mit den Röhren klemmen sie die Noppen des Steins darunter.',
         marks=[mark('box', WAND, WAND, B - 2 * WAND, T - 2 * WAND, 0.2, DUNKEL)]),
]

explodiere(teile, abstand=7, gruppen=[[p['id'] for p in noppen], [p['id'] for p in roehren]])
skaliere_masse(teile, oid='building_brick', stellen=3)
schreibe('building_brick', teile)
