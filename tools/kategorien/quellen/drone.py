"""3D-Modell: drone. Erzeugt tools/kategorien/modelle/drone.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Quadrocopter mit Kamera (300 × 300 × 90 mm über die Propeller gemessen). Weil nur achsparallele Formen gehen,
# ist der Rahmen ein H: zwei Querarme (vorne y ≈ 235, hinten y ≈ 65) durch den Rumpf, Motoren an den Enden.
# Die Propeller bleiben zufällig stehen: hinten quer (x), vorne längs (y). Kamera mit Gimbal vorne unter dem Rumpf.
# Explosion (nach_liste): Unterschale unten, darüber Arme, Flugsteuerung, Akku, Oberschale, Motoren und ganz
# oben die Propeller. Die Kamera wird nach vorn (dy > 0) abgezogen.
GEH = '#3A3F44'
PROP = '#2B2F33'
MX = (65, 235)       # Motormitten x
MY = (65, 235)       # Motormitten y: hinten, vorne
ZA, ZM, ZP = 42, 52, 76  # Unterkante Arme, Motoren, Propeller

PROP_INFO = ('Leichter Kunststoffpropeller (zwei Blätter). Gegen den Uhrzeigersinn drücken und drehen, dann abnehmen. '
             'Kanten sind scharf: Finger weg, solange die Motoren laufen.')
MOTOR_MAT = [['kupfer', 30], ['ndfeb', 25], ['stahl', 25], ['alu', 20]]
MOTOR_INFO = 'Bürstenloser Motor: Kupferspulen innen, Neodym-Magnete in der drehenden Glocke. Mit vier Schrauben am Arm.'

teile = [
    teil('propeller_hl', 'propellers', 'Propeller hinten links', 'Propeller', 'box',
         x=0, y=MY[0] - 6, w=130, d=12, z=ZP, h=6, r=6, mass=6, color=PROP, info=PROP_INFO,
         marks=[mark('cyl', 59, 0, 12, fill='#9AA2A8')]),
    teil('propeller_hr', 'propellers', 'Propeller hinten rechts', 'Propeller', 'box',
         x=170, y=MY[0] - 6, w=130, d=12, z=ZP, h=6, r=6, mass=6, color=PROP, info=PROP_INFO, label=False,
         marks=[mark('cyl', 59, 0, 12, fill='#9AA2A8')]),
    teil('propeller_vl', 'propellers', 'Propeller vorne links', 'Propeller', 'box',
         x=MX[0] - 6, y=170, w=12, d=130, z=ZP, h=6, r=6, mass=6, color=PROP, info=PROP_INFO, label=False,
         marks=[mark('cyl', 0, 59, 12, fill='#9AA2A8')]),
    teil('propeller_vr', 'propellers', 'Propeller vorne rechts', 'Propeller', 'box',
         x=MX[1] - 6, y=170, w=12, d=130, z=ZP, h=6, r=6, mass=6, color=PROP, info=PROP_INFO, label=False,
         marks=[mark('cyl', 0, 59, 12, fill='#9AA2A8')]),
] + [
    teil(f'motor_{n}', 'electric_motor', f'Motor {name}', 'Motor', 'cyl',
         x=mx - 14, y=my - 14, w=28, z=ZM, h=24, mass=30, materials=MOTOR_MAT, color='#9AA2A8', info=MOTOR_INFO,
         label=(n == 'hl'), marks=[mark('cyl', 4, 4, 20, fill='#5E656A'), mark('cyl', 11, 11, 6, fill='#C9CED2')])
    for n, name, mx, my in (('hl', 'hinten links', MX[0], MY[0]), ('hr', 'hinten rechts', MX[1], MY[0]),
                            ('vl', 'vorne links', MX[0], MY[1]), ('vr', 'vorne rechts', MX[1], MY[1]))
] + [
    teil('oberschale', 'plastic_housing', 'Rumpf-Oberschale', 'Oberschale', 'box',
         x=105, y=40, w=90, d=220, z=40, h=18, r=14, mass=45, color=GEH,
         info='Kunststoffdeckel des Rumpfs mit Akkuschacht und Statuslicht. Schrauben sitzen unten, dann vorsichtig aufclipsen.',
         marks=[mark('box', 12, 105, 66, 105, 6, '#2B2F33'), mark('cyl', 40, 20, 10, fill='#7FD07F')]),
    teil('akku', 'li_ion_battery', 'Lithium-Polymer-Akku', 'Akku', 'box',
         x=118, y=148, w=64, d=100, z=30, h=26, r=4, mass=200,
         materials=[['lco', 38], ['graphit', 20], ['elektrolyt', 15], ['alu', 10], ['kupfer', 8], ['pcabs', 9]], color='#2B2F33',
         info='Flugakku mit 11 Volt. Nach hinten aus dem Rumpf ziehen. Aufgebläht oder beschädigt nie mehr laden; Pole abkleben und zur Sammelstelle.',
         marks=[mark('box', 6, 10, 52, 70, 3, '#3F6E9C'), raster(8, 88, 4, 1, 8, 6, 12, fill='#7FD07F')[0]]),
    teil('flugsteuerung', 'circuit_board', 'Flugsteuerung mit Motorreglern', 'Flugsteuerung', 'box',
         x=112, y=76, w=76, d=70, z=24, h=1.6, r=3, mass=25, color='#2E6B45',
         materials=[['fr4', 45], ['kupfer', 22], ['chip', 25], ['lot', 8]],
         info='Hält die Drohne mit Lagesensoren, GPS und Funkchip in der Luft und steuert die vier Motoren. Enthält Gold und Kupfer.',
         marks=[mark('box', 28, 25, 20, 20, 1, '#22272B')] + raster(4, 4, 2, 2, 10, 10, 58, 52, fill='#22272B')),
    teil('arm_hinten', 'plastic_housing', 'Arm hinten', 'Arm hinten', 'box',
         x=MX[0] - 10, y=MY[0] - 7, w=190, d=14, z=ZA, h=10, r=5, mass=30, material_id='pc',
         materials=[['pcabs', 100]], color=GEH,
         info='Steifer Kunststoffarm mit den Motorkabeln innen. Faltbar, mit einem Stahlstift im Gelenk.'),
    teil('arm_vorne', 'plastic_housing', 'Arm vorne', 'Arm vorne', 'box',
         x=MX[0] - 10, y=MY[1] - 7, w=190, d=14, z=ZA, h=10, r=5, mass=30, material_id='pc',
         materials=[['pcabs', 100]], color=GEH,
         info='Vorderer Arm, baugleich mit dem hinteren. Kabel vor dem Abschrauben ablöten oder abziehen.'),
    teil('unterschale', 'plastic_housing', 'Rumpf-Unterschale', 'Unterschale', 'box',
         x=105, y=40, w=90, d=220, z=12, h=28, r=14, mass=50, color=GEH,
         info='Bodenteil des Rumpfs mit Abstandssensoren und Landefüßen. Kunststoff, kommt mit in die Elektro-Sammlung.',
         marks=[mark('cyl', 30, 60, 12, fill='#1E2226'), mark('cyl', 48, 60, 12, fill='#1E2226')]),
    teil('kamera', 'camera_lens_unit', 'Kamera mit Gimbal', 'Kamera', 'box',
         x=130, y=240, w=40, d=40, z=0, h=30, r=6, explode=[0, 60, 0], mass=50,
         materials=[['alu', 30], ['chip', 20], ['glas', 15], ['kupfer', 15], ['ndfeb', 10], ['pcabs', 10]], color='#2B2F33',
         info='Kamera mit Linsen und Bildsensor, die drei kleine Motoren (Gimbal) ruhig halten. Flachbandkabel vorsichtig abziehen.',
         marks=[mark('cyl', 12, 22, 16, fill='#1E2226'), mark('cyl', 15, 25, 10, fill='#3D5A80')]),
]

explodiere(teile, abstand=25, nach_liste=True, abstaende={'flugsteuerung': 20},
           gruppen=[[p['id'] for p in teile if p['id'].startswith('propeller')],
                    [p['id'] for p in teile if p['id'].startswith('motor')]])
skaliere_masse(teile, oid='drone')
schreibe('drone', teile)
