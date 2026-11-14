"""3D-Modell: smoke_detector. Erzeugt tools/kategorien/modelle/smoke_detector.json."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Typischer optischer Rauchmelder, Ø 100 × 40 mm, liegt auf der Montageplatte (Decke = unten).
# Haube mit Raucheinlässen und Prüftaste oben; innen Rauchkammer (Labyrinth) mit IR-LED und Fotodiode,
# Piezo-Summer und 9-V-Block auf/neben der Platine. Batterie wird nach rechts herausgezogen.
GEH = '#ECEDEA'
CHIP = '#3F4547'


def ring(cx, cy, r, n, w, fill):
    return [mark('cyl', round(cx + r * math.cos(2 * math.pi * k / n) - w / 2, 2),
                 round(cy + r * math.sin(2 * math.pi * k / n) - w / 2, 2), w, fill=fill) for k in range(n)]


teile = [
    teil('pruefknopf', 'plastic_housing', 'Prüftaste', 'Prüftaste', 'cyl',
         x=40, y=40, w=20, z=37, h=3, mass=2, color='#D8DAD6',
         info='Drücken löst einen Probealarm aus. Einmal im Monat testen, ob Batterie und Summer noch funktionieren.',
         marks=[mark('cyl', 6, 6, 8, fill='#C9302C')]),
    teil('kuppe', 'plastic_housing', 'Haubenkuppe', 'Kuppe', 'cyl',
         x=22, y=22, w=56, z=33, h=5, mass=8, color=GEH,
         info='Mittlerer, erhöhter Teil der Haube. Ein Stück mit der Haube, im Modell getrennt gezeigt.',
         marks=[mark('cyl', 16, 16, 24, fill='#D8DAD6')]),
    teil('haube', 'plastic_housing', 'Haube mit Raucheinlässen', 'Haube', 'cyl',
         x=2, y=2, w=96, z=20, h=13, mass=22, color=GEH,
         info='Rauch zieht durch die Schlitze ringsum ein. Haube gegen den Uhrzeigersinn drehen und abnehmen.',
         marks=ring(48, 48, 38, 16, 5, '#B9BCB8')),
    teil('rauchkammer', 'plastic_housing', 'Rauchkammer (Labyrinth)', 'Rauchkammer', 'cyl',
         x=16, y=31, w=38, z=11, h=14, mass=5, color='#2B2F33',
         info='Schwarzes Labyrinth mit feinem Insektengitter: Rauch kommt hinein, Licht von außen nicht. Lässt sich abziehen.',
         marks=ring(19, 19, 15, 12, 3, '#4A5156') + [mark('cyl', 11, 11, 16, fill='#1E2226')]),
    teil('gitter', 'plastic_housing', 'Insektengitter', 'Insektengitter', 'cyl', material_id='steel',
         x=14, y=29, w=42, z=11, h=13, mass=1.5, materials=[['stahl', 100]], color='#C9CDD0', opacity=0.45, wand=0.6, boden=0,
         info='Feines Edelstahlnetz rund um die Rauchkammer. Lässt Rauch hinein, aber keine Insekten, die Fehlalarm auslösen.'),
    teil('ir_led', 'circuit_board', 'Infrarot-LED', 'IR-LED', 'cyl', material_id='mixed_electronics',
         x=22, y=46, w=5, z=9.6, h=5, mass=0.2, materials=[['led', 60], ['kupfer', 40]], color='#5A5F8C', opacity=0.85,
         info='Sendet regelmäßig unsichtbare Lichtblitze in die Kammer.'),
    teil('fotodiode', 'circuit_board', 'Fotodiode', 'Fotodiode', 'cyl', material_id='mixed_electronics',
         x=42, y=46, w=5, z=9.6, h=5, mass=0.2, materials=[['chip', 60], ['kupfer', 40]], color='#2B2F33',
         info='Steht schräg zur LED und sieht normalerweise kein Licht. Rauchteilchen streuen das Licht zu ihr: Alarm.'),
    teil('piezo', 'piezo_buzzer', 'Piezo-Summer', 'Summer', 'cyl',
         x=37, y=73, w=20, z=9.6, h=7, mass=4, materials=[['keramik', 35], ['messing', 35], ['pcabs', 30]], color='#2B2F33',
         info='Keramikplättchen auf Messing schwingt bei Spannung und piept mit 85 dB. Auf der Platine lassen.',
         marks=[mark('cyl', 7, 7, 6, fill='#B8A060')]),
    teil('status_led', 'circuit_board', 'Rote Kontroll-LED', 'Kontroll-LED', 'cyl', material_id='mixed_electronics',
         x=66, y=22, w=4, z=9.6, h=4, mass=0.1, materials=[['led', 60], ['kupfer', 40]], color='#C9302C',
         info='Blinkt etwa alle 40 Sekunden kurz rot und zeigt so: Der Melder arbeitet.'),
    teil('batterieclip', 'alkaline_cell', '9-V-Batterieclip mit Kabel', 'Batterieclip', 'box', material_id='mixed_electronics',
         x=60, y=76, w=22, d=8, z=9.6, h=6, r=2, mass=1.5, materials=[['pvc', 40], ['kupfer', 35], ['stahl', 25]],
         color='#2B2F33',
         info='Druckknopf-Kontakte, die auf die Pole der Batterie gedrückt werden. Rotes Kabel Plus, schwarzes Minus.',
         marks=[mark('cyl', 4, 1.5, 5, fill='#B9BEC2'), mark('cyl', 13, 1.5, 5, fill='#B9BEC2')]),
    teil('mikrocontroller', 'circuit_board', 'Steuerchip', 'Chip', 'box',
         x=22, y=16, w=10, d=8, z=9.6, h=1.4, r=0.5, mass=0.3, materials=[['chip', 100]], color=CHIP,
         info='Misst alle paar Sekunden, prüft die Batterie und löst den Alarm aus.'),
    teil('platine', 'circuit_board', 'Platine', 'Platine', 'cyl',
         x=6, y=6, w=88, z=8, h=1.6, mass=10, color='#2E6B45',
         info='Runde Leiterplatte, mit zwei Schrauben im Gehäuse. Zusammen mit dem Gehäuse in die Elektro-Sammlung.',
         marks=[mark('box', 50, 18, 30, 52, 2, '#3E7D55')]),
    teil('batterie', 'alkaline_cell', '9-V-Blockbatterie', '9-V-Block', 'box',
         x=58, y=26, w=26.5, d=48.5, z=9.6, h=17.5, r=2, mass=45, explode=[85, 0, 0], color='#3A6EA5', sortBias=-10,
         info='Alkaline-Block für etwa ein Jahr. Piept der Melder kurz, ist sie leer: Pole abkleben und zur Batterie-Sammelbox.',
         marks=[mark('cyl', 4, 1, 6, fill='#B9BEC2'), mark('cyl', 16, 1, 6, fill='#B9BEC2')]),
    teil('gehaeuse', 'plastic_housing', 'Gehäuse-Unterteil', 'Gehäuse', 'cyl',
         x=0, y=0, w=100, z=6, h=14, mass=28, color=GEH, wand=2,
         info='Trägt Platine und Batteriefach. Ein Schieber verhindert, dass die Haube ohne Batterie schließt.'),
    teil('duebel', 'plastic_housing', 'Schrauben und Dübel', 'Schrauben+Dübel', 'cyl', material_id='steel',
         x=17, y=46, w=6, z=0.5, h=5, mass=4, explode=[-70, 0, 0], materials=[['stahl', 60], ['pp', 40]], color='#C9CDD0',
         info='Zwei Schrauben mit Kunststoffdübeln halten die Montageplatte an der Decke. Stahl und Kunststoff trennen.',
         marks=[mark('cyl', 1.5, 1.5, 3, fill='#5E656A')]),
    teil('sockel', 'plastic_housing', 'Montageplatte', 'Montageplatte', 'cyl',
         x=4, y=4, w=92, z=0, h=6, mass=18, color='#D8DAD6',
         info='Wird an die Decke geschraubt, der Melder rastet mit einer Drehung ein. Reiner Kunststoff.',
         marks=[mark('box', 14, 43, 10, 6, 3, '#B9BCB8'), mark('box', 68, 43, 10, 6, 3, '#B9BCB8')]),
]

explodiere(teile, abstand=40, gruppen=[['kuppe', 'haube']],
           abstaende={'ir_led': 15, 'fotodiode': 15, 'mikrocontroller': 15, 'piezo': 15, 'pruefknopf': 20, 'status_led': 15, 'batterieclip': 15, 'gitter': 15}, nach_liste=True)
skaliere_masse(teile, oid='smoke_detector')
schreibe('smoke_detector', teile)
