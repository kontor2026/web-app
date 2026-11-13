"""3D-Modell: takeaway_container. Erzeugt tools/kategorien/modelle/takeaway_container.json.

Typische Mikrowellen-Einwegbox 750 ml aus PP (18 × 12 × 5 cm): Schale mit umlaufendem Siegelrand, konische Wand,
aufgeschnappter Deckel mit Versteifungsrille. Deckel hebt nach oben ab.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

SCHWARZ = '#2E3236'
KLAR = '#E6ECEF'
teile = [
    teil('deckel', 'pp_lid', 'Schnappdeckel', 'Deckel', 'box',
         x=0, y=0, w=180, d=120, z=40, h=10, r=14, mass=6.5, opacity=0.7,
         info='Klarer PP-Deckel, schnappt über den Rand der Schale. An der Ecklasche abziehen, '
              'Deckel und Schale zusammen in die Gelbe Tonne.',
         color=KLAR, marks=[mark('box', 6, 6, 168, 108, 11, '#C9D0D5'), mark('box', 10, 10, 160, 100, 9, KLAR),
                            mark('box', 0, 0, 14, 14, 6, '#C9D0D5')]),
    teil('rand', 'pp_food_tray', 'Siegelrand', 'Rand', 'box',
         x=0, y=0, w=180, d=120, z=36, h=4, r=14, mass=3,
         info='Umlaufender Rand, über den der Deckel schnappt.',
         color=SCHWARZ, marks=[mark('box', 6, 6, 168, 108, 10, '#1D2023')]),
    teil('wand', 'pp_food_tray', 'Schale oben', 'Schale', 'box',
         x=6, y=6, w=168, d=108, z=18, h=18, r=12, mass=5.5,
         info='PP hält die Hitze aus der Mikrowelle aus. Schwarzer Kunststoff wird von Sortieranlagen schlecht erkannt; '
              'Essensreste auskratzen, ausspülen ist nicht nötig.',
         color=SCHWARZ),
    teil('boden', 'pp_food_tray', 'Schale unten mit Boden', 'Boden', 'box',
         x=11, y=11, w=158, d=98, z=0, h=18, r=10, mass=5, label=False,
         info='Die Schale wird nach unten schmaler, damit sich viele Schalen ineinander stapeln lassen.',
         color=SCHWARZ),
]
explodiere(teile, abstand=55, gruppen=[['rand', 'wand', 'boden']])
skaliere_masse(teile, oid='takeaway_container')
schreibe('takeaway_container', teile)
