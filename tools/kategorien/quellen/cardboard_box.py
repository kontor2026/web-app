"""3D-Modell: cardboard_box. Erzeugt tools/kategorien/modelle/cardboard_box.json.

Typischer Versandkarton 40 × 30 × 25 cm (Faltschachtel aus einwelliger Wellpappe): vier Wände als Mantel,
oben zwei lange Außenklappen über zwei kurzen Innenklappen, unten das gleiche Klappenpaar, oben und unten mit
PP-Klebeband verschlossen, Versandetikett auf dem Deckel. Teile werden über dem Mantel gestapelt.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

PAPPE = '#C49A6C'
INNEN = '#B98D5F'
BAND = '#C8A15A'
WELLE = [['papier', 100]]
BAND_MAT = [['pp', 75], ['klebstoff', 25]]  # PP-Folie mit Kautschuk-/Acrylatkleber
teile = [
    teil('etikett', 'paper_label', 'Versandetikett', 'Etikett', 'box',
         x=40, y=170, w=150, d=100, z=250.1, h=0.2, r=1, mass=1.5, materials=[['papier', 90], ['druck', 10]],
         info='Thermopapier mit Adresse und Barcode, selbstklebend. Darf beim Altpapier dranbleiben, '
              'Adresse vorher schwärzen oder abreißen.',
         color='#F4F2EE', marks=[mark('box', 8, 8, 80, 6, 0, '#3A3F44'), mark('box', 8, 18, 60, 6, 0, '#3A3F44'),
                                 mark('box', 8, 28, 70, 6, 0, '#3A3F44'), mark('box', 8, 60, 134, 30, 0, '#22272B')]),
    teil('klebeband_oben', 'packing_tape', 'Klebeband oben', 'Klebeband', 'box',
         x=0, y=125, w=400, d=50, z=250.1, h=0.1, r=0, mass=2.5, materials=BAND_MAT,
         info='PP-Folie mit Klebstoff, verschließt die Mittelfuge der Deckelklappen. Vor dem Flachfalten '
              'abziehen und in die Gelbe Tonne oder den Restmüll geben.',
         color=BAND, opacity=0.85),
    teil('band_seite_oben', 'packing_tape', 'Klebeband, Seitenende oben', 'Band', 'box',
         x=400, y=125, w=0.2, d=50, z=190, h=60.2, r=0, mass=0.6, materials=BAND_MAT, label=False, sortBias=12,
         info='Das Band läuft an den Seiten etwa 6 cm herunter, damit es sich nicht von der Fuge löst.',
         color=BAND, opacity=0.9),
    teil('klappe_hinten', 'cardboard_box_body', 'Deckelklappe hinten', 'Klappe hinten', 'box',
         x=0, y=0, w=400, d=150, z=246.1, h=4, r=0, explode=[0, -90, 175], mass=48, materials=WELLE,
         info='Lange Außenklappe, an der Rückwand angeknickt. Die beiden Außenklappen treffen sich in der Mitte.',
         color=PAPPE, marks=[mark('box', 0, 0, 400, 2, 0, '#9E7A52')]),
    teil('klappe_vorne', 'cardboard_box_body', 'Deckelklappe vorne', 'Klappe vorne', 'box',
         x=0, y=150, w=400, d=150, z=246.1, h=4, r=0, explode=[0, 90, 175], mass=48, materials=WELLE,
         info='Zweite Außenklappe. Darauf kleben Band und Etikett.',
         color=PAPPE, marks=[mark('box', 160, 100, 80, 40, 2, '#3A3F44'), mark('box', 170, 108, 60, 24, 1, PAPPE),
                             mark('box', 300, 95, 22, 30, 2, '#3A3F44'), mark('box', 305, 100, 12, 14, 6, PAPPE),
                             mark('box', 0, 148, 400, 2, 0, '#9E7A52')]),
    teil('innenklappe_links', 'cardboard_box_body', 'Innenklappe links', 'Innenklappen', 'box',
         x=4, y=4, w=150, d=292, z=242.1, h=4, r=0, explode=[-60, 0, 95], mass=25, materials=WELLE,
         info='Die zwei kurzen Klappen an den Seitenwänden werden zuerst eingeklappt, die langen kommen darüber.',
         color=INNEN, marks=[mark('box', 0, 0, 2, 292, 0, '#8E6B45')]),
    teil('innenklappe_rechts', 'cardboard_box_body', 'Innenklappe rechts', 'Innenklappe', 'box',
         x=246, y=4, w=150, d=292, z=242.1, h=4, r=0, explode=[60, 0, 95], mass=25, materials=WELLE, label=False,
         info='Gegenstück zur linken Innenklappe.',
         color=INNEN, marks=[mark('box', 148, 0, 2, 292, 0, '#8E6B45')]),
    teil('mantel', 'cardboard_box_body', 'Mantel aus vier Wänden', 'Mantel', 'box',
         x=0, y=0, w=400, d=300, z=8.1, h=234, r=1, mass=190, materials=[['papier', 99], ['druck', 1]],
         info='Ein Zuschnitt aus Wellpappe, an einer Ecke zum Ring verklebt. Zwischen zwei glatten Lagen steckt eine '
              'gewellte, das macht den Karton leicht und stabil. Flach gefaltet ins Altpapier.',
         color=PAPPE, marks=[mark('box', 4, 4, 392, 292, 0, '#8E6B45'), mark('box', 0, 0, 4, 4, 0, '#9E7A52')]),
    teil('bodenklappen', 'cardboard_box_body', 'Bodenklappen', 'Boden', 'box',
         x=0, y=0, w=400, d=300, z=0.1, h=8, r=0, mass=196, materials=WELLE,
         info='Unten liegen genauso zwei Innen- und zwei Außenklappen übereinander. Nach dem Aufschneiden des '
              'Bandes lässt sich der Karton flach falten.',
         color=PAPPE, marks=[mark('box', 0, 148, 400, 4, 0, '#8E6B45')]),
    teil('band_seite_unten', 'packing_tape', 'Klebeband, Seitenende unten', 'Band', 'box',
         x=400, y=125, w=0.2, d=50, z=0, h=60, r=0, mass=0.6, materials=BAND_MAT, label=False, sortBias=200,
         explode=[0, 0, -45], info='Unteres Bandende an der Seitenwand.', color=BAND, opacity=0.9),
    teil('klebeband_unten', 'packing_tape', 'Klebeband unten', 'Band unten', 'box',
         x=0, y=125, w=400, d=50, z=0, h=0.1, r=0, mass=2.5, materials=BAND_MAT, label=False,
         info='Verschließt die Bodenfuge. Ebenfalls abziehen, bevor der Karton ins Altpapier kommt.',
         color=BAND, opacity=0.85, explode=[0, 0, -45]),
]
EX = {'etikett': [0, 0, 400], 'klebeband_oben': [0, 0, 370], 'band_seite_oben': [0, 0, 370],
      'klappe_hinten': [0, 0, 230], 'klappe_vorne': [0, 0, 230],
      'innenklappe_links': [-200, 0, 110], 'innenklappe_rechts': [200, 0, 110],
      'mantel': [0, 0, 60], 'bodenklappen': [0, 0, 0]}
for p in teile:
    if p['id'] in EX:
        p['explode'] = EX[p['id']]
skaliere_masse(teile, oid='cardboard_box')
schreibe('cardboard_box', teile)
