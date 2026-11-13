"""3D-Modell: pencil_sharpener. Erzeugt tools/kategorien/modelle/pencil_sharpener.json.

Einfacher Metall-Anspitzer (Keilform) 25 × 35 × 20 mm, Bleistiftöffnung vorne (y = 35). Körper aus Aluminium-
Druckguss mit Griffrillen, die Stahlklinge liegt oben in einer Vertiefung neben dem längs laufenden Spanschlitz und wird von einer
Schraube gehalten. Explodiert: Klinge und Schraube nach oben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

teile = [
    teil('schraube', 'hinge_screws', 'Klingenschraube', 'Schraube', 'cyl',
         x=5.5, y=13.5, w=5, z=18, h=2, mass=0.3, color='#7B848B', sortBias=4,
         info='Winzige Kreuzschlitzschraube M2. Mit einem Feinmechaniker-Schraubendreher lösen, dann kann man '
              'die Klinge tauschen.',
         marks=[mark('box', 2.1, 0.8, 0.8, 3.4, fill='#3A3F44'), mark('box', 0.8, 2.1, 3.4, 0.8, fill='#3A3F44')]),
    teil('klinge', 'sharpener_blade', 'Messerklinge', 'Klinge', 'box',
         x=3, y=4, w=12, d=27, z=17, h=1, r=0.8, mass=1.5, color='#C3C9CE', sortBias=2,
         info='Gehärteter Stahl, die Schneide (rechts) steht über dem Spanschlitz. Vorsicht beim Anfassen, '
              'alte Klingen eingewickelt zum Metall geben.',
         marks=[mark('box', 10.5, 0.8, 1.2, 25.4, 0, '#E8ECEF'), mark('cyl', 3, 10, 4, fill='#8A9298'),
                mark('box', 1, 1, 8, 2, 0, '#AEB5BA')]),
    teil('korpus', 'sharpener_body', 'Anspitzerkörper (Aluminium)', 'Körper', 'box',
         x=0, y=0, w=25, d=35, z=0, h=18, r=2, mass=13, color='#A9B1B8',
         info='Aluminium-Druckguss mit kegelförmiger Bohrung für den Stift. Ohne Klinge ist es sortenreiner '
              'Aluminiumschrott.',
         marks=[mark('box', 2, 3, 14, 29, 1, '#959DA4'), mark('box', 15, 3, 3, 29, 1, '#2E3236'),
                mark('cyl', 8, 15, 2, fill='#5E666C'), mark('box', 19, 3, 4, 29, 1, '#B3BBC1')]
         + raster(20, 6, 1, 7, 3, 1.2, 0, 4, fill='#8C949B')),
]
explodiere(teile, abstand=8)
skaliere_masse(teile, oid='pencil_sharpener', stellen=2)
schreibe('pencil_sharpener', teile)
