"""3D-Modell: led_bulb. Erzeugt tools/kategorien/modelle/led_bulb.json.

Typische LED-Lampe in Birnenform (A60, E27, etwa 9 W). Steht auf dem Sockel. Kolben und Kühlkörper bestehen aus
mehreren Scheiben, die sich jeweils gemeinsam bewegen. Explodiert wird senkrecht gestapelt (jede Gruppe schwebt
über der Oberkante der darunter), die senkrecht stehende Treiberplatine wird seitlich (dx positiv) herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, schreibe  # noqa: E402

KOLBEN = '#F4F4F0'
ALU = '#C9CDD0'


def led_ring(n, rad, mitte, groesse=3):
    """n LED-Chips im Kreis, als marks relativ zum Teil."""
    import math
    return [mark('box', round(mitte + rad * math.cos(2 * math.pi * i / n) - groesse / 2, 2),
                 round(mitte + rad * math.sin(2 * math.pi * i / n) - groesse / 2, 2), groesse, groesse, 0.3, '#F6D86B')
            for i in range(n)]


teile = [
    teil('kolben_oben', 'bulb_diffuser', 'Streukolben (Kuppe)', 'Kolben', 'cyl',
         x=10, y=10, w=40, z=98, h=12, mass=1.6,
         info='Milchiger Kunststoff (Polycarbonat), streut das grelle Licht der LEDs. Ist meist nur eingeklebt '
              'und lässt sich mit etwas Drehen abziehen.',
         color=KOLBEN, opacity=0.6),
    teil('kolben_mitte', 'bulb_diffuser', 'Streukolben (Mitte)', 'Kolben Mitte', 'cyl',
         x=0, y=0, w=60, z=72, h=26, mass=3.6,
         info='Die breiteste Stelle der Birne, 60 mm. Aus Kunststoff statt Glas, darum bricht er nicht so leicht.',
         color=KOLBEN, opacity=0.6, label=False),
    teil('kolben_unten', 'bulb_diffuser', 'Streukolben (Hals)', 'Kolben Hals', 'cyl',
         x=4, y=4, w=52, z=56, h=16, mass=2.4,
         info='Unterer Rand des Kolbens, in den Kühlkörper geklebt.', color=KOLBEN, opacity=0.6, label=False),
    teil('led_chips', 'led_module', 'LED-Chips', 'LEDs', 'cyl',
         material_id='mixed_electronics', x=12, y=12, w=36, z=55.5, h=0.8, mass=0.4,
         materials=[['led', 60], ['keramik', 20], ['kupfer', 10], ['lot', 10]],
         info='Zwölf Leuchtdioden aus Galliumnitrid mit gelbem Leuchtstoff. Sie machen aus Strom fast ohne Wärme Licht.',
         color='#E8E8E2', marks=led_ring(12, 13, 18) + [mark('cyl', 14, 14, 8, fill='#F6D86B')]),
    teil('led_platine', 'led_module', 'LED-Platine (Aluminiumkern)', 'LED-Platine', 'cyl',
         material_id='mixed_electronics', x=9, y=9, w=42, z=54, h=1.5, mass=4,
         materials=[['alu', 75], ['kupfer', 10], ['fr4', 10], ['lot', 5]],
         info='Dünne Aluminiumscheibe mit Leiterbahnen. Leitet die Wärme der LEDs in den Kühlkörper. '
              'Mit zwei Schrauben oder Wärmeleitkleber befestigt.',
         color='#ECECE6', marks=[mark('cyl', 19, 19, 4, fill='#9DA6AD')]),
    teil('kuehl_oben', 'aluminium_heat_sink', 'Kühlkörper (oben)', 'Kühlkörper', 'cyl',
         x=2, y=2, w=56, z=40, h=14, mass=11,
         info='Gegossenes Aluminium, oft mit Kunststoff ummantelt. Gibt die Wärme der LEDs an die Luft ab. '
              'Wertvoll fürs Recycling.',
         color=ALU, marks=[mark('cyl', 7, 7, 42)]),
    teil('kuehl_unten', 'aluminium_heat_sink', 'Kühlkörper (Hals)', 'Kühlkörper Hals', 'cyl',
         x=8, y=8, w=44, z=25, h=15, mass=7,
         info='Verjüngt sich zum Sockel hin. Innen ist Platz für die Treiberplatine.', color=ALU, label=False),
    teil('elko', 'circuit_board', 'Elektrolytkondensator', 'Elko', 'cyl',
         material_id='mixed_electronics', x=32, y=26, w=8, z=28, h=12, mass=1.8,
         explode=[62, 0, 0],
         materials=[['alu', 55], ['papier', 20], ['pcabs', 10], ['gummi', 5], ['kupfer', 10]],
         info='Glättet den Strom, damit die Lampe nicht flackert. Fällt er aus, flackert die Lampe oder geht aus.',
         color='#2F4F7A', marks=[mark('cyl', 1.5, 1.5, 5, fill='#B9C0C6')]),
    teil('chips', 'circuit_board', 'Treiber-Chip und Gleichrichter', 'Chips', 'box',
         material_id='pcb', x=30.8, y=21, w=1.6, d=8, z=12, h=12, r=0.3, mass=0.8, explode=[62, 0, 0],
         materials=[['chip', 80], ['kupfer', 20]],
         info='Wandeln die 230-Volt-Wechselspannung in den gleichmäßigen Strom um, den die LEDs brauchen.',
         color='#22272B'),
    teil('treiber', 'circuit_board', 'Treiberplatine', 'Treiber', 'box',
         x=29.2, y=19, w=1.6, d=22, z=6, h=47, r=0.3, mass=5, explode=[50, 0, 0],
         info='Steht senkrecht im Sockel und Kühlkörper. Zwei Drähte führen zum Sockel. '
              'Die Lampe als Ganzes zur Sammelstelle bringen.',
         color='#2E6B45'),
    teil('sockel', 'lamp_base', 'Schraubsockel E27', 'Sockel', 'cyl',
         x=16.5, y=16.5, w=27, z=3, h=22, mass=4,
         info='Gewinde aus Aluminiumblech, in den Kühlkörper gepresst oder geklebt. Es passt in jede normale '
              'Lampenfassung.',
         color='#C2C6C9', marks=[mark('cyl', 1.5, 1.5, 24), mark('cyl', 3, 3, 21)]),
    teil('fusskontakt', 'lamp_base', 'Fußkontakt mit Isolierglas', 'Fußkontakt', 'cyl',
         material_id='copper', x=24, y=24, w=12, z=0, h=3, mass=2,
         materials=[['messing', 45], ['behaelterglas', 40], ['lot', 15]],
         info='Messingkontakt mit Lötpunkt, durch schwarzes Glas vom Gewinde getrennt. '
              'Hier fließt der Strom hinein.',
         color='#2A2B2D', marks=[mark('cyl', 3, 3, 6, fill='#D4B464')]),
]

# Senkrecht stapeln: Gruppen von unten nach oben, jede schwebt ABSTAND über der explodierten Oberkante der darunter.
ABSTAND = 16
gruppen = [['fusskontakt'], ['sockel'], ['kuehl_unten', 'kuehl_oben'], ['led_platine'], ['led_chips'],
           ['kolben_unten', 'kolben_mitte', 'kolben_oben']]
nach_id = {p['id']: p for p in teile}
oben = None
for g in gruppen:
    ps = [nach_id[i] for i in g]
    unten = min(p['z'] for p in ps)
    dz = 0 if oben is None else round(oben + ABSTAND - unten, 1)
    for p in ps:
        p['explode'] = [0, 0, dz]
    oben = max(p['z'] + p['h'] for p in ps) + dz

schreibe('led_bulb', teile)
