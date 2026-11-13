"""3D-Modell: roll_on_deodorant. Erzeugt tools/kategorien/modelle/roll_on_deodorant.json.

Typischer 50-ml-Deoroller: PP-Flasche (Ø 42 mm) mit Gewindehals, eingepresstem Kugelhalter aus PE,
Rollkugel aus PP und hoher Schraubkappe. Flaschenabschnitte bewegen sich gemeinsam,
Kugelhalter, Kugel und Kappe stapeln darüber.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

FLASCHE = '#EEF3F8'
KAPPE = '#1E5AA8'
teile = [
    teil('kappe', 'pp_flip_cap', 'Schraubkappe', 'Kappe', 'cyl',
         x=0, y=0, w=45, z=72, h=48, mass=7,
         info='Hohe Schraubkappe aus PP, die die Kugel vor dem Austrocknen schützt. Abschrauben und mit der '
              'Flasche in die Gelbe Tonne.',
         color=KAPPE, marks=[mark('cyl', 2, 2, 41, fill='#1A4F95'), mark('cyl', 5, 5, 35, fill='#2A6BBE'),
                             mark('cyl', 15, 15, 15, fill='#E8EEF6')]),
    *[teil(f'kugel{i}', 'roller_ball', 'Rollkugel', 'Kugel', 'cyl',
           x=22.5 - dm / 2, y=22.5 - dm / 2, w=dm, z=z0, h=5, mass=0.6, label=(i == 2), color='#FFFFFF',
           info='Hohlkugel aus PP, die beim Rollen das Deo aufträgt. Sie sitzt stramm im Kugelhalter.',
           marks=[mark('cyl', dm * 0.25, dm * 0.2, dm * 0.3, fill='#F7F7F4')] if i == 4 else None)
      for i, (dm, z0) in enumerate([(14, 87), (21, 92), (25, 97), (21, 102), (14, 107)][::-1])],
    teil('kugelhalter', 'roller_ball', 'Kugelhalter', 'Kugelhalter', 'cyl',
         material_id='ldpe', x=7.5, y=7.5, w=30, z=80, h=14, mass=2,
         info='Ring aus weichem PE, in den die Kugel einrastet. Mit einem Löffelstiel heraushebeln, '
              'dann lässt sich die Flasche ausspülen.',
         color='#E6E9EC', marks=[mark('cyl', 2.5, 2.5, 25, fill='#C9CED3'), mark('cyl', 5, 5, 20, fill='#9EA6AE')]),
    teil('hals', 'deodorant_bottle', 'Hals mit Gewinde', 'Hals', 'cyl',
         x=6, y=6, w=33, z=72, h=12, mass=2.5,
         info='Weiter Hals, in dem der Kugelhalter steckt.', color=FLASCHE,
         marks=[mark('cyl', 3, 3, 27, fill='#D3DCE5')]),
    teil('schulter', 'deodorant_bottle', 'Schulter', 'Schulter', 'cyl',
         x=4.5, y=4.5, w=36, z=66, h=6, mass=2.5, info='Übergang vom Rumpf zum Hals.', color=FLASCHE, label=False),
    teil('etikett', 'deodorant_bottle', 'Bedrucktes Etikett', 'Etikett', 'cyl',
         x=1.2, y=1.2, w=42.6, z=10, h=56, mass=0.6, materials=[['pp', 85], ['druck', 10], ['klebstoff', 5]],
         color='#7FA8D8', sortBias=1, explode=[60, 0, 0],
         marks=[mark('cyl', 0.3, 0.3, 42, fill=FLASCHE)],
         info='Dünne Folie aus dem gleichen Kunststoff wie die Flasche. Sie darf dranbleiben, das stört das Recycling nicht.'),
    teil('rumpf', 'deodorant_bottle', 'Flasche', 'Flasche', 'cyl',
         x=1.5, y=1.5, w=42, z=4, h=62, mass=15,
         info='Dickwandiges PP, Recyclingcode 5. Leer machen, Kugel heraushebeln, ausspülen und in die '
              'Gelbe Tonne. Glasflaschen gehören dagegen ins Altglas.',
         color=FLASCHE),
    teil('boden', 'deodorant_bottle', 'Boden', 'Boden', 'cyl',
         x=2.5, y=2.5, w=40, z=0, h=4, mass=3, info='Standboden mit Recyclingzeichen.', color=FLASCHE, label=False),
]
explodiere(teile, abstand=18, nach_liste=True, gruppen=[['hals', 'schulter', 'rumpf', 'boden'], [f'kugel{i}' for i in range(5)]])
skaliere_masse(teile, oid='roll_on_deodorant')
schreibe('roll_on_deodorant', teile)
