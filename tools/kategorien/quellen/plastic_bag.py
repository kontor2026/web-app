"""3D-Modell: plastic_bag. Erzeugt tools/kategorien/modelle/plastic_bag.json.

Typische Hemdchen-/Tragetasche aus LDPE, flach hingelegt (30 × 45 cm, Griffe hinten bei y = 0): Vorderlage mit
Aufdruck, eingefaltete Seitenfalten, Rücklage, zwei Griffschlaufen aus der Doppellage. Lagen werden nach oben
abgehoben, die Griffe nach hinten gezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

FOLIE = '#EDEDE8'
LDPE = [['ldpe', 98], ['druck', 2]]
teile = [
    teil('vorderlage', 'ldpe_film', 'Vorderlage mit Aufdruck', 'Vorderlage', 'box',
         x=0, y=80, w=300, d=370, z=2, h=1, r=2, mass=7.5, materials=LDPE, opacity=0.85,
         info='Etwa 0,03 mm dünne LDPE-Folie (Recyclingcode 4). Der Aufdruck ist nur Farbe auf der Folie und '
              'stört beim Recycling kaum.',
         color=FOLIE, marks=[mark('cyl', 90, 110, 120, fill='#2F8A4E'), mark('box', 70, 250, 160, 20, 4, '#2F8A4E'),
                             mark('box', 0, 358, 300, 8, 0, '#D4D4CE'), mark('box', 0, 0, 300, 4, 0, '#D4D4CE')]),
    teil('falte_links', 'ldpe_film', 'Seitenfalte links', 'Seitenfalte', 'box',
         x=0, y=80, w=50, d=370, z=1, h=1, r=1, mass=1.6, materials=[['ldpe', 100]], opacity=0.85,
         info='Nach innen gefaltete Seitenwand, damit die Tüte voll gepackt breiter wird.',
         color='#E2E2DC', marks=[mark('box', 24, 0, 2, 370, 0, '#C9C9C2')]),
    teil('falte_rechts', 'ldpe_film', 'Seitenfalte rechts', 'Seitenfalte', 'box',
         x=250, y=80, w=50, d=370, z=1, h=1, r=1, mass=1.6, materials=[['ldpe', 100]], opacity=0.85, label=False,
         info='Gegenstück zur linken Seitenfalte.',
         color='#E2E2DC', marks=[mark('box', 24, 0, 2, 370, 0, '#C9C9C2')]),
    teil('ruecklage', 'ldpe_film', 'Rücklage mit Bodennaht', 'Rücklage', 'box',
         x=0, y=80, w=300, d=370, z=0, h=1, r=2, mass=7, materials=[['ldpe', 100]], opacity=0.9,
         info='Hinten und vorne sind unten heiß verschweißt. Leere Tüten lieber wiederverwenden, '
              'kaputte locker in die Gelbe Tonne geben.',
         color=FOLIE, marks=[mark('box', 0, 358, 300, 8, 0, '#D4D4CE')]),
    teil('griff_links', 'ldpe_film', 'Griffschlaufe links', 'Griff', 'box',
         x=0, y=0, w=70, d=80, z=0, h=3, r=10, explode=[0, -50, 0], mass=1.2, materials=[['ldpe', 100]],
         opacity=0.85,
         info='Henkel aus derselben Folie, beim Ausstanzen der Griffmulde entstanden. Hier reißen Tüten am '
              'häufigsten ein.',
         color=FOLIE, marks=[mark('box', 0, 0, 70, 6, 3, '#D4D4CE')]),
    teil('griff_rechts', 'ldpe_film', 'Griffschlaufe rechts', 'Griff', 'box',
         x=230, y=0, w=70, d=80, z=0, h=3, r=10, explode=[0, -50, 0], mass=1.2, materials=[['ldpe', 100]],
         opacity=0.85, label=False,
         info='Gegenstück zur linken Schlaufe.',
         color=FOLIE, marks=[mark('box', 0, 0, 70, 6, 3, '#D4D4CE')]),
]
explodiere(teile, abstand=100)
skaliere_masse(teile, oid='plastic_bag')
schreibe('plastic_bag', teile)
