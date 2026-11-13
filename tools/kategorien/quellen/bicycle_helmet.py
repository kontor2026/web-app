"""3D-Modell: bicycle_helmet. Erzeugt tools/kategorien/modelle/bicycle_helmet.json.

Typischer In-Mold-Fahrradhelm (Größe M) aufrecht auf dem Tisch, hinten y = 0: 210 × 270 × 170 mm, ca. 300 g.
Dünne PC-Schale auf EPS-Schaum (unten bleibt ein Schaumrand frei), Lüftungsöffnungen, Schirm vorn, innen
Klettpolster, Verstellring mit Drehrad am Hinterkopf, Nylongurte mit Riemenverteilern und Kinnschnalle.
Kuppeln aus gestapelten Ellipsenscheiben (je eine Gruppe).
Explodiert: Schale hoch über dem Schaum, darunter Polster und Verstellring; Drehrad nach hinten, Gurte zur Seite.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

CX, CY, Z0 = 105, 135, 10
SCHALE = '#D8473C'
EPS, EPS_D = '#ECEBE6', '#B9B7AE'
LOCH = '#2E3236'


def ellipse(a, b, c, t):
    f = math.sqrt(max(1 - (t / c) ** 2, 0))
    return round(2 * a * f, 1), round(2 * b * f, 1)


def vents(w, d, w2, d2, n, fill, groesse=0.5):
    """n ovale Öffnungen im freien Ring zwischen Scheibe (w, d) und nächster Scheibe (w2, d2), vorn verteilt."""
    out = []
    for k in range(n):
        ang = math.radians(200 + (k + 0.5) * 140 / n)  # vorderer Bogen (y groß = vorn)
        rx, ry = (w + w2) / 4, (d + d2) / 4
        breite = max((w - w2) / 2, (d - d2) / 2) * groesse
        mx = w / 2 + rx * math.cos(ang) * -1
        my = d / 2 - ry * math.sin(ang)
        out.append(mark('cyl', round(mx - breite / 2, 1), round(my - breite * 0.4, 1), round(breite, 1),
                        round(breite * 0.8, 1), fill=fill))
    return out


def kuppel(pid, comp, name, short, a, b, c, grenzen, mass, info, fill, oben, **kw):
    """Halbellipsoid aus Scheiben (Halbachsen a, b, c ab Z0), oberste Scheibe zuerst."""
    roh = []
    for t0, t1 in zip(grenzen, grenzen[1:]):
        w, d = ellipse(a, b, c, t0)
        roh.append((t0, t1, w, d))
    vol = sum(w * d * (t1 - t0) for t0, t1, w, d in roh)
    out = []
    n = len(roh)
    for i, (t0, t1, w, d) in enumerate(reversed(roh)):
        extra = dict(kw)
        if i:
            extra['label'] = False
            w2, d2 = roh[n - i][2], roh[n - i][3]
            if i <= 3:
                extra['marks'] = vents(w, d, w2, d2, 5 - (i == 3), fill)
        else:
            extra['marks'] = oben(w, d)
        out.append(teil(f'{pid}_{i}', comp, name, short, 'cyl', x=round(CX - w / 2, 2), y=round(CY - d / 2, 2),
                        w=w, d=d, z=Z0 + t0, h=t1 - t0, mass=round(mass * w * d * (t1 - t0) / vol, 1), info=info,
                        **extra))
    return out


def schlitze(w, d, fill):
    """Lüftungsschlitze längs auf der obersten Scheibe."""
    out = []
    for fx, fl in ((0.14, 0.4), (0.32, 0.6), (0.5, 0.68), (0.68, 0.6), (0.86, 0.4)):
        sw = w * 0.08
        out.append(mark('box', round(w * fx - sw / 2, 1), round(d * (1 - fl) / 2, 1), round(sw, 1), round(d * fl, 1),
                        round(sw / 2, 1), fill))
    return out


GRENZEN_S = [14, 48, 80, 106, 128, 146, 160]
GRENZEN_E = [0, 48, 80, 106, 128, 146, 157]
schale = kuppel('schale', 'pc_shell', 'Außenschale aus Polycarbonat', 'Schale', 105, 135, 160, GRENZEN_S,
                40, 'Hauchdünne PC-Schale, im Werk direkt mit dem Schaum verbunden (In-Mold). Sie lässt sich nur mit '
                    'einem flachen Werkzeug abhebeln.', LOCH, lambda w, d: schlitze(w, d, LOCH),
                color=SCHALE, sortBias=4)
eps = kuppel('eps', 'eps_liner', 'Schaumkern aus EPS', 'EPS-Schaum', 102, 132, 157, GRENZEN_E,
             160, 'Expandiertes Polystyrol, das bei einem Sturz zusammengedrückt wird und so den Aufprall dämpft. '
                  'Nach jedem Sturz den Helm ersetzen: Der Schaum erholt sich nicht.',
             EPS_D, lambda w, d: schlitze(w, d, EPS_D), color=EPS)
POLSTER, POLSTER_H = '#3E4349', '#565C63'
GURT, GURT_H = '#1F2328', '#30353B'

teile = schale + eps + [
    teil('schirm', 'pc_shell', 'Schirm', 'Schirm', 'box', x=55, y=228, w=100, d=48, z=104, h=4, r=22, mass=12,
         color='#2B2F33', explode=[0, 120, 0],
         info='Kleiner Sonnenschirm vorn, nur mit zwei Clips in den Schaum gesteckt. Abziehen und separat entsorgen.',
         marks=[mark('box', 10, 4, 80, 6, 3, '#43484E'), mark('cyl', 14, 30, 8, fill='#55595E'),
                mark('cyl', 78, 30, 8, fill='#55595E')]),
    teil('polster', 'eps_liner', 'Innenpolster', 'Polster', 'box',
         material_id='pu_foam', x=45, y=55, w=120, d=160, z=125, h=6, r=30, mass=10,
         materials=[['schaum', 70], ['polyester', 25], ['klebstoff', 5]], color=POLSTER,
         info='Weiche Schaumpolster mit Stoffbezug, mit Klett am Schaum befestigt. Abziehen und waschen.',
         marks=[mark('box', 10, 8, 100, 30, 12, POLSTER_H), mark('box', 4, 55, 30, 70, 12, POLSTER_H),
                mark('box', 86, 55, 30, 70, 12, POLSTER_H), mark('box', 10, 132, 100, 22, 10, POLSTER_H)]),
    teil('verstellring', 'plastic_buckles', 'Verstellring', 'Verstellring', 'cyl',
         x=25, y=20, w=160, d=200, z=45, h=18, mass=30, color='#2B2F33',
         info='Kunststoffband, das um den Hinterkopf läuft und mit dem Drehrad enger gestellt wird. '
              'Am Schaum nur eingesteckt.',
         marks=[mark('cyl', 8, 8, 144, 184, fill='#8C8F92')]),
    teil('drehrad', 'plastic_buckles', 'Drehrad', 'Drehrad', 'cyl',
         x=90, y=8, w=30, z=45, h=14, mass=8, color='#C8302C', explode=[0, -60, 0],
         info='Rad mit Zahnstange im Inneren, das den Verstellring strafft. Mit Schraubenzieher aufclipsen.',
         marks=[mark('cyl', 5, 5, 20, fill='#A12520'), mark('box', 13, 3, 4, 24, 2, '#7E1C18')]),
    # Gurte: assembled unter dem Helm verstaut, explodiert flach daneben ausgelegt
    teil('gurt_links', 'nylon_straps', 'Gurt links (Y-Gurt)', 'Gurte', 'box',
         x=40, y=60, w=14, d=160, z=0, h=2, r=3, mass=12, color=GURT, explode=[260, 0, 0],
         info='Nylon-Gurtband, vorn und hinten im Schaum verankert. Zum Trennen dicht am Helm abschneiden.',
         marks=[mark('box', 3, 4, 8, 152, 2, GURT_H)]),
    teil('gurt_rechts', 'nylon_straps', 'Gurt rechts (Y-Gurt)', 'Gurt', 'box',
         x=156, y=60, w=14, d=160, z=0, h=2, r=3, mass=12, color=GURT, explode=[260, 0, 0], label=False,
         info='Gegenstück auf der anderen Seite.', marks=[mark('box', 3, 4, 8, 152, 2, GURT_H)]),
    teil('verteiler_links', 'plastic_buckles', 'Riemenverteiler links', 'Verteiler', 'box',
         x=39, y=150, w=16, d=24, z=2, h=5, r=3, mass=3, color='#2B2F33', explode=[260, 0, 0],
         info='Kunststoffschieber unter dem Ohr, an dem sich vorderer und hinterer Gurt treffen.',
         marks=[mark('box', 4, 4, 8, 16, 2, '#4A4F55')]),
    teil('verteiler_rechts', 'plastic_buckles', 'Riemenverteiler rechts', 'Verteiler', 'box',
         x=155, y=150, w=16, d=24, z=2, h=5, r=3, mass=3, color='#2B2F33', explode=[260, 0, 0], label=False,
         info='Gegenstück auf der anderen Seite.', marks=[mark('box', 4, 4, 8, 16, 2, '#4A4F55')]),
    teil('kinnriemen', 'nylon_straps', 'Kinnriemen', 'Kinnriemen', 'box',
         x=54, y=214, w=102, d=12, z=0, h=2, r=3, mass=6, color=GURT, explode=[260, 0, 0],
         info='Verbindet beide Seiten unter dem Kinn. Mit dem Schieber so einstellen, dass ein Finger darunter passt.',
         marks=[mark('box', 4, 3, 94, 6, 2, GURT_H)]),
    teil('schnalle', 'plastic_buckles', 'Kinnschnalle', 'Schnalle', 'box',
         x=90, y=208, w=30, d=24, z=2, h=8, r=5, mass=8, color='#1B1E21', explode=[260, 0, 0],
         info='Steckschnalle aus PP: Zum Öffnen die beiden Seitenlaschen zusammendrücken. Hinter der Schnalle '
              'den Gurt abschneiden, wenn man sie getrennt entsorgt.',
         marks=[mark('box', 4, 5, 12, 14, 3, '#3A3F44'), mark('box', 18, 4, 9, 16, 2, '#2E3237')]),
]
ab = {p['id']: 125 for p in schale}
ab.update({p['id']: 115 for p in eps})
explodiere(teile, abstand=25, nach_liste=True, abstaende=ab,
           gruppen=[[p['id'] for p in schale], [p['id'] for p in eps]])
skaliere_masse(teile, oid='bicycle_helmet')
schreibe('bicycle_helmet', teile)
