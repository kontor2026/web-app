"""3D-Modell: aluminium_foil. Erzeugt tools/kategorien/modelle/aluminium_foil.json.

Typische Haushaltsrolle Alufolie (30 cm breit, ca. 10 m, 0,011 mm dick, 40 mm Durchmesser) liegend auf dem
Papphülsenkern. Die runde Rolle ist in der Zeichnung ein Quader, in der Foto-Ansicht ein liegender Zylinder (form='liegend_x'), der Kern ragt an beiden
Enden 2 mm heraus. Explodiert wird der Kern seitlich herausgezogen, die Rolle hebt aus dem Spenderkarton, der Deckel darüber.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

ALU = '#D5D8DB'
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
folie = scheiben(0, 40, 1, 20)  # eine Rolle: Foto-Ansicht zeigt sie als liegenden Zylinder (form)
gesamt = sum(d for _, _, d in folie)
for i, (z, h, d) in enumerate(reversed(folie)):
    oben = i == 0
    teile.append(teil(f'folie_{i + 1}', 'aluminium_foil_sheet',
                      'Aufgewickelte Alufolie' if oben else 'Aufgewickelte Alufolie (Schnitt)', 'Alufolie', 'box',
                      x=2, y=round(MITTE_Y - d / 2, 2), w=296, d=d, z=z, h=h, r=0, explode=[0, 0, 0], form='liegend_x',
                      mass=round(110 * d / gesamt, 2), color=ALU, label=oben,
                      info='Gewalztes Aluminium, nur etwa 0,01 mm dick: eine Seite glänzt, die andere ist matt. '
                           'Saubere Reste zu einer faustgroßen Kugel knüllen, dann erkennt die Sortieranlage sie.',
                      marks=[mark('box', 0, round(d * 0.25, 1), 296, round(d * 0.2, 1), 0, '#E4E7EA', zeichnung=True)] if oben else None))
kern = scheiben(5, 35, 1, 15)
for i, (z, h, d) in enumerate(reversed(kern)):
    oben = i == 0
    teile.append(teil(f'kern_{i + 1}', 'aluminium_foil_sheet', 'Papphülse (Wickelkern)', 'Papphülse', 'box',
                      x=0, y=round(MITTE_Y - d / 2, 2), w=300, d=d, z=z, h=h, r=0, explode=[330, 0, 0], form='liegend_x',
                      mass=round(28 * d / sum(k[2] for k in kern), 2), material_id='cardboard',
                      materials=[['papier', 97], ['klebstoff', 3]], color=KERN, label=oben,
                      info='Gewickelte Pappe, auf der die Folie aufgerollt ist. Wenn die Rolle leer ist, '
                           'kommt die Hülse ins Altpapier.',
                      marks=[mark('box', 0, 0, 300, d, 0, '#A27B50', zeichnung=True),
                             mark('box', 0, round(d / 2 - 1, 1), 300, 2, 0, '#8E6A42', zeichnung=True)]
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
KARTON = '#24508F'
KARTONINFO = dict(material_id='cardboard', materials=[['papier', 90], ['druck', 5], ['klebstoff', 5]])
teile[:0] = [
    teil('deckel', KOMP, 'Klappdeckel', 'Deckel', 'box', x=0, y=0, w=306, d=44, z=40, h=4, r=1, explode=DECKEL,
         mass=6, color=KARTON, **KARTONINFO,
         info='Deckel des Spenderkartons, er hält die Rolle beim Abreißen fest. Leeren Karton flach falten und ins Altpapier.',
         marks=[mark('box', 0, 12, 306, 20, 0, '#C9CED3'), mark('box', 20, 16, 90, 12, 2, KARTON),
                mark('box', 2, 2, 302, 40, 1)]),
    teil('klappe', KOMP, 'Vordere Klappe', 'Klappe', 'box', x=0, y=44, w=306, d=0.6, z=30, h=14, r=0,
         explode=DECKEL, mass=3, color=KARTON, sortBias=30, label=False, **KARTONINFO,
         info='Die Klappe wird beim Abreißen auf die Folie gedrückt, damit sie gerade abreißt.'),
    teil('schneide', KOMP, 'Sägezahnkante aus Pappe', 'Sägezahn', 'box', material_id='cardboard',
         x=3, y=44.6, w=300, d=0.4, z=27, h=4, r=0, explode=DECKEL, mass=1, materials=[['papier', 97], ['klebstoff', 3]],
         color='#D9C7A4', sortBias=32,
         info='Gezahnte Kante aus fester Pappe zum Abreißen der Folie. Bleibt am Karton und kommt mit ins Altpapier.'),
]
teile.append(teil('karton', KOMP, 'Spenderkarton', 'Karton', 'box', x=0, y=0, w=306, d=44, z=0, h=40, r=1,
                  explode=[0, 0, 0], mass=24, color=KARTON, **KARTONINFO,
                  info='Bedruckter Faltkarton, schützt die Rolle. Pappe ins Altpapier, Folie und Rolle getrennt entsorgen.',
                  wand=1, marks=[mark('box', 2, 2, 302, 40, 1, '#3B3B38', zeichnung=True)]))
skaliere_masse(teile, oid='aluminium_foil', stellen=2)
schreibe('aluminium_foil', teile)
