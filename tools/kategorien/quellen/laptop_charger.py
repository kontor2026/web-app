"""3D-Modell: laptop_charger. Erzeugt tools/kategorien/modelle/laptop_charger.json.

Typisches 65-W-Laptop-Netzteil („Netzteil-Ziegel“, 98 × 50 × 24 mm) mit fest angeschlossenem Ladekabel und
Hohlstecker. Das Kabel ist auf dem Ziegel zu einem flachen Bündel gelegt, der Stecker liegt rechts daneben.
Links sitzt die Netzbuchse (C6, „Kleeblatt“) für das separate Netzkabel.
Explosion: Kabelbündel und Stecker nach rechts (dx > 0) auf den Tisch, Ziegel in Ebenen nach oben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

GEH = '#2B2E31'
DX = 135
ELKO = [['alu', 55], ['papier', 20], ['pcabs', 10], ['gummi', 5], ['kupfer', 10]]

teile = [
    teil('klettband', 'cable_insulation', 'Kabelbinder mit Klettverschluss', 'Klettband', 'box',
         material_id='pvc', x=48, y=3, w=9, d=44, z=24, h=7, r=2, explode=[DX, 0, 30], mass=2,
         materials=[['nylon', 100]], sortBias=5,
         info='Hält das aufgerollte Kabel zusammen. Einfach abziehen, es kommt in den Restmüll oder wird weiterverwendet.',
         color='#55606A', marks=raster(1.5, 2, 1, 8, 6, 2, 0, 5, fill='#4A535C')),
    teil('kabel_adern', 'cable_copper_core', 'Kupferadern des Ladekabels', 'Adern', 'cyl',
         x=20, y=9, w=60, d=32, z=25, h=4, explode=[DX, 0, 14], mass=28,
         materials=[['kupfer', 75], ['pvc', 25]],
         info='Zwei Leiter für Plus und Minus, oft als Innenader mit Kupfergeflecht darum. '
              'Nach dem Abisolieren kommt reines Kupfer zum Vorschein.',
         color='#C5803D', marks=[mark('cyl', 6, 4, 48, 24, fill='#B06F33'), mark('cyl', 12, 8, 36, 16, fill='#C5803D'),
                                 mark('cyl', 18, 11, 24, 10, fill='#34383C')]),
    teil('kabel_mantel', 'cable_insulation', 'Kabelmantel (Ladekabel, 1,8 m, aufgerollt)', 'Kabelmantel', 'cyl',
         x=14, y=5, w=72, d=40, z=24, h=6, explode=[DX, 0, -24], mass=42,
         info='Schwarzer PVC-Mantel, hier aufgerollt. Mit Abisolierzange längs aufschlitzen; '
              'nahe am Stecker sitzt meist ein Ferritkern gegen Funkstörungen.',
         color='#34373B', marks=[mark('cyl', 3, 2, 66, 36, fill='#2B2E31'), mark('cyl', 7, 4, 58, 32, fill='#34373B'),
                                 mark('cyl', 11, 6.5, 50, 27, fill='#2B2E31'), mark('cyl', 15, 9, 42, 22, fill='#34373B'),
                                 mark('cyl', 19, 11.5, 34, 17, fill='#34383C')]),
    teil('knickschutz', 'cable_insulation', 'Knickschutz am Gehäuse', 'Knickschutz', 'box',
         material_id='pvc', x=98, y=5, w=7, d=9, z=7, h=9, r=3, explode=[DX - 20, -12, -7], mass=3,
         materials=[['tpe', 100]], sortBias=5,
         info='Weiche Tülle, damit das Kabel am Gehäuse nicht abknickt. Hier brechen Kabel am häufigsten.',
         color='#2B2E31', marks=raster(2, 1.5, 3, 1, 1, 6, 2, fill='#3A3D40')),
    teil('stecker_huelle', 'connector_shell', 'Steckergriff (angespritzt)', 'Steckergriff', 'box',
         material_id='pvc', x=98, y=19, w=12, d=12, z=0, h=12, r=4, explode=[DX + 5, 30, 0], mass=6,
         materials=[['pvc', 90], ['lot', 10]],
         info='Kunststoff um die Lötstellen gespritzt. Kabel direkt dahinter abschneiden, dann sind Stecker '
              'und Kabel getrennt.',
         color=GEH, marks=raster(3, 2, 3, 1, 1.5, 8, 3, r=0.5, fill='#3A3D40')),
    teil('hohlstecker', 'connector_shell', 'Hohlstecker (5,5 mm)', 'Hohlstecker', 'box',
         x=110, y=22.25, w=10, d=5.5, z=3.25, h=5.5, r=2.7, explode=[DX + 18, 30, -3.25], mass=3,
         materials=[['stahl', 70], ['nickel', 10], ['messing', 15], ['pcabs', 5]],
         info='Vernickelte Metallhülse (Minus) mit Kontakt innen (Plus). Ein Magnet zieht den Stahl an.',
         color='#C9CDD0', marks=[mark('box', 6, 1.5, 4, 2.5, 1.2, '#2A2E31')]),
    teil('oberschale', 'plastic_housing', 'Gehäuse-Oberschale', 'Oberschale', 'box',
         x=0, y=0, w=98, d=50, z=12, h=12, r=6, mass=45,
         info='Schwer entflammbares PC/ABS. Die Schalen sind fast immer verschweißt; nicht aufbrechen, '
              'denn innen können Kondensatoren noch geladen sein.',
         color=GEH, marks=[mark('box', 20, 10, 58, 30, 4, '#34383C'), mark('cyl', 82, 20, 10, fill='#7FD36B')]),
    teil('kuehlblech', 'circuit_board', 'Kühlblech mit Transistoren', 'Kühlblech', 'box',
         material_id='aluminium', x=36, y=40, w=34, d=3, z=4.6, h=16, r=0.3, mass=16,
         materials=[['alu', 85], ['chip', 10], ['kupfer', 5]],
         info='Aluminiumblech, an das Schalttransistor und Gleichrichter geschraubt sind. Leitet ihre Wärme ab.',
         color='#C9CDD0'),
    teil('elko_gross', 'circuit_board', 'Hochvolt-Elko (400 V)', 'Elko 400 V', 'cyl',
         material_id='mixed_electronics', x=17, y=26, w=18, z=4.6, h=17, mass=13, materials=ELKO,
         info='Speichert die gleichgerichtete Netzspannung von rund 325 Volt. Kann auch ausgesteckt noch '
              'geladen sein, Anschlüsse nie berühren.',
         color='#2F4F7A', marks=[mark('cyl', 2, 2, 14, fill='#B9C0C6'), mark('box', 8, 2, 2, 14, 0.5, '#8A939A')]),
    teil('drossel', 'circuit_board', 'Netzfilter-Drossel', 'Netzdrossel', 'box',
         material_id='mixed_electronics', x=17, y=5, w=13, d=15, z=4.6, h=14, r=2, mass=10,
         materials=[['ferrit', 55], ['kupfer', 40], ['pcabs', 5]],
         info='Ringkern aus Ferrit mit zwei Kupferwicklungen. Hält Störungen vom Stromnetz fern.',
         color='#3A3F44', marks=[mark('cyl', 1.5, 2, 10, 11, fill='#C5803D'), mark('cyl', 4, 4.5, 5, 6)]),
    teil('trafo', 'circuit_board', 'Übertrager (Trafo)', 'Trafo', 'box',
         material_id='mixed_electronics', x=40, y=10, w=24, d=24, z=4.6, h=18, r=1, mass=34,
         materials=[['ferrit', 55], ['kupfer', 35], ['pcabs', 5], ['polyester', 5]],
         info='Ferritkern mit Kupferwicklungen, in gelbes Isolierband gewickelt. Trennt die Netzspannung sicher '
              'vom 19-Volt-Ausgang.',
         color='#E2C34A', marks=[mark('box', 3, 3, 18, 18, 1, '#3A3F44'), mark('box', 7, 7, 10, 10, 1, '#C5803D')]),
    teil('elko_aus1', 'circuit_board', 'Ausgangs-Elko', 'Elko Ausgang', 'cyl',
         material_id='mixed_electronics', x=72, y=8, w=10, z=4.6, h=14, mass=4, materials=ELKO,
         info='Glätten die 19-Volt-Ausgangsspannung, damit der Laptop gleichmäßig geladen wird.',
         color='#3B3B3B', marks=[mark('cyl', 2, 2, 6, fill='#B9C0C6')]),
    teil('elko_aus2', 'circuit_board', 'Ausgangs-Elko', 'Elko Ausgang', 'cyl',
         material_id='mixed_electronics', x=72, y=22, w=10, z=4.6, h=14, mass=4, materials=ELKO,
         info='Zweiter Ausgangskondensator, parallel zum ersten.', color='#3B3B3B', label=False,
         marks=[mark('cyl', 2, 2, 6, fill='#B9C0C6')]),
    teil('regler', 'circuit_board', 'Regler-Chip', 'Chip', 'box',
         material_id='pcb', x=42, y=44.5, w=8, d=3.5, z=4.6, h=1.6, r=0.3, mass=0.5, materials=[['chip', 100]],
         info='Steuert, wie oft der Strom durch den Trafo geschaltet wird, und begrenzt die Leistung auf 65 Watt.',
         color='#22272B', marks=[mark('cyl', 0.5, 0.5, 1)]),
    teil('netzbuchse', 'connector_shell', 'Netzbuchse C6 („Kleeblatt“)', 'Netzbuchse', 'box',
         material_id='copper', x=1, y=15, w=13, d=20, z=4.6, h=12, r=2, mass=8,
         materials=[['pcabs', 70], ['messing', 30]],
         info='Hier steckt das Netzkabel. Drei Messingkontakte in Kunststoff, auf die Platine gelötet.',
         color='#2B2E31', marks=[mark('cyl', 3, 2.5, 7), mark('cyl', 3, 10.5, 7), mark('cyl', 5, 7, 4, fill='#C9A74A')]),
    teil('sicherung', 'circuit_board', 'Glasrohrsicherung', 'Sicherung', 'box',
         material_id='mixed_electronics', x=3, y=38, w=12, d=5, z=4.6, h=5, r=2.4, mass=1,
         materials=[['glas', 60], ['messing', 30], ['kupfer', 10]], color='#D8E2E6', opacity=0.7,
         info='Brennt bei einem Kurzschluss durch und trennt das Netzteil vom Stromnetz.',
         marks=[mark('box', 0, 0, 2.5, 5, 1, '#C9CDD0'), mark('box', 9.5, 0, 2.5, 5, 1, '#C9CDD0')]),
    teil('gleichrichter', 'circuit_board', 'Brückengleichrichter', 'Gleichrichter', 'box',
         material_id='mixed_electronics', x=3, y=3, w=10, d=10, z=4.6, h=6, r=1, mass=2,
         materials=[['chip', 30], ['pcabs', 50], ['kupfer', 20]], color='#22272B',
         info='Vier Dioden in einem Block machen aus Wechselstrom pulsierenden Gleichstrom.',
         marks=[mark('box', 1, 1, 3, 3, 0.5, '#B7BCC0')]),
    teil('ykondensator', 'circuit_board', 'Entstör-Kondensator', 'Y-Kondensator', 'box',
         material_id='mixed_electronics', x=85, y=38, w=9, d=4, z=4.6, h=9, r=1.8, mass=1,
         materials=[['keramik', 70], ['kupfer', 20], ['pcabs', 10]], color='#2E6EB8',
         info='Blauer Scheibenkondensator, der Störsignale zwischen Netz- und Ausgangsseite ableitet.'),
    teil('platine', 'circuit_board', 'Platine', 'Platine', 'box',
         x=2, y=2, w=94, d=46, z=3, h=1.6, r=2, mass=24,
         info='Leiterplatte mit Netz- und Niederspannungsseite. Als Elektroschrott abgeben, dort werden Kupfer, '
              'Zinn und Gold zurückgewonnen.',
         color='#2E6B45', marks=[mark('box', 66, 3, 1.2, 40, 0.5, '#1E3F2A')]),
    teil('isolierfolie', 'plastic_housing', 'Isolierfolie', 'Isolierfolie', 'box',
         material_id='pc', x=1.5, y=1.5, w=95, d=47, z=2.4, h=0.4, r=2, mass=3, materials=[['pcabs', 100]],
         info='Dünne Kunststofffolie unter der Platine. Verhindert, dass Lötstellen das Gehäuse berühren.',
         color='#E8E4D8', opacity=0.75),
    teil('unterschale', 'plastic_housing', 'Gehäuse-Unterschale mit Typenschild', 'Unterschale', 'box',
         x=0, y=0, w=98, d=50, z=0, h=12, r=6, mass=50,
         info='Auf dem Typenschild an der Unterseite stehen 19 V und 3,42 A (65 W). Ganzes Netzteil zur '
              'Elektro-Sammlung bringen.',
         color=GEH, marks=[mark('box', 2, 15, 11, 20, 2, '#1E2022')]),
]
for p in teile:  # Bauteile auf der Platine zusammengebaut vor der Unterschale zeichnen, sonst scheinen sie durch
    if p['z'] == 4.6:
        p['sortBias'] = -14
explodiere(teile, abstand=22)
skaliere_masse(teile, oid='laptop_charger')
schreibe('laptop_charger', teile)
