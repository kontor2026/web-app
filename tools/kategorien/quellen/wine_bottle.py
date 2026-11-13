"""3D-Modell: wine_bottle. Erzeugt tools/kategorien/modelle/wine_bottle.json.

Typische 0,75-l-Weinflasche (Bordeaux-Form, grünes Glas, Ø 76 × 300 mm, ca. 500 g) mit Naturkorken und
Kapsel aus Alufolie. Schulter als Stapel schmaler werdender Scheiben, Etiketten als Bänder um Bauch und Hals.
Glas bleibt stehen, Korken und Kapsel schweben darüber (Kapsel ganz oben, weil sie zuerst ab muss),
Etiketten werden nach rechts gezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

GLAS = dict(color='#2F5E3A', opacity=0.7)
INNEN = '#244A2D'
C = 38


def rund(w, z, h):
    return dict(x=C - w / 2, y=C - w / 2, w=w, z=z, h=h)


INFO_G = 'Gehört zur Flasche, alles in einem Stück aus Glas geformt.'
glas = []


def g(id, name, short, w, z, h, mass, info=INFO_G, **extra):
    glas.append(teil(id, 'glass_container', name, short, 'cyl', **rund(w, z, h), mass=mass, info=info,
                     **{**GLAS, **extra}))


g('muendung', 'Mündung mit Wulst', 'Mündung', 31, 288, 12, 12,
  'Verdickter Rand am Flaschenhals. Unter dem Wulst schneidet man die Kapsel rundherum ein.',
  marks=[mark('cyl', 3.5, 3.5, 24, fill='#C49A63')])
g('hals', 'Flaschenhals', 'Hals', 29.5, 228, 60, 38, 'Langer, schmaler Hals, in dem der Korken steckt.')
for i, (w, z, h) in enumerate([(35, 220, 8), (46, 212, 8), (58, 204, 8), (68, 196, 8)]):
    g(f'schulter{i}', 'Flaschenschulter', 'Schulter', w, z, h, 12,
      'Die ausgeprägte Schulter der Bordeauxflasche hält beim Einschenken den Weinstein zurück. '
      'Grünes Glas schützt den Wein vor Licht.' if i == 3 else INFO_G, label=(i == 3))
g('koerper', 'Flaschenkörper', 'Körper', 76, 6, 190, 330,
  'Kalk-Natron-Glas aus Sand, Soda und Kalk. Leer und ohne Korken in den Grünglas-Container geben.')
g('boden', 'Boden mit Einstich', 'Boden', 70, 0, 6, 45,
  'Der Boden ist nach innen gewölbt (Einstich). Das macht die Flasche stabiler, und der Bodensatz sammelt '
  'sich am Rand.')

teile = [
    teil('kapsel', 'aluminium_capsule_foil', 'Kapsel (Flaschenhalsfolie)', 'Kapsel', 'cyl', **rund(32.5, 250, 50),
         mass=1.5, materials=[['alu', 80], ['ldpe', 15], ['druck', 5]], color='#7A1F2B', sortBias=1,
         marks=[mark('cyl', 3, 3, 26.5, fill='#9C3340'), mark('cyl', 12.25, 12.25, 8, fill='#5A1620'),
                mark('cyl', 7, 15, 2, fill='#5A1620'), mark('cyl', 23.5, 15, 2, fill='#5A1620')],
         info='Dünne Alufolie mit Kunststoff, schützt den Korken. Unter dem Wulst rundherum einschneiden und '
              'abziehen. Sie gehört in die Gelbe Tonne, nicht ins Altglas.'),
    teil('korken', 'cork_stopper', 'Naturkorken', 'Korken', 'cyl', **rund(24, 255, 44), mass=4,
         materials=[['kork', 100]], color='#C49A63', marks=[mark('cyl', 3, 3, 18, fill='#B08550')],
         info='Aus der Rinde der Korkeiche gestanzt. Mit dem Korkenzieher herausziehen. Naturkorken werden '
              'gesammelt und zu Dämmstoff verarbeitet.'),
    *glas,
    teil('halsschild', 'paper_label', 'Halsschild', 'Halsschild', 'cyl', **rund(30.1, 232, 14), mass=0.3,
         materials=[['papier', 90], ['druck', 5], ['klebstoff', 5]], color='#E9DFC4', sortBias=43,
         marks=[mark('cyl', 0.6, 0.6, 28.9, fill=INNEN)],
         info='Schmales Papierband mit dem Jahrgang. Darf am Glas bleiben.'),
    teil('etikett', 'paper_label', 'Bauchetikett', 'Etikett', 'cyl', **rund(76.6, 60, 95), mass=2.2,
         materials=[['papier', 90], ['druck', 5], ['klebstoff', 5]], color='#EFE6CF', sortBias=42,
         marks=[mark('cyl', 1.3, 1.3, 74, fill=INNEN)],
         info='Papier mit Leim. In warmem Wasser lässt es sich ablösen, beim Altglas darf es aber dranbleiben: '
              'Es verbrennt in der Schmelze.'),
]
for p in teile:
    p['explode'] = {'kapsel': [0, 0, 125], 'korken': [0, 0, 60], 'halsschild': [70, 0, 0],
                    'etikett': [110, 0, 0]}.get(p['id'], [0, 0, 0])
skaliere_masse(teile, oid='wine_bottle')
schreibe('wine_bottle', teile)
