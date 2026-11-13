"""3D-Modell: hair_straightener. Erzeugt tools/kategorien/modelle/hair_straightener.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Glätteisen geschlossen, flach liegend: Länge entlang y, Gelenk hinten (y = 0), Platten vorne (y 180..290).
# Zwei Arme übereinander (unten z 0..17, oben z 18..35), dazwischen die Platten mit den Heizern.
# Explosion nach Liste: Unterarm bleibt, darüber Platine, untere Heizung und Platte, obere Platte und Heizung, Oberarm.
# Gelenk nach hinten (dy < 0), Kabel nach rechts (dx > 0).

def platte(id, name, short, z):
    return teil(id, 'ceramic_plates', name, short, 'box', material_id='aluminium',
                x=3, y=180, w=24, d=110, z=z, h=4, r=3, mass=35, materials=[['alu', 88], ['keramik', 12]],
                info='Aluminiumplatte mit Keramikbeschichtung, die die Haare glättet. Nach dem Abkühlen aus dem Federrahmen hebeln.',
                color='#D5D0C8', marks=[mark('box', 2, 4, 20, 102, 2, fill='#E8E4DD')])


def heizer(id, name, short, z):
    return teil(id, 'heating_element', name, short, 'box', material_id='ceramic',
                x=6, y=185, w=18, d=100, z=z, h=3, r=1, mass=15, materials=[['keramik', 70], ['nichrom', 15], ['alu', 15]],
                info='Keramikheizer mit eingedruckter Heizbahn, erreicht bis 230 Grad. Erst ganz abkühlen lassen, dann ablösen.',
                color='#E9E1D0', marks=[mark('box', 2, 4, 14, 92, 1, fill='#C4672D')])


teile = [
    teil('oberarm', 'plastic_housing', 'Oberer Arm', 'Oberarm', 'box',
         x=0, y=10, w=30, d=290, z=18, h=17, r=8, mass=70, material_id='pc', materials=[['pcabs', 90], ['stahl', 10]],
         info='Hitzefeste Kunststoffschale mit gefedertem Plattenrahmen. Die Schalen sind verclipst und mit kleinen Schrauben gesichert.',
         color='#2E3338', marks=[mark('box', 3, 170, 24, 115, 4, fill='#3C4248')]),
    heizer('heizer_oben', 'Heizelement oben', 'Heizer oben', 22),
    platte('platte_oben', 'Heizplatte oben', 'Platte oben', 18),
    platte('platte_unten', 'Heizplatte unten', 'Platte unten', 13),
    heizer('heizer_unten', 'Heizelement unten', 'Heizer unten', 10),
    teil('platine', 'circuit_board', 'Steuerplatine mit Tasten', 'Platine', 'box',
         x=5, y=60, w=20, d=110, z=4, h=6, r=1, mass=15,
         info='Regelt die Temperatur und schaltet nach einer Stunde automatisch ab. Mit Tasten und Anzeige verlötet, kommt zum Elektroschrott.',
         color='#2F6B3A', marks=[mark('box', 5, 70, 10, 20, 1, fill='#222'), mark('box', 4, 20, 12, 30, 2, fill='#E0E4E7'),
                                 mark('box', 5, 95, 10, 8, 1, fill='#E74C3C')]),
    teil('unterarm', 'plastic_housing', 'Unterer Arm mit Bedienfeld', 'Unterarm', 'box',
         x=0, y=10, w=30, d=290, z=0, h=17, r=8, mass=70, material_id='pc', materials=[['pcabs', 90], ['stahl', 10]],
         info='Untere Schale mit Ein-Taste und Temperaturtasten, innen die Platine. Zuerst die Platten ausbauen, dann die Schale öffnen.',
         color='#2E3338', marks=[mark('box', 6, 80, 18, 40, 4, fill='#1E2226')]),
    teil('gelenk', 'plastic_housing', 'Federgelenk mit Verriegelung', 'Gelenk', 'box', material_id='steel',
         x=3, y=2, w=24, d=28, z=8, h=20, r=4, explode=[0, -50, 0], mass=15, materials=[['stahl', 60], ['pcabs', 40]],
         info='Achse mit Stahlfeder, die die Arme aufdrückt, und Schiebeverriegelung. Feder kann beim Ausbau herausspringen.',
         color='#9AA2A6'),
    teil('kabel', 'cable_insulation', 'Netzkabel mit Drehgelenk', 'Kabel', 'box',
         x=11, y=0, w=8, d=60, z=13, h=8, r=4, explode=[40, 0, 0], mass=50, materials=[['pvc', 85], ['pcabs', 15]],
         info='Etwa 2 m Kabel mit 360-Grad-Drehgelenk, damit es sich nicht verdreht. Längs aufschlitzen, um die Kupferadern freizulegen.',
         color='#2E3338', marks=[mark('box', 1, 0, 6, 10, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=13.5, y=0, w=3, d=60, z=15.5, h=3, r=1, explode=[40, 0, 12], mass=25,
         info='Zwei Kupferadern aus feiner Litze. Kupfer lässt sich fast verlustfrei wiederverwerten.',
         color='#B87333'),
]

explodiere(teile, abstand=25, fest=('unterarm',), nach_liste=True)
skaliere_masse(teile, oid='hair_straightener')
schreibe('hair_straightener', teile)
