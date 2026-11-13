"""3D-Modell: foam_food_tray. Erzeugt tools/kategorien/modelle/foam_food_tray.json.

Typische Fleischschale aus EPS/XPS (20 × 14 × 2 cm): Schale mit flachem Rand, Saugeinlage auf dem Boden,
PE-Stretchfolie darüber, Preisetikett auf der Folie. Ebenen nach oben gestapelt.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

WEISS = '#F3F1EC'
teile = [
    teil('etikett', 'ldpe_film', 'Preisetikett', 'Etikett', 'box',
         material_id='paper', x=120, y=80, w=65, d=45, z=20, h=0.2, r=1, mass=0.4,
         materials=[['papier', 85], ['druck', 8], ['klebstoff', 7]],
         info='Thermopapier mit Preis und Haltbarkeit, klebt auf der Folie. Kann mit der Folie in die Gelbe Tonne.',
         color='#F4F2EE', marks=[mark('box', 5, 5, 40, 6, 0, '#3A3F44'), mark('box', 5, 15, 55, 5, 0, '#3A3F44'),
                                 mark('box', 5, 30, 55, 10, 0, '#22272B')]),
    teil('folie', 'ldpe_film', 'Stretchfolie', 'Folie', 'box',
         x=0, y=0, w=200, d=140, z=18, h=2, r=8, mass=1.2, opacity=0.35,
         info='Dünne, dehnbare PE-Folie, um die Schale gespannt. Abziehen und locker in die Gelbe Tonne.',
         color='#DCE6EC'),
    teil('saugeinlage', 'absorbent_pad', 'Saugeinlage', 'Saugeinlage', 'box',
         x=45, y=30, w=110, d=80, z=3, h=3, r=3, mass=0.8,
         info='Zellstoffkissen in Kunststoffhülle, saugt Fleischsaft auf. Herausnehmen und in den Restmüll geben.',
         color='#F7F7F7', marks=raster(4, 4, 6, 1, 14, 72, 17.5, fill='#E3E3E3')),
    teil('rand', 'eps_tray', 'Schalenrand', 'Rand', 'box',
         x=0, y=0, w=200, d=140, z=14, h=4, r=10, mass=1.5,
         info='Breiter Rand, um den die Folie gespannt wird.',
         color=WEISS, marks=[mark('box', 8, 8, 184, 124, 8, '#D8D5CE')]),
    teil('schale', 'eps_tray', 'Schaumstoffschale', 'Schale', 'box',
         x=8, y=8, w=184, d=124, z=0, h=14, r=9, mass=2.6,
         info='Geschäumtes Polystyrol, zu 95 % Luft. Zerbrochen in die Gelbe Tonne, nicht ins Altpapier.',
         color=WEISS),
]
explodiere(teile, abstand=60, gruppen=[['rand', 'schale']])
skaliere_masse(teile, oid='foam_food_tray')
schreibe('foam_food_tray', teile)
