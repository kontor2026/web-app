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
    teil('borsten', 'nylon_bristles', 'Borstenfeld', 'Borsten', 'box',
         x=4.5, y=1.5, w=11, d=25, z=9, h=11, r=4, mass=1.0,
         info='Rund 30 Büschel aus Nylonfäden mit abgerundeten Enden. Wer sauberen Kunststoff will, zieht sie mit einer Zange heraus.',
         color='#F4F6F8', marks=raster(0.7, 0.5, 4, 8, 2, 2, 2.6, 3.1, shape='cyl', fill='#BFE3F5')),
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
    teil('hals', 'toothbrush_handle', 'Hals', 'Hals', 'box',
         x=6.5, y=28, w=7, d=32, z=3, h=6, r=3, mass=1.1,
         info='Schmaler, leicht federnder Übergang zwischen Kopf und Griff.', color=PP),
    teil('griff', 'toothbrush_handle', 'Griff', 'Griff', 'box',
         x=2, y=60, w=16, d=130, z=0, h=12, r=7, mass=10.3,
         info='Massiver Griffkörper aus Polypropylen. Es gibt auch Bürsten mit Wechselköpfen oder aus Holz, die weniger Plastikmüll machen.',
         color=PP, marks=[mark('box', 3, 20, 10, 50, 5, '#9CD3F0')]),
]

explodiere(teile, abstand=12, gruppen=[['kopf', 'hals', 'griff']])
skaliere_masse(teile, oid='toothbrush', stellen=2)
schreibe('toothbrush', teile)
