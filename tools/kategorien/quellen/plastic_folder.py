"""3D-Modell: plastic_folder. Erzeugt tools/kategorien/modelle/plastic_folder.json.

Kunststoff-Schnellhefter A4 (220 × 310 mm), geschlossen, Rücken links (x = 0). Vorderdeckel aus transparentem PP,
Rückendeckel aus gefärbtem PP mit Beschriftungsstreifen, innen links die Heftmechanik: zwei Stahl-Heftbänder
(Lochabstand 80 mm) und die PP-Deckschiene, die sie festklemmt. Explodiert: Vorderdeckel nach links aufgeklappt, Mechanik und Beschriftungsstreifen nach oben abgehoben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

teile = [
    teil('vorderdeckel', 'pp_sheet', 'Vorderdeckel (transparent)', 'Vorderdeckel', 'box',
         x=0, y=0, w=218, d=305, z=1.6, h=0.2, r=3, mass=12, color='#E6F0F4', opacity=0.6, explode=[-250, 0, 0],
         info='Klarsichtfolie aus Polypropylen, am Rücken mit dem Rückendeckel verschweißt. Ohne Papier '
              'und Metall gehört der Hefter in die Wertstofftonne oder den Restmüll, je nach Gemeinde.',
         marks=[mark('box', 2, 4, 6, 297, 0, '#C8D6DC'), mark('box', 10, 4, 1, 297, 0, '#C8D6DC'),
                mark('box', 214, 4, 2, 297, 0, '#D3E0E6')]),
    teil('deckschiene', 'pp_sheet', 'Deckschiene', 'Deckschiene', 'box',
         x=10, y=85, w=14, d=140, z=1.0, h=0.5, r=2, mass=2,
         info='Wird über die umgebogenen Heftbänder geschoben und hält die Blätter. Zum Leeren zur Seite schieben.',
         color='#2C6FB0', marks=[mark('cyl', 4, 21, 6, fill='#245C93'), mark('cyl', 4, 113, 6, fill='#245C93')]),
    teil('heftbaender', 'pp_sheet', 'Heftbänder aus Stahl', 'Heftbänder', 'box',
         x=12, y=90, w=10, d=130, z=0.5, h=0.4, r=1, mass=3, material_id='steel', color='#B5BCC2',
         info='Zwei flache Stahlzungen, die durch die Lochung der Blätter gesteckt werden. Vor dem Entsorgen '
              'herausziehen, sie gehören zum Metall.',
         marks=[mark('box', 2, 20, 6, 10, 1, '#8A9298'), mark('box', 2, 100, 6, 10, 1, '#8A9298')]),
    teil('etikett', 'pp_sheet', 'Beschriftungsstreifen (Papier)', 'Etikett', 'box',
         x=191, y=22, w=20, d=266, z=0.5, h=0.2, r=1, mass=1.5, material_id='paper', color='#F4F1EA',
         info='Eingeschobener Papierstreifen zum Beschriften. Herausziehen und ins Altpapier geben.',
         marks=[mark('box', 4, 20, 2, 200, 0, '#9AA3A8'), mark('box', 9, 30, 2, 150, 0, '#B4BCC0')]),
    teil('rueckdeckel', 'pp_sheet', 'Rückendeckel mit Beschriftungsstreifen', 'Rückendeckel', 'box',
         x=0, y=0, w=220, d=310, z=0, h=0.5, r=3, mass=13, color='#2C6FB0',
         info='Gefärbtes Polypropylen. Der Beschriftungsstreifen ist ein eingestecktes Papier, das vorher '
              'ins Altpapier kommt.',
         marks=[mark('box', 6, 4, 14, 302, 0, '#245C93'), mark('box', 188, 18, 26, 274, 1, '#3A7DBF'),
                mark('cyl', 2, 112, 5, fill='#EDEAE3'), mark('cyl', 2, 192, 5, fill='#EDEAE3'),
                mark('box', 30, 10, 150, 290, 2, '#2A69A7')]),
]
explodiere(teile, abstand=30, abstaende={'heftbaender': 25, 'deckschiene': 25, 'etikett': 80})
skaliere_masse(teile, oid='plastic_folder')
schreibe('plastic_folder', teile)
