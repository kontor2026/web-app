"""3D-Modell: backpack. Erzeugt tools/kategorien/modelle/backpack.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Schulrucksack aufrecht (laut CSV 300 × 150 × 450 mm), Rücken hinten (y = 0), Vortasche vorne.
# Explodiert: Hauptfach hebt vom Boden ab, Reißverschluss und Tragegriff schweben darüber, Vortasche nach vorne
# (dy > 0), Rückenteil mit Polster nach links, Schultergurte mit Schnallen nach rechts.
STOFF = '#2F4B6E'
DUNKEL = '#22374F'
NETZ = '#4A5156'
SCHNALLE = '#1E2226'
KOERPER_DZ = 40
LINKS, RECHTS = -320, 320
GURT = [['nylon', 75], ['schaum', 25]]

teile = [
    teil('griff', 'nylon_fabric', 'Tragegriff', 'Griff', 'box',
         x=120, y=64, w=60, d=18, z=441, h=9, r=6, explode=[0, 0, 85], mass=12,
         info='Gurtband aus Polyamid zum Aufhängen. Mehrfach durch den Stoff genäht, deshalb mit der Schere abtrennen.',
         color=DUNKEL),
    teil('rv_haupt', 'metal_zipper', 'Reißverschluss Hauptfach', 'Reißverschluss', 'box',
         x=15, y=68, w=270, d=10, z=440, h=1.5, r=2, explode=[0, 0, 62], mass=22,
         materials=[['polyester', 50], ['messing', 35], ['stahl', 15]],
         info='Läuft über Deckel und Seiten. Zipper und Schieber sind aus Metall: das Band beidseitig abschneiden, '
              'bevor der Stoff in die Textilsammlung geht.',
         color='#2A2E31', marks=[mark('box', 0, 4, 270, 2, 0, '#8E969A'), mark('box', 30, 1, 12, 8, 2, '#B8BEC4'),
                                 mark('box', 228, 1, 12, 8, 2, '#B8BEC4')]),
    teil('hauptfach', 'nylon_fabric', 'Hauptfach', 'Hauptfach', 'box',
         x=0, y=20, w=300, d=105, z=6, h=434, r=30, explode=[0, 0, KOERPER_DZ], mass=240,
         info='Robustes Polyamidgewebe mit wasserdichter PU-Beschichtung auf der Innenseite. Die Beschichtung macht '
              'das Recycling schwer, deshalb lieber reparieren oder weitergeben.',
         color=STOFF, marks=[mark('box', 15, 48, 270, 2, 0, DUNKEL)]),
    teil('boden', 'nylon_fabric', 'Bodenplatte', 'Boden', 'box',
         x=0, y=20, w=300, d=105, z=0, h=6, r=30, explode=[0, 0, 0], mass=45, materials=[['nylon', 60], ['pp', 40]],
         info='Verstärkter Boden mit eingelegter Kunststoffplatte, damit der Rucksack steht. Die Platte vorher herausnehmen.',
         color=DUNKEL),
    teil('rv_vorne', 'metal_zipper', 'Reißverschluss Vortasche', 'RV Vortasche', 'box',
         x=40, y=132, w=220, d=8, z=300, h=1.5, r=2, explode=[0, 80, 22], mass=10,
         materials=[['polyester', 50], ['messing', 35], ['stahl', 15]],
         info='Kleinerer Reißverschluss der Vortasche, ebenfalls mit Metallzähnen.',
         color='#2A2E31', marks=[mark('box', 0, 3, 220, 2, 0, '#8E969A'), mark('box', 20, 0, 12, 8, 2, '#B8BEC4')]),
    teil('vortasche', 'nylon_fabric', 'Vortasche', 'Vortasche', 'box',
         x=30, y=125, w=240, d=25, z=40, h=260, r=10, explode=[0, 80, 0], mass=60,
         info='Aufgenähte Tasche für Stifte und Kleinkram, mit Organizer-Fächern innen.',
         color=STOFF, marks=[mark('box', 10, 3, 220, 2, 0, DUNKEL)]),
    teil('polster', 'foam_padding', 'Rückenpolster', 'Polster', 'box',
         x=30, y=8, w=240, d=10, z=80, h=320, r=8, explode=[LINKS, 40, 0], mass=45,
         info='Weicher PU- oder EVA-Schaum, steckt zwischen Netzstoff und Hauptfach. Naht des Innenfutters öffnen und herausziehen.',
         color='#E5E1C8', marks=[mark('box', 4, 2, 232, 6, 3, '#D3CFB4')]),
    teil('rueckenteil', 'nylon_fabric', 'Rückenteil mit Netzstoff', 'Rückenteil', 'box', material_id='polyester',
         x=10, y=4, w=280, d=16, z=40, h=380, r=10, explode=[LINKS, 0, 0], mass=70, materials=[['polyester', 100]],
         info='Atmungsaktiver Polyester-Netzstoff über dem Polster. Liegt direkt am Rücken an.',
         color=NETZ, marks=raster(20, 4, 12, 1, 14, 8, 20, r=3, fill='#3A4045')),
    teil('brustgurt', 'plastic_buckles', 'Brustgurt-Schnalle', 'Brustschnalle', 'box',
         x=120, y=-16, w=60, d=12, z=280, h=22, r=4, explode=[RECHTS, 0, 0], mass=8,
         info='Steckschnalle aus Polyacetal oder Polypropylen. Gurtband direkt hinter der Schnalle abschneiden, '
              'dann ist der Kunststoff sortenrein.',
         color=SCHNALLE, marks=[mark('box', 26, 2, 8, 8, 2, '#3A3F44')]),
    teil('gurt_l', 'nylon_fabric', 'Schultergurt links', 'Schultergurt', 'box',
         x=45, y=-12, w=55, d=16, z=60, h=360, r=8, explode=[RECHTS, 0, 0], mass=60, materials=GURT,
         info='Gepolsterter Gurt: außen Polyamid, innen ein Schaumstreifen. Unten über eine Schnalle verstellbar.',
         color=DUNKEL, marks=[mark('box', 6, 3, 43, 10, 4, NETZ)]),
    teil('gurt_r', 'nylon_fabric', 'Schultergurt rechts', 'Schultergurt', 'box',
         x=200, y=-12, w=55, d=16, z=60, h=360, r=8, explode=[RECHTS, 0, 0], mass=60, materials=GURT, label=False,
         info='Gegenstück zum linken Schultergurt.', color=DUNKEL, marks=[mark('box', 6, 3, 43, 10, 4, NETZ)]),
    teil('schnalle_l', 'plastic_buckles', 'Leiterschnalle links', 'Leiterschnalle', 'box',
         x=52, y=-12, w=40, d=12, z=36, h=18, r=3, explode=[RECHTS, 0, 0], mass=5,
         info='Zum Verstellen der Gurtlänge. Kleine Kunststoffteile wie diese gehören in den Restmüll.',
         color=SCHNALLE, marks=[mark('box', 4, 4, 32, 4, 1, '#3A3F44')]),
    teil('schnalle_r', 'plastic_buckles', 'Leiterschnalle rechts', 'Leiterschnalle', 'box',
         x=207, y=-12, w=40, d=12, z=36, h=18, r=3, explode=[RECHTS, 0, 0], mass=5, label=False,
         info='Gegenstück zur linken Leiterschnalle.',
         color=SCHNALLE, marks=[mark('box', 4, 4, 32, 4, 1, '#3A3F44')]),
]

skaliere_masse(teile, oid='backpack')
schreibe('backpack', teile)
