"""3D-Modell: wool_sweater. Erzeugt tools/kategorien/modelle/wool_sweater.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Wollpullover ordentlich gefaltet, Vorderseite oben, Kragen hinten (y = 0), Bund vorne. 350 × 400 × 40 mm.
# Die Ärmel liegen unter dem Rückenteil eingeschlagen und werden zur Seite gezogen, Strickebenen heben sich nach oben ab.
WOLLE = '#8C3B3B'
RIPP = '#6E2D2D'
STRICK = [['wolle', 100]]
RIPPSTRICK = [['wolle', 95], ['polyester', 5]]

teile = [
    teil('kragen', 'wool_fabric', 'Rollkragen-Bündchen', 'Kragen', 'cyl',
         x=125, y=0, w=100, d=50, z=36, h=4, mass=15, materials=RIPPSTRICK, color=RIPP,
         info='Rippstrick, rund an den Halsausschnitt gekettelt. Ein wenig Kunstfaser hält ihn elastisch.',
         marks=[mark('cyl', 10, 7, 80, 36, fill='#4F2020')]),
    teil('etikett', 'care_label', 'Pflegeetikett', 'Etikett', 'box',
         x=165, y=6, w=22, d=24, z=35.7, h=0.3, r=1, mass=1, explode=[230, -60, 0], color='#F4F2EE',
         info='Polyester-Etikett mit Waschsymbolen: Wolle nur kalt oder im Wollprogramm waschen. '
              'Vor dem Recycling an der Naht abschneiden.',
         marks=[mark('box', 3, 4, 16, 2, 0, '#8E969A'), mark('box', 3, 9, 16, 2, 0, '#8E969A'),
                mark('box', 3, 14, 10, 2, 0, '#8E969A')]),
    teil('vorderteil', 'wool_fabric', 'Vorderteil mit Zopfmuster', 'Vorderteil', 'box',
         x=0, y=20, w=350, d=352, z=26, h=10, r=6, mass=150, materials=STRICK, color=WOLLE,
         info='Gestrickte Schafwolle. Tragbare Pullover in die Altkleidersammlung, kaputte kann man aufribbeln '
              'und das Garn neu verstricken.',
         marks=[mark('box', x, 50, 22, 290, 8, RIPP) for x in (60, 164, 268)]),
    teil('bund', 'wool_fabric', 'Bündchen am Saum', 'Bund', 'box',
         x=0, y=372, w=350, d=28, z=26, h=10, r=4, mass=25, materials=RIPPSTRICK, color=RIPP,
         info='Elastischer Rippstrick am unteren Rand, er hält den Pullover an der Hüfte.',
         marks=raster(6, 2, 34, 1, 4, 24, 10, fill='#4F2020')),
    teil('rueckenteil', 'wool_fabric', 'Rückenteil', 'Rückenteil', 'box',
         x=0, y=0, w=350, d=400, z=14, h=12, r=6, mass=150, materials=STRICK, color=WOLLE,
         info='Glatt rechts gestrickt, an Schultern und Seiten mit Wollgarn zusammengekettelt. '
              'Ein Faden aufgezogen, löst sich die ganze Masche.',
         marks=[mark('box', 0, 386, 350, 3, 0, RIPP)]),
    teil('aermel_l', 'wool_fabric', 'Ärmel links (eingeschlagen)', 'Ärmel', 'box',
         x=20, y=30, w=130, d=300, z=4, h=10, r=10, mass=70, materials=STRICK, color=WOLLE, explode=[-200, 0, 0],
         info='Langer Ärmel, beim Falten unter das Rückenteil geschlagen. Er ist an der Schulter angestrickt.'),
    teil('manschette_l', 'wool_fabric', 'Ärmelbündchen links', 'Bündchen', 'box',
         x=35, y=330, w=100, d=60, z=4, h=10, r=6, mass=8, materials=RIPPSTRICK, color=RIPP, explode=[-200, 0, 0],
         info='Rippstrick am Handgelenk, damit der Ärmel nicht rutscht.',
         marks=raster(4, 4, 12, 1, 4, 52, 8, fill='#4F2020')),
    teil('aermel_r', 'wool_fabric', 'Ärmel rechts (eingeschlagen)', 'Ärmel', 'box',
         x=200, y=30, w=130, d=300, z=4, h=10, r=10, mass=70, materials=STRICK, color=WOLLE, explode=[200, 0, 0],
         label=False, info='Gegenstück zum linken Ärmel.'),
    teil('manschette_r', 'wool_fabric', 'Ärmelbündchen rechts', 'Bündchen', 'box',
         x=215, y=330, w=100, d=60, z=4, h=10, r=6, mass=8, materials=RIPPSTRICK, color=RIPP, explode=[200, 0, 0],
         label=False, info='Gegenstück zum linken Ärmelbündchen.',
         marks=raster(4, 4, 12, 1, 4, 52, 8, fill='#4F2020')),
]

explodiere(teile, abstand=100, nach_liste=True)
skaliere_masse(teile, oid='wool_sweater')
schreibe('wool_sweater', teile)
