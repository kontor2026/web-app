"""3D-Modell: leather_shoe. Erzeugt tools/kategorien/modelle/leather_shoe.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Klassischer Herren-Schnürschuh (Derby, Größe ca. 42), Ferse hinten (y = 0), Spitze vorne (y = 290).
# 110 × 290 × 110 mm. Der Absatz hebt die Ferse um gut 2 cm an, deshalb beginnt der Schaft hinten höher als vorne.
# Explodiert: Ebenen von der Sohle nach oben, Fersenkappe nach links, Schnürsenkel nach rechts.
LEDER = '#5A3522'
DUNKEL = '#40261A'
HELL = '#B88B62'
GUMMI = '#2F2A26'

teile = [
    teil('senkel', 'shoelaces', 'Schnürsenkel', 'Schnürsenkel', 'box',
         x=38, y=100, w=34, d=70, z=96, h=4, r=3, mass=5, materials=[['polyester', 100]], color='#2A2420',
         explode=[130, 0, 40],
         info='Dünne, gewachste Senkel mit Kunststoffenden. Ausfädeln und weiterverwenden.',
         marks=[mark('box', 0, 6 + i * 14, 34, 2.5, 1, '#4A3F38') for i in range(5)]),
    teil('zunge', 'leather_upper', 'Zunge', 'Zunge', 'box',
         x=32, y=90, w=46, d=90, z=72, h=24, r=18, mass=18, materials=[['leder', 100]], color=LEDER,
         info='Weiche Lederlasche unter der Schnürung, am Vorderblatt angenäht.'),
    teil('fersenteil', 'leather_upper', 'Quartiere mit Schnürleiste', 'Quartiere', 'box',
         x=6, y=0, w=98, d=100, z=22, h=83, r=42, mass=85, materials=[['leder', 100]], color=LEDER,
         info='Die beiden seitlichen Lederteile mit den Ösen für die Schnürsenkel, hinten an der Ferse zusammengenäht. '
              'Tragbare Schuhe paarweise in den Schuhcontainer.',
         marks=[mark('cyl', 18, 18, 62, 70, fill=HELL)]
         + [mark('cyl', x, 80 + i * 4.5, 3, fill='#B7BCC0') for i in range(4) for x in (24, 71)]),
    teil('vorderblatt', 'leather_upper', 'Vorderblatt mit Kappe', 'Vorderblatt', 'box',
         x=4, y=95, w=102, d=195, z=10, h=60, r=48, mass=95, materials=[['leder', 100]], color=LEDER,
         info='Ein Stück Glattleder über Zehen und Rist. Der Schaft ist über einen Leisten gezogen und unter die '
              'Brandsohle geklebt: zum Trennen rundherum an der Sohlenkante aufschneiden.',
         marks=[mark('box', 6, 120, 90, 3, 1, DUNKEL), mark('box', 30, 0, 42, 70, 12, DUNKEL)]),
    teil('futter', 'leather_upper', 'Innenfutter', 'Futter', 'box',
         x=10, y=4, w=90, d=200, z=26, h=66, r=40, mass=40, materials=[['leder', 100]], color=HELL,
         info='Dünnes, ungefärbtes Leder innen im Schaft. Es nimmt Fußschweiß auf.'),
    teil('hinterkappe', 'leather_upper', 'Hinterkappe', 'Hinterkappe', 'box',
         material_id='polyurethane', x=12, y=3, w=86, d=42, z=26, h=50, r=34, mass=15, materials=[['tpu', 100]],
         color='#B8BCC0', explode=[-130, 0, 0],
         info='Versteifung aus Kunststoff zwischen Oberleder und Futter. Sie hält die Ferse in Form.'),
    teil('decksohle', 'leather_upper', 'Decksohle', 'Decksohle', 'box',
         x=12, y=6, w=86, d=276, z=25, h=2, r=40, mass=15, materials=[['leder', 100]], color=HELL,
         info='Dünne Lederschicht, auf der der Fuß steht. Meist eingeklebt.',
         marks=[mark('box', 20, 20, 46, 30, 8, '#A07650')]),
    teil('brandsohle', 'leather_upper', 'Brandsohle mit Gelenkfeder', 'Brandsohle', 'box',
         material_id='cardboard', x=8, y=4, w=94, d=282, z=22, h=3, r=42, mass=35,
         materials=[['papier', 60], ['leder', 25], ['stahl', 15]], color='#C9B79C',
         info='Feste Innensohle aus Lederfaserpappe. Ein Stahlstreifen (Gelenkfeder) stützt den Fußbogen.',
         marks=[mark('box', 42, 60, 10, 90, 2, '#8E969A')]),
    teil('laufsohle', 'rubber_outsole', 'Laufsohle', 'Laufsohle', 'box',
         x=0, y=88, w=110, d=202, z=0, h=10, r=48, mass=110, materials=[['gummi', 100]], color=GUMMI,
         info='Profilierte Gummisohle, auf den Schaft geklebt oder genäht. Nach Erwärmen des Klebers abziehen.',
         marks=[mark('box', 4, 4, 102, 194, 44, '#3D3732')] + raster(18, 30, 4, 7, 14, 6, 20, 22, r=2, fill='#221E1B')),
    teil('absatz', 'rubber_outsole', 'Absatz', 'Absatz', 'box',
         x=6, y=0, w=98, d=88, z=0, h=22, r=42, mass=70, materials=[['gummi', 70], ['leder', 30]], color='#3A332E',
         info='Mehrere aufeinandergeklebte Lagen mit einem Gummiflecken unten. Mit kleinen Nägeln befestigt: '
              'vorsichtig abhebeln.',
         marks=[mark('box', 6, 6, 86, 74, 36, GUMMI)]),
]

explodiere(teile, abstand=40, nach_liste=True)
skaliere_masse(teile, oid='leather_shoe')
schreibe('leather_shoe', teile)
