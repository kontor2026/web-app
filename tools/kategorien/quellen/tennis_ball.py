"""3D-Modell: tennis_ball. Erzeugt tools/kategorien/modelle/tennis_ball.json.

Tennisball Ø 67 mm, 58 g: hohler Gummikern (Ø 61 mm, Wand ca. 3,3 mm, mit Überdruck) aus zwei gepressten
Halbschalen, außen zwei Filzstücke (Wolle/Nylon) mit Klebenaht. Die Kugel ist aus gestapelten Zylinderscheiben
gebaut; jede Halbkugel bewegt sich als Gruppe. Explodiert: Filz unten, Kernhälften, Filz oben übereinander.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

D, C = 67, 33.5
FILZ, FILZ_D = '#D4E440', '#BFCF35'
KERN, HOHL = '#55585A', '#2E3032'
NAHT = '#F2F2EC'


def scheiben(pid, comp, name, short, R, grenzen, mass, info, marks_oben=None, marks_unten=None, **kw):
    """Kugelabschnitt aus Zylinderscheiben zwischen den z-Grenzen (Mitte C), oberste Scheibe zuerst."""
    roh = []
    for a, b in zip(grenzen, grenzen[1:]):
        zn = min(max(C, a), b)
        dm = round(2 * math.sqrt(max(R * R - (zn - C) ** 2, 0)), 1)
        roh.append((a, b, dm))
    vol = sum(dm * dm * (b - a) for a, b, dm in roh)
    out = []
    for i, (a, b, dm) in enumerate(reversed(roh)):
        extra = dict(kw)
        if i:
            extra['label'] = False
        if i == 0 and marks_oben:
            extra['marks'] = marks_oben
        if i == len(roh) - 1 and marks_unten:
            extra['marks'] = marks_unten
        out.append(teil(f'{pid}_{i}', comp, name, short, 'cyl', x=round(C - dm / 2, 2), y=round(C - dm / 2, 2), w=dm,
                        z=a, h=round(b - a, 2), mass=round(mass * dm * dm * (b - a) / vol, 2), info=info, **extra))
    return out


filz_oben = scheiben('filz_oben', 'felt_cover', 'Filzbezug obere Hälfte', 'Filz oben', 33.5, [C, 50, 60, 67], 6,
                     'Nadelfilz aus Wolle und Nylon, auf den Kern geklebt. Die weiße Naht ist eine Gummi-Klebenaht. '
                     'Nach dem Aufschneiden lässt sich der Filz abziehen.',
                     materials=[['wolle', 55], ['nylon', 40], ['klebstoff', 5]], color=FILZ,
                     marks_oben=[mark('box', 0, 18.5, 41, 2.5, 1, NAHT), mark('cyl', 8, 6, 8, fill=FILZ_D),
                                 mark('cyl', 26, 28, 7, fill=FILZ_D)])
kern_oben = scheiben('kern_oben', 'rubber_core', 'Gummikern obere Halbschale', 'Kern oben', 30.5, [C, 48, 58, 64], 23,
                     'Halbschale aus Naturkautschuk mit Füllstoffen. Beide Hälften sind verklebt und unter Überdruck '
                     'mit Luft gefüllt, darum springt der Ball.',
                     color=KERN)
kern_unten = scheiben('kern_unten', 'rubber_core', 'Gummikern untere Halbschale', 'Kern unten', 30.5, [3, 9, 19, C], 23,
                      'Innen hohl, die Wand ist nur gut 3 mm dick. Zum Trennen den Ball mit einer Säge halbieren, '
                      'dabei entweicht zischend die Luft.',
                      color=KERN, marks_unten=None)
kern_unten[0]['marks'] = [mark('cyl', 3.3, 3.3, 54.4, fill=HOHL)]
filz_unten = scheiben('filz_unten', 'felt_cover', 'Filzbezug untere Hälfte', 'Filz unten', 33.5, [0, 7, 17, C], 6,
                      'Zweites hantelförmiges Filzstück. Filz und Gummi lassen sich nicht recyceln: Restmüll.',
                      materials=[['wolle', 55], ['nylon', 40], ['klebstoff', 5]], color=FILZ)
filz_unten[0]['marks'] = [mark('cyl', 3, 3, 61, fill=FILZ_D)]

teile = filz_oben + kern_oben + kern_unten + filz_unten
gruppen = [[p['id'] for p in g] for g in (filz_oben, kern_oben, kern_unten, filz_unten)]
explodiere(teile, abstand=12, nach_liste=True, gruppen=gruppen)
skaliere_masse(teile, oid='tennis_ball', stellen=2)
schreibe('tennis_ball', teile)
