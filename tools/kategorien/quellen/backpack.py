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
         x=120, y=66, w=60, d=10, z=430, h=24, r=4, form='torus_y', explode=[0, 0, 85], mass=12,
         info='Gurtband aus Polyamid zum Aufhängen. Mehrfach durch den Stoff genäht, deshalb mit der Schere abtrennen.',
         color=DUNKEL),
    teil('rv_haupt', 'metal_zipper', 'Reißverschluss Hauptfach', 'Reißverschluss', 'box',
         x=85, y=66, w=130, d=10, z=440, h=1.5, r=2, explode=[0, 0, 62], mass=22,
         materials=[['polyester', 50], ['messing', 35], ['stahl', 15]],
         info='Läuft über Deckel und Seiten. Zipper und Schieber sind aus Metall: das Band beidseitig abschneiden, '
              'bevor der Stoff in die Textilsammlung geht.',
         color='#2A2E31', marks=[mark('box', 0, 4, 130, 2, 0, '#8E969A'), mark('box', 14, 1, 12, 8, 2, '#B8BEC4'),
                                 mark('box', 104, 1, 12, 8, 2, '#B8BEC4')]),
] + [
    # Hauptfach als Stapel: unten gerade, in der Mitte leicht gebaucht, oben rund zulaufend (Foto-Ansicht: glatte Hülle)
    teil('hauptfach' if i == 0 else f'hauptfach_{i}', 'nylon_fabric', 'Hauptfach', 'Hauptfach', 'box',
         x=x, y=y, w=w, d=d, z=z, h=h, r=r, explode=[0, 0, KOERPER_DZ], mass=m, label=None if i == 0 else False,
         info='Robustes Polyamidgewebe mit wasserdichter PU-Beschichtung auf der Innenseite. Die Beschichtung macht '
              'das Recycling schwer, deshalb lieber reparieren oder weitergeben.',
         color=STOFF)
    for i, (x, y, w, d, z, h, r, m) in enumerate([
        (80, 46, 140, 50, 432, 8, 25, 1), (50, 36, 200, 70, 416, 16, 35, 4), (24, 28, 252, 88, 386, 30, 44, 12),
        (10, 22, 280, 100, 346, 40, 50, 20), (3, 19, 294, 108, 286, 60, 40, 33), (0, 17, 300, 112, 166, 120, 34, 70),
        (0, 18, 300, 110, 46, 120, 32, 70), (0, 20, 300, 105, 6, 40, 30, 30)])
] + [
    teil('boden', 'nylon_fabric', 'Bodenplatte', 'Boden', 'box',
         x=0, y=20, w=300, d=105, z=0, h=6, r=30, explode=[0, 0, 0], mass=45, materials=[['nylon', 60], ['pp', 40]],
         info='Verstärkter Boden mit eingelegter Kunststoffplatte, damit der Rucksack steht. Die Platte vorher herausnehmen.',
         color=DUNKEL),
    teil('rv_vorne', 'metal_zipper', 'Reißverschluss Vortasche', 'RV Vortasche', 'box',
         x=60, y=129, w=180, d=8, z=298, h=1.5, r=2, explode=[0, 80, 22], mass=10,
         materials=[['polyester', 50], ['messing', 35], ['stahl', 15]],
         info='Kleinerer Reißverschluss der Vortasche, ebenfalls mit Metallzähnen.',
         color='#2A2E31', marks=[mark('box', 0, 3, 180, 2, 0, '#8E969A'), mark('box', 20, 0, 12, 8, 2, '#B8BEC4')]),
] + [
    # Vortasche: nach vorne gewölbter Beutel mit rundem oberen Rand
    teil('vortasche' if i == 0 else f'vortasche_{i}', 'nylon_fabric', 'Vortasche', 'Vortasche', 'box',
         x=x, y=125, w=w, d=d, z=z, h=h, r=r, explode=[0, 80, 0], mass=m, label=None if i == 0 else False,
         info='Aufgenähte Tasche für Stifte und Kleinkram, mit Organizer-Fächern innen.', color=STOFF)
    for i, (x, w, d, z, h, r, m) in enumerate([
        (70, 160, 10, 290, 10, 5, 3), (45, 210, 18, 270, 20, 8, 7), (32, 236, 25, 70, 200, 10, 40),
        (36, 228, 20, 48, 22, 10, 6), (44, 212, 12, 40, 8, 6, 2)])
] + [
    teil('polster', 'foam_padding', 'Rückenpolster', 'Polster', 'box',
         x=30, y=8, w=240, d=10, z=80, h=280, r=8, explode=[LINKS, 40, 0], mass=45,
         info='Weicher PU- oder EVA-Schaum, steckt zwischen Netzstoff und Hauptfach. Naht des Innenfutters öffnen und herausziehen.',
         color='#E5E1C8', marks=[mark('box', 4, 2, 232, 6, 3, '#D3CFB4')]),
    teil('rueckenteil', 'nylon_fabric', 'Rückenteil mit Netzstoff', 'Rückenteil', 'box', material_id='polyester',
         x=14, y=4, w=272, d=16, z=40, h=335, r=10, explode=[LINKS, 0, 0], mass=70, materials=[['polyester', 100]],
         info='Atmungsaktiver Polyester-Netzstoff über dem Polster. Liegt direkt am Rücken an.',
         color=NETZ, marks=raster(20, 4, 12, 1, 14, 8, 20, r=3, fill='#3A4045')),
    teil('brustgurt', 'plastic_buckles', 'Brustgurt-Schnalle', 'Brustschnalle', 'box',
         x=120, y=-16, w=60, d=12, z=280, h=22, r=4, explode=[RECHTS, 0, 0], mass=8,
         info='Steckschnalle aus Polyacetal oder Polypropylen. Gurtband direkt hinter der Schnalle abschneiden, '
              'dann ist der Kunststoff sortenrein.',
         color=SCHNALLE, marks=[mark('box', 26, 2, 8, 8, 2, '#3A3F44')]),
    teil('gurt_l', 'nylon_fabric', 'Schultergurt links', 'Schultergurt', 'box',
         x=45, y=-12, w=55, d=16, z=60, h=325, r=8, explode=[RECHTS, 0, 0], mass=60, materials=GURT,
         info='Gepolsterter Gurt: außen Polyamid, innen ein Schaumstreifen. Unten über eine Schnalle verstellbar.',
         color=DUNKEL, marks=[mark('box', 6, 3, 43, 10, 4, NETZ)]),
    teil('gurt_r', 'nylon_fabric', 'Schultergurt rechts', 'Schultergurt', 'box',
         x=200, y=-12, w=55, d=16, z=60, h=325, r=8, explode=[RECHTS, 0, 0], mass=60, materials=GURT, label=False,
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
