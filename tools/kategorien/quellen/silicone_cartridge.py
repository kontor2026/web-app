"""3D-Modell: silicone_cartridge. Erzeugt tools/kategorien/modelle/silicone_cartridge.json.

Volle 310-ml-Kartusche Sanitärsilikon, stehend (Ø 50 mm, 230 mm hoch ohne Düse). Die Spritzdüse liegt wie im Handel
lose bei und ist hier schräg an der Kartusche angelegt, damit die Maße der CSV (ohne aufgeschraubte Düse) passen.
Explodiert: Kartuschenrohr bleibt stehen, Dichtmasse und Kolben links heraus (dx < 0), Düse und Etikett rechts.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

ROHR = '#F2F1EC'
DUESE = '#EDEDE6'

teile = [
    teil('spitze', 'hdpe_cartridge_tube', 'Gewindespitze', 'Spitze', 'cyl',
         x=17, y=17, w=16, z=208, h=22, mass=3,
         info='Angespritzte Spitze mit Außengewinde, oben durch eine dünne Wand verschlossen. '
              'Vor dem Gebrauch abschneiden, dann die Düse aufschrauben.',
         color=ROHR, marks=[mark('cyl', 5, 5, 6, fill='#D8D6CE')]),
    teil('schulter', 'hdpe_cartridge_tube', 'Kartuschenschulter', 'Schulter', 'cyl',
         x=3, y=3, w=44, z=200, h=8, mass=4,
         info='Übergang vom Rohr zur Spitze.', color=ROHR, label=False),
    teil('rohr_oben', 'hdpe_cartridge_tube', 'Kartuschenrohr', 'Kartusche', 'cyl',
         x=0, y=0, w=50, z=100, h=100, mass=18,
         info='Steifes HDPE-Rohr. Restinhalt aushärten lassen; die leere Kartusche gehört in die Gelbe Tonne, '
              'eine noch volle zur Schadstoffsammlung oder zum Wertstoffhof.',
         color=ROHR, opacity=0.85, marks=[mark('cyl', 2, 2, 46, fill='#E4E2DA')]),
    teil('rohr_unten', 'hdpe_cartridge_tube', 'Kartuschenrohr unten', 'Rohr unten', 'cyl',
         x=0, y=0, w=50, z=0, h=100, mass=18,
         info='Unten offen: Hier drückt die Kartuschenpistole den Kolben nach oben.',
         color=ROHR, opacity=0.85, label=False),
    teil('dichtmasse', 'hdpe_cartridge_tube', 'Silikon-Dichtmasse', 'Silikon', 'cyl',
         material_id='silicone', x=1.5, y=1.5, w=47, z=14, h=186, explode=[-70, 0, 0], mass=310,
         materials=[['gummi', 100]],
         info='Pastöses Silikon, das an der Luft mit Feuchtigkeit aushärtet. Nicht in den Ausguss: '
              'Reste in der Kartusche aushärten lassen.',
         color='#FAFAFA', marks=[mark('cyl', 8, 8, 31, fill='#F0F0F0')]),
    teil('kolben', 'hdpe_cartridge_tube', 'Kolben', 'Kolben', 'cyl',
         x=1.5, y=1.5, w=47, z=2, h=10, explode=[-70, 0, 0], mass=4,
         info='Beweglicher HDPE-Boden. Die Pistole schiebt ihn nach oben und presst so die Masse heraus.',
         color='#E0DED6', marks=[mark('cyl', 13.5, 13.5, 20, fill='#CFCCC2')]),
    teil('duese', 'pp_nozzle', 'Spritzdüse', 'Düse', 'cyl',
         x=41, y=41, w=12, z=30, h=110, explode=[60, 0, 0], mass=5,
         info='Kegelförmige PP-Düse zum Aufschrauben. Die Spitze schräg anschneiden, je nach Fugenbreite. '
              'Mit ausgehärtetem Silikon in den Restmüll.',
         color=DUESE, marks=[mark('cyl', 3, 3, 6, fill='#CFCFC6'), mark('cyl', 5, 5, 2, fill='#9A9A92')]),
    teil('etikett', 'hdpe_cartridge_tube', 'Etikett', 'Etikett', 'box',
         material_id='paper', x=49.7, y=5, w=0.3, d=30, z=20, h=170, r=0, explode=[35, 0, 0], mass=3,
         materials=[['papier', 80], ['druck', 10], ['klebstoff', 10]],
         info='Bedrucktes Papieretikett mit Gefahrenhinweisen. Kann an der Kartusche bleiben.',
         color='#2F6DB5', sortBias=100),
]

explodiere(teile, abstand=20, gruppen=[['spitze', 'schulter', 'rohr_oben', 'rohr_unten']])
skaliere_masse(teile, oid='silicone_cartridge')
schreibe('silicone_cartridge', teile)
