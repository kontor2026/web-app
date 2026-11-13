"""3D-Modell: electric_shaver. Erzeugt tools/kategorien/modelle/electric_shaver.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Folienrasierer, stehend: Griff 60 × 35 mm bis z 128, darauf der Scherkopf bis z 150. Vorne = +y.
# Explosion: Gehäuse teilt sich in Vorder- (dy > 0) und Rückschale (dy < 0), Platine mit nach vorne, Taste noch weiter.
# Akku und Motor bleiben stehen, Antriebsbrücke, Klingenblock, Scherkopfrahmen und Scherfolie schweben darüber.

teile = [
    teil('scherfolie', 'shaver_foil_head', 'Scherfolie', 'Scherfolie', 'box', material_id='steel',
         x=6, y=8, w=48, d=19, z=146, h=4, r=6, mass=3, materials=[['nickel', 90], ['stahl', 10]],
         info='Hauchdünne, gelochte Folie aus galvanisch geformtem Nickel. Sehr empfindlich; Nickel kann Allergien auslösen.',
         color='#D5DADE', marks=raster(3, 3, 14, 4, 2, 2, 3, 4, shape='cyl', fill='#9AA2A6')),
    teil('scherkopfrahmen', 'shaver_foil_head', 'Scherkopfrahmen', 'Scherkopf', 'box', material_id='abs',
         x=2, y=3, w=56, d=29, z=128, h=18, r=8, mass=14, materials=[['pcabs', 90], ['stahl', 10]],
         info='Kunststoffrahmen, der die Folie spannt. Seitliche Tasten drücken und den Kopf nach oben abheben.',
         color='#3C4248', marks=[mark('box', 4, 5, 48, 19, 6, fill='#2E3338')]),
    teil('klingenblock', 'shaver_foil_head', 'Klingenblock', 'Klingen', 'box',
         x=8, y=11, w=44, d=13, z=124, h=14, r=2, mass=10, materials=[['stahl', 85], ['pcabs', 15]],
         info='Viele kleine Stahlklingen, die unter der Folie hin- und herschwingen und die Haare abschneiden. Scharf, nicht mit den Fingern abwischen.',
         color='#B8BEC4', marks=raster(2, 2, 20, 1, 1, 9, 2, fill='#7C858C')),
    teil('antrieb', 'electric_motor', 'Antriebsbrücke', 'Antrieb', 'box', material_id='abs',
         x=12, y=8, w=36, d=18, z=112, h=12, r=3, mass=6, materials=[['pcabs', 70], ['stahl', 30]],
         info='Wandelt die Drehung des Motors über einen Exzenter in eine Hin-und-Her-Bewegung um. Kunststoff mit Stahlstift.',
         color='#5F6B75', marks=[mark('cyl', 14, 5, 8, fill='#9AA2A6')]),
    teil('motor', 'electric_motor', 'Gleichstrommotor', 'Motor', 'cyl',
         x=18, y=6, w=24, d=20, z=75, h=35, explode=[0, 0, 0], mass=35,
         materials=[['stahl', 45], ['kupfer', 25], ['ferrit', 20], ['pcabs', 10]],
         info='Kleiner Gleichstrommotor mit Kupferwicklung und Ferritmagnet. An die Platine gelötet; Lötfahnen mit einer Zange abknipsen.',
         color='#9AA2A6', marks=[mark('cyl', 9, 7, 6, fill='#7C858C')]),
    teil('akku', 'li_ion_battery', 'Lithium-Ionen-Akku (14500)', 'Akku', 'cyl',
         x=23, y=10, w=14, z=15, h=50, explode=[0, 0, 0], mass=22,
         info='Rundzelle mit etwa 800 mAh, an die Platine gelötet. Nie anstechen oder biegen; Pole abkleben und zur Batteriesammelstelle bringen.',
         color='#2E86C1', marks=[mark('cyl', 4, 4, 6, fill='#9AA2A6')]),
    teil('platine', 'circuit_board', 'Ladeelektronik', 'Platine', 'box',
         x=8, y=27, w=44, d=3, z=10, h=100, r=0.5, explode=[0, 30, 0], mass=12,
         info='Steuert Laden und Motor und trägt die Ladeanzeige. Mit Akku und Motor verlötet, kommt zum Elektroschrott.',
         color='#2F6B3A', marks=[mark('box', 18, 0.5, 8, 2, 0.5, fill='#222')]),
    teil('vorderschale', 'plastic_housing', 'Vordere Gehäuseschale', 'Vorderschale', 'box',
         x=0, y=17, w=60, d=18, z=0, h=128, r=8, explode=[0, 60, 0], mass=30, materials=[['pcabs', 85], ['tpe', 15]],
         info='Vorderseite mit gummierter Griffzone und Fenster für die Ladeanzeige. Verclipst; mit einem Kunststoffhebel aufziehen.',
         color='#2E3338', marks=[mark('box', 8, 4, 44, 10, 4, fill='#1E2226')]),
    teil('taste', 'plastic_housing', 'Ein-/Aus-Taste', 'Taste', 'box',
         x=22, y=35, w=16, d=3, z=70, h=20, r=1, explode=[0, 85, 0], mass=2,
         info='Kunststofftaste über dem Schalter auf der Platine. Ist nur eingesetzt.',
         color='#9AA2A6'),
    teil('rueckschale', 'plastic_housing', 'Hintere Gehäuseschale', 'Rückschale', 'box',
         x=0, y=0, w=60, d=17, z=0, h=128, r=8, explode=[0, -50, 0], mass=28,
         info='Rückseite mit Ladebuchse unten. Sie ist mit zwei Schrauben unter dem Scherkopf befestigt.',
         color='#3C4248', marks=[mark('box', 8, 3, 44, 10, 4, fill='#2E3338')]),
]

explodiere(teile, abstand=12)
skaliere_masse(teile, oid='electric_shaver')
schreibe('electric_shaver', teile)
