"""3D-Modell: leather_shoe. Erzeugt tools/kategorien/modelle/leather_shoe.json.

Klassischer Herren-Schnürschuh (Derby, Größe ca. 42), Ferse hinten (y = 0), Spitze vorne (y = 290).
110 × 290 × 106 mm. Der Absatz hebt die Ferse um gut 2 cm an, deshalb beginnt der Schaft hinten höher als vorne.
Der Schaft ist aus waagrechten Scheiben gebaut, die nach oben zur Ferse hin kürzer werden: In der Foto-Ansicht
eine glatte, hohle Lederhülle mit Einstieg. Senkel liegen quer als runde Schnüre, die Ösen als kleine Ringe.
Explodiert: Ebenen von der Sohle nach oben, Hinterkappe nach links, Schnürsenkel nach rechts.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

LEDER = '#5A3522'
DUNKEL = '#40261A'
HELL = '#B88B62'
GUMMI = '#2F2A26'


def schichten(pid, comp, name, short, z0, lagen, mass, info, marks=None, **kw):
    """Scheiben (x, y, w, d, h, r) von unten nach oben, lückenlos ab z0. Die oberste trägt Nummer und marks."""
    vol = sum(w * d * h for _, _, w, d, h, _ in lagen)
    out, z = [], z0
    for i, (x, y, w, d, h, r) in enumerate(lagen):
        oben = i == len(lagen) - 1
        out.append(teil(f'{pid}_{i}', comp, name, short, 'box', x=x, y=y, w=w, d=d, z=z, h=h, r=r,
                        mass=round(mass * w * d * h / vol, 1), info=info, label=None if oben else False,
                        marks=marks if oben else None, **kw))
        z += h
    return out[::-1]


vorderblatt = schichten('vorderblatt', 'leather_upper', 'Vorderblatt mit Kappe', 'Vorderblatt', 10, [
    (4, 96, 102, 192, 12, 36),
    (4, 2, 102, 286, 10, 34),
    (5, 3, 100, 282, 10, 33),
    (7, 4, 96, 268, 10, 32),
    (10, 5, 90, 240, 10, 30),
    (12, 5, 86, 200, 10, 29),
], 95,
    'Ein Stück Glattleder über Zehen und Rist. Der Schaft ist über einen Leisten gezogen und unter die '
    'Brandsohle geklebt: zum Trennen rundherum an der Sohlenkante aufschneiden.',
    materials=[['leder', 100]], color=LEDER, wand=2.5, boden=12)
quartiere = schichten('fersenteil', 'leather_upper', 'Quartiere mit Schnürleiste', 'Quartiere', 72, [
    (14, 4, 82, 150, 10, 28),
    (15, 3, 80, 112, 10, 28),
    (16, 2, 78, 98, 12, 28),
], 85,
    'Die beiden seitlichen Lederteile mit den Ösen für die Schnürsenkel, hinten an der Ferse zusammengenäht. '
    'Tragbare Schuhe paarweise in den Schuhcontainer.',
    materials=[['leder', 100]], color=LEDER, wand=2.5,
    marks=[mark('box', 0, 0, 78, 98, 28, HELL, zeichnung=True)])

REIHEN = [(108, 95), (120, 90), (132, 86), (144, 82), (156, 78)]
senkel = [teil(f'senkel_{i}', 'shoelaces', 'Schnürsenkel', 'Schnürsenkel', 'box', form='liegend_x',
               x=38, y=y - 1.5, w=34, d=3, z=z, h=3, mass=1, materials=[['polyester', 100]], color='#2A2420',
               label=None if i == 0 else False, explode=[130, 0, 40],
               info='Dünne, gewachste Senkel mit Kunststoffenden. Ausfädeln und weiterverwenden.')
          for i, (y, z) in enumerate(REIHEN)]
oesen = [teil(f'oese_{i}_{s}', 'leather_upper', 'Ösen', 'Ösen', 'cyl', form='torus', material_id='steel',
              x=x, y=y - 3.5, w=7, d=7, z=z - 0.5, h=2, mass=0.2, materials=[['stahl', 100]], color='#8C7E62',
              label=None if (i, s) == (0, 0) else False, explode=[130, 0, 40],
              info='Kleine, brünierte Metallösen in den Quartieren. Sie verhindern, dass der Senkel das Leder einreißt.')
         for i, (y, z) in enumerate(REIHEN) for s, x in enumerate((31, 72))]

teile = senkel + oesen + [
    teil('zunge', 'leather_upper', 'Zunge', 'Zunge', 'box',
         x=34, y=90, w=42, d=30, z=90, h=16, r=14, mass=18, materials=[['leder', 100]], color=LEDER,
         info='Weiche Lederlasche unter der Schnürung, am Vorderblatt angenäht.'),
] + quartiere + vorderblatt + [
    teil('futter', 'leather_upper', 'Innenfutter', 'Futter', 'box',
         x=25, y=11, w=60, d=82, z=26, h=77, r=30, wand=1.5, boden=0, sortBias=-40, mass=40, materials=[['leder', 100]], color=HELL,
         info='Dünnes, ungefärbtes Leder innen im Schaft. Es nimmt Fußschweiß auf.'),
    teil('hinterkappe', 'leather_upper', 'Hinterkappe', 'Hinterkappe', 'box',
         material_id='polyurethane', x=24, y=14, w=62, d=30, z=28, h=38, r=30, sortBias=-40, mass=15, materials=[['tpu', 100]],
         color='#B8BCC0', explode=[-130, 0, 0],
         info='Versteifung aus Kunststoff zwischen Oberleder und Futter. Sie hält die Ferse in Form.'),
    teil('decksohle', 'leather_upper', 'Decksohle', 'Decksohle', 'box',
         x=18, y=16, w=74, d=256, z=25, h=2, r=34, mass=15, materials=[['leder', 100]], color=HELL,
         info='Dünne Lederschicht, auf der der Fuß steht. Meist eingeklebt.',
         marks=[mark('box', 20, 20, 46, 30, 8, '#A07650')]),
    teil('brandsohle', 'leather_upper', 'Brandsohle mit Gelenkfeder', 'Brandsohle', 'box',
         material_id='cardboard', x=18, y=16, w=74, d=256, z=22, h=3, r=34, mass=35,
         materials=[['papier', 60], ['leder', 25], ['stahl', 15]], color='#C9B79C',
         info='Feste Innensohle aus Lederfaserpappe. Ein Stahlstreifen (Gelenkfeder) stützt den Fußbogen.',
         marks=[mark('box', 42, 60, 10, 90, 2, '#8E969A')]),
    teil('laufsohle', 'rubber_outsole', 'Laufsohle', 'Laufsohle', 'box',
         x=0, y=88, w=110, d=202, z=0, h=10, r=48, mass=110, materials=[['gummi', 100]], color=GUMMI,
         info='Profilierte Gummisohle, auf den Schaft geklebt oder genäht. Nach Erwärmen des Klebers abziehen.',
         marks=[mark('box', 4, 4, 102, 194, 44, '#3D3732')] + raster(18, 30, 4, 7, 14, 6, 20, 22, r=2, fill='#221E1B')),
    teil('absatz', 'rubber_outsole', 'Absatz', 'Absatz', 'box',
         x=6, y=0, w=98, d=88, z=0, h=22, r=42, mass=70, materials=[['leder', 30], ['gummi', 70]], color='#3A332E',
         info='Mehrere aufeinandergeklebte Lederlagen mit einem Gummiflecken unten. Mit kleinen Nägeln befestigt: '
              'vorsichtig abhebeln.',
         marks=[mark('box', 6, 6, 86, 74, 36, GUMMI)]),
]

explodiere(teile, abstand=40, nach_liste=True, gruppen=[[p['id'] for p in vorderblatt + quartiere]])
skaliere_masse(teile, oid='leather_shoe')
schreibe('leather_shoe', teile)
