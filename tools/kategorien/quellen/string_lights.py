"""3D-Modell: string_lights. Erzeugt tools/kategorien/modelle/string_lights.json.

Typische Batterie-Lichterkette mit 40 LEDs an 4 m Draht und Batteriekasten für 3 AA-Zellen. Die Kette liegt lose
aufgerollt (links hinten), der Batteriekasten rechts vorne daneben.
Explosion: Kette in Schichten (Mantel, Kupferdraht, LEDs) nach oben, Batteriekasten geöffnet nach oben gestapelt,
Schiebeschalter nach rechts (dx > 0) herausgezogen.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

D = 105  # Durchmesser des Knäuels
KASTEN = '#2B2E31'


LOCH = '#1A1C1B'  # Innenraum des Knäuels (Ring), dunkel wie ein Schatten


def windungen(dm, n=6, breite=3.2, farben=None):
    """Konzentrische Drahtwindungen, innen ein dunkles Loch: das Knäuel ist ein lockerer Ring."""
    m = [mark('cyl', round(i * breite, 2), round(i * breite, 2), round(dm - 2 * i * breite, 2),
              fill=farben[i % 2] if farben else None) for i in range(n)]
    return m + [mark('cyl', round(n * breite, 2), round(n * breite, 2), round(dm - 2 * n * breite, 2), fill=LOCH)]


def led_kreise(dm, ringe=((0.46, 16), (0.4, 14), (0.34, 10))):
    out = []
    for f, n in ringe:
        for i in range(n):
            a = 2 * math.pi * (i + 0.5 * (n % 2)) / n
            out.append(mark('cyl', round(dm / 2 + f * dm * math.cos(a) - 2, 2), round(dm / 2 + f * dm * math.sin(a) - 2, 2),
                            4, fill='#F6D86B'))
    return out


AA = [['zinkmangan', 80], ['stahl', 20]]
teile = [
    teil('leds', 'led_module', '40 Mini-LEDs', 'LEDs', 'cyl',
         material_id='mixed_electronics', x=3, y=3, w=D - 6, z=28, h=4, mass=8,
         materials=[['led', 40], ['pcabs', 40], ['kupfer', 10], ['lot', 10]],
         info='Winzige Leuchtdioden, in Tropfen aus Kunstharz eingegossen und direkt auf den Draht gelötet. '
              'Sie lassen sich nicht einzeln abtrennen, die ganze Kette ist Elektroschrott.',
         color='#E4E6DC', opacity=0.75,
         marks=[mark('cyl', 19, 19, D - 44, fill=LOCH)]
         + led_kreise(D - 6)),
    teil('draht', 'cable_copper_core', 'Kupferdraht (lackiert)', 'Kupferdraht', 'cyl',
         x=2, y=2, w=D - 4, z=1, h=26, mass=30, materials=[['kupfer', 85], ['polyester', 15]],
         info='Zwei dünne, lackisolierte Kupferdrähte, an denen die LEDs hängen. Biegsam, aber bricht bei häufigem Knicken.',
         color='#C5803D', marks=windungen(D - 4, farben=('#C5803D', '#B06F33'))),
    teil('mantel', 'cable_insulation', 'Kabelisolierung', 'Isolierung', 'cyl',
         x=0, y=0, w=D, z=0, h=28, mass=22, materials=[['pvc', 100]],
         info='Grüne oder durchsichtige PVC-Hülle um den Draht. Zum Recycling muss sie in der Anlage vom Kupfer '
              'getrennt werden.',
         color='#3E7A4A', marks=windungen(D, farben=('#3E7A4A', '#336A3F'))),
    teil('zuleitung', 'cable_insulation', 'Zuleitung zum Batteriekasten', 'Zuleitung', 'box',
         material_id='pvc', x=86, y=96, w=6, d=14, z=1, h=4, r=2, explode=[-30, 30, 0], mass=3,
         materials=[['pvc', 60], ['kupfer', 40]], color='#336A3F',
         info='Etwa 30 cm Kabel ohne LEDs zwischen Kasten und Kette. Hier abschneiden, um den Kasten abzutrennen.'),
    teil('schieber', 'battery_box', 'Schiebeknopf (AN/AUS/TIMER)', 'Schiebeknopf', 'box',
         material_id='abs', x=148, y=128, w=2.5, d=8, z=7, h=6, r=0.8, explode=[60, 0, 0], mass=0.5,
         materials=[['pcabs', 100]], sortBias=20, color='#4A4F54',
         info='Der Knopf, mit dem man die Kette schaltet. Er steckt auf dem Schalter der kleinen Platine.'),
    teil('schalter', 'battery_box', 'Schiebeschalter mit Timer-Platine', 'Schalter', 'box',
         material_id='pcb', x=139, y=124, w=8, d=18, z=6, h=10, r=1, explode=[32, 0, 0], mass=3,
         materials=[['fr4', 35], ['kupfer', 20], ['chip', 15], ['stahl', 15], ['pcabs', 15]],
         info='Schaltet die Kette ein, aus oder auf Timer (6 Stunden an, 18 aus). Kleine Platine mit Chip und Widerstand.',
         color='#3A3D40', marks=[mark('box', 2, 4, 4, 6, 1, '#7FD36B')]),
    teil('deckel', 'battery_box', 'Batteriefach-Deckel', 'Deckel', 'box',
         x=80, y=108, w=68, d=50, z=18, h=4, r=4, mass=10,
         info='Wird zum Batteriewechsel aufgeschoben. Polypropylen, lässt sich gut recyceln, wenn die Elektronik entfernt ist.',
         color=KASTEN, marks=raster(10, 8, 1, 4, 48, 2, 0, 10, r=1, fill='#3A3D40')),
    teil('batterie_1', 'alkaline_cell', 'Mignon-Batterie (AA)', 'Batterie AA', 'box',
         x=88, y=112, w=50.5, d=14.5, z=3, h=14.5, r=7, mass=23, materials=AA,
         info='Drei 1,5-Volt-Zellen in Reihe ergeben 4,5 Volt. Vor dem Wegwerfen herausnehmen und in die Batteriesammlung geben.',
         color='#C8423A', marks=[mark('box', 0, 0, 6, 14.5, 3, '#B7BCC0')]),
    teil('batterie_2', 'alkaline_cell', 'Mignon-Batterie (AA)', 'Batterie AA', 'box',
         x=88, y=126.5, w=50.5, d=14.5, z=3, h=14.5, r=7, mass=23, materials=AA, label=False,
         info='Zweite Zelle, liegt umgekehrt zur ersten.', color='#C8423A',
         marks=[mark('box', 44.5, 0, 6, 14.5, 3, '#B7BCC0')]),
    teil('batterie_3', 'alkaline_cell', 'Mignon-Batterie (AA)', 'Batterie AA', 'box',
         x=88, y=141, w=50.5, d=14.5, z=3, h=14.5, r=7, mass=23, materials=AA, label=False,
         info='Dritte Zelle.', color='#C8423A', marks=[mark('box', 0, 0, 6, 14.5, 3, '#B7BCC0')]),
    teil('kontakte', 'battery_box', 'Kontaktfedern', 'Federn', 'box',
         material_id='steel', x=83, y=111, w=4, d=45, z=3, h=14, r=0.5, mass=3,
         materials=[['stahl', 90], ['nickel', 10]],
         info='Vernickelte Stahlfedern und -bleche, die die Batterien verbinden. Ein Magnet zieht sie an.',
         color='#C9CDD0', marks=raster(0.5, 4, 1, 3, 3, 7, 0, 14.5, r=1)),
    teil('kasten', 'battery_box', 'Batteriekasten', 'Batteriekasten', 'box',
         x=80, y=108, w=68, d=50, z=0, h=18, r=4, mass=18,
         info='Gehäuse aus Polypropylen mit drei Mulden. Erst die Batterien herausnehmen, dann den Kasten mit Kette '
              'zur Elektro-Sammlung bringen.',
         color=KASTEN, marks=[mark('box', 3, 3, 62, 44, 3, '#1E2022')]),
]
explodiere(teile, abstand=26, abstaende={'kontakte': 14})
for p in teile:  # Batteriekasten samt Inhalt nach rechts vorne, damit er die Kette nicht verdeckt
    if p['component_id'] in ('battery_box', 'alkaline_cell'):
        p['explode'] = [p['explode'][0] + 70, p['explode'][1] + 50, p['explode'][2]]
skaliere_masse(teile, oid='string_lights')
schreibe('string_lights', teile)
