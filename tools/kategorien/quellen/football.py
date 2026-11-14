"""3D-Modell: football. Erzeugt tools/kategorien/modelle/football.json.

Fußball Größe 5 (Ø 220 mm, 430 g), genäht: 32 Waben aus PU-Kunstleder mit Schaumrücken (12 Fünfecke, 20 Sechsecke),
darunter mehrere Futterlagen aus Polyester/Baumwolle, innen eine Latexblase mit Ventil. Die Kugel ist aus gestapelten
Zylinderscheiben gebaut, jede Halbkugel bewegt sich als Gruppe. Explodiert: Hülle unten, Futter, Blase, Futter und
Hülle oben übereinander, das Ventil seitlich daneben.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

C = 110
WEISS, SCHWARZ, NAHT = '#F2F1EC', '#2A2C2E', '#C9C7C0'
FUTTER, LATEX, INNEN = '#E3D6B8', '#C99A5B', '#8C8678'


OBEN = [C, 145, 172, 192, 206, 215, 220]
UNTEN = [0, 5, 14, 28, 48, 75, C]


def scheiben(pid, comp, name, short, R, grenzen, mass, info, punkte=False, **kw):
    """Kugelabschnitt aus Zylinderscheiben zwischen den z-Grenzen (Mitte C), oberste Scheibe zuerst.

    Alle Lagen nutzen dieselben Grenzen (auf ihren Radius gekappt), so bleibt jede innere Lage in der äußeren.
    punkte=True: schwarze Fünfeck-Waben auf dem sichtbaren Ring jeder Scheibe."""
    roh = []
    for a, b in zip(grenzen, grenzen[1:]):
        a, b = max(a, C - R), min(b, C + R)
        if b - a < 2:
            continue
        zn = min(max(C, a), b)
        roh.append((a, b, round(2 * math.sqrt(max(R * R - (zn - C) ** 2, 0)), 1)))
    vol = sum(dm * dm * (b - a) for a, b, dm in roh)
    out = []
    oben = list(reversed(roh))
    for i, (a, b, dm) in enumerate(oben):
        extra = dict(kw) if i == 0 else {k: v for k, v in kw.items() if k != 'marks'} | {'label': False}
        if punkte and 0 < i and a >= C:
            innen = oben[i - 1][2]
            rr, br = (dm + innen) / 4, min((dm - innen) / 2 * 0.6, 14)
            n = 5 if i % 2 else 6
            extra['marks'] = [mark('cyl', round(dm / 2 + rr * math.cos(2 * math.pi * (k + 0.5 * (i % 2)) / n) - br / 2, 1),
                                   round(dm / 2 + rr * math.sin(2 * math.pi * (k + 0.5 * (i % 2)) / n) - br / 2, 1),
                                   round(br, 1), fill=SCHWARZ) for k in range(n)]
        out.append(teil(f'{pid}_{i}', comp, name, short, 'cyl', x=round(C - dm / 2, 2), y=round(C - dm / 2, 2), w=dm,
                        z=a, h=round(b - a, 2), mass=round(mass * dm * dm * (b - a) / vol, 1), info=info, **extra))
    return out


HUELLE = [['kunstleder', 75], ['schaum', 18], ['druck', 2], ['klebstoff', 5]]
FUTTERSTOFF = [['polyester', 60], ['baumwolle', 30], ['klebstoff', 10]]

huelle_oben = scheiben('huelle_oben', 'pu_cover', 'Außenhülle obere Hälfte (PU-Waben)', 'Hülle oben', 110,
                       OBEN, 130,
                       'Waben aus PU-Kunstleder mit Schaumrücken, an den Kanten vernäht. Zum Zerlegen die Nähte '
                       'aufschneiden, dann lassen sich die Waben einzeln lösen.',
                       materials=HUELLE, color=WEISS, punkte=True,
                       marks=[mark('cyl', 9.4, 9.4, 40, fill=SCHWARZ), mark('cyl', 40, 18, 5, fill='#55585A')])
futter_oben = scheiben('futter_oben', 'pu_cover', 'Futterlagen obere Hälfte', 'Futter oben', 107,
                       OBEN, 35,
                       'Drei bis vier Lagen Polyester- und Baumwollgewebe, auf die Rückseite der Waben geklebt. '
                       'Sie halten den Ball rund.',
                       material_id='polyester', materials=FUTTERSTOFF, color=FUTTER, sortBias=-1)
ventil = [teil('ventil', 'latex_bladder', 'Ventil', 'Ventil', 'cyl', x=C - 7, y=C - 7, w=14, z=204, h=15, mass=3,
               info='Gummiventil, mit der Blase verschweißt. Zum Aufpumpen die Nadel anfeuchten und gerade einstecken.',
               color='#3C3F42', sortBias=-3, marks=[mark('cyl', 5, 5, 4, fill='#151718')])]
blase = scheiben('blase', 'latex_bladder', 'Latexblase', 'Blase', 103,
                 UNTEN + OBEN[1:], 85,
                 'Dünne Hülle aus Naturlatex, die die Luft hält. Sie kommt nach dem Aufschneiden einer Naht heraus.',
                 color=LATEX, sortBias=-2)
futter_unten = scheiben('futter_unten', 'pu_cover', 'Futterlagen untere Hälfte', 'Futter unten', 107,
                        UNTEN, 35,
                        'Gewebe und Kleber lassen sich nicht vom Kunstleder trennen: Ein alter Ball gehört in den Restmüll.',
                        material_id='polyester', materials=FUTTERSTOFF, color=FUTTER, sortBias=-1,
                        marks=[mark('cyl', 3, 3, 208, fill=INNEN)])
huelle_unten = scheiben('huelle_unten', 'pu_cover', 'Außenhülle untere Hälfte', 'Hülle unten', 110,
                        UNTEN, 130,
                        'Bei Nähbällen halten gewachste Polyesterfäden die Waben zusammen, bei Thermobällen sind sie '
                        'verklebt.',
                        materials=HUELLE, color=WEISS, marks=[mark('cyl', 3, 3, 214, fill=FUTTER)])

gruppen_liste = (huelle_oben, futter_oben, ventil, blase, futter_unten, huelle_unten)
teile = [p for g in gruppen_liste for p in g]
explodiere(teile, abstand=25, nach_liste=True, gruppen=[[p['id'] for p in g] for g in gruppen_liste])
# Ventil seitlich neben die Oberseite der Blase ziehen, sonst verschwindet es hinter dem Futter
v = next(p for p in teile if p['id'] == 'ventil')
v['explode'] = [170, 0, blase[0]['explode'][2] + 90]
skaliere_masse(teile, oid='football')
schreibe('football', teile)
