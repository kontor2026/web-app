"""3D-Modell: bicycle_helmet. Erzeugt tools/kategorien/modelle/bicycle_helmet.json.

Typischer In-Mold-Fahrradhelm (Größe M) aufrecht auf dem Tisch, hinten y = 0: 210 × 270 × 170 mm, ca. 300 g.
Dünne PC-Schale auf EPS-Schaum, innen Klettpolster, ein Verstellring mit Drehrad am Hinterkopf, Nylongurte mit
Riemenverteilern und Kinnschnalle. Kuppeln aus gestapelten Ellipsenscheiben (je eine Gruppe).
Explodiert: Schale über dem Schaum, darunter Polster und Verstellring; Drehrad nach hinten, Gurte zur Seite.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

CX, CY, Z0 = 105, 135, 10
SCHALE, SCHALE_D = '#D8473C', '#A8322A'
EPS, EPS_D = '#ECEBE6', '#B9B7AE'


def kuppel(pid, comp, name, short, a, b, c, grenzen, mass, info, marks=None, **kw):
    """Halbellipsoid aus Scheiben (Halbachsen a, b, c ab Z0), oberste Scheibe zuerst."""
    roh = []
    for t0, t1 in zip(grenzen, grenzen[1:]):
        f = math.sqrt(max(1 - (t0 / c) ** 2, 0))
        roh.append((t0, t1, round(2 * a * f, 1), round(2 * b * f, 1)))
    vol = sum(w * d * (t1 - t0) for t0, t1, w, d in roh)
    out = []
    for i, (t0, t1, w, d) in enumerate(reversed(roh)):
        extra = dict(kw)
        if i:
            extra['label'] = False
        elif marks:
            extra['marks'] = marks(w, d)
        out.append(teil(f'{pid}_{i}', comp, name, short, 'cyl', x=round(CX - w / 2, 2), y=round(CY - d / 2, 2),
                        w=w, d=d, z=Z0 + t0, h=t1 - t0, mass=round(mass * w * d * (t1 - t0) / vol, 1), info=info,
                        **extra))
    return out


def schlitze(w, d, fill):
    """Fünf Lüftungsschlitze längs auf der Kuppel."""
    out = []
    for fx, fl in ((0.12, 0.45), (0.3, 0.62), (0.5, 0.7), (0.7, 0.62), (0.88, 0.45)):
        sw = w * 0.09
        out.append(mark('box', round(w * fx - sw / 2, 1), round(d * (1 - fl) / 2, 1), round(sw, 1), round(d * fl, 1),
                        round(sw / 2, 1), fill))
    return out


schale = kuppel('schale', 'pc_shell', 'Außenschale aus Polycarbonat', 'Schale', 105, 135, 160, [0, 50, 95, 125, 160],
                40, 'Hauchdünne PC-Schale, im Werk direkt mit dem Schaum verbunden (In-Mold). Sie lässt sich nur mit '
                    'einem flachen Werkzeug abhebeln.',
                marks=lambda w, d: schlitze(w, d, '#3A3F44'),
                color=SCHALE)
eps = kuppel('eps', 'eps_liner', 'Schaumkern aus EPS', 'EPS-Schaum', 102, 132, 156, [0, 50, 95, 123, 156],
             160, 'Expandiertes Polystyrol, das bei einem Sturz zusammengedrückt wird und so den Aufprall dämpft. '
                  'Nach jedem Sturz den Helm ersetzen: Der Schaum erholt sich nicht.',
             marks=lambda w, d: schlitze(w, d, EPS_D), color=EPS)
POLSTER = '#3E4349'

teile = schale + eps + [
    teil('polster', 'eps_liner', 'Innenpolster', 'Polster', 'box',
         material_id='pu_foam', x=45, y=55, w=120, d=160, z=125, h=6, r=30, mass=10,
         materials=[['schaum', 70], ['polyester', 25], ['klebstoff', 5]], color=POLSTER,
         info='Weiche Schaumpolster mit Stoffbezug, mit Klett am Schaum befestigt. Abziehen und waschen.',
         marks=[mark('box', 10, 8, 100, 30, 12, '#565C63'), mark('box', 4, 55, 30, 70, 12, '#565C63'),
                mark('box', 86, 55, 30, 70, 12, '#565C63'), mark('box', 10, 132, 100, 22, 10, '#565C63')]),
    teil('verstellring', 'plastic_buckles', 'Verstellring', 'Verstellring', 'cyl',
         x=25, y=20, w=160, d=200, z=45, h=18, mass=30, color='#2B2F33',
         info='Kunststoffband, das um den Hinterkopf läuft und mit dem Drehrad enger gestellt wird. '
              'Am Schaum nur eingesteckt.',
         marks=[mark('cyl', 8, 8, 144, 184, fill='#8C8F92')]),
    teil('drehrad', 'plastic_buckles', 'Drehrad', 'Drehrad', 'cyl',
         x=90, y=8, w=30, z=45, h=14, mass=8, color='#C8302C', explode=[0, -45, 0],
         info='Rad mit Zahnstange im Inneren, das den Verstellring strafft. Mit Schraubenzieher aufclipsen.',
         marks=[mark('cyl', 5, 5, 20, fill='#A12520'), mark('box', 13, 3, 4, 24, 2, '#7E1C18')]),
    teil('gurte', 'nylon_straps', 'Kinn- und Seitengurte', 'Gurte', 'box',
         x=60, y=80, w=90, d=120, z=0, h=3, r=4, mass=30, color='#1F2328', explode=[250, 0, 0],
         info='Nylon-Gurtband, an den Schaumkern geklebt oder eingegossen. Zum Trennen dicht am Helm abschneiden.',
         marks=[mark('box', 4, 0, 16, 120, 2, '#30353B'), mark('box', 70, 0, 16, 120, 2, '#30353B'),
                mark('box', 37, 60, 16, 60, 2, '#30353B')]),
    teil('verteiler_links', 'plastic_buckles', 'Riemenverteiler links', 'Verteiler', 'box',
         x=38, y=120, w=16, d=22, z=0, h=6, r=3, mass=3, color='#2B2F33', explode=[250, 0, 0],
         info='Kunststoffschieber unter dem Ohr, an dem sich vorderer und hinterer Gurt treffen.',
         marks=[mark('box', 4, 4, 8, 14, 2, '#4A4F55')]),
    teil('verteiler_rechts', 'plastic_buckles', 'Riemenverteiler rechts', 'Verteiler', 'box',
         x=156, y=120, w=16, d=22, z=0, h=6, r=3, mass=3, color='#2B2F33', explode=[250, 0, 0], label=False,
         info='Gegenstück auf der anderen Seite.', marks=[mark('box', 4, 4, 8, 14, 2, '#4A4F55')]),
    teil('schnalle', 'plastic_buckles', 'Kinnschnalle', 'Schnalle', 'box',
         x=92, y=208, w=26, d=34, z=0, h=9, r=5, mass=8, color='#1B1E21', explode=[250, 0, 0],
         info='Steckschnalle aus PP: Zum Öffnen die beiden Seitenlaschen zusammendrücken. Hinter der Schnalle '
              'den Gurt abschneiden, wenn man sie getrennt entsorgt.',
         marks=[mark('box', 5, 4, 16, 12, 3, '#3A3F44'), mark('box', 2, 20, 22, 10, 2, '#2E3237')]),
]
explodiere(teile, abstand=25, nach_liste=True,
           gruppen=[[p['id'] for p in schale], [p['id'] for p in eps]])
skaliere_masse(teile, oid='bicycle_helmet')
schreibe('bicycle_helmet', teile)
