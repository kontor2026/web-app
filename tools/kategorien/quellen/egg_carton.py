"""3D-Modell: egg_carton. Erzeugt tools/kategorien/modelle/egg_carton.json.

Typischer Eierkarton für 6 Eier (3 × 2) aus Faserguss: Unterschale mit sechs Eiermulden und zwei Stützkegeln,
hinten angeformter Deckel, vorne die Verschlusslasche, Preisetikett auf dem Deckel. Deckel hebt nach oben ab,
Lasche klappt nach vorne weg.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

FASER = '#B9AE9C'
DUNKEL = '#9C907C'
teile = [
    teil('etikett', 'molded_pulp_tray', 'Preisetikett', 'Etikett', 'box',
         material_id='paper', x=45, y=30, w=70, d=45, z=70, h=0.2, r=1, mass=0.4, materials=[['papier', 85], ['druck', 8], ['klebstoff', 7]],
         info='Papieraufkleber mit Haltbarkeitsdatum und Erzeugercode. Darf am Karton bleiben.',
         color='#F4F2EE', marks=[mark('box', 5, 5, 45, 6, 0, '#3A3F44'), mark('box', 5, 15, 35, 5, 0, '#3A3F44'),
                                 mark('box', 5, 30, 60, 9, 0, '#B3423A')]),
    teil('deckel', 'molded_pulp_tray', 'Deckel', 'Deckel', 'box',
         x=0, y=0, w=160, d=105, z=36, h=34, r=10, mass=11,
         info='Hinten mit der Unterschale verbunden. Die Rippen machen den dünnen Faserguss stabil.',
         color=FASER, marks=[mark('box', 6, 6, 148, 93, 8, DUNKEL), mark('box', 10, 10, 140, 85, 6, FASER)]
                            + raster(14, 8, 3, 1, 32, 6, 48, fill=DUNKEL)),
    teil('kegel_links', 'molded_pulp_tray', 'Stützkegel links', 'Stützkegel', 'cyl',
         x=48, y=45, w=15, z=20, h=40, mass=0.8,
         info='Stützt den Deckel, damit die Eier beim Stapeln nicht zerdrückt werden.',
         color=FASER, marks=[mark('cyl', 4, 4, 7, fill=DUNKEL)]),
    teil('kegel_rechts', 'molded_pulp_tray', 'Stützkegel rechts', 'Stützkegel', 'cyl',
         x=97, y=45, w=15, z=20, h=40, mass=0.8, label=False,
         info='Gegenstück zum linken Kegel.',
         color=FASER, marks=[mark('cyl', 4, 4, 7, fill=DUNKEL)]),
    teil('schale', 'molded_pulp_tray', 'Unterschale mit Eiermulden', 'Unterschale', 'box',
         x=2, y=2, w=156, d=101, z=0, h=36, r=8, mass=14,
         info='Aus Altpapier gepresst und getrocknet. Sauber ins Altpapier, zerrissen auch in den Kompost.',
         color=FASER, marks=[mark('box', 2, 2, 152, 97, 6, DUNKEL)]
                            + raster(5, 3, 3, 2, 46, 46, 50, shape='cyl', fill='#857A68')),
    teil('lasche', 'molded_pulp_tray', 'Verschlusslasche', 'Lasche', 'box',
         x=40, y=100, w=80, d=5, z=10, h=24, r=1, explode=[0, 50, 0], mass=1.5,
         info='Wird in die Schlitze des Deckels gesteckt und hält den Karton geschlossen.',
         color=FASER, marks=[mark('box', 30, 0, 20, 5, 1, DUNKEL)]),
]
explodiere(teile, abstand=45)
skaliere_masse(teile, oid='egg_carton')
schreibe('egg_carton', teile)
