"""3D-Modell: earbuds. Erzeugt tools/kategorien/modelle/earbuds.json.

Typische kabellose In-Ear-Ohrhörer im Ladeetui, 61 × 47 × 22 mm, Etui flach mit dem Deckel nach oben (Scharnier
hinten, y = 0). Beide Ohrhörer liegen mit dem Silikonstöpsel nach unten in ihren Mulden. Der linke Ohrhörer wird
zerlegt und neben dem Etui gestapelt (dx > 0), der rechte bleibt ganz.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

LIPO = [['lco', 40], ['graphit', 20], ['elektrolyt', 15], ['alu', 10], ['kupfer', 10], ['folien', 5]]
WEISS = '#F2F2F0'
GRUEN = '#2E6B45'
CHIP = '#2B2F33'

# Linker Ohrhörer, liegt in der linken Mulde (x 7–27, y 9–35); Liste von oben nach unten
ohrhoerer_l = [
    teil('rueckschale', 'plastic_housing', 'Ohrhörer-Außenschale (Touchfläche)', 'Außenschale', 'box',
         material_id='pc', x=7, y=9, w=20, d=26, z=11, h=3.5, r=9, mass=1, color=WEISS,
         info='Außen liegende Kunststoffschale mit Touch-Sensor und Mikrofonöffnung. Mit der Innenschale verklebt.',
         marks=[mark('box', 4, 4, 12, 14, 5, '#E6E6E2'), mark('cyl', 8.5, 21, 3, fill='#5A6066')]),
    teil('platine_l', 'circuit_board', 'Platine mit Bluetooth-Chip', 'Platine', 'box',
         material_id='pcb', x=9, y=11, w=16, d=21, z=12.5, h=1, r=5, mass=0.6, color=GRUEN,
         info='Funkchip, zwei Mikrofone und Ladeelektronik auf kleinstem Raum. Die Antenne ist eine dünne Kupferbahn am Rand.',
         marks=[mark('box', 4, 5, 8, 7, 0.5, CHIP), mark('box', 3, 14, 4, 3, 0.5, CHIP),
                mark('cyl', 10, 15, 3, fill='#B9BEC2')]),
    teil('akku_l', 'li_ion_battery', 'Knopfzellen-Akku', 'Akku', 'cyl',
         material_id='li_ion', x=11, y=12, w=12, z=9, h=5.4, mass=1.6, materials=LIPO, color='#9BA3A8',
         info='Wiederaufladbare Lithium-Knopfzelle mit etwa 60 mAh. Sie ist eingeklebt und darf nicht angebohrt '
              'oder gequetscht werden.',
         marks=[mark('cyl', 1.5, 1.5, 9, fill='#B9BEC2'), mark('box', 5, 1, 2, 3, 0.5, '#C8423A')]),
    teil('treiber', 'speaker_driver', 'Lautsprecher (10 mm)', 'Lautsprecher', 'cyl',
         material_id='mixed_electronics', x=12, y=21, w=10, z=7, h=3.5, mass=0.8,
         materials=[['ndfeb', 35], ['kupfer', 20], ['stahl', 20], ['folien', 10], ['pcabs', 15]], color='#C9CDD1',
         info='Winziger Lautsprecher mit Neodym-Magnet und Schwingspule. Der Magnet ist stark, nicht in die Nähe '
              'von Bankkarten bringen.',
         marks=[mark('cyl', 1.5, 1.5, 7, fill='#C98F62'), mark('cyl', 3.5, 3.5, 3, fill='#5A6066')]),
    teil('innenschale', 'plastic_housing', 'Innenschale mit Schallröhrchen', 'Innenschale', 'box',
         material_id='pc', x=7, y=9, w=20, d=26, z=6, h=5, r=9, mass=1.2, color='#E6E6E2',
         info='Zeigt ins Ohr. Unten sitzen das Schallröhrchen mit Gitter und zwei Ladekontakte aus vergoldetem Metall.',
         marks=[mark('cyl', 5, 12, 10, fill='#D6D6D2'), mark('cyl', 8, 15, 4, fill='#5A6066'),
                mark('cyl', 4, 3, 2.5, fill='#D8B04A'), mark('cyl', 13.5, 3, 2.5, fill='#D8B04A')]),
    teil('ohrpolster', 'silicone_ear_tips', 'Silikon-Ohrstöpsel', 'Ohrstöpsel', 'cyl',
         x=11, y=20, w=12, z=3.5, h=3, mass=0.4, color='#DCDCD8',
         info='Weiche Silikonkappe in S, M oder L. Lässt sich von Hand vom Schallröhrchen abziehen und waschen.',
         marks=[mark('cyl', 3, 3, 6, fill='#C4C4C0'), mark('cyl', 4.5, 4.5, 3, fill='#5A6066')]),
]
explodiere(ohrhoerer_l, abstand=10, nach_liste=True)
for p in ohrhoerer_l:   # Stapel neben das Etui ziehen
    p['explode'][0] += 85

etui = [
    teil('deckel', 'plastic_housing', 'Etui-Deckel', 'Deckel', 'box',
         material_id='pc', x=0, y=0, w=61, d=47, z=15, h=7, r=16, mass=8, color=WEISS,
         info='Klappdeckel aus Polycarbonat. Ein kleiner Magnet vorne hält ihn geschlossen.',
         marks=[mark('box', 3, 3, 55, 41, 14, '#F7F7F5')]),
    teil('magnet_deckel', 'plastic_housing', 'Deckelmagnete', 'Magnete', 'box', material_id='mixed_electronics',
         x=24, y=41, w=13, d=3, z=15.5, h=2, r=0.5, mass=0.6, materials=[['ndfeb', 90], ['nickel', 10]],
         color='#8A9095', info='Neodym-Magnete im Deckel und im Unterteil. Sie halten den Deckel zu und ziehen die '
                               'Ohrhörer in die Mulden. Stark: nicht verschlucken!'),
    teil('scharnier', 'plastic_housing', 'Scharnier mit Feder', 'Scharnier', 'box', material_id='steel',
         x=22, y=0, w=17, d=3, z=13, h=4, r=1, mass=0.8, materials=[['stahl', 100]], color='#B9BEC2',
         info='Edelstahlstift mit kleiner Feder, die den Deckel aufschnappen lässt. Bricht oft als Erstes.'),
    teil('ohrhoerer_r', 'speaker_driver', 'Ohrhörer rechts (komplett)', 'Ohrhörer', 'box',
         material_id='mixed_electronics', x=34, y=9, w=20, d=26, z=6, h=8.5, r=9, mass=5.6,
         materials=[['pcabs', 45], ['lco', 12], ['graphit', 6], ['ndfeb', 10], ['kupfer', 12], ['chip', 10], ['gummi', 5]],
         color=WEISS, info='Gleich aufgebaut wie der linke Ohrhörer: Lautsprecher, Akku und Platine in einem '
                           'verklebten Gehäuse. Ganz zur Elektro-Sammlung geben.',
         marks=[mark('box', 4, 4, 12, 14, 5, '#E6E6E2'), mark('cyl', 8.5, 21, 3, fill='#5A6066')]),
    teil('federkontakte', 'circuit_board', 'Federkontakte und Haltemagnete', 'Federkontakte', 'box',
         material_id='mixed_electronics', x=10, y=11, w=14, d=4, z=4.5, h=1.5, r=0.5, mass=0.6,
         materials=[['ndfeb', 50], ['messing', 30], ['kontakte', 20]], color='#B9BEC2',
         info='Vergoldete Stifte in jeder Mulde laden den Ohrhörer, ein Magnet daneben hält ihn fest.',
         marks=[mark('cyl', 1, 1, 2, fill='#D8B04A'), mark('cyl', 11, 1, 2, fill='#D8B04A'),
                mark('box', 4.5, 0.5, 5, 3, 0.5, '#8A9095')]),
    teil('chip_etui', 'circuit_board', 'Lade-Chip', 'Lade-Chip', 'box',
         material_id='pcb', x=12, y=39, w=7, d=5, z=4.5, h=1, r=0.5, mass=0.3, materials=[['chip', 100]], color=CHIP,
         info='Steuert das Laden von Etui-Akku und Ohrhörern und schaltet die Status-LED.'),
    teil('usb_c', 'circuit_board', 'USB-C-Ladebuchse', 'USB-C', 'box', material_id='steel',
         x=26, y=41, w=9, d=5.8, z=2, h=3.2, r=1.5, mass=0.6, materials=[['stahl', 70], ['kontakte', 15], ['pcabs', 15]],
         color='#B9BEC2', info='Ladebuchse aus Stahlblech mit vergoldeten Kontakten, an die Platine gelötet.',
         marks=[mark('box', 1.5, 3.8, 6, 1.4, 0.7, '#2A2E31')]),
    teil('platine_etui', 'circuit_board', 'Etui-Platine', 'Etui-Platine', 'box',
         x=8, y=37, w=45, d=8, z=1, h=1, r=1, mass=2.5, color=GRUEN,
         info='Leiterplatte mit Ladebuchse, LED und Leiterbahnen zu den Federkontakten.',
         marks=[mark('cyl', 20, 1, 2.5, fill='#7FD36B')] + raster(30, 1.5, 3, 1, 1.5, 1, 3, fill=CHIP)),
    teil('akku_etui', 'li_ion_battery', 'Lithium-Polymer-Akku (Etui)', 'Etui-Akku', 'box',
         x=10, y=9, w=41, d=26, z=1.5, h=3, r=2, mass=9, materials=LIPO, color='#9BA3A8',
         info='Etwa 400 mAh, reicht für drei bis vier Ladungen der Ohrhörer. Flacher Akku im Folienbeutel, '
              'nicht knicken oder durchstechen.',
         marks=[mark('box', 2, 2, 37, 22, 1.5), mark('box', 4, 4, 12, 6, 1, '#E8E8E2')]),
    teil('unterschale', 'plastic_housing', 'Etui-Unterteil', 'Etui', 'box',
         material_id='pc', x=0, y=0, w=61, d=47, z=0, h=15, r=16, mass=15, color=WEISS,
         info='Unterteil mit zwei Mulden für die Ohrhörer. Ist der Etui-Akku nicht ausbaubar, das ganze Etui '
              'zur Elektro-Sammlung bringen.',
         marks=[mark('box', 5, 7, 24, 30, 10, '#E0E0DC'), mark('box', 32, 7, 24, 30, 10, '#E0E0DC'),
                mark('cyl', 29, 41, 3, fill='#7FD36B')]),
]
explodiere(etui, abstand=16, nach_liste=True)
teile = etui + ohrhoerer_l
skaliere_masse(teile, oid='earbuds')
schreibe('earbuds', teile)
