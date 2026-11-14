"""3D-Modell: desktop_pc. Erzeugt tools/kategorien/modelle/desktop_pc.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Midi-Tower (200 × 420 × 450 mm), steht aufrecht. Hinten = y 0 (Anschlüsse), vorne = y groß (Frontblende).
# Das Mainboard (ATX, 244 × 305 mm) steht senkrecht am linken Mainboard-Träger (x ≈ 6), alle Bauteile ragen
# nach rechts (x positiv) in den Innenraum; die abnehmbare Seitenwand sitzt rechts bei x 198..200.
# Explosion seitlich: das Gehäuse bleibt stehen, die Bauteile werden schichtweise nach rechts (dx > 0)
# herausgezogen. Die Seitenwand geht nach hinten (dy < 0), damit sie das Innenleben nicht verdeckt;
# Frontblende nach vorn, Netzkabel nach links.
GEH = '#3A3F44'
PCB = '#2E6B45'
CHIP = '#22272B'

teile = [
    teil('seitenwand', 'steel_pc_case', 'Seitenwand', 'Seitenwand', 'box',
         x=198, y=0, w=2, d=400, z=0, h=450, r=0.5, explode=[0, -450, 0], mass=1000, color=GEH,
         info='Stahlblech, hinten mit zwei Rändelschrauben befestigt. Schrauben lösen und nach hinten abziehen.'),
    teil('frontblende', 'plastic_front_panel', 'Frontblende', 'Frontblende', 'box',
         x=0, y=400, w=200, d=20, z=0, h=450, r=3, explode=[0, 70, 0], mass=600, color='#2B2F33',
         info='Kunststoffblende mit Einschalter, USB-Buchsen und Staubfilter. Unten kräftig ziehen, sie ist nur eingeclipst.',
         marks=[mark('cyl', 90, 4, 12, fill='#5DADE2'), mark('box', 30, 6, 14, 6, 1, '#1E2226'),
                mark('box', 50, 6, 14, 6, 1, '#1E2226')]),
    teil('einschalter', 'plastic_front_panel', 'Einschalter', 'Einschalter', 'cyl',
         x=90, y=420, w=16, d=4, z=400, h=16, explode=[0, 110, 0], mass=5, materials=[['pcabs', 80], ['kupfer', 10], ['led', 10]],
         color='#5DADE2', sortBias=500,
         info='Runder Taster mit blauer Leuchte. Hinten hängt ein dünnes Kabel, das zum Mainboard führt; einfach abziehen.'),
    teil('usb_front', 'plastic_front_panel', 'USB-Buchsen vorne', 'USB vorne', 'box',
         x=70, y=420, w=60, d=3, z=370, h=10, r=1, explode=[0, 110, 0], mass=12, materials=[['pcabs', 50], ['stahl', 30], ['kupfer', 20]],
         color='#1E2226', sortBias=500,
         info='Zwei USB-Buchsen und Kopfhöreranschluss auf einer kleinen Platine, mit Kabeln ans Mainboard gesteckt.'),
    teil('gehaeuseluefter', 'cpu_cooler', 'Gehäuselüfter vorne', 'Gehäuselüfter', 'box', material_id='mixed_electronics',
         x=40, y=374, w=120, d=25, z=250, h=120, r=4, mass=150,
         materials=[['pcabs', 65], ['kupfer', 20], ['ferrit', 10], ['stahl', 5]], color='#2B2F33',
         info='120-mm-Lüfter hinter der Frontblende, saugt kühle Luft an. Vier Schrauben lösen und das Kabel vom Mainboard abziehen.',
         marks=[mark('cyl', 6, 2, 108, 21, fill='#1E2226')]),
    teil('kuehlerluefter', 'cpu_cooler', 'Lüfter des CPU-Kühlers', 'Kühlerlüfter', 'box', material_id='mixed_electronics',
         x=22, y=155, w=120, d=25, z=290, h=120, r=4, mass=130,
         materials=[['pcabs', 60], ['kupfer', 20], ['ferrit', 10], ['stahl', 5], ['chip', 5]], color='#2B2F33',
         info='120-mm-Lüfter, mit Drahtklammern am Kühlkörper. Er bläst die warme Luft nach hinten aus dem Gehäuse.',
         marks=[mark('cyl', 6, 2, 108, 21, fill='#1E2226')]),
    teil('kuehler', 'cpu_cooler', 'CPU-Kühlkörper mit Heatpipes', 'CPU-Kühler', 'box',
         x=10.6, y=100, w=150, d=55, z=290, h=125, r=2, mass=550, materials=[['alu', 75], ['kupfer', 25]], color='#C9CED2',
         info='Viele dünne Aluminiumlamellen auf Kupfer-Heatpipes. Leicht verdrehen, damit sich die Wärmeleitpaste löst, dann abheben.',
         marks=raster(4, 5, 1, 1, 142, 45, 0, fill='#B5BBC0') + raster(20, 8, 4, 1, 8, 8, 32, shape='cyl', fill='#B87333')),
    teil('ram', 'circuit_board', 'Arbeitsspeicher (2 Module)', 'RAM', 'box',
         x=7.6, y=195, w=31, d=16, z=280, h=133, r=0.5, mass=70,
         materials=[['fr4', 45], ['chip', 30], ['kupfer', 15], ['alu', 10]], color='#1F3A5F',
         info='Zwei Speicherriegel mit Speicherchips. Die Klammern am Steckplatz zur Seite drücken, dann gerade herausziehen.'),
    teil('cpu', 'circuit_board', 'Prozessor (CPU)', 'Prozessor', 'box',
         x=7.6, y=110, w=3, d=40, z=330, h=40, r=1, mass=30, materials=[['chip', 50], ['kupfer', 35], ['fr4', 15]],
         color='#B5BBC0',
         info='Das Rechenzentrum des PCs: ein Siliziumchip unter einem vernickelten Kupferdeckel. Enthält auch etwas Gold.'),
    teil('ssd', 'hard_drive', 'M.2-SSD', 'SSD', 'box', material_id='pcb',
         x=7.6, y=110, w=2.5, d=22, z=230, h=80, r=0.5, mass=8, materials=[['fr4', 45], ['chip', 40], ['kupfer', 10], ['lot', 5]],
         color=PCB,
         info='Flacher Speicherriegel mit dem Betriebssystem und allen Daten. Eine Schraube lösen; vor dem Abgeben Daten löschen.'),
    teil('grafikkarte', 'circuit_board', 'Grafikkarte', 'Grafikkarte', 'box',
         x=7.6, y=15, w=112, d=250, z=185, h=40, r=3, mass=900,
         materials=[['alu', 35], ['fr4', 20], ['kupfer', 15], ['pcabs', 15], ['chip', 10], ['stahl', 5]], color='#2B2F33',
         info='Eigene Platine mit Grafikchip, Speicher, Kühlkörper und Lüftern. Hinten verschraubt, im Steckplatz mit einem Riegel gesichert.',
         marks=[mark('cyl', 10, 20, 90, 95, fill='#1E2226'), mark('cyl', 10, 135, 90, 95, fill='#1E2226')]),
    teil('mainboard', 'circuit_board', 'Mainboard (Hauptplatine)', 'Mainboard', 'box',
         x=6, y=15, w=1.6, d=244, z=140, h=305, r=0.5, mass=600,
         materials=[['fr4', 50], ['kupfer', 18], ['chip', 15], ['stahl', 7], ['alu', 5], ['lot', 5]], color=PCB,
         info='Verbindet alle Bauteile. Mit neun Schrauben am Gehäuse, vorher alle Stecker abziehen. Enthält Gold, Kupfer und Zinn.'),
    teil('festplatte', 'hard_drive', 'Festplatte (3,5 Zoll)', 'Festplatte', 'box',
         x=40, y=240, w=101.6, d=147, z=20, h=26, r=2, mass=640,
         materials=[['alu', 55], ['stahl', 15], ['fr4', 10], ['kupfer', 10], ['ndfeb', 5], ['chip', 5]], color='#B5BBC0',
         info='Drehende Magnetscheiben mit Lese-Schreibkopf und Neodym-Magneten. Daten löschen oder die Platte zerstören.',
         marks=[mark('box', 6, 6, 89, 100, 4, '#C9CED2'), mark('box', 10, 112, 82, 30, 1, '#E8E8E0')]),
    teil('netzteil', 'power_supply_unit', 'Netzteil', 'Netzteil', 'box',
         x=20, y=5, w=150, d=140, z=5, h=86, r=2, mass=1700,
         materials=[['stahl', 45], ['kupfer', 15], ['alu', 10], ['fr4', 10], ['ferrit', 8], ['chip', 5], ['pcabs', 5], ['elektrolyt', 2]],
         color='#2B2F33',
         info='Macht aus 230 Volt die Gleichspannungen für den PC. Nur ausschrauben, nicht öffnen: Die Kondensatoren können noch geladen sein.',
         marks=[mark('cyl', 15, 10, 120, fill='#1E2226')] + raster(25, 70, 1, 4, 100, 3, 0, 12, fill='#3A3F44')),
    teil('gehaeuse', 'steel_pc_case', 'Gehäuse (Stahlrahmen)', 'Gehäuse', 'box',
         x=0, y=0, w=198, d=400, z=0, h=450, r=1, mass=3400, color=GEH,
         info='Leeres Gehäuse aus verzinktem Stahlblech mit Laufwerksschächten. Wenn alles ausgebaut ist: ab zum Altmetall.',
         marks=raster(30, 50, 7, 6, 14, 3, 20, 8, fill='#22262A') + [mark('box', 20, 250, 150, 120, 4, '#2B2F33')]),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box', form='liegend_x',
         x=20, y=180, w=160, d=10, z=0, h=8, r=4, explode=[0, 330, 0], mass=150, materials=[['pvc', 90], ['pp', 10]],
         color='#2B2F33', info='1,5 m Kaltgerätekabel mit PVC-Mantel. Stecker abschneiden und längs aufschlitzen.',
         marks=[mark('box', 0, 0, 25, 10, 2, '#4A5156'), mark('box', 135, 0, 25, 10, 2, '#4A5156')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box', form='liegend_x',
         x=20, y=205, w=160, d=4, z=0, h=4, r=1, explode=[0, 340, 0], mass=70, color='#B87333',
         info='Drei Kupferadern (Phase, Neutralleiter, Schutzleiter). Reines Kupfer ist wertvoll.'),
]


# Explosion von Hand: Mainboard mit allem, was darauf steckt, rechts neben dem Gehäuse; der Kühler hebt sich nach
# oben ab, damit Prozessor und RAM sichtbar bleiben; Netzteil und Festplatte unten rechts.
VERSATZ = {
    'mainboard': [230, 0, 0], 'cpu': [262, 0, 0], 'ram': [262, 0, 0], 'ssd': [262, 0, 0],
    'grafikkarte': [262, 0, -30], 'kuehler': [330, 0, 150], 'kuehlerluefter': [330, 0, 150],
    'netzteil': [250, -40, -110], 'festplatte': [260, 120, -60], 'gehaeuseluefter': [250, 110, 100],
}
for p in teile:
    if p['id'] in VERSATZ:
        p['explode'] = VERSATZ[p['id']]
    elif p['explode'] is None:
        p['explode'] = [0, 0, 0]
skaliere_masse(teile, oid='desktop_pc')
for p in teile:   # Foto-Ansicht: echte Formen (form) tragen keine aufgemalten Details
    if p.get('form') and p.get('marks'):
        p['marks'] = [dict(k, zeichnung=True) for k in p['marks']]
schreibe('desktop_pc', teile)
