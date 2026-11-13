"""3D-Modell: beverage_carton. Erzeugt tools/kategorien/modelle/beverage_carton.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, schreibe  # noqa: E402

teile = [
    teil('deckel', 'hdpe_screw_cap', 'Schraubdeckel', 'Deckel', 'cyl',
         material_id='hdpe', x=20, y=15, w=30, z=184, h=11, explode=[0, 0, 46], mass=2, materials=[['hdpe', 100]], info='HDPE. Bleibt am Karton: Deckel und Ausgießer werden in der Sortieranlage zusammen mit dem Karton erfasst.', color='#F2F0EA', marks=[{'shape': 'cyl', 'x': 4, 'y': 4, 'w': 22}]),
    teil('ausgiesser', 'hdpe_screw_cap', 'Ausgießer', 'Ausgießer', 'cyl',
         material_id='hdpe', x=17, y=12, w=36, z=181, h=4, explode=[0, 0, 25], mass=1.5, materials=[['hdpe', 100]], info='Kunststoffring mit Gewinde, auf den Karton geschweißt. Beim ersten Aufdrehen schneidet er die Verpackung auf.', color='#F2F0EA', marks=[{'shape': 'cyl', 'x': 6, 'y': 6, 'w': 24}]),
    teil('karton', 'carton_body', 'Verbundkarton', 'Karton', 'box',
         material_id='composite_carton', x=0, y=0, w=70, d=60, z=0, h=181, r=2, explode=[0, 0, 0], mass=26.5, materials=[['verbund', 100]], info='Etwa 75 % Pappe, 20 % Polyethylen und 5 % Aluminium, fest miteinander verbunden. Im Recycling wird nur die Pappe zurückgewonnen.', color='#E7E1D3', marks=[{'shape': 'box', 'x': 0, 'y': 28, 'w': 70, 'd': 4, 'r': 0}, {'shape': 'cyl', 'x': 19, 'y': 14, 'w': 32}]),
]

schreibe('beverage_carton', teile)
