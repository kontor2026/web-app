"""3D-Modell: hair_straightener. Erzeugt tools/kategorien/modelle/hair_straightener.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Glätteisen geschlossen, flach liegend: Länge entlang y, Gelenk hinten (y klein), Platten vorne (y 180..290).
# Zwei Arme übereinander (unten z 0..17, oben z 18..35). Im oberen Arm hinten die Platine mit Anzeige und Tasten,
# vorne in beiden Armen je eine gefederte Heizplatte mit Keramikheizer.
# Explosion nach Liste: Unterarm bleibt, darüber Federn, untere Heizung und Platte, obere Platte, Heizung, Federn,
# Platine mit Anzeige und Oberarm. Gelenk nach hinten (dy < 0), Kabel nach rechts (dx > 0).
SCHWARZ = '#2E3338'
FEDER = '#9AA2A6'


def platte(id, name, short, z):
    return teil(id, 'ceramic_plates', name, short, 'box', material_id='aluminium',
                x=3, y=180, w=24, d=110, z=z, h=4, r=3, mass=35, materials=[['alu', 88], ['keramik', 12]],
                info='Aluminiumplatte mit Keramikbeschichtung, die die Haare glättet. Nach dem Abkühlen aus dem '
                     'Federrahmen hebeln.',
                color='#D5D0C8', marks=[mark('box', 2, 4, 20, 102, 2, fill='#E8E4DD')])


def heizer(id, name, short, z):
    return teil(id, 'heating_element', name, short, 'box', material_id='ceramic',
                x=6, y=185, w=18, d=100, z=z, h=3, r=1, mass=15,
                materials=[['keramik', 70], ['nichrom', 15], ['alu', 15]],
                info='Keramikheizer mit eingedruckter Heizbahn, erreicht bis 230 Grad. Erst ganz abkühlen lassen, '
                     'dann ablösen.',
                color='#E9E1D0', marks=[mark('box', 2, 4, 14, 92, 1, fill='#C4672D')] + raster(4, 2, 2, 1, 4, 3, 6, r=0.5, fill='#B8BEC4'))


def federn(oben, z):
    s = 'oben' if oben else 'unten'
    return [teil(f'feder_{s}{i}', 'ceramic_plates', 'Andruckfeder', 'Federn', 'cyl', material_id='steel',
                 x=12, y=y, w=6, z=z, h=6, mass=1, materials=[['stahl', 100]], color=FEDER, label=oben and i == 0,
                 info='Kleine Stahlfedern drücken die Platten nach außen, damit sie sich dem Haar anpassen.',
                 marks=[mark('cyl', 1.5, 1.5, 3, fill='#6B7378')])
            for i, y in enumerate((200, 262))]


teile = [
    teil('oberarm', 'plastic_housing', 'Oberer Arm', 'Oberarm', 'box',
         x=0, y=5, w=30, d=295, z=18, h=17, r=9, mass=70, material_id='pc', materials=[['pcabs', 90], ['stahl', 10]],
         info='Hitzefeste Kunststoffschale mit gefedertem Plattenrahmen. Die Schalen sind verclipst und mit kleinen '
              'Schrauben gesichert.',
         color=SCHWARZ, marks=[mark('box', 3, 175, 24, 115, 4, fill='#3C4248'), mark('box', 7, 70, 16, 30, 2, '#14171A'),
                               mark('box', 10, 77, 4, 6, 0.5, '#E8833A'), mark('box', 16, 77, 4, 6, 0.5, '#E8833A'),
                               mark('box', 10, 87, 10, 2, 0.5, '#E8833A'),
                               mark('cyl', 10, 108, 10, fill='#4A5156'), mark('cyl', 10, 122, 10, fill='#4A5156'),
                               mark('cyl', 9, 40, 12, fill='#C0392B'), mark('box', 13, 43, 4, 6, 1, '#E9EEF2')]),
    teil('anzeige', 'circuit_board', 'LED-Temperaturanzeige', 'Anzeige', 'box', material_id='mixed_electronics',
         x=8, y=71, w=14, d=28, z=29, h=3, r=1, mass=2, materials=[['led', 30], ['pcabs', 50], ['kupfer', 20]],
         color='#22272B', info='Siebensegment-Anzeige, zeigt die eingestellte Temperatur. Auf die Platine gelötet.',
         marks=[mark('box', 2, 6, 4, 6, 0.5, '#E8833A'), mark('box', 8, 6, 4, 6, 0.5, '#E8833A')]),
    teil('platine', 'circuit_board', 'Steuerplatine mit Tasten', 'Platine', 'box',
         x=5, y=35, w=20, d=120, z=26, h=1.6, r=1, mass=12,
         info='Regelt die Temperatur und schaltet nach einer Stunde automatisch ab. Mit Tasten und Anzeige verlötet, '
              'kommt zum Elektroschrott.',
         color='#2F6B3A', marks=[mark('box', 5, 100, 10, 12, 1, fill='#222'), mark('cyl', 5, 75, 8, fill='#B7BCC0'),
                                 mark('cyl', 5, 89, 8, fill='#B7BCC0'), mark('cyl', 5, 6, 10, fill='#B7BCC0'),
                                 mark('box', 4, 20, 12, 10, 1, fill='#C5803D')]),
    *federn(True, 25),
    teil('fuehler', 'heating_element', 'Temperaturfühler (NTC)', 'Temperaturfühler', 'box',
         material_id='mixed_electronics', x=17, y=230, w=6, d=10, z=25, h=2, r=1, mass=0.5,
         materials=[['keramik', 50], ['kupfer', 30], ['pcabs', 20]], color='#3B3F44',
         info='Winziger Sensor auf dem Heizer, meldet der Platine die Temperatur der Platte.'),
    heizer('heizer_oben', 'Heizelement oben', 'Heizer oben', 22),
    platte('platte_oben', 'Heizplatte oben', 'Platte oben', 18),
    platte('platte_unten', 'Heizplatte unten', 'Platte unten', 13),
    heizer('heizer_unten', 'Heizelement unten', 'Heizer unten', 10),
    *federn(False, 4),
    *[teil(f'schraube{i}', 'plastic_housing', 'Gehäuseschraube', 'Schrauben', 'cyl', material_id='steel',
           x=12, y=y, w=6, z=3, h=3, mass=0.5, materials=[['stahl', 100]], color=FEDER, label=i == 0,
           info='Kleine Kreuzschlitzschrauben halten die Armschalen zusammen. Oft unter Gummistopfen versteckt.',
           marks=[mark('box', 1, 2.5, 4, 1), mark('box', 2.5, 1, 1, 4)])
      for i, y in enumerate((60, 150))],
    teil('unterarm', 'plastic_housing', 'Unterer Arm', 'Unterarm', 'box',
         x=0, y=5, w=30, d=295, z=0, h=17, r=9, mass=70, material_id='pc', materials=[['pcabs', 90], ['stahl', 10]],
         info='Untere Schale mit Schiebeverriegelung. Zuerst die Platten ausbauen, dann die Schale öffnen.',
         color=SCHWARZ, marks=[mark('box', 3, 175, 24, 115, 4, fill='#3C4248'), mark('box', 9, 110, 12, 24, 4, '#1E2226')]),
    teil('gelenk', 'plastic_housing', 'Federgelenk', 'Gelenk', 'box', material_id='steel',
         x=3, y=8, w=24, d=24, z=8, h=20, r=4, explode=[0, -60, 0], mass=15, materials=[['stahl', 60], ['pcabs', 40]],
         info='Achse mit Stahlfeder, die die Arme aufdrückt. Feder kann beim Ausbau herausspringen.',
         color=FEDER, marks=[mark('cyl', 7, 7, 10, fill='#6B7378')]),
    teil('kabel', 'cable_insulation', 'Netzkabel mit Drehgelenk', 'Kabel', 'box',
         x=11, y=0, w=8, d=60, z=13, h=8, r=4, explode=[45, 0, 0], mass=50, materials=[['pvc', 85], ['pcabs', 15]],
         info='Etwa 2 m Kabel mit 360-Grad-Drehgelenk, damit es sich nicht verdreht. Längs aufschlitzen, um die '
              'Kupferadern freizulegen.',
         color=SCHWARZ, marks=[mark('box', 1, 0, 6, 10, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=13.5, y=0, w=3, d=60, z=15.5, h=3, r=1, explode=[45, 0, 12], mass=25,
         info='Zwei Kupferadern aus feiner Litze. Kupfer lässt sich fast verlustfrei wiederverwerten.',
         color='#B87333'),
]

explodiere(teile, abstand=22, fest=('unterarm',), nach_liste=True,
           abstaende={'anzeige': 12, 'fuehler': 10, **{f'feder_{s}{i}': 12 for s in ('oben', 'unten') for i in range(2)},
                      **{f'schraube{i}': 12 for i in range(2)}})
skaliere_masse(teile, oid='hair_straightener')
schreibe('hair_straightener', teile)
