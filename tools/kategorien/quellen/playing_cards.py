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
# Herz in der Kartenmitte: zwei Kreise oben, darunter Stufen, die zur Spitze schmaler werden
HERZ = [mark('cyl', 18, 32, 12, 12, fill=ROT), mark('cyl', 28, 32, 12, 12, fill=ROT)] + [
    mark('box', 19 + i * 2, 38 + i * 3, 20 - i * 4, 3.2, 1, ROT) for i in range(5)]

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
         marks=[mark('box', 3, 3, 4, 7, 1, ROT), mark('cyl', 3, 11, 4, fill=ROT),
                mark('box', 51, 78, 4, 7, 1, ROT), mark('cyl', 51, 74, 4, fill=ROT)] + HERZ),
    teil('stapel', 'coated_cards', 'Kartenstapel (54 Karten)', 'Kartenstapel', 'box',
         x=1, y=1, w=58, d=88, z=2.5, h=16.2, r=3, mass=97, color='#E9E4D8',
         info='Gleiche beschichtete Karten, zusammen gut 16 mm hoch. Vollständige Spiele lieber weitergeben, '
              'einzelne Karten taugen zum Basteln.',
         marks=[mark('box', 3, 3, 52, 82, 2, '#3E6FA8')] + raster(8, 8, 4, 7, 6, 6, 12, 11.5, 'cyl', fill='#F6F3EC')),
    teil('schachtel', 'cardboard_box_body', 'Schachtel', 'Schachtel', 'box',
         x=0, y=0, w=60, d=90, z=0, h=19.5, r=1, mass=10, materials=[['papier', 92], ['druck', 8]], color=PAPPE,
         info='Faltschachtel aus dünnem bedrucktem Karton, an einer Lasche verklebt. Leer flach drücken und ins Altpapier.',
         marks=[mark('box', 3, 3, 54, 66, 2, '#F2EEE4'), mark('box', 5, 5, 50, 62, 1.5, PAPPE),
                mark('cyl', 15, 14, 30, 30, fill='#F2EEE4'), mark('cyl', 18, 17, 24, 24, fill=ROT),
                mark('box', 10, 50, 40, 5, 1, '#F2EEE4'), mark('box', 16, 58, 28, 3, 1, '#C9D4E4'),
                mark('box', 20, 2, 20, 6, 3, '#244B80')]),
]

explodiere(teile, abstand=40, abstaende={'folie': 30}, nach_liste=True)
skaliere_masse(teile, oid='playing_cards')
schreibe('playing_cards', teile)
