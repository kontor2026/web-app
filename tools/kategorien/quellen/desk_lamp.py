"""3D-Modell: desk_lamp. Erzeugt tools/kategorien/modelle/desk_lamp.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# LED-Schreibtischlampe mit Gelenkarm (150 × 150 × 400 mm). Schwerer Stahlfuß, hinten (y klein) das Drehgelenk,
# zwei senkrechte Aluminium-Armteile mit Ellbogengelenk und Zugfeder, oben das Kopfgelenk mit einem kurzen
# Kopfarm nach vorn, an dem der Schirm mit LED-Modul und Streuscheibe hängt.
# Explosion: Fuß bleibt stehen, Gewicht, Gelenke und Armteile schweben übereinander (jedes Teil über der
# Oberkante des darunterliegenden), ebenso Streuscheibe, LED-Modul und Schirm. Kabel nach rechts (dx > 0).
ALU = '#C9CED2'
SCHWARZ = '#2B2F33'

teile = [
    teil('kopfgelenk', 'lamp_arm', 'Kopfgelenk', 'Kopfgelenk', 'cyl',
         x=63, y=16, w=24, z=370, h=30, mass=25, materials=[['alu', 80], ['stahl', 20]], color=SCHWARZ,
         info='Gelenk zwischen Oberarm und Kopf mit Stahlschraube und Reibscheibe. Schraube lösen, dann trennen.',
         marks=[mark('cyl', 7, 7, 10, fill='#9AA2A8')]),
    teil('kopfarm', 'lamp_arm', 'Kopfarm', 'Kopfarm', 'box',
         x=69, y=35, w=12, d=65, z=380, h=10, r=5, mass=25, color=ALU,
         info='Kurzes Aluminiumrohr zum Schirm. Innen läuft das dünne Kabel zum LED-Modul.'),
    teil('schirm', 'lamp_shade', 'Lampenschirm', 'Schirm', 'cyl',
         x=20, y=40, w=110, z=341, h=39, mass=120, color=SCHWARZ,
         info='Pulverbeschichtetes Stahlblech, leitet Wärme ab. Den Haltering am Kopfarm abschrauben; ab ins Altmetall.',
         marks=[mark('cyl', 40, 40, 30, fill='#3A3F44')]),
    teil('ledmodul', 'led_module', 'LED-Modul', 'LED-Modul', 'cyl',
         x=35, y=55, w=80, z=340, h=3, mass=25, materials=[['alu', 50], ['led', 20], ['fr4', 20], ['kupfer', 10]], color='#ECECE6',
         info='Aluminiumplatine mit vielen kleinen weißen LEDs. Hält viele Jahre; sie wird mit zwei Schrauben gelöst.',
         marks=raster(12, 12, 4, 4, 6, 6, 14, shape='cyl', fill='#F6D86B')),
    teil('streuscheibe', 'led_module', 'Streuscheibe', 'Streuscheibe', 'cyl', material_id='pc',
         x=22, y=42, w=106, z=338, h=2, mass=15, materials=[['pcabs', 100]], color='#F4F6F8', opacity=0.75,
         info='Milchige Kunststoffscheibe, die das grelle LED-Licht weich verteilt. Eingeclipst, vorsichtig heraushebeln.'),
    teil('oberarm', 'lamp_arm', 'Oberarm', 'Oberarm', 'box',
         x=67, y=20, w=16, d=16, z=254, h=116, r=4, mass=50, color=ALU,
         info='Aluminiumrohr mit dem Kabel innen. Aluminium lässt sich sehr gut recyceln.'),
    teil('ellbogen', 'lamp_arm', 'Ellbogengelenk', 'Ellbogen', 'cyl',
         x=63, y=16, w=24, z=230, h=24, mass=25, materials=[['alu', 70], ['stahl', 30]], color=SCHWARZ,
         info='Mittleres Gelenk; die Stahlschraube darin kann man mit einem Inbusschlüssel lösen.',
         marks=[mark('cyl', 7, 7, 10, fill='#9AA2A8')]),
    teil('zugfeder', 'lamp_arm', 'Zugfeder', 'Zugfeder', 'box', material_id='steel',
         x=69, y=40, w=12, d=6, z=60, h=150, r=3, mass=20, materials=[['stahl', 100]], color='#9AA2A8',
         info='Stahlfeder, die den Arm in jeder Stellung hält. Steht unter Spannung: beim Aushängen festhalten.'),
    teil('unterarm', 'lamp_arm', 'Unterarm', 'Unterarm', 'box',
         x=67, y=20, w=16, d=16, z=40, h=190, r=4, mass=80, color=ALU,
         info='Längstes Armteil aus Aluminiumrohr. Nach Lösen der Gelenkschrauben vom Fuß abnehmen.'),
    teil('drehgelenk', 'lamp_arm', 'Drehgelenk am Fuß', 'Drehgelenk', 'cyl',
         x=60, y=13, w=30, z=25, h=15, mass=40, materials=[['alu', 60], ['stahl', 30], ['pcabs', 10]], color=SCHWARZ,
         info='Lässt den Arm drehen. Durch die Mitte läuft das Kabel in den Fuß.',
         marks=[mark('cyl', 9, 9, 12, fill='#1E2226')]),
    teil('treiber', 'led_module', 'LED-Treiber mit Dimmer', 'Treiber', 'box', material_id='pcb',
         x=20, y=95, w=60, d=40, z=19, h=1.6, r=2, mass=15, materials=[['fr4', 45], ['kupfer', 25], ['chip', 15], ['ferrit', 10], ['lot', 5]],
         color='#2E6B45',
         info='Kleine Platine im Fuß: macht aus 230 Volt den Strom für die LEDs und regelt die Helligkeit über die Touch-Taste.',
         marks=[mark('box', 6, 8, 14, 14, 1, '#C5803D'), mark('box', 30, 10, 10, 10, 1, '#22272B')]),
    teil('gewicht', 'steel_lamp_base', 'Gewichtsplatte', 'Gewicht', 'box',
         x=15, y=15, w=120, d=120, z=3, h=15, r=6, mass=320, color='#5E656A',
         info='Schwere Stahlplatte, damit die Lampe nicht umkippt. Reines Metall, ab ins Altmetall.'),
    teil('standfuss', 'steel_lamp_base', 'Fußgehäuse', 'Fuß', 'box',
         x=0, y=0, w=150, d=150, z=0, h=25, r=10, mass=200, materials=[['stahl', 90], ['textil', 10]], color=SCHWARZ,
         info='Stahlblech-Gehäuse mit Filzunterseite und Touch-Taste. Bodenplatte abschrauben, um Kabel und Platine zu lösen.',
         marks=[mark('cyl', 40, 110, 20, fill='#5DADE2')]),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=10, y=4, w=130, d=8, z=0, h=8, r=4, explode=[170, 0, 0], mass=50, materials=[['pvc', 90], ['pp', 10]],
         color=SCHWARZ, info='1,8 m PVC-Kabel mit Eurostecker. Längs aufschlitzen, um die Kupferadern zu trennen.',
         marks=[mark('box', 0, 0, 16, 8, 2, '#4A5156')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=10, y=16, w=130, d=4, z=0, h=4, r=1, explode=[170, 0, 0], mass=25, color='#B87333',
         info='Zwei dünne Kupferadern. Kupfer ist wertvoll und wird eingeschmolzen.'),
]

explodiere(teile, abstand=25, fest=('standfuss',), abstaende={'treiber': 15})
skaliere_masse(teile, oid='desk_lamp')
schreibe('desk_lamp', teile)
