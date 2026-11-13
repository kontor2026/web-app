"""3D-Modell: extension_cord. Erzeugt tools/kategorien/modelle/extension_cord.json.

Typische 4-fach-Steckdosenleiste mit beleuchtetem Schalter (225 × 54 × 38 mm), 1,4 m Kabel H05VV-F 3G1,5
und Schutzkontaktstecker. Das Kabel liegt hinter der Leiste aufgerollt (y 226..284), der Stecker liegt auf der
Seite dahinter, die Stifte zeigen nach hinten (y groß).
Explosion: Leiste in Ebenen nach oben (Oberteil, Schalter, Kontaktschienen, Unterteil), Kupferadern über dem
Kabelmantel, Stecker und Stifte nach hinten (dy > 0) abgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

WEISS = '#F1F2F0'
MESSING = '#D4B464'
DOSEN = [10, 54, 98, 142]  # y-Anfang der vier Steckdosen (je 40 mm)


def windungen(dm, n=4, breite=7.5):
    return [mark('cyl', i * breite, i * breite, dm - 2 * i * breite) for i in range(n)]


def steckdose(y0):
    """Runde Steckdosenmulde mit zwei Löchern und Schutzkontakten links und rechts."""
    return [mark('cyl', 8, y0, 38, 38, fill='#E2E3E0'), mark('cyl', 17, y0 + 16.5, 5, fill='#2A2E31'),
            mark('cyl', 32, y0 + 16.5, 5, fill='#2A2E31'), mark('box', 26, y0 + 1, 2, 6, 0.5, '#B7BCC0'),
            mark('box', 26, y0 + 31, 2, 6, 0.5, '#B7BCC0')]


teile = [
    teil('oberteil', 'plastic_housing', 'Gehäuse-Oberteil mit Steckdosen', 'Oberteil', 'box',
         x=0, y=0, w=54, d=225, z=19, h=19, r=8, mass=95, explode=[-80, 0, 45],
         info='Weißes PP oder PC mit vier Steckdosen. Innen mit Schrauben am Unterteil befestigt, die oft unter '
              'Aufklebern sitzen. Nur ausgesteckt öffnen!',
         color=WEISS, marks=sum((steckdose(y) for y in DOSEN), []) + [mark('box', 17, 191, 20, 26, 3, '#4A4D50')]),
    teil('schalter', 'rocker_switch', 'Beleuchteter Wippschalter', 'Schalter', 'box',
         x=17, y=191, w=20, d=26, z=20, h=18, r=2, mass=12, explode=[-80, 0, 75],
         materials=[['pcabs', 55], ['messing', 25], ['kupfer', 10], ['stahl', 5], ['chip', 5]],
         info='Schaltet beide Leiter ab, die rote Glimmlampe zeigt an, ob Strom anliegt. Lässt sich mit einem '
              'kleinen Schraubendreher aus dem Gehäuse drücken.',
         color='#C8423A', marks=[mark('box', 2, 2, 16, 10, 2, '#E35A4E'), mark('box', 2, 14, 16, 10, 2, '#A9362E')]),
    teil('glimmlampe', 'rocker_switch', 'Glimmlampe im Schalter', 'Glimmlampe', 'box', material_id='mixed_electronics',
         x=24, y=196, w=6, d=12, z=21, h=5, r=2.5, mass=1, materials=[['glas', 50], ['kupfer', 30], ['chip', 20]],
         color='#E8A060',
         info='Kleine Neon-Lampe mit Vorwiderstand. Leuchtet rot, solange der Schalter an ist und Strom anliegt.'),
    teil('kinderschutz_0', 'plastic_housing', 'Kinderschutz-Klappe', 'Kinderschutz', 'box',
         x=12, y=18, w=30, d=22, z=31, h=1.5, r=3, mass=1.5, color='#E8E8E2',
         info='Federnder Schieber unter jeder Dose. Er gibt die Löcher nur frei, wenn beide Stifte gleichzeitig drücken.',
         marks=[mark('box', 3, 9, 8, 4, 1, '#C9CBC6'), mark('box', 19, 9, 8, 4, 1, '#C9CBC6')]),
    teil('kinderschutz_1', 'plastic_housing', 'Kinderschutz-Klappe', 'Kinderschutz', 'box',
         x=12, y=62, w=30, d=22, z=31, h=1.5, r=3, mass=1.5, color='#E8E8E2', label=False,
         info='Federnder Schieber unter jeder Dose. Er gibt die Löcher nur frei, wenn beide Stifte gleichzeitig drücken.',
         marks=[mark('box', 3, 9, 8, 4, 1, '#C9CBC6'), mark('box', 19, 9, 8, 4, 1, '#C9CBC6')]),
    teil('kinderschutz_2', 'plastic_housing', 'Kinderschutz-Klappe', 'Kinderschutz', 'box',
         x=12, y=106, w=30, d=22, z=31, h=1.5, r=3, mass=1.5, color='#E8E8E2', label=False,
         info='Federnder Schieber unter jeder Dose. Er gibt die Löcher nur frei, wenn beide Stifte gleichzeitig drücken.',
         marks=[mark('box', 3, 9, 8, 4, 1, '#C9CBC6'), mark('box', 19, 9, 8, 4, 1, '#C9CBC6')]),
    teil('kinderschutz_3', 'plastic_housing', 'Kinderschutz-Klappe', 'Kinderschutz', 'box',
         x=12, y=150, w=30, d=22, z=31, h=1.5, r=3, mass=1.5, color='#E8E8E2', label=False,
         info='Federnder Schieber unter jeder Dose. Er gibt die Löcher nur frei, wenn beide Stifte gleichzeitig drücken.',
         marks=[mark('box', 3, 9, 8, 4, 1, '#C9CBC6'), mark('box', 19, 9, 8, 4, 1, '#C9CBC6')]),
    teil('schrauben', 'plastic_housing', 'Gehäuseschrauben (6 Stück)', 'Schrauben', 'cyl', material_id='steel',
         x=4, y=120, w=4, z=3, h=28, mass=3, color='#9BA3A8', materials=[['stahl', 100]],
         info='Halten Ober- und Unterteil zusammen; Köpfe sitzen unten, oft unter Gummifüßen oder Aufklebern.',
         marks=[mark('cyl', 1, 1, 2, fill='#5E656A')]),
    teil('schiene_l', 'plug_pins', 'Kontaktschiene Phase', 'Schiene Phase', 'box',
         material_id='copper', x=13, y=12, w=3, d=176, z=5, h=12, r=0.5, mass=12, materials=[['messing', 100]],
         info='Gestanztes Messingblech mit federnden Klemmen für je einen Steckerstift. Wertvoll fürs Recycling.',
         color=MESSING, marks=raster(0.5, 14.5, 1, 4, 2, 9, 0, 44, r=0.5, fill='#B08F3C')),
    teil('schiene_pe', 'plug_pins', 'Schutzleiter-Schiene', 'Schutzleiter', 'box',
         material_id='copper', x=25.5, y=10, w=3, d=176, z=5, h=12, r=0.5, mass=14, materials=[['messing', 100]],
         info='Verbindet die Schutzkontakt-Bügel aller Steckdosen mit dem grün-gelben Leiter.',
         color=MESSING, marks=raster(0.5, 1, 1, 4, 2, 6, 0, 44, r=0.5, fill='#B08F3C')),
    teil('schiene_n', 'plug_pins', 'Kontaktschiene Neutralleiter', 'Neutralleiter', 'box',
         material_id='copper', x=38, y=12, w=3, d=176, z=5, h=12, r=0.5, mass=12, materials=[['messing', 100]],
         info='Zweite Messingschiene für den blauen Neutralleiter.', color=MESSING,
         marks=raster(0.5, 14.5, 1, 4, 2, 9, 0, 44, r=0.5, fill='#B08F3C')),
    teil('zugentlastung', 'plastic_housing', 'Zugentlastung', 'Zugentlastung', 'box',
         x=15, y=205, w=24, d=14, z=4, h=8, r=1, mass=4,
         info='Kunststoffbügel mit zwei Schrauben, der das Kabel festklemmt, damit es nicht aus den Klemmen reißt.',
         color='#3A3D40', marks=[mark('cyl', 2, 4, 6), mark('cyl', 16, 4, 6)]),
    teil('unterteil', 'plastic_housing', 'Gehäuse-Unterteil', 'Unterteil', 'box',
         x=0, y=0, w=54, d=225, z=0, h=19, r=8, mass=80,
         info='Wanne mit Stegen, in die die Schienen eingelegt sind. Ohne Metallteile kann der Kunststoff recycelt werden.',
         color=WEISS, marks=[mark('box', 4, 4, 46, 217, 6, '#E2E3E0')]),
    teil('adern', 'cable_copper_core', 'Drei Kupferadern (1,5 mm²)', 'Adern', 'cyl',
         x=3, y=229, w=52, z=1, h=14, mass=62, materials=[['kupfer', 70], ['pvc', 30]],
         info='Braun (Phase), Blau (Neutralleiter) und Grün-Gelb (Schutzleiter), jede Ader aus feinen Kupferdrähten '
              'mit eigener Isolierung.',
         color='#C5803D', marks=windungen(52, 3, 7) + [mark('cyl', 2, 22, 5, fill='#7B4A2A'),
                                                       mark('cyl', 2, 27, 5, fill='#3A6BB0'),
                                                       mark('cyl', 2, 32, 5, fill='#7FB04A')]),
    teil('mantel', 'cable_insulation', 'Kabelmantel', 'Kabelmantel', 'cyl',
         x=0, y=226, w=58, z=0, h=16, mass=70, materials=[['pvc', 100]],
         info='Weißer PVC-Mantel, 1,4 m lang, hier aufgerollt. Stecker und Leiste abschneiden, dann längs aufschlitzen.',
         color=WEISS, marks=windungen(58)),
    teil('stecker', 'plastic_housing', 'Schutzkontaktstecker', 'Stecker', 'box',
         material_id='pvc', x=10, y=286, w=36, d=24, z=0, h=36, r=4, explode=[0, 14, 0], mass=30,
         materials=[['pvc', 85], ['stahl', 10], ['messing', 5]],
         info='Angespritzter Weich-PVC-Stecker mit zwei Schutzkontakt-Blechen an den Seiten. '
              'Direkt am Stecker abschneiden.',
         color=WEISS, marks=[mark('box', 2, 2, 32, 20, 3, '#E2E3E0')]),
    teil('stift_l', 'plug_pins', 'Steckerstift links', 'Stift', 'box',
         x=16.1, y=310, w=4.8, d=19, z=15.6, h=4.8, r=2.4, explode=[0, 30, 0], mass=4.5,
         materials=[['messing', 95], ['nickel', 5]],
         info='Vernickeltes Messing, 4,8 mm dick. Im Stecker eingespritzt, kommt nur beim Aufschneiden heraus.',
         color='#C9CDD0'),
    teil('stift_r', 'plug_pins', 'Steckerstift rechts', 'Stift', 'box',
         x=35.1, y=310, w=4.8, d=19, z=15.6, h=4.8, r=2.4, explode=[0, 30, 0], mass=4.5,
         materials=[['messing', 95], ['nickel', 5]], label=False,
         info='Zweiter Stift, 19 mm Abstand zum ersten.', color='#C9CDD0'),
]
explodiere(teile, abstand=24, abstaende={'adern': 30, 'glimmlampe': 12})
skaliere_masse(teile, oid='extension_cord')
schreibe('extension_cord', teile)
