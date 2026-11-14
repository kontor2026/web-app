"""3D-Modell: vinyl_record. Erzeugt tools/kategorien/modelle/vinyl_record.json.

LP (12 Zoll, Ø 302 mm, 33 1/3 U/min) in Papp-Plattenhülle 314 × 314 mm, liegend, mit Schutzfolie.
Die Platte steckt in einer Papier-Innenhülle, beidseitig ein Papieretikett. Rillen als konzentrische marks.
Explosion: Folie, Etikett, Platte, Etikett unten und Innenhülle schweben über der Hülle (Reihenfolge nach Liste).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

H = 314          # Hülle
P = 302          # Platte
O = (H - P) / 2  # Versatz der Platte in der Hülle
LBL = 100        # Etikett
VINYL = '#1C1D1F'


def mitte(w_teil, w):
    return (w_teil - w) / 2


def rillen(w):
    """Konzentrische Rillenbänder (Liedgruppen) und Auslaufrille, relativ zur Platte."""
    ms = [mark('cyl', mitte(w, 296), mitte(w, 296), 296, fill='#2A2B2E')]
    for i, dm in enumerate((288, 262, 236, 210, 184, 158, 130)):
        ms.append(mark('cyl', mitte(w, dm), mitte(w, dm), dm, fill='#232427' if i % 2 else '#303134'))
    ms.append(mark('cyl', mitte(w, 120), mitte(w, 120), 120, fill='#18191B'))
    ms.append(mark('cyl', mitte(w, 7.2), mitte(w, 7.2), 7.2, fill='#E8E4DA', zeichnung=True))
    return ms


teile = [
    teil('folie', 'cardboard_sleeve', 'Schutzfolie', 'Folie', 'box', material_id='pp',
         x=0, y=0, w=H, d=H, z=3.2, h=0.05, r=1, mass=3, materials=[['pp', 100]], color='#E4ECF0', opacity=0.2,
         info='Dünne Schrumpffolie aus Kunststoff, schützt die neue Hülle. Abziehen und in die Gelbe Tonne oder den Restmüll, '
              'nicht ins Altpapier.'),
    teil('etikett_oben', 'pvc_record', 'Etikett Seite A', 'Etikett A', 'cyl', material_id='paper',
         x=O + mitte(P, LBL), y=O + mitte(P, LBL), w=LBL, z=2.4, h=0.05, mass=0.5,
         materials=[['papier', 90], ['druck', 10]], color='#C8423A', wand=(LBL - 7.2) / 2, boden=0,
         info='Bedrucktes Papier mit Titel und Seite, beim Pressen fest ins Vinyl eingepresst. Es lässt sich nicht ablösen.',
         marks=[mark('box', 22, 28, 56, 6, 1, '#F2E6C8'), mark('box', 30, 66, 40, 4, 1, '#F2E6C8'),
                mark('cyl', mitte(LBL, 7.2), mitte(LBL, 7.2), 7.2, fill='#E8E4DA', zeichnung=True)]),
    teil('platte', 'pvc_record', 'Schallplatte aus Vinyl', 'Platte', 'cyl',
         x=O, y=O, w=P, z=0.9, h=1.5, mass=140, materials=[['pvc', 99], ['druck', 1]], color=VINYL, wand=(P - 7.2) / 2, boden=0,
         info='PVC mit Ruß gefärbt. In der spiralförmigen Rille steckt der Ton als feine Wellen, die die Nadel abtastet. '
              'Weitergeben oder verkaufen; über die Hausmülltonnen wird PVC nicht recycelt.',
         marks=rillen(P)),
    teil('etikett_unten', 'pvc_record', 'Etikett Seite B', 'Etikett B', 'cyl', material_id='paper',
         x=O + mitte(P, LBL), y=O + mitte(P, LBL), w=LBL, z=0.85, h=0.05, mass=0.5, label=False,
         materials=[['papier', 90], ['druck', 10]], color='#3E6FA8', wand=(LBL - 7.2) / 2, boden=0,
         info='Etikett der Rückseite, ebenfalls eingepresst.',
         marks=[mark('cyl', mitte(LBL, 7.2), mitte(LBL, 7.2), 7.2, fill='#E8E4DA', zeichnung=True)]),
    teil('innenhuelle', 'cardboard_sleeve', 'Papier-Innenhülle', 'Innenhülle', 'box', material_id='paper',
         x=O - 1, y=O - 1, w=P + 2, d=P + 2, z=0.6, h=0.25, r=1, mass=9, materials=[['papier', 97], ['druck', 3]],
         color='#EFEBE0',
         info='Weißes Papier, oft mit Folie gefüttert, mit rundem Sichtloch für das Etikett. Reines Papier darf ins Altpapier, '
              'gefütterte Hüllen in den Restmüll.',
         marks=[mark('cyl', mitte(P + 2, 110), mitte(P + 2, 110), 110, fill='#D9D3C2')]),
    teil('huelle', 'cardboard_sleeve', 'Plattenhülle (Cover)', 'Cover', 'box',
         x=0, y=0, w=H, d=H, z=0, h=3.2, r=1, mass=48, materials=[['papier', 94], ['druck', 6]], color='#E2B33C',
         info='Gefalteter Karton, an drei Seiten verklebt, rundum bedruckt. Die Platte wird an der offenen Seite herausgezogen. '
              'Eine leere Hülle kommt ins Altpapier.',
         marks=[mark('box', 30, 30, 254, 200, 3, '#C8423A'), mark('cyl', 107, 60, 100, 100, fill='#F2E6C8'),
                mark('box', 30, 250, 180, 14, 2, '#22272B'), mark('box', 30, 272, 120, 8, 2, '#22272B')]),
]

explodiere(teile, abstand=110, abstaende={'etikett_oben': 30, 'etikett_unten': 30}, nach_liste=True)
skaliere_masse(teile, oid='vinyl_record')
schreibe('vinyl_record', teile)
