"""3D-Modell: power_bank. Erzeugt tools/kategorien/modelle/power_bank.json.

Typische flache 10.000-mAh-Powerbank: zwei Lithium-Polymer-Zellen nebeneinander, vorne (y groß) die Platine
mit USB-C- und USB-A-Buchse, Ladechip, Spule, Taster und vier Anzeige-LEDs. Ebenen werden nach oben abgehoben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, schreibe  # noqa: E402

GEH = '#2F3438'
ZELLE = [['lco', 40], ['graphit', 20], ['elektrolyt', 15], ['alu', 15], ['kupfer', 10]]
teile = [
    teil('oberschale', 'plastic_housing', 'Gehäuse-Oberschale', 'Oberschale', 'box',
         x=0, y=0, w=70, d=140, z=8, h=7, r=9, mass=24,
         info='PC/ABS, meist mit Clips eingerastet und zusätzlich verklebt. Nicht aufhebeln: '
              'Ein Schraubendreher kann darunter den Akku beschädigen.',
         color=GEH, marks=raster(27, 120.5, 4, 1, 2, 2, 5, shape='cyl', fill='#7FC8F0')
                         + [mark('cyl', 54, 122, 6, fill='#4A5156'), mark('box', 14, 30, 42, 60, 6)]),
    teil('polster', 'plastic_housing', 'Schaumstoff-Klebepads', 'Schaumpolster', 'box', material_id='pu_foam',
         x=10, y=20, w=50, d=70, z=12, h=1, r=3, mass=2, sortBias=-6, materials=[['schaum', 70], ['klebstoff', 30]],
         color='#3F4448', info='Doppelseitig klebender Schaum hält die Zellen fest und dämpft Stöße. Beim Öffnen '
                               'kleben die Zellen oft am Deckel: langsam und ohne Werkzeug lösen.',
         marks=[mark('box', 2, 2, 20, 66, 2, '#4A5054'), mark('box', 28, 2, 20, 66, 2, '#4A5054')]),
    teil('lichtleiter', 'plastic_housing', 'Lichtleiter', 'Lichtleiter', 'box', material_id='pc',
         x=25, y=118, w=20, d=7, z=4.5, h=3, r=1, mass=0.4, materials=[['pcabs', 100]], color='#DCEAF0', opacity=0.6,
         info='Klarer Kunststoffsteg, der das Licht der LEDs zu den kleinen Fenstern im Gehäuse leitet.',
         marks=raster(1.5, 2.5, 4, 1, 2, 2, 5, shape='cyl', fill='#BFD7E2')),
    teil('leds', 'circuit_board', 'Anzeige-LEDs', 'LEDs', 'box',
         material_id='mixed_electronics', x=26, y=119, w=18, d=5, z=3.2, h=1, r=0.5, mass=0.3,
         materials=[['led', 50], ['kupfer', 20], ['pcabs', 30]],
         info='Vier kleine Leuchtdioden zeigen an, wie voll der Akku ist.',
         color='#E8E8E2', marks=raster(1, 1.5, 4, 1, 2, 2, 5, fill='#7FC8F0')),
    teil('taster', 'circuit_board', 'Taster', 'Taster', 'box',
         material_id='mixed_electronics', x=53, y=121, w=8, d=8, z=3.2, h=3.5, r=1, mass=0.5,
         materials=[['stahl', 50], ['pcabs', 40], ['kupfer', 10]],
         info='Kleiner Drucktaster. Ein Druck zeigt den Ladestand an.',
         color='#B7BCC0', marks=[mark('cyl', 2, 2, 4, fill='#2A2E31')]),
    teil('ladechip', 'circuit_board', 'Lade- und Wandler-Chip', 'Ladechip', 'box',
         material_id='pcb', x=10, y=116, w=6, d=6, z=3.2, h=1, r=0.3, mass=0.4, materials=[['chip', 100]],
         info='Steuert das Laden der Zellen und wandelt 3,7 Volt in 5 Volt für das Handy um.',
         color='#22272B', marks=[mark('cyl', 0.6, 0.6, 1)]),
    teil('spule', 'circuit_board', 'Speicherdrossel', 'Spule', 'box',
         material_id='mixed_electronics', x=17.5, y=115, w=7, d=7, z=3.2, h=4, r=0.5, mass=1.5,
         materials=[['ferrit', 60], ['kupfer', 40]],
         info='Kupferdraht auf einem Ferritkern. Speichert kurz Energie, damit der Spannungswandler arbeiten kann.',
         color='#3A3F44', marks=[mark('cyl', 1, 1, 5, fill='#C5803D'), mark('cyl', 2.5, 2.5, 2)]),
    teil('usb_a', 'circuit_board', 'USB-A-Buchse (Ausgang)', 'USB-A', 'box',
         material_id='steel', x=34, y=126, w=13.5, d=14, z=3.2, h=6, r=0.5, mass=2.5,
         materials=[['stahl', 70], ['kontakte', 15], ['pcabs', 15]],
         info='Hier wird das Handy angeschlossen. Stahlblech mit vergoldeten Kontakten.',
         color='#B7BCC0', marks=[mark('box', 1.5, 9, 10.5, 3, 0.3, '#2A2E31')]),
    teil('usb_c', 'circuit_board', 'USB-C-Buchse (Ein- und Ausgang)', 'USB-C', 'box',
         material_id='steel', x=18, y=132, w=9, d=8, z=3.2, h=3.2, r=1.5, mass=1,
         materials=[['stahl', 70], ['kontakte', 15], ['pcabs', 15]],
         info='Zum Aufladen der Powerbank, kann aber auch selbst laden.',
         color='#B7BCC0', marks=[mark('box', 1.5, 5, 6, 1.6, 0.8, '#2A2E31')]),
    teil('platine', 'circuit_board', 'Platine', 'Platine', 'box',
         x=4, y=112, w=62, d=26, z=2, h=1.2, r=1.5, mass=6,
         info='Leiterplatte mit Kupferbahnen, Lot und Chips. Als Elektroschrott abgeben, '
              'dort werden Kupfer und Gold zurückgewonnen.',
         color='#2E6B45', marks=[mark('box', 2, 2, 10, 6, 0.5), mark('box', 50, 2, 10, 6, 0.5)]),
    teil('schutz', 'li_ion_battery', 'Schutzschaltung der Zellen', 'Schutzplatine', 'box',
         material_id='pcb', x=6, y=104, w=58, d=6, z=2, h=3, r=0.5, mass=2,
         info='Verhindert Überladen, Tiefentladen und Kurzschluss. Über Nickelstreifen mit den Zellen verlötet.',
         color='#2E6B45', marks=[mark('box', 6, 1.5, 4, 3, 0.3, '#22272B'), mark('box', 48, 1.5, 4, 3, 0.3, '#22272B'),
                                mark('box', 13, 1, 32, 4, 0.5, '#C9CDD0')]),
    teil('nickel', 'li_ion_battery', 'Nickelstreifen (Zellverbinder)', 'Nickelstreifen', 'box', material_id='steel',
         x=8, y=100, w=54, d=4, z=11.5, h=0.3, r=0.5, mass=1, sortBias=-5, materials=[['nickel', 100]], color='#C9CDD0',
         info='Dünne Nickelbleche, an die Pole der Zellen geschweißt. Sie verbinden beide Zellen parallel mit der Schutzplatine.',
         marks=[mark('box', 4, 1, 6, 2, 0.5, '#A8AEB3'), mark('box', 36, 1, 6, 2, 0.5, '#A8AEB3')]),
    teil('zelle_1', 'li_ion_battery', 'Lithium-Polymer-Zelle 1', 'Zelle 1', 'box',
         x=4, y=4, w=30.5, d=99, z=2, h=10, r=2, mass=91, sortBias=-5, materials=ZELLE,
         info='5.000 mAh in einer Folientasche. Niemals einstechen, biegen oder erhitzen: '
              'Beschädigte Zellen können brennen. Pole abkleben.',
         color='#9DA6AD', marks=[mark('box', 3, 6, 24.5, 80, 2), mark('box', 6, 12, 18.5, 20, 1, '#C8423A')]),
    teil('zelle_2', 'li_ion_battery', 'Lithium-Polymer-Zelle 2', 'Zelle 2', 'box',
         x=35.5, y=4, w=30.5, d=99, z=2, h=10, r=2, mass=91, sortBias=-5, materials=ZELLE,
         info='Parallel zur ersten Zelle geschaltet, zusammen 10.000 mAh bei 3,7 Volt.',
         color='#9DA6AD', marks=[mark('box', 3, 6, 24.5, 80, 2), mark('box', 6, 12, 18.5, 20, 1, '#C8423A')]),
    teil('unterschale', 'plastic_housing', 'Gehäuse-Unterschale', 'Unterschale', 'box',
         x=0, y=0, w=70, d=140, z=0, h=8, r=9, mass=26,
         info='Wanne mit Stegen, in der Zellen und Platine liegen. Oft mit Schaumstoff gepolstert.',
         color=GEH, marks=[mark('box', 18, 132, 9, 8, 1.5), mark('box', 34, 133, 13.5, 7, 0.5)]),
]
explodiere(teile, abstand=45, abstaende={'nickel': 20, 'ladechip': 12, 'spule': 12}, nach_liste=True)
schreibe('power_bank', teile)
