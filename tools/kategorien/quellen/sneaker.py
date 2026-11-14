"""3D-Modell: sneaker. Erzeugt tools/kategorien/modelle/sneaker.json.

Ein Sportschuh (Größe ca. 42), Ferse hinten (y = 0), Spitze vorne (y = 290). 110 × 290 × 120 mm.
Der Schaft ist aus waagrechten Scheiben gebaut, die nach oben zur Ferse hin kürzer werden (Zehenkappe, Rist,
Kragen). In der Foto-Ansicht werden sie zu einer glatten, hohlen Hülle verbunden, oben offen (Einstieg).
Schnürsenkel liegen quer als runde Schnüre auf dem Rist, die Ösen als kleine Ringe daneben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, schreibe  # noqa: E402

OBER = '#ECEAE5'
SOHLE = '#F6F5F1'
SENKEL = '#F4F2EE'


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


SCHAFT = [['polyester', 80], ['tpu', 15], ['schaum', 5]]
# Vorderschaft: Zehenkappe und Rist, nach oben kürzer (die Spitze fällt ab)
vorfuss = schichten('vorfuss', 'textile_upper', 'Obermaterial Vorfuß', 'Obermaterial', 32, [
    (5, 3, 100, 285, 10, 36),
    (6, 4, 98, 280, 10, 35),
    (8, 6, 94, 266, 10, 34),
    (10, 8, 90, 240, 10, 32),
    (12, 8, 86, 206, 10, 31),
], 62,
    'Atmungsaktives Polyester-Netzgewebe mit aufgeschweißten Kunststoff-Verstärkungen. Mit dem Messer entlang der '
    'Sohlennaht abtrennen.', materials=SCHAFT, color=OBER, wand=3)
# Fersenteil: um den Knöchel, oben offen (Einstieg)
ferse = schichten('ferse', 'textile_upper', 'Fersenteil mit Kragen', 'Fersenteil', 82, [
    (13, 6, 84, 170, 10, 30),
    (14, 5, 82, 130, 10, 30),
    (15, 4, 80, 106, 12, 30),
    (16, 3, 78, 96, 12, 30),
], 50,
    'Gepolsterter Schaft rund um Knöchel und Ferse. Mit dem Vorderschaft vernäht und an die Sohle geklebt.',
    materials=[['polyester', 65], ['schaum', 25], ['tpu', 10]], color=OBER, wand=3,
    marks=[mark('box', 0, 0, 78, 96, 38, '#D9D6CF', zeichnung=True), mark('cyl', 9, 8, 60, 80, fill='#C9C6BF', zeichnung=True)])

# Ösen links und rechts der Schnürung, Schnüre quer darüber (Höhe folgt dem Rist)
REIHEN = [(108, 113), (122, 109), (136, 105), (150, 101), (164, 97), (178, 93)]
senkel = [teil(f'senkel_{i}', 'shoelaces', 'Schnürsenkel', 'Schnürsenkel', 'box', form='liegend_x',
               x=36, y=y - 2.5, w=38, d=5, z=z + 1, h=5, mass=1.5, materials=[['polyester', 100]], color=SENKEL,
               label=None if i == 0 else False, explode=[130, 0, 40],
               info='Geflochtenes Polyester mit Kunststoffenden. Ausfädeln: Sie lassen sich weiterverwenden oder mit dem '
                    'Textil abgeben.')
          for i, (y, z) in enumerate(REIHEN)]
senkel.append(teil('senkel_schleife', 'shoelaces', 'Schnürsenkel', 'Schnürsenkel', 'cyl', form='torus',
                   x=40, y=100, w=30, d=14, z=119, h=3.5, mass=1, materials=[['polyester', 100]], color=SENKEL,
                   label=False, explode=[130, 0, 40], info='Schleife des Schnürsenkels.'))
oesen = [teil(f'oese_{i}_{s}', 'textile_upper', 'Ösen', 'Ösen', 'cyl', form='torus', material_id='polyurethane',
              x=x, y=y - 4, w=9, d=8, z=z - 1, h=3, mass=0.3, materials=[['tpu', 100]], color='#C9C6BF',
              label=None if (i, s) == (0, 0) else False, explode=[130, 0, 40],
              info='Verstärkte Schnürlöcher aus Kunststoff, mit dem Obermaterial verschweißt.')
         for i, (y, z) in enumerate(REIHEN) for s, x in enumerate((27, 74))]

teile = senkel + oesen + [
    teil('zunge', 'textile_upper', 'Zunge', 'Zunge', 'box',
         x=33, y=92, w=44, d=26, z=96, h=24, r=12, mass=14, materials=[['polyester', 70], ['schaum', 30]], color=OBER,
         info='Gepolsterte Lasche unter den Schnürsenkeln, oben am Schaft angenäht. Im Inneren steckt Schaumstoff.',
         marks=[mark('box', 12, 6, 20, 10, 2, '#5E656A')]),
    teil('kragen', 'textile_upper', 'Gepolsterter Kragen', 'Kragen', 'cyl', form='torus',
         x=13, y=1, w=84, d=100, z=106, h=12, mass=8, materials=[['polyester', 60], ['schaum', 40]], color='#DAD7D0',
         marks=[mark('cyl', 10, 10, 64, 80, fill='#5E656A', zeichnung=True)],
         info='Schaumgepolsterter Rand um den Einstieg, innen mit Futterstoff bezogen.'),
] + ferse + vorfuss + [
    teil('fersenkappe', 'textile_upper', 'Fersenkappe', 'Fersenkappe', 'box',
         material_id='polyurethane', x=24, y=16, w=62, d=30, z=38, h=36, r=30, sortBias=-40, mass=14, materials=[['tpu', 100]],
         color='#B8BCC0', explode=[-130, 0, 0],
         info='Feste Kunststoffschale zwischen Futter und Obermaterial. Sie hält die Ferse im Schuh stabil.'),
    teil('einlegesohle', 'foam_midsole', 'Einlegesohle', 'Einlegesohle', 'box',
         material_id='pu_foam', x=16, y=14, w=78, d=262, z=35, h=4, r=36, mass=22,
         materials=[['schaum', 85], ['polyester', 15]], color='#5E656A',
         info='Weicher Schaumstoff mit Stoffbezug. Lose eingelegt: einfach herausziehen.',
         marks=[mark('box', 10, 4, 66, 60, 30, '#6E7579')]),
    teil('zwischensohle', 'foam_midsole', 'Zwischensohle (EVA)', 'Zwischensohle', 'box',
         x=3, y=0, w=104, d=290, z=8, h=24, r=48, mass=108, materials=[['schaum', 100]], color=SOHLE,
         info='Leichter EVA-Schaum, der beim Laufen federt. Mit der Laufsohle verklebt: nur mit Heißluft und Messer trennbar.'),
    teil('laufsohle', 'rubber_outsole', 'Laufsohle', 'Laufsohle', 'box',
         x=0, y=0, w=110, d=290, z=0, h=8, r=50, mass=118, materials=[['gummi', 100]], color='#3A3F44',
         info='Abriebfester Gummi mit Profil für Halt. Nach Erwärmen des Klebers von der Zwischensohle abziehen.',
         marks=raster(14, 14, 6, 18, 10, 6, 14, 14.5, r=2, fill='#262B2F')),
]

explodiere(teile, abstand=40, fest=('laufsohle',),
           gruppen=[[p['id'] for p in vorfuss + ferse]])
schreibe('sneaker', teile)
