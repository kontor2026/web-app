"""3D-Modell: baseball_cap. Erzeugt tools/kategorien/modelle/baseball_cap.json."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Basecap aufrecht auf dem Tisch, Verschluss hinten (y = 0), Schirm vorne (bis y = 250). 190 × 250 × 110 mm.
# Die Krone (Kopföffnung 190 × 185 mm) ist als Kuppel aus zwölf Ellipsenscheiben gestapelt, vorne steiler als
# hinten. Sie hebt sich als Ganzes ab, darunter liegt das Schweißband. Der Schirm (Ellipse, hintere Hälfte unter
# der Krone) wird nach vorne gezogen und in Bezug, Einlage und Unterseite aufgefächert, der Klickverschluss nach
# hinten.
STOFF = '#22385A'
NAHT = '#1A2C47'
OESE = '#1C2C40'
BW = [['baumwolle', 100]]
CX = 95  # Mitte in x

# Kuppelprofil: Ellipsoid, vorne fast senkrecht, hinten flacher. (z, h, y_hinten, y_vorne, breite) je Scheibe,
# oben feiner unterteilt, damit die Foto-Ansicht die Scheiben zu einer runden Kuppel verbindet.
HK = 106
GRENZEN = [0, 18, 34, 48, 60, 70, 79, 86, 92, 97, 101, 104, HK]


def profil(z):
    t = z / HK
    k = max(0.0, 1 - t ** 2.2) ** 0.5
    w = 190 * k
    yb = 0 + 105 * (1 - k) ** 0.9
    yf = 185 - 75 * (1 - k) ** 1.3
    return yb, yf, w


SCHEIBEN = []
for a, b in zip(GRENZEN, GRENZEN[1:]):
    yb, yf, w = profil(a + 0.35 * (b - a))
    w, yb, yf = max(w, 24), min(yb, 96), max(yf, 120)
    SCHEIBEN.append((a, b - a, round(yb, 1), round(yf, 1), round(w, 1)))
VOL = sum(h * (yf - yb) * w for _, h, yb, yf, w in SCHEIBEN)


def scheibe(i, z, h, yb, yf, w):
    d = round(yf - yb, 1)
    marks = [mark('box', round(w / 2 - 0.75, 1), 0, 1.5, d, 0, NAHT, zeichnung=True)]  # Mittelnaht vorne/hinten
    if i == 4:  # gestickte Lüftungsösen, je eine pro Bahn (nur Zeichnung, in der Kuppel verdeckt)
        for a in (30, 90, 150, 210, 270, 330):
            marks.append(mark('cyl', round(w / 2 + 0.86 * w / 2 * math.cos(math.radians(a)) - 3, 1),
                              round(d / 2 + 0.86 * d / 2 * math.sin(math.radians(a)) - 3, 1), 6, fill=OESE,
                              zeichnung=True))
    oben = i == len(SCHEIBEN) - 1
    return teil(f'krone_{i + 1}', 'cotton_fabric', 'Krone aus sechs Stoffbahnen' if i == 0 else f'Krone, Lage {i + 1}',
                'Krone', 'cyl', x=round(CX - w / 2, 1), y=yb, w=w, d=d, z=z, h=h,
                mass=round(64 * h * d * w / VOL, 1),
                materials=[['baumwolle', 90], ['polyester', 10]] if i == 0 else BW, color=STOFF, label=i == 0,
                info='Sechs dreieckige Bahnen aus Baumwoll-Twill, oben zusammengenäht. Die zwei vorderen Bahnen sind '
                     'innen mit Vlies versteift. Tragbare Caps in die Altkleidersammlung.' if i == 0 else
                     'Teil der Kuppel aus Stoffbahnen.' + (' Oben laufen alle Nähte unter dem Knopf zusammen.' if oben else ''),
                marks=marks)


teile = [
    teil('knopf', 'cotton_fabric', 'Stoffbezogener Knopf', 'Knopf', 'cyl', material_id='steel',
         x=CX - 7, y=round((SCHEIBEN[-1][2] + SCHEIBEN[-1][3]) / 2 - 7, 1), w=14, z=HK - 1.5, h=5, mass=1.5, materials=[['stahl', 70], ['baumwolle', 30]], color=STOFF,
         info='Metallknopf mit Stoffbezug, deckt die Stelle ab, an der die sechs Bahnen oben zusammenlaufen.',
         marks=[mark('cyl', 3, 3, 8, fill=NAHT)]),
] + [scheibe(i, *s) for i, s in reversed(list(enumerate(SCHEIBEN)))] + [
    teil('etikett', 'cotton_fabric', 'Pflegeetikett', 'Etikett', 'box', material_id='polyester',
         x=100, y=14, w=20, d=0.3, z=8, h=30, r=0, mass=0.5, materials=[['polyester', 100]], color='#F4F2EE',
         explode=[0, -140, 0],
         info='Polyester-Etikett innen hinten am Schweißband. Vor dem Recycling abschneiden.'),
    teil('schweissband', 'cotton_fabric', 'Schweißband', 'Schweißband', 'cyl',
         x=8, y=8, w=174, d=169, z=0, h=25, mass=8, materials=[['baumwolle', 60], ['polyester', 40]], color='#3A3F44',
         info='Stoffband mit Einlage innen am Rand. Es saugt Schweiß auf und lässt sich mit der Schere heraustrennen.',
         marks=[mark('cyl', 5, 5, 164, 159, fill='#4A5056')]),
    teil('verschluss_loch', 'plastic_buckles', 'Verschlussband mit Löchern', 'Verschluss', 'box',
         x=58, y=10, w=37, d=3, z=6, h=16, r=1, mass=3, color='#22272B', explode=[0, -80, 0],
         info='Klickverschluss aus Polypropylen. Die Bänder direkt hinter der Naht abschneiden.'),
    teil('verschluss_noppe', 'plastic_buckles', 'Verschlussband mit Noppen', 'Noppenband', 'box',
         x=95, y=10, w=37, d=3.5, z=6, h=16, r=1, mass=3, color='#22272B', explode=[0, -80, 0],
         info='Die Noppen rasten in die Löcher des Gegenstücks ein. Reines PP, ab in die Wertstoffsammlung.'),
    teil('schirm_oben', 'cotton_fabric', 'Schirmbezug oben', 'Schirmbezug', 'cyl',
         x=CX - 88, y=140, w=176, d=110, z=3.5, h=1.5, mass=5, materials=BW, color=STOFF, explode=[0, 130, 60],
         info='Stoff über dem Schirm, mit mehreren parallelen Nähten auf die Einlage gesteppt.',
         marks=[m for k in range(4) for m in (mark('cyl', 6 + 7 * k, 6 + 7 * k, 164 - 14 * k, 98 - 14 * k, fill=NAHT, zeichnung=True),
                                            mark('cyl', 7.5 + 7 * k, 7.5 + 7 * k, 161 - 14 * k, 95 - 14 * k,
                                                 fill=STOFF, zeichnung=True))]),
    teil('schirm_einlage', 'visor_insert', 'Schirmeinlage', 'Einlage', 'cyl',
         x=CX - 86, y=142, w=172, d=106, z=1.5, h=2, mass=12, color='#E8E6E1', explode=[0, 130, 30],
         info='Gebogene Platte aus Polypropylen (früher Pappe). Schirmnaht aufschneiden und herausziehen.'),
    teil('schirm_unten', 'cotton_fabric', 'Schirmbezug unten', 'Schirm unten', 'cyl',
         x=CX - 88, y=140, w=176, d=110, z=0, h=1.5, mass=5, materials=BW, color='#3F5F84',
         explode=[0, 130, 0], info='Unterseite des Schirms, oft in einer zweiten Farbe. Mit dem Bezug oben vernäht.'),
]

explodiere(teile, abstand=40, gruppen=[[f'krone_{i + 1}' for i in range(len(SCHEIBEN))]], abstaende={'knopf': 25},
           nach_liste=True)
skaliere_masse(teile, oid='baseball_cap')
schreibe('baseball_cap', teile)
