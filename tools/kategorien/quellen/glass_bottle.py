"""3D-Modell: glass_bottle. Erzeugt tools/kategorien/modelle/glass_bottle.json.

Typische braune Mehrweg-Bierflasche (Longneck, Ø 60 mm, 230 mm hoch, ca. 360 g) mit Kronkorken.
Schulter und Hals als Stapel immer schmalerer Scheiben, Etiketten als Bänder um Bauch und Hals.
Die Flasche bleibt stehen, Dichtung und Kronkorken schweben darüber, die Etiketten werden nach rechts gezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

GLAS = dict(color='#6B4A2B', opacity=0.75)
INNEN = '#5A3D22'
C = 30


def rund(w, z, h):
    return dict(x=C - w / 2, y=C - w / 2, w=w, z=z, h=h)


INFO_G = 'Gehört zur Flasche, alles in einem Stück aus Glas geblasen.'
glas = []


def g(id, name, short, w, z, h, mass, info=INFO_G, **extra):
    glas.append(teil(id, 'glass_container', name, short, 'cyl', **rund(w, z, h), mass=mass, info=info,
                     **{**GLAS, **extra}))


g('muendung', 'Mündung mit Wulst', 'Mündung', 28.5, 216, 10, 9,
  'Verdickter Rand, unter den der Kronkorken gepresst wird. Ist er angeschlagen, wird die Flasche aussortiert.',
  marks=[mark('cyl', 5, 5, 18.5, fill=INNEN)])
g('hals', 'Flaschenhals', 'Hals', 25, 186, 30, 22,
  'Langer, schmaler Hals. Daran greifen die Maschinen in der Abfüllanlage.')
g('halsfuss', 'Flaschenhals', 'Hals', 28, 172, 14, 12, label=False)
for i, (w, z) in enumerate([(35, 164), (43, 156), (50, 148), (56, 140)]):
    g(f'schulter{i}', 'Flaschenschulter', 'Schulter', w, z, 8, 12,
      'Übergang zum Hals. Braunes Glas schützt das Bier vor Licht, sonst schmeckt es schnell muffig.'
      if i == 3 else INFO_G, label=(i == 3))
g('koerper', 'Flaschenkörper', 'Körper', 60, 6, 134, 230,
  'Kalk-Natron-Glas aus Sand, Soda und Kalk. Als Mehrwegflasche bis zu 50-mal gespült und neu befüllt, '
  'danach nach Farbe getrennt eingeschmolzen.')
g('boden', 'Boden mit Scheuerring', 'Boden', 56, 0, 6, 40,
  'Dicker Boden. Der helle, zerkratzte Ring entsteht, wenn Flaschen im Kasten und auf dem Band aneinanderreiben.')

teile = [
    teil('kronkorken', 'crown_cap', 'Kronkorken', 'Kronkorken', 'cyl', **rund(32, 223, 7), mass=2.0,
         materials=[['weissblech', 100]], color='#B8BEC4',
         info='Weißblech mit 21 Zacken, auf den Wulst gepresst. Mit dem Öffner abhebeln, er gehört in die '
              'Gelbe Tonne oder zum Metall.',
         marks=[mark('cyl', 2, 2, 28, fill='#C8CDD2'), mark('cyl', 6, 6, 20, fill='#C9A646')]),
    teil('dichtung', 'crown_cap', 'Dichtungseinlage', 'Dichtung', 'cyl', **rund(26, 223.6, 0.6), mass=0.2,
         material_id='ldpe', materials=[['ldpe', 100]], color='#E4E0D2',
         info='Weiche Kunststoffschicht innen im Kronkorken. Sie dichtet ab, damit die Kohlensäure drinbleibt. '
              'Bleibt am Kronkorken.'),
    *glas,
    teil('halsetikett', 'paper_label', 'Halsschleife', 'Halsetikett', 'cyl', **rund(25.6, 192, 18), mass=0.5,
         materials=[['papier', 90], ['druck', 5], ['klebstoff', 5]], color='#C9A646', sortBias=9,
         marks=[mark('cyl', 0.8, 0.8, 24, fill='#5C3F25')],
         info='Papierstreifen rund um den Hals. Darf beim Altglas dranbleiben, er verbrennt in der Schmelze.'),
    teil('etikett', 'paper_label', 'Bauchetikett', 'Etikett', 'cyl', **rund(60.6, 40, 70), mass=2,
         materials=[['papier', 90], ['druck', 5], ['klebstoff', 5]], color='#E8DDC0', sortBias=31,
         marks=[mark('cyl', 1.3, 1.3, 58, fill='#5C3F25')],
         info='Papier mit wasserlöslichem Leim. In der Spülanlage der Brauerei weicht es in heißer Lauge ab.'),
]
for p in teile:
    p['explode'] = {'kronkorken': [0, 0, 28], 'dichtung': [0, 0, 15], 'halsetikett': [60, 0, 0],
                    'etikett': [90, 0, 0]}.get(p['id'], [0, 0, 0])
skaliere_masse(teile, oid='glass_bottle')
schreibe('glass_bottle', teile)
