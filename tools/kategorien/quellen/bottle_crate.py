"""3D-Modell: bottle_crate. Erzeugt tools/kategorien/modelle/bottle_crate.json.

Typischer Mehrweg-Getränkekasten für 20 × 0,5 l (40 × 30 × 30 cm) aus HDPE, ein einziges Spritzgussteil.
Zur Erklärung zerlegt: offener Rahmen aus vier Wänden mit Oberrand und Griffmulden an den Schmalseiten,
Gefache mit 5 × 4 Zellen, Boden mit Ablauflöchern und Stapelfuß, dazu das In-Mould-Etikett.
Explodiert hebt der Rahmen weit nach oben ab, das Gefache schwebt knapp über dem Boden.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

KASTEN = '#2F6E3B'
DUNKEL = '#1F4A27'
LOCH = '#163A1E'
RAHMEN = 370
HINTEN = -400  # hintere Wände zuerst zeichnen, sonst verdecken sie das Gefache  # Hub des Rahmens
INFO_W = 'Teil des Rahmens. Rippen und Durchbrüche sparen Material und halten den Kasten trotzdem stabil.'


def w(id, name, short, x, y, bw, bd, z, h, mass, info=INFO_W, label=False, **extra):
    return teil(id, 'hdpe_crate_body', name, short, 'box', x=x, y=y, w=bw, d=bd, z=z, h=h, r=2, mass=mass,
                info=info, color=KASTEN, label=label, explode=[0, 0, RAHMEN], **extra)


teile = [
    # Oberrand: vier Leisten
    w('rand_v', 'Oberrand', 'Oberrand', 0, 286, 400, 14, 290, 10, 60, label=True,
      info='Verstärkter, umlaufender Rand. Er trägt beim Stapeln das Gewicht der Kästen darüber.',
      marks=[mark('box', 4, 4, 392, 6, 2, DUNKEL)]),
    w('rand_h', 'Oberrand', 'Oberrand', 0, 0, 400, 14, 290, 10, 60, marks=[mark('box', 4, 4, 392, 6, 2, DUNKEL)], sortBias=HINTEN),
    w('rand_l', 'Oberrand', 'Oberrand', 0, 14, 14, 272, 290, 10, 40, marks=[mark('box', 4, 0, 6, 272, 0, DUNKEL)], sortBias=HINTEN),
    w('rand_r', 'Oberrand', 'Oberrand', 386, 14, 14, 272, 290, 10, 40, marks=[mark('box', 4, 0, 6, 272, 0, DUNKEL)]),
    # Schmalseite rechts mit Griffmulde: Griffleiste, zwei Pfosten, Wand darunter
    w('griff_r', 'Griffleiste', 'Griff', 388, 12, 12, 276, 262, 28, 45, label=True,
      info='Über der Griffmulde liegt eine abgerundete Leiste, an der man den vollen Kasten (rund 17 kg) trägt.'),
    w('pfosten_r1', 'Seitenwand', 'Wand', 388, 12, 12, 83, 215, 47, 20),
    w('pfosten_r2', 'Seitenwand', 'Wand', 388, 205, 12, 83, 215, 47, 20),
    w('wand_r', 'Seitenwand', 'Wand', 388, 12, 12, 276, 12, 203, 120, label=True,
      info='Außenwand. Rippen und Durchbrüche sparen Material und halten den Kasten trotzdem stabil.'),
    # Schmalseite links, genauso
    w('griff_l', 'Griffleiste', 'Griff', 0, 12, 12, 276, 262, 28, 45, sortBias=HINTEN),
    w('pfosten_l1', 'Seitenwand', 'Wand', 0, 12, 12, 83, 215, 47, 20, sortBias=HINTEN),
    w('pfosten_l2', 'Seitenwand', 'Wand', 0, 205, 12, 83, 215, 47, 20, sortBias=HINTEN),
    w('wand_l', 'Seitenwand', 'Wand', 0, 12, 12, 276, 12, 203, 120, sortBias=HINTEN),
    # Längsseiten
    w('wand_v', 'Längswand', 'Längswand', 0, 288, 400, 12, 12, 278, 200,
      info='Lange Außenwand. Abgeschabte Stellen zeigen, wie oft der Kasten schon im Umlauf war.'),
    w('wand_h', 'Längswand', 'Längswand', 0, 0, 400, 12, 12, 278, 200, sortBias=HINTEN),
    teil('etikett', 'hdpe_crate_body', 'In-Mould-Etikett', 'Etikett', 'box',
         material_id='pp', x=120, y=300, w=160, d=0.3, z=110, h=90, r=0, explode=[0, 70, RAHMEN], mass=5,
         materials=[['pp', 95], ['druck', 5]],
         info='Bedrucktes PP-Etikett, beim Spritzgießen eingeschmolzen. Nicht abreißen: Kästen haben Pfand und '
              'werden über Jahre wiederbefüllt.',
         color='#F2F0EA', sortBias=120),
    teil('gefache', 'hdpe_crate_body', 'Gefache', 'Gefache', 'box',
         x=12, y=12, w=376, d=276, z=12, h=170, r=2, mass=430, explode=[0, 0, 30],
         info='Trennstege für 20 Flaschen, damit sie nicht aneinanderschlagen und zerbrechen.',
         color=KASTEN, marks=raster(4, 4, 5, 4, 68, 62, 75, 69, r=8, fill=LOCH)),
    teil('boden', 'hdpe_crate_body', 'Boden mit Ablauflöchern', 'Boden', 'box',
         x=0, y=0, w=400, d=300, z=4, h=8, r=4, mass=200, explode=[0, 0, 0],
         info='Gitterboden, damit Wasser ablaufen kann. Am Ende wird der ganze Kasten gemahlen und zu neuen '
              'Kästen gespritzt.',
         color=KASTEN, marks=raster(18, 18, 9, 6, 22, 22, 42, 46, r=3, fill=LOCH)),
    teil('fuss', 'hdpe_crate_body', 'Stapelfuß', 'Stapelfuß', 'box',
         x=8, y=8, w=384, d=284, z=0, h=4, r=6, mass=40, explode=[0, 0, 0], color=DUNKEL,
         info='Etwas schmaler als der Kasten. Er greift beim Stapeln in den Rand des Kastens darunter, '
              'so rutscht der Stapel nicht.'),
]
skaliere_masse(teile, oid='bottle_crate')
schreibe('bottle_crate', teile)
