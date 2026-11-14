"""3D-Modell: microwave. Erzeugt tools/kategorien/modelle/microwave.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Mikrowelle 450 × 350 × 260 mm, Front vorne (y = 350). Garraum links (x 15..325), Technikraum rechts (x 335..445)
# mit Hochspannungstrafo, Kondensator, Magnetron und Lüfter; Steuerplatine hinter dem Bedienfeld.
# Explosion nach Liste: Bodenplatte bleibt, darüber Technik und Garraum mit Drehteller, Blechhaube ganz oben.
# Tür und Bedienfeld nach vorne (dy > 0), Kabel nach rechts (dx > 0).
WARNUNG = ' Nie selbst öffnen: Der Hochspannungskondensator kann auch ausgesteckt noch tödliche Spannung speichern; nur der Wertstoffhof bzw. die Elektroschrott-Annahme darf das Gerät zerlegen.'

teile = [
    teil('haube', 'steel_microwave_cavity', 'Gehäusehaube (Stahlblech)', 'Haube', 'box',
         x=0, y=0, w=450, d=325, z=10, h=250, r=4, mass=2000, materials=[['druck', 3], ['stahl', 97]],  # sichtbar: lackiertes Blech
         info='Lackiertes Stahlblech, U-förmig über das Gerät gebogen und hinten verschraubt.' + WARNUNG,
         color='#DADCDD', marks=raster(345, 40, 1, 12, 90, 6, 0, 14, r=2, fill='#B8BEC4')),
    teil('drehteller', 'glass_turntable', 'Drehteller (Glas)', 'Drehteller', 'cyl',
         x=25, y=25, w=290, z=48, h=6, mass=1200,
         info='Hitzebeständiges Glas, einfach herausheben. Gehört nicht in den Altglascontainer, sondern in den Restmüll oder wird weiterverwendet.',
         color='#CFE3EA', opacity=0.65, marks=[mark('cyl', 20, 20, 250, fill='#BBD3DC', zeichnung=True)]),
    teil('rollenring', 'glass_turntable', 'Rollenring', 'Rollenring', 'cyl', material_id='pp',
         x=95, y=95, w=150, z=40, h=8, mass=80, materials=[['pp', 70], ['nylon', 30]],
         info='Kunststoffring mit drei Rollen, auf dem der Drehteller läuft. Reiner Kunststoff, zum Spülen herausnehmen.',
         color='#9AA2A6', wand=12, boden=0,
         marks=[mark('cyl', 15, 15, 120, fill='#7C858C', zeichnung=True)] + [mark('cyl', x, y, 14, fill='#2E3338') for x, y in ((68, 0), (6, 100), (130, 100))]),
    teil('garraum', 'steel_microwave_cavity', 'Garraum (Stahlblech)', 'Garraum', 'box',
         x=15, y=15, w=310, d=305, z=30, h=215, r=2, mass=3000,
         info='Innenraum aus beschichtetem Stahlblech, der die Mikrowellen einschließt. Ist mit dem Gehäuserahmen vernietet und kommt ins Altmetall.',
         color='#C9CED2', marks=[mark('box', 250, 120, 50, 60, 2, fill='#B5A57A')] + raster(30, 30, 6, 3, 6, 6, 12, shape='cyl', fill='#9AA2A6')),
    teil('drehtellermotor', 'glass_turntable', 'Drehtellermotor', 'Tellermotor', 'cyl', material_id='mixed_electronics',
         x=150, y=150, w=40, z=10, h=20, mass=120, materials=[['kupfer', 25], ['stahl', 35], ['pcabs', 30], ['nylon', 10]],
         info='Kleiner Synchronmotor unter dem Garraum, dreht den Teller mit 5 Umdrehungen pro Minute. Enthält eine Kupferspule und ein Kunststoffgetriebe.',
         marks=[mark('cyl', 6, 6, 28, fill='#B87333'), mark('cyl', 16, 16, 8, fill='#9AA2A6')]),
    teil('magnetron', 'magnetron', 'Magnetron', 'Magnetron', 'box',
         x=340, y=70, w=90, d=100, z=120, h=90, r=4, mass=900,
         materials=[['stahl', 35], ['kupfer', 25], ['ferrit', 20], ['keramik', 10], ['alu', 10]],
         info='Erzeugt die Mikrowellen; hat Kühlrippen aus Aluminium und zwei starke Ferritmagnete. Die Keramik innen kann giftiges Berylliumoxid enthalten, darum nie aufbrechen.',
         color='#B8BEC4', marks=raster(5, 5, 1, 12, 80, 4, 0, 8, r=1, fill='#D5DADE') + [mark('cyl', 30, 35, 30, fill='#7C858C')]),
    teil('luefter', 'magnetron', 'Kühllüfter', 'Lüfter', 'box', material_id='mixed_electronics',
         x=345, y=25, w=95, d=30, z=130, h=90, r=3, mass=150, materials=[['pp', 40], ['kupfer', 25], ['stahl', 35]],
         info='Bläst Luft über das Magnetron und durch den Garraum. Der Motor hat eine Kupferwicklung.',
         color='#5F6B75', marks=[mark('box', 30, 2, 35, 26, 4, fill='#B87333')]),
    teil('kondensator', 'magnetron', 'Hochspannungskondensator', 'HV-Kondensator', 'box',
         x=345, y=15, w=50, d=40, z=10, h=60, r=14, mass=250, materials=[['alu', 45], ['pp', 35], ['stahl', 10], ['kupfer', 10]],
         info='Speichert über 2000 Volt für das Magnetron und kann auch Tage nach dem Ausstecken noch tödlich sein. Nur die Elektroschrott-Annahme darf ihn ausbauen und entladen.',
         color='#9AA2A6', marks=[mark('box', 8, 12, 10, 16, 2, fill='#D5DADE'), mark('box', 32, 12, 10, 16, 2, fill='#D5DADE')]),
    teil('trafo', 'magnetron', 'Hochspannungstransformator', 'HV-Trafo', 'box', material_id='mixed_electronics',
         x=345, y=190, w=90, d=110, z=10, h=100, r=2, mass=3500, materials=[['stahl', 62], ['kupfer', 33], ['pcabs', 5]],
         info='Schwerstes Bauteil: Eisenkern mit dicken Kupferwicklungen, wandelt 230 Volt in etwa 2000 Volt um. Wertvoll für das Metallrecycling.',
         color='#5A6670', marks=[mark('box', 10, 20, 70, 70, 6, fill='#B87333'), mark('box', 25, 35, 40, 40, 2, fill='#5A6670')]),
    teil('platine', 'circuit_board', 'Steuerplatine', 'Platine', 'box',
         x=340, y=305, w=105, d=17, z=40, h=200, r=1, mass=150,
         info='Steuert Zeit, Leistung und Anzeige über Relais. Steckverbinder abziehen; die Platine kommt zum Elektroschrott.',
         color='#2F6B3A', marks=[mark('box', 10, 4, 25, 9, 1, fill='#222'), mark('box', 50, 4, 40, 9, 1, fill='#E0E4E7')]),
    teil('bodenplatte', 'steel_microwave_cavity', 'Bodenplatte', 'Bodenplatte', 'box',
         x=0, y=0, w=450, d=325, z=0, h=10, r=2, mass=800, materials=[['stahl', 95], ['gummi', 5]],
         info='Verzinktes Stahlblech mit vier Gummifüßen, trägt Trafo und Garraum. Kommt ins Altmetall.',
         color='#7C858C', marks=raster(15, 15, 2, 2, 20, 20, 400, 275, shape='cyl', fill='#2E3338')),
    teil('tuer', 'plastic_front_panel', 'Tür mit Sichtfenster', 'Tür', 'box', material_id='abs',
         x=0, y=325, w=330, d=25, z=10, h=250, r=3, explode=[0, 120, 0], mass=1800,
         materials=[['pcabs', 35], ['glas', 30], ['stahl', 30], ['gummi', 5]],
         info='Kunststoffrahmen mit Glasscheibe und gelochtem Metallgitter, das die Mikrowellen abschirmt. Die Scharniere sind mit dem Gehäuse verschraubt.',
         color='#2E3338', marks=[mark('box', 10, 5, 310, 15, 2, fill='#4A545C')]),
    teil('bedienfeld', 'plastic_front_panel', 'Bedienfeld', 'Bedienfeld', 'box',
         x=330, y=325, w=120, d=25, z=10, h=250, r=3, explode=[0, 120, 0], mass=300,
         info='Kunststoffblende mit Anzeige, Tasten und Drehknopf. Ist eingeclipst: unten kräftig herausziehen.',
         color='#3C4248', marks=[mark('box', 10, 5, 100, 15, 2, fill='#2E3338')]),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=370, y=0, w=80, d=8, z=20, h=8, r=4, explode=[80, 0, 0], form='liegend_x', mass=150, materials=[['pvc', 90], ['pp', 10]],
         info='Etwa 1 m dickes PVC-Kabel mit Schutzkontaktstecker. Längs aufschlitzen, um die Kupferadern freizulegen.',
         color='#2E3338', marks=[mark('box', 70, 1, 10, 6, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=370, y=2.5, w=80, d=3, z=22.5, h=3, r=1, explode=[80, 0, 15], form='liegend_x', mass=80,
         info='Drei Kupferadern für bis zu 1200 Watt. Kupfer lässt sich fast verlustfrei wiederverwerten.',
         color='#B87333'),
]

explodiere(teile, abstand=30, fest=('bodenplatte',), nach_liste=True)
skaliere_masse(teile, oid='microwave')
for p in teile:  # gerundete Formen (form): marks nur in der Zeichnung, oben flach würden sie schweben
    if p.get('form'):
        p['marks'] = [dict(m, zeichnung=True) for m in p.get('marks') or []]
schreibe('microwave', teile)
