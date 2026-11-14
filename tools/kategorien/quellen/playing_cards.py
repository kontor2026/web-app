"""3D-Modell: playing_cards. Erzeugt tools/kategorien/modelle/playing_cards.json.

Kartenspiel (55 Karten, 58 × 88 mm) in einer Faltschachtel 60 × 90 × 20 mm mit Einstecklasche, liegend.
Die Schachtel ist in Deckellasche und Schachtelkörper geteilt, das Kartenpaket in die oberste Karte und den Stapel.
Explosion: Folie, Lasche, oberste Karte und Stapel schweben über der Schachtel (Reihenfolge nach Liste).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

PAPPE = '#2F5E9E'
KARTE = '#F6F3EC'
ROT = '#C8423A'

teile = [
    teil('folie', 'cardboard_box_body', 'Cellophanfolie', 'Folie', 'box', material_id='pp',
         x=0, y=0, w=60, d=90, z=20, h=0.05, r=1, mass=1, materials=[['pp', 100]], color='#E4ECF0', opacity=0.35,
         info='Dünne Kunststofffolie mit Aufreißfaden um neue Spiele. Abziehen und in die Gelbe Tonne geben.',
         marks=[mark('box', 0, 70, 60, 2, 0, ROT)]),
    teil('lasche', 'cardboard_box_body', 'Deckellasche', 'Lasche', 'box',
         x=0, y=72, w=60, d=18, z=19.5, h=0.5, r=1, mass=2, materials=[['papier', 92], ['druck', 8]], color=PAPPE,
         info='Klappe mit Einstecklasche, verschließt die Schachtel oben. Sie ist an der Rückwand angeknickt.',
         marks=[mark('box', 10, 4, 40, 10, 5, '#244B80')]),
    teil('karte_oben', 'coated_cards', 'Oberste Karte (Herz-Ass)', 'Karte', 'box',
         x=1, y=1, w=58, d=88, z=18.7, h=0.3, r=3, mass=1.8, color=KARTE,
         info='Karton, beidseitig bedruckt und mit Kunststoff beschichtet, damit die Karten gleiten und nicht knicken. '
              'Wegen der Beschichtung gehören alte Karten in den Restmüll.',
         marks=[mark('box', 4, 4, 6, 8, 1, ROT), mark('cyl', 20, 32, 18, 18, fill=ROT), mark('box', 48, 76, 6, 8, 1, ROT)]),
    teil('stapel', 'coated_cards', 'Kartenstapel (54 Karten)', 'Kartenstapel', 'box',
         x=1, y=1, w=58, d=88, z=2.5, h=16.2, r=3, mass=97, color='#E9E4D8',
         info='Gleiche beschichtete Karten, zusammen gut 16 mm hoch. Vollständige Spiele lieber weitergeben, '
              'einzelne Karten taugen zum Basteln.',
         marks=[mark('box', 3, 3, 52, 82, 2, '#3E6FA8')] + raster(8, 8, 4, 7, 6, 6, 12, 11.5, 'cyl', fill='#F6F3EC')),
    teil('schachtel', 'cardboard_box_body', 'Schachtel', 'Schachtel', 'box',
         x=0, y=0, w=60, d=90, z=0, h=19.5, r=1, mass=10, materials=[['papier', 92], ['druck', 8]], color=PAPPE,
         info='Faltschachtel aus dünnem bedrucktem Karton, an einer Lasche verklebt. Leer flach drücken und ins Altpapier.',
         marks=[mark('box', 1, 1, 58, 88, 1, '#1E3B66'), mark('box', 20, 2, 20, 8, 4, '#244B80')]),
]

explodiere(teile, abstand=40, abstaende={'folie': 30}, nach_liste=True)
skaliere_masse(teile, oid='playing_cards')
schreibe('playing_cards', teile)
