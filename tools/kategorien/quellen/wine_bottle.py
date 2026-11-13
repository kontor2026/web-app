"""3D-Modell: wine_bottle. Erzeugt tools/kategorien/modelle/wine_bottle.json.

Typische 0,75-l-Weinflasche (Bordeaux-Form, grünes Glas, 76 × 300 mm, Naturkorken, Kapsel aus Alufolie).
Glasabschnitte bewegen sich gemeinsam, Korken und Kapsel werden darüber gestapelt (Kapsel ganz oben, weil sie
zuerst entfernt wird), Etiketten seitlich herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

GLAS = '#2F5E3A'
OP = 0.7
teile = [
    teil('kapsel', 'aluminium_capsule_foil', 'Kapsel (Flaschenhalsfolie)', 'Kapsel', 'cyl',
         x=22.5, y=22.5, w=31, z=250, h=50, mass=1.5, materials=[['alu', 80], ['ldpe', 15], ['druck', 5]],
         info='Dünne Alufolie mit Kunststoff, schützt den Korken. Unter dem Wulst am Hals rundherum einschneiden '
              'und abziehen. Sie gehört in die Gelbe Tonne, nicht ins Altglas.',
         color='#7A1F2B', marks=[mark('cyl', 4, 4, 23, fill='#9C3340'), mark('cyl', 12, 12, 7, fill='#5A1620')]),
    teil('korken', 'cork_stopper', 'Naturkorken', 'Korken', 'cyl',
         x=26, y=26, w=24, z=254, h=45, mass=4,
         info='Aus der Rinde der Korkeiche gestanzt. Mit dem Korkenzieher herausziehen. Naturkorken werden '
              'gesammelt und zu Dämmstoff verarbeitet.',
         color='#C49A63', marks=[mark('cyl', 3, 3, 18, fill='#B08550')]),
    teil('mundstueck', 'glass_container', 'Mündung mit Wulst', 'Mündung', 'cyl',
         x=23, y=23, w=30, z=286, h=12, mass=12,
         info='Verdickter Rand, an dem die Kapsel sitzt. Teil der Flasche, in einem Stück geformt.',
         color=GLAS, opacity=OP, marks=[mark('cyl', 3, 3, 24, fill='#C49A63')]),
    teil('hals', 'glass_container', 'Flaschenhals', 'Hals', 'cyl',
         x=23.5, y=23.5, w=29, z=240, h=46, mass=40,
         info='Langer, schmaler Hals, in dem der Korken steckt.', color=GLAS, opacity=OP),
    teil('schulter_oben', 'glass_container', 'Flaschenschulter (oben)', 'Schulter', 'cyl',
         x=18, y=18, w=40, z=225, h=15, mass=28,
         info='Die Schulter hält beim Einschenken den Weinstein zurück.', color=GLAS, opacity=OP, label=False),
    teil('schulter', 'glass_container', 'Flaschenschulter', 'Schulter', 'cyl',
         x=6, y=6, w=64, z=205, h=20, mass=45,
         info='Ausgeprägte Schulter der Bordeauxflasche. Grünes Glas schützt den Wein vor Licht.',
         color=GLAS, opacity=OP),
    teil('koerper', 'glass_container', 'Flaschenkörper', 'Körper', 'cyl',
         x=0, y=0, w=76, z=0, h=205, mass=370,
         info='Kalk-Natron-Glas aus Sand, Soda und Kalk. Unten mit Einstich (Boden nach innen gewölbt). '
              'Leer in den Grünglas-Container geben, Korken vorher heraus.',
         color=GLAS, opacity=OP, marks=[mark('cyl', 6, 6, 64)]),
    teil('halsschild', 'paper_label', 'Halsschild', 'Halsschild', 'box',
         x=52.5, y=28, w=0.3, d=20, z=245, h=14, r=0, explode=[55, 0, 0], mass=0.3,
         info='Kleines Papierschild mit dem Jahrgang. Darf am Glas bleiben.', color='#E9DFC4', sortBias=100),
    teil('etikett', 'paper_label', 'Bauchetikett', 'Etikett', 'box',
         x=76, y=13, w=0.3, d=50, z=70, h=95, r=0, explode=[55, 0, 0], mass=2.2,
         info='Papier mit Leim. In warmem Wasser lässt es sich ablösen, beim Altglas darf es aber dranbleiben: '
              'Es verbrennt in der Schmelze.',
         color='#EFE6CF', sortBias=100),
]
explodiere(teile, abstand=22, nach_liste=True,
           gruppen=[['mundstueck', 'hals', 'schulter_oben', 'schulter', 'koerper']])
skaliere_masse(teile, oid='wine_bottle')
schreibe('wine_bottle', teile)
