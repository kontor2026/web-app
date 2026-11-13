"""3D-Modell: eraser. Erzeugt tools/kategorien/modelle/eraser.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

# Radiergummi flach auf dem Tisch, 20 × 40 × 10 mm laut CSV, Länge entlang y. Eine Papiermanschette umschließt die
# Mitte (oben, unten, beide Seiten). Explodiert: Radierblock nach vorne aus der Manschette gezogen (dy > 0),
# Oberseite der Manschette angehoben, Seitenteile nach außen geklappt.
WEISS = '#F3F1EC'
HUELLE = '#3E6E9E'

teile = [
    teil('manschette_oben', 'paper_label', 'Papiermanschette (Oberseite)', 'Manschette', 'box',
         x=0, y=8, w=20, d=24, z=9.7, h=0.3, r=0, explode=[0, 0, 16], mass=0.08, materials=[['papier', 92], ['druck', 8]],
         info='Bedruckter Papierstreifen um den Radierer. Er schützt die Kanten und lässt sich einfach abstreifen; ins Altpapier.',
         color=HUELLE, marks=[mark('box', 2, 6, 16, 6, 1, WEISS), mark('box', 2, 15, 16, 3, 0.5, '#F2E23A')]),
    teil('manschette_links', 'paper_label', 'Manschette (linke Seite)', 'Seite links', 'box',
         x=0, y=8, w=0.3, d=24, z=0.3, h=9.4, r=0, explode=[-14, 0, 22], mass=0.03, label=False,
         info='Seitenteil des Papierstreifens.',
         color=HUELLE),
    teil('manschette_rechts', 'paper_label', 'Manschette (rechte Seite)', 'Seite rechts', 'box',
         x=19.7, y=8, w=0.3, d=24, z=0.3, h=9.4, r=0, explode=[14, 0, 0], mass=0.03, label=False,
         info='Seitenteil des Papierstreifens.',
         color=HUELLE),
    teil('radierer', 'eraser_block', 'Radierblock', 'Radierer', 'box',
         x=0.3, y=0, w=19.4, d=40, z=0.3, h=9.4, r=1.5, explode=[0, 52, 0], mass=14.8,
         materials=[['gummi', 65], ['tpe', 35]],
         info='Weicher Kunststoff-Radierer (synthetischer Kautschuk mit Weichmachern), nimmt Grafit vom Papier auf. '
              'Am besten ganz aufbrauchen, Reste in den Restmüll.',
         color=WEISS, marks=[mark('box', 0, 0, 19.4, 3, 1.5, '#E4E1D8')]),
    teil('manschette_unten', 'paper_label', 'Manschette (Unterseite)', 'Unterseite', 'box',
         x=0, y=8, w=20, d=24, z=0, h=0.3, r=0, explode=[0, 0, 0], mass=0.08,
         info='Hier sind die Enden des Papierstreifens überlappend verklebt.',
         color=HUELLE, marks=[mark('box', 8, 0, 6, 24, 0, '#2F5A85')]),
]

skaliere_masse(teile, oid='eraser', stellen=2)
schreibe('eraser', teile)
