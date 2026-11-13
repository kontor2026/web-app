"""3D-Modell: aluminium_can. Erzeugt tools/kategorien/modelle/aluminium_can.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, schreibe  # noqa: E402

teile = [
    teil('lasche', 'aluminium_can_body', 'Aufreißlasche', 'Lasche', 'box',
         material_id='aluminium', x=26.5, y=20, w=13, d=20, z=115, h=0.5, r=4, explode=[0, 0, 35], mass=0.25, materials=[['alu', 100]], info='Hebel zum Öffnen, mit einer Niete am Deckel befestigt. Dranlassen: lose fällt sie durch die Sortieranlage.', color='#B9C0C6', marks=[{'shape': 'box', 'x': 3.5, 'y': 9, 'w': 6, 'd': 8, 'r': 3}]),
    teil('deckel', 'aluminium_can_body', 'Deckel', 'Deckel', 'cyl',
         material_id='aluminium', x=6, y=6, w=54, z=111, h=4, explode=[0, 0, 20], mass=2.4, materials=[['alu', 100]], info='Härtere Aluminiumlegierung mit Magnesium als der Rumpf. Wird nach dem Befüllen auf den Rumpf gefalzt.', color='#C9CED3', marks=[{'shape': 'cyl', 'x': 24, 'y': 11, 'w': 6}, {'shape': 'box', 'x': 16, 'y': 34, 'w': 22, 'd': 14, 'r': 6}]),
    teil('hals', 'aluminium_can_body', 'Eingezogener Hals', 'Hals', 'cyl',
         material_id='aluminium', x=4, y=4, w=58, z=103, h=8, explode=[0, 0, 0], mass=0.6, materials=[['alu', 100]], info='Der Rumpf wird oben enger gerollt, damit ein kleinerer Deckel passt. Das spart Aluminium.', color='#C9CED3'),
    teil('rumpf', 'aluminium_can_body', 'Dosenrumpf', 'Rumpf', 'cyl',
         material_id='aluminium', x=0, y=0, w=66, z=0, h=103, explode=[0, 0, 0], mass=9.5, materials=[['alu', 100]], info='Aus einer Aluminiumscheibe in einem Stück tiefgezogen, die Wand ist dünner als ein Haar. Innen schützt ein Lack vor dem Getränk.', color='#C9CED3', marks=[{'shape': 'cyl', 'x': 4, 'y': 4, 'w': 58}]),
    teil('lack', 'aluminium_can_body', 'Außenlack und Druck', 'Druck', 'box',
         x=66, y=13, w=0.3, d=40, z=8, h=90, r=0, explode=[50, 0, 0], mass=0.25, materials=[['druck', 100]], info='Farbe und Lack verbrennen beim Einschmelzen. Aluminium lässt sich danach ohne Qualitätsverlust immer wieder recyceln.', color='#C8362F', sortBias=100),
]

schreibe('aluminium_can', teile)
