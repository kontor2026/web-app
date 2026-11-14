"""3D-Modell: toy_car. Erzeugt tools/kategorien/modelle/toy_car.json.

Spielzeugauto im Maßstab etwa 1:64 (30 × 70 × 25 mm, Front bei y = 70), Karosserie aus Zinkdruckguss (Zamak),
Bodenplatte aus Kunststoff, mit zwei Nieten (angegossene Zapfen der Karosserie) verbunden. Innen ein Fenstereinsatz
aus klarem PS und ein Innenraum mit Sitzen. Zwei Stahlachsen mit vier Kunststoffrädern.
Explosion: von oben nach unten Karosserie (mit Dach), Fenster, Innenraum, Achsen, Bodenplatte, Nieten;
Räder seitlich von den Achsen abgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

LACK = '#C8302A'
ZAMAK = [['zink', 100]]
RAD = '#2B2D2F'
ACHS_Y = (14, 56)    # Achsmitten
RD, RB = 13, 4       # Raddurchmesser, Radbreite

teile = [
    teil('dach', 'toy_car_body', 'Dach (Karosserie)', 'Dach', 'box', material_id='steel',
         x=7, y=24, w=16, d=24, z=21.5, h=3.5, r=3, mass=4, materials=ZAMAK, color=LACK,
         info='Das Dach ist mit der Karosserie in einem Stück gegossen und über schmale Säulen verbunden.',
         marks=[mark('box', 3, 4, 10, 16, 2, '#D84A40')]),
    teil('karosserie', 'toy_car_body', 'Karosserie aus Zinkdruckguss', 'Karosserie', 'box', material_id='steel',
         x=1, y=0, w=28, d=70, z=6.5, h=10, r=5, mass=27, materials=ZAMAK, color=LACK,
         info='Zamak, eine Zinklegierung mit etwas Aluminium, in eine Form gegossen und lackiert. Zum Öffnen die zwei '
              'Nieten an der Unterseite aufbohren. Metallreste gehören zum Wertstoffhof.',
         marks=[mark('box', 5, 17, 18, 35, 2, '#3A3F44'), mark('box', 4, 62, 20, 6, 2, '#D84A40'),
                mark('box', 3, 66, 5, 3, 1, '#F2E6C8'), mark('box', 20, 66, 5, 3, 1, '#F2E6C8'),
                mark('box', 3, 1, 5, 2.5, 1, '#E8A33C'), mark('box', 20, 1, 5, 2.5, 1, '#E8A33C')]),
    teil('fenster', 'toy_car_body', 'Fenstereinsatz', 'Fenster', 'box', material_id='ps',
         x=6, y=18, w=18, d=34, z=16.5, h=5, r=3, mass=1.2, materials=[['ps', 100]], color='#BFD3DD', opacity=0.6,
         info='Klares Polystyrol, ein Stück für alle Scheiben. Es wird von innen in die Karosserie gesteckt.',
         marks=[mark('box', 1, 6, 16, 22, 2, '#A9C2CE')]),
    teil('innenraum', 'toy_car_body', 'Innenraum mit Sitzen', 'Innenraum', 'box', material_id='pp',
         x=6, y=20, w=18, d=30, z=8, h=8, r=2, mass=1.5, materials=[['pp', 100]], color='#3A3F44',
         info='Schwarzer Kunststoffeinsatz mit Sitzen und Lenkrad, zwischen Bodenplatte und Karosserie eingeklemmt.',
         marks=[mark('box', 2, 4, 6, 7, 1, '#22272B'), mark('box', 10, 4, 6, 7, 1, '#22272B'),
                mark('box', 2, 16, 14, 8, 1, '#22272B'), mark('cyl', 2.5, 12, 5, 2, fill='#5B6166')]),
]
for n, y in enumerate(ACHS_Y):
    teile.append(teil(f'achse_{n + 1}', 'steel_axles', 'Achsen aus Stahldraht' if n == 0 else 'Achse hinten', 'Achse',
                      'box', x=2, y=y - 0.6, w=26, d=1.2, z=5.9, h=1.2, r=0.6, mass=0.4, color='#9AA2A6',
                      label=None if n == 0 else False,
                      info='Dünner Stahldraht, an den Enden breitgedrückt, damit die Räder nicht abfallen. '
                           'Sie liegt in Rillen der Bodenplatte.' if n == 0 else 'Zweite Achse.'))
teile += [
    teil('bodenplatte', 'toy_car_body', 'Bodenplatte', 'Bodenplatte', 'box',
         x=4, y=1, w=22, d=68, z=4, h=1.9, r=3, mass=3, color='#5B6166',
         info='Kunststoffplatte (ABS) mit Achsaufnahmen. Sie wird von den Nieten gehalten; '
              'nach dem Aufbohren fällt sie ab.',
         marks=[mark('box', 0, 12.8, 22, 2.4, 0.5, '#3A3F44'), mark('box', 0, 54.8, 22, 2.4, 0.5, '#3A3F44'),
                mark('cyl', 8, 5.5, 5, fill='#7A8288'), mark('cyl', 8, 59.5, 5, fill='#7A8288')]),
]
for n, (seite, y) in enumerate([(s, y) for y in ACHS_Y for s in (0, 1)]):
    teile.append(teil(f'rad_{n + 1}', 'pp_wheels', 'Räder (4 Stück)' if n == 0 else f'Rad {n + 1}', 'Räder', 'box',
                      x=0 if seite == 0 else 30 - RB, y=y - RD / 2, w=RB, d=RD, z=0, h=RD, r=1.5, mass=0.6, color=RAD,
                      label=None if n == 0 else False,
                      info='Kunststoffräder, auf die Achse gesteckt. Mit einer Zange abziehen.' if n == 0
                      else 'Weiteres Rad.',
                      marks=[mark('box', 0.8, 3.5, 2.4, 6, 1, '#9AA2A6')]))
teile += [
    teil(f'niete_{n + 1}', 'toy_car_body', 'Nieten' if n == 0 else 'Niete hinten', 'Nieten', 'cyl', material_id='steel',
         x=13, y=y, w=4, z=2.5, h=1.5, mass=0.1, materials=ZAMAK, color='#B8BEC2', label=None if n == 0 else False,
         info='Zapfen der Karosserie, durch die Bodenplatte gesteckt und breitgepresst. Mit einem 3-mm-Bohrer '
              'aufbohren, dann lässt sich das Auto zerlegen.' if n == 0 else 'Zweite Niete.')
    for n, y in enumerate((5.5, 60.5))
]

by = {p['id']: p for p in teile}
raeder = [p for p in teile if p['id'].startswith('rad_')]
rest = [p for p in teile if p not in raeder]
explodiere(rest, abstand=12, nach_liste=True,
           gruppen=[['dach', 'karosserie'], ['achse_1', 'achse_2'], ['niete_1', 'niete_2']])
dz = by['achse_1']['explode'][2]
for p in raeder:
    p['explode'] = [-14 if p['x'] == 0 else 14, 0, dz]
skaliere_masse(teile, oid='toy_car', stellen=2)
schreibe('toy_car', teile)
