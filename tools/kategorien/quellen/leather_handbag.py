"""3D-Modell: leather_handbag. Erzeugt tools/kategorien/modelle/leather_handbag.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Lederhandtasche aufrecht stehend, 300 × 120 mm Grundfläche, Korpus 200 mm hoch, Henkel bis 250 mm.
# Explodiert: Vorder- und Rückwand nach vorne/hinten, Seitenteile nach links/rechts, Futter, Reißverschluss und
# Henkel steigen über dem Boden nach oben.
LEDER = '#8A5A3B'
KANTE = '#5C3A24'
FUTTER = '#C9B48F'
LEDER_M = [['leder', 95], ['polyester', 5]]

teile = [
    teil('henkel_v', 'leather_panel', 'Henkel vorne', 'Henkel', 'box',
         x=75, y=106, w=150, d=8, z=200, h=50, r=4, mass=45, materials=[['leder', 85], ['polyester', 5], ['stahl', 10]],
         color=KANTE,
         info='Zwei verklebte Lederstreifen mit Kunststoffkern, an beiden Enden mit Metallringen oder Nieten befestigt.'),
    teil('henkel_h', 'leather_panel', 'Henkel hinten', 'Henkel', 'box',
         x=75, y=6, w=150, d=8, z=200, h=50, r=4, mass=45, materials=[['leder', 85], ['polyester', 5], ['stahl', 10]],
         color=KANTE, label=False, info='Gegenstück am Rückenteil.'),
    teil('schieber', 'metal_zipper', 'Schieber mit Zipper', 'Schieber', 'box',
         x=228, y=50, w=16, d=20, z=200, h=5, r=2, mass=5, materials=[['messing', 70], ['stahl', 30]], color='#C9A24A',
         info='Gegossener Metallschieber mit Lederanhänger. Er verbindet die beiden Zahnreihen beim Ziehen.'),
    teil('reissverschluss', 'metal_zipper', 'Reißverschluss', 'Reißverschluss', 'box',
         x=20, y=54, w=260, d=12, z=196, h=4, r=1, mass=15, materials=[['messing', 55], ['polyester', 40], ['stahl', 5]],
         color='#2A2E31',
         info='Metallzähne auf Polyesterband, oben zwischen Futter und Leder eingenäht. Mit der Schere am Band entlang heraustrennen.',
         marks=[mark('box', 0, 4, 260, 4, 0.5, '#C9A24A')]),
    teil('vorderteil', 'leather_panel', 'Vorderwand', 'Vorderwand', 'box',
         x=0, y=114, w=300, d=6, z=10, h=190, r=2, mass=150, materials=LEDER_M, color=LEDER, explode=[0, 90, 0],
         info='Rindsleder, an den Kanten eingefasst und mit Polyestergarn vernäht. Nähte auftrennen, dann bleiben flache Lederstücke '
              'zum Basteln übrig.'),
    teil('seite_l', 'leather_panel', 'Seitenteil links', 'Seitenteil', 'box',
         x=0, y=6, w=6, d=108, z=10, h=190, r=2, mass=45, materials=LEDER_M, color=LEDER, explode=[-90, 0, 0],
         info='Schmaler Lederstreifen (Keder), der Vorder- und Rückwand verbindet und der Tasche ihre Tiefe gibt.'),
    teil('seite_r', 'leather_panel', 'Seitenteil rechts', 'Seitenteil', 'box',
         x=294, y=6, w=6, d=108, z=10, h=190, r=2, mass=45, materials=LEDER_M, color=LEDER, explode=[90, 0, 0],
         label=False, info='Gegenstück zum linken Seitenteil.'),
    teil('futter', 'polyester_lining', 'Innenfutter mit Innentasche', 'Futter', 'box',
         x=8, y=8, w=284, d=104, z=13, h=183, r=4, mass=60, color=FUTTER,
         info='Eingenähter Beutel aus Polyester-Satin. An der oberen Naht entlang herausschneiden.',
         marks=[mark('box', 40, 6, 120, 4, 1, '#B39E78')]),
    teil('bodeneinlage', 'leather_panel', 'Bodeneinlage', 'Bodeneinlage', 'box', material_id='pp',
         x=10, y=10, w=280, d=100, z=10, h=3, r=6, mass=25, materials=[['pp', 100]], color='#E8E6E1',
         info='Feste Kunststoffplatte, damit der Boden nicht durchhängt. Lose unter dem Futter oder eingeklebt.'),
    teil('boden', 'leather_panel', 'Boden mit Standfüßen', 'Boden', 'box',
         x=0, y=0, w=300, d=120, z=0, h=10, r=8, mass=80, materials=[['leder', 90], ['stahl', 10]], color=KANTE,
         info='Doppeltes Leder mit vier Metallfüßchen, die den Boden vor Abrieb schützen. Die Füße aufbiegen und abziehen.',
         marks=[mark('cyl', x, y, 10, fill='#C9A24A') for x in (20, 270) for y in (20, 90)]),
]

explodiere(teile, abstand=50, abstaende={'schieber': 15}, nach_liste=True)
skaliere_masse(teile, oid='leather_handbag')
schreibe('leather_handbag', teile)
