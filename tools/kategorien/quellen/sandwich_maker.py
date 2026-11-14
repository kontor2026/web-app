"""3D-Modell: sandwich_maker. Erzeugt tools/kategorien/modelle/sandwich_maker.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Sandwichmaker, zugeklappt: Scharnier hinten (y = 0), Verschlussgriff vorne (y = 240).
# Zwei Schalen mit je einer beschichteten Backplatte und einem Rohrheizkörper.
# Explosion nach Liste: Bodenplatte bleibt, darüber Unterschale, Thermostat, untere Heizung und Platte,
# obere Platte, obere Heizung, Oberschale. Verschluss nach vorne, Scharnier nach hinten, Kabel nach rechts.

def platte(id, name, short, z):
    return teil(id, 'nonstick_plates', name, short, 'box', x=15, y=20, w=200, d=200, z=z, h=12, r=20, mass=300,
                materials=[['alu', 97], ['ptfe', 3]],
                info='Aluminiumguss mit Antihaftbeschichtung (PTFE) und zwei dreieckigen Mulden. Von innen mit vier Schrauben an der Schale befestigt.',
                color='#3A3F44', marks=[mark('box', 10, 10, 85, 180, 8, fill='#2A2D30'), mark('box', 105, 10, 85, 180, 8, fill='#2A2D30')])


HEIZ_INFO = ('Rohrheizkörper: Heizdraht in Keramikpulver in einem Stahlrohr, als U auf die Rückseite der Platte gepresst. '
             'Erst ganz abkühlen lassen.')


def heizung(id, name, short, z):
    """U-förmiges Heizrohr aus drei geraden Stücken (linker Schenkel trägt die Nummer)."""
    farbe, mats = '#9AA2A6', [['stahl', 55], ['nichrom', 20], ['keramik', 25]]
    return [
        teil(f'{id}', 'heating_element', name, short, 'box', x=30, y=30, w=10, d=180, z=z, h=8, r=5, form='liegend_y', mass=30,
             materials=mats, info=HEIZ_INFO, color=farbe, marks=[mark('box', 2, 0, 6, 180, 3, '#B5BBC0')]),
        teil(f'{id}_b', 'heating_element', name, short, 'box', x=40, y=30, w=150, d=10, z=z, h=8, r=5, form='liegend_x', mass=25,
             materials=mats, info=HEIZ_INFO, color=farbe, label=False, marks=[mark('box', 0, 2, 150, 6, 3, '#B5BBC0')]),
        teil(f'{id}_c', 'heating_element', name, short, 'box', x=190, y=30, w=10, d=180, z=z, h=8, r=5, form='liegend_y', mass=30,
             materials=mats, info=HEIZ_INFO, color=farbe, label=False,
             marks=[mark('box', 2, 0, 6, 180, 3, '#B5BBC0'), mark('box', 1, 170, 8, 10, 2, '#C4672D')]),
    ]


teile = [
    teil('griff', 'plastic_housing', 'Tragegriff', 'Griff', 'box',
         x=80, y=196, w=70, d=40, z=90, h=10, r=8, mass=30, material_id='phenolic_resin', sortBias=200,
         materials=[['phenolharz', 60], ['pcabs', 40]], color='#1E2226',
         marks=[mark('box', 8, 26, 54, 8, 4, fill='#3C4248')],
         info='Griff vorne auf der Oberschale. Er bleibt kühl, weil er aus hitzefestem Kunststoff ist und Abstand zur Platte hat.'),
    teil('oberschale', 'plastic_housing', 'Obere Gehäuseschale', 'Oberschale', 'box',
         x=0, y=10, w=230, d=220, z=50, h=40, r=40, mass=180, material_id='phenolic_resin', materials=[['phenolharz', 60], ['pcabs', 40]],
         info='Hitzefeste Kunststoffschale mit Kontrollleuchten. Die Schrauben sitzen innen unter der Backplatte.',
         color='#2E3338', marks=[mark('box', 20, 16, 190, 150, 30, fill='#3C4248'), mark('box', 30, 26, 170, 4, 2, fill='#4A5158'),
                                 mark('box', 18, 172, 50, 18, 6, fill='#1E2226'), mark('cyl', 28, 177, 8, fill='#E74C3C'),
                                 mark('cyl', 50, 177, 8, fill='#2ECC71')]),
    teil('lampen', 'thermostat', 'Kontrollleuchten', 'Leuchten', 'box', material_id='mixed_electronics',
         x=26, y=188, w=30, d=10, z=80, h=8, r=2, mass=4, materials=[['glas', 40], ['kupfer', 30], ['pcabs', 30]],
         color='#E8E2C8', marks=[mark('cyl', 2, 1, 8, fill='#E74C3C'), mark('cyl', 20, 1, 8, fill='#2ECC71')],
         info='Rot heißt Strom an, grün heißt heiß genug. Zwei kleine Lämpchen hinter durchsichtigen Kappen.'),
    *heizung('heizung_oben', 'Heizelement oben', 'Heizung oben', 62),
    platte('platte_oben', 'Backplatte oben', 'Platte oben', 50),
    platte('platte_unten', 'Backplatte unten', 'Platte unten', 38),
    *heizung('heizung_unten', 'Heizelement unten', 'Heizung unten', 30),
    teil('thermostat', 'thermostat', 'Thermostat (Bimetall)', 'Thermostat', 'box',
         x=160, y=100, w=30, d=25, z=24, h=8, r=3, mass=15, materials=[['bimetall', 40], ['keramik', 25], ['kupfer', 20], ['kontakte', 15]],
         info='Eine Bimetallscheibe schaltet die Heizung bei etwa 200 Grad ab und lässt die grüne Lampe leuchten. Sitzt unter der unteren Platte.',
         color='#B8BEC4', marks=[mark('cyl', 9, 6, 13, fill='#D5DADE')]),
    teil('unterschale', 'plastic_housing', 'Untere Gehäuseschale', 'Unterschale', 'box',
         x=0, y=10, w=230, d=220, z=8, h=42, r=40, mass=180, material_id='phenolic_resin', materials=[['phenolharz', 60], ['pcabs', 40]],
         info='Hitzefeste Schale, in der Platte, Heizung und Thermostat sitzen. Erst nach dem Abschrauben der Bodenplatte zugänglich.',
         color='#2E3338'),
    teil('bodenplatte', 'plastic_housing', 'Bodenplatte mit Füßen', 'Bodenplatte', 'box',
         x=5, y=15, w=220, d=210, z=0, h=8, r=36, mass=100, materials=[['stahl', 85], ['gummi', 15]],
         info='Stahlblech mit Gummifüßen und Lüftungsschlitzen. Nach dem Lösen der Schrauben kommt man an den Thermostat.',
         color='#7C858C', marks=raster(14, 14, 2, 2, 16, 16, 176, 166, shape='cyl', fill='#2E3338')
         + raster(60, 60, 6, 1, 6, 90, 18, r=3, fill='#5E666C')),
    teil('verschluss', 'plastic_housing', 'Verschlussgriff', 'Verschluss', 'box',
         x=95, y=230, w=40, d=10, z=36, h=54, r=4, explode=[0, 60, 0], mass=25, sortBias=60,
         marks=[mark('box', 6, 2, 28, 6, 3, fill='#4A5158')],
         info='Hält beide Schalen zusammen, damit das Sandwich gepresst wird. Mit einem Stift im Gelenk befestigt.',
         color='#3C4248'),
    teil('scharnier', 'plastic_housing', 'Scharnier', 'Scharnier', 'box', material_id='steel',
         x=70, y=0, w=90, d=12, z=40, h=22, r=3, explode=[0, -50, 0], mass=40, materials=[['stahl', 100]],
         info='Stahlscharnier, das beide Schalen verbindet. Abschrauben und zum Altmetall geben.',
         color='#9AA2A6'),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=160, y=14, w=70, d=8, z=2, h=8, r=4, explode=[70, 0, 0], form='liegend_x', mass=80, materials=[['pvc', 90], ['pp', 10]],
         info='Etwa 80 cm PVC-Mantel mit Stecker. Längs aufschlitzen, um die Kupferadern freizulegen.',
         color='#2E3338', marks=[mark('box', 60, 1, 10, 6, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=160, y=16.5, w=70, d=3, z=4.5, h=3, r=1, explode=[70, 0, 15], form='liegend_x', mass=40,
         info='Drei Kupferadern. Kupfer lässt sich fast verlustfrei wiederverwerten.',
         color='#B87333'),
]

explodiere(teile, abstand=60, fest=('bodenplatte',), nach_liste=True, abstaende={'griff': 70, 'lampen': 30, 'oberschale': 110},
           gruppen=[['heizung_oben', 'heizung_oben_b', 'heizung_oben_c'], ['heizung_unten', 'heizung_unten_b', 'heizung_unten_c']])
for p in teile:  # Griff zusätzlich nach links, sonst scheint er auf der Oberschale zu liegen
    if p['id'] == 'griff':
        p['explode'][0] = -150
skaliere_masse(teile, oid='sandwich_maker')
for p in teile:  # gerundete Formen (form): marks nur in der Zeichnung, oben flach würden sie schweben
    if p.get('form'):
        p['marks'] = [dict(m, zeichnung=True) for m in p.get('marks') or []]
schreibe('sandwich_maker', teile)
