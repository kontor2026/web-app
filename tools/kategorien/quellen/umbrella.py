"""3D-Modell: umbrella. Erzeugt tools/kategorien/modelle/umbrella.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Geschlossener Stockschirm liegend, Spitze hinten (y = 0), Rundhakengriff vorne (y = 900) nach oben gebogen.
# Schirmachse bei x = 45, z = 39. Das gebündelte Dach ist ein Stapel aus drei Abschnitten (schmal zur Spitze hin).
# Explodiert: Dach schwebt hoch über dem Gestell, Rippen und Schieber über der Stange, Griff nach vorne (dy > 0),
# Halteband zur Seite (dx > 0).
DACH = '#24476B'
DACH_DZ = 110
GESTELL_DZ = 35
GRIFF_DY = 60
GRIFF = '#5A3A26'

teile = [
    teil('band', 'polyester_canopy', 'Halteband mit Druckknopf', 'Halteband', 'box',
         x=10, y=400, w=70, d=30, z=74, h=2, r=3, explode=[100, 0, 0], mass=6,
         materials=[['polyester', 90], ['messing', 10]],
         info='Hält den geschlossenen Schirm zusammen. Der Druckknopf ist aus Metall: Band abschneiden, bevor der Stoff '
              'in die Textilsammlung geht.',
         color=DACH, marks=[mark('cyl', 54, 9, 12, fill='#C9A24A')]),
    teil('dach_mitte', 'polyester_canopy', 'Schirmdach (gebündelt)', 'Schirmdach', 'box',
         x=10, y=200, w=70, d=280, z=4, h=70, r=30, explode=[0, 0, DACH_DZ], mass=45,
         info='Wasserabweisendes Polyestergewebe aus acht Bahnen, an den Rippenspitzen und in der Mitte angenäht. '
              'Zum Trennen die Nähte an den Rippenenden aufschneiden.',
         color=DACH, marks=[mark('box', 34, 0, 2, 280, 1, '#1B3753')]),
    teil('dach_vorne', 'polyester_canopy', 'Schirmdach (unten, am Schieber)', 'Dach unten', 'box',
         x=6, y=480, w=78, d=215, z=0, h=78, r=34, explode=[0, 0, DACH_DZ], mass=50, label=False,
         info='Hier ist das Dach am dicksten gebündelt, weil die Bahnen an den Rippen-Enden zusammenlaufen.',
         color=DACH, marks=[mark('box', 38, 0, 2, 215, 1, '#1B3753')]),
    teil('dach_spitze', 'polyester_canopy', 'Schirmdach (an der Spitze)', 'Dach oben', 'box',
         x=22, y=30, w=46, d=170, z=16, h=46, r=18, explode=[0, 0, DACH_DZ], mass=15, label=False,
         info='Zur Spitze hin liegen die Bahnen eng um die Stange.',
         color=DACH, marks=[mark('box', 22, 0, 2, 170, 1, '#1B3753')]),
    teil('rippen', 'steel_frame', 'Rippen und Streben', 'Rippen', 'box',
         x=30, y=50, w=30, d=640, z=24, h=30, r=8, explode=[0, 0, GESTELL_DZ], mass=120,
         materials=[['stahl', 85], ['pp', 10], ['messing', 5]],
         info='Acht lange Rippen und acht kurze Streben aus Federstahl, mit Drahtgelenken verbunden. '
              'Abgeknickte Rippen sind spitz: vorsichtig anfassen und als Metallschrott abgeben.',
         color='#3A3F44', marks=raster(3, 10, 4, 1, 2, 620, 7, fill='#8E969A')),
    teil('schieber', 'steel_frame', 'Schieber (Läufer)', 'Schieber', 'box', material_id='pp',
         x=36, y=690, w=18, d=40, z=30, h=18, r=6, explode=[0, 0, GESTELL_DZ], mass=12, materials=[['pp', 100]],
         info='Kunststoffhülse, an der die Streben hängen. Beim Öffnen wird sie die Stange hinaufgeschoben.',
         color='#2A2E31', marks=[mark('box', 3, 4, 12, 32, 4, '#3A3F44')]),
    teil('sperrfeder', 'steel_frame', 'Sperrfeder', 'Feder', 'box',
         x=42, y=735, w=6, d=12, z=36, h=5, r=1, explode=[0, 0, GESTELL_DZ], mass=2,
         info='Kleine Blattfeder in der Stange. Sie rastet ein und hält den Schirm offen.',
         color='#B8BEC4'),
    teil('spitze', 'steel_frame', 'Schirmspitze', 'Spitze', 'box', material_id='pp',
         x=41, y=0, w=8, d=30, z=35, h=8, r=4, mass=8, explode=[0, 0, 0], materials=[['pp', 100]],
         info='Kunststoffkappe auf dem Ende der Stange. Schützt vor Verletzungen und hält das Dach oben fest.',
         color='#2A2E31'),
    teil('stange', 'steel_frame', 'Schirmstange', 'Stange', 'box',
         x=40, y=30, w=10, d=760, z=34, h=10, r=5, explode=[0, 0, 0], mass=70,
         info='Verchromtes Stahlrohr, das Herzstück des Gestells. Lässt sich als Metallschrott verwerten, '
              'wenn Griff und Stoff entfernt sind.',
         color='#B8BEC4', marks=[mark('box', 4, 0, 2, 760, 1, '#E3E7EA')]),
    teil('griff_haken', 'plastic_handle', 'Griff: Hakenende', 'Haken', 'box',
         x=33, y=830, w=24, d=40, z=66, h=24, r=10, explode=[0, GRIFF_DY, 0], mass=15, label=False,
         info='Das umgebogene Ende des Rundhakens.',
         color=GRIFF),
    teil('griff_bogen', 'plastic_handle', 'Griff: Bogen', 'Bogen', 'box',
         x=33, y=870, w=24, d=30, z=26, h=64, r=10, explode=[0, GRIFF_DY, 0], mass=20, label=False,
         info='Die Rundung des Hakengriffs.',
         color=GRIFF),
    teil('griff', 'plastic_handle', 'Hakengriff', 'Griff', 'box',
         x=32, y=780, w=26, d=90, z=26, h=26, r=12, explode=[0, GRIFF_DY, 0], mass=35,
         info='Kunststoff in Holzoptik, mit einer Schraube oder Kleber auf der Stange befestigt. '
              'Schraube lösen und Griff abziehen, dann ist er sortenrein.',
         color=GRIFF, marks=[mark('box', 10, 4, 6, 6, 1, '#9AA2A6')]),
]

skaliere_masse(teile, oid='umbrella')
schreibe('umbrella', teile)
