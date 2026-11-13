"""3D-Modell: candle_jar. Erzeugt tools/kategorien/modelle/candle_jar.json.

Typische Duftkerze im Glas (Ø 80 mm, 90 mm hoch): dickwandiges Behälterglas mit massivem Boden, Paraffin-
Duftwachs, Baumwolldocht mit Blech-Dochthalter und Papieretikett. Docht und Halter stapeln gemeinsam über dem
Wachs, das Wachs über dem Glas, das Etikett wird seitlich gezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

GLAS = '#D7E7EA'
teile = [
    teil('docht', 'cotton_wick', 'Docht', 'Docht', 'cyl',
         x=38.75, y=38.75, w=2.5, z=10, h=66, mass=0.3,
         info='Geflochtene Baumwolle, mit Wachs getränkt. Aus dem warmen Wachs ziehen; er kommt in den Restmüll.',
         color='#2E2A26'),
    teil('dochthalter', 'wick_holder', 'Dochthalter', 'Dochthalter', 'cyl',
         x=32, y=32, w=16, z=8, h=2, mass=0.6, materials=[['stahl', 95], ['alu', 5]],
         info='Blechplättchen am Glasboden, oft mit einem Klebepunkt festgeklebt. Es hält den Docht gerade. '
              'Mit einem Löffel lösen und zum Metall geben.',
         color='#B9BFC4', marks=[mark('cyl', 6, 6, 4, fill='#8E959B')]),
    teil('wachs', 'paraffin_wax', 'Duftwachs', 'Wachs', 'cyl',
         x=4, y=4, w=72, z=8, h=62, mass=220, materials=[['wachs', 97], ['organisch', 3]],
         info='Paraffin mit Duftöl und Farbe. Reste im warmen Wasserbad schmelzen und ausgießen, '
              'daraus lassen sich neue Kerzen machen. Wachs nie in den Ausguss kippen.',
         color='#E8C9D2', marks=[mark('cyl', 32, 32, 8, fill='#D3AFBA')]),
    teil('glas_wand', 'glass_container', 'Glaswand', 'Glas', 'cyl',
         x=0, y=0, w=80, z=8, h=82, mass=120,
         info='Dickwandiges Behälterglas. Ganz leer und ohne Wachsreste in den Altglascontainer, oder gespült '
              'als Vorratsglas oder Stiftebecher weiterverwenden.',
         color=GLAS, opacity=0.65, marks=[mark('cyl', 4, 4, 72, fill='#EAF2F4')]),
    teil('glas_boden', 'glass_container', 'Glasboden', 'Boden', 'cyl',
         x=0, y=0, w=80, z=0, h=8, mass=60, label=False,
         info='Massiver Boden, damit die Wärme der Flamme den Tisch nicht erreicht.',
         color=GLAS, opacity=0.7),
    teil('etikett', 'glass_container', 'Papieretikett', 'Etikett', 'box',
         material_id='paper', x=80, y=20, w=0.3, d=40, z=25, h=35, r=0, explode=[45, 0, 0], mass=0.5,
         materials=[['papier', 85], ['druck', 8], ['klebstoff', 7]],
         info='Bedrucktes Papier mit Klebstoff. Darf am Glas bleiben, die Glashütte brennt es ab.',
         color='#3F5E4C', sortBias=100),
]
explodiere(teile, abstand=25, nach_liste=True, gruppen=[['docht', 'dochthalter'], ['glas_wand', 'glas_boden']])
skaliere_masse(teile, oid='candle_jar')
schreibe('candle_jar', teile)
