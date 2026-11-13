"""3D-Modell: plush_toy. Erzeugt tools/kategorien/modelle/plush_toy.json.

Sitzender Teddybär, 200 × 150 × 250 mm (Gesicht vorn bei y groß), Plüsch aus Polyester, gefüllt mit
Polyesterwatte, Sicherheitsaugen und Nase aus Kunststoff mit Sicherungsscheibe. Rumpf (birnenförmig) und Kopf
(kugelig) aus gestapelten Ellipsenscheiben, Schnauze vorn, Ohren oben, Arme seitlich nach vorn hängend,
Beine liegen nach vorn ausgestreckt mit heller Fußsohle. Füllungen von Rumpf und Kopf als eigene Teile.
Explosion: Stapel nach Liste (Ohren, Kopfhülle, Kopffüllung, Rumpfhülle, Rumpffüllung);
Arme seitlich, Beine, Augen und Nase nach vorne, Pflegeetikett nach rechts herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

FELL = '#B07A45'
FELL_D = '#9C6A3B'
HELL = '#D9B38A'
WATTE = '#F4F2EE'
WATTE_D = '#E3DFD6'
AUGE = '#1C1D1F'
CX = 100


def scheiben(pid, comp, name, short, cy, stufen, mass, info, color, label=True, marks=None, **kw):
    """Stapel aus Ellipsenscheiben um (CX, cy): stufen = [(z, h, w, d), ...] von oben nach unten."""
    vol = sum(h * w * d for _, h, w, d in stufen)
    out = []
    for i, (z, h, w, d) in enumerate(stufen):
        extra = dict(kw)
        if i or not label:
            extra['label'] = False
        if marks and marks.get(i):
            extra['marks'] = marks[i]
        out.append(teil(f'{pid}_{i}', comp, name, short, 'cyl', x=CX - w / 2, y=cy - d / 2, w=w, d=d, z=z, h=h,
                        mass=round(mass * h * w * d / vol, 1), info=info, color=color, **extra))
    return out


# Kopf: Mittelpunkt y = 72
kopf = scheiben('kopf', 'polyester_plush', 'Kopf (Plüschhülle)', 'Kopf', 72,
                [(222, 10, 66, 58), (205, 17, 102, 88), (170, 35, 120, 104), (150, 20, 108, 94), (140, 10, 76, 66)],
                40, 'Plüschstoff aus Polyester: ein gewebter Grund mit langen, aufgeschnittenen Fasern. An der Halsnaht '
                    'mit dem Rumpf vernäht.', FELL, sortBias=3,
                marks={0: [mark('box', 31, 4, 4, 50, 2, FELL_D)], 1: [mark('box', 49, 2, 4, 14, 2, FELL_D)]})
kopffuellung = scheiben('kopffuellung', 'polyester_fill', 'Füllung Kopf', 'Füllung Kopf', 72,
                        [(205, 14, 90, 78), (170, 35, 112, 96), (152, 18, 98, 84)],
                        50, 'Lockere Polyesterwatte, von Hand oder maschinell durch eine Naht gestopft. Naht auftrennen, '
                            'herausziehen und als Füllung weiterverwenden.', WATTE,
                        marks={0: [mark('cyl', 15, 12, 34, 24, fill=WATTE_D), mark('cyl', 46, 36, 30, 26, fill=WATTE_D)]})
# Rumpf: Mittelpunkt y = 68, birnenförmig
rumpf = scheiben('rumpf', 'polyester_plush', 'Rumpf (Plüschhülle)', 'Rumpf', 68,
                 [(125, 15, 78, 66), (100, 25, 104, 88), (60, 40, 124, 104), (20, 40, 134, 112), (0, 20, 116, 98)],
                 60, 'Größtes Schnittteil mit der Stopfnaht am Rücken. Saubere Kuscheltiere lieber verschenken; '
                     'sonst Naht aufschneiden, Füllung und Kunststoffteile trennen, Rest in den Restmüll.', FELL,
                 sortBias=3, marks={1: [mark('cyl', 32, 58, 40, 26, fill=HELL)], 2: [mark('box', 60, 2, 4, 12, 2, FELL_D)]})
rumpffuellung = scheiben('rumpffuellung', 'polyester_fill', 'Füllung Rumpf', 'Füllung Rumpf', 68,
                         [(100, 25, 96, 80), (60, 40, 116, 96), (20, 40, 126, 104), (4, 16, 108, 90)],
                         90, 'Der größte Teil der Watte. Manche Kuscheltiere haben unten zusätzlich ein Säckchen mit '
                             'Kunststoffgranulat, damit sie sitzen.', WATTE,
                         marks={0: [mark('cyl', 18, 14, 34, 26, fill=WATTE_D), mark('cyl', 46, 40, 32, 28, fill=WATTE_D)]})

teile = [
    teil('ohr_links', 'polyester_plush', 'Ohren', 'Ohren', 'cyl',
         x=36, y=58, w=38, d=18, z=212, h=34, mass=3, color=FELL,
         info='Plüschtaschen, mit etwas Watte gefüllt und am Kopf angenäht.',
         marks=[mark('cyl', 7, 5, 24, 9, fill=HELL)]),
    teil('ohr_rechts', 'polyester_plush', 'Ohr rechts', 'Ohr', 'cyl', label=False,
         x=126, y=58, w=38, d=18, z=212, h=34, mass=3, color=FELL,
         info='Zweites Ohr.', marks=[mark('cyl', 7, 5, 24, 9, fill=HELL)]),
] + kopf + [
    teil('schnauze', 'polyester_plush', 'Schnauze', 'Schnauze', 'cyl',
         x=72, y=124, w=56, d=24, z=163, h=30, mass=6, color=HELL, sortBias=4,
         info='Kurzfloriger heller Plüsch, eigenes Schnittteil, auf dem Nase und Mundnaht sitzen.',
         marks=[mark('box', 27, 15, 2, 8, 1, '#6B4A2B')]),
    teil('auge_links', 'plastic_eyes', 'Sicherheitsaugen', 'Augen', 'cyl',
         x=70, y=116, w=13, d=8, z=192, h=13, mass=1.5, color=AUGE, sortBias=5,
         info='Kunststoffaugen mit Schaft, innen mit einer Sicherungsscheibe festgeklemmt, damit Kinder sie nicht '
              'abreißen. Zum Trennen den Stoff rundherum aufschneiden.',
         marks=[mark('cyl', 3, 2, 4, 3, fill='#FFFFFF')]),
    teil('auge_rechts', 'plastic_eyes', 'Auge rechts', 'Auge', 'cyl', label=False,
         x=117, y=116, w=13, d=8, z=192, h=13, mass=1.5, color=AUGE, sortBias=5,
         info='Zweites Auge.', marks=[mark('cyl', 3, 2, 4, 3, fill='#FFFFFF')]),
    teil('nase', 'plastic_eyes', 'Nase', 'Nase', 'cyl',
         x=90, y=127, w=20, d=11, z=193, h=6, mass=2, color='#2B2D2F', sortBias=5,
         info='Ebenfalls Kunststoff mit Sicherungsscheibe. Bei manchen Tieren ist die Nase nur aufgestickt.',
         marks=[mark('cyl', 5, 2, 6, 3, fill='#55585C')]),
] + kopffuellung + rumpf + [
    # Arme: Oberarm an der Schulter, Unterarm mit Pfote weiter vorn und tiefer
    teil('arm_links', 'polyester_plush', 'Arme', 'Arme', 'cyl',
         x=24, y=48, w=36, d=48, z=88, h=40, mass=7, color=FELL, sortBias=4,
         info='Gefüllte Plüschschläuche, in die Seitennähte des Rumpfs eingenäht.'),
    teil('pfote_links', 'polyester_plush', 'Unterarm mit Pfote links', 'Arm', 'cyl', label=False,
         x=20, y=76, w=36, d=50, z=52, h=36, mass=5, color=FELL, sortBias=4,
         info='Unterarm mit heller Pfote.', marks=[mark('cyl', 6, 26, 24, 20, fill=HELL)]),
    teil('arm_rechts', 'polyester_plush', 'Arm rechts', 'Arm', 'cyl', label=False,
         x=140, y=48, w=36, d=48, z=88, h=40, mass=7, color=FELL, sortBias=4, info='Zweiter Arm.'),
    teil('pfote_rechts', 'polyester_plush', 'Unterarm mit Pfote rechts', 'Arm', 'cyl', label=False,
         x=144, y=76, w=36, d=50, z=52, h=36, mass=5, color=FELL, sortBias=4,
         info='Unterarm mit heller Pfote.', marks=[mark('cyl', 6, 26, 24, 20, fill=HELL)]),
    teil('etikett', 'polyester_plush', 'Pflegeetikett', 'Etikett', 'box',
         x=160, y=24, w=34, d=16, z=0, h=0.6, r=1, mass=1, materials=[['polyester', 95], ['druck', 5]],
         color='#F4F2EE',
         info='Eingenähtes Etikett mit Material, Waschhinweis und CE-Zeichen. Es besteht wie der Plüsch aus Polyester '
              'und darf dranbleiben.',
         marks=[mark('box', 14, 3, 17, 2, 0, '#9AA0A6'), mark('box', 14, 7, 17, 2, 0, '#9AA0A6'),
                mark('box', 14, 11, 12, 2, 0, '#9AA0A6')]),
    # Beine: liegen nach vorn ausgestreckt, Fuß vorn etwas höher, Sohle als helle Fläche an der Vorderseite
    teil('bein_links', 'polyester_plush', 'Beine', 'Beine', 'cyl',
         x=40, y=74, w=54, d=42, z=0, h=40, mass=10, color=FELL, sortBias=4,
         info='Gefüllte Beine mit eingesetzter Fußsohle aus hellem Stoff.'),
    teil('fuss_links', 'polyester_plush', 'Fuß links', 'Fuß', 'cyl', label=False,
         x=42, y=116, w=50, d=29, z=0, h=50, mass=5, color=FELL, sortBias=5,
         info='Fuß mit eingesetzter Sohle.'),
    teil('sohle_links', 'polyester_plush', 'Fußsohle links', 'Sohle', 'box', label=False,
         x=50, y=145, w=34, d=4, z=7, h=36, r=2, mass=1, color=HELL, sortBias=6,
         info='Helle Sohle aus kurzflorigem Stoff, rundherum eingenäht.'),
    teil('bein_rechts', 'polyester_plush', 'Bein rechts', 'Bein', 'cyl', label=False,
         x=106, y=74, w=54, d=42, z=0, h=40, mass=10, color=FELL, sortBias=4, info='Zweites Bein.'),
    teil('fuss_rechts', 'polyester_plush', 'Fuß rechts', 'Fuß', 'cyl', label=False,
         x=108, y=116, w=50, d=29, z=0, h=50, mass=5, color=FELL, sortBias=5,
         info='Fuß mit eingesetzter Sohle.'),
    teil('sohle_rechts', 'polyester_plush', 'Fußsohle rechts', 'Sohle', 'box', label=False,
         x=116, y=145, w=34, d=4, z=7, h=36, r=2, mass=1, color=HELL, sortBias=6,
         info='Helle Sohle aus kurzflorigem Stoff, rundherum eingenäht.'),
] + rumpffuellung

by = {p['id']: p for p in teile}
ids = lambda ps: [p['id'] for p in ps]  # noqa: E731
stapel = ['ohr_links', 'ohr_rechts'] + ids(kopf) + ['schnauze'] + ids(kopffuellung) + ids(rumpf) + ids(rumpffuellung)
explodiere([by[i] for i in stapel], abstand=40, nach_liste=True,
           abstaende={i: 70 for i in ids(kopf) + ids(rumpf) + ['schnauze']},
           gruppen=[['ohr_links', 'ohr_rechts'], ids(kopf) + ['schnauze'], ids(kopffuellung), ids(rumpf),
                    ids(rumpffuellung)])
kopf_dz = by['kopf_0']['explode'][2]
rumpf_dz = by['rumpf_0']['explode'][2]
for i in ('auge_links', 'auge_rechts', 'nase'):
    by[i]['explode'] = [0, 70, kopf_dz]
for i in ('arm_links', 'pfote_links'):
    by[i]['explode'] = [-70, 0, rumpf_dz]
for i in ('arm_rechts', 'pfote_rechts'):
    by[i]['explode'] = [70, 0, rumpf_dz]
for i in ('bein_links', 'bein_rechts', 'fuss_links', 'fuss_rechts', 'sohle_links', 'sohle_rechts'):
    by[i]['explode'] = [0, 170, 0]
by['etikett']['explode'] = [90, 0, 0]
skaliere_masse(teile, oid='plush_toy')
schreibe('plush_toy', teile)
