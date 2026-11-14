"""3D-Modell: takeaway_container. Erzeugt tools/kategorien/modelle/takeaway_container.json.

Typische Mikrowellen-Einwegbox 750 ml aus PP (18 × 12 × 5 cm): Schale mit umlaufendem Siegelrand, konische Wand,
aufgeschnappter Deckel mit Versteifungsrille. Deckel hebt nach oben ab.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

SCHWARZ = '#2A2C2E'
KLAR = '#E6ECEF'
teile = [
    teil('deckel', 'pp_lid', 'Schnappdeckel', 'Deckel', 'box',
         x=0, y=0, w=180, d=120, z=40, h=10, r=14, mass=6.5, opacity=0.7,
         info='Klarer PP-Deckel, schnappt über den Rand der Schale. An der Ecklasche abziehen, '
              'Deckel und Schale zusammen in die Gelbe Tonne.',
         color=KLAR, marks=[mark('box', 6, 6, 168, 108, 11, '#C9D0D5'), mark('box', 10, 10, 160, 100, 9, KLAR),
                            mark('box', 24, 22, 132, 76, 7, '#D5DCE0'), mark('box', 28, 26, 124, 68, 5, KLAR),
                            mark('cyl', 150, 86, 14, 10, fill='#C9D0D5'),
                            mark('box', 0, 0, 14, 14, 6, '#C9D0D5')]),
    teil('siegel', 'pp_lid', 'Siegelaufkleber', 'Aufkleber', 'box',
         material_id='paper', x=80, y=120, w=24, d=0.3, z=28, h=20, r=0, explode=[-30, 55, 50], mass=0.3,
         materials=[['papier', 85], ['druck', 5], ['klebstoff', 10]],
         info='Papieraufkleber über Deckel und Schale, zeigt dass die Box seit dem Einpacken zu ist. '
              'Kleine Papierreste dürfen dranbleiben.',
         color='#E2574C', sortBias=60),
    teil('rand', 'pp_food_tray', 'Schale mit Siegelrand', 'Schale', 'box',
         x=0, y=0, w=180, d=120, z=36, h=4, r=14, mass=3,
         info='PP hält die Hitze aus der Mikrowelle aus. Schwarzer Kunststoff wird von Sortieranlagen schlecht '
              'erkannt; Essensreste auskratzen, ausspülen ist nicht nötig.',
         color=SCHWARZ, wand=6, boden=0, marks=[mark('box', 6, 6, 168, 108, 10, '#1D2023', zeichnung=True), mark('box', 18, 16, 144, 88, 8, '#25292D', zeichnung=True),
                               mark('box', 0, 0, 14, 14, 6, '#3A3F44')]),
    teil('wand', 'pp_food_tray', 'Schale oben', 'Schale', 'box',
         x=6, y=6, w=168, d=108, z=18, h=18, r=12, mass=5.5, label=False,
         info='Die Wand ist nur etwa 0,5 mm dick. Rillen in der Wand machen die Schale steif.',
         color=SCHWARZ, wand=1, boden=0),
    teil('boden', 'pp_food_tray', 'Schale unten mit Boden', 'Boden', 'box',
         x=11, y=11, w=158, d=98, z=0, h=18, r=10, mass=5, label=False,
         info='Die Schale wird nach unten schmaler, damit sich viele Schalen ineinander stapeln lassen.',
         color=SCHWARZ, wand=1),
]
explodiere(teile, abstand=110, gruppen=[['rand', 'wand', 'boden']])
skaliere_masse(teile, oid='takeaway_container')
schreibe('takeaway_container', teile)
