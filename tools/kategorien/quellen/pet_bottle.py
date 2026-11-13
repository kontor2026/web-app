"""3D-Modell: pet_bottle. Erzeugt tools/kategorien/modelle/pet_bottle.json.

0,5-l-Einweg-PET-Flasche mit Pfand: 65 mm Durchmesser, 230 mm hoch, ca. 25 g.
Schulter als Stapel immer schmalerer Scheiben, Griffrillen als schmale Scheiben im Körper.
Die Flasche bleibt stehen, Ring und Deckel schweben über dem Hals, das Rundum-Etikett wird nach rechts gezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

PET = dict(material_id='pet', materials=[['pet', 100]], color='#CFE3E8', opacity=0.55)
HDPE = dict(material_id='hdpe', materials=[['hdpe', 100]], color='#2F6DB5')
C = 32.5  # Mittelpunkt


def rund(w, z, h):
    return dict(x=C - w / 2, y=C - w / 2, w=w, z=z, h=h)


INFO_K = 'Gehört zur Flasche aus PET (Recyclingcode 1). Wird beim Recycling mit der ganzen Flasche geschreddert.'
koerper = []


def k(id, name, short, w, z, h, mass, info, **extra):
    koerper.append(teil(id, 'pet_bottle_body', name, short, 'cyl', **rund(w, z, h), mass=mass, info=info,
                        **{**PET, **extra}))


k('hals', 'Flaschenhals mit Gewinde', 'Hals', 27, 200, 26, 1.6,
  'Dickwandig und nicht verstreckt, darum je Zentimeter der schwerste Teil der Flasche. Das Gewinde hält den Deckel.',
  marks=[mark('cyl', 5, 5, 17, fill='#B8CFD5')])
k('tragring', 'Tragring', 'Tragring', 35, 198, 2, 0.4,
  'Ring am Hals, an dem die Flasche in der Abfüllanlage hängt und transportiert wird. Gehört zur Flasche.')
k('halsunten', 'Flaschenhals', 'Hals', 27, 180, 18, 1.0, INFO_K, label=False)
for i, (w, z, h) in enumerate([(34, 174, 6), (43, 167, 7), (52, 160, 7), (60, 153, 7)]):
    k(f'schulter{i}', 'Flaschenschulter', 'Schulter', w, z, h, 0.8,
      'Übergang vom Hals zum Körper. Beim Streckblasen aus dem Rohling mitgeformt, die Wand wird hier dünner.'
      if i == 3 else INFO_K, label=(i == 3))
k('koerper', 'Flaschenkörper', 'Körper', 65, 59, 94, 9.5,
  'PET, Recyclingcode 1. Wird aus einem reagenzglasgroßen Rohling heiß aufgeblasen. '
  'Pfandflaschen werden meist wieder zu neuen Flaschen.')
for i, z in enumerate([56, 44, 32]):
    k(f'rille{i}', 'Griffrille', 'Griffrille', 61.5, z, 3, 0.4,
      'Rillen machen die dünne Wand steifer und die Flasche griffiger.' if i == 0 else INFO_K, label=(i == 0))
for i, z in enumerate([47, 35]):
    k(f'band{i}', 'Flaschenkörper', 'Körper', 65, z, 9, 1.2, INFO_K, label=False)
k('unterteil', 'Flaschenkörper', 'Körper', 65, 7, 25, 2.6, INFO_K, label=False)
k('boden', 'Petaloid-Boden', 'Boden', 60, 0, 7, 2.2,
  'Der Boden hat fünf Füße (Petaloid), damit er dem Druck der Kohlensäure standhält und die Flasche gerade steht.')

teile = [
    teil('deckel', 'hdpe_screw_cap', 'Schraubdeckel', 'Deckel', 'cyl', **rund(30, 208, 22), mass=2.0,
         info='HDPE, Recyclingcode 2. Seit 2024 hängt er per Lasche an der Flasche, damit er mit ihr recycelt wird. '
              'Dran lassen!', **HDPE,
         marks=[mark('cyl', 3, 3, 24, fill='#3A7CC6'), mark('cyl', 9, 9, 12)]),
    teil('ring', 'hdpe_screw_cap', 'Sicherungsring mit Lasche', 'Ring', 'cyl', **rund(31, 204, 4), mass=0.4,
         info='Reißt beim ersten Öffnen teilweise ab und zeigt, dass die Flasche unbenutzt ist. '
              'Die Lasche hält den Deckel fest.', **HDPE),
    *koerper,
    teil('etikett', 'plastic_label', 'Rundum-Etikett', 'Etikett', 'cyl', **rund(66, 80, 70), mass=0.5,
         material_id='pp', materials=[['pp', 100]],
         info='Dünne bedruckte PP-Folie, rundum geklebt. In der Recyclinganlage schwimmt sie im Wasser oben und '
              'wird so vom PET getrennt.', color='#D9483B', sortBias=4,
         marks=[mark('cyl', 1, 1, 64, fill='#C3D6DB')]),
]

# Explosion: Flasche bleibt stehen, Deckel und Ring über dem Hals, Etikett nach rechts
for p in teile:
    p['explode'] = {'deckel': [0, 0, 48], 'ring': [0, 0, 34], 'etikett': [95, 0, 0]}.get(p['id'], [0, 0, 0])

skaliere_masse(teile, oid='pet_bottle', stellen=2)
schreibe('pet_bottle', teile)
