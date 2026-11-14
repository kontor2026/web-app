"""3D-Modell: cling_film. Erzeugt tools/kategorien/modelle/cling_film.json.

Typische Haushaltsrolle Frischhaltefolie (30 cm breit, ca. 30 m LDPE-Folie, 40 mm Durchmesser) liegend auf dem
Papphülsenkern. Die runde Rolle ist aus waagrechten Scheiben (Kreissehnen) aufgebaut, der Kern ragt an beiden
Enden 2 mm heraus. Explodiert wird der Kern seitlich herausgezogen, die Rolle hebt aus dem Spenderkarton, der Deckel darüber.
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
folie = scheiben(0, 40, 8, 20)
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
kern = scheiben(5, 35, 5, 15)
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
# Spenderkarton mit Klappdeckel: Rolle liegt innen (zusammengebaut verdeckt), hebt explodiert heraus.
KOMP = teile[0]['component_id']
ROLLE = [0, 0, 90]
DECKEL = [0, 0, 180]
for p in teile:
    p['x'] += 3
    p['y'] += 2
    p['z'] += 2
    p['sortBias'] = -20
    p['explode'] = [330, 0, 90] if p['id'].startswith('kern') else ROLLE
KARTON = '#2E7D6B'
KARTONINFO = dict(material_id='cardboard', materials=[['papier', 90], ['druck', 5], ['klebstoff', 5]])
teile[:0] = [
    teil('deckel', KOMP, 'Klappdeckel', 'Deckel', 'box', x=0, y=0, w=306, d=44, z=40, h=4, r=1, explode=DECKEL,
         mass=6, color=KARTON, **KARTONINFO,
         info='Deckel des Spenderkartons, er hält die Rolle beim Abreißen fest. Leeren Karton flach falten und ins Altpapier.',
         marks=[mark('box', 0, 12, 306, 20, 0, '#F4F6F5'), mark('box', 20, 16, 90, 12, 2, KARTON),
                mark('box', 2, 2, 302, 40, 1)]),
    teil('klappe', KOMP, 'Vordere Klappe', 'Klappe', 'box', x=0, y=44, w=306, d=0.6, z=30, h=14, r=0,
         explode=DECKEL, mass=3, color=KARTON, sortBias=30, label=False, **KARTONINFO,
         info='Die Klappe wird beim Abreißen auf die Folie gedrückt, damit sie gerade abreißt.'),
    teil('schneide', KOMP, 'Abreißschiene aus Metall', 'Schneide', 'box', material_id='steel',
         x=3, y=44.6, w=300, d=0.4, z=27, h=4, r=0, explode=DECKEL, mass=4, materials=[['stahl', 100]],
         color='#9DA4AA', sortBias=32,
         info='Gezahnte Stahlschiene zum Abreißen der Folie. Vorsicht, scharf! Vor dem Altpapier abziehen, '
              'sie gehört in die Gelbe Tonne.'),
]
teile.append(teil('karton', KOMP, 'Spenderkarton', 'Karton', 'box', x=0, y=0, w=306, d=44, z=0, h=40, r=1,
                  explode=[0, 0, 0], mass=24, color=KARTON, **KARTONINFO,
                  info='Bedruckter Faltkarton, schützt die Rolle. Pappe ins Altpapier, Folie und Rolle getrennt entsorgen.',
                  wand=1, marks=[mark('box', 2, 2, 302, 40, 1, '#3B3B38', zeichnung=True)]))
skaliere_masse(teile, oid='cling_film', stellen=2)
schreibe('cling_film', teile)
