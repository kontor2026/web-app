"""3D-Modell: plush_toy. Erzeugt tools/kategorien/modelle/plush_toy.json.

Sitzender Teddybär, 200 × 150 × 250 mm (Front bei y = 150), Plüsch aus Polyester, gefüllt mit Polyesterwatte,
Sicherheitsaugen und Nase aus Kunststoff mit Sicherungsscheibe. Aus elliptischen Zylindern aufgebaut:
Rumpf, Kopf mit Schnauze, Ohren, Arme, Beine; Füllungen von Rumpf und Kopf als eigene Teile.
Explosion: Stapel nach Liste (unten Rumpffüllung, darüber Rumpfhülle, Kopffüllung, Kopf mit Schnauze, Ohren);
Arme seitlich, Beine, Augen und Nase nach vorne, Pflegeetikett nach rechts herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

FELL = '#B07A45'
HELL = '#D9B38A'
WATTE = '#F4F2EE'
AUGE = '#1C1D1F'

teile = [
    teil('ohr_links', 'polyester_plush', 'Ohren', 'Ohren', 'cyl',
         x=45, y=48, w=36, d=18, z=225, h=25, mass=3, color=FELL,
         info='Plüschtaschen, mit etwas Watte gefüllt und am Kopf angenäht.',
         marks=[mark('cyl', 7, 4, 22, 10, fill=HELL)]),
    teil('ohr_rechts', 'polyester_plush', 'Ohr rechts', 'Ohr', 'cyl', label=False,
         x=119, y=48, w=36, d=18, z=225, h=25, mass=3, color=FELL,
         info='Zweites Ohr.', marks=[mark('cyl', 7, 4, 22, 10, fill=HELL)]),
    teil('kopf', 'polyester_plush', 'Kopf (Plüschhülle)', 'Kopf', 'cyl',
         x=40, y=28, w=120, d=100, z=140, h=85, mass=40, color=FELL,
         info='Plüschstoff aus Polyester: ein gewebter Grund mit langen, aufgeschnittenen Fasern. An der Halsnaht '
              'mit dem Rumpf vernäht.',
         marks=[mark('cyl', 20, 15, 80, 60, fill='#A67142')]),
    teil('schnauze', 'polyester_plush', 'Schnauze', 'Schnauze', 'cyl',
         x=73, y=128, w=54, d=22, z=160, h=34, mass=6, color=HELL,
         info='Kurzfloriger heller Plüsch, eigenes Schnittteil, auf dem Nase und Mundnaht sitzen.'),
    teil('kopffuellung', 'polyester_fill', 'Füllung Kopf', 'Füllung Kopf', 'cyl',
         x=45, y=33, w=110, d=90, z=145, h=75, mass=50, color=WATTE,
         info='Lockere Polyesterwatte, von Hand oder maschinell durch eine Naht gestopft. Naht auftrennen, '
              'herausziehen und als Füllung weiterverwenden.',
         marks=[mark('cyl', 25, 20, 60, 50, fill='#E8E4DA')]),
    teil('rumpf', 'polyester_plush', 'Rumpf (Plüschhülle)', 'Rumpf', 'cyl',
         x=35, y=20, w=130, d=110, z=0, h=140, mass=60, color=FELL,
         info='Größtes Schnittteil mit der Stopfnaht am Rücken. Saubere Kuscheltiere lieber verschenken; '
              'sonst Naht aufschneiden, Füllung und Kunststoffteile trennen, Rest in den Restmüll.',
         marks=[mark('cyl', 30, 40, 70, 60, fill=HELL)]),
    teil('rumpffuellung', 'polyester_fill', 'Füllung Rumpf', 'Füllung Rumpf', 'cyl',
         x=40, y=25, w=120, d=100, z=5, h=135, mass=90, color=WATTE,
         info='Der größte Teil der Watte. Manche Kuscheltiere haben unten zusätzlich ein Säckchen mit '
              'Kunststoffgranulat, damit sie sitzen.',
         marks=[mark('cyl', 25, 20, 70, 60, fill='#E8E4DA')]),
    teil('auge_links', 'plastic_eyes', 'Sicherheitsaugen', 'Augen', 'cyl',
         x=70, y=122, w=12, d=6, z=188, h=12, mass=1.5, color=AUGE,
         info='Kunststoffaugen mit Schaft, innen mit einer Sicherungsscheibe festgeklemmt, damit Kinder sie nicht abreißen. '
              'Zum Trennen den Stoff rundherum aufschneiden.',
         marks=[mark('cyl', 2, 1, 4, 2, fill='#FFFFFF')]),
    teil('auge_rechts', 'plastic_eyes', 'Auge rechts', 'Auge', 'cyl', label=False,
         x=118, y=122, w=12, d=6, z=188, h=12, mass=1.5, color=AUGE,
         info='Zweites Auge.', marks=[mark('cyl', 2, 1, 4, 2, fill='#FFFFFF')]),
    teil('nase', 'plastic_eyes', 'Nase', 'Nase', 'cyl',
         x=91, y=138, w=18, d=10, z=194, h=8, mass=2, color='#2B2D2F',
         info='Ebenfalls Kunststoff mit Sicherungsscheibe. Bei manchen Tieren ist die Nase nur aufgestickt.'),
    teil('arm_links', 'polyester_plush', 'Arme', 'Arme', 'cyl',
         x=2, y=55, w=40, d=55, z=70, h=70, mass=12, color=FELL,
         info='Gefüllte Plüschschläuche, in die Seitennähte des Rumpfs eingenäht.',
         marks=[mark('cyl', 8, 25, 24, 26, fill=HELL)]),
    teil('arm_rechts', 'polyester_plush', 'Arm rechts', 'Arm', 'cyl', label=False,
         x=158, y=55, w=40, d=55, z=70, h=70, mass=12, color=FELL,
         info='Zweiter Arm.', marks=[mark('cyl', 8, 25, 24, 26, fill=HELL)]),
    teil('bein_links', 'polyester_plush', 'Beine', 'Beine', 'cyl',
         x=38, y=75, w=52, d=75, z=0, h=48, mass=15, color=FELL,
         info='Gefüllte Beine mit eingesetzter Fußsohle aus hellem Stoff.',
         marks=[mark('cyl', 10, 45, 32, 26, fill=HELL)]),
    teil('bein_rechts', 'polyester_plush', 'Bein rechts', 'Bein', 'cyl', label=False,
         x=110, y=75, w=52, d=75, z=0, h=48, mass=15, color=FELL,
         info='Zweites Bein.', marks=[mark('cyl', 10, 45, 32, 26, fill=HELL)]),
    teil('etikett', 'polyester_plush', 'Pflegeetikett', 'Etikett', 'box',
         x=165, y=60, w=0.3, d=30, z=15, h=40, r=0, mass=1, materials=[['polyester', 95], ['druck', 5]],
         color='#F4F2EE',
         info='Eingenähtes Etikett mit Material, Waschhinweis und CE-Zeichen. Es besteht wie der Plüsch aus Polyester '
              'und darf dranbleiben.'),
]

by = {p['id']: p for p in teile}
stapel = ['ohr_links', 'ohr_rechts', 'kopf', 'schnauze', 'kopffuellung', 'rumpf', 'rumpffuellung']
ordnung = ['ohr_links', 'ohr_rechts', 'kopf', 'schnauze', 'auge_links', 'auge_rechts', 'nase', 'kopffuellung',
           'rumpf', 'arm_links', 'arm_rechts', 'etikett', 'bein_links', 'bein_rechts', 'rumpffuellung']
teile = [by[i] for i in ordnung]
explodiere([by[i] for i in stapel], abstand=30, nach_liste=True,
           gruppen=[['ohr_links', 'ohr_rechts'], ['kopf', 'schnauze']])
kopf_dz = by['kopf']['explode'][2]
rumpf_dz = by['rumpf']['explode'][2]
for i in ('auge_links', 'auge_rechts'):
    by[i]['explode'] = [0, 60, kopf_dz]
by['nase']['explode'] = [0, 60, kopf_dz]
by['arm_links']['explode'] = [-50, 0, rumpf_dz]
by['arm_rechts']['explode'] = [50, 0, rumpf_dz]
for i in ('bein_links', 'bein_rechts'):
    by[i]['explode'] = [0, 85, rumpf_dz]
by['etikett']['explode'] = [100, 0, rumpf_dz]
skaliere_masse(teile, oid='plush_toy')
schreibe('plush_toy', teile)
