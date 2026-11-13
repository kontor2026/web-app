"""3D-Modell: coffee_machine. Erzeugt tools/kategorien/modelle/coffee_machine.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Kaffeepadmaschine (classifier verlangt eine Pumpe): Wassertank hinten (y 0..65), Gehäuseturm mit Brühkopf oben,
# vorne (y groß) Tropfschale mit Tassenrost. Innen: Vibrationspumpe, Durchlauferhitzer, Silikonschläuche, Steuerplatine.
# Explosion nach Liste: Bodenplatte bleibt, Innenleben darüber, dann Gehäuse, Padhalter und Deckel.
# Wassertank nach hinten (dy < 0), Tropfschale und Rost nach vorne (dy > 0), Kabel nach rechts (dx > 0).

GRAU = '#3C4248'
DUNKEL = '#2E3338'
teile = [
    teil('deckel', 'plastic_housing', 'Brühkammerdeckel mit Hebel', 'Deckel', 'box',
         x=20, y=90, w=160, d=150, z=284, h=46, r=30, mass=130, materials=[['pcabs', 85], ['stahl', 10], ['gummi', 5]],
         info='Klappdeckel, wird mit dem Hebel verriegelt. Das Scharnier hinten hat eine Stahlfeder.',
         color=DUNKEL, marks=[mark('box', 20, 122, 60, 20, 8, fill='#9AA2A6'), mark('cyl', 40, 20, 80, fill=GRAU),
                              mark('box', 20, 2, 120, 6, 3, '#24282C'), mark('cyl', 104, 124, 12, fill='#5DADE2'),
                              mark('cyl', 124, 124, 12, fill='#4A5156'), mark('cyl', 124, 106, 12, fill='#4A5156')]),
    teil('duschsieb', 'water_pump', 'Duschsieb', 'Duschsieb', 'cyl', material_id='steel',
         x=60, y=125, w=80, z=282, h=2, mass=15, materials=[['stahl', 100]], color='#C9CED2',
         info='Edelstahlplatte mit feinen Löchern im Deckel: verteilt das heiße Wasser gleichmäßig über das Pad. '
              'Mit einer Schraube in der Mitte befestigt.',
         marks=raster(14, 14, 7, 7, 3, 3, 8, shape='cyl', fill='#7C858C') + [mark('cyl', 36, 36, 8, fill='#9AA2A6')]),
    teil('dichtung', 'water_pump', 'Brühkammerdichtung', 'Dichtung', 'cyl', material_id='silicone',
         x=48, y=113, w=104, z=279, h=3, mass=6, materials=[['gummi', 100]], color='#E4E1D6',
         info='Silikonring, der die Brühkammer abdichtet. Mit den Fingern herausziehen.',
         marks=[mark('cyl', 8, 8, 88, fill='#3C4248')]),
    teil('padhalter', 'plastic_housing', 'Padhalter', 'Padhalter', 'cyl', material_id='pp',
         x=50, y=115, w=100, z=266, h=13, mass=50, materials=[['pp', 100]],
         info='Schale, in die das Kaffeepad gelegt wird. Reines Polypropylen; benutzte Pads gehören in den Bioabfall '
              'oder Restmüll.',
         color=GRAU, marks=[mark('cyl', 15, 15, 70, fill=DUNKEL), mark('cyl', 45, 45, 10, fill='#1E2226')]),
    teil('gehaeuse', 'plastic_housing', 'Gehäuse (Turm)', 'Gehäuse', 'box',
         x=0, y=70, w=200, d=105, z=20, h=260, r=12, mass=420,
         info='Kunststoffgehäuse aus zwei Schalen. Schrauben sitzen unter der Tropfschale und hinter dem Wassertank, '
              'oft mit Sonderköpfen.',
         color=GRAU, marks=[mark('cyl', 64, 5, 11, fill=DUNKEL), mark('cyl', 94.5, 5, 11, fill='#5DADE2'),
                            mark('cyl', 125, 5, 11, fill=DUNKEL), mark('box', 67, 8, 5, 1.5, 0.5, '#C9CED2'),
                            mark('box', 126, 8, 9, 1.5, 0.5, '#C9CED2')]),
    teil('kopf', 'plastic_housing', 'Gehäuse (Brühkopf)', 'Brühkopf', 'box',
         x=0, y=175, w=200, d=65, z=200, h=80, r=12, mass=150,
         info='Vorderer Teil des Gehäuses über der Tasse. Innen läuft das Kaffeewasser vom Padhalter zum Auslauf.',
         color=GRAU),
    teil('auslauf', 'plastic_housing', 'Kaffeeauslauf', 'Auslauf', 'box', material_id='pp',
         x=80, y=192, w=40, d=22, z=186, h=14, r=8, mass=12, materials=[['pp', 100]], color='#24282C',
         info='Zwei Röhrchen, durch die der Kaffee in die Tassen läuft. Zum Reinigen nach unten abziehen.',
         marks=[mark('cyl', 7, 6, 10, fill='#111'), mark('cyl', 23, 6, 10, fill='#111')]),
    teil('schlaeuche', 'water_pump', 'Silikonschläuche mit Rückschlagventil', 'Schläuche', 'box', material_id='silicone',
         x=118, y=130, w=16, d=40, z=80, h=170, r=3, mass=30, materials=[['gummi', 90], ['messing', 10]],
         info='Verbinden Tank, Pumpe, Erhitzer und Brühkopf. Mit Klemmen gesichert; Klemme aufbiegen und Schlauch abziehen.',
         color='#E9EEF2', opacity=0.8),
    teil('durchlauferhitzer', 'heating_element', 'Durchlauferhitzer', 'Erhitzer', 'box',
         x=40, y=90, w=70, d=70, z=90, h=80, r=6, mass=300,
         materials=[['alu', 70], ['nichrom', 10], ['keramik', 10], ['stahl', 5], ['bimetall', 5]],
         info='Aluminiumblock mit eingegossenem Heizstab, erhitzt das Wasser auf 90 Grad. Zwei Bimetall-Sicherungen schalten bei Überhitzung ab.',
         color='#B8BEC4', marks=[mark('box', 8, 8, 54, 54, 6, fill='#C4672D'), mark('box', 50, 5, 12, 10, 2, fill='#9AA2A6')]),
    teil('thermosicherung', 'heating_element', 'Thermosicherung (Bimetall)', 'Thermoschalter', 'box',
         material_id='mixed_electronics', x=58, y=96, w=16, d=12, z=170, h=6, r=2, mass=5,
         materials=[['bimetall', 50], ['kupfer', 20], ['keramik', 20], ['stahl', 10]], color='#9AA2A6',
         info='Kleiner Schalter mit einer Bimetall-Scheibe: Wird der Erhitzer zu heiß, biegt sie sich und schaltet ab.',
         marks=[mark('cyl', 3, 1, 10, fill='#C9CED2')]),
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
         x=15, y=0, w=170, d=65, z=30, h=280, r=14, explode=[0, -110, 0], mass=170,
         info='Durchsichtiger Kunststofftank, wird nach oben herausgehoben. Unten sitzt ein federbelastetes Ventil, '
              'das beim Abnehmen schließt.',
         color='#CFE3EA', opacity=0.6, marks=[mark('box', 6, 6, 158, 53, 10, fill='#B5CCD5')]),
    teil('tankdeckel', 'water_tank', 'Tankdeckel', 'Tankdeckel', 'box', material_id='pp',
         x=15, y=0, w=170, d=65, z=310, h=10, r=14, explode=[0, -110, 50], mass=30, materials=[['pp', 100]],
         color=DUNKEL, info='Klappdeckel aus Polypropylen, hält Staub vom Wasser fern. Einfach abziehen.',
         marks=[mark('box', 70, 20, 30, 10, 5, GRAU)]),
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

# Das Wassertank-Teil muss in der Liste vor dem Tankdeckel stehen (oberstes Teil zuerst).
i, j = [next(k for k, p in enumerate(teile) if p['id'] == n) for n in ('wassertank', 'tankdeckel')]
teile.insert(i, teile.pop(j))
for p in teile:
    if p['id'] in ('gehaeuse', 'kopf'):
        p['explode'] = [-300, 0, 0]  # Gehäuse zur Seite, damit Pumpe, Erhitzer und Platine frei liegen
i, j = [next(k for k, p in enumerate(teile) if p['id'] == n) for n in ('durchlauferhitzer', 'thermosicherung')]
teile.insert(i, teile.pop(j))
explodiere(teile, abstand=25, fest=('bodenplatte',), nach_liste=True,
           abstaende={'thermosicherung': 15, 'duschsieb': 30, 'dichtung': 25, 'padhalter': 80, 'deckel': 60})
skaliere_masse(teile, oid='coffee_machine')
schreibe('coffee_machine', teile)
