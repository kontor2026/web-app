"""3D-Modell: digital_camera. Erzeugt tools/kategorien/modelle/digital_camera.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Kompaktkamera mit Zoomobjektiv (110 × 65 × 45 mm). Sie liegt auf dem Rücken: Display unten, Objektiv zeigt
# nach oben (z). Gehäuse z 0..28, das eingefahrene Objektiv ragt bis z 45. Oben (y 0) ist die Kameraoberseite,
# unten (y 65) die Klappe für Akku und Speicherkarte. Links der Blitz, rechts der Objektivtubus.
# Explosion: Rückschale bleibt, Display, Platine, Sensor, Tubus, Linsen und Frontschale schweben darüber
# (nach_liste). Akku und Karte werden durch die Klappe nach vorn herausgezogen (dy > 0).
GEH = '#3A3F44'
GLAS = '#BFD8E0'
LX, LY = 66, 32.5  # Mitte des Objektivs

teile = [
    teil('frontschale', 'plastic_housing', 'Frontschale (Aluminium)', 'Frontschale', 'box', material_id='aluminium',
         x=0, y=0, w=110, d=65, z=14, h=14, r=6, mass=50, sortBias=1, materials=[['alu', 85], ['pcabs', 15]], color='#9AA2A8',
         info='Vorderes Gehäuseteil aus Aluminium mit Öffnung für das Objektiv. Nach dem Lösen der kleinen Schrauben '
              'an Seiten und Boden abheben.',
         marks=[mark('cyl', LX - 23, LY - 23, 46, fill='#2B2F33'), mark('box', 8, 5, 30, 10, 2, '#E8ECEE'),
                mark('cyl', 92, 8, 6, fill='#C0392B')]),
    teil('frontlinse', 'camera_lens_unit', 'Frontlinse', 'Frontlinse', 'cyl', material_id='special_glass',
         x=LX - 10, y=LY - 10, w=20, z=42, h=3, mass=3, materials=[['glas', 100]], color=GLAS, opacity=0.65,
         info='Vorderste Glaslinse, sammelt das Licht. Optisches Glas, nicht ins Altglas.'),
    teil('linse_mitte', 'camera_lens_unit', 'Zoomlinse', 'Zoomlinse', 'cyl', material_id='special_glass',
         x=LX - 8, y=LY - 8, w=16, z=32, h=3, mass=2, materials=[['glas', 100]], color=GLAS, opacity=0.65,
         info='Bewegliche Linsengruppe: Ein kleiner Motor verschiebt sie zum Zoomen.'),
    teil('linse_hinten', 'camera_lens_unit', 'Fokuslinse', 'Fokuslinse', 'cyl', material_id='special_glass',
         x=LX - 6, y=LY - 6, w=12, z=22, h=3, mass=1.5, materials=[['glas', 100]], color=GLAS, opacity=0.65,
         info='Stellt scharf, indem sie sich ein winziges Stück vor oder zurück bewegt.'),
    teil('tubus', 'camera_lens_unit', 'Objektivtubus', 'Tubus', 'cyl',
         x=LX - 22, y=LY - 22, w=44, z=16, h=26, mass=40, materials=[['pcabs', 60], ['alu', 25], ['stahl', 10], ['kupfer', 5]],
         color='#2B2F33',
         info='Ineinander gesteckte Ringe, die beim Einschalten ausfahren. Mit drei Schrauben auf dem Sensor befestigt.',
         marks=[mark('cyl', 4, 4, 36, fill='#3A3F44'), mark('cyl', 12, 12, 20, fill='#1E2226')]),
    teil('ausloeser', 'plastic_housing', 'Auslöser mit Zoomhebel', 'Auslöser', 'cyl', material_id='aluminium',
         x=80, y=0, w=14, d=4, z=16, h=10, mass=2, materials=[['alu', 60], ['pcabs', 30], ['stahl', 10]],
         color='#C9CED2', explode=[0, -40, 40],
         info='Metallknopf auf der Oberseite, darum ein Ring als Zoomhebel. Darunter sitzt ein winziger Taster auf einem Flachbandkabel.'),
    teil('zoommotor', 'camera_lens_unit', 'Zoommotor', 'Zoommotor', 'cyl',
         x=90, y=44, w=10, z=16, h=12, mass=5, materials=[['stahl', 40], ['kupfer', 35], ['ndfeb', 20], ['pcabs', 5]],
         color='#B5BBC0', sortBias=-8,
         info='Winziger Elektromotor mit Zahnrädern, der den Tubus aus- und einfährt. Enthält einen Neodym-Magneten.'),
    teil('bildsensor', 'camera_lens_unit', 'Bildsensor', 'Bildsensor', 'box',
         x=LX - 10, y=LY - 7.5, w=20, d=15, z=14, h=2, r=1, mass=3, materials=[['chip', 50], ['keramik', 30], ['glas', 20]],
         color='#4B3B5C',
         info='Siliziumchip mit Millionen lichtempfindlicher Punkte (Pixel), hinter einem Schutzglas. Nicht berühren.',
         marks=[mark('box', 4, 3, 12, 9, 0.5, '#7A5C8C')]),
    teil('blitz', 'circuit_board', 'Blitzeinheit mit Kondensator', 'Blitz', 'box', material_id='mixed_electronics',
         x=6, y=3, w=34, d=13, z=16, h=10, r=3, mass=15,
         materials=[['alu', 35], ['glas', 15], ['kupfer', 15], ['papier', 10], ['elektrolyt', 10], ['fr4', 10], ['pcabs', 5]],
         color='#C9CED2',
         info='Blitzröhre mit Reflektor und einem großen Kondensator, der auf über 300 Volt aufgeladen wird. '
              'Gefährlich: nie an die Kontakte fassen, auch wenn der Akku fehlt.',
         marks=[mark('box', 2, 2, 22, 9, 2, '#F2F2E8'), mark('cyl', 25, 2, 8, fill='#2B2F33')]),
    teil('hauptplatine', 'circuit_board', 'Hauptplatine', 'Hauptplatine', 'box',
         x=44, y=4, w=62, d=57, z=12, h=1.2, r=2, mass=18,
         materials=[['fr4', 45], ['kupfer', 20], ['chip', 25], ['lot', 10]], color='#2E6B45',
         info='Mit Bildprozessor, Speicher und Kartenleser. Flachbandkabel zu Display und Objektiv vorsichtig lösen.',
         marks=[mark('box', 40, 42, 12, 12, 1, '#22272B'), mark('box', 4, 44, 10, 8, 1, '#22272B')]),
    teil('akku', 'li_ion_battery', 'Lithium-Ionen-Akku', 'Akku', 'box',
         x=4, y=17, w=36, d=44, z=4, h=9, r=2, explode=[0, 80, 0], mass=22, color='#2B2F33',
         materials=[['lco', 38], ['graphit', 20], ['elektrolyt', 15], ['alu', 12], ['kupfer', 8], ['pcabs', 7]],
         info='Wechselakku mit Kontakten an einer Kante. Klappe öffnen, Riegel zur Seite schieben, Akku herausnehmen. '
              'Pole abkleben und zur Batterie-Sammelstelle.',
         marks=[mark('box', 4, 6, 28, 30, 2, '#5DADE2')]),
    teil('speicherkarte', 'memory_card', 'SD-Speicherkarte', 'Speicherkarte', 'box',
         x=10, y=33, w=24, d=32, z=13.5, h=2.1, r=1, explode=[0, 80, 15], mass=2,
         materials=[['pcabs', 55], ['chip', 35], ['kupfer', 10]], color='#1F3A5F',
         info='Speichert die Fotos. Zum Lösen eindrücken; die Fotos vorher sichern und die Karte löschen oder behalten.',
         marks=[mark('box', 3, 3, 18, 10, 1, '#E8E8E0')]),
    teil('display', 'lcd_panel', 'LCD-Display', 'Display', 'box',
         x=6, y=8, w=74, d=49, z=1.5, h=3.5, r=2, mass=14,
         materials=[['displayglas', 70], ['folien', 15], ['led', 5], ['kupfer', 5], ['chip', 5]], color='#31373B',
         info='3-Zoll-Bildschirm mit Hintergrundlicht, zeigt nach hinten. Flach anfassen, das Glas bricht leicht.',
         marks=[mark('box', 6, 2, 62, 45, 1, '#9AA2A8')]),
    teil('rueckschale', 'plastic_housing', 'Rückschale mit Tasten', 'Rückschale', 'box',
         x=0, y=0, w=110, d=65, z=0, h=14, r=6, mass=40, color=GEH,
         info='Hinteres Gehäuseteil mit Displayfenster, Tasten und Stativgewinde. Kunststoff mit kleinen Metallteilen.',
         marks=[mark('box', 4, 6, 78, 53, 3, '#2B2F33'), mark('cyl', 88, 20, 14, fill='#4A5156')]),
]

explodiere(teile, abstand=18, nach_liste=True,
           abstaende={'frontschale': 40, 'frontlinse': 12, 'linse_mitte': 12, 'linse_hinten': 12, 'bildsensor': 10})
next(p for p in teile if p['id'] == 'blitz')['explode'][0] = -60  # Blitz nach links neben den Tubus
skaliere_masse(teile, oid='digital_camera')
schreibe('digital_camera', teile)
