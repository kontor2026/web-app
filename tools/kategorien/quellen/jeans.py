"""3D-Modell: jeans. Erzeugt tools/kategorien/modelle/jeans.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Jeans flach gelegt, Vorderseite oben, Bund hinten (y = 0). Die Unterschenkel sind auf Kniehöhe nach hinten
# unter die Hose geschlagen, so passt sie auf 350 × 400 mm. Stoffebenen werden nach oben abgehoben,
# das Pflegeetikett zur Seite gezogen.
DENIM = '#3C5A82'
DUNKEL = '#2E4766'
NAHT = '#C98A3D'
DENIM_MAT = [['baumwolle', 98], ['polyester', 2]]
NIETE = [['messing', 85], ['kupfer', 15]]

teile = [
    teil('knopf', 'metal_rivets', 'Hosenknopf', 'Knopf', 'cyl',
         x=166, y=12, w=18, z=25.5, h=7, mass=4, materials=[['messing', 70], ['stahl', 30]],
         info='Metallknopf, mit einem Stift durch den Stoff genietet. Vor dem Textilrecycling mit dem Stoff drumherum herausschneiden.',
         color='#B08D4A', marks=[mark('cyl', 3, 3, 12, fill='#C9A24A')]),
    teil('niete_1', 'metal_rivets', 'Niete', 'Nieten', 'cyl',
         x=12, y=46, w=7, z=24, h=2.5, mass=0.6, materials=NIETE,
         info='Kupfer- oder Messingnieten verstärken die Taschenecken. Jede einzeln ausschneiden: '
              'Metall stört beim Zerfasern der Baumwolle.',
         color='#B87333', marks=[mark('cyl', 2, 2, 3, fill='#8A5427')]),
    teil('niete_2', 'metal_rivets', 'Niete', 'Niete', 'cyl',
         x=112, y=48, w=7, z=24, h=2.5, mass=0.6, materials=NIETE, label=False,
         info='Niete an der inneren Ecke der linken Vordertasche.', color='#B87333'),
    teil('niete_3', 'metal_rivets', 'Niete', 'Niete', 'cyl',
         x=231, y=48, w=7, z=24, h=2.5, mass=0.6, materials=NIETE, label=False,
         info='Niete an der inneren Ecke der rechten Vordertasche.', color='#B87333'),
    teil('niete_4', 'metal_rivets', 'Niete', 'Niete', 'cyl',
         x=331, y=46, w=7, z=24, h=2.5, mass=0.6, materials=NIETE, label=False,
         info='Niete an der äußeren Ecke der rechten Vordertasche.', color='#B87333'),
    teil('bund', 'denim_fabric', 'Hosenbund mit Gürtelschlaufen', 'Bund', 'box',
         x=0, y=0, w=350, d=42, z=17, h=8, r=4, mass=30, materials=DENIM_MAT,
         info='Doppelt gelegter Denim mit Einlage. Die Gürtelschlaufen sind mehrfach übernäht.',
         color=DENIM, marks=[mark('box', 0, 40, 350, 1.5, 0, NAHT)]
         + [mark('box', x, 0, 10, 42, 1, DUNKEL) for x in (30, 110, 230, 310)] + [mark('box', 175, 8, 6, 26, 1, DUNKEL)]),
    teil('reissverschluss', 'metal_zipper', 'Reißverschluss', 'Reißverschluss', 'box',
         x=168, y=44, w=14, d=156, z=20, h=1.5, r=1, mass=6, materials=[['messing', 55], ['polyester', 40], ['stahl', 5]],
         info='Messingzähne auf einem Polyesterband, unter der Schlitzleiste versteckt. Links und rechts '
              'vom Band abschneiden, dann bleibt reiner Denim übrig.',
         color='#2A2E31', marks=[mark('box', 5, 0, 4, 156, 0.5, '#C9A24A'), mark('box', 3.5, 2, 7, 12, 1.5, '#B08D4A')]),
] + [
    teil(f'vorderteil_{i}' if i else 'vorderteil', 'denim_fabric', 'Vorderteil', 'Vorderteil', 'box',
         x=x, y=y, w=w, d=d, z=z, h=h, r=r, mass=m, materials=DENIM_MAT, label=None if i == 0 else False,
         info='Baumwoll-Denim, das Vorderteil beider Hosenbeine. Tragbare Jeans in die Altkleidersammlung, kaputte zum '
              'Textilrecycling: Dort werden sie zu Fasern für Dämmstoff gerissen.',
         color=DENIM, marks=[mark('box', 0, 2, 114, 2, 1, NAHT), mark('box', 224, 2, 114, 2, 1, NAHT),
                             mark('box', 166, 2, 3, 170, 1, NAHT), mark('box', 168, 172, 2, 182, 0, DUNKEL),
                             mark('box', 254, 10, 40, 36, 3, DUNKEL)] if i == 0 else None)
    # Weich gewölbte Stofflage: drei nach oben schmalere Scheiben, in der Foto-Ansicht eine glatte Fläche
    for i, (x, y, w, d, z, h, r, m) in enumerate([(6, 42, 338, 354, 22.5, 1.5, 24, 40),
                                                   (3, 40, 344, 358, 20, 2.5, 14, 50),
                                                   (0, 38, 350, 362, 17, 3, 6, 60)])
] + [
    teil('tasche_l', 'denim_fabric', 'Taschenbeutel links', 'Taschenbeutel', 'box', material_id='cotton',
         x=15, y=30, w=110, d=170, z=16, h=1, r=10, mass=8, materials=[['baumwolle', 65], ['polyester', 35]],
         info='Dünnes Futter aus Baumwoll-Polyester-Mischgewebe innen in der Vordertasche.',
         color='#E8E6E1'),
    teil('tasche_r', 'denim_fabric', 'Taschenbeutel rechts', 'Taschenbeutel', 'box', material_id='cotton',
         x=225, y=30, w=110, d=170, z=16, h=1, r=10, mass=8, materials=[['baumwolle', 65], ['polyester', 35]],
         label=False, info='Gegenstück zum linken Taschenbeutel.', color='#E8E6E1'),
    teil('etikett', 'care_label', 'Pflegeetikett', 'Etikett', 'box',
         x=300, y=4, w=30, d=34, z=16, h=0.3, r=1, explode=[80, 0, 0], mass=1, materials=[['polyester', 100]],
         info='Polyester-Etikett innen am Bund mit Waschsymbolen und Fasergehalt. Abschneiden, '
              'weil es ein anderes Material ist als der Denim.',
         color='#F4F2EE', marks=[mark('box', 4, 5, 22, 3, 0, '#8E969A'), mark('box', 4, 11, 22, 3, 0, '#8E969A'),
                                mark('box', 4, 17, 14, 3, 0, '#8E969A')]),
    teil('rueckenteil', 'denim_fabric', 'Rückenteil mit Gesäßtaschen', 'Rückenteil', 'box',
         x=0, y=0, w=350, d=400, z=10, h=6, r=6, mass=180, materials=DENIM_MAT,
         info='Hinterer Stoff beider Beine mit aufgenähten Gesäßtaschen. Oft ist hinten am Bund ein Patch aus '
              'Leder oder Kunstleder, der ebenfalls abgeschnitten wird.',
         color=DENIM, marks=[mark('box', 172, 0, 3, 400, 1, NAHT)]),
    teil('bein_l', 'denim_fabric', 'Unterschenkel links (umgeschlagen)', 'Bein links', 'box',
         x=8, y=120, w=164, d=280, z=0, h=10, r=8, mass=90, materials=DENIM_MAT,
         info='Der untere Teil des Hosenbeins, unter die Hose geschlagen. Hier liegen vier Lagen Stoff übereinander.',
         color=DUNKEL, marks=[mark('box', 0, 268, 164, 3, 0, NAHT)]),
    teil('bein_r', 'denim_fabric', 'Unterschenkel rechts (umgeschlagen)', 'Bein rechts', 'box',
         x=178, y=120, w=164, d=280, z=0, h=10, r=8, mass=90, materials=DENIM_MAT, label=False,
         info='Gegenstück zum linken Unterschenkel.', color=DUNKEL, marks=[mark('box', 0, 268, 164, 3, 0, NAHT)]),
]

explodiere(teile, abstand=70, gruppen=[['vorderteil', 'vorderteil_1', 'vorderteil_2']], abstaende={f'niete_{i}': 25 for i in range(1, 5)}, nach_liste=True)
skaliere_masse(teile, oid='jeans')
schreibe('jeans', teile)
