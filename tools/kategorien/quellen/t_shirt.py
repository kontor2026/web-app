"""3D-Modell: t_shirt. Erzeugt tools/kategorien/modelle/t_shirt.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, schreibe  # noqa: E402

# Kurzarm-T-Shirt flach ausgebreitet, Kragen hinten (y = 0), Saum vorne. 330 × 345 × 7 mm.
STOFF = '#4C7FB5'
SAUM = '#3F6E9E'
teile = [
    teil('kragen', 'cotton_fabric', 'Kragenbündchen', 'Kragen', 'cyl',
         x=120, y=0, w=90, d=46, z=5, h=1.5, mass=7, materials=[['baumwolle', 95], ['polyester', 5]], color=SAUM,
         info='Elastischer Rippstrick, rund an den Halsausschnitt genäht. Etwas Elasthan sorgt dafür, dass er nicht ausleiert.',
         marks=[mark('cyl', 7, 6, 76, 34, fill='#2E5277')]),
    teil('vorderteil', 'cotton_fabric', 'Vorderteil', 'Vorderteil', 'box',
         x=50, y=26, w=230, d=319, z=2.5, h=2.5, r=4, mass=52, materials=[['baumwolle', 98], ['polyester', 2]], color=STOFF,
         info='Baumwoll-Single-Jersey. Tragbare Shirts in die Altkleidersammlung, kaputte zum Textilrecycling: '
              'Daraus werden Putzlappen oder Dämmstoff.',
         marks=[mark('box', 0, 305, 230, 3, 0, SAUM), mark('box', 75, 60, 80, 60, 6, '#E8E6E1')]),
    teil('etikett', 'care_label', 'Pflegeetikett', 'Etikett', 'box',
         x=155, y=4, w=20, d=20, z=2.5, h=0.3, r=1, mass=0.5, materials=[['polyester', 100]], color='#F4F2EE',
         info='Polyester-Etikett mit Waschsymbolen und Fasergehalt. Vor dem Recycling an der Naht abschneiden, '
              'weil es ein anderes Material ist.',
         marks=[mark('box', 3, 4, 14, 2, 0, '#8E969A'), mark('box', 3, 8, 14, 2, 0, '#8E969A'),
                mark('box', 3, 12, 10, 2, 0, '#8E969A')]),
    teil('rueckenteil', 'cotton_fabric', 'Rückenteil', 'Rückenteil', 'box',
         x=50, y=0, w=230, d=345, z=0, h=2.5, r=4, mass=56, materials=[['baumwolle', 98], ['polyester', 2]], color=STOFF,
         info='Gleicher Stoff wie vorne, an Schultern und Seiten mit Polyestergarn vernäht. Zum Trennen die Nähte aufschneiden.',
         marks=[mark('box', 0, 331, 230, 3, 0, SAUM)]),
    teil('aermel_l', 'cotton_fabric', 'Ärmel links', 'Ärmel', 'box',
         x=0, y=10, w=50, d=120, z=0, h=5, r=6, mass=16, materials=[['baumwolle', 98], ['polyester', 2]], color=STOFF,
         explode=[-40, 0, 0],
         info='Doppellagiger Ärmel, an der Schulter angesetzt. Der umgenähte Saum verhindert, dass der Stoff ausfranst.',
         marks=[mark('box', 2, 0, 3, 120, 0, SAUM)]),
    teil('aermel_r', 'cotton_fabric', 'Ärmel rechts', 'Ärmel', 'box',
         x=280, y=10, w=50, d=120, z=0, h=5, r=6, mass=16, materials=[['baumwolle', 98], ['polyester', 2]], color=STOFF,
         explode=[40, 0, 0], label=False,
         info='Gegenstück zum linken Ärmel.',
         marks=[mark('box', 45, 0, 3, 120, 0, SAUM)]),
]

explodiere(teile, abstand=90)
schreibe('t_shirt', teile)
