"""3D-Modell: aluminium_tray. Erzeugt tools/kategorien/modelle/aluminium_tray.json.

Typische Aluschale 1 l mit Kartondeckel (20 × 15 × 4 cm): tiefgezogene Schale mit Bördelrand, beschichteter
Kartondeckel, der in den Rand eingebördelt wird. Deckel hebt nach oben ab.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

ALU = '#C9CED3'
teile = [
    teil('deckel', 'cardboard_lid', 'Kartondeckel', 'Deckel', 'box',
         x=4, y=4, w=192, d=142, z=38, h=1.5, r=8, mass=4, materials=[['papier', 80], ['ldpe', 15], ['druck', 5]],
         info='Karton, innen mit Kunststoff oder Alu beschichtet, damit er nicht durchweicht. In den Restmüll.',
         color='#E8E2D5', marks=[mark('box', 8, 8, 176, 126, 6, '#F4F2EE'), mark('box', 20, 20, 100, 8, 0, '#3A3F44'),
                                 mark('box', 20, 34, 70, 6, 0, '#3A3F44')]),
    teil('rand', 'aluminium_tray_body', 'Bördelrand', 'Rand', 'box',
         x=0, y=0, w=200, d=150, z=36, h=3, r=10, mass=2.5,
         info='Breiter, gerollter Rand. Er wird über den Deckel gedrückt und hält ihn fest.',
         color=ALU, marks=[mark('box', 7, 7, 186, 136, 8, '#8E959C')]),
    teil('wand', 'aluminium_tray_body', 'Schale oben', 'Schale', 'box',
         x=6, y=6, w=188, d=138, z=18, h=18, r=12, mass=5, label=False,
         info='Etwa 0,08 mm dünnes Aluminium, in die Form gepresst. Die Falten an den Ecken entstehen dabei.',
         color=ALU),
    teil('boden', 'aluminium_tray_body', 'Schale unten mit Boden', 'Schale', 'box',
         x=12, y=12, w=176, d=126, z=0, h=18, r=14, mass=4.5,
         info='Essensreste auskratzen, dann in die Gelbe Tonne. Aluminium lässt sich ohne Qualitätsverlust einschmelzen.',
         color=ALU),
]
explodiere(teile, abstand=70, gruppen=[['rand', 'wand', 'boden']])
skaliere_masse(teile, oid='aluminium_tray')
schreibe('aluminium_tray', teile)
