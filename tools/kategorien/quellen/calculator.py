"""3D-Modell: calculator. Erzeugt tools/kategorien/modelle/calculator.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Typischer Schul-Taschenrechner mit Solarzelle, 80 × 160 × 15 mm. Hinten (y = 0) Solarzelle und Display,
# vorne das Tastenfeld mit 5 × 8 Tasten. Unten im Gehäuse eine Knopfzelle LR1130 hinter einem kleinen Deckel.
GEH = '#2E3338'
teile = [
    teil('solarzelle', 'solar_cell', 'Solarzelle', 'Solarzelle', 'box',
         x=44, y=6, w=30, d=10, z=14, h=1, r=0.5, mass=2,
         materials=[['glas', 50], ['chip', 30], ['kupfer', 10], ['folien', 10]], color='#5B3E36',
         info='Dünne Silizium-Zelle hinter einem Glasstreifen. Liefert bei Licht den Strom, die Batterie springt nur bei Dunkelheit ein.',
         marks=raster(1, 1, 4, 1, 6.5, 8, 7.2, r=0.3, fill='#6E4A40')),
    teil('fenster', 'plastic_housing', 'Display-Fenster', 'Fenster', 'box', material_id='pc',
         x=8, y=20, w=64, d=26, z=13.6, h=1.4, r=2, mass=3, color='#C9DEDF', opacity=0.6,
         info='Klare Kunststoffscheibe, schützt das empfindliche LCD. Von innen eingeklebt.'),
    teil('oberschale', 'plastic_housing', 'Gehäuse-Oberteil', 'Oberteil', 'box',
         x=0, y=0, w=80, d=160, z=8, h=6, r=8, mass=30, color=GEH,
         info='Hat Ausschnitte für Display, Solarzelle und Tasten. Mit Schrauben von unten befestigt, die oft unter Gummifüßen stecken.',
         marks=[mark('box', 8, 20, 64, 26, 2, '#1E2226'), mark('box', 44, 6, 30, 10, 1, '#1E2226'),
                mark('box', 6, 54, 68, 100, 4, '#1E2226')]),
    teil('tastenmatte', 'silicone_keypad', 'Silikon-Tastenmatte', 'Tastenmatte', 'box',
         x=6, y=54, w=68, d=100, z=7.2, h=7.3, r=4, mass=14, color='#4A5258',
         info='Alle 40 Tasten sind eine einzige Silikonmatte mit leitfähigen Kohle-Pillen auf der Unterseite. Lässt sich als Ganzes herausheben.',
         marks=raster(2, 3, 5, 8, 10.5, 8.5, 13.2, 12, r=2) + [mark('box', 2, 3, 10.5, 8.5, 2, '#C9302C')]),
    teil('lcd', 'lcd_panel', 'Flüssigkristall-Anzeige (LCD)', 'LCD', 'box',
         x=8, y=20, w=64, d=26, z=9, h=2.2, r=1, mass=6, color='#A9B4A2',
         materials=[['glas', 85], ['folien', 15]],
         info='Zwei dünne Glasplatten mit Flüssigkristallen dazwischen. Zerbricht leicht, flach anfassen.',
         marks=raster(4, 8, 10, 1, 5, 10, 5.8, r=0.5, fill='#7E897A')),
    teil('leitgummi', 'lcd_panel', 'Leitgummi-Streifen', 'Leitgummi', 'box', material_id='silicone',
         x=10, y=44, w=60, d=2, z=7.2, h=1.8, r=0.5, mass=0.5, materials=[['gummi', 90], ['graphit', 10]], color='#E1DED6',
         info='Gummistreifen mit feinen leitenden Schichten. Verbindet das LCD ohne Löten mit der Platine.'),
    teil('chip', 'circuit_board', 'Rechenchip (unter Epoxid-Tropfen)', 'Chip', 'cyl',
         x=33, y=34, w=14, z=7.2, h=1.2, mass=0.5, materials=[['chip', 60], ['phenolharz', 40]], color='#1E2226',
         info='Der Chip ist direkt auf die Platine geklebt und mit schwarzem Kunstharz vergossen. Er macht alle Rechnungen.'),
    teil('platine', 'circuit_board', 'Platine mit Kontaktfeldern', 'Platine', 'box',
         x=4, y=4, w=72, d=152, z=6, h=1.2, r=4, mass=8, color='#2E6B45',
         info='Unter jeder Taste ein kammförmiges Kontaktfeld aus Kohle oder Gold. In die Elektro-Sammlung geben.',
         marks=raster(5, 54, 5, 8, 9, 7, 13.2, 12, r=1, fill='#D9D2B8')),
    teil('knopfzelle', 'button_cell', 'Knopfzelle LR1130', 'Knopfzelle', 'cyl',
         x=60, y=132, w=11.6, z=2, h=3.1, mass=2.3, explode=[70, 0, 10], color='#B9BEC2',
         info='Alkali-Knopfzelle 1,5 V als Reserve. Beide Seiten abkleben und in die Batterie-Sammelbox geben, nie verschlucken lassen.',
         marks=[mark('cyl', 2, 2, 7.6, fill='#D0D4D7')]),
    teil('batteriedeckel', 'plastic_housing', 'Batteriedeckel', 'Batteriedeckel', 'box',
         x=54, y=126, w=22, d=22, z=0, h=1.2, r=2, mass=1, explode=[70, 0, 0], color=GEH,
         info='Mit einer kleinen Schraube befestigt. Darunter liegt die Knopfzelle.',
         marks=[mark('cyl', 9, 9, 4, fill='#9BA3A8')]),
    teil('unterschale', 'plastic_housing', 'Gehäuse-Unterteil', 'Unterteil', 'box',
         x=0, y=0, w=80, d=160, z=0, h=8, r=8, mass=28, color=GEH,
         info='Wanne mit Gummifüßen und Batteriefach. Ohne Elektronik ist es reiner ABS-Kunststoff.',
         marks=[mark('box', 54, 126, 22, 22, 2, '#1E2226')]),
]

explodiere(teile, abstand=55, abstaende={'chip': 15, 'leitgummi': 15}, nach_liste=True)
skaliere_masse(teile, oid='calculator')
schreibe('calculator', teile)
