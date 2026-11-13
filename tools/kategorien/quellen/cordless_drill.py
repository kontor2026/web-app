"""3D-Modell: cordless_drill. Erzeugt tools/kategorien/modelle/cordless_drill.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# 18-Volt-Akkuschrauber (80 × 200 × 220 mm), steht auf dem Akku. Kopf waagerecht entlang y (vorne = Bohrfutter,
# y groß), darunter der Griff mit Schalter und Abzug, unten der Schiebeakku. Im Kopf von hinten nach vorn:
# Motor, Planetengetriebe, Drehmomentring, Bohrfutter. Das Kunststoffgehäuse besteht aus zwei Halbschalen (x 40).
# Explosion: Halbschalen zur Seite (links dx < 0, rechts dx > 0, je diagonal, damit sie nichts verdecken),
# Antriebsstrang nach vorn auseinandergezogen, Planetenräder aus dem Getriebe nach oben, Akku nach hinten
# (dy < 0) mit Zellen und Schutzplatine darüber.
GEH = '#2E3338'
AKZENT = '#D9822B'
STAHL = '#9AA2A8'

teile = [
    teil('schale_links_kopf', 'plastic_housing', 'Gehäusehälfte links (Kopf)', 'Halbschale links', 'box',
         x=12, y=5, w=28, d=135, z=150, h=70, r=10, explode=[-80, 80, 0], mass=90, color=AKZENT,
         info='Linke Gehäusehälfte aus Kunststoff mit Gummi-Einlagen. Etwa zehn Torx-Schrauben lösen, dann abheben.',
         marks=raster(6, 10, 1, 4, 16, 3, 0, 8, fill='#1E2226')),
    teil('schale_links_griff', 'plastic_housing', 'Gehäusehälfte links (Griff)', 'Griff links', 'box',
         x=22, y=95, w=18, d=55, z=60, h=90, r=6, explode=[-80, 80, 0], mass=60, materials=[['pcabs', 85], ['tpe', 15]], color=GEH,
         label=False, info='Griffteil der linken Schale, mit weichem Gummi überzogen. Gehört zur Kopfschale.'),
    teil('schale_rechts_kopf', 'plastic_housing', 'Gehäusehälfte rechts (Kopf)', 'Halbschale rechts', 'box',
         x=40, y=5, w=28, d=135, z=150, h=70, r=10, explode=[80, -80, 0], mass=90, color=AKZENT,
         info='Rechte Gehäusehälfte; in ihren Stegen liegen Motor und Getriebe. Kunststoff mit Glasfasern, nicht sortenrein.',
         marks=raster(6, 10, 1, 4, 16, 3, 0, 8, fill='#1E2226')),
    teil('schale_rechts_griff', 'plastic_housing', 'Gehäusehälfte rechts (Griff)', 'Griff rechts', 'box',
         x=40, y=95, w=18, d=55, z=60, h=90, r=6, explode=[80, -80, 0], mass=60, materials=[['pcabs', 85], ['tpe', 15]], color=GEH,
         label=False, info='Griffteil der rechten Schale mit Gummiüberzug.'),
    teil('planetenraeder', 'gearbox', 'Planetenräder', 'Planetenräder', 'cyl',
         x=26, y=104, w=28, z=170, h=30, explode=[0, 20, 80], mass=60,
         info='Kleine gehärtete Stahlzahnräder, die die schnelle Motordrehung langsam und kräftig machen. Gefettet: Handschuhe tragen.',
         color='#B5BBC0', marks=[mark('cyl', 9, 9, 10, fill='#7D858B'), mark('cyl', 2, 10, 8, fill='#7D858B'),
                                 mark('cyl', 18, 10, 8, fill='#7D858B')]),
    teil('bohrfutter', 'drill_chuck', 'Schnellspannbohrfutter', 'Bohrfutter', 'box',
         x=21, y=152, w=38, d=48, z=166, h=38, r=10, explode=[0, 75, 0], mass=180, materials=[['stahl', 85], ['pcabs', 15]],
         color='#3A3F44',
         info='Spannt Bohrer und Bits mit drei Stahlbacken. Ganz öffnen, die Linksschraube innen lösen, dann abschrauben.',
         marks=[mark('box', 4, 34, 30, 14, 6, '#5E656A')]),
    teil('drehmomentring', 'gearbox', 'Drehmomentring', 'Drehmoment', 'box', material_id='abs',
         x=12, y=140, w=56, d=12, z=157, h=56, r=6, explode=[0, 45, 0], mass=30, materials=[['pcabs', 70], ['stahl', 30]],
         color=GEH,
         info='Stellt ein, ab welcher Kraft die Rutschkupplung auslöst. Innen drücken Stahlfedern auf Kugeln.',
         marks=raster(4, 2, 6, 1, 4, 8, 9, fill='#F2F2F2')),
    teil('getriebe', 'gearbox', 'Getriebegehäuse mit Gangschalter', 'Getriebe', 'box',
         x=22, y=95, w=36, d=45, z=166, h=38, r=10, explode=[0, 20, 0], mass=120, materials=[['stahl', 55], ['pcabs', 45]],
         color='#5E656A',
         info='Hält die Planetenräder; mit dem Schieber oben wählt man zwei Gänge. Mit dem Motor zusammen herausheben.',
         marks=[mark('box', 10, 10, 16, 20, 4, '#1E2226')]),
    teil('motor', 'electric_motor', 'Gleichstrommotor', 'Motor', 'box',
         x=22, y=35, w=36, d=60, z=167, h=36, r=12, explode=[0, -15, 0], mass=230,
         materials=[['stahl', 45], ['kupfer', 25], ['ferrit', 22], ['graphit', 5], ['pcabs', 3]], color=STAHL,
         info='Bürstenmotor mit Kupferwicklung und Ferritmagneten. Drähte abschneiden; viel Kupfer und Stahl.',
         marks=[mark('box', 4, 4, 28, 10, 4, '#B87333')] + raster(6, 20, 4, 1, 3, 30, 7, fill='#7D858B')),
    teil('abzug', 'plastic_housing', 'Abzug', 'Abzug', 'box',
         x=32, y=148, w=16, d=16, z=118, h=24, r=5, explode=[0, 30, 0], mass=8, color=GEH,
         info='Je weiter man drückt, desto schneller dreht der Motor. Steckt auf dem Schalter.'),
    teil('schalter', 'circuit_board', 'Schalter mit Drehzahlregler', 'Schalter', 'box', material_id='mixed_electronics',
         x=27, y=105, w=26, d=43, z=110, h=38, r=3, mass=30,
         materials=[['pcabs', 40], ['kupfer', 25], ['fr4', 15], ['chip', 10], ['kontakte', 10]], color='#3A3F44',
         info='Elektronischer Schalter mit Rechts-/Linkslauf-Schieber. Regelt die Drehzahl mit einem Leistungstransistor.',
         marks=[mark('box', 4, 4, 18, 8, 2, '#C0392B')]),
    teil('akku_platine', 'circuit_board', 'Akku-Schutzplatine', 'Akku-Platine', 'box',
         x=10, y=70, w=60, d=80, z=32, h=1.6, r=2, mass=15, color='#2E6B45',
         info='Überwacht jede Zelle und schaltet ab, bevor der Akku zu leer, zu voll oder zu heiß wird. Mit Ladestandsanzeige.',
         marks=raster(40, 4, 4, 1, 4, 3, 5, fill='#7FD07F') + [mark('box', 6, 30, 30, 20, 1, '#22272B')]),
    teil('akku_zellen', 'battery_pack', 'Akkuzellen (5 × 18650)', 'Akkuzellen', 'box',
         x=7, y=65, w=65, d=95, z=8, h=20, r=3, mass=230,
         materials=[['nmc', 40], ['graphit', 18], ['elektrolyt', 12], ['stahl', 15], ['kupfer', 8], ['alu', 7]], color='#3F6E9C',
         info='Fünf runde Lithium-Ionen-Zellen in Reihe, zusammen 18 Volt. Niemals öffnen oder anbohren: Brandgefahr.',
         marks=raster(2, 1.5, 1, 5, 61, 17, 0, 19, r=8, fill='#5E8CB8')),
    teil('akku_gehaeuse', 'battery_pack', 'Akkugehäuse', 'Akkugehäuse', 'box', material_id='abs',
         x=0, y=55, w=80, d=120, z=0, h=60, r=8, mass=120, materials=[['pcabs', 80], ['tpe', 10], ['kupfer', 5], ['stahl', 5]],
         color=GEH,
         info='Kunststoffgehäuse mit Führungsschienen und Kontakten. Den ganzen Akku vom Gerät abschieben und ungeöffnet zur Batteriesammlung bringen.',
         marks=[mark('box', 20, 10, 40, 100, 4, '#3A3F44'), mark('box', 32, 100, 16, 12, 2, AKZENT)]),
]

akku = [p for p in teile if p['id'] in ('akku_platine', 'akku_zellen', 'akku_gehaeuse')]
explodiere(akku, abstand=25, fest=('akku_gehaeuse',))
for p in akku:
    p['explode'][1] = -200
explodiere([p for p in teile if p['id'] == 'schalter'], abstand=25)
skaliere_masse(teile, oid='cordless_drill')
schreibe('cordless_drill', teile)
