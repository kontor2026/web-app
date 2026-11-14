"""3D-Modell: bubble_wrap. Erzeugt tools/kategorien/modelle/bubble_wrap.json.

Typischer Zuschnitt Luftpolsterfolie (30 × 80 cm, Noppen 20 mm, ca. 4,5 mm hoch), einmal gefaltet auf 30 × 40 cm
(Falz hinten bei y = 0). Jede Hälfte besteht aus Noppenfolie und glatter Trägerfolie; die untere Hälfte hat die
Noppen oben, die umgeklappte obere unten. Die Lagen werden nach oben abgehoben, der Falz nach hinten gezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

FOLIE = '#E4EEF1'
NOPPE = '#AFCAD4'
LDPE = [['ldpe', 100]]
NOPPEN = (raster(5, 5, 12, 16, 20, 20, 24.2, 24.5, shape='cyl', fill=NOPPE)  # 20-mm-Noppen auf 300 × 394 mm
          + [dict(m, zeichnung=True) for m in raster(9, 8, 12, 16, 6, 5, 24.2, 24.5, shape='cyl', fill='#F7FBFC')])  # Glanzlicht je Noppe
teile = [
    teil('traeger_oben', 'ldpe_film', 'Trägerfolie (obere Hälfte)', 'Trägerfolie', 'box',
         x=0, y=6, w=300, d=394, z=9.5, h=0.5, r=1, mass=2.4, materials=LDPE, color=FOLIE, opacity=0.6,
         info='Glatte LDPE-Folie, auf die die Noppenfolie warm aufgeschweißt ist. Durch sie sieht man die Noppen.',
         marks=raster(5, 5, 12, 16, 20, 20, 24.2, 24.5, shape='cyl', fill='#C2D7DE')),
    teil('noppen_oben', 'ldpe_film', 'Noppenfolie (obere Hälfte)', 'Noppenfolie', 'box',
         x=0, y=6, w=300, d=394, z=5, h=4.5, r=1, mass=3.6, materials=LDPE, color=FOLIE, opacity=0.55,
         info='Tiefgezogene Folie mit Luftblasen. Die eingeschlossene Luft federt Stöße ab. Umgeklappt zeigen die '
              'Noppen nach unten.',
         marks=NOPPEN),
    teil('noppen_unten', 'ldpe_film', 'Noppenfolie (untere Hälfte)', 'Noppen unten', 'box',
         x=0, y=6, w=300, d=394, z=0.5, h=4.5, r=1, mass=3.6, materials=LDPE, color=FOLIE, opacity=0.55,
         info='Zerplatzte Noppen machen nichts: die Folie bleibt reines LDPE. Mehrfach verwenden, dann sauber in die '
              'Gelbe Tonne.',
         marks=NOPPEN),
    teil('traeger_unten', 'ldpe_film', 'Trägerfolie (untere Hälfte)', 'Träger unten', 'box',
         x=0, y=6, w=300, d=394, z=0, h=0.5, r=1, mass=2.4, materials=LDPE, color=FOLIE, opacity=0.6, label=False,
         info='Unterseite der Folie. Beide Lagen sind aus demselben Kunststoff und müssen nicht getrennt werden.'),
    teil('falz', 'ldpe_film', 'Falzkante', 'Falz', 'box',
         x=0, y=0, w=300, d=6, z=0, h=10, r=2, explode=[0, -50, 0], mass=0.3, materials=LDPE, color=FOLIE,
         opacity=0.7,
         info='Hier ist der Zuschnitt umgeklappt. Die Noppen am Knick werden oft zerdrückt.',
         marks=raster(5, 1, 12, 1, 20, 4, 24.2, fill=NOPPE)),
]
explodiere(teile, abstand=100)
skaliere_masse(teile, oid='bubble_wrap')
schreibe('bubble_wrap', teile)
