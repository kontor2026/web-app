"""3D-Modell: umbrella. Erzeugt tools/kategorien/modelle/umbrella.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Geschlossener Stockschirm liegend, Spitze hinten (y = 0), Rundhakengriff vorne flach auf dem Tisch (J-Form in der
# Draufsicht). Schirmachse bei x = 45, z = 45. 90 × 900 × 90 mm.
# Das gebündelte Dach ist ein Stapel aus vier Abschnitten, die zur Spitze schmaler werden; jeder Abschnitt besteht
# aus drei Scheiben (oben schmal, Mitte breit, unten schmal), damit er rund wirkt. Innen: Stange, Krone,
# Rippenbündel, Schieber und zwei Sperrfedern.
# Explodiert: Dach hoch über dem Gestell, Rippen über Schieber und Federn, Stange unten, Griff nach vorne (dy > 0),
# Spitze nach hinten (dy < 0), Halteband zur Seite (dx > 0).
DACH = '#24476B'
FALTE = '#1B3753'
GRIFF = '#5A3A26'
ACHSE_X, ACHSE_Z = 45, 45
DACH_DZ = 190
RIPPEN_DZ = 95
GRIFF_DY = 70

# Dachabschnitte: (y, d, Durchmesser)
DACH_SEG = [(45, 150, 40), (195, 170, 58), (365, 170, 74), (535, 170, 86)]


def dach():
    out = []
    for i, (y, d, D) in enumerate(DACH_SEG):
        schmal = round(D * 0.7)
        scheiben = [  # (Name, w, z, h)
            ('o', schmal, ACHSE_Z + D / 4, D / 4),
            ('m', D, ACHSE_Z - D / 4, D / 2),
            ('u', schmal, ACHSE_Z - D / 2, D / 4),
        ]
        for name, w, z, h in scheiben:
            haupt = i == 3 and name == 'o'
            marks = []
            if name == 'o':
                marks = [mark('box', w / 2 - 1, 0, 2, d, 1, FALTE), mark('box', w * 0.2, 0, 1.5, d, 1, FALTE),
                         mark('box', w * 0.8 - 1.5, 0, 1.5, d, 1, FALTE)]
            out.append(teil('dach' if haupt else f'dach_{i + 1}{name}', 'polyester_canopy',
                            'Schirmdach (gebündelt)', 'Schirmdach', 'box',
                            x=ACHSE_X - w / 2, y=y, w=w, d=d, z=z, h=h, r=min(w / 2, 20) if name != 'm' else 6,
                            explode=[0, 0, DACH_DZ], mass=D * d / 1000, label=haupt,
                            info=('Wasserabweisendes Polyestergewebe aus acht Bahnen, an den Rippenspitzen und an der '
                                  'Krone angenäht. Zum Trennen die Nähte an den Rippenenden aufschneiden, dann kann '
                                  'der Stoff in die Textilsammlung.') if haupt
                            else 'Teil des zusammengefalteten Schirmdachs.',
                            color=DACH, marks=marks))
    return out


teile = [
    teil('band', 'polyester_canopy', 'Halteband mit Druckknopf', 'Halteband', 'box',
         x=ACHSE_X - 32, y=470, w=64, d=26, z=ACHSE_Z + 37, h=2, r=3, explode=[110, 0, 0], mass=6,
         materials=[['polyester', 90], ['messing', 10]],
         info='Hält den geschlossenen Schirm zusammen. Der Druckknopf ist aus Metall: Band abschneiden, bevor der Stoff '
              'in die Textilsammlung geht.',
         color='#1E3C5A', marks=[mark('cyl', 46, 7, 12, fill='#C9A24A'), mark('cyl', 49, 10, 6, fill='#A8832F')]),
    *dach(),
    teil('kappen', 'steel_frame', 'Rippenkappen (8 Stück)', 'Rippenkappen', 'box', material_id='pp',
         x=ACHSE_X - 22, y=705, w=44, d=12, z=ACHSE_Z - 22, h=44, r=10, explode=[0, 0, DACH_DZ], form='liegend_y',
         mass=8, materials=[['pp', 100]],
         info='Kleine Kunststoffkappen auf den Rippenenden. Das Dach ist hier festgenäht, die Kappen schützen vor '
              'Stichen.',
         color='#2A2E31', marks=raster(6, 2, 4, 1, 6, 8, 9, r=3, fill='#3E444A')),
    teil('krone', 'steel_frame', 'Krone (Rippenhalter)', 'Krone', 'box', material_id='pp',
         x=ACHSE_X - 10, y=45, w=20, d=25, z=ACHSE_Z - 10, h=20, r=8, explode=[0, 0, RIPPEN_DZ], mass=6, sortBias=-5,
         materials=[['pp', 100]],
         info='Kunststoffstern oben an der Stange. Hier sind alle Rippen mit einem Draht eingehängt.',
         color='#2A2E31', marks=[mark('cyl', 4, 6, 12, fill='#3E444A')]),
    teil('rippen', 'steel_frame', 'Rippen und Streben', 'Rippen', 'box',
         x=ACHSE_X - 10, y=70, w=20, d=635, z=ACHSE_Z - 10, h=20, r=6, explode=[0, 0, RIPPEN_DZ], mass=120, sortBias=-5, form='liegend_y',
         materials=[['stahl', 85], ['pp', 10], ['messing', 5]],
         info='Acht lange Rippen und acht kurze Streben aus Federstahl, mit Drahtgelenken verbunden. '
              'Abgeknickte Rippen sind spitz: vorsichtig anfassen und als Metallschrott abgeben.',
         color='#3A3F44', marks=raster(2.5, 10, 4, 1, 1.5, 615, 4.5, fill='#8E969A')),
    teil('schieber', 'steel_frame', 'Schieber (Läufer)', 'Schieber', 'box', material_id='pp',
         x=ACHSE_X - 10, y=600, w=20, d=40, z=ACHSE_Z - 10, h=20, r=6, explode=[0, 0, 40], mass=12,
         materials=[['pp', 100]],
         info='Kunststoffhülse, an der die Streben hängen. Beim Öffnen wird sie die Stange hinaufgeschoben.',
         color='#2A2E31', marks=[mark('box', 4, 4, 12, 32, 4, '#3E444A')]),
    teil('feder_oben', 'steel_frame', 'Sperrfeder (offen)', 'Federn', 'box',
         x=ACHSE_X - 2, y=470, w=4, d=14, z=ACHSE_Z + 1, h=5.5, r=1, explode=[0, 0, 22], mass=1,
         info='Zwei kleine Blattfedern in der Stange. Die obere rastet ein und hält den Schirm offen, '
              'die untere hält ihn geschlossen.',
         color='#B8BEC4'),
    teil('feder_unten', 'steel_frame', 'Sperrfeder (geschlossen)', 'Feder', 'box',
         x=ACHSE_X - 2, y=660, w=4, d=14, z=ACHSE_Z + 1, h=5.5, r=1, explode=[0, 0, 22], mass=1, label=False,
         info='Hält den Schieber unten, solange der Schirm geschlossen ist.', color='#B8BEC4'),
    teil('spitze', 'steel_frame', 'Schirmspitze', 'Spitze', 'box',
         x=ACHSE_X - 4, y=0, w=8, d=45, z=ACHSE_Z - 4, h=8, r=4, explode=[0, -40, 0], mass=6, form='liegend_y',
         materials=[['stahl', 70], ['pp', 30]],
         info='Vernickelte Metallspitze am Ende der Stange, mit Kunststoffkappe gegen Verletzungen.',
         color='#B8BEC4', marks=[mark('box', 1, 0, 6, 8, 3, '#2A2E31')]),
    teil('stange', 'steel_frame', 'Schirmstange', 'Stange', 'box',
         x=ACHSE_X - 5, y=45, w=10, d=755, z=ACHSE_Z - 5, h=10, r=5, explode=[0, 0, 0], mass=70, form='liegend_y',
         info='Verchromtes Stahlrohr, das Herzstück des Gestells. Lässt sich als Metallschrott verwerten, '
              'wenn Griff und Stoff entfernt sind.',
         color='#B8BEC4', marks=[mark('box', 4, 0, 2, 755, 1, '#E3E7EA', zeichnung=True),
                                 mark('box', 3, 427, 4, 12, 1, '#5A6268'), mark('box', 3, 617, 4, 12, 1, '#5A6268')]),
    # Rundhakengriff flach liegend: Schaft, Bogen, zurücklaufendes Hakenende (J-Form)
    teil('griff', 'plastic_handle', 'Hakengriff', 'Griff', 'box',
         x=ACHSE_X - 13, y=770, w=26, d=95, z=ACHSE_Z - 13, h=26, r=12, explode=[0, GRIFF_DY, 0], mass=30, form='liegend_y',
         info='Kunststoff in Holzoptik, mit einer Schraube oder Kleber auf der Stange befestigt. '
              'Schraube lösen und Griff abziehen, dann ist er sortenrein.',
         color=GRIFF, marks=[mark('cyl', 9, 4, 8, fill='#9AA2A6'), mark('box', 5, 20, 3, 70, 1.5, '#6B4630', zeichnung=True),
                             mark('box', 15, 25, 2, 60, 1, '#6B4630', zeichnung=True)]),
    teil('griff_bogen', 'plastic_handle', 'Griff: Bogen', 'Bogen', 'box',
         x=ACHSE_X - 13, y=865, w=56, d=35, z=ACHSE_Z - 13, h=26, r=16, explode=[0, GRIFF_DY, 0], mass=20, form='liegend_x',
         label=False, info='Die Rundung des Hakengriffs.', color=GRIFF,
         marks=[mark('box', 10, 6, 36, 3, 1.5, '#6B4630', zeichnung=True)]),
    teil('griff_haken', 'plastic_handle', 'Griff: Hakenende', 'Haken', 'box',
         x=ACHSE_X + 17, y=815, w=26, d=50, z=ACHSE_Z - 13, h=26, r=12, explode=[0, GRIFF_DY, 0], mass=12, form='liegend_y',
         label=False, info='Das zurückgebogene Ende des Rundhakens. Damit hängt man den Schirm auf.',
         color=GRIFF, marks=[mark('box', 11, 6, 3, 40, 1.5, '#6B4630', zeichnung=True)]),
]

for p in teile:  # Foto-Ansicht: flache marks schweben über runden Formen, dort nur in der Zeichnung
    if p.get('form'):
        p['marks'] = [dict(m, zeichnung=True) for m in p.get('marks') or []]
skaliere_masse(teile, oid='umbrella')
schreibe('umbrella', teile)
