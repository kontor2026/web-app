"""3D-Modell: ring_binder. Erzeugt tools/kategorien/modelle/ring_binder.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# A4-Ordner (8 cm Rücken) flach auf dem Tisch, Vorderdeckel oben, Rücken links (x = 0). 285 × 320 × 80 mm laut CSV.
# Graupappe-Deckel mit PP-Folie kaschiert, Hebelmechanik auf dem Rückdeckel vernietet, Stahlkanten unten.
# Explodiert: Ebenen nach oben, Rücken und Rückenschild nach links herausgezogen.
PAPPE = '#8C9AA6'
FOLIE = '#3E6E9E'
STAHL = '#B8BEC4'

teile = [
    teil('folie_vorne', 'pp_cover_film', 'PP-Folie Vorderdeckel', 'Folie vorne', 'box',
         x=3, y=0, w=282, d=320, z=79.6, h=0.4, r=2, mass=7,
         info='Hauchdünne Polypropylenfolie, die die Pappe abwaschbar macht. Abziehen, dann darf die Pappe ins Altpapier.',
         color=FOLIE, opacity=0.8, marks=[mark('box', 90, 120, 120, 70, 3, '#F3F1EC')]),
    teil('kante_vorne', 'cardboard_cover', 'Stahlkante Vorderdeckel', 'Kante vorne', 'box',
         x=3, y=314, w=282, d=6, z=80, h=0.6, r=0, mass=5, material_id='steel',
         info='Schmaler Stahlstreifen an der Unterkante, damit der Ordner im Regal nicht durchscheuert. Mit einer Zange abbiegen.',
         color=STAHL),
    teil('deckel_vorne', 'cardboard_cover', 'Vorderdeckel (Graupappe)', 'Vorderdeckel', 'box',
         x=3, y=0, w=282, d=320, z=77, h=2.6, r=2, mass=165,
         info='Feste Graupappe aus Altpapier. Ohne Folie und Metall gehört sie ins Altpapier.',
         color=PAPPE),
    teil('ring_vorne', 'ring_mechanism', 'Bügel vorne', 'Bügel vorne', 'box',
         x=28, y=112, w=30, d=8, z=6.6, h=68, r=3, mass=14,
         info='Halbrunder Stahlbügel, der durch die Lochung der Blätter greift. Er öffnet sich mit dem Hebel.',
         color=STAHL),
    teil('ring_hinten', 'ring_mechanism', 'Bügel hinten', 'Bügel hinten', 'box',
         x=28, y=192, w=30, d=8, z=6.6, h=68, r=3, mass=14, label=False,
         info='Zweiter Bügel im Abstand von 8 cm, genau passend zur Zweifachlochung.',
         color=STAHL),
    teil('hebel', 'ring_mechanism', 'Hebel', 'Hebel', 'box',
         x=30, y=215, w=40, d=50, z=6.6, h=8, r=6, mass=18,
         info='Stahlhebel, der die Bügel öffnet und schließt. Mit dem Niederhalter zusammen hält er das Papier fest.',
         color=STAHL, marks=[mark('cyl', 12, 30, 16, 12, fill='#8E969A')]),
    teil('grundplatte', 'ring_mechanism', 'Grundplatte der Mechanik', 'Grundplatte', 'box',
         x=20, y=80, w=60, d=190, z=2.6, h=4, r=4, mass=55,
         info='Gestanztes Stahlblech, das alle Teile der Mechanik trägt. Wertvoller Stahlschrott für den Wertstoffhof.',
         color='#9AA2A6', marks=[mark('box', 8, 10, 44, 170, 3, '#B0B6BA')]),
    teil('niete', 'ring_mechanism', 'Nieten', 'Nieten', 'box',
         x=45, y=86, w=10, d=178, z=0, h=2.6, r=3, mass=4,
         info='Zwei Hohlnieten halten die Mechanik in der Pappe. Aufbohren oder mit einem Schraubendreher aufhebeln.',
         color='#8E969A', marks=[mark('cyl', 1, 1, 8), mark('cyl', 1, 169, 8)]),
    teil('deckel_hinten', 'cardboard_cover', 'Rückdeckel (Graupappe)', 'Rückdeckel', 'box',
         x=3, y=0, w=282, d=320, z=0.4, h=2.6, r=2, mass=165,
         info='Trägt die Mechanik. Erst die Mechanik abtrennen, dann die Pappe ins Altpapier.',
         color=PAPPE, marks=[mark('cyl', 260, 150, 10, 20, fill='#5A6268')]),
    teil('kante_hinten', 'cardboard_cover', 'Stahlkante Rückdeckel', 'Kante hinten', 'box',
         x=3, y=314, w=282, d=6, z=-0.6, h=0.6, r=0, mass=5, material_id='steel', label=False,
         info='Gegenstück zur vorderen Stahlkante.',
         color=STAHL),
    teil('folie_hinten', 'pp_cover_film', 'PP-Folie Rückdeckel', 'Folie hinten', 'box',
         x=3, y=0, w=282, d=320, z=0, h=0.4, r=2, mass=7,
         info='Folie auf der Rückseite. Sie ist nur aufgeklebt und lässt sich von einer Ecke aus abziehen.',
         color=FOLIE, opacity=0.8),
    teil('ruecken', 'cardboard_cover', 'Rücken mit Griffloch', 'Rücken', 'box',
         x=0, y=0, w=3, d=320, z=0, h=80, r=0, explode=[-60, 0, 0], mass=48, materials=[['papier', 90], ['pp', 10]],
         info='Pappe des Rückens, mit Folie bezogen. Im Griffloch steckt oft ein Metallring, der vorher heraus muss.',
         color=FOLIE),
    teil('rueckenschild', 'cardboard_cover', 'Rückenschild', 'Rückenschild', 'box',
         x=-0.3, y=40, w=0.3, d=180, z=10, h=60, r=0, explode=[-120, 0, 0], mass=2, material_id='paper',
         materials=[['papier', 95], ['druck', 5]],
         info='Papierschild zum Beschriften, in einer Folientasche. Darf ins Altpapier.',
         color='#F3F1EC'),
]

explodiere(teile, abstand=55, nach_liste=True, abstaende={'niete': 25},
           gruppen=[['folie_vorne', 'kante_vorne'], ['folie_hinten', 'kante_hinten']])
skaliere_masse(teile, oid='ring_binder')
schreibe('ring_binder', teile)
