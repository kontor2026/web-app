"""3D-Modell: yogurt_cup. Erzeugt tools/kategorien/modelle/yogurt_cup.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, schreibe  # noqa: E402

teile = [
    teil('deckel', 'aluminium_lid_foil', 'Aluminium-Deckelfolie', 'Deckel', 'cyl',
         material_id='aluminium', x=0, y=0, w=75, z=70, h=0.2, explode=[0, 0, 25], mass=0.4, materials=[['alu', 90], ['pp', 10]], info='Aluminiumfolie mit Siegellack. Ganz abziehen und getrennt in die Gelbe Tonne werfen, sonst erkennt die Anlage den Becher als Metall.', color='#E3E6E9', marks=[{'shape': 'cyl', 'x': 4, 'y': 4, 'w': 67, 'fill': '#D8DCE0'}]),
    teil('rand', 'pp_cup_body', 'Siegelrand', 'Rand', 'cyl',
         material_id='pp', x=0, y=0, w=75, z=68, h=2, explode=[0, 0, 0], mass=0.5, materials=[['pp', 100]], info='Flacher Rand, auf den die Deckelfolie heiß gesiegelt wird.', color='#F2F0EA', wand=3.5, boden=0, marks=[{'shape': 'cyl', 'x': 3, 'y': 3, 'w': 69, 'zeichnung': True}]),
    teil('oben', 'pp_cup_body', 'Becherwand oben', 'Becher', 'cyl',
         material_id='pp', x=2.5, y=2.5, w=70, z=44, h=24, explode=[0, 0, 0], mass=1.1, materials=[['pp', 100]], info='PP, Recyclingcode 5. Tiefgezogen aus einer dünnen Folie, darum nach oben breiter.', color='#F2F0EA', wand=1, boden=0),
    teil('mitte', 'pp_cup_body', 'Becherwand Mitte', 'Wand', 'cyl',
         material_id='pp', x=5.5, y=5.5, w=64, z=22, h=22, explode=[0, 0, 0], mass=1.0, materials=[['pp', 100]], info='Die Wand ist hier nur etwa 0,3 mm dick. Den Halt gibt die Papp-Banderole.', color='#F2F0EA', wand=1.1, boden=0, label=False),
    teil('boden', 'pp_cup_body', 'Becherboden', 'Boden', 'cyl',
         material_id='pp', x=8.5, y=8.5, w=58, z=0, h=22, explode=[0, 0, 0], mass=0.9, materials=[['pp', 100]], info='Auskratzen reicht, ausspülen ist nicht nötig. Becher und Deckel getrennt einwerfen.', color='#F2F0EA', wand=1.2),
    teil('banderole', 'cardboard_sleeve', 'Papp-Banderole', 'Banderole', 'cyl',
         material_id='cardboard', x=1.5, y=1.5, w=72, z=5, h=60, explode=[95, 0, 0], mass=2.1, materials=[['papier', 100]], info='Bedruckter Karton rund um den Becher. An der Perforation aufreißen und ins Altpapier geben.', color='#8FB04A', wand=0.6, boden=0),
]

schreibe('yogurt_cup', teile)
