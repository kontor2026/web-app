"""3D-Modell: bed_sheet. Erzeugt tools/kategorien/modelle/bed_sheet.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Bettlaken (ca. 150 × 250 cm) zu einem Paket von 300 × 400 × 30 mm gefaltet: 32 Stofflagen.
# Explodiert heben sich vier Faltpakete nach oben ab, das eingenähte Etikett wird zur Seite gezogen.
STOFF = '#E9EEF2'
FALTE = '#CDD6DD'
SAUM = '#B9C4CC'
BW = [['baumwolle', 100]]

teile = [
    teil('etikett', 'cotton_fabric', 'Pflegeetikett', 'Etikett', 'box', material_id='polyester',
         x=20, y=360, w=30, d=26, z=30, h=0.3, r=1, mass=1, materials=[['polyester', 100]], color='#F4F2EE',
         explode=[310, 0, 0],
         info='Eingenähtes Polyester-Etikett mit Waschsymbolen (bis 60 °C). Vor dem Recycling abschneiden.',
         marks=[mark('box', 4, 5, 22, 3, 0, '#8E969A'), mark('box', 4, 12, 22, 3, 0, '#8E969A')]),
    teil('lage_1', 'cotton_fabric', 'Oberste Faltlagen mit Saum', 'Faltlagen oben', 'box',
         x=0, y=0, w=300, d=400, z=22, h=8, r=4, mass=150, materials=BW, color=STOFF,
         info='Baumwoll-Perkal oder Linon, glatt gewebt. Gut erhaltene Laken in die Altkleidersammlung, '
              'verschlissene als Putz- oder Malerlappen weiterverwenden.',
         marks=[mark('box', 0, 375, 300, 5, 0, SAUM), mark('box', 149, 0, 2, 400, 0, FALTE)]),
    teil('lage_2', 'cotton_fabric', 'Faltlagen 2', 'Faltlagen', 'box',
         x=0, y=0, w=300, d=400, z=15, h=7, r=4, mass=150, materials=BW, color=STOFF,
         info='Jede Faltung legt den Stoff doppelt. So werden aus einem großen Tuch acht Lagen in diesem Paket.',
         marks=[mark('box', 0, 199, 300, 2, 0, FALTE)]),
    teil('lage_3', 'cotton_fabric', 'Faltlagen 3', 'Faltlagen', 'box',
         x=0, y=0, w=300, d=400, z=8, h=7, r=4, mass=150, materials=BW, color=STOFF, label=False,
         info='Reine Baumwolle, ohne Knöpfe oder Reißverschluss: das Laken kann ganz ins Textilrecycling.',
         marks=[mark('box', 149, 0, 2, 400, 0, FALTE)]),
    teil('lage_4', 'cotton_fabric', 'Unterste Faltlagen mit Saum', 'Faltlagen unten', 'box',
         x=0, y=0, w=300, d=400, z=0, h=8, r=4, mass=150, materials=BW, color=STOFF,
         info='Am Rand ist der Stoff doppelt umgeschlagen und vernäht (Saum), damit er nicht ausfranst.',
         marks=[mark('box', 0, 20, 300, 5, 0, SAUM)]),
]

explodiere(teile, abstand=110)
skaliere_masse(teile, oid='bed_sheet')
schreibe('bed_sheet', teile)
