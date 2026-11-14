"""3D-Modell: food_container. Erzeugt tools/kategorien/modelle/food_container.json.

Typische Frischhaltedose aus Polypropylen (ca. 1 l, 18 × 12 × 7 cm) mit Klickdeckel: vier angespritzte
Verschlusslaschen und eine Silikondichtung in der Deckelnut. Explodiert: Dose unten, Dichtung und Deckel
darüber, die Laschen auf Deckelhöhe nach außen geklappt.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

DOSE = '#E8EEF0'
DECKEL = '#4A90B8'
LASCHE = '#3C7DA3'
DZ = 34  # Deckelhöhe explodiert, siehe Ausgabe von explodiere

LASCHE_INFO = ('Klappe mit Filmscharnier, aus einem Stück mit dem Deckel gespritzt. Sie schnappt unter den Rand der '
               'Dose. Bricht sie ab, ist der Deckel undicht.')
teile = [
    teil('deckel', 'pp_lid', 'Klickdeckel', 'Deckel', 'box',
         x=0, y=0, w=180, d=120, z=62, h=8, r=14, mass=34,
         info='Polypropylen (PP, Recyclingcode 5). Deckel abnehmen, Dichtung herausziehen, dann gehören Deckel und '
              'Dose in die Gelbe Tonne.',
         color=DECKEL, marks=[mark('box', 10, 10, 160, 100, 10, '#5AA0C8'), mark('box', 70, 50, 40, 20, 6, '#3C7DA3')]),
    teil('lasche_vorne', 'pp_lid', 'Verschlusslasche vorne', 'Lasche', 'box',
         x=70, y=116, w=40, d=4, z=50, h=20, r=1.5, explode=[0, 26, DZ], mass=2, info=LASCHE_INFO, color=LASCHE),
    teil('lasche_hinten', 'pp_lid', 'Verschlusslasche hinten', 'Lasche', 'box',
         x=70, y=0, w=40, d=4, z=50, h=20, r=1.5, explode=[0, -26, DZ], mass=2, label=False,
         info=LASCHE_INFO, color=LASCHE),
    teil('lasche_links', 'pp_lid', 'Verschlusslasche links', 'Lasche', 'box',
         x=0, y=45, w=4, d=30, z=50, h=20, r=1.5, explode=[-26, 0, DZ], mass=2, label=False,
         info=LASCHE_INFO, color=LASCHE),
    teil('lasche_rechts', 'pp_lid', 'Verschlusslasche rechts', 'Lasche', 'box',
         x=176, y=45, w=4, d=30, z=50, h=20, r=1.5, explode=[26, 0, DZ], mass=2, label=False,
         info=LASCHE_INFO, color=LASCHE),
    teil('dichtung', 'silicone_seal', 'Silikondichtung', 'Dichtung', 'box',
         x=4, y=4, w=172, d=112, z=61, h=3, r=12, mass=5,
         info='Weicher Silikonring in der Nut des Deckels, macht die Dose auslaufsicher. Mit einem stumpfen Messer '
              'herausziehen: Silikon kommt in den Restmüll.',
         color='#F2F2F2', opacity=0.85, wand=3, boden=0, marks=[mark('box', 4, 4, 164, 104, 9, DECKEL, zeichnung=True)]),
    teil('rand', 'pp_food_tray', 'Dosenrand', 'Rand', 'box',
         x=2, y=2, w=176, d=116, z=55, h=6, r=13, mass=12,
         info='Verstärkter Rand mit Wulst, unter den die Laschen greifen.',
         color=DOSE, opacity=0.85, wand=4, boden=0, marks=[mark('box', 4, 4, 168, 108, 10, '#D8E0E3', zeichnung=True)]),
    teil('schale', 'pp_food_tray', 'Dose', 'Dose', 'box',
         x=6, y=6, w=168, d=108, z=0, h=55, r=12, mass=58,
         info='Leicht konische Schale, damit man mehrere Dosen ineinanderstapeln kann. Essensreste auskratzen, '
              'Ausspülen ist für die Gelbe Tonne nicht nötig.',
         color=DOSE, opacity=0.85, wand=2, marks=[mark('box', 6, 6, 156, 96, 9, '#D8E0E3', zeichnung=True)]),
]
explodiere(teile, abstand=16, nach_liste=True, gruppen=[['rand', 'schale']])
assert teile[0]['explode'][2] == DZ, teile[0]['explode']
skaliere_masse(teile, oid='food_container')
schreibe('food_container', teile)
