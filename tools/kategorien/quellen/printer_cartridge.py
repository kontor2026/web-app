"""3D-Modell: printer_cartridge. Erzeugt tools/kategorien/modelle/printer_cartridge.json.

Typische Tintenpatrone mit integriertem Druckkopf (40 × 60 × 70 mm, aufrecht, Düse unten). Gehäuse aus PP mit
verschweißtem Deckel, innen ein Schaumstoffschwamm, der die Tinte hält. Unten führt ein Sieb aus Edelstahl die Tinte
zum Druckkopf; dessen Düsenplatte ist mit einem Schutzstreifen abgeklebt. Vorn am Kopfteil (y = 58) klebt die
Kontaktfolie mit Chip, explodiert nach vorne gezogen. Sonst wird von unten nach oben gestapelt.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

GEH = '#2B2E33'
teile = [
    teil('deckel', 'ink_cartridge', 'Deckel mit Belüftung', 'Deckel', 'box',
         x=0, y=0, w=40, d=60, z=62, h=8, r=4, mass=5,
         info='Mit dem Gehäuse verschweißt. Die Rillen sind ein Labyrinth, das Luft nachströmen lässt, '
              'aber keine Tinte heraus. Nicht aufbrechen.',
         color=GEH, marks=[mark('box', 4, 4, 32, 30, 2, '#E6E8EA'), mark('box', 7, 8, 18, 4, 0, '#3A3F44'),
                           mark('box', 7, 15, 24, 3, 0, '#9AA3A8'), mark('cyl', 26, 42, 6, fill='#111317')]
         + raster(6, 40, 1, 4, 14, 1.2, 0, 3, fill='#1C1E22')),
    teil('schwamm', 'ink_sponge', 'Tintenschwamm (getränkt)', 'Schwamm', 'box',
         x=3, y=3, w=34, d=54, z=12, h=48, r=3, mass=16, materials=[['schaum', 45], ['tinte', 55]],
         color='#2C3E73',
         info='Polyurethan-Schaum, der die Tinte wie ein Schwamm festhält. Nicht öffnen, die Tinte färbt stark. '
              'Leere Patronen im Handel oder bei Sammelboxen zurückgeben.',
         marks=raster(4, 4, 4, 6, 4, 4, 7, 8, shape='cyl', fill='#24345F')),
    teil('gehaeuse', 'ink_cartridge', 'Patronengehäuse (PP)', 'Gehäuse', 'box',
         x=0, y=0, w=40, d=60, z=10, h=52, r=4, mass=17,
         info='Spritzguss aus Polypropylen. Recyclingfirmen reinigen und befüllen es neu, deshalb die Patrone '
              'nicht zerlegen, sondern ganz zurückgeben.',
         color=GEH, marks=[mark('box', 2.5, 2.5, 35, 55, 3, '#16181B')]),
    teil('sieb', 'ink_cartridge', 'Tintensieb', 'Sieb', 'cyl',
         x=14, y=40, w=12, z=9, h=1, mass=0.3, material_id='steel', color='#B5BCC2',
         info='Feines Edelstahlgewebe, das Schmutz und Luftblasen von den Düsen fernhält.',
         marks=raster(2, 2, 4, 4, 1, 1, 2.2, shape='box', fill='#8A9298')),
    teil('kopfteil', 'ink_cartridge', 'Düsenkopf-Träger', 'Kopfteil', 'box',
         x=6, y=34, w=28, d=24, z=2, h=8, r=2, mass=3,
         info='Schmaler Fuß der Patrone. Ein Kanal führt die Tinte vom Sieb zum Druckkopf.',
         color='#3A3E44'),
    teil('druckkopf', 'cartridge_chip', 'Druckkopf mit Düsenplatte', 'Druckkopf', 'box',
         x=14, y=38, w=12, d=16, z=1, h=1, r=0.5, mass=0.4, material_id='mixed_electronics',
         materials=[['chip', 60], ['nickel', 25], ['kupfer', 15]], color='#C9A94A',
         info='Silizium-Chip mit hunderten winzigen Heizern, darüber eine Platte mit Düsen, feiner als ein Haar. '
              'Nicht mit den Fingern berühren, sonst verstopfen die Düsen.',
         marks=raster(3, 2, 2, 1, 1, 12, 5, fill='#3A3F44')),
    teil('schutzstreifen', 'ink_cartridge', 'Schutzstreifen der Düsen', 'Schutzstreifen', 'box',
         x=6, y=36, w=28, d=20, z=0.5, h=0.3, r=1, mass=0.2, material_id='pp',
         materials=[['pp', 80], ['klebstoff', 20]], color='#E4572E',
         info='Schützt die Düsen vor dem Austrocknen. Vor dem Einsetzen an der Lasche abziehen und in den Restmüll.',
         marks=[mark('box', 2, 2, 24, 3, 0, '#F2F2F2')]),
    teil('kontaktfolie', 'cartridge_chip', 'Kontaktfolie mit Chip', 'Chip', 'box',
         x=8, y=58, w=24, d=0.3, z=2.5, h=7.5, r=0, mass=0.6, color='#C08A2E', sortBias=1,
         info='Biegsame Folie mit vergoldeten Kontakten und einem Speicherchip, der den Füllstand merkt. '
              'Dranlassen, Wiederbefüller nutzen ihn weiter.'),
]
explodiere([p for p in teile if p['id'] != 'kontaktfolie'], abstand=16, abstaende={'druckkopf': 8, 'schutzstreifen': 10})
by = {p['id']: p for p in teile}
by['kontaktfolie']['explode'] = [0, 30, by['kopfteil']['explode'][2] + 14]  # mit dem Kopfteil, nach vorn gezogen
skaliere_masse(teile, oid='printer_cartridge')
schreibe('printer_cartridge', teile)
