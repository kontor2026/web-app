"""3D-Modell: earbuds. Erzeugt tools/kategorien/modelle/earbuds.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Typische kabellose Ohrhörer im Ladeetui, 61 × 47 × 22 mm, Etui flach mit dem Deckel nach oben.
# Der linke Ohrhörer wird zerlegt und seitlich gestapelt (dx > 0), der rechte bleibt ganz im Etui.
LIPO = [['lco', 40], ['graphit', 20], ['elektrolyt', 15], ['alu', 10], ['kupfer', 10], ['folien', 5]]

ohrhoerer_l = [
    teil('ohrpolster', 'silicone_ear_tips', 'Silikon-Ohrstöpsel', 'Ohrstöpsel', 'cyl',
         x=11, y=9, w=12, z=13, h=5, mass=0.4, color='#E6E6E6',
         info='Weiche Silikonkappe in S, M oder L. Lässt sich von Hand vom Schallrohr abziehen und waschen.',
         marks=[mark('cyl', 3.5, 3.5, 5, fill='#9BA3A8')]),
    teil('treiber', 'speaker_driver', 'Lautsprecher (10 mm)', 'Lautsprecher', 'cyl',
         material_id='mixed_electronics', x=12, y=10, w=10, z=10, h=3.5, mass=0.8,
         materials=[['ndfeb', 35], ['kupfer', 20], ['stahl', 20], ['folien', 10], ['pcabs', 15]], color='#C9CDD1',
         info='Winziger Lautsprecher mit Neodym-Magnet und Schwingspule. Der Magnet ist stark, nicht in die Nähe von Bankkarten bringen.',
         marks=[mark('cyl', 2, 2, 6, fill='#C98F62'), mark('cyl', 3.5, 3.5, 3, fill='#5A6066')]),
    teil('platine_l', 'circuit_board', 'Platine mit Bluetooth-Chip', 'Platine', 'box',
         material_id='pcb', x=9, y=21, w=16, d=16, z=9, h=1.2, r=3, mass=0.6, color='#2E6B45',
         info='Funkchip, Mikrofon und Ladeelektronik auf kleinstem Raum. Die Antenne ist eine dünne Kupferbahn.',
         marks=[mark('box', 3, 3, 7, 7, 0.5, '#2B2F33'), mark('cyl', 11, 11, 3, fill='#B9BEC2')]),
    teil('akku_l', 'li_ion_battery', 'Knopfzellen-Akku', 'Akku', 'cyl',
         material_id='li_ion', x=11, y=23, w=12, z=7, h=5.4, mass=1.6, materials=LIPO, color='#9BA3A8',
         info='Wiederaufladbare Lithium-Knopfzelle mit etwa 60 mAh. Sie ist oft eingeklebt und darf nicht angebohrt oder gequetscht werden.',
         marks=[mark('cyl', 2, 2, 8, fill='#B9BEC2')]),
    teil('gehaeuse_l', 'plastic_housing', 'Ohrhörer-Gehäuse', 'Gehäuse', 'box',
         material_id='pc', x=6, y=7, w=22, d=33, z=5, h=10, r=10, mass=2.6, color='#F2F2F0',
         info='Zwei verklebte Kunststoffschalen. Öffnen geht nur mit Wärme und Hebelwerkzeug, darum ganz zur Elektro-Sammlung geben.',
         marks=[mark('cyl', 3, 3, 16, fill='#E6E6E6'), mark('cyl', 9, 26, 4, fill='#B9BEC2')]),
]
# Linken Ohrhörer für sich stapeln und dann neben das Etui ziehen
explodiere(ohrhoerer_l, abstand=12)
for p in ohrhoerer_l:
    p['explode'][0] += 70

teile = [
    teil('deckel', 'plastic_housing', 'Etui-Deckel', 'Deckel', 'box',
         material_id='pc', x=0, y=0, w=61, d=47, z=15, h=7, r=16, mass=9, color='#F2F2F0',
         info='Klappdeckel mit kleinem Magnet, der ihn geschlossen hält. Das Scharnier ist meist ein Stahlstift.',
         marks=[mark('cyl', 27, 41, 6, 4, fill='#7FD36B')]),
    teil('ohrhoerer_r', 'speaker_driver', 'Ohrhörer rechts (komplett)', 'Ohrhörer', 'box',
         material_id='mixed_electronics', x=33, y=7, w=22, d=33, z=5, h=10, r=10, mass=6,
         materials=[['pcabs', 45], ['lco', 12], ['graphit', 6], ['ndfeb', 10], ['kupfer', 12], ['chip', 10], ['gummi', 5]],
         color='#F2F2F0', info='Gleich aufgebaut wie der linke Ohrhörer: Lautsprecher, Akku und Platine in einem verklebten Gehäuse.',
         marks=[mark('cyl', 3, 3, 16, fill='#E6E6E6'), mark('cyl', 5, 5, 12, fill='#C9CDD1')]),
    teil('chip_etui', 'circuit_board', 'Lade-Chip', 'Lade-Chip', 'box',
         material_id='pcb', x=24, y=40, w=7, d=5, z=4.5, h=1, r=0.5, mass=0.3, materials=[['chip', 100]], color='#2B2F33',
         info='Steuert das Laden von Etui-Akku und Ohrhörern und schaltet die Status-LED.'),
    teil('platine_etui', 'circuit_board', 'Etui-Platine mit USB-C-Buchse', 'Etui-Platine', 'box',
         x=8, y=38, w=45, d=8, z=3.5, h=1, r=1, mass=2.5, color='#2E6B45',
         info='Leiterplatte mit Ladebuchse, LED und Federkontakten, über die die Ohrhörer geladen werden.',
         marks=[mark('box', 34, 1, 9, 5, 1, '#B9BEC2'), mark('cyl', 19, 2, 2.5, fill='#7FD36B')]),
    teil('akku_etui', 'li_ion_battery', 'Lithium-Polymer-Akku (Etui)', 'Etui-Akku', 'box',
         x=10, y=8, w=41, d=28, z=1.5, h=3.5, r=2, mass=9, materials=LIPO, color='#9BA3A8',
         info='Etwa 400 mAh, reicht für drei bis vier Ladungen der Ohrhörer. Flacher Akku im Folienbeutel, nicht knicken oder durchstechen.',
         marks=[mark('box', 2, 2, 37, 24, 1.5)]),
    teil('unterschale', 'plastic_housing', 'Etui-Unterteil', 'Etui', 'box',
         material_id='pc', x=0, y=0, w=61, d=47, z=0, h=15, r=16, mass=16, color='#F2F2F0',
         info='Unterteil mit zwei Mulden für die Ohrhörer. Ist der Etui-Akku nicht ausbaubar, das ganze Etui zur Elektro-Sammlung bringen.',
         marks=[mark('box', 5, 6, 24, 35, 11, '#E0E0DC'), mark('box', 32, 6, 24, 35, 11, '#E0E0DC')]),
] + ohrhoerer_l

explodiere(teile, abstand=20)
skaliere_masse(teile, oid='earbuds')
schreibe('earbuds', teile)
