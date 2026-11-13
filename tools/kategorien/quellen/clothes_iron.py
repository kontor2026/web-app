"""3D-Modell: clothes_iron. Erzeugt tools/kategorien/modelle/clothes_iron.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Dampfbügeleisen auf der Sohle, Spitze vorne (y = 270), Kabel hinten (y = 0).
# Explosion: Sohle bleibt, darüber Heizelement, Hitzeschutzblech, Thermostat, Wassertank, Oberschale, Temperaturregler.
# Heckkappe nach hinten (dy < 0), Sprühdüse nach vorne, Kabel nach rechts (dx > 0).

teile = [
    teil('regler', 'plastic_housing', 'Temperaturregler', 'Regler', 'cyl',
         x=40, y=190, w=40, z=72, h=8, mass=10,
         info='Drehknopf, der über eine Achse den Thermostat verstellt. Lässt sich mit einem flachen Schraubendreher abhebeln.',
         color='#9AA2A6', marks=[mark('box', 18, 4, 4, 14, 1, fill='#2E3338')]),
    teil('oberschale', 'plastic_housing', 'Gehäuse mit Griff', 'Gehäuse', 'box',
         x=10, y=20, w=100, d=220, z=72, h=68, r=40, mass=200,
         info='Hitzefester Kunststoff mit Griff und Dampftasten. Ist mit Schrauben von unten durch die Sohle befestigt.',
         color='#5DADE2', marks=[mark('box', 30, 40, 40, 110, 18, fill='#2E3338'), mark('cyl', 38, 170, 12, fill='#E9EEF2'),
                                 mark('cyl', 52, 170, 12, fill='#E9EEF2')]),
    teil('wassertank', 'water_tank', 'Wassertank', 'Wassertank', 'box',
         x=12, y=30, w=96, d=225, z=36, h=36, r=45, mass=90,
         info='Durchsichtiger Kunststofftank für etwa 300 ml Wasser. Ist eingeklipst; ohne Metall gehört er zum Kunststoff.',
         color='#CFE3EA', opacity=0.6, marks=[mark('box', 30, 190, 30, 20, 8, fill='#3C4248')]),
    teil('thermostat', 'thermostat', 'Thermostat (Bimetall)', 'Thermostat', 'box',
         x=45, y=120, w=30, d=30, z=26, h=10, r=3, mass=30, materials=[['bimetall', 40], ['keramik', 20], ['kupfer', 20], ['kontakte', 20]],
         info='Ein Bimetallstreifen schaltet die Heizung aus, wenn die eingestellte Temperatur erreicht ist. Klickt beim Aufheizen hörbar.',
         color='#B8BEC4', marks=[mark('cyl', 10, 10, 10, fill='#D5DADE')]),
    teil('hitzeschild', 'iron_soleplate', 'Hitzeschutzblech', 'Hitzeschild', 'box', material_id='steel',
         x=10, y=15, w=100, d=235, z=22, h=4, r=45, mass=60, materials=[['stahl', 100]],
         info='Dünnes Stahlblech zwischen heißer Sohle und Kunststoffteilen. Kommt zum Altmetall.',
         color='#9AA2A6'),
    teil('heizelement', 'heating_element', 'Rohrheizkörper', 'Heizelement', 'box',
         x=15, y=25, w=90, d=210, z=16, h=6, r=40, mass=150, materials=[['stahl', 50], ['nichrom', 20], ['keramik', 30]],
         info='U-förmiges Heizrohr mit Nickel-Chrom-Draht, in die Sohle eingegossen. Lässt sich nicht von der Sohle trennen.',
         color='#8C7B6B', marks=[mark('box', 0, 0, 10, 200, 5, fill='#C4672D'), mark('box', 80, 0, 10, 200, 5, fill='#C4672D'),
                                 mark('box', 0, 0, 90, 10, 5, fill='#C4672D')]),
    teil('sohle', 'iron_soleplate', 'Bügelsohle', 'Sohle', 'box',
         x=0, y=0, w=120, d=270, z=0, h=16, r=55, mass=450, materials=[['alu', 95], ['keramik', 5]],
         info='Aluminiumguss mit Keramikbeschichtung und Dampflöchern. Wertvolles Aluminium für den Metallschrott.',
         color='#C9CED2', marks=raster(30, 40, 4, 12, 4, 4, 18, 16, shape='cyl', fill='#7C858C')),
    teil('heckkappe', 'plastic_housing', 'Heckkappe mit Kabelgelenk', 'Heckkappe', 'box',
         x=25, y=0, w=70, d=22, z=20, h=70, r=8, explode=[0, -50, 0], mass=40,
         info='Rückwand mit Stellfläche und Kabelgelenk. Hinter ihr liegen die Kabelanschlüsse; zwei Schrauben lösen.',
         color='#2E3338'),
    teil('spruehduese', 'water_tank', 'Sprühdüse', 'Sprühdüse', 'box', material_id='pp',
         x=50, y=240, w=20, d=22, z=76, h=14, r=4, explode=[0, 40, 0], mass=5, materials=[['pp', 100]],
         info='Kleine Pumpdüse, die Wasser aus dem Tank auf die Wäsche sprüht. Reiner Kunststoff.',
         color='#E9EEF2'),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=40, y=4, w=80, d=8, z=30, h=8, r=4, explode=[80, -50, 0], mass=100, materials=[['pvc', 85], ['textil', 15]],
         info='Etwa 2 m Kabel mit Stoffummantelung oder PVC. Längs aufschlitzen, um die Kupferadern freizulegen.',
         color='#2E3338', marks=[mark('box', 70, 1, 10, 6, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=40, y=6.5, w=80, d=3, z=32.5, h=3, r=1, explode=[80, -50, 15], mass=50,
         info='Drei Kupferadern für bis zu 2400 Watt. Kupfer lässt sich fast verlustfrei wiederverwerten.',
         color='#B87333'),
]

explodiere(teile, abstand=20, fest=('sohle',))
skaliere_masse(teile, oid='clothes_iron')
schreibe('clothes_iron', teile)
