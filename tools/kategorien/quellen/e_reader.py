"""3D-Modell: e_reader. Erzeugt tools/kategorien/modelle/e_reader.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Typischer 6-Zoll-E-Book-Reader, 115 × 160 × 8 mm. E-Ink-Bildschirm oben (y klein), darunter breiterer Rand.
# Innen: flacher Akku unter der oberen Bildschirmhälfte, Platine mit Prozessor, Speicher und WLAN unten.
GEH = '#2B2F33'
CHIP = '#3F4547'
ZELLE = [['lco', 40], ['graphit', 20], ['elektrolyt', 15], ['alu', 15], ['kupfer', 10]]
text = raster(10, 10, 1, 18, 75, 1.6, 0, 5.6, r=0.3, fill='#8E908A')
teile = [
    teil('rahmen', 'plastic_housing', 'Frontrahmen', 'Rahmen', 'box',
         x=0, y=0, w=115, d=160, z=7, h=1, r=8, mass=14, color=GEH,
         info='Dünner Kunststoffrahmen um den Bildschirm, rundum verklebt. Mit Wärme und einem Plektrum vorsichtig lösen.',
         marks=[mark('box', 10, 12, 95, 126, 1, '#D7D8D0')] + raster(20, 22, 1, 17, 75, 1.4, 0, 6.4, r=0.3, fill='#9A9C95')
         + [mark('box', 20, 22, 40, 2.6, 0.5, '#55585A'), mark('box', 50, 129, 15, 1.4, 0.5, '#9A9C95'),
            mark('box', 46, 146, 23, 3, 1.5, '#3A3F43')]),
    teil('frontlicht', 'e_ink_display', 'Frontlicht mit Touch-Folie', 'Frontlicht', 'box',
         x=10, y=12, w=95, d=126, z=6.2, h=0.8, r=1, mass=10,
         materials=[['folien', 60], ['glas', 25], ['led', 10], ['kupfer', 5]], color='#E6ECEC', opacity=0.65,
         info='Lichtleiter-Folie mit kleinen LEDs am Rand, die den Bildschirm von vorne beleuchten. Darüber die Touch-Schicht.',
         marks=raster(4, 123, 10, 1, 3, 2, 9.5, r=0.5, fill='#F2E3A0')),
    teil('eink', 'e_ink_display', 'E-Ink-Bildschirm', 'E-Ink', 'box',
         x=10, y=12, w=95, d=126, z=5.2, h=1, r=1, mass=30,
         materials=[['displayglas', 60], ['folien', 30], ['chip', 5], ['kupfer', 5]], color='#D7D8D0',
         info='Winzige Kapseln mit schwarzen und weißen Farbteilchen auf einer Glasplatte. Braucht nur beim Umblättern Strom. Sehr dünn, bricht leicht.',
         marks=text),
    teil('traeger', 'plastic_housing', 'Display-Trägerplatte', 'Trägerplatte', 'box', material_id='aluminium',
         x=8, y=10, w=99, d=140, z=4.8, h=0.4, r=2, mass=12, materials=[['alu', 100]], color='#C3C8CC',
         info='Dünnes Aluminiumblech unter dem Bildschirm. Macht das Gerät steif und schützt das Glas vor Druck von hinten.',
         marks=[mark('box', 40, 128, 20, 8, 1, '#8D9399')] + raster(4, 4, 2, 2, 3, 3, 88, 129, shape='cyl')),
    teil('flex', 'e_ink_display', 'Display-Flachbandkabel', 'Flexkabel', 'box', material_id='mixed_electronics',
         x=46, y=132, w=22, d=12, z=2.2, h=0.4, r=1, mass=0.8, materials=[['folien', 70], ['kupfer', 30]],
         color='#C98A2E', info='Biegsame Folie mit Kupferbahnen, verbindet Bildschirm und Platine. Stecker vorsichtig hochklappen, nicht ziehen.',
         marks=raster(3, 2, 8, 1, 1.2, 8, 2.2, r=0.2, fill='#E0B062')),
    teil('soc', 'circuit_board', 'Prozessor', 'Prozessor', 'box',
         x=22, y=100, w=12, d=12, z=2.2, h=1, r=0.5, mass=1, materials=[['chip', 100]], color=CHIP,
         info='Steuert Bildschirm, Speicher und WLAN. Unter einem Abschirmblech auf der Platine.'),
    teil('speicher', 'circuit_board', 'Speicherchip (Bücher)', 'Speicher', 'box',
         x=42, y=100, w=11, d=13, z=2.2, h=1, r=0.5, mass=1, materials=[['chip', 100]], color=CHIP,
         info='Speichert Tausende Bücher. Vor dem Abgeben das Gerät auf Werkseinstellungen zurücksetzen.'),
    teil('wlan', 'circuit_board', 'WLAN-Modul', 'WLAN', 'box',
         x=62, y=101, w=10, d=10, z=2.2, h=1.2, r=0.5, mass=0.6, materials=[['stahl', 40], ['chip', 40], ['kupfer', 20]],
         color='#B7BCC0', info='Funkchip unter einem Blechdeckel zum Herunterladen von Büchern.'),
    teil('taster', 'circuit_board', 'Ein-/Aus-Taster', 'Taster', 'box', material_id='mixed_electronics',
         x=72, y=154, w=10, d=4, z=2, h=3, r=1, mass=0.5, materials=[['stahl', 50], ['pcabs', 40], ['kupfer', 10]],
         color='#B7BCC0', info='Kleiner Drucktaster an der Unterkante.'),
    teil('usb_c', 'circuit_board', 'USB-C-Buchse', 'USB-C', 'box', material_id='steel',
         x=52, y=151, w=9, d=8, z=1.5, h=3.2, r=1.5, mass=1, materials=[['stahl', 70], ['kontakte', 15], ['pcabs', 15]],
         color='#B7BCC0', info='Ladebuchse aus Stahlblech mit vergoldeten Kontakten.',
         marks=[mark('box', 1.5, 5, 6, 1.6, 0.8, '#2A2E31')]),
    *[teil(f'schraube{i}', 'circuit_board', 'Kreuzschlitz-Schraube M1,4', 'Schrauben', 'cyl', material_id='steel',
           x=x, y=y, w=2.6, z=2.2, h=0.8, mass=0.1, materials=[['stahl', 100]], color='#9AA0A6', label=i == 0,
           info='Vier winzige Schrauben halten die Platine in der Rückschale. Mit einem Feinmechaniker-Schraubendreher (PH00) lösen.',
           marks=[mark('box', 0.5, 1.1, 1.6, 0.4), mark('box', 1.1, 0.5, 0.4, 1.6)])
      for i, (x, y) in enumerate([(12.5, 90.5), (99.5, 90.5), (12.5, 143.5), (99.5, 143.5)])],
    teil('platine', 'circuit_board', 'Hauptplatine', 'Platine', 'box',
         x=10, y=88, w=95, d=62, z=1.2, h=1, r=2, mass=10, color='#2E6B45',
         info='Leiterplatte mit Kupferbahnen, Lot und Chips. Mit kleinen Schrauben befestigt; in die Elektro-Sammlung geben.',
         marks=raster(70, 6, 2, 3, 8, 6, 11, 9, r=0.5, fill='#22272B')),
    teil('akku', 'li_ion_battery', 'Lithium-Polymer-Akku', 'Akku', 'box',
         x=12, y=14, w=91, d=70, z=1.2, h=3.6, r=2, mass=24, materials=ZELLE, color='#9DA6AD',
         info='Etwa 1.500 mAh, hält wochenlang. Flach verklebt: nie biegen oder einstechen, Pole abkleben und zur Batterie-Sammelstelle.',
         marks=[mark('box', 4, 4, 83, 62, 2), mark('box', 34, 58, 22, 10, 1, '#C8423A')]),
    teil('rueckschale', 'plastic_housing', 'Rückschale', 'Rückschale', 'box',
         x=0, y=0, w=115, d=160, z=0, h=7, r=8, mass=50, color=GEH,
         info='Gummierte Kunststoffwanne, in der alle Teile liegen. Leer ausgebaut ist sie reiner Kunststoff.',
         marks=[mark('box', 3, 3, 109, 154, 6, '#23272A'), mark('box', 74, 154, 8, 3, 1, '#14171A'),
                mark('box', 53, 155, 9, 2, 1, '#14171A')]),
]

explodiere(teile, abstand=65, abstaende={'soc': 18, 'speicher': 18, 'wlan': 18, 'flex': 18, **{f'schraube{i}': 12 for i in range(4)}}, nach_liste=True)
skaliere_masse(teile, oid='e_reader')
schreibe('e_reader', teile)
