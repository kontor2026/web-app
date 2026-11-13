"""3D-Modell: electric_toothbrush. Erzeugt tools/kategorien/modelle/electric_toothbrush.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Stehende Schall-/Rotationszahnbürste: Griffrohr Ø 28 mm, Aufsteckbürste oben, Borsten zeigen nach vorne (+y).
# Innenleben (Chassis) wird seitlich (dx > 0) herausgezogen, Aufsteckbürste oben abgehoben.
INNEN = 45  # seitlicher Versatz des Chassis

teile = [
    teil('borsten', 'brush_head', 'Borstenfeld (Nylon)', 'Borsten', 'box', material_id='nylon',
         x=9, y=20, w=10, d=10, z=204, h=24, r=3, mass=1.5, materials=[['nylon', 100]],
         info='Abgerundete Nylonborsten, in den Bürstenkopf eingeschmolzen. Nach drei Monaten ist der Kopf abgenutzt und gehört in den Restmüll.',
         color='#F2F4F5', marks=raster(1.5, 1.5, 3, 3, 2, 2, 3, shape='cyl')),
    teil('aufsteckhals', 'brush_head', 'Aufsteckbürste mit Hals', 'Aufsteckbürste', 'cyl',
         x=8, y=8, w=12, z=182, h=48, mass=7, materials=[['pp', 90], ['stahl', 10]],
         info='Polypropylen mit kleiner Metallfeder innen. Gerade nach oben abziehen; wegen der Feder nicht in die Gelbe Tonne.',
         color='#E9EEF2', marks=[mark('cyl', 3, 3, 6, fill='#9AA2A6')]),
    teil('dichtring', 'plastic_housing', 'Dichtring', 'Dichtring', 'cyl', material_id='silicone',
         x=5, y=5, w=18, z=178, h=4, mass=0.8, materials=[['gummi', 100]],
         info='Silikonring, hält Wasser und Zahnpasta aus dem Griff fern. Ist er rissig, rostet der Motor.',
         color='#5A6670', marks=[mark('cyl', 5, 5, 8, fill='#3A444C')]),
    teil('welle', 'electric_motor', 'Antriebswelle', 'Welle', 'cyl', material_id='steel',
         x=12, y=12, w=4, z=168, h=28, explode=[INNEN, 0, 60], mass=3, materials=[['stahl', 100]],
         info='Edelstahlstift, der die Schwingung des Motors auf die Bürste überträgt. Steckt fest im Motor.',
         color='#B8BEC4'),
    teil('motor', 'electric_motor', 'Schwingmotor', 'Motor', 'cyl',
         x=6, y=6, w=16, z=126, h=40, explode=[INNEN, 0, 50], mass=22,
         materials=[['kupfer', 30], ['stahl', 40], ['ndfeb', 20], ['pcabs', 10]],
         info='Kupferspulen und Neodym-Magnete bringen die Welle zum Schwingen. Magnete sind wertvoll, aber zerbrechlich.',
         marks=[mark('cyl', 2, 2, 12, fill='#B87333'), mark('cyl', 6, 6, 4, fill='#9AA2A6')]),
    teil('platine', 'circuit_board', 'Steuerplatine', 'Platine', 'box',
         x=7, y=13, w=14, d=2, z=74, h=50, r=0.5, explode=[INNEN, 0, 40], mass=6,
         info='Steuert Putzmodi, Timer und Ladung. Ist mit dem Akku verlötet, deshalb nur mit Zange trennen.',
         color='#2F6B3A', marks=[mark('box', 3, 0.3, 4, 1.4, fill='#222')]),
    teil('akku', 'li_ion_battery', 'Lithium-Ionen-Akku (14500)', 'Akku', 'cyl',
         x=7, y=7, w=14, z=21, h=50, explode=[INNEN, 0, 30], mass=19,
         info='Rundzelle mit etwa 800 mAh, an die Platine gelötet. Pole abkleben und zur Batteriesammelstelle bringen.',
         color='#3B6EA5', marks=[mark('cyl', 4, 4, 6, fill='#C9CDD0')]),
    teil('ladespule', 'circuit_board', 'Ladespule (induktiv)', 'Ladespule', 'cyl', material_id='copper',
         x=5, y=5, w=18, z=11, h=8, explode=[INNEN, 0, 20], mass=6, materials=[['kupfer', 60], ['ferrit', 40]],
         info='Kupferspule auf Ferritkern. Nimmt die Energie der Ladestation ohne Kontakt auf, deshalb ist der Griff ganz dicht.',
         color='#B87333', marks=[mark('cyl', 2, 2, 14, fill='#C98A4B'), mark('cyl', 5, 5, 8, fill='#555')]),
    teil('taste', 'plastic_housing', 'Ein-/Aus-Taste', 'Taste', 'box', material_id='rubber',
         x=10, y=26, w=8, d=3, z=118, h=16, r=1.5, explode=[0, 25, 0], mass=1, materials=[['tpu', 100]],
         info='Weiche Kunststoff-Kappe über dem Taster der Platine. Dichtet den Griff gegen Wasser ab.',
         color='#4A7FB5'),
    teil('griff', 'plastic_housing', 'Griffgehäuse', 'Griff', 'cyl',
         x=0, y=0, w=28, z=10, h=168, mass=30, materials=[['pcabs', 85], ['tpu', 15]],
         info='Wasserdichtes Kunststoffrohr mit Gummi-Griffzone. Das Innenleben lässt sich nach oben herausdrücken, oft erst nach Aufschneiden des Bodens.',
         color='#E9EEF2', marks=[mark('cyl', 3, 3, 22, fill='#D5DCE2')]),
    teil('bodenkappe', 'plastic_housing', 'Bodenkappe', 'Boden', 'cyl',
         x=0, y=0, w=28, z=0, h=10, explode=[INNEN, 0, 0], mass=4,
         info='Verschließt den Griff unten und sitzt auf der Ladestation. Meist verklebt oder mit Bajonett verschlossen.',
         color='#C9D1D8'),
]

explodiere(teile, abstand=15, fest=('griff',))
teile[0]['explode'] = list(teile[1]['explode'])  # Borsten bleiben am Aufsteckhals
skaliere_masse(teile, oid='electric_toothbrush')
schreibe('electric_toothbrush', teile)
