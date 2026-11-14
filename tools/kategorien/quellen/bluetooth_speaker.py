"""3D-Modell: bluetooth_speaker. Erzeugt tools/kategorien/modelle/bluetooth_speaker.json.

Typischer runder Bluetooth-Lautsprecher (Röhre 180 × 70 mm, liegt waagerecht, Achse entlang x).
Die Röhre (Gitter) und die Gummi-Endkappen sind aus je acht waagerechten Scheiben aufgebaut, deren Tiefe dem
Kreisquerschnitt folgt. Innen ein Kunststoffrahmen mit Akku (2 Zellen), darüber zwei nach oben gerichtete
Lautsprecher und die Platine mit Bluetooth- und Verstärkerchip.
Explosion: Endkappen und Passivmembranen zur Seite (dx), obere Gitterhälfte nach oben und hinten, Rest in Ebenen.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

GITTER = '#46525F'
GUMMI = '#23272A'
CHIP = '#22272B'
TREIBER = [['ndfeb', 25], ['stahl', 35], ['kupfer', 15], ['papier', 10], ['pcabs', 15]]
PASSIV = [['gummi', 40], ['stahl', 40], ['pcabs', 20]]
R = 35  # Radius der Röhre
L = 152  # Länge des Gitters zwischen den Kappen (x 14..166)
GRENZEN = [0, 7, 15, 25, 35, 45, 55, 63, 70]
SCHEIBEN = []  # (z, h, y, d) je Scheibe, unten zuerst
for z0, z1 in zip(GRENZEN, GRENZEN[1:]):
    off = abs((z0 + z1) / 2 - R)
    d = round(2 * math.sqrt(R * R - off * off), 1)
    SCHEIBEN.append((z0, z1 - z0, round(R - d / 2, 2), d))


def maschen(w, d):
    return raster(4, 2.5, int((w - 8) // 6), max(int((d - 4) // 6), 1), 3, 3, 6, shape='cyl', fill='#2F3840')


def nur_zeichnung(ms):
    for m in ms:
        m['zeichnung'] = True  # Lochblech liegt unter dem Stoff: in der Foto-Ansicht nicht sichtbar
    return ms


gitter_o, gitter_u, kappe_l, kappe_r = [], [], [], []
for i, (z, h, y, d) in enumerate(SCHEIBEN):
    oben = z >= R
    gruppe = gitter_o if oben else gitter_u
    erste = (oben and z == R) or (not oben and z + h == R)
    marks = nur_zeichnung(maschen(L, d))
    if i == 0:
        marks = [mark('box', 30, 4, 92, d - 8, 4, GUMMI)]
    gruppe.append(teil(
        f'gitter{i}', 'speaker_grille',
        'Lautsprechergitter (Oberhälfte)' if oben else 'Lautsprechergitter (Unterhälfte)',
        'Gitter oben' if oben else 'Gitter unten', 'box', x=14, y=y, w=L, d=d, z=z, h=h, r=min(d / 2, 6),
        mass=h * d / 70 * 4, color=GITTER, label=erste,
        materials=[['polyester', 10], ['stahl', 70], ['gummi', 20]] if i == 0 else [['polyester', 15], ['stahl', 85]],
        info=('Gelochtes Stahlblech, außen mit Stoff bespannt. Schützt die Lautsprecher und ist rundum eingeklebt '
              'oder eingeclipst; mit einem flachen Hebel lösen.') if erste else
             ('Unterste Scheibe mit Gummistreifen, damit der Lautsprecher nicht wegrollt.' if i == 0
              else 'Teil der Gitterröhre.'),
        marks=marks))
    for seite, x, dx, liste in (('links', 0, -95, kappe_l), ('rechts', 166, 95, kappe_r)):
        km = [mark('box', 3, 3, 8, d - 6, min((d - 6) / 2, 3), '#2F3438')] if d > 40 else []
        if seite == 'rechts' and z == 25:
            km = [mark('box', 3, d / 2 - 6, 8, 12, 2, '#14171A')]  # Klappe über der Ladebuchse
        liste.append(teil(
            f'kappe_{seite[0]}{i}', 'rubber_shell', f'Gummi-Endkappe {seite}', 'Endkappe', 'box',
            x=x, y=y, w=14, d=d, z=z, h=h, r=min(d / 2, 6), explode=[dx, 0, 0], mass=h * d / 70 * 3.5,
            color=GUMMI, label=seite == 'links' and z == 35,
            info=('Weiche Gummikappe an der Röhrenseite. Abziehen oder abhebeln, darunter sitzen die Schrauben '
                  'des Innenrahmens.') if seite == 'links' else
                 'Zweite Endkappe, mit Gummiklappe über der USB-C-Ladebuchse.',
            marks=km))

tasten = teil('tasten', 'rubber_shell', 'Gummi-Tastenleiste', 'Tasten', 'box',
              x=50, y=27, w=80, d=16, z=70, h=2.5, r=7, mass=5, color=GUMMI,
              info='Silikonstreifen mit Ein-, Bluetooth-, Play- und Lautstärketasten. Darunter liegen kleine Taster '
                   'auf der Platine.',
              marks=[mark('cyl', 5 + k * 14.5, 4, 8, fill='#3A3F44') for k in range(5)]
              + [mark('box', 8.5, 7.3, 1.2, 1.4, 0.3, '#C9CED2'), mark('box', 18.5, 7.3, 4, 1.4, 0.3, '#C9CED2'),
                 mark('box', 61.5, 7.3, 4, 1.4, 0.3, '#C9CED2'), mark('box', 62.9, 5.9, 1.2, 4.2, 0.3, '#C9CED2'),
                 mark('cyl', 34.5, 7, 2, fill='#4D8FD6')])

innen = [
    teil('treiber_l', 'speaker_driver', 'Lautsprecher links', 'Lautsprecher', 'cyl',
         x=24, y=12, w=46, z=32, h=24, mass=55, materials=TREIBER, color='#3B3B3B',
         info='Breitbandlautsprecher mit Neodym-Magnet. Der Magnet ist stark: nicht an Bankkarten oder Handys halten.',
         marks=[mark('cyl', 3, 3, 40, fill='#55493C'), mark('cyl', 15, 15, 16, fill='#6B6158')]),
    teil('treiber_r', 'speaker_driver', 'Lautsprecher rechts', 'Lautsprecher', 'cyl',
         x=110, y=12, w=46, z=32, h=24, mass=55, materials=TREIBER, color='#3B3B3B', label=False,
         info='Zweiter Lautsprecher für Stereo-Klang.',
         marks=[mark('cyl', 3, 3, 40, fill='#55493C'), mark('cyl', 15, 15, 16, fill='#6B6158')]),
    teil('bt_chip', 'circuit_board', 'Bluetooth-Chip', 'Bluetooth', 'box',
         x=79, y=22, w=9, d=9, z=33.6, h=1.2, r=0.5, mass=0.5, materials=[['chip', 100]], color=CHIP,
         info='Empfängt die Musik per Funk vom Handy und wandelt sie in ein Tonsignal um.'),
    teil('verstaerker', 'circuit_board', 'Verstärker-Chip', 'Verstärker', 'box',
         x=92, y=22, w=8, d=8, z=33.6, h=1.2, r=0.5, mass=0.5, materials=[['chip', 100]], color=CHIP,
         info='Macht das schwache Tonsignal so stark, dass es die Lautsprecher bewegen kann. Wird beim Spielen warm.'),
    teil('usb_c', 'circuit_board', 'USB-C-Ladebuchse', 'USB-C', 'box', material_id='steel',
         x=103, y=29, w=4, d=9, z=33.6, h=3.2, r=1.2, mass=1, materials=[['stahl', 70], ['kontakte', 15], ['pcabs', 15]],
         color='#B7BCC0', info='Ladebuchse aus Stahlblech mit vergoldeten Kontakten, sitzt an der rechten Kappe.'),
    teil('platine', 'circuit_board', 'Platine', 'Platine', 'box',
         x=73, y=14, w=34, d=42, z=32, h=1.6, r=2, mass=18, color='#2E6B45',
         info='Leiterplatte mit Kupferbahnen und Lot, mit Steckern am Akku und an den Lautsprechern angeschlossen. '
              'In die Elektro-Sammlung geben.',
         marks=raster(6, 30, 5, 1, 3, 3, 5, r=0.5, fill='#B08A3A') + raster(4, 4, 1, 3, 2, 4, 0, 6, r=0.5, fill='#8A6F4A')),
    *[teil(f'schraube{k}', 'rubber_shell', 'Schraube Innenrahmen', 'Schrauben', 'cyl', material_id='steel',
           x=x, y=y, w=4, z=32, h=2, mass=0.4, materials=[['stahl', 100]], color='#C9CDD0', label=k == 0,
           info='Vier Kreuzschlitzschrauben halten den Innenrahmen im Gitter. Erst sichtbar, wenn die Kappen ab sind.',
           marks=[mark('box', 0.8, 1.7, 2.4, 0.6), mark('box', 1.7, 0.8, 0.6, 2.4)])
      for k, (x, y) in enumerate([(18, 10), (18, 56), (158, 10), (158, 56)])],
    teil('akku', 'li_ion_battery', 'Lithium-Ionen-Akku (2 Zellen)', 'Akku', 'box',
         x=57, y=16, w=66, d=38, z=12, h=19, r=8, mass=95,
         materials=[['lco', 40], ['graphit', 20], ['elektrolyt', 15], ['alu', 10], ['kupfer', 10], ['folien', 5]],
         info='Zwei Rundzellen (18650) in Schrumpffolie, zusammen etwa 5.000 mAh. Stecker abziehen, Pole abkleben '
              'und zur Batteriesammlung bringen; nie anbohren.',
         color='#3F6FA8', marks=[mark('box', 2, 1, 62, 17, 8, '#4A7DB8'), mark('box', 2, 20, 62, 17, 8, '#4A7DB8'),
                                 mark('box', 54, 14, 8, 10, 1, '#E8E8E8')]),
    teil('rahmen', 'rubber_shell', 'Innenrahmen (Kunststoff)', 'Innenrahmen', 'box',
         material_id='abs', x=16, y=8, w=148, d=54, z=8, h=24, r=8, mass=60, materials=[['pcabs', 100]],
         info='Stabiler Kunststoffrahmen, der Akku, Lautsprecher und Platine trägt. An den Enden mit den Kappen '
              'verschraubt.',
         color='#4A4F54', marks=[mark('box', 40, 7, 68, 40, 6, '#3A3F44'), mark('cyl', 8, 8, 30, fill='#3A3F44'),
                                 mark('cyl', 110, 8, 30, fill='#3A3F44')]),
]
passiv = [
    teil('passiv_l', 'speaker_driver', 'Passivmembran links', 'Passivmembran', 'box',
         material_id='rubber', x=14, y=13, w=6, d=44, z=13, h=44, r=3, explode=[-50, 0, 0], mass=20,
         materials=PASSIV, color='#5A6066',
         info='Gummimembran mit Metallgewicht, aber ohne Magnet. Sie schwingt mit und verstärkt die Bässe.',
         marks=[mark('box', 1.5, 10, 3, 24, 1.5, '#8A939A')]),
    teil('passiv_r', 'speaker_driver', 'Passivmembran rechts', 'Passivmembran', 'box',
         material_id='rubber', x=160, y=13, w=6, d=44, z=13, h=44, r=3, explode=[50, 0, 0], mass=20,
         materials=PASSIV, color='#5A6066', label=False, info='Zweite Passivmembran am anderen Ende.',
         marks=[mark('box', 1.5, 10, 3, 24, 1.5, '#8A939A')]),
]
teile = ([tasten] + list(reversed(gitter_o)) + innen + list(reversed(gitter_u))
         + list(reversed(kappe_l)) + passiv + list(reversed(kappe_r)))
explodiere(teile, abstand=30, gruppen=[[p['id'] for p in gitter_o], [p['id'] for p in gitter_u]],
           abstaende={'tasten': 20, 'rahmen': 60, 'bt_chip': 12, 'verstaerker': 12, 'usb_c': 12,
                      **{f'schraube{k}': 14 for k in range(4)}})
# Malerreihenfolge: zusammengebaut liegt das Innenleben hinter den Gitterscheiben, explodiert darüber.
for p in innen + passiv:
    p['sortBias'] = -60
for p in gitter_o + [tasten]:  # obere Gitterhälfte nach hinten schieben, damit die Lautsprecher frei liegen
    p['explode'][1] = -70
skaliere_masse(teile, oid='bluetooth_speaker')
schreibe('bluetooth_speaker', teile)
