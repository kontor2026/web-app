"""3D-Modell: tape_dispenser. Erzeugt tools/kategorien/modelle/tape_dispenser.json.

Typischer Tisch-Klebebandabroller 60 × 130 × 70 mm: Sockel aus Polystyrol mit eingelegtem Stahlgewicht, zwei
Seitenwangen, in denen die Spule mit der Klebebandrolle (19 mm × 33 m auf 1-Zoll-Papierkern) läuft, vorne die Nase mit
der gezahnten Abreißklinge. Die Rolle (Achse quer, x) ist ein liegender Zylinder (in der Zeichnung ein Quader). Explodiert:
Wangen zur Seite, Nase mit Klinge nach vorne, Gewicht, Rolle, Kern und Spule nach oben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

PS = '#2F3A45'
BAND = '#E9E4D0'
teile = [
    teil('spule', 'ps_dispenser_body', 'Spule mit Achse', 'Spule', 'box',
         x=3, y=50, w=54, d=10, z=40, h=10, r=4, mass=4, form='liegend_x',
         info='Steckt im Papierkern und läuft in den Kerben der Seitenwangen. Nach oben herausheben, '
              'dann lässt sich die leere Rolle abziehen.',
         color='#55626E', marks=[mark('box', 17, 1, 20, 8, 3, '#6E7C88', zeichnung=True)]),
    teil('kern', 'ps_dispenser_body', 'Papierkern der Rolle', 'Papierkern', 'box',
         x=20.5, y=39, w=19, d=32, z=29, h=32, r=8, mass=3, material_id='cardboard', form='liegend_x',
         materials=[['papier', 95], ['klebstoff', 5]], color='#B98F5A', sortBias=-20,
         info='Gewickelte Pappe mit 25 mm Innendurchmesser. Leere Kerne gehören ins Altpapier.',
         marks=[mark('box', 4, 4, 11, 24, 5, '#8E6A3E', zeichnung=True)]),
    teil('band_mitte', 'ps_dispenser_body', 'Klebebandrolle (PP-Folie mit Acrylkleber)', 'Klebeband', 'box',
         x=20.5, y=30, w=19, d=50, z=20, h=50, r=12, mass=32, material_id='pp', form='liegend_x',
         materials=[['pp', 75], ['klebstoff', 25]], color=BAND, opacity=0.85,
         info='Etwa 33 m Polypropylenfolie mit Acrylatkleber. Klebebandreste gehören in den Restmüll, '
              'sie verkleben im Recycling die Maschinen.',
         marks=[mark('box', 2, 2, 15, 46, 10, '#DCD5BC', zeichnung=True)]),
    teil('klinge', 'steel_cutting_blade', 'Abreißklinge (gezahnt)', 'Klinge', 'box',
         x=4, y=118, w=52, d=10, z=62, h=1, r=0.5, mass=3, explode=[0, 70, 30],
         info='Gezahntes Stahlblech, in einen Schlitz der Nase gesteckt. Mit einem Schraubendreher heraushebeln '
              'und vor dem Wegwerfen in Pappe oder Klebeband einwickeln, die Zähne sind scharf.',
         color='#C3C9CE', marks=raster(1, 7.5, 25, 1, 1.4, 2.5, 2) + [mark('box', 0, 0, 52, 2, 0, '#9AA2A6')]),
    teil('nase', 'ps_dispenser_body', 'Nase mit Klingenhalter', 'Nase', 'box',
         x=0, y=95, w=60, d=35, z=20, h=42, r=4, mass=22, explode=[0, 70, 0],
         info='Hier läuft das Band über eine Auflage zur Klinge. Die Klinge steckt in einem Schlitz oben.',
         color=PS, marks=[mark('box', 4, 23, 52, 10, 1, '#1E262E'), mark('box', 6, 4, 48, 16, 2, '#3D4A57'),
                         mark('box', 20.5, 0, 19, 24, 0, '#B9B39C')]),
    teil('wange_links', 'ps_dispenser_body', 'Seitenwange links', 'Wange links', 'box',
         x=0, y=20, w=5, d=75, z=20, h=38, r=2, mass=8, explode=[-40, 0, 0],
         info='Hält die Spule. Die Kerbe oben ist das Lager für die Achse.',
         color=PS),
    teil('wange_rechts', 'ps_dispenser_body', 'Seitenwange rechts', 'Wange rechts', 'box',
         x=55, y=20, w=5, d=75, z=20, h=38, r=2, mass=8, explode=[40, 0, 0], label=False,
         info='Gegenstück zur linken Wange.', color=PS),
    teil('gewicht', 'ps_dispenser_body', 'Stahlgewicht', 'Gewicht', 'box',
         x=6, y=10, w=48, d=110, z=2, h=12, r=3, mass=70, material_id='steel',
         info='Ein Stahlblock im Sockel macht den Abroller schwer, damit man das Band mit einer Hand abreißen kann. '
              'Unten aus dem Sockel herausdrücken und zum Metallschrott geben.',
         color='#7B848B', marks=[mark('box', 4, 6, 40, 98, 2, '#8D969D')]),
    teil('sockel', 'ps_dispenser_body', 'Sockel (Polystyrol)', 'Sockel', 'box',
         x=0, y=0, w=60, d=130, z=0, h=20, r=6, mass=45,
         info='Hohler Sockel aus schlagfestem Polystyrol. Ohne Gewicht und Klinge kann er in den Wertstoffhof '
              'oder Restmüll, er ist keine Verpackung.',
         color=PS, marks=[mark('box', 5, 5, 50, 120, 4, '#3D4A57')]),
]
explodiere(teile, abstand=12)
skaliere_masse(teile, oid='tape_dispenser')
schreibe('tape_dispenser', teile)
