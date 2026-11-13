"""3D-Modell: alarm_clock. Erzeugt tools/kategorien/modelle/alarm_clock.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Typischer digitaler Batterie-Wecker, stehend 100 × 60 × 78 mm, Display vorne (y groß).
# Gehäuse in Vorder- und Rückschale geteilt. Innen stehen Platine, LCD und Sichtscheibe hintereinander,
# unten liegen Lautsprecher und zwei AA-Batterien. Oben Schlummertaste und Einstelltasten.
# Explosion von Hand: Rückschale nach hinten, Vorderschale nach links (weg vom Betrachter),
# Platine, LCD und Scheibe nach oben und gestaffelt nach vorne, Tasten über den Körper.
GEH = '#2E3338'
teile = [
    teil('schlummertaste', 'plastic_housing', 'Schlummertaste', 'Schlummertaste', 'box',
         x=25, y=20, w=50, d=16, z=78, h=4, r=3, mass=4, explode=[0, 0, 45], color='#C9302C',
         info='Große Taste oben: drücken, und der Wecker klingelt nach ein paar Minuten noch einmal.',
         marks=[mark('box', 4, 4, 42, 8, 2, '#D9534F')]),
    teil('einstelltasten', 'plastic_housing', 'Einstelltasten', 'Einstelltasten', 'box',
         x=8, y=4, w=84, d=10, z=78, h=2.5, r=2, mass=3, explode=[0, 0, 45], color='#4A5258',
         info='Gummitasten für Uhrzeit, Weckzeit und Licht. Drücken unten auf Kontaktfelder der Platine.',
         marks=raster(4, 2, 4, 1, 16, 6, 21, r=2, fill='#5E656A')),
    teil('frontscheibe', 'plastic_housing', 'Sichtscheibe', 'Sichtscheibe', 'box', material_id='pc',
         x=10, y=57, w=80, d=2, z=26, h=44, r=0.5, mass=8, explode=[0, 60, 20], color='#C9DEDF', opacity=0.6,
         info='Klare Kunststoffscheibe vor dem Display, von innen eingeklebt.'),
    teil('lcd', 'lcd_panel', 'Flüssigkristall-Anzeige (LCD)', 'LCD', 'box',
         x=14, y=50, w=72, d=2.5, z=30, h=36, r=0.5, mass=10, explode=[0, 32, 20], color='#A9B4A2',
         materials=[['glas', 85], ['folien', 15]],
         info='Zeigt die großen Ziffern. Zwei Glasplatten mit Flüssigkristall, über Leitgummis mit der Platine verbunden. Bricht leicht.'),
    teil('chip', 'circuit_board', 'Uhrenchip (unter Epoxid)', 'Chip', 'box',
         x=40, y=45.6, w=14, d=2, z=16, h=10, r=0.5, mass=0.5, explode=[0, 8, 20], materials=[['chip', 60], ['phenolharz', 40]],
         color='#1E2226', info='Zählt mithilfe eines Quarzes die Sekunden und steuert Anzeige und Weckton.'),
    teil('platine', 'circuit_board', 'Platine', 'Platine', 'box',
         x=10, y=44, w=80, d=1.6, z=12, h=60, r=0.5, mass=18, explode=[0, 0, 20], color='#2E6B45',
         info='Steht hinter dem Display. Mit zwei Schrauben in der Rückschale; in die Elektro-Sammlung geben.'),
    teil('lautsprecher', 'speaker_driver', 'Lautsprecher', 'Lautsprecher', 'cyl',
         x=63, y=10, w=34, z=3, h=10, mass=15, explode=[0, 0, 0],
         materials=[['stahl', 35], ['ndfeb', 20], ['kupfer', 15], ['papier', 15], ['pcabs', 15]], color='#5E656A',
         info='Kleiner Lautsprecher für den Weckton, mit Magnet und Kupferspule. Von Bankkarten fernhalten.',
         marks=[mark('cyl', 5, 5, 24, fill='#2B2F33'), mark('cyl', 13, 13, 8, fill='#9BA3A8')]),
    teil('batterie_1', 'alkaline_cell', 'Alkaline-Batterie AA', 'Batterien', 'box',
         x=8, y=8, w=50.5, d=14.5, z=2, h=14.5, r=7, mass=23, explode=[0, 0, 0], color='#3A6EA5',
         info='Zwei AA-Zellen mit je 1,5 V. Herausnehmen und in die Batterie-Sammelbox geben, nie in den Restmüll.',
         marks=[mark('box', 44, 1.5, 6, 11.5, 3, '#C9A227')]),
    teil('batterie_2', 'alkaline_cell', 'Alkaline-Batterie AA', 'Batterie', 'box',
         x=8, y=23, w=50.5, d=14.5, z=2, h=14.5, r=7, mass=23, explode=[0, 0, 0], color='#3A6EA5', label=False,
         info='Zweite AA-Zelle, umgekehrt eingelegt. Ausgelaufene Batterien hinterlassen weißen Belag an den Federn.',
         marks=[mark('box', 0.5, 1.5, 6, 11.5, 3, '#C9A227')]),
    teil('vorderschale', 'plastic_housing', 'Vorderschale', 'Vorderschale', 'box',
         x=0, y=30, w=100, d=30, z=0, h=78, r=6, mass=50, explode=[-140, 0, 0], color=GEH,
         info='Vorderes Gehäuseteil mit Displayfenster. Nach Lösen der Schrauben im Batteriefach abziehbar.',
         marks=[mark('box', 4, 4, 92, 22, 4, '#23272A')]),
    teil('rueckschale', 'plastic_housing', 'Rückschale mit Batteriefach', 'Rückschale', 'box',
         x=0, y=0, w=100, d=30, z=0, h=78, r=6, mass=55, explode=[0, -75, 0], color=GEH,
         info='Hinteres Gehäuseteil mit Batteriefach und Lautsprecher-Löchern. Reiner Kunststoff, wenn alles ausgebaut ist.',
         marks=[mark('box', 4, 4, 92, 22, 4, '#23272A')]),
]

skaliere_masse(teile, oid='alarm_clock')
schreibe('alarm_clock', teile)
