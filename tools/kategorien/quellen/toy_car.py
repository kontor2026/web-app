"""3D-Modell: toy_car. Erzeugt tools/kategorien/modelle/toy_car.json.

Spielzeugauto im Maßstab etwa 1:64 (30 × 70 × 24 mm, Front bei y = 70), Karosserie aus Zinkdruckguss (Zamak),
Bodenplatte aus Kunststoff, mit zwei Nieten (angegossene Zapfen der Karosserie) verbunden. Innen ein Fenstereinsatz
aus klarem PS und ein Innenraum mit Sitzen. Zwei Stahlachsen mit vier Kunststoffrädern (je vier Scheiben, damit sie
von der Seite rund wirken).
Explosion: von oben nach unten Dach/Karosserie, Fenster, Innenraum, Achsen, Bodenplatte, Nieten;
Räder seitlich von den Achsen abgezogen.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

LACK, LACK_H, LACK_D = '#C8302A', '#D84A40', '#9E241F'
ZAMAK = [['zink', 100]]
RAD = '#2B2D2F'
ACHS_Y = (15, 55)    # Achsmitten
RD, RB = 13, 3       # Raddurchmesser, Radbreite
RZ = RD / 2          # Achshöhe

teile = [
    teil('dach', 'toy_car_body', 'Dach (Karosserie)', 'Dach', 'box', material_id='steel',
         x=6, y=25, w=18, d=21, z=21, h=3, r=3, mass=4, materials=ZAMAK, color=LACK,
         info='Das Dach ist mit der Karosserie in einem Stück gegossen und über schmale Säulen verbunden.',
         marks=[mark('box', 3, 3, 12, 15, 2, LACK_H)]),
    teil('karosserie', 'toy_car_body', 'Karosserie aus Zinkdruckguss', 'Karosserie', 'box', material_id='steel',
         x=3, y=0, w=24, d=70, z=5.5, h=9, r=5, mass=27, materials=ZAMAK, color=LACK,
         info='Zamak, eine Zinklegierung mit etwas Aluminium, in eine Form gegossen und lackiert. Zum Öffnen die zwei '
              'Nieten an der Unterseite aufbohren. Metallreste gehören zum Wertstoffhof.',
         marks=[mark('box', 2, 52, 20, 12, 3, LACK_H),            # Motorhaube
                mark('box', 11.5, 53, 1, 10, 0.5, LACK_D),         # Haubenmittellinie
                mark('box', 6, 66.5, 12, 3, 1, '#2B2F33'),         # Kühlergrill
                mark('box', 1.5, 65.5, 4, 3.5, 1.5, '#F2E6C8'), mark('box', 18.5, 65.5, 4, 3.5, 1.5, '#F2E6C8'),
                mark('box', 1.5, 0.8, 4, 2.5, 1, '#E8A33C'), mark('box', 18.5, 0.8, 4, 2.5, 1, '#E8A33C'),
                mark('box', 7, 0.6, 10, 2, 0.5, '#3A3F44'),          # Nummernschild hinten
                mark('box', 2, 4, 20, 13, 3, LACK_H)]),           # Kofferraumdeckel
    teil('fenster', 'toy_car_body', 'Fenstereinsatz', 'Fenster', 'box', material_id='ps',
         x=5, y=20, w=20, d=31, z=14.5, h=6.5, r=4, mass=1.2, materials=[['ps', 100]], color='#BFD3DD', opacity=0.55,
         info='Klares Polystyrol, ein Stück für alle Scheiben. Es wird von innen in die Karosserie gesteckt.',
         marks=[mark('box', 2, 1, 16, 3, 1, '#A9C2CE'), mark('box', 2, 27, 16, 3, 1, '#A9C2CE')]),
    teil('innenraum', 'toy_car_body', 'Innenraum mit Sitzen', 'Innenraum', 'box', material_id='pp',
         x=6, y=22, w=18, d=27, z=14.5, h=2.5, r=2, mass=1.5, materials=[['pp', 100]], color='#3A3F44',
         info='Schwarzer Kunststoffeinsatz mit Sitzen und Lenkrad, zwischen Bodenplatte und Karosserie eingeklemmt.',
         marks=[mark('box', 2, 12, 6, 7, 1, '#22272B'), mark('box', 10, 12, 6, 7, 1, '#22272B'),
                mark('box', 2, 2, 14, 7, 1, '#22272B'), mark('cyl', 2.5, 21, 5, 2, fill='#5B6166')]),
]
for n, y in enumerate(ACHS_Y):
    teile.append(teil(f'achse_{n + 1}', 'steel_axles', 'Achsen aus Stahldraht' if n == 0 else 'Achse hinten', 'Achse',
                      'box', x=1, y=y - 0.6, w=28, d=1.2, z=RZ - 0.6, h=1.2, r=0.6, mass=0.4, color='#9AA2A6',
                      label=None if n == 0 else False,
                      info='Dünner Stahldraht, an den Enden breitgedrückt, damit die Räder nicht abfallen. '
                           'Sie liegt in Rillen der Bodenplatte.' if n == 0 else 'Zweite Achse.'))
teile += [
    teil('bodenplatte', 'toy_car_body', 'Bodenplatte', 'Bodenplatte', 'box',
         x=4, y=1, w=22, d=68, z=3.5, h=1.9, r=3, mass=3, color='#5B6166',
         info='Kunststoffplatte (ABS) mit Achsaufnahmen. Sie wird von den Nieten gehalten; '
              'nach dem Aufbohren fällt sie ab.',
         marks=[mark('box', 0, 12.8, 22, 2.4, 0.5, '#3A3F44'), mark('box', 0, 52.8, 22, 2.4, 0.5, '#3A3F44'),
                mark('cyl', 8.5, 4.5, 5, fill='#7A8288'), mark('cyl', 8.5, 58.5, 5, fill='#7A8288'),
                mark('box', 6, 24, 10, 20, 1, '#4E5459')]),
]
# Räder: je vier waagrechte Scheiben (Sehnen eines Kreises), rechte Räder vor der Karosserie zeichnen
GRENZEN = (0, 1.2, 3, RZ, RD - 3, RD - 1.2, RD)
raeder = []
for n, (seite, y) in enumerate([(s, y) for y in ACHS_Y for s in (0, 1)]):
    gruppe = []
    for k, (z0, z1) in enumerate(zip(GRENZEN, GRENZEN[1:])):
        zm = (abs(z0 - RZ) + abs(z1 - RZ)) / 2
        d = round(2 * math.sqrt(RZ ** 2 - min(zm, RZ - 0.3) ** 2), 1)
        erstes = n == 0 and k == 5
        gruppe.append(teil(f'rad_{n + 1}_{k}', 'pp_wheels', 'Räder (4 Stück)' if erstes else f'Rad {n + 1}',
                           'Räder', 'box', x=0 if seite == 0 else 30 - RB, y=round(y - d / 2, 2), w=RB, d=d,
                           z=z0, h=round(z1 - z0, 2), r=1, mass=0.1, color=RAD, label=None if erstes else False,
                           sortBias=12 if seite else None,
                           info='Kunststoffräder, auf die Achse gesteckt. Mit einer Zange abziehen.' if erstes
                           else 'Weiteres Rad.',
                           marks=[mark('box', 0.6, d / 2 - 2.5, 1.8, 5, 0.8, '#9AA2A6')] if k == 5 else None))
    raeder.append(gruppe)
teile += [p for g in reversed(raeder) for p in g if p['label'] is None] + \
         [p for g in raeder for p in g if p['label'] is not None]
teile += [
    teil(f'niete_{n + 1}', 'toy_car_body', 'Nieten' if n == 0 else 'Niete hinten', 'Nieten', 'cyl', material_id='steel',
         x=13, y=y, w=4, z=2, h=1.5, mass=0.1, materials=ZAMAK, color='#B8BEC2', label=None if n == 0 else False,
         info='Zapfen der Karosserie, durch die Bodenplatte gesteckt und breitgepresst. Mit einem 3-mm-Bohrer '
              'aufbohren, dann lässt sich das Auto zerlegen.' if n == 0 else 'Zweite Niete.')
    for n, y in enumerate((5.5, 59.5))
]

by = {p['id']: p for p in teile}
rad_teile = [p for g in raeder for p in g]
rest = [p for p in teile if p not in rad_teile]
explodiere(rest, abstand=14, nach_liste=True,
           gruppen=[['dach', 'karosserie'], ['achse_1', 'achse_2'], ['niete_1', 'niete_2']])
dz = by['bodenplatte']['explode'][2]
for p in rad_teile:
    p['explode'] = [-40, 0, 0] if p['x'] == 0 else [40, 0, dz]
skaliere_masse(teile, oid='toy_car', stellen=2)
schreibe('toy_car', teile)
