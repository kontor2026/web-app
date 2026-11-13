"""3D-Modell: television. Erzeugt tools/kategorien/modelle/television.json.

Typischer 55-Zoll-LCD-Fernseher (1230 × 710 mm, 50 mm dick), liegt mit dem Bildschirm nach oben.
Direkte LED-Beleuchtung (Direct-LED): LED-Leisten mit Streulinsen liegen auf dem Rückblech, darüber mit etwa
12 mm Luftabstand die Diffusorplatte und die Folien. Der abgenommene Standfuß und das Netzkabel liegen
zusammengebaut flach unter dem Gerät (z 0..10).

Explosion wie beim Laptop in drei Bereichen:
- hinten (dy negativ): Panel-Modul vom Rückblech aufwärts: LED-Leisten, Diffusorplatte, Folien, LCD, Frontrahmen
- Mitte: Rückwand unten, darüber Netzteil, Hauptplatine mit Prozessor und Lautsprecher
- rechts (dx positiv): Standfuß und Netzkabel
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

GEH = '#2B2F33'
PCB = '#2E6B45'
CHIP = '#22272B'
W, D = 1230, 710

teile = [
    teil('rahmen', 'plastic_housing', 'Frontrahmen', 'Frontrahmen', 'box',
         x=0, y=0, w=W, d=D, z=57, h=3, r=6, mass=600, color=GEH,
         info='Sehr schmaler Rahmen um das Bild, eingeclipst oder mit kleinen Schrauben von hinten befestigt.',
         marks=[mark('box', 9, 9, 1212, 682, 1, '#31373B'), mark('box', 590, 696, 50, 10, 2, '#4A5156')]),
    teil('panel', 'lcd_panel', 'LCD-Panel', 'LCD-Panel', 'box',
         x=8, y=8, w=1214, d=694, z=55, h=2, r=1, mass=3200,
         materials=[['displayglas', 82], ['folien', 14], ['chip', 2], ['kupfer', 2]], color='#31373B',
         info='Zwei Glasscheiben mit Flüssigkristallen, außen Polarisationsfolien. Die Steuerplatine (T-Con) hängt mit '
              'Folienkabeln am Rand. Nur zu zweit und flach tragen: Es bricht sehr leicht.',
         marks=[mark('box', 2, 2, 1210, 690, 1, '#3D464C')] + raster(200, 0, 8, 1, 30, 2, 110, fill='#C5803D')),
    teil('folien', 'led_backlight', 'Optische Folien', 'Folien', 'box', material_id='pet',
         x=10, y=10, w=1210, d=690, z=54, h=1, r=1, mass=300, materials=[['folien', 100]], color='#EEF2F4', opacity=0.75,
         info='Prismen- und Streufolien, lose aufgelegt. Sie lenken das Licht nach vorn und machen das Bild heller.'),
    teil('diffusor', 'led_backlight', 'Diffusorplatte', 'Diffusor', 'box', material_id='ps',
         x=10, y=10, w=1210, d=690, z=52, h=2, r=1, mass=1300, materials=[['ps', 100]], color='#F2F4F5', opacity=0.8,
         info='Milchige Kunststoffplatte, die aus den einzelnen LED-Punkten eine gleichmäßig helle Fläche macht.'),
    teil('led_leisten', 'led_backlight', 'LED-Leisten auf Reflektorfolie', 'LED-Leisten', 'box',
         x=12, y=12, w=1206, d=686, z=38, h=4, r=1, mass=450, material_id='mixed_electronics',
         materials=[['pet', 45], ['alu', 20], ['led', 12], ['kupfer', 10], ['fr4', 8], ['pcabs', 5]], color='#F4F4F0',
         info='Weiße Reflektorfolie mit sechs LED-Leisten, jede LED unter einer kleinen Streulinse. Defekte Leisten sind '
              'der häufigste Grund für ein dunkles Bild und lassen sich einzeln tauschen.',
         marks=[mark('box', 20, 50 + i * 110, 1166, 14, 2, '#E3E6E8') for i in range(6)]
         + [mark('cyl', 40 + j * 98, 52 + i * 110, 10, fill='#F6D86B') for i in range(6) for j in range(12)]),
    teil('rueckblech', 'steel_backplate', 'Rückblech', 'Rückblech', 'box',
         x=4, y=4, w=1222, d=702, z=35, h=3, r=3, mass=3500, color='#9AA2A8',
         info='Großes verzinktes Stahlblech mit Sicken, trägt Beleuchtung und Panel. Mit dem Magneten prüfen: Stahl.',
         marks=raster(300, 150, 2, 2, 12, 12, 600, 400, shape='cyl', fill='#7D858B')),
    teil('soc', 'circuit_board', 'Hauptprozessor (SoC)', 'Prozessor', 'box',
         x=760, y=450, w=24, d=24, z=19.6, h=2, r=0.5, mass=5, materials=[['chip', 85], ['alu', 15]], color=CHIP,
         info='Der Rechner des Smart-TV: Er entschlüsselt Sender, Streams und Apps. Unter einem kleinen Alu-Kühlkörper.',
         marks=[mark('box', 3, 3, 18, 18, 1, '#9AA2A8')]),
    teil('hauptplatine', 'circuit_board', 'Hauptplatine mit Anschlüssen', 'Hauptplatine', 'box',
         x=700, y=400, w=260, d=170, z=18, h=1.6, r=2, mass=220,
         materials=[['fr4', 50], ['kupfer', 18], ['chip', 12], ['stahl', 12], ['lot', 8]], color=PCB,
         info='Mit Tuner, HDMI-, USB- und Antennenbuchsen. Hier sind Konten für Streamingdienste gespeichert: '
              'vorher auf Werkseinstellungen zurücksetzen.',
         marks=raster(240, 10, 1, 4, 16, 18, 0, 26, fill='#B7BCC0') + [mark('box', 20, 120, 40, 30, 1, CHIP)]),
    teil('trafo', 'circuit_board', 'Transformator', 'Trafo', 'box', material_id='mixed_electronics',
         x=420, y=440, w=40, d=36, z=19.6, h=15, r=2, mass=150, materials=[['ferrit', 50], ['kupfer', 40], ['pcabs', 10]],
         color='#3A3F44',
         info='Kupferwicklungen auf einem Ferritkern, trennt die Netzspannung von der übrigen Elektronik.',
         marks=[mark('box', 5, 5, 30, 26, 2, '#C5803D')]),
    teil('netzteil', 'circuit_board', 'Netzteilplatine', 'Netzteil', 'box',
         x=280, y=400, w=300, d=200, z=18, h=1.6, r=2, mass=400, color=PCB,
         info='Versorgt Elektronik und LED-Leisten mit Strom. Die großen Kondensatoren können nach dem Ausstecken noch '
              'geladen sein: nicht an die Beinchen fassen.',
         marks=[mark('box', 200, 20, 80, 30, 2, '#9AA2A8'), mark('box', 10, 150, 40, 40, 2, '#2B2F33'),
                mark('cyl', 40, 50, 30, fill='#2F4F7A'), mark('cyl', 80, 50, 22, fill='#2F4F7A')]),
    teil('lautsprecher_l', 'speaker_driver', 'Lautsprecher links', 'Lautsprecher', 'box',
         x=60, y=600, w=140, d=40, z=18, h=16, r=6, mass=180,
         materials=[['pcabs', 45], ['ferrit', 30], ['stahl', 10], ['kupfer', 10], ['papier', 5]], color='#4A5156',
         info='Kleiner Breitband-Lautsprecher in einer Kunststoffbox, strahlt nach unten ab. Der Magnet zieht Metall an: '
              'von Bankkarten fernhalten.',
         marks=[mark('box', 10, 6, 120, 28, 10, '#2F3438'), mark('cyl', 58, 8, 24, fill='#6E7579')]),
    teil('lautsprecher_r', 'speaker_driver', 'Lautsprecher rechts', 'Lautsprecher', 'box',
         x=1030, y=600, w=140, d=40, z=18, h=16, r=6, mass=180, label=False,
         materials=[['pcabs', 45], ['ferrit', 30], ['stahl', 10], ['kupfer', 10], ['papier', 5]], color='#4A5156',
         info='Zweiter Lautsprecher für Stereo-Ton. Ausgebaut für Bastelprojekte weiter nutzbar.',
         marks=[mark('box', 10, 6, 120, 28, 10, '#2F3438'), mark('cyl', 58, 8, 24, fill='#6E7579')]),
    teil('rueckwand', 'plastic_housing', 'Rückwand', 'Rückwand', 'box',
         x=0, y=0, w=W, d=D, z=10, h=8, r=6, mass=2000, color=GEH,
         info='Große Kunststoffschale mit vielen Schrauben, auch unter der VESA-Halterung. Danach rundum vorsichtig aufclipsen.',
         marks=[mark('box', 465, 205, 300, 300, 6, '#24282C')] + raster(60, 60, 1, 14, 200, 5, 0, 18, fill='#24282C')),
    teil('standfuss', 'plastic_housing', 'Standfuß', 'Standfuß', 'box', material_id='steel',
         x=415, y=200, w=400, d=250, z=0, h=10, r=30, mass=1300, materials=[['stahl', 65], ['pcabs', 35]],
         color='#3A3F44',
         info='Mittiger Standfuß aus Stahlblech mit Kunststoffverkleidung, mit vier Schrauben an der Rückwand. '
              'Abgeschraubt passt der Fernseher an eine Wandhalterung.',
         marks=[mark('box', 150, 20, 100, 80, 8, '#4A5156')]),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=860, y=250, w=250, d=12, z=0, h=8, r=4, mass=150, materials=[['pvc', 90], ['pp', 10]], color=GEH,
         info='Zwei-Meter-Kabel mit PVC-Mantel. Stecker abschneiden und den Mantel längs aufschlitzen.',
         marks=[mark('box', 0, 0, 40, 12, 2, '#4A5156')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=860, y=280, w=250, d=4, z=0, h=4, r=1, mass=60, color='#B87333',
         info='Zwei Kupferadern. Reines Kupfer wird eingeschmolzen und neu verwendet.'),
]

by = {p['id']: p for p in teile}
HINTEN = ['rahmen', 'panel', 'folien', 'diffusor', 'led_leisten', 'rueckblech']
MITTE = ['soc', 'hauptplatine', 'trafo', 'netzteil', 'lautsprecher_l', 'lautsprecher_r', 'rueckwand']
RECHTS = ['standfuss', 'kabel', 'kupferadern']

# Panel-Modul nach hinten, Rückblech liegt auf dem Tisch
h = [by[i] for i in HINTEN]
explodiere(h, abstand=110)
for p in h:
    p['explode'] = [0, -(D + 80), round(p['explode'][2] - 35, 1)]
# Rückwand auf dem Tisch, Platinen und Lautsprecher darüber, Bauteile knapp über den Platinen
m = [by[i] for i in MITTE]
by['rueckwand']['explode'] = [0, 0, -10]
explodiere(m, abstand=110, abstaende={'soc': 35, 'trafo': 35})
# Fuß und Kabel nach rechts
for p in (by[i] for i in RECHTS):
    p['explode'] = [W + 40 - 415, 0, 0]

skaliere_masse(teile, oid='television')
schreibe('television', teile)
