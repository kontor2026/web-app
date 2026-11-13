"""3D-Modell: bluetooth_speaker. Erzeugt tools/kategorien/modelle/bluetooth_speaker.json.

Typischer runder Bluetooth-Lautsprecher (Röhre 180 × 70 mm, liegt waagerecht, Achse entlang x).
Die Röhre ist aus je zwei Scheiben für Ober- und Unterhälfte des Gitters aufgebaut. An den Enden Gummikappen
mit Passivmembranen dahinter, oben eine Gummi-Tastenleiste. Innen ein Kunststoffrahmen mit Akku (2 Zellen),
darüber zwei nach oben gerichtete Lautsprecher und die Platine.
Explosion: Gummikappen und Passivmembranen zur Seite (dx), Rest in Ebenen nach oben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

GITTER = '#3C4650'
GUMMI = '#23272A'
TREIBER = [['ndfeb', 25], ['stahl', 35], ['kupfer', 15], ['papier', 10], ['pcabs', 15]]
PASSIV = [['stahl', 40], ['gummi', 40], ['pcabs', 20]]
L = 152  # Länge des Gitters zwischen den Kappen (x 14..166)


def maschen(w, d):
    return raster(4, 3, int((w - 8) // 6), int((d - 6) // 6), 3, 3, 6, shape='cyl', fill='#2F3840')


teile = [
    teil('tasten', 'rubber_shell', 'Gummi-Tastenleiste', 'Tasten', 'box',
         x=50, y=27, w=80, d=16, z=69, h=2.5, r=6, mass=5,
         info='Silikonstreifen mit Ein-, Bluetooth- und Lautstärketasten. Darunter liegen kleine Taster auf der Platine.',
         color=GUMMI, marks=[mark('cyl', 6 + i * 14, 4, 8, fill='#3A3F44') for i in range(5)]),
    teil('gitter_oben', 'speaker_grille', 'Gitter (oberer Rand)', 'Gitter oben', 'box',
         x=14, y=13, w=L, d=44, z=60, h=10, r=2, mass=12, color=GITTER, materials=[['stahl', 85], ['polyester', 15]],
         info='Oberste Scheibe der Gitterröhre.', label=False, marks=maschen(L, 44)),
    teil('gitter_mitte_o', 'speaker_grille', 'Lautsprechergitter (Oberhälfte)', 'Gitter', 'box',
         x=14, y=0, w=L, d=70, z=35, h=25, r=2, mass=30, color=GITTER, materials=[['stahl', 85], ['polyester', 15]],
         info='Gelochtes Stahlblech, außen mit Stoff bespannt. Schützt die Lautsprecher und ist rundum eingeklebt '
              'oder eingeclipst; mit einem flachen Hebel lösen.',
         marks=maschen(L, 70)),
    teil('treiber_l', 'speaker_driver', 'Lautsprecher links', 'Lautsprecher', 'cyl',
         x=24, y=12, w=46, z=32, h=24, mass=55, materials=TREIBER, color='#3B3B3B',
         info='Breitbandlautsprecher mit Neodym-Magnet. Der Magnet ist stark: nicht an Bankkarten oder Handys halten.',
         marks=[mark('cyl', 3, 3, 40, fill='#55493C'), mark('cyl', 15, 15, 16, fill='#6B6158')]),
    teil('treiber_r', 'speaker_driver', 'Lautsprecher rechts', 'Lautsprecher', 'cyl',
         x=110, y=12, w=46, z=32, h=24, mass=55, materials=TREIBER, color='#3B3B3B', label=False,
         info='Zweiter Lautsprecher für Stereo-Klang.',
         marks=[mark('cyl', 3, 3, 40, fill='#55493C'), mark('cyl', 15, 15, 16, fill='#6B6158')]),
    teil('platine', 'circuit_board', 'Platine mit Bluetooth-Chip', 'Platine', 'box',
         x=73, y=14, w=34, d=42, z=32, h=1.6, r=2, mass=20,
         info='Leiterplatte mit Bluetooth- und Verstärker-Chip und der USB-C-Ladebuchse. Mit Steckern am Akku und '
              'an den Lautsprechern angeschlossen.',
         color='#2E6B45', marks=[mark('box', 6, 8, 10, 10, 0.5, '#22272B'), mark('box', 19, 8, 9, 9, 0.5, '#22272B'),
                                 mark('box', 12, 34, 10, 6, 1, '#B7BCC0')]),
    teil('akku', 'li_ion_battery', 'Lithium-Ionen-Akku (2 Zellen)', 'Akku', 'box',
         x=57, y=16, w=66, d=38, z=12, h=19, r=8, mass=95,
         materials=[['lco', 40], ['graphit', 20], ['elektrolyt', 15], ['alu', 10], ['kupfer', 10], ['folien', 5]],
         info='Zwei Rundzellen (18650) in Schrumpffolie, zusammen etwa 5.000 mAh. Stecker abziehen, Pole abkleben '
              'und zur Batteriesammlung bringen; nie anbohren.',
         color='#3F6FA8', marks=[mark('box', 2, 1, 62, 17, 8, '#4A7DB8'), mark('box', 2, 20, 62, 17, 8, '#4A7DB8')]),
    teil('rahmen', 'rubber_shell', 'Innenrahmen (Kunststoff)', 'Innenrahmen', 'box',
         material_id='abs', x=16, y=8, w=148, d=54, z=8, h=24, r=8, mass=60, materials=[['pcabs', 100]],
         info='Stabiler Kunststoffrahmen, der Akku, Lautsprecher und Platine trägt. An den Enden mit den Kappen '
              'verschraubt.',
         color='#4A4F54', marks=[mark('box', 40, 7, 68, 40, 6, '#3A3F44')]),
    teil('gitter_mitte_u', 'speaker_grille', 'Lautsprechergitter (Unterhälfte)', 'Gitter unten', 'box',
         x=14, y=0, w=L, d=70, z=10, h=25, r=2, mass=30, color=GITTER, materials=[['stahl', 85], ['polyester', 15]],
         info='Untere Hälfte der Gitterröhre.', label=False, marks=maschen(L, 70)),
    teil('gitter_unten', 'speaker_grille', 'Gitter (unterer Rand) mit Gummifuß', 'Gitter Boden', 'box',
         x=14, y=13, w=L, d=44, z=0, h=10, r=2, mass=14, color=GITTER,
         materials=[['stahl', 70], ['polyester', 10], ['gummi', 20]],
         info='Unterste Scheibe mit Gummistreifen, damit der Lautsprecher nicht wegrollt.', label=False,
         marks=[mark('box', 30, 16, 92, 12, 6, GUMMI)]),
    teil('kappe_l', 'rubber_shell', 'Gummi-Endkappe links', 'Endkappe', 'box',
         x=0, y=0, w=14, d=70, z=0, h=70, r=6, explode=[-50, 0, 0], mass=25, color=GUMMI,
         info='Weiche Gummikappe an der Röhrenseite. Abziehen oder abhebeln, darunter sitzen die Schrauben '
              'des Innenrahmens.',
         marks=[mark('box', 3, 10, 8, 50, 4, '#2F3438')]),
    teil('passiv_l', 'speaker_driver', 'Passivmembran links', 'Passivmembran', 'box',
         material_id='rubber', x=14, y=10, w=6, d=50, z=10, h=50, r=2, explode=[-24, 0, 0], mass=20,
         materials=PASSIV, color='#5A6066',
         info='Gummimembran mit Metallgewicht ohne Magnet. Sie schwingt mit und verstärkt die Bässe.',
         marks=[mark('box', 1.5, 12, 3, 26, 1.5, '#8A939A')]),
    teil('passiv_r', 'speaker_driver', 'Passivmembran rechts', 'Passivmembran', 'box',
         material_id='rubber', x=160, y=10, w=6, d=50, z=10, h=50, r=2, explode=[24, 0, 0], mass=20,
         materials=PASSIV, color='#5A6066', label=False, info='Zweite Passivmembran am anderen Ende.',
         marks=[mark('box', 1.5, 12, 3, 26, 1.5, '#8A939A')]),
    teil('kappe_r', 'rubber_shell', 'Gummi-Endkappe rechts', 'Endkappe', 'box',
         x=166, y=0, w=14, d=70, z=0, h=70, r=6, explode=[50, 0, 0], mass=25, color=GUMMI, label=False,
         info='Zweite Endkappe, oft mit Gummiklappe über der Ladebuchse.',
         marks=[mark('box', 3, 10, 8, 50, 4, '#2F3438')]),
]
explodiere(teile, abstand=30, gruppen=[['gitter_oben', 'gitter_mitte_o'], ['gitter_mitte_u', 'gitter_unten']],
           abstaende={'tasten': 20})
skaliere_masse(teile, oid='bluetooth_speaker')
schreibe('bluetooth_speaker', teile)
