"""3D-Modell: baking_tray. Erzeugt tools/kategorien/modelle/baking_tray.json.

Typisches emailliertes Backblech (460 × 380 × 20 mm, 1,3 kg): tiefgezogenes Stahlblech mit Rollrand und
eingerolltem Versteifungsdraht, innen und außen Emaille. Explodiert schweben Draht, Innen-Emaille, Blech und
Außen-Emaille übereinander.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

EMAILLE = '#2E3134'
teile = [
    teil('draht', 'steel_baking_tray', 'Versteifungsdraht im Rollrand', 'Randdraht', 'box',
         x=0, y=0, w=460, d=380, z=16, h=4, r=15, mass=90,
         info='Stahldraht, um den der obere Rand eingerollt ist. Er verhindert, dass sich das Blech in der Hitze '
              'verzieht.',
         color='#9DA4AA', marks=[mark('box', 4, 4, 452, 372, 12, '#C4C9CD')]),
    teil('emaille_innen', 'steel_baking_tray', 'Emaille innen', 'Emaille innen', 'box',
         material_id='special_glass', x=4, y=4, w=452, d=372, z=0.9, h=0.2, r=12, mass=45,
         materials=[['emaille', 100]],
         info='Glasartige Schicht, bei 800 °C auf den Stahl geschmolzen. Hart und kratzfest; im Metallwerk '
              'schmilzt sie zu Schlacke.',
         color=EMAILLE, marks=[mark('box', 12, 12, 428, 348, 8, '#383B3F')]),
    teil('blech', 'steel_baking_tray', 'Stahlblech mit Rollrand', 'Blech', 'box',
         x=0, y=0, w=460, d=380, z=0.1, h=19.9, r=15, mass=1370,
         info='Tiefgezogenes Stahlblech, 1 mm dick. Zum Altmetall auf den Wertstoffhof, nicht in die Gelbe Tonne. '
              'Mit Magnet erkennbar: Stahl haftet, Aluminiumbleche nicht.',
         color='#6E767C', marks=[mark('box', 4, 4, 452, 372, 12, '#5E656A'), mark('box', 16, 16, 428, 348, 8, '#80878D')]),
    teil('emaille_aussen', 'steel_baking_tray', 'Emaille außen', 'Emaille außen', 'box',
         material_id='special_glass', x=0, y=0, w=460, d=380, z=0, h=0.1, r=15, mass=45,
         materials=[['emaille', 100]],
         info='Dünnere Emailleschicht auf der Unterseite, schützt vor Rost.',
         color=EMAILLE),
]
explodiere(teile, abstand=110, nach_liste=True)
skaliere_masse(teile, oid='baking_tray')
schreibe('baking_tray', teile)
