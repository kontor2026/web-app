"""3D-Modell: cling_film. Erzeugt tools/kategorien/modelle/cling_film.json.

Typische Haushaltsrolle Frischhaltefolie (30 cm breit, ca. 30 m LDPE-Folie, 40 mm Durchmesser) liegend auf dem
Papphülsenkern. Die runde Rolle ist aus waagrechten Scheiben (Kreissehnen) aufgebaut, der Kern ragt an beiden
Enden 2 mm heraus. Explodiert wird der Kern seitlich herausgezogen, das lose Folienende nach vorne abgehoben.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

FOLIE = '#DDE9EC'
KERN = '#B58C5E'
MITTE_Y, MITTE_Z = 20, 20


def scheiben(z0, z1, n, radius):
    """Waagrechte Scheiben eines liegenden Zylinders: (z, h, Sehnenlänge in y)."""
    h = (z1 - z0) / n
    out = []
    for i in range(n):
        zc = z0 + (i + 0.5) * h
        out.append((round(z0 + i * h, 2), round(h, 2), round(2 * math.sqrt(radius ** 2 - (zc - MITTE_Z) ** 2), 1)))
    return out


teile = []
folie = scheiben(0, 40, 5, 20)
gesamt = sum(d for _, _, d in folie)
for i, (z, h, d) in enumerate(reversed(folie)):
    oben = i == 0
    teile.append(teil(f'folie_{i + 1}', 'ldpe_film', 'Aufgewickelte Folie' if oben else 'Aufgewickelte Folie (Schnitt)',
                      'Folienwickel', 'box', x=2, y=round(MITTE_Y - d / 2, 2), w=296, d=d, z=z, h=h, r=0,
                      explode=[0, 0, 0], mass=round(90 * d / gesamt, 2), materials=[['ldpe', 100]], color=FOLIE,
                      opacity=0.8, label=oben,
                      info='Etwa 30 m hauchdünne LDPE-Folie (0,01 mm), die durch ihre Haftkraft an Schüsseln klebt. '
                           'Saubere Folienreste locker in die Gelbe Tonne, verschmutzte in den Restmüll.',
                      marks=[mark('box', 0, round(d * 0.3, 1), 296, round(d * 0.15, 1), 0, '#F4F9FA')] if oben else None))
kern = scheiben(5, 35, 3, 15)
for i, (z, h, d) in enumerate(reversed(kern)):
    oben = i == 0
    teile.append(teil(f'kern_{i + 1}', 'ldpe_film', 'Papphülse (Wickelkern)', 'Papphülse', 'box',
                      x=0, y=round(MITTE_Y - d / 2, 2), w=300, d=d, z=z, h=h, r=0, explode=[330, 0, 0],
                      mass=round(28 * d / sum(k[2] for k in kern), 2), material_id='cardboard',
                      materials=[['papier', 97], ['klebstoff', 3]], color=KERN, label=oben,
                      info='Gewickelte Pappe, auf der die Folie aufgerollt ist. Wenn die Rolle leer ist, '
                           'kommt die Hülse ins Altpapier.',
                      marks=[mark('box', 0, 0, 300, d, 0, '#A27B50'), mark('box', 0, round(d / 2 - 1, 1), 300, 2, 0, '#8E6A42')]
                      if oben else None))
teile.insert(1, teil('folienende', 'ldpe_film', 'Loses Folienende', 'Folienende', 'box',
                     x=2, y=40, w=296, d=0.3, z=6, h=24, r=0, explode=[0, 45, 0], mass=0.5,
                     materials=[['ldpe', 100]], color=FOLIE, opacity=0.7,
                     info='Hier zieht man die Folie ab. Sie haftet an sich selbst, deshalb sucht man den Anfang oft lange.'))
skaliere_masse(teile, oid='cling_film', stellen=2)
schreibe('cling_film', teile)
