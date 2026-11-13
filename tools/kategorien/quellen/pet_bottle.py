"""3D-Modell: pet_bottle. Erzeugt tools/kategorien/modelle/pet_bottle.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, schreibe  # noqa: E402

teile = [
    teil('deckel', 'hdpe_screw_cap', 'Schraubdeckel', 'Deckel', 'cyl',
         material_id='hdpe', x=17.5, y=17.5, w=30, z=208, h=22, explode=[0, 0, 47], mass=1.8, materials=[['hdpe', 100]], info='HDPE, Recyclingcode 2. Seit 2024 bleibt er per Lasche an der Flasche hängen, damit er mit ihr recycelt wird.', color='#2F6DB5', marks=[{'shape': 'cyl', 'x': 4, 'y': 4, 'w': 22}]),
    teil('ring', 'hdpe_screw_cap', 'Sicherungsring', 'Ring', 'cyl',
         material_id='hdpe', x=17, y=17, w=31, z=203, h=3, explode=[0, 0, 29], mass=0.4, materials=[['hdpe', 100]], info='Reißt beim ersten Öffnen ab und zeigt, dass die Flasche unbenutzt ist. Gehört zum Deckel.', color='#2F6DB5'),
    teil('hals', 'pet_bottle_body', 'Flaschenhals mit Gewinde', 'Hals', 'cyl',
         material_id='pet', x=19, y=19, w=27, z=175, h=37, explode=[0, 0, 0], mass=2.5, materials=[['pet', 100]], info='Dickwandig und nicht verstreckt, darum der schwerste Teil der Flasche je Zentimeter. Beim Recycling wird alles zusammen geschreddert.', color='#CFE3E8', opacity=0.6, marks=[{'shape': 'cyl', 'x': 5.5, 'y': 5.5, 'w': 16}]),
    teil('schulter', 'pet_bottle_body', 'Flaschenschulter', 'Schulter', 'cyl',
         material_id='pet', x=8.5, y=8.5, w=48, z=150, h=25, explode=[0, 0, 0], mass=3.3, materials=[['pet', 100]], info='Übergang vom Hals zum Körper. Teil der Flasche, beim Streckblasen aus dem Rohling mitgeformt.', color='#CFE3E8', opacity=0.6),
    teil('koerper', 'pet_bottle_body', 'Flaschenkörper', 'Körper', 'cyl',
         material_id='pet', x=0, y=0, w=65, z=0, h=150, explode=[0, 0, 0], mass=16.5, materials=[['pet', 100]], info='PET, Recyclingcode 1. Wird aus einem reagenzglasgroßen Rohling heiß aufgeblasen. Pfandflaschen werden zu neuen Flaschen recycelt.', color='#CFE3E8', opacity=0.6, marks=[{'shape': 'cyl', 'x': 8.5, 'y': 8.5, 'w': 48}]),
    teil('etikett', 'plastic_label', 'Etikett', 'Etikett', 'box',
         material_id='pp', x=65, y=12, w=0.3, d=41, z=75, h=70, r=0, explode=[60, 0, 0], mass=0.5, materials=[['pp', 100]], info='Dünne PP-Folie, rundum geklebt. In der Recyclinganlage wird sie abgetrennt, weil sie leichter ist als PET und im Wasser schwimmt.', color='#D9483B', sortBias=100),
]

schreibe('pet_bottle', teile)
