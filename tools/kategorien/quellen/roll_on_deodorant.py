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
         color=KAPPE, marks=[mark('cyl', 5, 5, 35, fill='#2A6BBE')]),
    teil('kugel', 'roller_ball', 'Rollkugel', 'Kugel', 'cyl',
         x=10, y=10, w=25, z=87, h=25, mass=3,
         info='Hohlkugel aus PP, die beim Rollen das Deo aufträgt.',
         color='#FFFFFF', marks=[mark('cyl', 3, 3, 19, fill='#F2F2EE'), mark('cyl', 7, 6, 7, fill='#FAFAF8')]),
    teil('kugelhalter', 'roller_ball', 'Kugelhalter', 'Kugelhalter', 'cyl',
         material_id='ldpe', x=7.5, y=7.5, w=30, z=80, h=14, mass=2,
         info='Ring aus weichem PE, in den die Kugel einrastet. Mit einem Löffelstiel heraushebeln, '
              'dann lässt sich die Flasche ausspülen.',
         color='#E6E9EC', marks=[mark('cyl', 2.5, 2.5, 25, fill='#C9CED3')]),
    teil('hals', 'deodorant_bottle', 'Hals mit Gewinde', 'Hals', 'cyl',
         x=6, y=6, w=33, z=72, h=12, mass=2.5,
         info='Weiter Hals, in dem der Kugelhalter steckt.', color=FLASCHE,
         marks=[mark('cyl', 3, 3, 27, fill='#D3DCE5')]),
    teil('schulter', 'deodorant_bottle', 'Schulter', 'Schulter', 'cyl',
         x=4.5, y=4.5, w=36, z=66, h=6, mass=2.5, info='Übergang vom Rumpf zum Hals.', color=FLASCHE, label=False),
    teil('rumpf', 'deodorant_bottle', 'Flasche', 'Flasche', 'cyl',
         x=1.5, y=1.5, w=42, z=4, h=62, mass=15,
         info='Dickwandiges PP, Recyclingcode 5. Leer machen, Kugel heraushebeln, ausspülen und in die '
              'Gelbe Tonne. Glasflaschen gehören dagegen ins Altglas.',
         color=FLASCHE),
    teil('boden', 'deodorant_bottle', 'Boden', 'Boden', 'cyl',
         x=2.5, y=2.5, w=40, z=0, h=4, mass=3, info='Standboden mit Recyclingzeichen.', color=FLASCHE, label=False),
]
explodiere(teile, abstand=12, nach_liste=True, gruppen=[['hals', 'schulter', 'rumpf', 'boden']])
skaliere_masse(teile, oid='roll_on_deodorant')
schreibe('roll_on_deodorant', teile)
