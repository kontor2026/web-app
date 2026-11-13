"""3D-Modell: swim_goggles. Erzeugt tools/kategorien/modelle/swim_goggles.json.

Schwimmbrille für Kinder/Jugendliche, mit den Gläsern nach oben auf dem Tisch: 160 × 40 × 35 mm, ca. 30 g.
Zwei getönte PC-Augenschalen (Linse und Rahmen aus einem Stück) mit Silikon-Dichtungen darunter, verstellbarer
Nasensteg, seitliche Bandclips und ein geteiltes Silikon-Kopfband, das flach hinter den Dichtungen liegt.
Explodiert: Schalen und Steg nach oben, Clips zur Seite, Kopfband nach vorne.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

LINSE, RAHMEN = '#3E6F92', '#2A5574'
SILIKON = '#2F3A44'
CLIP = '#E8EAEC'


def linse(seite, x, label=True):
    return teil(f'linse_{seite}', 'tinted_lenses', f'Augenschale {seite} mit Linse', 'Linse', 'cyl',
                x=x, y=1, w=58, d=38, z=10, h=22, mass=6, color=LINSE, opacity=0.72, label=label,
                info='Getönte Schale aus Polycarbonat, innen mit Antibeschlag-Schicht (nicht mit dem Finger reiben). '
                     'Sie lässt sich von innen aus der Dichtung drücken.',
                marks=[mark('cyl', 4, 3, 50, 32, fill=RAHMEN), mark('cyl', 7, 5, 44, 28, fill='#5B8DB0'),
                       mark('cyl', 12, 8, 12, 6, fill='#9CC3DC')])


def dichtung(seite, x, label=True):
    return teil(f'dichtung_{seite}', 'silicone_head_strap', f'Silikondichtung {seite}', 'Dichtung', 'cyl',
                x=x, y=2, w=56, d=36, z=0, h=10, mass=3, color=SILIKON, label=label,
                info='Weicher Silikonrand, der am Gesicht abdichtet. Silikon kann nicht in die Gelbe Tonne: '
                     'Eine kaputte Brille kommt in den Restmüll.',
                marks=[mark('cyl', 6, 5, 44, 26, fill='#1C232A')])


def clip(seite, x, dx, label=True):
    return teil(f'clip_{seite}', 'tinted_lenses', f'Bandclip {seite}', 'Bandclip', 'box',
                material_id='pp', x=x, y=12, w=14, d=16, z=10, h=16, r=3, mass=1.5, color=CLIP, label=label,
                explode=[dx, 0, 0],
                info='Clip mit Rastzähnen, durch den das Kopfband gefädelt ist. Zum Verstellen den Bügel '
                     'aufklappen und das Band ziehen.',
                marks=[mark('box', 3, 2, 8, 12, 2, '#B9BEC2')])


teile = [
    teil('nasensteg', 'tinted_lenses', 'Verstellbarer Nasensteg', 'Nasensteg', 'box',
         material_id='pp', x=72, y=13, w=16, d=14, z=18, h=10, r=3, mass=1, color=SILIKON, explode=[0, 0, 35],
         info='Steg zwischen den Augenschalen. Es gibt ihn in mehreren Größen, er wird einfach eingeklickt.',
         marks=[mark('box', 2, 4, 12, 2, 1, '#55606A'), mark('box', 2, 8, 12, 2, 1, '#55606A')]),
    linse('links', 14),
    linse('rechts', 88, label=False),
    clip('links', 0, -30),
    clip('rechts', 146, 30, label=False),
    dichtung('links', 15),
    dichtung('rechts', 89, label=False),
    teil('kopfband', 'silicone_head_strap', 'Geteiltes Kopfband', 'Kopfband', 'box',
         x=0, y=30, w=160, d=10, z=0, h=2, r=2, mass=8, color='#2C6FA6', explode=[0, 60, 0],
         info='Elastisches Silikonband, hinten geteilt, damit es am Kopf nicht rutscht. Aus den Clips fädeln.',
         marks=[mark('box', 4, 1, 152, 3, 1.5, '#235C8B'), mark('box', 4, 6, 152, 3, 1.5, '#235C8B')]),
]
explodiere(teile, abstand=15, fest=('dichtung_links', 'dichtung_rechts'))
skaliere_masse(teile, oid='swim_goggles', stellen=2)
schreibe('swim_goggles', teile)
