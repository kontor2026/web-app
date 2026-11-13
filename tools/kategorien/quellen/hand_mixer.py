"""3D-Modell: hand_mixer. Erzeugt tools/kategorien/modelle/hand_mixer.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Handmixer steht auf seinen eingesetzten Rührbesen: Körper waagerecht entlang x (0..200), Griff oben,
# Besen vorne links (x 35..67) nach unten. Kabel kommt hinten rechts (x = 200) heraus.
# Explosion: Besen bleiben stehen, Unterschale, Getriebe, Motor, Schalter und Oberschale schweben darüber,
# Kabel nach rechts (dx > 0).
BESEN = [(12, 'links'), (46, 'rechts')]

teile = [
    teil('auswurftaste', 'plastic_housing', 'Auswurftaste', 'Auswurftaste', 'box',
         x=20, y=35, w=26, d=20, z=150, h=6, r=4, mass=8, materials=[['pcabs', 80], ['stahl', 20]],
         info='Drückt über eine Stahlfeder die Besen aus dem Getriebe. Kappe ist nur aufgesteckt.',
         color='#9AA2A6'),
    teil('oberschale', 'plastic_housing', 'Gehäuse-Oberschale mit Griff', 'Oberschale', 'box',
         x=0, y=5, w=200, d=80, z=110, h=40, r=22, mass=150,
         info='Obere Hälfte mit Handgriff. Die Schrauben sitzen von unten in der Unterschale, eine oft unter dem Typenschild.',
         color='#E9EEF2', marks=[mark('box', 70, 28, 105, 24, 10, fill='#C5CDD3'), mark('box', 50, 32, 14, 16, 3, fill='#5F6B75')]),
    teil('schalter', 'plastic_housing', 'Stufenschalter mit Entstörkondensator', 'Schalter', 'box', material_id='mixed_electronics',
         x=40, y=30, w=30, d=30, z=100, h=14, r=2, mass=20,
         materials=[['pcabs', 50], ['kupfer', 25], ['kontakte', 10], ['pp', 15]],
         info='Schiebeschalter für fünf Stufen; der Kondensator verhindert Funkstörungen. Kabel sind gelötet oder gesteckt.',
         color='#5F6B75', marks=[mark('box', 4, 8, 10, 14, 2, fill='#9AA2A6'), mark('box', 17, 5, 10, 20, 2, fill='#D9B44A')]),
    teil('luefterrad', 'electric_motor', 'Lüfterrad', 'Lüfterrad', 'box', material_id='pp',
         x=154, y=25, w=10, d=40, z=78, h=36, r=2, mass=8, materials=[['pp', 100]],
         info='Sitzt auf der Motorwelle und bläst Kühlluft durch die Schlitze im Gehäuse.',
         color='#5F6B75', marks=raster(2, 3, 1, 6, 6, 3, 0, 6, r=1, fill='#4A545C')),
    teil('motor', 'electric_motor', 'Universalmotor', 'Motor', 'box',
         x=90, y=22, w=62, d=46, z=76, h=40, r=16, mass=280,
         materials=[['kupfer', 32], ['stahl', 55], ['graphit', 3], ['pcabs', 10]],
         info='Motor mit Kupferwicklungen und Kohlebürsten, treibt über eine Schnecke beide Besen an. Mit zwei Schrauben befestigt.',
         marks=[mark('box', 8, 6, 46, 34, 12, fill='#B87333'), mark('cyl', 2, 18, 10, fill='#9AA2A6')]),
    teil('getriebe', 'electric_motor', 'Schneckengetriebe', 'Getriebe', 'box', material_id='nylon',
         x=25, y=15, w=60, d=60, z=82, h=18, r=6, mass=60, materials=[['nylon', 55], ['stahl', 45]],
         info='Zwei Kunststoffzahnräder mit Stahlbuchsen drehen die Besen gegenläufig. Sie sind gefettet; Fett mit Papier abwischen.',
         color='#E9EEF2', marks=[mark('cyl', 6, 3, 24, fill='#D5DADE'), mark('cyl', 6, 33, 24, fill='#D5DADE'), mark('box', 34, 25, 26, 10, 3, fill='#9AA2A6')]),
    teil('unterschale', 'plastic_housing', 'Gehäuse-Unterschale', 'Unterschale', 'box',
         x=0, y=5, w=200, d=80, z=72, h=38, r=22, mass=140,
         info='Untere Hälfte mit den beiden Öffnungen für die Besen und Lüftungsschlitzen. Kommt zum Kunststoff, wenn alle Metallteile entfernt sind.',
         color='#E9EEF2', marks=[mark('cyl', 44, 16, 14, fill='#9AA2A6'), mark('cyl', 44, 50, 14, fill='#9AA2A6')] + raster(150, 15, 5, 1, 4, 50, 9, r=1, fill='#9AA2A6')),
]
for y, seite in BESEN:
    teile.append(teil(f'schaft_{seite}', 'mixer_beaters', f'Besenschaft {seite}', f'Schaft {seite}', 'cyl',
                      x=47, y=y + 12, w=8, z=45, h=37, mass=12, materials=[['stahl', 100]],
                      info='Edelstahlschaft mit Nut, rastet im Getriebe ein. Auswurftaste drücken, dann lösen sich die Besen.',
                      color='#B8BEC4', label=seite == 'links'))
    teile.append(teil(f'besen_{seite}', 'mixer_beaters', f'Rührbesen {seite}', f'Besen {seite}', 'cyl',
                      x=35, y=y, w=32, z=0, h=45, mass=35, materials=[['stahl', 100]],
                      info='Vier gebogene Edelstahldrähte. Reiner Stahl: kommt zum Altmetall.',
                      color='#C9CED2', label=seite == 'links',
                      marks=[mark('box', 2, 14, 28, 4, 1, fill='#9AA2A6'), mark('box', 14, 2, 4, 28, 1, fill='#9AA2A6')]))
teile += [
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=150, y=41, w=50, d=8, z=74, h=8, r=4, explode=[70, 0, 0], mass=60, materials=[['pvc', 90], ['pp', 10]],
         info='Etwa 1,2 m PVC-Mantel mit Eurostecker. Längs aufschlitzen, um die Kupferadern freizulegen.',
         color='#2E3338', marks=[mark('box', 40, 1, 10, 6, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=150, y=43.5, w=50, d=3, z=76.5, h=3, r=1, explode=[70, 0, 15], mass=25,
         info='Zwei Kupferadern aus feiner Litze. Kupfer lässt sich fast verlustfrei wiederverwerten.',
         color='#B87333'),
]

BESENTEILE = [p['id'] for p in teile if p['component_id'] == 'mixer_beaters']
explodiere(teile, abstand=20, fest=BESENTEILE)
skaliere_masse(teile, oid='hand_mixer')
schreibe('hand_mixer', teile)
