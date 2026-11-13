"""3D-Modell: smartphone. Erzeugt tools/kategorien/modelle/smartphone.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, schreibe  # noqa: E402

teile = [
    teil('deckglas', 'smartphone_display', 'Deckglas', 'Deckglas', 'box',
         material_id='special_glass', x=0, y=0, w=76, d=151, h=0.6, z=7.9, r=10, explode=[0, 0, 266.8], color='#C9DEDF', opacity=0.6, mass=15, materials=[['glas', 100]], info='Chemisch gehärtetes Glas. Schützt das Display und ist zugleich die Touch-Oberfläche.', marks=[{'shape': 'box', 'x': 30, 'y': 4, 'w': 16, 'd': 1.6, 'r': 0.8}]),
    teil('display', 'smartphone_display', 'Display-Einheit (LCD)', 'Display', 'box',
         material_id='special_glass', x=0.5, y=0.5, w=75, d=150, h=0.8, z=7.1, r=9.5, explode=[0, 0, 216.20000000000002], color='#31373B', mass=28, materials=[['displayglas', 45], ['folien', 35], ['led', 10], ['kupfer', 10]], info='Mehrere verklebte Schichten: Glas mit leitfähiger Indium-Schicht, Folien, LED-Hintergrundlicht.', marks=[{'shape': 'box', 'x': 3, 'y': 3, 'w': 69, 'd': 144, 'r': 7, 'fill': '#3D464C'}, {'shape': 'box', 'x': 19, 'y': 3, 'w': 37, 'd': 7, 'r': 3, 'fill': '#31373B'}]),
    teil('kamera', 'circuit_board', 'Kameramodul', 'Kamera', 'box',
         material_id='mixed_electronics', x=6, y=6, w=24, d=38, h=4.5, z=3, r=4, explode=[0, 0, 119.60000000000001], color='#5E656A', mass=9, materials=[['chip', 35], ['alu', 30], ['glas', 20], ['ndfeb', 15]], info='Zwei Kameras mit Bildsensor, Linsen und kleinem Magnetantrieb für den Autofokus.', marks=[{'shape': 'cyl', 'x': 5, 'y': 5, 'w': 14, 'fill': '#262B2F'}, {'shape': 'cyl', 'x': 5, 'y': 21, 'w': 14, 'fill': '#262B2F'}]),
    teil('soc', 'circuit_board', 'Prozessor (SoC)', 'Prozessor', 'box',
         material_id='pcb', x=40, y=14, w=14, d=14, h=1, z=4.2, r=1, explode=[0, 0, 151.79999999999998], color='#3F4547', mass=1.2, materials=[['chip', 100]], info='Rechenkern, Grafik und Arbeitsspeicher in einem Gehäuse. Feinste Golddrähte verbinden den Chip.'),
    teil('speicher', 'circuit_board', 'Speicherchip (NAND)', 'Speicher', 'box',
         material_id='pcb', x=56, y=14, w=11, d=16, h=1, z=4.2, r=1, explode=[0, 0, 151.79999999999998], color='#3F4547', mass=0.8, materials=[['chip', 100]], info='Speichert Fotos und Apps. Daten vor dem Abgeben unbedingt löschen.'),
    teil('platine', 'circuit_board', 'Hauptplatine', 'Platine', 'box',
         material_id='pcb', x=32, y=6, w=38, d=50, h=1.2, z=3, r=3, explode=[0, 0, 119.60000000000001], mass=12, materials=[['fr4', 45], ['kupfer', 25], ['chip', 20], ['lot', 10]], info='Zwei gestapelte Leiterplatten mit Funkchips und Stromversorgung. Hier steckt das meiste Gold.'),
    teil('akku', 'li_ion_battery', 'Lithium-Ionen-Akku', 'Akku', 'box',
         material_id='li_ion', x=22, y=60, w=46, d=64, h=4.2, z=3, r=3, explode=[0, 0, 119.60000000000001], mass=48, materials=[['lco', 38], ['graphit', 20], ['elektrolyt', 15], ['kupfer', 10], ['alu', 10], ['folien', 7]], info='Etwa 3.100 mAh. Mit Klebestreifen befestigt. Aufgebläht oder beschädigt gehört er sofort in die Sammlung.', marks=[{'shape': 'box', 'x': 4, 'y': 4, 'w': 38, 'd': 56, 'r': 2}]),
    teil('taptic', 'circuit_board', 'Vibrationsmotor', 'Vibration', 'box',
         material_id='mixed_electronics', x=8, y=128, w=30, d=13, h=3.6, z=3, r=2, explode=[0, 0, 119.60000000000001], color='#9BA3A8', mass=4, materials=[['stahl', 50], ['ndfeb', 30], ['kupfer', 20]], info='Ein Magnet schwingt in einer Kupferspule hin und her und erzeugt das Klick-Gefühl.'),
    teil('lautsprecher', 'circuit_board', 'Lautsprecher', 'Lautsprecher', 'box',
         material_id='mixed_electronics', x=44, y=131, w=22, d=12, h=3, z=3, r=2, explode=[0, 0, 119.60000000000001], color='#6E7579', mass=3, materials=[['pcabs', 40], ['ndfeb', 40], ['kupfer', 20]], info='Kleiner Neodym-Magnet mit Schwingspule. Lässt sich ausgebaut weiterverwenden.'),
    teil('spule', 'smartphone_back_cover', 'Ladespule (kabellos)', 'Ladespule', 'cyl',
         material_id='mixed_electronics', x=16, y=56, w=44, h=0.5, z=1.5, explode=[0, 0, 69], color='#C98F62', mass=3, materials=[['kupfer', 70], ['ferrit', 30]], info='Flache Kupferspule für kabelloses Laden. Darunter eine Ferritfolie, die das Feld bündelt.', marks=[{'shape': 'cyl', 'x': 8, 'y': 8, 'w': 28}, {'shape': 'cyl', 'x': 15, 'y': 15, 'w': 14}]),
    teil('sim', 'sim_tray', 'SIM-Kartenschlitten', 'SIM-Schlitten', 'box',
         material_id='steel', x=71, y=40, w=4, d=24, z=3, h=1, r=1, explode=[45, 0, 0], mass=1, materials=[['stahl', 100]], info='Hält die SIM-Karte. Mit einer Büroklammer in das kleine Loch neben dem Schlitten drücken, dann springt er heraus.'),
    teil('rahmen', 'aluminium_frame', 'Gehäuserahmen', 'Rahmen', 'box',
         material_id='aluminium', x=0, y=0, w=76, d=151, h=1.5, z=0.3, r=10, explode=[0, 0, 34.5], mass=45, materials=[['alu', 100]], info='Aus einem Aluminiumblock gefräst. Trägt alle Bauteile und dient als Antenne.', marks=[{'shape': 'box', 'x': 2.5, 'y': 2.5, 'w': 71, 'd': 146, 'r': 8}]),
    teil('rueckglas', 'smartphone_back_cover', 'Rückglas', 'Rückglas', 'box',
         material_id='special_glass', x=0, y=0, w=76, d=151, h=0.8, z=0, r=10, explode=[0, 0, 0], color='#C9DEDF', mass=20, materials=[['glas', 100]], info='Glas statt Metall, damit kabelloses Laden funktioniert. Bricht leicht und ist teuer zu tauschen.', marks=[{'shape': 'box', 'x': 4, 'y': 4, 'w': 28, 'd': 30, 'r': 6}]),
]

schreibe('smartphone', teile)
