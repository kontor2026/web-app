"""3D-Modell: monitor. Erzeugt tools/kategorien/modelle/monitor.json.

Typischer 24-Zoll-LCD-Monitor (540 × 320 mm, Gehäuse 37 mm dick), liegt mit dem Bildschirm nach oben.
Kantenbeleuchtung (Edge-LED): eine LED-Leiste an der unteren Kante leuchtet in eine Lichtleiterplatte.
Der abgenommene Standfuß und das Netzkabel liegen zusammengebaut flach unter dem Gerät (z 0..8).

Explosion wie beim Laptop in drei Bereichen:
- hinten (dy negativ): Panel-Modul vom Metallrahmen aufwärts: Rückblech, Lichtleiter + LED-Leiste, Folien, LCD, Frontrahmen
- Mitte: Rückwand unten, darüber Netzteil- und Hauptplatine mit ihren Bauteilen
- rechts (dx positiv): Standfuß und Netzkabel
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

GEH = '#2B2F33'
PCB = '#2E6B45'
CHIP = '#22272B'
W, D = 540, 320

teile = [
    teil('rahmen', 'plastic_housing', 'Frontrahmen', 'Frontrahmen', 'box',
         x=0, y=0, w=W, d=D, z=40.5, h=4.5, r=6, mass=300, color=GEH,
         info='Schmaler Kunststoffrahmen um das Bild, nur eingeclipst. Mit einem Plektrum rundum aufhebeln.',
         marks=[mark('box', 7, 7, 526, 296, 1, '#31373B'), mark('box', 255, 308, 30, 6, 1, '#4A5156')]),
    teil('panel', 'lcd_panel', 'LCD-Panel', 'LCD-Panel', 'box',
         x=6, y=10, w=528, d=304, z=38, h=2.5, r=1, mass=650,
         materials=[['displayglas', 80], ['folien', 15], ['chip', 3], ['kupfer', 2]], color='#31373B',
         info='Zwei dünne Glasscheiben mit Flüssigkristallen dazwischen und Polarisationsfolien außen. '
              'Flach anfassen: Es bricht leicht, die Kanten sind scharf.',
         marks=[mark('box', 1.5, 1.5, 525, 301, 1, '#3D464C')]),
    teil('tcon', 'circuit_board', 'Panel-Steuerplatine (T-Con)', 'T-Con', 'box',
         x=150, y=0, w=240, d=10, z=38, h=1.6, r=1, mass=40, color=PCB,
         info='Verteilt die Bilddaten über dünne Folienleiter an die Treiberchips am Glasrand. Mit Flachbandkabel gesteckt.',
         marks=raster(10, 2, 8, 1, 14, 6, 28, fill=CHIP)),
    teil('folien', 'led_backlight', 'Diffusor- und Prismenfolien', 'Folien', 'box', material_id='pet',
         x=8, y=12, w=524, d=298, z=37.3, h=0.7, r=1, mass=150, materials=[['folien', 100]], color='#EEF2F4', opacity=0.75,
         info='Drei bis vier lose gestapelte Kunststofffolien. Sie verteilen das Licht gleichmäßig und lenken es nach vorn.'),
    teil('lichtleiter', 'led_backlight', 'Lichtleiterplatte mit Reflektorfolie', 'Lichtleiter', 'box', material_id='ps',
         x=8, y=12, w=524, d=288, z=34.3, h=3, r=1, mass=480, materials=[['ps', 90], ['folien', 10]], color='#DCE8EE', opacity=0.7,
         info='Klare Kunststoffplatte mit aufgedrucktem Punktmuster: Sie leitet das Licht der LED-Leiste über die '
              'ganze Fläche. Darunter liegt eine weiße Reflektorfolie.',
         marks=raster(20, 16, 12, 6, 6, 6, 43, 44, shape='cyl', fill='#C9D9E0')),
    teil('led_leiste', 'led_backlight', 'LED-Leiste', 'LED-Leiste', 'box',
         x=8, y=302, w=524, d=8, z=34.3, h=3, r=0.5, mass=40, material_id='mixed_electronics',
         materials=[['alu', 55], ['led', 20], ['kupfer', 15], ['fr4', 10]], color='#ECECE6',
         info='Schmale Aluminiumleiste mit vielen kleinen weißen LEDs an der unteren Kante. Sie ist das Licht des Monitors.',
         marks=raster(4, 2.5, 40, 1, 4, 3, 13, fill='#F6D86B')),
    teil('rueckblech', 'steel_backplate', 'Metallrahmen (Rückblech)', 'Rückblech', 'box',
         x=4, y=4, w=532, d=312, z=32, h=2.3, r=3, mass=700, color='#9AA2A8',
         info='Verzinktes Stahlblech, trägt das ganze Panel-Modul. Erst Platinen abschrauben, dann mit dem Magneten prüfen: Stahl.',
         marks=raster(90, 60, 2, 2, 8, 8, 352, 200, shape='cyl', fill='#7D858B')),
    teil('scaler', 'circuit_board', 'Bildprozessor (Scaler)', 'Bildprozessor', 'box',
         x=345, y=225, w=16, d=16, z=15.6, h=1.4, r=0.5, mass=3, materials=[['chip', 100]], color=CHIP,
         info='Rechnet das Bildsignal vom Computer auf die Auflösung des Panels um und steuert das Bildschirmmenü.'),
    teil('hauptplatine', 'circuit_board', 'Hauptplatine mit Anschlüssen', 'Hauptplatine', 'box',
         x=320, y=200, w=150, d=95, z=14, h=1.6, r=2, mass=90,
         materials=[['fr4', 50], ['kupfer', 18], ['chip', 12], ['stahl', 12], ['lot', 8]], color=PCB,
         info='Mit HDMI- und DisplayPort-Buchsen am Rand. Mit vier Schrauben am Rückblech, Kabel vorsichtig abziehen.',
         marks=[mark('box', 4, 80, 18, 12, 1, '#B7BCC0'), mark('box', 28, 80, 22, 12, 1, '#B7BCC0'),
                mark('box', 100, 10, 30, 14, 1, CHIP)]),
    teil('trafo', 'circuit_board', 'Transformator', 'Trafo', 'box', material_id='mixed_electronics',
         x=180, y=230, w=30, d=26, z=15.6, h=14, r=2, mass=55, materials=[['ferrit', 50], ['kupfer', 40], ['pcabs', 10]],
         color='#3A3F44',
         info='Kupferwicklungen auf einem Ferritkern. Er trennt die gefährliche Netzspannung vom Rest des Monitors.',
         marks=[mark('box', 4, 4, 22, 18, 2, '#C5803D')]),
    teil('elko', 'circuit_board', 'Elektrolytkondensator', 'Elko', 'cyl', material_id='mixed_electronics',
         x=130, y=240, w=18, z=15.6, h=15, mass=20,
         materials=[['alu', 50], ['papier', 20], ['elektrolyt', 15], ['pcabs', 10], ['gummi', 5]], color='#2F4F7A',
         info='Speichert Energie und glättet die Spannung. Kann noch Minuten nach dem Ausstecken geladen sein: '
              'nicht an die Beinchen fassen.',
         marks=[mark('cyl', 3, 3, 12, fill='#B9C0C6')]),
    teil('netzteil', 'circuit_board', 'Netzteilplatine', 'Netzteil', 'box',
         x=110, y=200, w=180, d=105, z=14, h=1.6, r=2, mass=110, color=PCB,
         info='Macht aus 230 Volt die Niederspannung für Elektronik und LEDs. Enthält Kupfer, Ferrit und Elektronikbauteile.',
         marks=[mark('box', 4, 70, 20, 30, 2, '#2B2F33'), mark('box', 110, 10, 30, 22, 1, '#9AA2A8')]),
    teil('rueckwand', 'plastic_housing', 'Rückwand', 'Rückwand', 'box',
         x=0, y=0, w=W, d=D, z=8, h=6, r=6, mass=650, color=GEH,
         info='Große Kunststoffschale. Schrauben sitzen unter der Standfuß-Halterung (VESA), danach rundum aufclipsen.',
         marks=[mark('box', 220, 110, 100, 100, 4, '#24282C')] + raster(40, 30, 1, 10, 120, 4, 0, 10, fill='#24282C')),
    teil('standfuss', 'steel_stand', 'Standfuß mit Hals', 'Standfuß', 'box',
         x=40, y=60, w=240, d=200, z=0, h=8, r=40, mass=850, materials=[['stahl', 70], ['pcabs', 30]], color='#3A3F44',
         info='Stahlplatte mit Kunststoffhülle und Hals. Abgenommen über eine Taste oder vier VESA-Schrauben; '
              'zu Hause weiter nutzbar oder ins Altmetall.',
         marks=[mark('box', 80, 10, 80, 120, 10, '#4A5156')]),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=320, y=110, w=180, d=10, z=0, h=8, r=4, form='liegend_x', mass=120, materials=[['pvc', 90], ['pp', 10]], color=GEH,
         info='1,5 m Kaltgerätekabel mit PVC-Mantel. Stecker abschneiden und längs aufschlitzen.',
         marks=[mark('box', 0, 0, 30, 10, 2, '#4A5156'), mark('box', 150, 0, 30, 10, 2, '#4A5156')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=320, y=135, w=180, d=4, z=0, h=4, r=1, form='liegend_x', mass=60, color='#B87333',
         info='Drei Kupferadern (Phase, Neutralleiter, Schutzleiter). Reines Kupfer lohnt sich beim Schrotthändler.'),
]

by = {p['id']: p for p in teile}
HINTEN = ['rahmen', 'panel', 'tcon', 'folien', 'lichtleiter', 'led_leiste', 'rueckblech']
MITTE = ['scaler', 'hauptplatine', 'trafo', 'elko', 'netzteil', 'rueckwand']
RECHTS = ['standfuss', 'kabel', 'kupferadern']

# Panel-Modul nach hinten, unterstes Teil (Rückblech) liegt auf dem Tisch
h = [by[i] for i in HINTEN]
explodiere(h, abstand=60, gruppen=[['panel', 'tcon'], ['lichtleiter', 'led_leiste']])
for p in h:
    p['explode'] = [0, -(D + 50), round(p['explode'][2] - 32, 1)]
# Rückwand bleibt liegen (unter ihr liegt nur der Fuß, der zur Seite geht), Platinen schweben darüber
m = [by[i] for i in MITTE]
by['rueckwand']['explode'] = [0, 0, -8]
explodiere(m, abstand=60, abstaende={'scaler': 20, 'trafo': 20, 'elko': 20})
# Fuß und Kabel nach rechts
for p in (by[i] for i in RECHTS):
    p['explode'] = [W + 20, 0, 0]

skaliere_masse(teile, oid='monitor')
for p in teile:  # gerundete Formen (form): marks nur in der Zeichnung, oben flach würden sie schweben
    if p.get('form'):
        p['marks'] = [dict(m, zeichnung=True) for m in p.get('marks') or []]
schreibe('monitor', teile)
