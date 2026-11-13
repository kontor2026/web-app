"""3D-Modell: glass_bottle. Erzeugt tools/kategorien/modelle/glass_bottle.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, schreibe  # noqa: E402

teile = [
    teil('kronkorken', 'crown_cap', 'Kronkorken', 'Kronkorken', 'cyl',
         material_id='steel', x=14, y=14, w=32, z=224, h=6, explode=[0, 0, 22], mass=2.2, materials=[['weissblech', 90], ['ldpe', 10]], info='Weißblech mit Kunststoffdichtung innen. Mit dem Öffner abhebeln, er gehört in die Metallsammlung.', color='#B8BEC4', marks=[{'shape': 'cyl', 'x': 5, 'y': 5, 'w': 22}]),
    teil('hals', 'glass_container', 'Flaschenhals', 'Hals', 'cyl',
         material_id='glass', x=17, y=17, w=26, z=170, h=56, explode=[0, 0, 0], mass=40, materials=[['behaelterglas', 100]], info='Langer Hals mit verstärktem Rand für den Kronkorken. Teil der Flasche, in einem Stück geblasen.', color='#6B4A2B', opacity=0.75, marks=[{'shape': 'cyl', 'x': 5, 'y': 5, 'w': 16}]),
    teil('schulter', 'glass_container', 'Flaschenschulter', 'Schulter', 'cyl',
         material_id='glass', x=7, y=7, w=46, z=140, h=30, explode=[0, 0, 0], mass=52, materials=[['behaelterglas', 100]], info='Übergang zum Hals. Braunes Glas schützt das Getränk vor Licht.', color='#6B4A2B', opacity=0.75),
    teil('koerper', 'glass_container', 'Flaschenkörper', 'Körper', 'cyl',
         material_id='glass', x=0, y=0, w=60, z=0, h=140, explode=[0, 0, 0], mass=263, materials=[['behaelterglas', 100]], info='Kalk-Natron-Glas aus Sand, Soda und Kalk. Als Mehrwegflasche bis zu 50-mal befüllt, danach nach Farbe getrennt eingeschmolzen.', color='#6B4A2B', opacity=0.75, marks=[{'shape': 'cyl', 'x': 7, 'y': 7, 'w': 46}]),
    teil('etikett', 'paper_label', 'Bauchetikett', 'Etikett', 'box',
         material_id='paper', x=60, y=10, w=0.3, d=40, z=30, h=75, r=0, explode=[55, 0, 0], mass=2, materials=[['papier', 100]], info='Papier mit wasserlöslichem Leim. In der Spülanlage der Brauerei weicht es ab.', color='#E8DDC0', sortBias=100),
    teil('halsetikett', 'paper_label', 'Halsetikett', 'Halsetikett', 'box',
         material_id='paper', x=43, y=20, w=0.3, d=20, z=185, h=25, r=0, explode=[55, 0, 0], mass=0.5, materials=[['papier', 100]], info='Kleines Papieretikett am Hals. Beim Altglas darf es dranbleiben, es verbrennt in der Schmelze.', color='#C9A646', sortBias=100),
]

schreibe('glass_bottle', teile)
