"""3D-Modell: badminton_racket. Erzeugt tools/kategorien/modelle/badminton_racket.json.

Einfacher Freizeit-Badmintonschläger flach liegend, Kopf hinten (y = 0), Griff vorne: 216 × 670 × 28 mm, ca. 90 g.
Ovaler Aluminiumrahmen mit Nylon-Ösenband, Nylonbespannung, Kunststoff-T-Stück, Stahlschaft, Griffkern aus Holz
mit PU-Griffband und Endkappe. Explodiert: Bespannung nach oben, Schaft und Griff entlang der Achse
auseinandergezogen, Griffband zur Seite.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

ALU, SAITE, SAITE_D = '#B8C0C6', '#F1EFE6', '#D9D5C6'
SW, SD = 186, 226  # Saitenfeld (Ellipse)


def saitenbild(ox, oy, fill):
    """Längs- und Quersaiten innerhalb der Ellipse SW × SD, relativ versetzt um ox, oy."""
    out = []
    for i in range(1, 22):
        u = -1 + 2 * i / 22
        lang = SD * math.sqrt(1 - u * u)
        out.append(mark('box', round(ox + SW / 2 * (1 + u) - 0.5, 1), round(oy + (SD - lang) / 2, 1), 1,
                        round(lang, 1), 0, fill))
    for j in range(1, 23):
        v = -1 + 2 * j / 23
        lang = SW * math.sqrt(1 - v * v)
        out.append(mark('box', round(ox + (SW - lang) / 2, 1), round(oy + SD / 2 * (1 + v) - 0.5, 1),
                        round(lang, 1), 1, 0, fill))
    return out


teile = [
    teil('saiten', 'nylon_strings', 'Bespannung', 'Saiten', 'cyl',
         x=15, y=12, w=SW, d=SD, z=17, h=1, mass=5, color=SAITE, opacity=0.2, sortBias=6,
         info='Etwa 10 m Nylonsaite, mit rund 9 kg je Saite gespannt. Vor dem Entsorgen quer in der Mitte '
              'durchschneiden, damit nichts zurückschnellt.',
         marks=saitenbild(0, 0, SAITE_D)),
    teil('oesenband', 'aluminium_racket_frame', 'Ösenband', 'Ösenband', 'cyl',
         material_id='nylon', x=9, y=6, w=SW + 12, d=SD + 12, z=11, h=6, mass=3, form='torus', materials=[['nylon', 100]],
         color='#2B2F33',
         info='Kunststoffband mit kleinen Röhrchen (Ösen), damit die Saiten nicht am scharfen Alurand reißen. '
              'Nach dem Ausschneiden der Saiten lässt es sich herausziehen.',
         marks=[mark('cyl', 6, 6, SW, SD, fill='#E7E5DD')] + [
             mark('cyl', round(SW / 2 + 6 + (SW / 2 + 3) * math.cos(t) - 1.5, 1),
                  round(SD / 2 + 6 + (SD / 2 + 3) * math.sin(t) - 1.5, 1), 3, fill='#8A9096')
             for t in [k * 2 * math.pi / 40 for k in range(40)]]),
    teil('rahmen', 'aluminium_racket_frame', 'Schlägerkopf (Aluminiumrahmen)', 'Rahmen', 'cyl',
         x=2, y=0, w=216, d=250, z=10, h=9, mass=42, form='torus', materials=[['alu', 94], ['nylon', 6]], color=ALU,
         info='Gebogenes Aluminiumprofil mit Kunststoffösen für die Saiten. Ohne Saiten ist der Rahmen Altmetall '
              'für den Wertstoffhof.',
         marks=[mark('cyl', 13, 12, SW, SD, fill='#E7E5DD'), mark('box', 98, 2, 20, 4, 2, '#2B2F33')]),
    teil('t_stueck', 'aluminium_racket_frame', 'T-Stück', 'T-Stück', 'box',
         material_id='abs', x=100, y=245, w=20, d=30, z=9, h=11, r=4, mass=5, color='#2B2F33',
         explode=[0, 20, 0],
         info='Kunststoffverbinder zwischen Kopf und Schaft, verklebt. Mit Heißluft lässt er sich lösen.'),
    teil('schaft', 'aluminium_racket_frame', 'Schaft aus Stahl', 'Schaft', 'box',
         material_id='steel', x=106.5, y=275, w=7, d=195, z=11, h=7, r=3.5, mass=18, form='liegend_y', color='#8E979E',
         explode=[0, 45, 0],
         info='Dünnes Stahlrohr, das den Schlag federnd überträgt. Mit einem Magneten erkennt man: Stahl, kein Alu.',
         marks=[mark('box', 1.5, 60, 4, 50, 2, '#C8323C'), mark('box', 1.5, 115, 4, 12, 2, '#E7E5DD')]),
    teil('griffband', 'racket_grip', 'Griffband', 'Griffband', 'box',
         x=96, y=478, w=28, d=184, z=0, h=28, r=9, mass=7, form='liegend_y', materials=[['kunstleder', 85], ['klebstoff', 15]],
         color='#C8323C', explode=[70, 70, 0],
         info='Spiralförmig gewickeltes PU-Band mit Klebestreifen. Am Ende das Klebeband lösen und abwickeln.',
         marks=[mark('box', 2, 10 + i * 18, 24, 2, 1, '#A32832') for i in range(9)]),
    teil('griff', 'aluminium_racket_frame', 'Griffkern', 'Griffkern', 'box',
         material_id='wood', x=98.5, y=470, w=23, d=192, z=2.5, h=23, r=6, mass=11, form='liegend_y', color='#C9A26B',
         explode=[0, 70, 0],
         info='Achteckiger Kern aus Holz oder Schaum, auf den Schaft geklebt. Er gibt dem Griff seine Form.'),
    teil('endkappe', 'aluminium_racket_frame', 'Endkappe', 'Endkappe', 'box',
         material_id='pp', x=96, y=662, w=28, d=8, z=0, h=28, r=6, mass=2, form='liegend_y', color='#2B2F33',
         explode=[0, 100, 0],
         info='Aufgesteckte Kunststoffkappe am Griffende, oft mit Logo.'),
]
explodiere(teile, abstand=40, fest=('rahmen',), abstaende={'saiten': 60, 'oesenband': 60})
for p in teile:  # Foto-Ansicht: flache marks schweben über runden Formen, dort nur in der Zeichnung
    if p.get('form'):
        p['marks'] = [dict(m, zeichnung=True) for m in p.get('marks') or []]
skaliere_masse(teile, oid='badminton_racket')
schreibe('badminton_racket', teile)
