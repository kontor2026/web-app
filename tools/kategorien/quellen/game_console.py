"""3D-Modell: game_console. Erzeugt tools/kategorien/modelle/game_console.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Stationäre Spielkonsole, liegend (350 × 260 × 100 mm). Links die Hauptplatine mit APU (Prozessor + Grafik),
# Grafikspeicher und Kühlkörper mit Radiallüfter, darunter die SSD; rechts das eingebaute Netzteil.
# Explosion: Unterschale bleibt liegen, das Innenleben schwebt schichtweise darüber, die Oberschale ganz oben
# (nach_liste, weil sie zusammengebaut schon bei z 50 beginnt).
GEH = '#2B2F33'
PCB = '#2E6B45'
CHIP = '#22272B'

teile = [
    teil('oberschale', 'plastic_housing', 'Oberschale', 'Oberschale', 'box',
         x=0, y=0, w=350, d=260, z=50, h=50, r=10, mass=650, color=GEH,
         info='Obere Gehäusehälfte aus Kunststoff. Garantiesiegel und Schrauben sitzen unter den Gummifüßen, dann rundum aufclipsen.',
         marks=raster(250, 30, 6, 1, 6, 200, 14, fill='#1E2226')
         + raster(20, 30, 6, 1, 4, 120, 10, fill='#1E2226')
         + [mark('box', 150, 238, 50, 8, 3, '#4A5156'), mark('cyl', 316, 236, 10, fill='#3D4449'),
            mark('cyl', 319, 239, 4, fill='#EDEFF1')]),
    teil('leuchtleiste', 'plastic_housing', 'Lichtleiste mit Lichtleiter', 'Lichtleiste', 'box',
         x=40, y=260, w=270, d=1.2, z=48, h=4, r=0.5, mass=6, sortBias=120, material_id='pc',
         materials=[['pcabs', 100]], color='#7FB8F0', opacity=0.9,
         info='Durchsichtiger Kunststoffstreifen, der das Licht einer LED auf der Platine nach vorne leitet. '
              'Zeigt an, ob die Konsole an ist.'),
    teil('tasten', 'plastic_housing', 'Ein- und Auswurftaste', 'Tasten', 'box',
         x=290, y=260, w=40, d=1.2, z=56, h=6, r=1, mass=4, sortBias=120,
         info='Zwei flache Kunststofftasten drücken auf kleine Schalter der Platine. Einfach herausklipsen.',
         color='#3D4449'),
    teil('luefter', 'cooling_fan', 'Radiallüfter', 'Lüfter', 'cyl',
         x=60, y=80, w=100, z=70, h=25, mass=180,
         materials=[['pcabs', 55], ['kupfer', 20], ['ferrit', 10], ['stahl', 10], ['chip', 5]], color='#3A3F44',
         info='Saugt Luft an und bläst sie durch den Kühlkörper nach hinten hinaus. Stecker abziehen, drei Schrauben lösen. '
              'Staub mit einem Pinsel entfernen.',
         marks=[mark('cyl', 30, 30, 40, fill='#1E2226'), mark('cyl', 44, 44, 12, fill='#9AA2A8')]),
    teil('kuehlkoerper', 'cpu_cooler', 'Kühlkörper (Aluminiumlamellen)', 'Kühlkörper', 'box',
         x=50, y=70, w=120, d=120, z=40, h=28, r=2, mass=420, color='#C9CED2',
         info='Dichte Aluminiumlamellen nehmen die Wärme der APU auf. Nach dem Abschrauben leicht verdrehen, um die Wärmeleitpaste zu lösen.',
         marks=raster(4, 4, 1, 22, 112, 2, 0, 5.2, fill='#B5BBC0')),
    teil('heatpipes', 'cpu_cooler', 'Kupferplatte mit Heatpipes', 'Heatpipes', 'box', material_id='copper',
         x=70, y=100, w=80, d=60, z=34, h=4, r=2, mass=160, materials=[['kupfer', 95], ['elektrolyt', 5]], color='#B87333',
         info='Kupferplatte und Rohre mit etwas Flüssigkeit darin, die die Wärme sehr schnell zu den Lamellen leiten. Wertvolles Kupfer.',
         marks=raster(8, 6, 4, 1, 8, 48, 18, r=4, fill='#C98A4B')),
    teil('abschirmblech', 'plastic_housing', 'Abschirmblech', 'Abschirmblech', 'box', material_id='steel',
         x=12, y=17, w=211, d=226, z=33.6, h=1, r=3, mass=300, explode=[-300, 0, 60], materials=[['stahl', 100]], color='#9AA2A8',
         info='Stahlblech über der Platine gegen Funkstörungen. In der Mitte eine Öffnung für den Kühler. Mit dem Magneten prüfen: Stahl.',
         marks=[mark('box', 56, 81, 84, 64, 2, '#7D858B')]),
    teil('speicher', 'circuit_board', 'Grafikspeicher (GDDR)', 'Grafikspeicher', 'box',
         x=140, y=100, w=16, d=60, z=31.6, h=1.2, r=0.5, mass=12, materials=[['chip', 100]], color=CHIP,
         info='Acht schnelle Speicherchips rund um die APU, hier gebündelt gezeigt. Gemeinsamer Speicher für Spiele und Grafik.',
         marks=raster(1, 2, 1, 4, 14, 12, 0, 15, fill='#33393D')),
    teil('apu', 'circuit_board', 'APU (Prozessor und Grafik)', 'APU', 'box',
         x=90, y=110, w=40, d=40, z=31.6, h=2.5, r=1, mass=25, materials=[['chip', 60], ['fr4', 25], ['kupfer', 15]],
         color='#5E656A',
         info='Ein großer Chip mit Prozessor und Grafikeinheit. Er wird sehr heiß und braucht deshalb den Kühler darüber.',
         marks=[mark('box', 8, 8, 24, 24, 1, '#B5BBC0')]),
    teil('cmos', 'circuit_board', 'Knopfzelle für die Uhr (CR2032)', 'Knopfzelle', 'cyl',
         material_id='li_ion', x=180, y=40, w=20, z=31.6, h=3.2, mass=3, materials=[['knopfzelle', 100]],
         color='#C9CED2', marks=[mark('cyl', 3, 3, 14, fill='#B5BBC0')],
         info='Hält Uhrzeit und Einstellungen, wenn der Stecker gezogen ist. Herausdrücken und getrennt in die Batteriesammlung.'),
    teil('wlan', 'circuit_board', 'WLAN- und Bluetooth-Modul', 'WLAN-Modul', 'box',
         x=180, y=200, w=30, d=22, z=31.6, h=2, r=1, mass=6, materials=[['fr4', 40], ['chip', 30], ['stahl', 20], ['kupfer', 10]],
         color='#9AA2A8', marks=[mark('cyl', 22, 3, 5, fill='#D4A73A'), mark('cyl', 22, 13, 5, fill='#D4A73A')],
         info='Funkmodul für Controller und Internet. Zwei dünne Antennenkabel sind mit kleinen Steckern aufgeklipst.'),
    teil('usb', 'circuit_board', 'USB-Buchsen vorne', 'USB-Buchsen', 'box',
         x=30, y=246, w=40, d=15, z=31.6, h=7, r=0.5, mass=8, sortBias=120,
         materials=[['stahl', 60], ['pcabs', 25], ['kupfer', 15]], color='#1E2226',
         marks=[mark('box', 2, 2, 16, 11, 0.5, '#B7BCC0'), mark('box', 22, 2, 16, 11, 0.5, '#B7BCC0')],
         info='Zwei USB-Buchsen aus Stahlblech, auf die Hauptplatine gelötet. Hier werden Controller geladen.'),
    teil('mainboard', 'circuit_board', 'Hauptplatine', 'Hauptplatine', 'box',
         x=10, y=15, w=215, d=230, z=30, h=1.6, r=2, mass=380,
         materials=[['fr4', 50], ['kupfer', 20], ['chip', 15], ['stahl', 8], ['lot', 7]], color=PCB,
         info='Mit HDMI-, USB- und Netzwerkbuchsen an der Rückseite. Alle Flachbandkabel abziehen, dann ausschrauben.',
         marks=[mark('box', 4, 2, 20, 10, 1, '#B7BCC0'), mark('box', 30, 2, 14, 10, 1, '#B7BCC0'),
                mark('box', 50, 2, 14, 10, 1, '#B7BCC0'), mark('box', 150, 180, 30, 30, 1, CHIP)]),
    teil('ssd', 'hard_drive', 'SSD (2,5 Zoll)', 'SSD', 'box',
         x=20, y=165, w=100, d=70, z=10, h=7, r=2, mass=60, explode=[-60, 200, 0],
         materials=[['alu', 45], ['fr4', 25], ['chip', 25], ['kupfer', 5]], color='#5E656A',
         info='Speichert Spiele und Spielstände. Einschub herausziehen; Konto vorher abmelden und Daten löschen.',
         marks=[mark('box', 10, 10, 80, 50, 2, '#E8E8E0')]),
    teil('trafo', 'power_supply_unit', 'Transformator', 'Trafo', 'box',
         x=250, y=40, w=40, d=40, z=9.6, h=30, r=2, mass=160, materials=[['ferrit', 50], ['kupfer', 40], ['pcabs', 10]],
         color='#3A3F44',
         info='Kupferwicklungen auf einem Ferritkern. Er trennt die Netzspannung vom Rest der Konsole.',
         marks=[mark('box', 5, 5, 30, 30, 2, '#C5803D')]),
    teil('netzbuchse', 'power_supply_unit', 'Netzbuchse', 'Netzbuchse', 'box',
         x=300, y=0, w=24, d=14, z=9.6, h=16, r=2, mass=12, materials=[['pcabs', 60], ['messing', 30], ['kupfer', 10]],
         color='#1E2226', marks=[mark('cyl', 5, 3, 5, fill='#B7BCC0'), mark('cyl', 14, 3, 5, fill='#B7BCC0')],
         info='Hier wird das Netzkabel eingesteckt. Die Messingkontakte führen 230 Volt: nur ausgesteckt öffnen.'),
    teil('elko', 'power_supply_unit', 'Elektrolytkondensator', 'Elko', 'cyl',
         x=300, y=55, w=25, z=9.6, h=35, mass=30,
         materials=[['alu', 50], ['papier', 20], ['elektrolyt', 15], ['pcabs', 10], ['gummi', 5]], color='#2F4F7A',
         info='Speichert Energie und glättet die Spannung. Kann noch nach dem Ausstecken geladen sein: nicht an die Beinchen fassen.',
         marks=[mark('cyl', 4, 4, 17, fill='#B9C0C6')]),
    teil('netzteil', 'power_supply_unit', 'Netzteilplatine mit Kühlblechen', 'Netzteil', 'box',
         x=230, y=15, w=110, d=230, z=8, h=1.6, r=2, mass=420,
         materials=[['fr4', 35], ['alu', 25], ['kupfer', 20], ['ferrit', 10], ['chip', 10]], color=PCB,
         info='Eingebautes Netzteil: macht aus 230 Volt die Niederspannung. Nur als Ganzes ausbauen, nicht weiter öffnen.',
         marks=[mark('box', 10, 120, 90, 20, 2, '#C9CED2'), mark('box', 10, 160, 90, 20, 2, '#C9CED2'),
                mark('box', 80, 205, 24, 18, 2, '#1E2226')]),
    teil('unterschale', 'plastic_housing', 'Unterschale mit Laufwerksschacht', 'Unterschale', 'box',
         x=0, y=0, w=350, d=260, z=0, h=50, r=10, mass=700, color=GEH, wand=3, boden=2.5,
         info='Untere Gehäusehälfte aus Kunststoff mit Gummifüßen. Trägt Platine und Netzteil; leer ab in die Elektro-Sammlung.',
         marks=[dict(m, zeichnung=True) for m in raster(20, 20, 2, 2, 20, 20, 290, 200, shape='cyl', fill='#1E2226')]),
]

explodiere(teile, abstand=35, nach_liste=True, abstaende={'apu': 15, 'speicher': 15, 'trafo': 15, 'elko': 15, 'cmos': 15, 'wlan': 15, 'usb': 15,
                                                        'netzbuchse': 15, 'oberschale': 150},
           gruppen=[['oberschale', 'leuchtleiste', 'tasten']])
skaliere_masse(teile, oid='game_console')
schreibe('game_console', teile)
