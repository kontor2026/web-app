"""3D-Modell: kitchen_knife. Erzeugt tools/kategorien/modelle/kitchen_knife.json.

Typisches Küchen-/Allzweckmesser flach auf dem Tisch, Spitze hinten (y = 0), Griff vorne. 25 × 320 × 20 mm.
Klinge 20 cm aus Edelstahl, Rücken gerade (rechts, x = 25), Schneide links läuft in vier Abschnitten zur Spitze
hoch. Geschmiedeter Kropf, durchgehende Angel zwischen zwei Griffschalen aus Kunststoff, drei Nieten.
Explodiert: obere Schale und Nieten über der Angel, untere Schale nach rechts herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

STAHL = '#C3C9CE'
SCHNEIDE = '#E6EAED'
GRIFF = '#2E3338'
NIET = '#B8BEC4'
NIET_Y = (222, 260, 298)

# Klinge in Abschnitten: (y, d, w), Rücken bündig rechts bei x = 25
KLINGE = [(0, 22, 7), (22, 26, 14), (48, 32, 20), (80, 116, 25)]

teile = []
for i, (y, d, w) in enumerate(KLINGE):
    letzte = i == len(KLINGE) - 1
    marks = [mark('box', 0, 1, 2.5, d - 2, 1, SCHNEIDE)]
    if letzte:
        marks += [mark('box', 6, 70, 14, 26, 2, '#B2B8BD', zeichnung=True), mark('box', 22, 0, 2, d, 1, '#D5DADD')]
    teile.append(teil('klinge' if letzte else f'klinge_{i + 1}', 'knife_blade', 'Klinge', 'Klinge', 'box',
                      x=25 - w, y=y, w=w, d=d, z=9, h=2, r=[3, 3, 3, 2][i], mass=[4, 9, 14, 48][i], label=letzte,
                      info=('Rostfreier Messerstahl, an der linken Kante scharf geschliffen. Vor dem Wegwerfen in dicke '
                            'Pappe wickeln und festkleben, dann als Metallschrott zum Wertstoffhof.') if letzte
                      else 'Hier wird die Klinge schmaler und läuft in der Spitze aus.',
                      color=STAHL, marks=marks))

teile = [
    *[teil('niet' if i == 0 else f'niet_{i + 1}', 'knife_handle', 'Griffniete', 'Nieten', 'cyl', material_id='steel',
           x=9.5, y=y - 3, w=6, z=0, h=20.3, mass=1, label=i == 0,
           info=('Drei Edelstahlnieten gehen durch Griffschalen und Angel und halten alles zusammen. Wer den Griff '
                 'abtrennen will, muss sie aufbohren.') if i == 0 else 'Eine der drei Griffnieten.',
           color=NIET, sortBias=-1, marks=[mark('cyl', 1, 1, 4, fill='#D5DADD')]) for i, y in enumerate(NIET_Y)],
    teil('schale_oben', 'knife_handle', 'Griffschale oben', 'Griffschale', 'box',
         x=1, y=206, w=23, d=114, z=11, h=9, r=9, explode=[-40, 0, 0], mass=16,
         info='Kunststoff (POM oder PP), auf die Angel genietet. Abtrennen nur mit Bohrer oder Säge, sonst das ganze '
              'Messer zum Wertstoffhof bringen.',
         color=GRIFF, marks=[mark('box', 4, 4, 15, 106, 6, '#3E444A', zeichnung=True)]
         + [mark('cyl', 9.5, y - 206 - 3, 6, fill='#B8BEC4') for y in NIET_Y]),
    *teile,
    teil('kropf', 'knife_blade', 'Kropf', 'Kropf', 'box',
         x=0, y=196, w=25, d=10, z=1, h=19, r=3, mass=15,
         info='Geschmiedete Verdickung zwischen Klinge und Griff. Sie schützt die Finger davor, auf die Schneide '
              'zu rutschen, und gibt dem Messer Gewicht.',
         color='#B2B8BD', marks=[mark('box', 2, 2, 21, 6, 2, '#C3C9CE')]),
    teil('angel', 'knife_blade', 'Angel (Erl)', 'Angel', 'box',
         x=1, y=206, w=23, d=112, z=9, h=2, r=8, mass=20,
         info='Verlängerung der Klinge, die durch den ganzen Griff läuft. Durchgehende Angeln halten länger.',
         color=STAHL, marks=[mark('cyl', 9.5, y - 206 - 2.5, 5, fill='#7E868C') for y in NIET_Y]),
    teil('schale_unten', 'knife_handle', 'Griffschale unten', 'Schale unten', 'box',
         x=1, y=206, w=23, d=114, z=0, h=9, r=9, explode=[38, 0, 0], mass=16,
         info='Das Gegenstück auf der anderen Seite der Angel. Beide Schalen sind aus demselben Kunststoff.',
         color=GRIFF, marks=[mark('box', 4, 4, 15, 106, 6, '#3E444A', zeichnung=True)]
         + [mark('cyl', 9.5, y - 206 - 3, 6, fill='#1E2226') for y in NIET_Y]),
]
fest = [p['id'] for p in teile if p['id'].startswith('klinge')] + ['kropf', 'angel']
explodiere(teile, abstand=14, fest=fest, nach_liste=True)
for p in teile:  # Griffschale und Nieten etwas nach vorne, damit der Kropf frei bleibt
    if p['id'] == 'schale_oben' or p['id'].startswith('niet'):
        p['explode'][1] = 30
skaliere_masse(teile, oid='kitchen_knife')
schreibe('kitchen_knife', teile)
