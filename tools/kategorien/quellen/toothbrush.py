"""3D-Modell: toothbrush. Erzeugt tools/kategorien/modelle/toothbrush.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Handzahnbürste auf dem Rücken liegend, Borsten nach oben (laut CSV 20 × 190 × 20 mm), Kopf hinten (y = 0).
# Griffkörper aus PP (Kopf, Hals, Griff aus einem Stück) mit aufgespritzter Weichgummi-Griffzone.
# Die Borstenbüschel stecken in Bohrungen im Kopf und werden von kleinen Metallankern gehalten.
# Explodiert: Borsten über die Anker über den Kopf, Griffpolster über den Griff.
PP = '#3B7DD8'

teile = [
    *[teil('borsten_spitze' if i == 0 else f'borsten_spitze_{i}', 'nylon_bristles', 'Indikatorborsten', 'Indikator', 'cyl',
           x=5.0 + 2.6 * i, y=2.6, w=2.4, z=9, h=12, mass=0.05, sortBias=-1.5, color='#3B9BD8', label=(i == 0),
           info='Gefärbte Büschel vorne am Kopf. Wenn die Farbe verblasst, ist es Zeit für eine neue Bürste.'
           if i == 0 else 'Ein gefärbtes Borstenbüschel.') for i in range(4)],
    *[teil('borsten' if k == 0 else f'borsten_{k}', 'nylon_bristles', 'Borstenfeld', 'Borsten', 'cyl',
           x=5.0 + 2.6 * (k % 4), y=6.9 + 3.1 * (k // 4), w=2.4, z=9, h=11, mass=0.8 / 24, color='#F4F6F8',
           label=(k == 0),
           info='Rund 30 Büschel aus Nylonfäden mit abgerundeten Enden. Wer sauberen Kunststoff will, zieht sie mit einer Zange heraus.'
           if k == 0 else 'Ein Borstenbüschel aus Nylon.') for k in range(24)],
    teil('anker', 'nylon_bristles', 'Borstenanker', 'Anker', 'box', material_id='copper',
         x=5, y=2, w=10, d=24, z=7.5, h=1.5, r=2, mass=0.2, materials=[['messing', 100]],
         info='Winzige Metallplättchen aus Messingdraht, die jedes Büschel in der Bohrung festklemmen. '
              'Sie gehen beim Herausziehen der Borsten mit.',
         color='#C9A74C', marks=raster(0.4, 0.8, 4, 8, 1.6, 0.6, 2.6, 3.1, fill='#8F7430')),
    teil('griffpolster', 'toothbrush_handle', 'Weiche Griffzone', 'Griffpolster', 'box', material_id='rubber',
         x=5, y=80, w=10, d=50, z=12, h=1.5, r=5, mass=1.2, materials=[['tpe', 100]],
         info='Weicher Kunststoff (TPE), direkt auf den Griff gespritzt. Er lässt sich nicht abziehen, '
              'deshalb ist die ganze Zahnbürste Restmüll.',
         color='#9CD3F0', marks=raster(2.5, 4, 1, 7, 5, 3, 0, 6.5, r=1.5, fill='#7FBEDF')),
    teil('kopf', 'toothbrush_handle', 'Bürstenkopf', 'Kopf', 'box',
         x=4, y=0, w=12, d=28, z=4, h=5, r=5, mass=1.2,
         info='Der Kopf hat Bohrungen für die Borstenbüschel. Zahnärzte empfehlen, die Bürste alle drei Monate zu wechseln.',
         color=PP),
    teil('daumenauflage', 'toothbrush_handle', 'Daumenauflage', 'Daumen', 'box', material_id='rubber',
         x=7.5, y=40, w=5, d=14, z=9, h=1, r=2.5, mass=0.2, materials=[['tpe', 100]],
         info='Kleines geriffeltes Gummipolster am Hals, auf dem der Daumen liegt. Angespritzt, nicht lösbar.',
         color='#9CD3F0', marks=raster(1, 1.5, 1, 4, 3, 1.2, 0, 3, r=0.5, fill='#7FBEDF')),
    teil('hals', 'toothbrush_handle', 'Hals', 'Hals', 'box',
         x=6.5, y=28, w=7, d=32, z=3, h=6, r=3, form='liegend_y', mass=1.1,
         info='Schmaler, leicht federnder Übergang zwischen Kopf und Griff.', color=PP),
    teil('griff', 'toothbrush_handle', 'Griff', 'Griff', 'box',
         x=2, y=60, w=16, d=130, z=0, h=12, r=7, form='liegend_y', mass=10.3,
         info='Massiver Griffkörper aus Polypropylen. Es gibt auch Bürsten mit Wechselköpfen oder aus Holz, die weniger Plastikmüll machen.',
         color=PP, marks=[mark('box', 3, 20, 10, 50, 5, '#9CD3F0', zeichnung=True)]),
]

BUESCHEL = [p['id'] for p in teile if p['id'].startswith('borsten')]
explodiere(teile, abstand=12, gruppen=[['kopf', 'hals', 'griff'], BUESCHEL], abstaende={'daumenauflage': 8})
skaliere_masse(teile, oid='toothbrush', stellen=2)
schreibe('toothbrush', teile)
