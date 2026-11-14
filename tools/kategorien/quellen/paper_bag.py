"""3D-Modell: paper_bag. Erzeugt tools/kategorien/modelle/paper_bag.json.

Typische Papier-Tragetasche (26 × 14 × 27 cm Korpus, Kraftpapier ca. 90 g/m², Kordelgriffe aus gedrehtem Papier,
Kreuzboden mit Karton-Einlage), aufgestellt. Die Wände werden zu allen Seiten weggezogen, die Griffe mit ihren
Wänden nach außen und etwas nach oben, die Bodeneinlage hebt nach oben ab.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

KRAFT = '#B8946A'
DUNKEL = '#A8865F'
WAND = [['papier', 97], ['druck', 2], ['klebstoff', 1]]
GRIFF = [['papier', 96], ['klebstoff', 4]]
H = 270  # Korpushöhe, darüber die Griffe bis 320 mm
AUS = 120  # Wände nach außen


def griff(seite, y, dy, mit_label):
    """Kordelgriff als Schlaufe: zwei Schenkel innen an der Wand und der Bogen darüber."""
    ex = [0, dy * 0.45, 70]
    farbe = '#B88C5A'
    info = ('Gedrehte Papierkordel, innen mit einem Pappstreifen angeklebt. Ist der Kleber aus Kunststoff, '
            'Griffe abreißen, der Rest darf ins Altpapier.') if mit_label else 'Zweiter Griff, genauso eingeklebt.'
    return [
        teil(f'griff_{seite}', 'paper_bag_body', f'Kordelgriff {seite}', 'Griff', 'box',
             x=85, y=y, w=90, d=4, z=H + 42, h=6, r=2, form='liegend_x', explode=ex, mass=1.2, materials=GRIFF, color=farbe,
             label=None if mit_label else False, info=info),
        teil(f'griff_{seite}_l', 'paper_bag_body', 'Kordel, Schenkel', 'Kordel', 'cyl',
             x=85, y=y, w=5, d=4, z=H - 2, h=44, explode=ex, mass=0.65, materials=GRIFF, color=farbe, label=False,
             info='Linkes Ende der Kordel, unter dem Pappstreifen festgeklebt.'),
        teil(f'griff_{seite}_r', 'paper_bag_body', 'Kordel, Schenkel', 'Kordel', 'cyl',
             x=170, y=y, w=5, d=4, z=H - 2, h=44, explode=ex, mass=0.65, materials=GRIFF, color=farbe, label=False,
             info='Rechtes Ende der Kordel, unter dem Pappstreifen festgeklebt.'),
    ]


teile = [
    *griff('vorne', 135, AUS, True),
    *griff('hinten', 2, -AUS, False),
    teil('verstaerkung_vorne', 'paper_bag_body', 'Griffverstärkung vorne', 'Verstärkung', 'box',
         x=70, y=137, w=120, d=2, z=H - 40, h=40, r=0, explode=[0, AUS * 0.45, 0], mass=1.5, materials=GRIFF, color=DUNKEL,
         info='Pappstreifen innen am Rand, an den die Griffenden geklebt sind. Er verteilt das Gewicht, '
              'damit die Tasche nicht einreißt.'),
    teil('verstaerkung_hinten', 'paper_bag_body', 'Griffverstärkung hinten', 'Verstärkung', 'box',
         x=70, y=1, w=120, d=2, z=H - 40, h=40, r=0, explode=[0, -AUS * 0.45, 0], mass=1.5, materials=GRIFF, color=DUNKEL,
         label=False, info='Gegenstück an der Rückwand.'),
    teil('wand_vorne', 'paper_bag_body', 'Vorderwand', 'Vorderwand', 'box',
         x=0, y=139, w=260, d=1, z=0, h=H, r=0, explode=[0, AUS, 0], mass=7.5, materials=WAND, color=KRAFT,
         info='Kraftpapier aus langen Holzfasern, oft mit hohem Altpapieranteil. Am oberen Rand nach innen '
              'umgeschlagen, damit die Kante stabil ist.'),
    teil('wand_hinten', 'paper_bag_body', 'Rückwand mit Längsnaht', 'Rückwand', 'box',
         x=0, y=0, w=260, d=1, z=0, h=H, r=0, explode=[0, -AUS, 0], mass=7.8, materials=WAND, color=KRAFT,
         info='Die ganze Tasche ist aus einem Papierschlauch gefaltet. Seine Längsnaht ist hinten verklebt.'),
    teil('seite_links', 'paper_bag_body', 'Seitenfalte links', 'Seitenfalte', 'box',
         x=0, y=1, w=1, d=138, z=0, h=H, r=0, explode=[-AUS, 0, 0], mass=3.6, materials=WAND, color=DUNKEL,
         info='Seitenwand mit Mittelknick. Leer faltet sie sich nach innen, so liegt die Tasche flach.'),
    teil('seite_rechts', 'paper_bag_body', 'Seitenfalte rechts', 'Seitenfalte', 'box',
         x=259, y=1, w=1, d=138, z=0, h=H, r=0, explode=[AUS, 0, 0], mass=3.6, materials=WAND, color=DUNKEL,
         label=False, info='Gegenstück zur linken Seitenfalte.'),
    teil('bodeneinlage', 'paper_bag_body', 'Bodeneinlage (Karton)', 'Bodeneinlage', 'box',
         x=3, y=3, w=254, d=134, z=2, h=1, r=1, explode=[0, 0, 120], mass=10, material_id='cardboard',
         materials=[['papier', 100]], color='#B08A5E',
         info='Loser Kartonzuschnitt, der den Boden steif macht. Darf mit der Tasche ins Altpapier.',
         marks=[mark('box', 0, 64, 254, 6, 0, '#9E7A52')]),
    teil('boden', 'paper_bag_body', 'Kreuzboden', 'Boden', 'box',
         x=1, y=1, w=258, d=138, z=0, h=2, r=0, explode=[0, 0, 0], mass=8, materials=[['papier', 95], ['klebstoff', 5]],
         color=KRAFT,
         info='Das Schlauchende ist zu einem rechteckigen Boden gefaltet und verklebt. Er trägt das ganze Gewicht.',
         marks=[mark('box', 0, 0, 258, 34, 0, DUNKEL), mark('box', 0, 104, 258, 34, 0, DUNKEL),
                mark('box', 0, 64, 258, 10, 0, '#B48E5C')]),
]
skaliere_masse(teile, oid='paper_bag')
schreibe('paper_bag', teile)
