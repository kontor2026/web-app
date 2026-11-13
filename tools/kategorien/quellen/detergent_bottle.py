"""3D-Modell: detergent_bottle. Erzeugt tools/kategorien/modelle/detergent_bottle.json.

Typische 1,5-l-Flüssigwaschmittelflasche aus HDPE (100 × 70 mm, 260 mm hoch) mit angeformtem Griff, Ausgießer-
Einsatz und aufgeschraubter Dosierkappe aus PP. Flaschenabschnitte und Griff bewegen sich gemeinsam,
Ausgießer und Kappe stapeln über dem Hals, die Etiketten werden seitlich abgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

FLASCHE = '#F3F1EC'
KAPPE = '#2F6DB5'
teile = [
    teil('dosierkappe', 'pp_flip_cap', 'Dosierkappe', 'Dosierkappe', 'cyl',
         x=7, y=12, w=46, z=212, h=48, mass=12,
         info='Wird aufgeschraubt und dient umgedreht als Messbecher, innen sind Füllstriche eingeprägt. '
              'Mit der Flasche in die Gelbe Tonne, gern aufgeschraubt.',
         color=KAPPE, marks=[mark('cyl', 5, 5, 36, fill='#3A7CC6')]),
    teil('ausgiesser', 'pp_flip_cap', 'Ausgießer-Einsatz', 'Ausgießer', 'cyl',
         material_id='ldpe', x=13, y=18, w=34, z=214, h=10, mass=3,
         info='Eingepresster Ausgießer mit Rinne: Was beim Eingießen danebenläuft, fließt in die Flasche zurück. '
              'Bleibt in der Flasche stecken.',
         color='#E6E9EC', marks=[mark('cyl', 4, 4, 26, fill='#C9CED3'), mark('cyl', 10, 10, 14, fill='#2A2E31')]),
    teil('hals', 'hdpe_bottle_body', 'Flaschenhals mit Gewinde', 'Hals', 'cyl',
         x=11, y=16, w=38, z=198, h=24, mass=6,
         info='Weiter Hals mit grobem Gewinde für die Dosierkappe.', color=FLASCHE,
         marks=[mark('cyl', 4, 4, 30, fill='#D6D3CA')]),
    teil('griff', 'hdpe_bottle_body', 'Angeformter Griff', 'Griff', 'box',
         x=60, y=25, w=34, d=20, z=198, h=38, r=8, mass=8,
         info='Hohler Griff, beim Blasformen in einem Stück mit der Flasche geformt. Durch die Griffmulde läuft '
              'die Flüssigkeit beim Ausgießen mit.',
         color=FLASCHE, marks=[mark('box', 6, 6, 22, 8, 4, '#D6D3CA')]),
    teil('schulter', 'hdpe_bottle_body', 'Flaschenschulter', 'Schulter', 'box',
         x=3, y=3, w=94, d=64, z=172, h=26, r=20, mass=12,
         info='Die Schulter verjüngt sich zum Hals und zum Griff.', color=FLASCHE, label=False),
    teil('rumpf', 'hdpe_bottle_body', 'Flaschenrumpf', 'Rumpf', 'box',
         x=0, y=0, w=100, d=70, z=8, h=164, r=18, mass=45,
         info='HDPE, Recyclingcode 2, oft mit Rezyklat. Restlos leeren, Deckel draufschrauben und in die Gelbe Tonne. '
              'Waschmittel ist reizend, nicht ins Auge bringen.',
         color=FLASCHE),
    teil('boden', 'hdpe_bottle_body', 'Flaschenboden', 'Boden', 'box',
         x=3, y=3, w=94, d=64, z=0, h=8, r=16, mass=8,
         info='Leicht eingezogener Standboden mit Quetschnaht und Recyclingzeichen.', color=FLASCHE, label=False),
    teil('etikett_vorne', 'plastic_label', 'Etikett vorne', 'Etikett', 'box',
         x=100, y=8, w=0.3, d=54, z=30, h=130, r=0, explode=[60, 0, 0], mass=2,
         materials=[['pp', 92], ['druck', 5], ['klebstoff', 3]],
         info='Bedruckte PP-Folie mit Klebstoff. Passt zum Kunststoffrecycling und darf dranbleiben.',
         color=KAPPE, sortBias=100),
    teil('etikett_hinten', 'plastic_label', 'Etikett hinten', 'Etikett', 'box',
         x=-0.3, y=8, w=0.3, d=54, z=30, h=120, r=0, explode=[-60, 0, 0], mass=1.5,
         materials=[['pp', 92], ['druck', 5], ['klebstoff', 3]], label=False,
         info='Rückseite mit Dosiertabelle, Inhaltsstoffen und Gefahrenhinweisen.',
         color='#E8EEF4'),
]
explodiere(teile, abstand=25, nach_liste=True, gruppen=[['hals', 'griff', 'schulter', 'rumpf', 'boden']])
skaliere_masse(teile, oid='detergent_bottle')
schreibe('detergent_bottle', teile)
