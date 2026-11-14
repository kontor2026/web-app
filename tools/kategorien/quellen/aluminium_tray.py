"""3D-Modell: aluminium_tray. Erzeugt tools/kategorien/modelle/aluminium_tray.json.

Typische Aluschale 1 l mit Kartondeckel (20 × 15 × 4 cm): tiefgezogene Schale mit Bördelrand, beschichteter
Kartondeckel, der in den Rand eingebördelt wird. Deckel hebt nach oben ab.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

ALU = '#EEF0F2'
FALTE = '#A9AFB5'
teile = [
    teil('deckel', 'cardboard_lid', 'Kartondeckel', 'Deckel', 'box',
         x=4, y=4, w=192, d=142, z=38.6, h=0.9, r=8, mass=4, materials=[['papier', 92], ['druck', 8]],
         info='Weißer Karton mit Beschriftungsfeld. Weil er innen beschichtet ist, gehört er nicht ins Altpapier, '
              'sondern in den Restmüll.',
         color='#E8E2D5', marks=[mark('box', 8, 8, 176, 126, 6, '#F4F2EE'),
                                 mark('box', 20, 20, 100, 8, 0, '#3A3F44'), mark('box', 20, 34, 70, 6, 0, '#3A3F44'),
                                 mark('box', 20, 62, 120, 1.2, 0, '#9A958C'), mark('box', 20, 80, 120, 1.2, 0, '#9A958C'),
                                 mark('box', 20, 98, 120, 1.2, 0, '#9A958C'),
                                 mark('cyl', 152, 96, 22, 22, fill='#D7D2C6'), mark('cyl', 157, 101, 12, 12, fill='#F4F2EE')]),
    teil('beschichtung', 'cardboard_lid', 'Innenbeschichtung des Deckels', 'Beschichtung', 'box',
         x=4, y=4, w=192, d=142, z=38, h=0.6, r=8, mass=1.2, material_id='aluminium',
         materials=[['alu', 55], ['ldpe', 45]], color='#D9DDE1',
         info='Hauchdünne Alu- oder PE-Schicht auf der Unterseite des Deckels. Sie hält Fett und Dampf ab und '
              'lässt sich nicht vom Karton lösen.',
         marks=[mark('box', 6, 6, 180, 130, 6, '#E6E9EC')]),
    teil('rand', 'aluminium_tray_body', 'Bördelrand', 'Rand', 'box',
         x=0, y=0, w=200, d=150, z=36, h=2, r=10, mass=2.5,
         info='Breiter, gerollter Rand. Er wird über den Deckel gedrückt und hält ihn fest. Vorsicht, die Kante kann '
              'scharf sein.',
         color=ALU, wand=6, boden=0,
         marks=[mark('box', 1.5, 1.5, 197, 147, 9, '#B7BDC3', zeichnung=True), mark('box', 3, 3, 194, 144, 8, ALU, zeichnung=True),
                           mark('box', 7, 7, 186, 136, 8, '#8E959C', zeichnung=True),
                           # Bodenrippen, durch die Öffnung sichtbar (nur Zeichnung)
                           mark('box', 20, 20, 160, 110, 10, '#9AA1A8', zeichnung=True),
                           *[mark('box', 30, 30 + i * 18, 140, 4, 2, '#868D94', zeichnung=True) for i in range(6)],
                           # Stauchfalten in den Ecken
                           mark('box', 2, 4, 5, 1.2, 0, FALTE), mark('box', 4, 2, 1.2, 5, 0, FALTE),
                           mark('box', 193, 4, 5, 1.2, 0, FALTE), mark('box', 194.8, 2, 1.2, 5, 0, FALTE),
                           mark('box', 2, 144.8, 5, 1.2, 0, FALTE), mark('box', 4, 143, 1.2, 5, 0, FALTE),
                           mark('box', 193, 144.8, 5, 1.2, 0, FALTE), mark('box', 194.8, 143, 1.2, 5, 0, FALTE)]),
    teil('wand', 'aluminium_tray_body', 'Schale oben', 'Schale', 'box',
         x=6, y=6, w=188, d=138, z=18, h=18, r=12, mass=5, label=False, wand=1, boden=0,
         info='Etwa 0,08 mm dünnes Aluminium, in die Form gepresst. Die Falten an den Ecken entstehen dabei.',
         color=ALU),
    teil('boden', 'aluminium_tray_body', 'Schale unten mit Boden', 'Schale', 'box',
         x=12, y=12, w=176, d=126, z=0, h=18, r=14, mass=4.5, wand=1,
         info='Essensreste auskratzen, dann in die Gelbe Tonne. Aluminium lässt sich ohne Qualitätsverlust einschmelzen.',
         color=ALU),
]
explodiere(teile, abstand=85, gruppen=[['rand', 'wand', 'boden']], abstaende={'deckel': 30})
skaliere_masse(teile, oid='aluminium_tray')
schreibe('aluminium_tray', teile)
