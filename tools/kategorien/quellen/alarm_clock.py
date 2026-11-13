"""3D-Modell: alarm_clock. Erzeugt tools/kategorien/modelle/alarm_clock.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Typischer digitaler Batterie-Wecker, stehend 100 × 60 × 80 mm, Display vorne (y groß).
# Gehäuse in Vorder- und Rückschale geteilt. Innen stehen Platine, Leitgummi, LCD und Sichtscheibe hintereinander,
# unten hinten liegen Lautsprecher und zwei AA-Batterien. Oben Schlummertaste und Einstelltasten.
# Die Sichtscheibe sitzt bündig in der Front (1 mm vorstehend), damit das Display zusammengebaut sichtbar ist.
# Explosion von Hand: Rückschale nach hinten, Vorderschale nach links (weg vom Betrachter),
# Platine, LCD und Scheibe nach oben und gestaffelt nach vorne, Batterien und Lautsprecher nach rechts.
GEH = '#2E3338'
teile = [
    teil('schlummertaste', 'plastic_housing', 'Schlummertaste mit Licht', 'Schlummertaste', 'box',
         x=25, y=22, w=50, d=16, z=78, h=4, r=3, mass=4, explode=[0, 0, 45], color='#C9302C',
         info='Große Taste oben: drücken, und der Wecker klingelt nach ein paar Minuten noch einmal. Schaltet auch das Licht an.',
         marks=[mark('box', 4, 4, 42, 8, 2, '#D9534F')]),
    teil('einstelltasten', 'plastic_housing', 'Einstelltasten', 'Einstelltasten', 'box', material_id='silicone',
         x=8, y=4, w=84, d=10, z=78, h=2.5, r=2, mass=3, explode=[0, 0, 45], color='#4A5258',
         materials=[['gummi', 100]],
         info='Gummitasten für Uhrzeit, Weckzeit und Alarm an/aus. Drücken unten auf Kontaktfelder der Platine.',
         marks=raster(4, 2, 4, 1, 16, 6, 21, r=2, fill='#6E767C')),
    teil('schrauben', 'plastic_housing', 'Gehäuseschrauben (4 Stück)', 'Schrauben', 'cyl', material_id='steel',
         x=48, y=12, w=4, z=30, h=12, mass=2, explode=[0, -75, 100], color='#9AA2A8',
         info='Kleine Kreuzschlitzschrauben im Batteriefach halten beide Schalen zusammen.',
         marks=[mark('cyl', 1, 1, 2, fill='#5E656A')]),
    teil('sichtscheibe', 'plastic_housing', 'Sichtscheibe', 'Sichtscheibe', 'box', material_id='pc',
         x=8, y=59, w=84, d=2, z=22, h=50, r=1, mass=8, explode=[0, 60, 20], color='#B9CED0', opacity=0.55, sortBias=8,
         info='Klare Kunststoffscheibe vor dem Display, eingeklebt. Mit einem Föhn erwärmen, dann lässt sie sich lösen.'),
    teil('lcd', 'lcd_panel', 'Flüssigkristall-Anzeige (LCD)', 'LCD', 'box',
         x=12, y=56.4, w=76, d=2.6, z=26, h=42, r=0.5, mass=10, explode=[0, 34, 20], color='#9FAE98', sortBias=11,
         materials=[['glas', 85], ['folien', 15]],
         info='Zeigt die großen Ziffern. Zwei Glasplatten mit Flüssigkristall dazwischen. Bricht leicht, flach anfassen.'),
    teil('leitgummi', 'lcd_panel', 'Leitgummi-Streifen', 'Leitgummi', 'box', material_id='silicone',
         x=14, y=47.6, w=72, d=8.8, z=22, h=4, r=1, mass=1, explode=[0, 22, 20], color='#E1DED6',
         materials=[['gummi', 90], ['graphit', 10]],
         info='Gummistreifen mit feinen leitenden Schichten. Verbindet das LCD ohne Löten mit der Platine.',
         marks=raster(1, 1, 24, 1, 1.5, 6.8, 2.95, fill='#7E7A72')),
    teil('led', 'circuit_board', 'Hintergrund-LED', 'LED', 'box', material_id='mixed_electronics',
         x=46, y=45.6, w=8, d=4, z=70, h=3, r=1, mass=0.2, explode=[0, 10, 20],
         materials=[['led', 60], ['kupfer', 40]], color='#F4F0D0',
         info='Beleuchtet das Display kurz, wenn man die Schlummertaste drückt.'),
    teil('chip', 'circuit_board', 'Uhrenchip (unter Epoxid)', 'Chip', 'box',
         x=34, y=45.6, w=14, d=2, z=32, h=12, r=0.5, mass=0.5, explode=[0, 8, 20],
         materials=[['chip', 60], ['phenolharz', 40]], color='#1E2226',
         info='Schwarzer Kunstharz-Tropfen über dem Chip. Zählt die Sekunden und steuert Anzeige und Weckton.'),
    teil('quarz', 'circuit_board', 'Uhrenquarz 32 kHz', 'Quarz', 'box', material_id='mixed_electronics',
         x=56, y=45.6, w=8, d=2.5, z=34, h=3, r=1.2, mass=0.2, explode=[0, 8, 20],
         materials=[['stahl', 50], ['glas', 30], ['kupfer', 20]], color='#B9BEC2',
         info='Winziger Quarzkristall, der genau 32.768-mal pro Sekunde schwingt. Daraus zählt der Chip die Zeit.'),
    teil('platine', 'circuit_board', 'Platine', 'Platine', 'box',
         x=10, y=44, w=80, d=1.6, z=12, h=62, r=0.5, mass=18, explode=[0, 0, 20], color='#2E6B45',
         info='Steht hinter dem Display. Mit zwei Schrauben in der Rückschale; in die Elektro-Sammlung geben.'),
    teil('lautsprecher', 'speaker_driver', 'Lautsprecher', 'Lautsprecher', 'cyl',
         x=63, y=8, w=34, z=3, h=10, mass=15, explode=[125, 0, 0],
         materials=[['stahl', 35], ['ndfeb', 20], ['kupfer', 15], ['papier', 15], ['pcabs', 15]], color='#5E656A',
         info='Kleiner Lautsprecher für den Weckton, mit Magnet und Kupferspule. Von Bankkarten fernhalten.',
         marks=[mark('cyl', 5, 5, 24, fill='#2B2F33'), mark('cyl', 13, 13, 8, fill='#9BA3A8')]),
    teil('batterie_1', 'alkaline_cell', 'Alkaline-Batterie AA', 'Batterien', 'box',
         x=8, y=8, w=50.5, d=14.5, z=2, h=14.5, r=7, mass=23, explode=[118, 0, 0], color='#3A6EA5',
         info='Zwei AA-Zellen mit je 1,5 V. Herausnehmen und in die Batterie-Sammelbox geben, nie in den Restmüll.',
         marks=[mark('box', 44, 1.5, 6, 11.5, 3, '#C9A227'), mark('box', 4, 3, 30, 8.5, 2, '#5E8CB8')]),
    teil('batterie_2', 'alkaline_cell', 'Alkaline-Batterie AA', 'Batterie', 'box',
         x=8, y=23, w=50.5, d=14.5, z=2, h=14.5, r=7, mass=23, explode=[118, 0, 0], color='#3A6EA5', label=False,
         info='Zweite AA-Zelle, umgekehrt eingelegt. Ausgelaufene Batterien hinterlassen weißen Belag an den Federn.',
         marks=[mark('box', 0.5, 1.5, 6, 11.5, 3, '#C9A227'), mark('box', 16, 3, 30, 8.5, 2, '#5E8CB8')]),
    teil('federn', 'alkaline_cell', 'Batterie-Kontaktfedern', 'Kontaktfedern', 'box', material_id='steel',
         x=3, y=8, w=4, d=30, z=2, h=14, r=1, mass=2, explode=[100, 0, 0], color='#B9BEC2',
         materials=[['stahl', 90], ['nickel', 10]],
         info='Vernickelte Stahlfedern drücken die Batterien an. Grüner oder weißer Belag heißt: Batterie ist ausgelaufen.',
         marks=raster(0.5, 2, 1, 2, 3, 11, 0, 15, r=1.5, fill='#8E969B')),
    teil('vorderschale', 'plastic_housing', 'Vorderschale', 'Vorderschale', 'box',
         x=0, y=30, w=100, d=29, z=0, h=78, r=3, mass=50, explode=[-140, 0, 0], color=GEH,
         info='Vorderes Gehäuseteil mit Displayfenster. Nach Lösen der Schrauben im Batteriefach abziehbar.',
         marks=[mark('box', 22, 5, 56, 10, 2, '#23272A')]),
    teil('rueckschale', 'plastic_housing', 'Rückschale', 'Rückschale', 'box',
         x=0, y=2, w=100, d=28, z=0, h=78, r=3, mass=52, explode=[0, -75, 0], color=GEH,
         info='Hinteres Gehäuseteil mit Lautsprecher-Löchern. Reiner Kunststoff, wenn alles ausgebaut ist.',
         marks=raster(6, 2, 4, 1, 18, 10, 21, r=2, fill='#23272A')),
    teil('batteriedeckel', 'plastic_housing', 'Batteriefachdeckel', 'Batteriedeckel', 'box',
         x=4, y=0, w=58, d=2, z=1, h=20, r=1, mass=3, explode=[0, -120, 0], color='#3A3F44',
         info='Rastet hinten unten ein. Mit dem Daumen auf den Pfeil drücken und herunterschieben.'),
]

skaliere_masse(teile, oid='alarm_clock')
schreibe('alarm_clock', teile)
