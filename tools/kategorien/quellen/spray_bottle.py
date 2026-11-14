"""3D-Modell: spray_bottle. Erzeugt tools/kategorien/modelle/spray_bottle.json.

Typische 500-ml-Sprühflasche für Reiniger: ovaler HDPE-Körper (72 × 50 mm) und Pistolen-Sprühkopf
(Trigger) aus PP mit Haube, Düse, Abzug, Kolbenpumpe, Stahlfeder, Verschlussring und Steigrohr.
Die Flasche bleibt stehen, die Triggerteile stapeln darüber, Steigrohr nach links, Etikett nach rechts.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402


def scheiben(teile, pid, n):
    """Foto-Ansicht: hohes Teil in n Scheiben teilen, damit die glatte Hülle (Stapel) nur oben einzieht."""
    i = next(k for k, p in enumerate(teile) if p['id'] == pid)
    p = teile[i]
    zs = [round(p['z'] + k * p['h'] / n, 2) for k in range(n)] + [p['z'] + p['h']]
    neu = []
    for k in range(n):
        q = dict(p, z=zs[k], h=round(zs[k + 1] - zs[k], 2), mass=round(p['mass'] / n, 3))
        if k < n - 1:
            q.update(id=f'{pid}_{k + 1}', label=False, marks=None)
            q = {f: v for f, v in q.items() if v is not None}
        neu.append(q)
    teile[i:i + 1] = neu[::-1]


FLASCHE = '#F2F4F5'
TRIGGER = '#2E8B57'
teile = [
    teil('duese', 'trigger_sprayer', 'Drehdüse', 'Düse', 'box',
         x=84, y=18, w=16, d=14, z=240, h=14, r=3, mass=1,
         info='Drehbare Düsenkappe mit den Stellungen Stopp, Strahl und Sprühnebel.',
         color='#E8C547', marks=[mark('box', 3, 3, 10, 8, 2, '#D4B23A')]),
    teil('haube', 'trigger_sprayer', 'Sprühkopf-Haube', 'Haube', 'box',
         x=24, y=12, w=62, d=26, z=212, h=48, r=8, mass=7,
         info='Äußere Hülle des Sprühkopfs. Darunter sitzen Pumpe, Feder und Ventile. '
              'Den ganzen Sprühkopf abschrauben und mit der Flasche in die Gelbe Tonne geben.',
         color=TRIGGER, marks=[mark('box', 6, 5, 50, 16, 6, '#3A9D66')]),
    teil('feder', 'trigger_sprayer', 'Rückstellfeder', 'Feder', 'cyl',
         material_id='steel', x=34, y=21, w=8, z=218, h=16, mass=0.6, materials=[['stahl', 100]],
         info='Kleine Edelstahlfeder, die den Abzug nach jedem Sprühstoß zurückdrückt. '
              'Sie bleibt im Sprühkopf, Sortieranlagen trennen das Metall heraus.',
         color='#9DA4AA', marks=[mark('cyl', 2, 2, 4, fill='#6E757B')]),
    teil('pumpe', 'trigger_sprayer', 'Kolbenpumpe mit Ventilen', 'Pumpe', 'cyl',
         x=30, y=17, w=16, z=205, h=30, mass=3, materials=[['pp', 80], ['ldpe', 15], ['gummi', 5]],
         info='Zylinder mit Kolben und zwei kleinen Rückschlagventilen: eines saugt aus dem Steigrohr an, '
              'das andere lässt nur zur Düse hin durch.',
         color='#E6E9EC', marks=[mark('cyl', 4, 4, 8, fill='#C9CED3')]),
    teil('abzug', 'trigger_sprayer', 'Abzug (Hebel)', 'Abzug', 'box',
         x=62, y=17, w=12, d=16, z=178, h=40, r=4, mass=2.5,
         info='Beim Ziehen drückt der Hebel den Kolben in die Pumpe, die Flüssigkeit schießt aus der Düse.',
         color=TRIGGER),
    teil('verschlussring', 'trigger_sprayer', 'Verschlussring', 'Verschluss', 'cyl',
         x=20, y=9, w=32, z=188, h=18, mass=4,
         info='Schraubring mit Gewinde, der den Sprühkopf auf der Flasche hält.',
         color=TRIGGER, marks=[mark('cyl', 5, 5, 22, fill='#257048')]),
    teil('hals', 'hdpe_bottle_body', 'Flaschenhals mit Gewinde', 'Hals', 'cyl',
         x=22, y=11, w=28, z=188, h=16, mass=3,
         info='Standardgewinde, auf das der Sprühkopf passt. Deshalb lassen sich Sprühköpfe oft weiterverwenden.',
         color=FLASCHE, wand=2.5, boden=0, marks=[mark('cyl', 4, 4, 20, fill='#D6D9DB', zeichnung=True)]),
    teil('schulter', 'hdpe_bottle_body', 'Flaschenschulter', 'Schulter', 'cyl',
         x=12, y=5, w=48, d=40, z=175, h=13, mass=4,
         info='Übergang vom ovalen Körper zum runden Hals.', color=FLASCHE, label=False),
    teil('rumpf', 'hdpe_bottle_body', 'Flaschenkörper', 'Flasche', 'cyl',
         x=0, y=0, w=72, d=50, z=6, h=169, mass=27,
         info='HDPE, Recyclingcode 2. Reiniger restlos aufbrauchen, nicht mit anderen Reinigern mischen. '
              'Mit Sprühkopf in die Gelbe Tonne.',
         color=FLASCHE),
    teil('boden', 'hdpe_bottle_body', 'Flaschenboden', 'Boden', 'cyl',
         x=2, y=2, w=68, d=46, z=0, h=6, mass=3,
         info='Am Boden sieht man die Quetschnaht und das Recyclingzeichen.', color=FLASCHE, label=False),
    teil('steigrohr', 'trigger_sprayer', 'Steigrohr', 'Steigrohr', 'cyl',
         material_id='ldpe', x=36, y=23, w=4, z=8, h=200, explode=[55, 0, 0], mass=0.8, materials=[['ldpe', 100]],
         info='Schlauch bis fast zum Boden, durch den die Pumpe die Flüssigkeit ansaugt. Bleibt am Sprühkopf.',
         color='#EDEDE8'),
    teil('etikett', 'plastic_label', 'Etikett', 'Etikett', 'cyl',
         x=-1.2, y=-1.2, w=74.4, d=52.4, z=40, h=135, mass=1.2,
         materials=[['pp', 92], ['druck', 5], ['klebstoff', 3]],
         info='PP-Folienetikett rundum mit Gefahrenhinweisen. Passt zum Kunststoffrecycling und darf dranbleiben.',
         color=TRIGGER, sortBias=1, wand=0.4, boden=0, marks=[mark('cyl', 1.7, 1.7, 71, 49, fill=FLASCHE, zeichnung=True)]),
]
# Innenteile zusammengebaut hinter Haube und Flasche zeichnen
for p in teile:
    if p['id'] in ('steigrohr', 'pumpe', 'feder'):
        p['sortBias'] = -60
EX = {'duese': [30, 0, 150], 'haube': [0, 0, 150], 'feder': [0, 0, 92], 'pumpe': [0, 0, 62],
      'abzug': [45, 0, 70], 'verschlussring': [0, 0, 36], 'steigrohr': [-50, 50, 0], 'etikett': [95, 0, 0]}
for p in teile:
    p['explode'] = EX.get(p['id'], [0, 0, 0])
scheiben(teile, 'rumpf', 4)
skaliere_masse(teile, oid='spray_bottle')
schreibe('spray_bottle', teile)
