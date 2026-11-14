"""3D-Modell: bed_sheet. Erzeugt tools/kategorien/modelle/bed_sheet.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

# Bettlaken (ca. 150 × 250 cm) zu einem Paket von 300 × 400 × 30 mm gefaltet: 32 Stofflagen.
# Die vier Faltpakete liegen leicht versetzt wie bei echter Wäsche. Explodiert schieben sie sich treppenartig nach
# hinten oben, so dass von jedem Paket die Vorderkante und ein Streifen der Oberseite sichtbar bleibt; das
# eingenähte Etikett wird zur Seite gezogen.
STOFF = '#DCE7EF'
FALTE = '#C3D1DC'
SAUM = '#AFC0CD'
BW = [['baumwolle', 100]]


def lage(nr, name, short, z, dx, info, marks, label=True):
    k = 4 - nr  # 0 = unten
    return teil(f'lage_{nr}', 'cotton_fabric', name, short, 'box',
                x=2 + dx, y=2 - dx, w=296, d=396, z=z, h=7.5, r=6, mass=150, materials=BW, color=STOFF,
                explode=[0, -80 * k, 60 * k], label=label, info=info,
                marks=marks + [mark('box', 0, 0, 296, 2, 1, FALTE, zeichnung=True),
                                     mark('box', 294, 0, 2, 396, 1, FALTE, zeichnung=True)])


teile = [
    teil('etikett', 'cotton_fabric', 'Pflegeetikett', 'Etikett', 'box', material_id='polyester',
         x=24, y=362, w=30, d=26, z=30, h=0.3, r=1, mass=1, materials=[['polyester', 100]], color='#F4F2EE',
         explode=[300, 60, 0],
         info='Eingenähtes Polyester-Etikett mit Waschsymbolen (bis 60 °C). Vor dem Recycling abschneiden.',
         marks=[mark('box', 4, 5, 22, 3, 0, '#8E969A'), mark('box', 4, 12, 22, 3, 0, '#8E969A'),
                mark('box', 4, 19, 12, 3, 0, '#8E969A')]),
    lage(1, 'Oberste Faltlagen mit Saum', 'Oberste Lagen', 22.5, 0,
         'Baumwoll-Perkal oder Linon, glatt gewebt. Gut erhaltene Laken in die Altkleidersammlung, '
         'verschlissene als Putz- oder Malerlappen weiterverwenden.',
         [mark('box', 36, 350, 224, 14, 0, SAUM), mark('box', 36, 356, 224, 1.5, 0, '#94A7B6'),
          mark('box', 147, 20, 2, 330, 0, FALTE)]),
    lage(2, 'Faltlagen 2', 'Faltlagen', 15, 3,
         'Jede Faltung legt den Stoff doppelt. So werden aus einem großen Tuch 32 Lagen in diesem Paket.',
         [mark('box', 6, 197, 284, 2, 0, FALTE)]),
    lage(3, 'Faltlagen 3', 'Faltlagen', 7.5, -2,
         'Reine Baumwolle, ohne Knöpfe oder Reißverschluss: Das Laken kann ganz ins Textilrecycling.',
         [mark('box', 147, 6, 2, 384, 0, FALTE)], label=False),
    lage(4, 'Unterste Faltlagen mit Saum', 'Unterste Lagen', 0, 1,
         'Am Rand ist der Stoff doppelt umgeschlagen und mit Polyestergarn vernäht (Saum), damit er nicht ausfranst.',
         [mark('box', 30, 320, 236, 14, 0, SAUM), mark('box', 30, 326, 236, 1.5, 0, '#94A7B6')]),
]

skaliere_masse(teile, oid='bed_sheet')
schreibe('bed_sheet', teile)
