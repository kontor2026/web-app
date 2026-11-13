"""3D-Modell: baseball_cap. Erzeugt tools/kategorien/modelle/baseball_cap.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Basecap aufrecht auf dem Tisch, Verschluss hinten (y = 0), Schirm vorne (bis y = 250). 190 × 250 × 110 mm.
# Die Krone aus sechs Stoffbahnen ist aus drei Scheiben gestapelt und hebt sich als Ganzes ab, darunter liegt das
# Schweißband. Der Schirm wird nach vorne gezogen und in Ober-, Einlage- und Unterteil aufgefächert,
# der Klickverschluss nach hinten.
STOFF = '#2F4A6B'
NAHT = '#243A55'
BW = [['baumwolle', 100]]

teile = [
    teil('knopf', 'cotton_fabric', 'Stoffbezogener Knopf', 'Knopf', 'cyl', material_id='steel',
         x=88, y=88, w=14, z=105, h=5, mass=1.5, materials=[['stahl', 70], ['baumwolle', 30]], color=STOFF,
         info='Metallknopf mit Stoffbezug, deckt die Stelle ab, an der die sechs Bahnen oben zusammenlaufen.'),
    teil('krone_oben', 'cotton_fabric', 'Krone, Spitze', 'Krone', 'cyl',
         x=30, y=30, w=130, d=130, z=80, h=25, mass=15, materials=BW, color=STOFF,
         info='Sechs dreieckige Stoffbahnen aus Baumwoll-Twill, mit Ziernähten zusammengenäht.',
         marks=[mark('box', 63, 0, 4, 130, 1, NAHT), mark('box', 0, 63, 130, 4, 1, NAHT)]
         + [mark('cyl', x, y, 6, fill=NAHT) for x, y in ((28, 28), (96, 28), (28, 96), (96, 96))]),
    teil('krone_mitte', 'cotton_fabric', 'Krone, Mitte', 'Krone', 'cyl',
         x=10, y=10, w=170, d=170, z=40, h=40, mass=20, materials=BW, color=STOFF, label=False,
         info='Mittlerer Teil der Stoffbahnen. Die vorderen zwei Bahnen sind innen mit Vlies verstärkt.'),
    teil('krone_unten', 'cotton_fabric', 'Krone, Rand', 'Krone', 'cyl',
         x=0, y=0, w=190, d=190, z=0, h=40, mass=25, materials=[['baumwolle', 90], ['polyester', 10]], color=STOFF,
         label=False, info='Unterer Rand der Krone, hier sind Schirm und Schweißband angenäht. Tragbare Caps in die Altkleidersammlung.'),
    teil('etikett', 'cotton_fabric', 'Pflegeetikett', 'Etikett', 'box', material_id='polyester',
         x=110, y=10, w=20, d=0.3, z=8, h=30, r=0, mass=0.5, materials=[['polyester', 100]], color='#F4F2EE',
         explode=[0, -130, 0],
         info='Polyester-Etikett innen hinten am Schweißband. Vor dem Recycling abschneiden.'),
    teil('schweissband', 'cotton_fabric', 'Schweißband', 'Schweißband', 'cyl',
         x=8, y=8, w=174, d=174, z=0, h=25, mass=8, materials=[['baumwolle', 60], ['polyester', 40]], color='#3A3F44',
         info='Stoffband mit Einlage innen am Rand. Es saugt Schweiß auf und lässt sich mit der Schere heraustrennen.',
         marks=[mark('cyl', 5, 5, 164, fill='#4A5056')]),
    teil('verschluss_loch', 'plastic_buckles', 'Verschlussband mit Löchern', 'Verschluss', 'box',
         x=50, y=0, w=45, d=3, z=6, h=18, r=1, mass=3, color='#22272B', explode=[0, -70, 0],
         info='Klickverschluss aus Polypropylen. Die Bänder direkt hinter der Naht abschneiden.'),
    teil('verschluss_noppe', 'plastic_buckles', 'Verschlussband mit Noppen', 'Noppenband', 'box',
         x=95, y=0, w=45, d=3.5, z=6, h=18, r=1, mass=3, color='#22272B', explode=[0, -70, 0],
         info='Die Noppen rasten in die Löcher des Gegenstücks ein. Reines PP, ab in die Wertstoffsammlung.'),
    teil('schirm_oben', 'cotton_fabric', 'Schirmbezug oben', 'Schirmbezug', 'box',
         x=25, y=180, w=140, d=70, z=3.5, h=1.5, r=34, mass=5, materials=BW, color=STOFF, explode=[0, 120, 50],
         info='Stoff über dem Schirm, mit mehreren parallelen Nähten auf die Einlage gesteppt.',
         marks=[mark('box', 10, 58, 120, 1.5, 0, NAHT), mark('box', 10, 62, 120, 1.5, 0, NAHT)]),
    teil('schirm_einlage', 'visor_insert', 'Schirmeinlage', 'Einlage', 'box',
         x=27, y=181, w=136, d=67, z=1.5, h=2, r=32, mass=12, color='#E8E6E1', explode=[0, 120, 25],
         info='Gebogene Platte aus Polypropylen (früher Pappe). Schirmnaht aufschneiden und herausziehen.'),
    teil('schirm_unten', 'cotton_fabric', 'Schirmbezug unten', 'Schirmbezug', 'box',
         x=25, y=180, w=140, d=70, z=0, h=1.5, r=34, mass=5, materials=BW, color='#3F5F84', label=False,
         explode=[0, 120, 0], info='Unterseite des Schirms, oft in einer zweiten Farbe.'),
]

explodiere(teile, abstand=35, gruppen=[['krone_oben', 'krone_mitte', 'krone_unten']], abstaende={'knopf': 25},
           nach_liste=True)
skaliere_masse(teile, oid='baseball_cap')
schreibe('baseball_cap', teile)
