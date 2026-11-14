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
OBEN = [C, 45, 53, 59, 64, 67]
UNTEN = [0, 3, 8, 14, 22, C]


def scheiben(pid, comp, name, short, R, grenzen, mass, info, marks_oben=None, marks_unten=None, **kw):
    """Kugelabschnitt aus Zylinderscheiben zwischen den z-Grenzen (Mitte C), oberste Scheibe zuerst."""
    roh = []
    for a, b in zip(grenzen, grenzen[1:]):
        a, b = max(a, C - R), min(b, C + R)  # alle Lagen mit denselben Grenzen, so bleibt der Kern im Filz
        if b - a < 1:
            continue
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


filz_oben = scheiben('filz_oben', 'felt_cover', 'Filzbezug obere Hälfte', 'Filz oben', 33.5, OBEN, 6,
                     'Nadelfilz aus Wolle und Nylon, auf den Kern geklebt. Die weiße Naht ist eine Gummi-Klebenaht. '
                     'Nach dem Aufschneiden lässt sich der Filz abziehen.',
                     materials=[['wolle', 55], ['nylon', 40], ['klebstoff', 5]], color=FILZ,
                     marks_oben=[mark('box', 5, 12.6, 17.7, 2.5, 1, NAHT), mark('cyl', 6, 4, 5, fill=FILZ_D)])
# Die Naht läuft oben quer und auf den Ringen darunter erst links/rechts, dann vorne/hinten herum.
for i, p in enumerate(filz_oben[1:], 1):
    innen, dm = filz_oben[i - 1]['w'], p['w']
    rr, br = (dm + innen) / 4, max((dm - innen) / 2 * 0.55, 1.6)
    m = dm / 2
    if i <= 2:
        orte = [(m - rr, m), (m + rr, m)]
    else:
        orte = [(m, m - rr), (m, m + rr)]
    lang = br * 2.4
    bw, bd = (br * 0.7, lang) if i <= 2 else (lang, br * 0.7)  # quer zur Blickrichtung, entlang des Rings
    p['marks'] = [mark('box', round(x - bw / 2, 2), round(y - bd / 2, 2), round(bw, 2), round(bd, 2), 0.6, NAHT)
                  for x, y in orte]
kern_oben = scheiben('kern_oben', 'rubber_core', 'Gummikern obere Halbschale', 'Kern oben', 30.5, OBEN, 23,
                     'Halbschale aus Naturkautschuk mit Füllstoffen. Beide Hälften sind verklebt und unter Überdruck '
                     'mit Luft gefüllt, darum springt der Ball.',
                     color=KERN, sortBias=-1)
kern_unten = scheiben('kern_unten', 'rubber_core', 'Gummikern untere Halbschale', 'Kern unten', 30.5, UNTEN, 23,
                      'Innen hohl, die Wand ist nur gut 3 mm dick. Zum Trennen den Ball mit einer Säge halbieren, '
                      'dabei entweicht zischend die Luft.',
                      color=KERN, sortBias=-1)
kern_unten[0]['marks'] = [mark('cyl', 3.3, 3.3, 54.4, fill=HOHL)]
filz_unten = scheiben('filz_unten', 'felt_cover', 'Filzbezug untere Hälfte', 'Filz unten', 33.5, UNTEN, 6,
                      'Zweites hantelförmiges Filzstück. Filz und Gummi lassen sich nicht recyceln: Restmüll.',
                      materials=[['wolle', 55], ['nylon', 40], ['klebstoff', 5]], color=FILZ)
filz_unten[0]['marks'] = [mark('cyl', 3, 3, 61, fill=FILZ_D)]

teile = filz_oben + kern_oben + kern_unten + filz_unten
gruppen = [[p['id'] for p in g] for g in (filz_oben, kern_oben, kern_unten, filz_unten)]
explodiere(teile, abstand=24, nach_liste=True, gruppen=gruppen)
skaliere_masse(teile, oid='tennis_ball', stellen=2)
schreibe('tennis_ball', teile)
