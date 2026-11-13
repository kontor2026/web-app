"""3D-Modell: candle_jar. Erzeugt tools/kategorien/modelle/candle_jar.json.

Typische Duftkerze im Glas (Ø 80 mm, 90 mm hoch): dickwandiges Behälterglas mit massivem Boden, Paraffin-
Duftwachs bis etwa 2 cm unter den Rand, Baumwolldocht mit Blech-Dochthalter und rundum geklebtem Papieretikett.
Docht und Halter stapeln gemeinsam über dem Wachs, das Wachs über dem Glas, das Etikett wird nach rechts gezogen.
Das Glas wird zuerst gezeichnet, damit man das Wachs durch das Glas sieht.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

GLAS = '#D7E7EA'
WACHS = '#E8C9D2'
C = 40


def rund(w, z, h):
    return dict(x=C - w / 2, y=C - w / 2, w=w, z=z, h=h)


teile = [
    teil('docht', 'cotton_wick', 'Docht', 'Docht', 'cyl', **rund(2.5, 70, 9), mass=0.05,
         color='#2E2A26', marks=[mark('cyl', 0.5, 0.5, 1.5, fill='#111')],
         info='Geflochtene Baumwolle, mit Wachs getränkt. Die verkohlte Spitze vor dem Anzünden auf 5 mm kürzen. '
              'Aus dem warmen Wachs ziehen, er kommt in den Restmüll.'),
    teil('docht_innen', 'cotton_wick', 'Docht', 'Docht', 'cyl', **rund(2.5, 10, 60), mass=0.25,
         color='#2E2A26', label=False, sortBias=-20,
         info='Der Docht steckt bis zum Boden im Wachs. Das geschmolzene Wachs steigt in ihm nach oben und verbrennt.'),
    teil('dochthalter', 'wick_holder', 'Dochthalter', 'Dochthalter', 'cyl', **rund(16, 8, 2), mass=0.6, sortBias=-20,
         materials=[['stahl', 95], ['klebstoff', 5]], color='#B9BFC4',
         marks=[mark('cyl', 5, 5, 6, fill='#8E959B')],
         info='Blechplättchen am Glasboden, mit einem Klebepunkt festgeklebt. Es hält den Docht gerade und '
              'löscht die Flamme, bevor das Glas zu heiß wird. Mit einem Löffel lösen und zum Metall geben.'),
    teil('wachs', 'paraffin_wax', 'Duftwachs', 'Wachs', 'cyl', **rund(72, 8, 62), mass=220,
         materials=[['wachs', 97], ['organisch', 3]], color=WACHS,
         marks=[mark('cyl', 6, 6, 60, fill='#EDD3DB'), mark('cyl', 31, 31, 10, fill='#D3AFBA')],
         info='Paraffin mit Duftöl und Farbe. Reste im warmen Wasserbad schmelzen und ausgießen, daraus lassen '
              'sich neue Kerzen machen. Wachs nie in den Ausguss kippen.'),
    teil('glas_rand', 'glass_container', 'Glasrand', 'Glas', 'cyl', **rund(80, 70, 20), mass=35,
         color=GLAS, opacity=0.45, sortBias=-25, marks=[mark('cyl', 4, 4, 72, fill='#EEF5F6')],
         info='Dickwandiges Behälterglas. Ganz leer und ohne Wachsreste in den Altglascontainer, oder gespült '
              'als Vorratsglas oder Stiftebecher weiterverwenden.'),
    teil('glas_wand', 'glass_container', 'Glaswand', 'Glas', 'cyl', **rund(80, 8, 62), mass=85,
         color=GLAS, opacity=0.45, sortBias=-25, label=False,
         info='Dickwandiges Behälterglas, es hält die Hitze der Flamme aus.'),
    teil('glas_boden', 'glass_container', 'Glasboden', 'Boden', 'cyl', **rund(80, 0, 8), mass=60,
         color=GLAS, opacity=0.6, label=False,
         info='Massiver Boden, damit die Wärme der Flamme den Tisch nicht erreicht.'),
    teil('etikett', 'glass_container', 'Papieretikett', 'Etikett', 'cyl', **rund(80.6, 10, 26), explode=[115, 0, 0],
         material_id='paper', mass=0.5, materials=[['papier', 85], ['druck', 8], ['klebstoff', 7]],
         color='#3F5E4C', sortBias=40, marks=[mark('cyl', 0.8, 0.8, 79, fill='#B59DA4')],
         info='Bedrucktes Papier mit Klebstoff. Darf am Glas bleiben, die Glashütte brennt es ab.'),
]
explodiere(teile, abstand=25, nach_liste=True,
           gruppen=[['docht', 'docht_innen', 'dochthalter'], ['glas_rand', 'glas_wand', 'glas_boden']])
skaliere_masse(teile, oid='candle_jar')
schreibe('candle_jar', teile)
