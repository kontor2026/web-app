"""3D-Modell: tea_bag. Erzeugt tools/kategorien/modelle/tea_bag.json.

Typischer Teebeutel (gefalteter Filterpapierbeutel ca. 55 × 70 mm mit 2 g Tee, Baumwollfaden, Papieretikett,
Heftklammer), flach hingelegt, gefalteter Kopf hinten bei y = 0. Etikett und Faden liegen auf dem Beutel.
Die Filterlagen werden nach oben abgehoben, der Tee liegt dazwischen, Faden und Etikett schweben darüber.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

FILTER = '#EFE9DC'
teile = [
    teil('etikett', 'paper_tag', 'Etikett', 'Etikett', 'box',
         x=10, y=34, w=36, d=28, z=4.6, h=0.3, r=1, mass=0.1, materials=[['papier', 95], ['druck', 5]],
         color='#F4F1EA',
         info='Kleines Kartonetikett zum Festhalten, mit der Teesorte bedruckt. Abreißen und ins Altpapier '
              'oder mit in den Biomüll.',
         marks=[mark('box', 3, 3, 30, 22, 1, '#2F7A4A'), mark('box', 7, 10, 22, 4, 0, '#F4F1EA')]),
    teil('faden', 'cotton_string', 'Baumwollfaden', 'Faden', 'box',
         x=27, y=8, w=1, d=26, z=4.6, h=0.15, r=0, mass=0.05, color='#F7F4EC',
         info='Ungebleichter Baumwollfaden, durch Etikett und Beutel geknotet oder geklammert. Er verrottet im '
              'Kompost.'),
    teil('klammer', 'staple', 'Heftklammer', 'Klammer', 'box',
         x=24, y=2, w=7, d=2, z=1.2, h=0.4, r=0, mass=0.02, color='#AEB4B9',
         info='Winzige Stahlklammer, die den Faden am Beutel hält. Vor dem Kompostieren herausziehen, '
              'viele Marken kommen inzwischen ohne Klammer aus.',
         marks=[mark('box', 0, 0.7, 7, 0.6, 0, '#868D93')]),
    teil('filter_oben', 'filter_paper', 'Filterpapier (Oberseite)', 'Filterpapier', 'box',
         x=0, y=8, w=55, d=62, z=4.4, h=0.2, r=2, mass=0.12, materials=[['papier', 90], ['pp', 10]],
         color=FILTER, opacity=0.85,
         info='Dünnes Papier aus Zellstoff und Hanf- oder Abacafasern. Viele Beutel enthalten etwas Kunststoff zum '
              'Heißsiegeln, darum kommen nicht alle in den Kompost.',
         marks=[mark('box', 0, 29, 55, 2, 0, '#E0D8C6')] + raster(4, 4, 6, 1, 4, 2, 8.6, fill='#E0D8C6')),
    teil('tee', 'filter_paper', 'Teeblätter (Inhalt)', 'Tee', 'box',
         x=2, y=10, w=51, d=58, z=0.2, h=4.2, r=3, mass=2.0, material_id='wood', materials=[['organisch', 100]],
         color='#5A4632',
         info='Etwa 2 g fein geschnittener Tee. Nach dem Aufbrühen gehört er in den Biomüll oder auf den Kompost.',
         marks=raster(4, 4, 6, 7, 3, 3, 8, 8, shape='cyl', fill='#3F3022')),
    teil('filter_unten', 'filter_paper', 'Filterpapier (Unterseite)', 'Filter unten', 'box',
         x=0, y=8, w=55, d=62, z=0, h=0.2, r=2, mass=0.12, materials=[['papier', 90], ['pp', 10]],
         color=FILTER, label=False,
         info='Zweite Seite desselben Papierstreifens. Beutel und Tee zusammen in den Biomüll, wenn der Beutel '
              'kunststofffrei ist.'),
    teil('kopf', 'filter_paper', 'Gefalteter Kopf', 'Kopf', 'box',
         x=0, y=0, w=55, d=8, z=0, h=1.2, r=1, mass=0.05, materials=[['papier', 100]], color='#E6DFCE',
         info='Das Beutelende ist mehrfach umgefaltet und so ohne Kleber verschlossen. Hier sitzt die Klammer.',
         marks=[mark('box', 0, 3, 55, 1, 0, '#CFC6B2')]),
]
explodiere(teile, abstand=25, gruppen=[['faden', 'etikett']], abstaende={'klammer': 12})
skaliere_masse(teile, oid='tea_bag', stellen=2)
schreibe('tea_bag', teile)
