"""3D-Modell: desk_lamp. Erzeugt tools/kategorien/modelle/desk_lamp.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# LED-Schreibtischlampe mit Gelenkarm (150 × 150 × 400 mm). Schwerer Stahlfuß mit Filz-Bodenplatte, hinten (y klein)
# das Drehgelenk, zwei senkrechte Aluminium-Armteile mit Ellbogengelenk und Zugfeder, oben das Kopfgelenk mit einem
# kurzen Kopfarm nach vorn, an dem der kegelförmige Schirm (vier Scheiben) mit LED-Modul und Streuscheibe hängt.
# Explosion: Bodenplatte bleibt liegen, Fuß, Gewicht, Gelenke und Armteile schweben übereinander. Der Schirm mit
# LED-Modul und Streuscheibe wandert nach links (dx < 0), die Zugfeder nach vorn, Kabel und Stecker nach rechts.
ALU = '#C9CED2'
SCHWARZ = '#2B2F33'
SCHRAUBE = '#9AA2A8'
KREUZ = [mark('box', 1.5, 4.5, 9, 3, 0.5, '#5E656A')]

schirm_info = ('Pulverbeschichtetes Stahlblech, leitet die Wärme der LEDs ab. Den Haltering am Kopfarm abschrauben; '
               'ab ins Altmetall.')
schirm = [
    teil(f'schirm{i}', 'lamp_shade', 'Lampenschirm', 'Schirm', 'cyl',
         x=75 - w / 2, y=95 - w / 2, w=w, z=z, h=h, mass=m, color=SCHWARZ, label=i == 0,
         info=schirm_info if i == 0 else 'Teil des kegelförmigen Lampenschirms.',
         marks=[mark('cyl', w / 2 - 12, w / 2 - 12, 24, fill='#3A3F44'), mark('cyl', w / 2 - 4, w / 2 - 4, 8, fill=SCHRAUBE)]
         if i == 0 else [])
    for i, (w, z, h, m) in enumerate([(56, 372, 8, 18), (84, 362, 10, 28), (102, 350, 12, 36), (112, 341, 9, 30)])
]
teile = [
    teil('kopfgelenk', 'lamp_arm', 'Kopfgelenk', 'Kopfgelenk', 'cyl',
         x=63, y=16, w=24, z=370, h=30, mass=25, materials=[['alu', 80], ['stahl', 20]], color=SCHWARZ,
         info='Gelenk zwischen Oberarm und Kopf mit Stahlschraube und Reibscheibe. Schraube lösen, dann trennen.',
         marks=[mark('cyl', 7, 7, 10, fill=SCHRAUBE)]),
    teil('kopfarm', 'lamp_arm', 'Kopfarm', 'Kopfarm', 'box',
         x=69, y=35, w=12, d=62, z=380, h=10, r=5, mass=25, color=ALU,
         info='Kurzes Aluminiumrohr zum Schirm. Innen läuft das dünne Kabel zum LED-Modul.'),
    *schirm,
    teil('ledmodul', 'led_module', 'LED-Modul', 'LED-Modul', 'cyl',
         x=35, y=55, w=80, z=340, h=3, mass=25, materials=[['alu', 50], ['led', 20], ['fr4', 20], ['kupfer', 10]],
         color='#ECECE6',
         info='Aluminiumplatine mit 24 kleinen weißen LEDs. Hält viele Jahre; sie wird mit zwei Schrauben gelöst.',
         marks=[mark('cyl', 2, 2, 76, fill='#DADAD2')]
         + [mark('box', 40 + 30 * c - 2.5, 40 + 30 * s - 2.5, 5, 5, 1, '#F6D86B')
            for c, s in [(1, 0), (0.87, 0.5), (0.5, 0.87), (0, 1), (-0.5, 0.87), (-0.87, 0.5), (-1, 0), (-0.87, -0.5),
                         (-0.5, -0.87), (0, -1), (0.5, -0.87), (0.87, -0.5)]]
         + [mark('box', 40 + 16 * c - 2.5, 40 + 16 * s - 2.5, 5, 5, 1, '#F6D86B')
            for c, s in [(1, 0), (0.5, 0.87), (-0.5, 0.87), (-1, 0), (-0.5, -0.87), (0.5, -0.87)]]
         + [mark('cyl', 36, 36, 8, fill='#2E6B45')]),
    teil('streuscheibe', 'led_module', 'Streuscheibe', 'Streuscheibe', 'cyl', material_id='pc',
         x=22, y=42, w=106, z=337, h=3, mass=15, materials=[['pcabs', 100]], color='#F4F6F8', opacity=0.75,
         info='Milchige Kunststoffscheibe, die das grelle LED-Licht weich verteilt. Eingeclipst, vorsichtig heraushebeln.'),
    teil('oberarm', 'lamp_arm', 'Oberarm', 'Oberarm', 'box',
         x=67, y=20, w=16, d=16, z=254, h=116, r=4, mass=50, color=ALU,
         info='Aluminiumrohr mit dem Kabel innen. Aluminium lässt sich sehr gut recyceln.'),
    teil('gelenkschraube', 'lamp_arm', 'Gelenkschraube mit Rändelmutter', 'Gelenkschraube', 'cyl', material_id='steel',
         x=69, y=22, w=12, z=242, h=4, mass=8, materials=[['stahl', 100]], color=SCHRAUBE, sortBias=-30,
         info='Stahlschraube quer durch das Ellbogengelenk. Mit der Rändelmutter stellt man ein, wie schwer sich der Arm '
              'bewegt.', marks=[mark('cyl', 3, 3, 6, fill='#5E656A')]),
    teil('ellbogen', 'lamp_arm', 'Ellbogengelenk', 'Ellbogen', 'cyl',
         x=63, y=16, w=24, z=230, h=24, mass=25, materials=[['alu', 70], ['stahl', 30]], color=SCHWARZ,
         info='Mittleres Gelenk aus Aluminiumguss. Nach Herausziehen der Gelenkschraube fallen die Armteile auseinander.',
         marks=[mark('cyl', 7, 7, 10, fill=SCHRAUBE)]),
    teil('zugfeder', 'lamp_arm', 'Zugfeder', 'Zugfeder', 'box', material_id='steel',
         x=69, y=40, w=12, d=6, z=60, h=150, r=3, mass=20, materials=[['stahl', 100]], color='#9AA2A8',
         info='Stahlfeder, die den Arm in jeder Stellung hält. Steht unter Spannung: beim Aushängen festhalten.',
         marks=[mark('box', 1, 1, 10, 4, 2, '#7E868C')]),
    teil('unterarm', 'lamp_arm', 'Unterarm', 'Unterarm', 'box',
         x=67, y=20, w=16, d=16, z=40, h=190, r=4, mass=80, color=ALU,
         info='Längstes Armteil aus Aluminiumrohr. Nach Lösen der Gelenkschrauben vom Fuß abnehmen.',
         marks=[mark('cyl', 4, 4, 8, fill='#4A5156')]),
    teil('drehgelenk', 'lamp_arm', 'Drehgelenk am Fuß', 'Drehgelenk', 'cyl',
         x=60, y=13, w=30, z=25, h=15, mass=40, materials=[['alu', 60], ['stahl', 30], ['pcabs', 10]], color=SCHWARZ,
         info='Lässt den Arm drehen. Durch die Mitte läuft das Kabel in den Fuß.',
         marks=[mark('cyl', 9, 9, 12, fill='#1E2226')]),
    teil('standfuss', 'steel_lamp_base', 'Fußgehäuse', 'Fuß', 'box',
         x=0, y=0, w=150, d=150, z=3, h=22, r=10, mass=180, materials=[['stahl', 95], ['pcabs', 5]], color=SCHWARZ,
         info='Stahlblech-Gehäuse mit Touch-Feld zum Ein- und Dimmen. Von unten verschraubt.',
         marks=[mark('cyl', 40, 110, 20, fill='#3A4046'), mark('cyl', 45, 115, 10, fill='#5DADE2'),
                mark('box', 66, 117, 34, 6, 3, '#3A4046'), mark('box', 66, 117, 20, 6, 3, '#9AA2A8')]),
    teil('touch', 'led_module', 'Touch-Sensor', 'Touch-Sensor', 'box', material_id='pcb',
         x=32, y=102, w=76, d=34, z=20, h=1.6, r=2, mass=6,
         materials=[['fr4', 55], ['kupfer', 20], ['chip', 15], ['lot', 10]], color='#2E6B45',
         info='Kleine Platine direkt unter dem Touch-Feld. Sie merkt die Berührung durch das Blech und ist mit einem '
              'Flachkabel am Treiber angesteckt.',
         marks=[mark('cyl', 8, 8, 18, fill='#C5803D'), mark('box', 40, 10, 8, 8, 0.5, '#22272B')]),
    teil('treiber', 'led_module', 'LED-Treiber', 'Treiber', 'box', material_id='pcb',
         x=20, y=40, w=60, d=40, z=18, h=1.6, r=2, mass=15,
         materials=[['fr4', 45], ['kupfer', 25], ['chip', 15], ['ferrit', 10], ['lot', 5]], color='#2E6B45',
         info='Kleine Platine im Fuß: macht aus 230 Volt den Strom für die LEDs. Mit zwei Schrauben auf dem Gewicht.',
         marks=[mark('cyl', 6, 8, 14, fill='#C5803D'), mark('box', 30, 10, 10, 10, 1, '#22272B'),
                mark('cyl', 44, 22, 10, fill='#3C5A8A'), mark('box', 6, 28, 18, 8, 1, '#E8E8E8')]),
    teil('gewicht', 'steel_lamp_base', 'Gewichtsplatte', 'Gewicht', 'box',
         x=15, y=15, w=120, d=120, z=4, h=14, r=6, mass=320, color='#5E656A',
         info='Schwere Stahlplatte, damit die Lampe nicht umkippt. Reines Metall, ab ins Altmetall.',
         marks=[mark('cyl', 3, 3, 6, fill='#4A5156'), mark('cyl', 111, 3, 6, fill='#4A5156'),
                mark('cyl', 3, 111, 6, fill='#4A5156'), mark('cyl', 111, 111, 6, fill='#4A5156')]),
    *[teil(f'schraube{i}', 'steel_lamp_base', 'Schraube Bodenplatte', 'Schrauben', 'cyl', material_id='steel',
           x=x, y=y, w=6, z=3, h=1, mass=1, materials=[['stahl', 100]], color=SCHRAUBE, label=i == 0,
           info='Vier Kreuzschlitzschrauben halten Bodenplatte, Gewicht und Fußgehäuse zusammen.',
           marks=[mark('box', 1, 2.6, 4, 0.8), mark('box', 2.6, 1, 0.8, 4)])
      for i, (x, y) in enumerate([(18, 18), (126, 18), (18, 126), (126, 126)])],
    teil('bodenplatte', 'steel_lamp_base', 'Bodenplatte mit Filz', 'Bodenplatte', 'box',
         x=1, y=1, w=148, d=148, z=0, h=3, r=9, mass=40, materials=[['stahl', 75], ['textil', 25]], color='#3A3F44',
         info='Stahlblech mit Filz auf der Unterseite, damit der Tisch keine Kratzer bekommt. Filz vor dem Recycling abziehen.',
         marks=[mark('box', 6, 6, 136, 136, 7, '#33383C')]),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=10, y=4, w=130, d=8, z=0, h=8, r=4, explode=[190, 0, 0], mass=50, materials=[['pvc', 90], ['pp', 10]],
         color=SCHWARZ, info='1,8 m PVC-Kabel. Längs aufschlitzen, um die Kupferadern zu trennen.',
         marks=[mark('box', 0, 0, 16, 8, 2, '#4A5156'), mark('box', 60, 0, 22, 8, 3, '#3A3F44')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=10, y=16, w=130, d=4, z=0, h=4, r=1, explode=[190, 0, 0], mass=25, color='#B87333',
         info='Zwei dünne Kupferadern. Kupfer ist wertvoll und wird eingeschmolzen.'),
    teil('stecker', 'cable_insulation', 'Eurostecker', 'Stecker', 'box',
         x=110, y=26, w=30, d=16, z=0, h=12, r=5, explode=[190, 0, 0], mass=15,
         materials=[['pvc', 70], ['messing', 30]], color=SCHWARZ,
         info='Angespritzter Stecker mit zwei Messingstiften. Nicht zu öffnen: das ganze Kabel zum Elektroschrott.',
         marks=[mark('box', 22, 4, 8, 8, 3, '#3A3F44')]),
]
bewegt = {p['id'] for p in schirm} | {'ledmodul', 'streuscheibe', 'zugfeder'}
explodiere([p for p in teile if p['id'] not in bewegt], abstand=22, fest=('bodenplatte',),
           abstaende={'treiber': 12, 'touch': 12, 'gelenkschraube': 10, **{f'schraube{i}': 8 for i in range(4)}})
# Schirmgruppe links neben dem Arm, auf Höhe des Oberarms; Zugfeder neben dem Unterarm nach vorn.
oben = next(p for p in teile if p['id'] == 'oberarm')['explode'][2]
for p in schirm:
    p['explode'] = [-190, 0, oben]
for pid, dz in (('ledmodul', oben - 45), ('streuscheibe', oben - 90)):
    next(p for p in teile if p['id'] == pid)['explode'] = [-190, 0, dz]
unten = next(p for p in teile if p['id'] == 'unterarm')['explode'][2]
next(p for p in teile if p['id'] == 'zugfeder')['explode'] = [0, 60, unten]
skaliere_masse(teile, oid='desk_lamp')
schreibe('desk_lamp', teile)
