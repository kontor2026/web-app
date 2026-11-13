"""3D-Modell: external_hard_drive. Erzeugt tools/kategorien/modelle/external_hard_drive.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Typische externe 2,5-Zoll-Festplatte, 80 × 115 × 20 mm. Im Kunststoffgehäuse liegt ein 2,5-Zoll-Laufwerk
# (70 × 100 × 9,5 mm), vorne (y groß) die USB-Brückenplatine mit Micro-B-Buchse.
# Laufwerk aufgeschlüsselt: Deckel, Kopfarm, Scheibe, Spindelmotor, Schwingspulen-Magnet, Grundplatte, Laufwerksplatine.
GEH = '#2B2F33'
ALU = '#C9CED2'
CHIP = '#3F4547'
teile = [
    teil('oberschale', 'plastic_housing', 'Gehäuse-Oberteil', 'Oberteil', 'box',
         x=0, y=0, w=80, d=115, z=10, h=10, r=8, mass=42, color=GEH,
         info='Kunststoffhälfte, nur mit Rastnasen eingeclipst. Mit einem Plektrum an der Fuge entlang aufhebeln.',
         marks=[mark('cyl', 37, 105, 3, fill='#7FC8F0')]),
    teil('hdd_deckel', 'hard_drive', 'Laufwerksdeckel', 'Deckel', 'box', material_id='steel',
         x=5, y=4, w=70, d=100, z=13, h=0.6, r=3, mass=12, materials=[['stahl', 95], ['folien', 5]], color='#B9BEC2',
         info='Dünnes Stahlblech, mit Torx-Schrauben verschraubt (eine steckt oft unter dem Etikett). Innen ist es staubfrei.',
         marks=[mark('box', 6, 50, 58, 42, 2, '#E8E8E2')] + [mark('cyl', x, y, 2.5, fill='#5E656A')
                                                              for x, y in ((2, 2), (65.5, 2), (2, 95.5), (65.5, 95.5), (32.2, 31.7))]),
    teil('kopfarm', 'hard_drive', 'Kopfarm mit Lese-/Schreibkopf', 'Kopfarm', 'box', material_id='aluminium',
         x=42, y=36, w=10, d=50, z=10.5, h=1.5, r=2, mass=4, materials=[['alu', 80], ['kupfer', 15], ['chip', 5]], color='#9BA3A8',
         info='Schwenkt in Millisekunden über die Scheibe. Der Kopf an der Spitze schwebt nur wenige Nanometer über der Oberfläche.',
         marks=[mark('box', 3.5, 1, 3, 4, 0.5, '#5E656A'), mark('cyl', 1, 38, 8, fill='#B87333')]),
    teil('scheibe', 'hard_drive', 'Magnetscheibe (Platter)', 'Scheibe', 'cyl', material_id='aluminium',
         x=6, y=4.5, w=65, z=9, h=1.3, mass=9, materials=[['alu', 92], ['nickel', 8]], color='#D9DDE0',
         info='Aluminiumscheibe mit hauchdünner Magnetschicht, dreht sich 5.400-mal pro Minute. Zum Datenschutz zerkratzen oder verbiegen.',
         marks=[mark('cyl', 26, 26, 13, fill='#9BA3A8')]),
    teil('spindel', 'hard_drive', 'Spindelmotor', 'Spindelmotor', 'cyl', material_id='mixed_electronics',
         x=26, y=24.5, w=25, z=5.5, h=3.5, mass=14, materials=[['stahl', 40], ['kupfer', 25], ['ndfeb', 15], ['alu', 20]],
         color='#7C858C', info='Flacher Motor mit Kupferspulen und Ringmagnet, dreht die Scheibe. Steckt fest in der Grundplatte.',
         marks=[mark('cyl', 7.5, 7.5, 10, fill='#5E656A')]),
    teil('magnet', 'hard_drive', 'Schwingspulen-Magnet', 'Magnet', 'box', material_id='mixed_electronics',
         x=50, y=78, w=21, d=20, z=6, h=4, r=3, mass=10, materials=[['ndfeb', 55], ['stahl', 45]], color='#8A9196',
         info='Sehr starker Neodym-Magnet zwischen zwei Stahlplatten, er bewegt den Kopfarm. Finger aufpassen, er schnappt kräftig zu.'),
    teil('grundplatte', 'hard_drive', 'Laufwerks-Grundplatte', 'Grundplatte', 'box', material_id='aluminium',
         x=5, y=4, w=70, d=100, z=4.5, h=8.5, r=3, mass=42, materials=[['alu', 100]], color=ALU,
         info='Gegossenes Aluminium, trägt Motor, Arm und Magnet. Ausgeschlachtet ist sie gut verwertbares Altmetall.',
         marks=[mark('cyl', 1, 0.5, 67, fill='#AEB4B8'), mark('box', 38, 70, 30, 28, 2, '#AEB4B8')]),
    teil('hdd_platine', 'circuit_board', 'Laufwerksplatine', 'Laufwerksplatine', 'box',
         x=6, y=48, w=68, d=54, z=3.5, h=1, r=2, mass=9, color='#2E6B45',
         info='Steuert Motor und Kopf. An der Unterseite des Laufwerks verschraubt, mit SATA-Stecker zur Brückenplatine.',
         marks=[mark('box', 10, 12, 14, 14, 0.5, CHIP), mark('box', 30, 14, 10, 10, 0.5, CHIP),
                mark('box', 8, 47, 52, 6, 0.5, '#D4AF37')]),
    teil('usb_buchse', 'circuit_board', 'USB-Micro-B-Buchse', 'USB-Buchse', 'box', material_id='steel',
         x=31, y=108, w=12, d=7.5, z=5.2, h=3.5, r=0.5, mass=1.5, sortBias=12, materials=[['stahl', 70], ['kontakte', 15], ['pcabs', 15]],
         color='#C9CED2', info='Breite USB-3-Buchse für das Kabel zum Computer. Angelötet, wackelt sie oft nach Jahren.',
         marks=[mark('box', 1.5, 4, 9, 2, 0.5, '#2A2E31')]),
    teil('bruecke', 'circuit_board', 'USB-SATA-Brückenplatine', 'Brückenplatine', 'box',
         x=8, y=104, w=64, d=10, z=4, h=1.2, r=1, mass=6, color='#2E6B45',
         info='Wandelt USB in SATA um. Ohne sie lässt sich das Laufwerk direkt in einen Laptop einbauen.',
         marks=[mark('box', 6, 2, 7, 6, 0.3, CHIP), mark('box', 50, 2, 8, 6, 0.3, CHIP)]),
    teil('puffer_l', 'plastic_housing', 'Gummipuffer', 'Gummipuffer', 'box', material_id='silicone',
         x=1, y=20, w=4, d=60, z=4, h=8, r=1.5, mass=1.5, materials=[['gummi', 100]], color='#4A5156', sortBias=-8,
         info='Weiche Gummistreifen links und rechts. Sie dämpfen Stöße, damit der Kopf die Scheibe nicht berührt.'),
    teil('puffer_r', 'plastic_housing', 'Gummipuffer', 'Gummipuffer', 'box', material_id='silicone',
         x=75, y=20, w=4, d=60, z=4, h=8, r=1.5, mass=1.5, materials=[['gummi', 100]], color='#4A5156', sortBias=-8, label=False,
         info='Zweiter Gummipuffer auf der anderen Seite.'),
    teil('unterschale', 'plastic_housing', 'Gehäuse-Unterteil', 'Unterteil', 'box',
         x=0, y=0, w=80, d=115, z=0, h=10, r=8, mass=45, color=GEH,
         info='Wanne mit Gummifüßen, das Laufwerk liegt in Gummi-Puffern. Kunststoff ohne Elektronik.',
         marks=[mark('box', 4, 3, 72, 102, 6, '#23272A')]),
]

explodiere(teile, abstand=50, nach_liste=True)
skaliere_masse(teile, oid='external_hard_drive')
schreibe('external_hard_drive', teile)
