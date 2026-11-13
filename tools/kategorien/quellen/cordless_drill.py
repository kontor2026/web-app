"""3D-Modell: cordless_drill. Erzeugt tools/kategorien/modelle/cordless_drill.json."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# 18-Volt-Akkuschrauber (80 × 200 × 220 mm), steht auf dem Akku. Kopf waagerecht entlang y (vorne = Bohrfutter,
# y groß), darunter der Griff mit Abzug und Drehrichtungsschalter, unten der Schiebeakku.
# Im Kopf von hinten nach vorn: Lüfterrad, Motor, Planetengetriebe, Drehmomentring, Bohrfutter. Liegende Zylinder
# (Motor, Getriebe, Ring, Futter) sind als waagerechte Scheiben gestapelt.
# Explosion: Halbschalen zur Seite (links dx < 0, rechts dx > 0), Antriebsstrang nach vorn auseinander,
# Akku nach vorn (dy > 0, so wird er auch abgezogen) mit Zellen und Schutzplatine darüber.
GEH = '#2E3338'
AKZENT = '#D9822B'
STAHL = '#9AA2A8'


def liegend(pid, comp, name, short, cx, cz, R, y0, tiefe, n, explode, mass, info, marks_oben=None, **extra):
    """Liegender Zylinder entlang y als n waagerechte Scheiben (Boxen). Nur die mittlere Scheibe hat ein Label."""
    out = []
    hs = 2 * R / n
    for i in range(n):
        z0 = cz - R + i * hs
        zm = z0 + hs / 2
        halb = math.sqrt(max(R * R - (zm - cz) ** 2, 0)) * 1.04
        e = dict(extra)
        if i != n // 2:
            e['label'] = False
        if i == n - 1 and marks_oben:
            e['marks'] = marks_oben(2 * halb)
        out.append(teil(f'{pid}_{i}', comp, name, short, 'box', x=round(cx - halb, 2), y=y0, w=round(2 * halb, 2),
                        d=tiefe, z=round(z0, 2), h=round(hs, 2), r=round(min(3, halb / 2), 2), explode=list(explode),
                        mass=round(mass / n, 2), info=info, **e))
    return out


SL = [-125, 0, 0]
SR = [160, 0, 0]

teile = [
    # linke Halbschale: Kopf, Griff, Fuß
    teil('schale_links', 'plastic_housing', 'Gehäusehälfte links', 'Schale links', 'box',
         x=12, y=5, w=28, d=135, z=150, h=70, r=6, explode=SL, mass=90, color=AKZENT,
         materials=[['pcabs', 85], ['tpe', 15]],
         info='Linke Gehäusehälfte aus glasfaserverstärktem Kunststoff. Etwa zehn Torx-Schrauben lösen, dann abheben.',
         marks=raster(8, 12, 1, 5, 14, 2.5, 0, 6, fill='#1E2226')),
    teil('schale_links_griff', 'plastic_housing', 'Gehäusehälfte links (Griff)', 'Griff links', 'box',
         x=22, y=95, w=18, d=55, z=72, h=78, r=6, explode=SL, mass=55, materials=[['pcabs', 80], ['tpe', 20]],
         color=GEH, label=False, info='Griffteil der linken Schale, mit weichem Gummi überzogen.'),
    teil('schale_links_fuss', 'plastic_housing', 'Gehäusehälfte links (Fuß)', 'Fuß links', 'box',
         x=4, y=55, w=36, d=120, z=60, h=12, r=8, explode=SL, mass=35, color=AKZENT, label=False,
         info='Fuß der linken Schale mit Führungsschiene für den Akku.'),
    # rechte Halbschale
    teil('schale_rechts', 'plastic_housing', 'Gehäusehälfte rechts', 'Schale rechts', 'box',
         x=40, y=5, w=28, d=135, z=150, h=70, r=6, explode=SR, mass=90, color=AKZENT,
         materials=[['pcabs', 85], ['tpe', 15]],
         info='Rechte Gehäusehälfte; in ihren Stegen liegen Motor und Getriebe. Kunststoff mit Glasfasern, nicht sortenrein.',
         marks=raster(6, 12, 1, 5, 14, 2.5, 0, 6, fill='#1E2226')),
    teil('schale_rechts_griff', 'plastic_housing', 'Gehäusehälfte rechts (Griff)', 'Griff rechts', 'box',
         x=40, y=95, w=18, d=55, z=72, h=78, r=6, explode=SR, mass=55, materials=[['pcabs', 80], ['tpe', 20]],
         color=GEH, label=False, info='Griffteil der rechten Schale mit Gummiüberzug.'),
    teil('schale_rechts_fuss', 'plastic_housing', 'Gehäusehälfte rechts (Fuß)', 'Fuß rechts', 'box',
         x=40, y=55, w=36, d=120, z=60, h=12, r=8, explode=SR, mass=35, color=AKZENT, label=False,
         info='Fuß der rechten Schale mit Führungsschiene für den Akku.'),
    teil('schrauben', 'plastic_housing', 'Torx-Schrauben (10 Stück)', 'Schrauben', 'cyl', material_id='steel',
         x=14, y=20, w=6, z=200, h=14, explode=[-195, 0, 0], mass=8, color='#7D858B',
         info='Halten die beiden Schalen zusammen. Man braucht einen Torx-Schraubendreher T10 oder T15.',
         marks=[mark('cyl', 1.5, 1.5, 3, fill='#4A5156')]),
    teil('planetenraeder', 'gearbox', 'Planetenräder', 'Planetenräder', 'cyl',
         x=26, y=104, w=28, z=172, h=26, explode=[0, 20, 75], mass=60, color='#B5BBC0',
         info='Kleine gehärtete Stahlzahnräder, die die schnelle Motordrehung langsam und kräftig machen. Gefettet: Handschuhe tragen.',
         marks=[mark('cyl', 9, 9, 10, fill='#7D858B'), mark('cyl', 2, 10, 8, fill='#7D858B'),
                mark('cyl', 18, 10, 8, fill='#7D858B')]),
]

# Antriebsstrang (Achse bei x = 40, z = 185)
teile += liegend('bohrfutter', 'drill_chuck', 'Schnellspannbohrfutter', 'Bohrfutter', 40, 185, 18, 154, 46, 5,
                 [0, 105, 0], 180, 'Spannt Bohrer und Bits mit drei Stahlbacken. Ganz öffnen, die Linksschraube innen '
                 'lösen, dann abschrauben.', materials=[['stahl', 85], ['pcabs', 15]], color='#3A3F44',
                 marks_oben=lambda w: raster(1, 4, 1, 6, round(max(w - 2, 1), 2), 2, 0, 6, fill='#5E656A'))
teile += liegend('drehmomentring', 'gearbox', 'Drehmomentring', 'Drehmoment', 40, 185, 27, 140, 13, 5,
                 [0, 70, 0], 30, 'Stellt ein, ab welcher Kraft die Rutschkupplung auslöst. Innen drücken Stahlfedern '
                 'auf Kugeln.', material_id='abs', materials=[['pcabs', 70], ['stahl', 30]], color=GEH,
                 marks_oben=lambda w: raster(2, 3, max(int((w - 4) // 6), 1), 1, 2, 7, 6, fill='#F2F2F2'))
teile += liegend('getriebe', 'gearbox', 'Getriebegehäuse mit Gangschalter', 'Getriebe', 40, 185, 19, 96, 44, 5,
                 [0, 35, 0], 120, 'Hält die Planetenräder; mit dem Schieber oben wählt man zwei Gänge. Zusammen mit '
                 'dem Motor herausheben.', materials=[['stahl', 55], ['pcabs', 45]], color='#5E656A',
                 marks_oben=lambda w: [mark('box', 1, 6, round(max(w - 2, 1), 2), 18, 2, '#1E2226')])
teile += liegend('motor', 'electric_motor', 'Gleichstrommotor', 'Motor', 40, 185, 18, 36, 58, 5,
                 [0, 0, 0], 230, 'Bürstenmotor mit Kupferwicklung und Ferritmagneten. Drähte abschneiden; viel Kupfer '
                 'und Stahl.', materials=[['stahl', 45], ['kupfer', 25], ['ferrit', 22], ['graphit', 5], ['pcabs', 3]],
                 color=STAHL, marks_oben=lambda w: raster(1, 6, 1, 4, round(max(w - 2, 1), 2), 2, 0, 12, fill='#7D858B'))
teile += [
    teil('kohlebuersten', 'electric_motor', 'Kohlebürsten', 'Kohlebürsten', 'box', material_id='mixed_electronics',
         x=30, y=26, w=20, d=8, z=196, h=8, r=2, explode=[0, -40, 30], mass=6, color='#2B2F33',
         materials=[['graphit', 70], ['kupfer', 20], ['stahl', 10]],
         info='Zwei Graphitstücke drücken mit Federn auf den drehenden Kommutator und übertragen den Strom. Nutzen sich ab.',
         marks=[mark('box', 2, 2, 6, 4, 1, '#B87333'), mark('box', 12, 2, 6, 4, 1, '#B87333')]),
    teil('luefter', 'electric_motor', 'Lüfterrad', 'Lüfter', 'box', material_id='abs',
         x=23, y=12, w=34, d=8, z=168, h=34, r=12, explode=[0, -40, 0], mass=6, color='#3A3F44',
         materials=[['pcabs', 100]],
         info='Sitzt auf der Motorwelle und saugt Kühlluft durch die Schlitze im Gehäuse.',
         marks=raster(4, 2, 6, 1, 2, 4, 4.6, fill='#1E2226')),
    # Griff
    teil('richtung', 'plastic_housing', 'Drehrichtungsschalter', 'Rechts/Links', 'box',
         x=18, y=110, w=44, d=8, z=140, h=8, r=3, explode=[0, 0, 52], mass=4, color='#C0392B',
         info='Schieber quer durch den Griff: von links gedrückt rechtsherum, von rechts linksherum. Steckt nur.'),
    teil('schalter', 'circuit_board', 'Schalter mit Drehzahlregler', 'Schalter', 'box', material_id='mixed_electronics',
         x=27, y=104, w=26, d=40, z=100, h=38, r=3, explode=[0, 0, 25], mass=30,
         materials=[['pcabs', 40], ['kupfer', 25], ['fr4', 15], ['chip', 10], ['kontakte', 10]], color='#3A3F44',
         info='Elektronischer Schalter. Regelt die Drehzahl mit einem Leistungstransistor auf einem Kühlblech.',
         marks=[mark('box', 4, 6, 18, 10, 2, '#9AA2A8'), mark('box', 6, 24, 14, 10, 1, '#1E2226')]),
    teil('abzug', 'plastic_housing', 'Abzug', 'Abzug', 'box',
         x=32, y=144, w=16, d=20, z=112, h=26, r=5, explode=[0, 40, 25], mass=8, color=GEH,
         info='Je weiter man drückt, desto schneller dreht der Motor. Steckt auf dem Stößel des Schalters.',
         marks=[mark('box', 3, 12, 10, 6, 2, '#4A5156')]),
    teil('led', 'circuit_board', 'LED-Arbeitslicht', 'LED', 'box', material_id='mixed_electronics',
         x=33, y=160, w=14, d=10, z=63, h=6, r=2, explode=[0, 40, 60], mass=2,
         materials=[['led', 40], ['fr4', 30], ['kupfer', 30]], color='#E8E4C8',
         info='Kleine LED im Fuß, leuchtet beim Drücken des Abzugs auf die Bohrstelle.',
         marks=[mark('cyl', 4, 2, 6, fill='#FFF6B0')]),
    # Akku (nach vorn abgezogen)
    teil('akku_platine', 'circuit_board', 'Akku-Schutzplatine', 'Akku-Platine', 'box',
         x=10, y=70, w=60, d=80, z=32, h=1.6, r=2, explode=[0, 200, 80], mass=15, color='#2E6B45',
         info='Überwacht jede Zelle und schaltet ab, bevor der Akku zu leer, zu voll oder zu heiß wird.',
         marks=raster(40, 4, 4, 1, 4, 3, 5, fill='#7FD07F') + [mark('box', 6, 30, 30, 20, 1, '#22272B'),
                                                             mark('box', 42, 40, 12, 10, 1, '#22272B')]),
    teil('akku_zellen', 'battery_pack', 'Akkuzellen (5 × 18650)', 'Akkuzellen', 'box',
         x=7, y=65, w=65, d=95, z=8, h=20, r=3, explode=[0, 200, 72], mass=230,
         materials=[['nmc', 40], ['graphit', 18], ['elektrolyt', 12], ['stahl', 15], ['kupfer', 8], ['alu', 7]],
         color='#3F6E9C',
         info='Fünf runde Lithium-Ionen-Zellen in Reihe, zusammen 18 Volt. Niemals öffnen oder anbohren: Brandgefahr.',
         marks=raster(2, 1.5, 1, 5, 61, 17, 0, 19, r=8, fill='#5E8CB8') + raster(30, 3, 1, 5, 6, 13, 0, 19, fill='#B9BEC2')),
    teil('akku_kontakte', 'battery_pack', 'Akku-Kontaktblock', 'Kontakte', 'box', material_id='copper',
         x=28, y=92, w=24, d=36, z=60, h=10, r=2, explode=[95, 200, 0], mass=12,
         materials=[['kupfer', 50], ['kontakte', 10], ['pcabs', 40]], color='#3A3F44',
         info='Federnde Kupferkontakte, über die der Strom ins Gerät fließt. Nicht mit Metall überbrücken.',
         marks=raster(4, 4, 4, 1, 2, 28, 5, fill='#C9A24B')),
    teil('akku_gehaeuse', 'battery_pack', 'Akkugehäuse mit Ladeanzeige', 'Akkugehäuse', 'box', material_id='abs',
         x=0, y=55, w=80, d=120, z=0, h=60, r=8, explode=[0, 200, 0], mass=120,
         materials=[['pcabs', 80], ['tpe', 10], ['kupfer', 5], ['stahl', 5]], color=GEH,
         info='Kunststoffgehäuse mit Führungsschienen. Den ganzen Akku abschieben und ungeöffnet zur Batteriesammlung bringen.',
         marks=[mark('box', 6, 8, 4, 104, 2, '#4A5156'), mark('box', 70, 8, 4, 104, 2, '#4A5156'),
                mark('box', 30, 100, 20, 12, 2, AKZENT)] + raster(34, 112, 3, 1, 3, 3, 5, fill='#7FD07F')),
    teil('entriegelung', 'battery_pack', 'Entriegelungstaste', 'Entriegelung', 'box', material_id='abs',
         x=28, y=172, w=24, d=8, z=36, h=16, r=3, explode=[0, 220, 0], mass=4, materials=[['pcabs', 100]],
         color=AKZENT, info='Drücken und den Akku nach vorn abziehen. Eine Feder lässt die Taste wieder einrasten.'),
]

skaliere_masse(teile, oid='cordless_drill')
schreibe('cordless_drill', teile)
