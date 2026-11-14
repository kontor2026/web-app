"""3D-Modell: broom. Erzeugt tools/kategorien/modelle/broom.json.

Typischer Haushaltsbesen (Kopf 300 mm breit, Stiel 1,0 m, gesamt 1,2 m) flach auf dem Tisch: Der Stiel liegt
in Tiefenrichtung (y), vorn am Kopf die Borsten. PP-Kopf mit eingestanzten Borstenbündeln (Drahtanker),
Stielhalter aus Stahlblech, Holzstiel mit Gewinde und Aufhängekappe. Explodiert: Stiel und Kappe in
Stielrichtung herausgedreht, Borsten nach vorn gezogen, Drahtanker und Stielhalter über den Kopf gehoben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

KOPF = '#C8462F'
STAHL = '#A9AFB4'
teile = [
    teil('drahtanker', 'broom_bristles', 'Drahtanker der Borstenbündel', 'Drahtanker', 'box',
         material_id='steel', x=10, y=101, w=280, d=6, z=20, h=40, r=1, explode=[0, -40, 110], mass=12,
         info='Jedes Borstenbündel wird mit einem kleinen Drahtstück in sein Loch gestanzt. Die Anker lassen '
              'sich nicht herausholen, deshalb Kopf und Borsten zusammen entsorgen.',
         color='#9DA4AA', marks=raster(2, 1, 20, 1, 8, 4, 14, fill='#6E767C')),
    teil('schraube_l', 'broom_head', 'Schraube', 'Schraube', 'cyl',
         material_id='steel', x=129, y=160, w=8, z=56, h=19, explode=[0, 30, 130], mass=2,
         materials=[['stahl', 98], ['zink', 2]],
         info='Verzinkte Holzschraube, hält den Stielhalter am Kopf. Mit einem Kreuzschlitz-Schraubendreher lösen.',
         color='#C3C9CE', marks=[mark('box', 1.5, 3.5, 5, 1, 0.3, '#6E767C'), mark('box', 3.5, 1.5, 1, 5, 0.3, '#6E767C')]),
    teil('schraube_r', 'broom_head', 'Schraube', 'Schraube', 'cyl',
         material_id='steel', x=163, y=160, w=8, z=56, h=19, explode=[0, 30, 130], mass=2, label=False,
         materials=[['stahl', 98], ['zink', 2]],
         info='Zweite Schraube des Stielhalters.',
         color='#C3C9CE', marks=[mark('box', 1.5, 3.5, 5, 1, 0.3, '#6E767C'), mark('box', 3.5, 1.5, 1, 5, 0.3, '#6E767C')]),
    teil('borsten', 'broom_bristles', 'Borsten', 'Borsten', 'box',
         x=4, y=0, w=292, d=104, z=6, h=68, r=6, explode=[0, -110, 0], mass=150,
         info='Gekräuselte PP-Fasern in vielen Bündeln. Sind sie abgenutzt, kann man bei vielen Besen nur den '
              'Kopf tauschen und den Stiel weiternutzen.',
         color='#3B3B3D', marks=raster(8, 6, 20, 4, 9, 9, 14, 24, shape='cyl', fill='#2A2A2C')
         + raster(15, 18, 19, 4, 4, 4, 14, 24, shape='cyl', fill='#4A4A4D')),
    teil('stielhalter', 'broom_head', 'Stielhalter', 'Stielhalter', 'box',
         material_id='steel', x=125, y=150, w=50, d=40, z=70, h=4, r=4, explode=[0, 30, 80], mass=31,
         materials=[['stahl', 98], ['zink', 2]],
         info='Verzinktes Blech, mit zwei Schrauben auf den Kopf geschraubt. Es stützt den Stiel, damit er '
              'beim Kehren nicht abbricht. Abschrauben und zum Metallschrott.',
         color=STAHL, marks=[mark('cyl', 3, 9, 10, fill='#7D858B'), mark('cyl', 37, 9, 10, fill='#7D858B'),
                             mark('box', 15, 2, 20, 36, 6, '#BAC0C5')]),
    teil('kopf', 'broom_head', 'Besenkopf', 'Kopf', 'box',
         x=0, y=100, w=300, d=60, z=10, h=60, r=8, explode=[0, 0, 0], mass=260,
         info='Spritzgegossener PP-Körper mit vielen Bohrungen für die Borsten und einem Gewindeloch für den '
              'Stiel. Kopf mit Borsten in den Restmüll oder zum Wertstoffhof.',
         color=KOPF, marks=[mark('box', 6, 6, 288, 48, 6, '#B23C28'), mark('cyl', 138, 30, 24, fill='#7A2A1C'),
                            mark('cyl', 131, 52, 6, fill='#7A2A1C'), mark('cyl', 165, 52, 6, fill='#7A2A1C')]
         + raster(20, 12, 2, 1, 40, 6, 220, r=3, fill='#D35A43')),
    teil('stiel', 'wooden_handle', 'Holzstiel mit Gewinde', 'Stiel', 'box',
         x=138, y=160, w=24, d=1020, z=28, h=24, r=10, explode=[0, 130, 0], mass=280, form='liegend_y',
         info='Buchen- oder Kiefernholz, lackiert, vorn mit Gewinde. Aus dem Kopf herausdrehen: Der Stiel passt '
              'auf einen neuen Kopf oder kommt zum Altholz.',
         color='#C99A62', marks=[dict(m, zeichnung=True) for m in raster(4, 2, 1, 8, 16, 2, 0, 4, r=1, fill='#A87C48')
                                 + [mark('box', 6, 40, 12, 970, 6, '#D7AC76')]]),
    teil('kappe', 'wooden_handle', 'Aufhängekappe', 'Kappe', 'box',
         material_id='pp', x=136, y=1180, w=28, d=20, z=26, h=28, r=8, explode=[0, 180, 0], mass=6, form='liegend_y',
         materials=[['pp', 100]],
         info='Kunststoffkappe mit Loch zum Aufhängen am Stielende. Abziehen und getrennt entsorgen.',
         color=KOPF, marks=[mark('cyl', 8, 4, 12, fill='#7A2A1C', zeichnung=True)]),
]
skaliere_masse(teile, oid='broom')
schreibe('broom', teile)
