"""3D-Modell: leather_handbag. Erzeugt tools/kategorien/modelle/leather_handbag.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Lederhandtasche aufrecht stehend, 300 × 120 mm Grundfläche (vorne mit Außentasche 127 mm), Korpus 203 mm hoch,
# Henkel als Bogen (zwei Stege + Griff) bis 250 mm. Oben ist die Tasche mit einem Reißverschluss zwischen zwei
# Lederblenden geschlossen.
# Explodiert: Vorderwand, Außentasche und Drehverschluss nach vorne, Rückwand nach hinten, Seitenteile zur Seite;
# Henkel, Schieber, Reißverschluss, Blenden, Futter, Bodeneinlage und Boden stapeln sich über den Füßen.
LEDER = '#8A5A3B'
KANTE = '#5C3A24'
FUTTER = '#C9B48F'
GOLD = '#C9A24A'
LEDER_M = [['leder', 95], ['polyester', 5]]
HENKEL_M = [['leder', 85], ['polyester', 5], ['stahl', 10]]


def henkel(seite, y):
    vorne = seite == 'v'
    return [
        teil(f'griff_{seite}', 'leather_panel', 'Henkel' if vorne else 'Henkel hinten', 'Henkel', 'box',
             x=70, y=y, w=160, d=7, z=240, h=10, r=4, mass=26, materials=HENKEL_M, color=KANTE, label=vorne,
             info='Zwei verklebte Lederstreifen mit Kunststoffkern, die Kanten sind eingefärbt. An den Enden mit '
                  'Metallnieten am Korpus befestigt: Nieten aufbohren, dann löst sich der Henkel.'
             if vorne else 'Gegenstück an der Rückseite.',
             marks=[mark('box', 4, 3, 152, 1, 0, '#4A2E1C')]),
        teil(f'steg_{seite}1', 'leather_panel', 'Henkelsteg', 'Henkelsteg', 'box', x=70, y=y, w=12, d=7, z=203,
             h=37, r=2, mass=7, materials=HENKEL_M, color=KANTE, label=False, info='Steg des Henkels mit Niete.',
             marks=[mark('cyl', 3, 0.5, 6, fill=GOLD)]),
        teil(f'steg_{seite}2', 'leather_panel', 'Henkelsteg', 'Henkelsteg', 'box', x=218, y=y, w=12, d=7, z=203,
             h=37, r=2, mass=7, materials=HENKEL_M, color=KANTE, label=False, info='Steg des Henkels mit Niete.',
             marks=[mark('cyl', 3, 0.5, 6, fill=GOLD)]),
    ]


def fuss(i, x, y):
    return teil(f'fuss_{i}', 'leather_panel', 'Metallfüßchen', 'Füßchen', 'cyl', material_id='steel',
                x=x, y=y, w=10, z=0, h=3, mass=2, materials=[['messing', 60], ['stahl', 40]], color=GOLD,
                label=i == 4,
                info='Vier Füßchen schützen den Boden vor Abrieb. Die Laschen innen aufbiegen und die Füße abziehen.'
                if i == 4 else 'Weiteres Füßchen.', marks=[mark('cyl', 3, 3, 4, fill='#A88638')])


teile = henkel('v', 113) + henkel('h', 0) + [
    teil('schieber', 'metal_zipper', 'Schieber mit Zipper', 'Schieber', 'box',
         x=226, y=50, w=16, d=20, z=203, h=5, r=2, mass=5, materials=[['messing', 70], ['stahl', 30]], color=GOLD,
         info='Gegossener Metallschieber mit Lederanhänger. Er verbindet die beiden Zahnreihen beim Ziehen.',
         marks=[mark('box', 4, 3, 8, 14, 2, '#A88638')]),
    teil('reissverschluss', 'metal_zipper', 'Reißverschluss', 'Reißverschluss', 'box',
         x=20, y=52, w=260, d=16, z=200, h=3, r=1, mass=15, materials=[['messing', 55], ['polyester', 40], ['stahl', 5]],
         color='#2A2E31',
         info='Metallzähne auf Polyesterband, zwischen Futter und Lederblenden eingenäht. Mit der Schere am Band '
              'entlang heraustrennen.',
         marks=[mark('box', 0, 6, 260, 4, 0.5, GOLD)]),
    teil('blende_h', 'leather_panel', 'Lederblende hinten', 'Blende', 'box',
         x=6, y=6, w=288, d=48, z=196, h=6, r=2, mass=20, materials=LEDER_M, color=LEDER, label=False,
         info='Schmaler Lederstreifen, der die Öffnung hinter dem Reißverschluss abdeckt.',
         marks=[mark('box', 4, 42, 280, 1.2, 0, KANTE)]),
    teil('blende_v', 'leather_panel', 'Lederblende vorne', 'Blende', 'box',
         x=6, y=66, w=288, d=48, z=196, h=6, r=2, mass=20, materials=LEDER_M, color=LEDER,
         info='Lederblenden links und rechts vom Reißverschluss schließen die Tasche oben. Nähte auftrennen.',
         marks=[mark('box', 4, 5, 280, 1.2, 0, KANTE)]),
    teil('verschluss', 'leather_panel', 'Drehverschluss', 'Drehschloss', 'box', material_id='steel',
         x=138, y=124, w=24, d=4, z=140, h=18, r=3, mass=8, materials=[['messing', 70], ['stahl', 30]], color=GOLD,
         explode=[0, 330, 0], sortBias=70,
         info='Metallschloss der Außentasche, innen mit zwei umgebogenen Laschen befestigt. Laschen aufbiegen.'),
    teil('vortasche', 'leather_panel', 'Außentasche mit Klappe', 'Außentasche', 'box',
         x=40, y=120, w=220, d=4, z=40, h=130, r=3, mass=45, materials=LEDER_M, color='#7C4F33', explode=[0, 280, 0], sortBias=40,
         info='Aufgenähte Ledertasche für das Handy. Die Klappe wird vom Drehschloss gehalten.'),
    teil('vorderteil', 'leather_panel', 'Vorderwand', 'Vorderwand', 'box',
         x=0, y=114, w=300, d=6, z=3, h=200, r=2, mass=110, materials=LEDER_M, color=LEDER, explode=[0, 230, 0],
         info='Rindsleder, an den Kanten eingefasst und mit Polyestergarn vernäht. Nähte auftrennen, dann bleiben '
              'flache Lederstücke zum Basteln übrig.'),
    teil('rueckwand', 'leather_panel', 'Rückwand', 'Rückwand', 'box',
         x=0, y=0, w=300, d=6, z=3, h=200, r=2, mass=110, materials=LEDER_M, color=LEDER, explode=[0, -160, 0],
         info='Gleich aufgebaut wie die Vorderwand, innen mit Futter verklebt.'),
    teil('seite_l', 'leather_panel', 'Seitenteil links', 'Seitenteil', 'box',
         x=0, y=6, w=6, d=108, z=3, h=200, r=2, mass=35, materials=LEDER_M, color=LEDER, explode=[-130, 0, 0],
         info='Schmaler Lederstreifen (Keder), der Vorder- und Rückwand verbindet und der Tasche ihre Tiefe gibt.'),
    teil('seite_r', 'leather_panel', 'Seitenteil rechts', 'Seitenteil', 'box',
         x=294, y=6, w=6, d=108, z=3, h=200, r=2, mass=35, materials=LEDER_M, color=LEDER, explode=[130, 0, 0],
         label=False, info='Gegenstück zum linken Seitenteil.'),
    teil('futter', 'polyester_lining', 'Innenfutter mit Innentasche', 'Futter', 'box',
         x=8, y=8, w=284, d=104, z=16, h=180, r=4, mass=60, color=FUTTER,
         info='Eingenähter Beutel aus Polyester-Satin. An der oberen Naht entlang herausschneiden.',
         marks=[mark('box', 40, 6, 120, 4, 1, '#B39E78'), mark('box', 190, 6, 70, 4, 1, '#B39E78')]),
    teil('bodeneinlage', 'leather_panel', 'Bodeneinlage', 'Bodeneinlage', 'box', material_id='pp',
         x=10, y=10, w=280, d=100, z=13, h=3, r=6, mass=25, materials=[['pp', 100]], color='#E8E6E1',
         info='Feste Kunststoffplatte, damit der Boden nicht durchhängt. Lose unter dem Futter oder eingeklebt.'),
    teil('boden', 'leather_panel', 'Boden', 'Boden', 'box',
         x=0, y=0, w=300, d=120, z=3, h=10, r=8, mass=70, materials=LEDER_M, color=KANTE,
         info='Doppeltes, besonders festes Leder. Hier sitzen die Metallfüßchen.',
         marks=[mark('box', 6, 6, 288, 108, 6, '#6A4430')]),
] + [fuss(i + 1, x, y) for i, (x, y) in enumerate(((15, 15), (275, 15), (15, 95), (275, 95)))]

explodiere(teile, abstand=40, nach_liste=True,
           gruppen=[['griff_v', 'steg_v1', 'steg_v2', 'griff_h', 'steg_h1', 'steg_h2']],
           abstaende={'schieber': 15, 'reissverschluss': 25, 'bodeneinlage': 30})
skaliere_masse(teile, oid='leather_handbag')
schreibe('leather_handbag', teile)
