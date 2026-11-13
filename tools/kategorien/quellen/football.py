"""3D-Modell: football. Erzeugt tools/kategorien/modelle/football.json.

Fußball Größe 5 (Ø 220 mm, 430 g), genäht: 32 Waben aus PU-Kunstleder mit Schaumrücken (12 Fünfecke, 20 Sechsecke),
darunter mehrere Futterlagen aus Polyester/Baumwolle, innen eine Latexblase mit Ventil. Die Kugel ist aus gestapelten
Zylinderscheiben gebaut, jede Halbkugel bewegt sich als Gruppe. Explodiert: Hülle unten, Futter, Blase, Ventil,
Futter und Hülle oben übereinander.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

C = 110
WEISS, SCHWARZ, NAHT = '#F2F1EC', '#2A2C2E', '#C9C7C0'
FUTTER, LATEX, INNEN = '#E3D6B8', '#C99A5B', '#8C8678'


def scheiben(pid, comp, name, short, R, grenzen, mass, info, **kw):
    """Kugelabschnitt aus Zylinderscheiben zwischen den z-Grenzen (Mitte C), oberste Scheibe zuerst."""
    roh = []
    for a, b in zip(grenzen, grenzen[1:]):
        zn = min(max(C, a), b)
        roh.append((a, b, round(2 * math.sqrt(max(R * R - (zn - C) ** 2, 0)), 1)))
    vol = sum(dm * dm * (b - a) for a, b, dm in roh)
    out = []
    for i, (a, b, dm) in enumerate(reversed(roh)):
        extra = dict(kw) if i == 0 else {k: v for k, v in kw.items() if k != 'marks'} | {'label': False}
        out.append(teil(f'{pid}_{i}', comp, name, short, 'cyl', x=round(C - dm / 2, 2), y=round(C - dm / 2, 2), w=dm,
                        z=a, h=round(b - a, 2), mass=round(mass * dm * dm * (b - a) / vol, 1), info=info, **extra))
    return out


HUELLE = [['kunstleder', 75], ['schaum', 18], ['druck', 2], ['klebstoff', 5]]
FUTTERSTOFF = [['polyester', 60], ['baumwolle', 30], ['klebstoff', 10]]

huelle_oben = scheiben('huelle_oben', 'pu_cover', 'Außenhülle obere Hälfte (PU-Waben)', 'Hülle oben', 110,
                       [C, 150, 180, 200, 212, 220], 130,
                       'Waben aus PU-Kunstleder mit Schaumrücken, an den Kanten vernäht. Zum Zerlegen die Nähte '
                       'aufschneiden, dann lassen sich die Waben einzeln lösen.',
                       materials=HUELLE, color=WEISS,
                       marks=[mark('cyl', 21, 21, 40, fill=SCHWARZ), mark('cyl', 37, 37, 8, fill='#55585A'),
                              mark('box', 39, 2, 2, 19, 1, NAHT), mark('box', 39, 61, 2, 19, 1, NAHT),
                              mark('box', 2, 39, 19, 2, 1, NAHT), mark('box', 61, 39, 19, 2, 1, NAHT)])
futter_oben = scheiben('futter_oben', 'pu_cover', 'Futterlagen obere Hälfte', 'Futter oben', 107,
                       [C, 148, 178, 198, 217], 35,
                       'Drei bis vier Lagen Polyester- und Baumwollgewebe, auf die Rückseite der Waben geklebt. '
                       'Sie halten den Ball rund.',
                       material_id='polyester', materials=FUTTERSTOFF, color=FUTTER)
ventil = [teil('ventil', 'latex_bladder', 'Ventil', 'Ventil', 'cyl', x=C - 7, y=C - 7, w=14, z=204, h=15, mass=3,
               info='Gummiventil, mit der Blase verschweißt. Zum Aufpumpen die Nadel anfeuchten und gerade einstecken.',
               color='#3C3F42', marks=[mark('cyl', 5, 5, 4, fill='#151718')])]
blase = scheiben('blase', 'latex_bladder', 'Latexblase', 'Blase', 103,
                 [7, 16, 36, 70, C, 150, 184, 204, 213], 85,
                 'Dünne Hülle aus Naturlatex, die die Luft hält. Sie kommt nach dem Aufschneiden einer Naht heraus.',
                 color=LATEX)
futter_unten = scheiben('futter_unten', 'pu_cover', 'Futterlagen untere Hälfte', 'Futter unten', 107,
                        [3, 22, 42, 72, C], 35,
                        'Gewebe und Kleber lassen sich nicht vom Kunstleder trennen: Ein alter Ball gehört in den Restmüll.',
                        material_id='polyester', materials=FUTTERSTOFF, color=FUTTER,
                        marks=[mark('cyl', 3, 3, 208, fill=INNEN)])
huelle_unten = scheiben('huelle_unten', 'pu_cover', 'Außenhülle untere Hälfte', 'Hülle unten', 110,
                        [0, 8, 20, 40, 70, C], 130,
                        'Bei Nähbällen halten gewachste Polyesterfäden die Waben zusammen, bei Thermobällen sind sie '
                        'verklebt.',
                        materials=HUELLE, color=WEISS, marks=[mark('cyl', 3, 3, 214, fill=FUTTER)])

gruppen_liste = (huelle_oben, futter_oben, ventil, blase, futter_unten, huelle_unten)
teile = [p for g in gruppen_liste for p in g]
explodiere(teile, abstand=25, nach_liste=True, gruppen=[[p['id'] for p in g] for g in gruppen_liste])
skaliere_masse(teile, oid='football')
schreibe('football', teile)
