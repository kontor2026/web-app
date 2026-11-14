"""3D-Modell: skateboard. Erzeugt tools/kategorien/modelle/skateboard.json.

Komplettes Street-Skateboard (8 × 31,5 Zoll) auf den Rollen stehend, Tail hinten (y = 0): 200 × 800 × 100 mm, ca. 2,3 kg.
Ahornholz-Deck mit Griptape, zwei Aluminium-Achsen (Grundplatte, Achsschenkel mit Stahlachse, Königsbolzen,
zwei Lenkgummis), vier PU-Rollen 54 mm mit je zwei Kugellagern, Achsmuttern und acht Montageschrauben.
Rollen liegen quer (Achse in x): jede Rolle aus drei Scheiben, Lager als flache Blöcke.
Explodiert: Achsteile, Deck, Griptape und Schrauben stapeln nach oben, Rollen, Lager und Muttern wandern
entlang der Achse nach außen, Königsbolzen zur Brettmitte.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

W, L = 200, 800
ACHSEN = (('hinten', 175, 70), ('vorne', 625, -70))  # (Name, y-Mitte, dy Königsbolzen)
ALU, ALU_D = '#B9C0C5', '#8F989F'
STAHL, STAHL_D = '#7D868D', '#5C646A'
ROLLE, ROLLE_D = '#F2EEDF', '#D9D3BE'
GUMMI = '#E0A23A'


def spiegel(x, w, rechts):
    return round(W - x - w, 2) if rechts else x


def achse(name, yt, kdy, erste):
    lab = {} if erste else {'label': False}
    stummel = [teil(f'achse_{name}_{s}', 'aluminium_trucks', 'Achse (Stahl)', 'Achse', 'box',
                    material_id='steel', x=spiegel(2, 38, s == 'r'), y=yt - 4, w=38, d=8, z=23, h=8, r=3.5, mass=10, form='liegend_x',
                    materials=[['stahl', 100]], color=STAHL, label=erste and s == 'l',
                    info='Stahlachse, fest in den Achsschenkel eingepresst. Auf ihr sitzen Lager und Rolle.')
               for s in ('l', 'r')]
    return [
        teil(f'grundplatte_{name}', 'aluminium_trucks', 'Grundplatte', 'Grundplatte', 'box',
             x=65, y=yt - 40, w=70, d=80, z=72, h=16, r=8, mass=120, color=ALU, **lab,
             info='Gegossene Aluminiumplatte, mit vier Schrauben unter das Deck geschraubt. Altmetall für den '
                  'Wertstoffhof.',
             marks=[mark('cyl', 14, 8, 9, fill=ALU_D), mark('cyl', 47, 8, 9, fill=ALU_D),
                    mark('cyl', 14, 63, 9, fill=ALU_D), mark('cyl', 47, 63, 9, fill=ALU_D),
                    mark('cyl', 26, 30, 18, fill='#A3ABB1')]),
        teil(f'gummi_oben_{name}', 'aluminium_trucks', 'Lenkgummi brettseitig', 'Lenkgummi', 'cyl',
             material_id='polyurethane', x=86, y=yt - 14, w=28, z=58, h=14, mass=9, materials=[['tpu', 100]],
             color=GUMMI, **lab,
             info='Lenkgummi (Bushing) aus PU. Je weicher, desto leichter lenkt das Brett. Austauschbar.',
             marks=[mark('cyl', 9.5, 9.5, 9, fill='#B47C22')]),
        teil(f'achsschenkel_{name}', 'aluminium_trucks', 'Achsschenkel (Hanger)', 'Achsschenkel', 'box',
             x=40, y=yt - 17, w=120, d=34, z=22, h=36, r=10, mass=165, color=ALU, **lab,
             info='Dreieckiger Aluguss, der beim Lehnen kippt und so lenkt. Die Stahlachse steckt fest darin.',
             marks=[mark('cyl', 50, 7, 20, fill=ALU_D), mark('cyl', 55.5, 12.5, 9, fill='#4A5056')]),
        *stummel,
        teil(f'gummi_unten_{name}', 'aluminium_trucks', 'Lenkgummi straßenseitig', 'Lenkgummi', 'cyl',
             material_id='polyurethane', x=87, y=yt - 13, w=26, z=12, h=10, mass=8, materials=[['tpu', 100]],
             color=GUMMI, label=False,
             info='Zweites, kleineres Lenkgummi unter dem Achsschenkel, mit Unterlegscheibe und Mutter gehalten.',
             marks=[mark('cyl', 8.5, 8.5, 9, fill='#B47C22')]),
        teil(f'koenigsbolzen_{name}', 'aluminium_trucks', 'Königsbolzen mit Mutter', 'Königsbolzen', 'cyl',
             material_id='steel', x=95.5, y=yt - 4.5, w=9, z=8, h=78, mass=25, materials=[['stahl', 100]],
             color=STAHL, explode=[0, kdy, 0], **lab,
             info='Dicker Stahlbolzen, der Grundplatte, Lenkgummis und Achsschenkel zusammenhält. Mutter mit '
                  '14er-Schlüssel lösen.',
             marks=[mark('cyl', 1.5, 1.5, 6, fill=STAHL_D)]),
    ], [p['id'] for p in stummel] + [f'achsschenkel_{name}']


def rad(name, yt, rechts, erste):
    s = -1 if not rechts else 1
    lab = {} if erste else {'label': False}
    rid = f'rad_{name}_{"r" if rechts else "l"}'
    scheiben = []
    for i, (z0, h, d) in enumerate(((0, 4, 26), (4, 7, 44), (11, 32, 54), (43, 7, 44), (50, 4, 26))):
        oben = i == 4
        scheiben.append(teil(
            f'{rid}_{i}', 'pu_wheels', 'Rolle (PU, 54 mm)', 'Rolle', 'box', x=spiegel(5, 32, rechts),
            y=yt - d / 2, w=32, d=d, z=z0, h=h, r=min(6, d / 4), mass=round(95 * h * d / 2560, 1),
            materials=[['tpu', 100]], color=ROLLE, explode=[s * 80, 0, 0],
            label=oben and erste,
            info='Gegossenes, hartes Polyurethan. Nach dem Lösen der Achsmutter einfach von der Achse ziehen.',
            marks=[mark('box', 4, 4, 24, d - 8, 3, ROLLE_D)] if oben else None))
    lager = [
        teil(f'lager_{name}_{"r" if rechts else "l"}_{t}', 'steel_bearings', 'Kugellager 608', 'Kugellager', 'box',
             x=spiegel(x0, 7, rechts), y=yt - 11, w=7, d=22, z=16, h=22, r=2.5, mass=12, form='liegend_x',
             materials=[['stahl', 94], ['nylon', 4], ['gummi', 2]], color='#A7AFB5', explode=[s * dx, 0, 0],
             label=erste and t == 'a',
             info='Zwei Kugellager je Rolle (Typ 608, 22 mm), Stahlkugeln hinter Abdeckscheiben. Mit der Achse '
                  'aus der Rolle hebeln. Stahlschrott.',
             marks=[mark('box', 1, 3, 5, 16, 2, STAHL_D, zeichnung=True)])
        for t, x0, dx in (('a', 6, 120), ('i', 30, 60))
    ]
    mutter = teil(f'mutter_{name}_{"r" if rechts else "l"}', 'aluminium_trucks', 'Achsmutter', 'Achsmutter', 'box',
                  material_id='steel', x=spiegel(0, 5, rechts), y=yt - 6, w=5, d=12, z=21, h=12, r=1.5, mass=3, form='liegend_x',
                  materials=[['stahl', 95], ['nylon', 5]], color=STAHL, explode=[s * 150, 0, 0], label=erste,
                  info='Selbstsichernde Mutter mit Nylonring. Mit dem Skate-Tool (13er) lösen.')
    return scheiben, lager, mutter


schrauben = []
for name, yt, _ in ACHSEN:
    for i, (dx, dy) in enumerate(((-20.5, -27), (20.5, -27), (-20.5, 27), (20.5, 27))):
        schrauben.append(teil(f'schraube_{name}_{i}', 'aluminium_trucks', 'Montageschraube mit Mutter', 'Schraube',
                              'cyl', material_id='steel', x=W / 2 + dx - 4.5, y=yt + dy - 4.5, w=9, z=69, h=30, mass=6,
                              materials=[['stahl', 100]], color='#2E3236',
                              label=not schrauben,
                              info='Senkkopfschraube (Kreuz oder Inbus) von oben durch Griptape und Deck, unten mit '
                                   'Mutter. Mit dem Skate-Tool herausdrehen.',
                              marks=[mark('box', 3.5, 1, 2, 7, 0.5, '#5C646A'), mark('box', 1, 3.5, 7, 2, 0.5, '#5C646A')]))

loecher = [mark('cyl', W / 2 + dx - 4.5, yt + dy - 4.5, 9, fill='#6B5A44')
           for _, yt, _ in ACHSEN for dx in (-20.5, 20.5) for dy in (-27, 27)]
teile = schrauben + [
    teil('griptape', 'grip_tape', 'Griptape', 'Griptape', 'box',
         x=1, y=1, w=W - 2, d=L - 2, z=99, h=1, r=94, mass=80,
         materials=[['keramik', 40], ['pvc', 35], ['klebstoff', 25]], color='#26292C',
         info='Schmirgelartige Folie mit Körnern aus Siliziumcarbid, damit die Schuhe nicht rutschen. Mit dem '
              'Föhn erwärmen und langsam abziehen.',
         marks=[mark('cyl', m['x'] - 1, m['y'] - 1, 9, fill='#55595D') for m in loecher]
         + [mark('box', m['x'] + 2.5, m['y'] + 0.5, 2, 6, 0.5, '#1A1C1E') for m in loecher]
         + [mark('box', m['x'] + 0.5, m['y'] + 2.5, 6, 2, 0.5, '#1A1C1E') for m in loecher]),
    teil('deck', 'wooden_deck', 'Deck aus Ahornholz', 'Deck', 'box',
         x=0, y=0, w=W, d=L, z=88, h=11, r=95, mass=950,
         materials=[['holz', 92], ['klebstoff', 6], ['druck', 2]], color='#D3B07C',
         info='Sieben verleimte Schichten Ahornfurnier, an den Enden hochgebogen (Nose und Tail). Unten oft '
              'bedruckt. Ohne Achsen und Griptape ist es Altholz.',
         marks=loecher),
]
gruppen = []
for k, (name, yt, kdy) in enumerate(ACHSEN):
    tl, gr = achse(name, yt, kdy, k == 0)
    teile += tl
    gruppen.append(gr)
for k, (name, yt, _) in enumerate(ACHSEN):
    for rechts in (False, True):
        sch, lag, mut = rad(name, yt, rechts, k == 0 and not rechts)
        teile += sch + lag + [mut]

explodiere(teile, abstand=25, nach_liste=True, gruppen=gruppen, abstaende={'griptape': 110, **{
    p['id']: 50 for p in schrauben}})
skaliere_masse(teile, oid='skateboard')
schreibe('skateboard', teile)
