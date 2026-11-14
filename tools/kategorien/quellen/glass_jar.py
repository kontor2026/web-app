"""3D-Modell: glass_jar. Erzeugt tools/kategorien/modelle/glass_jar.json.

Typisches Schraubglas (Marmelade, Gurken, ca. 300 ml, Ø 75 × 100 mm, Twist-off-Deckel TO 66).
Gewinde als abwechselnd breitere und schmalere Scheiben, Etikett als Band um den Körper.
Glas bleibt stehen, Dichtung und Deckel schweben darüber, das Etikett wird nach rechts gezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

GLAS = dict(color='#DCE8E4', opacity=0.6)
C = 37.5
GOLD, GOLD_H, GOLD_D = '#C9A646', '#D8B85A', '#B8963A'


def rund(w, z, h):
    return dict(x=C - w / 2, y=C - w / 2, w=w, z=z, h=h)


INFO_G = 'Gehört zum Glas, alles in einem Stück gepresst und geblasen.'
glas = []


def g(id, name, short, w, z, h, mass, info=INFO_G, **extra):
    glas.append(teil(id, 'glass_container', name, short, 'cyl', **rund(w, z, h), mass=mass, info=info,
                     **{**GLAS, **extra}))


g('rand', 'Glasrand (Mündung)', 'Mündung', 64, 93, 3, 3,
  'Glatter Rand, auf den die Dichtung des Deckels drückt. Hat er eine Macke, bleibt das Glas nicht dicht.',
  marks=[mark('cyl', 4, 4, 56, fill='#EEF4F2', zeichnung=True)])
for i, (w, z, h) in enumerate([(67.5, 91.5, 1.5), (64, 89.5, 2), (67.5, 88, 1.5), (64, 86, 2)]):
    g(f'gewinde{i}', 'Gewindegang', 'Gewinde', w, z, h, 2.5,
      'Kurze, schräge Gewindegänge aus Glas. Die vier Nocken des Deckels greifen hier ein, '
      'schon eine Vierteldrehung macht das Glas zu.' if i == 0 else INFO_G, label=(i == 0))
g('halsring', 'Halsring', 'Halsring', 69, 84, 2, 4, 'Wulst unter dem Gewinde. Bis hierhin reicht der Deckel.', label=False)
g('schulter', 'Schulter', 'Schulter', 72, 80, 4, 8, INFO_G, label=False)
g('koerper', 'Glaskörper', 'Glaskörper', 75, 5, 75, 150,
  'Weißglas (farblos). Leer, aber ungespült in den Weißglas-Container. Der Deckel gehört nicht ins Altglas.')
g('boden', 'Glasboden', 'Boden', 71, 0, 5, 22,
  'Dicker Boden mit Prägung: Zahlen und Zeichen verraten Glashütte und Form, aus der das Glas kommt.')

# Körper in 3 gleich breite Abschnitte teilen: die Foto-Ansicht verbindet die Scheiben zu einer glatten Hülle,
# so bleibt die Wand gerade statt fassförmig
_i = next(i for i, p in enumerate(glas) if p['id'] == 'koerper')
_k = glas.pop(_i)
for _n in range(3):
    _p = dict(_k, id='koerper' if _n == 0 else f'koerper{_n + 1}', z=_k['z'] + _k['h'] * _n / 3, h=_k['h'] / 3,
              mass=_k['mass'] / 3, label=_k.get('label', True) if _n == 0 else False,
              info=_k['info'] if _n == 0 else INFO_G, marks=_k.get('marks') if _n == 3 - 1 else None)
    glas.insert(_i + _n, _p)

teile = [
    teil('deckel', 'twist_off_lid', 'Twist-off-Deckel', 'Deckel', 'cyl', **rund(68, 91, 9), mass=14,
         materials=[['weissblech', 96], ['druck', 4]], color='#E3C77A',
         info='Weißblech, innen lackiert, mit vier Nocken. Der Knopf in der Mitte wölbt sich hoch, wenn das '
              'Vakuum weg ist. Abschrauben und in die Gelbe Tonne geben.',
         marks=[mark('cyl', 3, 3, 62, fill=GOLD_H), mark('cyl', 8, 8, 52, fill=GOLD_H),
                mark('cyl', 23, 23, 22, fill=GOLD_D), mark('cyl', 28, 28, 12, fill='#C9A646')]),
    teil('dichtung', 'twist_off_lid', 'Dichtungsmasse', 'Dichtung', 'cyl', **rund(64, 96, 1.2), mass=1,
         material_id='pvc', materials=[['pvc', 100]], color='#E4E0D2',
         marks=[mark('cyl', 5, 5, 54, fill='#D8B85A')],
         info='Weicher Kunststoffring innen im Deckel. Er macht das Glas luftdicht, beim Öffnen hört man es '
              'ploppen. Bleibt am Deckel.'),
    *glas,
    teil('etikett', 'paper_label', 'Papieretikett', 'Etikett', 'cyl', **rund(75.6, 15, 55), mass=1.5,
         materials=[['papier', 90], ['druck', 5], ['klebstoff', 5]], color='#E8DDC0', sortBias=11,
         wand=0.3, boden=0, marks=[mark('cyl', 1, 1, 73.6, fill='#CCD8D4', zeichnung=True)],
         info='Papier mit Leim. Darf beim Altglas dranbleiben, es verbrennt in der Schmelze.'),
]
for p in teile:
    p['explode'] = {'deckel': [0, 0, 62], 'dichtung': [0, 0, 28], 'etikett': [125, 0, 0]}.get(p['id'], [0, 0, 0])
skaliere_masse(teile, oid='glass_jar')
schreibe('glass_jar', teile)
