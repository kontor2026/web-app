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


def heizung(id, name, short, z):
    return teil(id, 'heating_element', name, short, 'box', x=25, y=30, w=180, d=180, z=z, h=6, r=30, mass=80,
                materials=[['stahl', 55], ['nichrom', 20], ['keramik', 25]],
                info='Rohrheizkörper: Heizdraht in Keramikpulver in einem Stahlrohr, auf die Rückseite der Platte gepresst. Erst ganz abkühlen lassen.',
                color='#9AA2A6', marks=[mark('box', 0, 0, 180, 10, 5, fill='#C4672D'), mark('box', 0, 0, 10, 180, 5, fill='#C4672D'),
                                        mark('box', 170, 0, 10, 180, 5, fill='#C4672D')])


teile = [
    teil('oberschale', 'plastic_housing', 'Obere Gehäuseschale', 'Oberschale', 'box',
         x=0, y=10, w=230, d=220, z=50, h=50, r=40, mass=180, material_id='phenolic_resin', materials=[['phenolharz', 60], ['pcabs', 40]],
         info='Hitzefeste Kunststoffschale mit Kontrollleuchten. Die Schrauben sitzen innen unter der Backplatte.',
         color='#2E3338', marks=[mark('cyl', 95, 185, 10, fill='#E74C3C'), mark('cyl', 125, 185, 10, fill='#2ECC71'), mark('box', 20, 20, 190, 150, 30, fill='#3C4248')]),
    heizung('heizung_oben', 'Heizelement oben', 'Heizung oben', 62),
    platte('platte_oben', 'Backplatte oben', 'Platte oben', 50),
    platte('platte_unten', 'Backplatte unten', 'Platte unten', 38),
    heizung('heizung_unten', 'Heizelement unten', 'Heizung unten', 32),
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
         color='#7C858C', marks=raster(14, 14, 2, 2, 16, 16, 176, 166, shape='cyl', fill='#2E3338')),
    teil('verschluss', 'plastic_housing', 'Verschlussgriff', 'Verschluss', 'box',
         x=85, y=222, w=60, d=18, z=40, h=45, r=6, explode=[0, 60, 0], mass=25,
         info='Hält beide Schalen zusammen, damit das Sandwich gepresst wird. Mit einem Stift im Gelenk befestigt.',
         color='#3C4248'),
    teil('scharnier', 'plastic_housing', 'Scharnier', 'Scharnier', 'box', material_id='steel',
         x=70, y=0, w=90, d=12, z=40, h=22, r=3, explode=[0, -50, 0], mass=40, materials=[['stahl', 100]],
         info='Stahlscharnier, das beide Schalen verbindet. Abschrauben und zum Altmetall geben.',
         color='#9AA2A6'),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=160, y=14, w=70, d=8, z=2, h=8, r=4, explode=[70, 0, 0], mass=80, materials=[['pvc', 90], ['pp', 10]],
         info='Etwa 80 cm PVC-Mantel mit Stecker. Längs aufschlitzen, um die Kupferadern freizulegen.',
         color='#2E3338', marks=[mark('box', 60, 1, 10, 6, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=160, y=16.5, w=70, d=3, z=4.5, h=3, r=1, explode=[70, 0, 15], mass=40,
         info='Drei Kupferadern. Kupfer lässt sich fast verlustfrei wiederverwerten.',
         color='#B87333'),
]

explodiere(teile, abstand=60, fest=('bodenplatte',), nach_liste=True)
skaliere_masse(teile, oid='sandwich_maker')
schreibe('sandwich_maker', teile)
