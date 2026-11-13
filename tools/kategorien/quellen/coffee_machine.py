"""3D-Modell: coffee_machine. Erzeugt tools/kategorien/modelle/coffee_machine.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Kaffeepadmaschine (classifier verlangt eine Pumpe): Wassertank hinten (y 0..65), Gehäuseturm mit Brühkopf oben,
# vorne (y groß) Tropfschale mit Tassenrost. Innen: Vibrationspumpe, Durchlauferhitzer, Silikonschläuche, Steuerplatine.
# Explosion nach Liste: Bodenplatte bleibt, Innenleben darüber, dann Gehäuse, Padhalter und Deckel.
# Wassertank nach hinten (dy < 0), Tropfschale und Rost nach vorne (dy > 0), Kabel nach rechts (dx > 0).

teile = [
    teil('deckel', 'plastic_housing', 'Brühkammerdeckel mit Hebel', 'Deckel', 'box',
         x=20, y=90, w=160, d=150, z=296, h=34, r=30, mass=130, materials=[['pcabs', 85], ['stahl', 10], ['gummi', 5]],
         info='Klappdeckel mit Duschsieb und Dichtung, wird mit dem Hebel verriegelt. Das Scharnier hat eine Stahlfeder.',
         color='#2E3338', marks=[mark('box', 50, 120, 60, 22, 8, fill='#9AA2A6'), mark('cyl', 40, 20, 80, fill='#3C4248')]),
    teil('padhalter', 'plastic_housing', 'Padhalter', 'Padhalter', 'cyl', material_id='pp',
         x=50, y=115, w=100, z=280, h=16, mass=50, materials=[['pp', 100]],
         info='Schale, in die das Kaffeepad gelegt wird. Reines Polypropylen; benutzte Pads gehören in den Bioabfall oder Restmüll.',
         color='#3C4248', marks=[mark('cyl', 15, 15, 70, fill='#2E3338'), mark('cyl', 45, 45, 10, fill='#1E2226')]),
    teil('gehaeuse', 'plastic_housing', 'Gehäuse', 'Gehäuse', 'box',
         x=0, y=70, w=200, d=170, z=20, h=260, r=30, mass=600,
         info='Kunststoffgehäuse aus zwei Schalen. Schrauben sitzen unter der Tropfschale und hinter dem Wassertank, oft mit Sonderköpfen.',
         color='#3C4248', marks=[mark('cyl', 50, 45, 100, fill='#2E3338'), mark('cyl', 90, 150, 14, fill='#5DADE2')]),
    teil('schlaeuche', 'water_pump', 'Silikonschläuche mit Rückschlagventil', 'Schläuche', 'box', material_id='silicone',
         x=118, y=130, w=16, d=40, z=80, h=170, r=3, mass=30, materials=[['gummi', 90], ['messing', 10]],
         info='Verbinden Tank, Pumpe, Erhitzer und Brühkopf. Mit Klemmen gesichert; Klemme aufbiegen und Schlauch abziehen.',
         color='#E9EEF2', opacity=0.8),
    teil('durchlauferhitzer', 'heating_element', 'Durchlauferhitzer', 'Erhitzer', 'box',
         x=40, y=90, w=70, d=70, z=90, h=80, r=6, mass=300,
         materials=[['alu', 70], ['nichrom', 10], ['keramik', 10], ['stahl', 5], ['bimetall', 5]],
         info='Aluminiumblock mit eingegossenem Heizstab, erhitzt das Wasser auf 90 Grad. Zwei Bimetall-Sicherungen schalten bei Überhitzung ab.',
         color='#B8BEC4', marks=[mark('box', 8, 8, 54, 54, 6, fill='#C4672D'), mark('box', 50, 5, 12, 10, 2, fill='#9AA2A6')]),
    teil('pumpe', 'water_pump', 'Vibrationspumpe', 'Pumpe', 'box',
         x=120, y=80, w=55, d=45, z=30, h=45, r=10, mass=250,
         materials=[['kupfer', 30], ['stahl', 40], ['pcabs', 25], ['messing', 5]],
         info='Eine Kupferspule lässt einen Kolben hin und her schwingen und drückt das Wasser durch das Pad. In Gummilagern eingesetzt, lässt sich herausziehen.',
         color='#5F6B75', marks=[mark('box', 6, 6, 43, 33, 8, fill='#B87333')]),
    teil('platine', 'circuit_board', 'Steuerplatine', 'Platine', 'box',
         x=15, y=80, w=18, d=100, z=30, h=120, r=1, mass=60,
         info='Steuert Pumpe, Heizung und Tasten. Steckverbinder abziehen und die Platine zum Elektroschrott geben.',
         color='#2F6B3A', marks=[mark('box', 4, 20, 10, 15, 1, fill='#222'), mark('box', 4, 60, 10, 20, 2, fill='#E0E4E7')]),
    teil('bodenplatte', 'plastic_housing', 'Bodenplatte', 'Bodenplatte', 'box',
         x=10, y=0, w=180, d=250, z=0, h=20, r=20, mass=300, materials=[['pcabs', 90], ['gummi', 10]],
         info='Fuß der Maschine mit Gummifüßen und Kabelführung. Ist mit dem Gehäuse verschraubt.',
         color='#2E3338', marks=raster(10, 10, 2, 2, 16, 16, 144, 214, shape='cyl', fill='#1E2226')),
    teil('wassertank', 'water_tank', 'Wassertank mit Deckel', 'Wassertank', 'box',
         x=15, y=0, w=170, d=65, z=30, h=290, r=14, explode=[0, -100, 0], mass=200,
         info='Durchsichtiger Kunststofftank, wird nach oben herausgehoben. Reines Polypropylen ohne Metall, gehört zum Kunststoff.',
         color='#CFE3EA', opacity=0.6, marks=[mark('box', 5, 5, 160, 55, 10, fill='#3C4248')]),
    teil('tassenrost', 'plastic_housing', 'Tassenrost', 'Tassenrost', 'box', material_id='steel',
         x=40, y=180, w=120, d=65, z=40, h=4, r=6, explode=[0, 110, 0], mass=30, materials=[['stahl', 100]],
         info='Edelstahlgitter, auf dem die Tasse steht. Lose aufgelegt, zum Spülen abnehmen.',
         color='#C9CED2', marks=raster(8, 8, 1, 7, 104, 3, 0, 8, r=1, fill='#7C858C')),
    teil('tropfschale', 'plastic_housing', 'Tropfschale', 'Tropfschale', 'box', material_id='pp',
         x=35, y=175, w=130, d=75, z=20, h=20, r=10, explode=[0, 110, 0], mass=80, materials=[['pp', 100]],
         info='Fängt Tropfen und Restwasser auf. Nach vorne herausziehen und regelmäßig leeren.',
         color='#2E3338'),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=130, y=40, w=70, d=8, z=5, h=8, r=4, explode=[80, 0, 0], mass=80, materials=[['pvc', 90], ['pp', 10]],
         info='Etwa 80 cm PVC-Mantel mit Stecker. Längs aufschlitzen, um die Kupferadern freizulegen.',
         color='#2E3338', marks=[mark('box', 60, 1, 10, 6, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=130, y=42.5, w=70, d=3, z=7.5, h=3, r=1, explode=[80, 0, 15], mass=40,
         info='Drei Kupferadern aus feiner Litze. Kupfer lässt sich fast verlustfrei wiederverwerten.',
         color='#B87333'),
]

explodiere(teile, abstand=25, fest=('bodenplatte',), nach_liste=True)
skaliere_masse(teile, oid='coffee_machine')
schreibe('coffee_machine', teile)
