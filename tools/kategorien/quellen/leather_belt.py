"""3D-Modell: leather_belt. Erzeugt tools/kategorien/modelle/leather_belt.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Ledergürtel (ca. 110 cm, 35 mm breit) aufgerollt, die Kante steht auf dem Tisch. Rolle Ø 94 mm, 38 mm hoch,
# Foto-Ansicht: die Windungen sind echte Ringe (wand, unten offen), innen bleibt ein Loch von gut 4 cm,
# die Schnalle sitzt außen rechts am Riemenende. Explodiert heben sich die Windungen teleskopartig nach oben ab,
# Schnalle, Dorn, Schraube und Schlaufe werden nach rechts gezogen.
LEDER = '#7A4A2A'
KANTE = '#5C3720'
STAHL = '#B7BCC0'

teile = [
    teil('spitze', 'leather_strap', 'Riemenspitze mit Löchern (innere Windung)', 'Riemenspitze', 'cyl',
         x=16, y=19, w=62, z=0, h=38, wand=10, boden=0, mass=30, materials=[['leder', 100]], color=LEDER,
         info='Das Ende mit den Lochreihen, innen in der Rolle. Rindsleder, pflanzlich oder mit Chromsalzen gegerbt.',
         marks=[mark('cyl', 4, 4, 54, fill=KANTE, zeichnung=True), mark('cyl', 10, 10, 42, fill='#3A2416', zeichnung=True)]),
    teil('windung_mitte', 'leather_strap', 'Riemen, mittlere Windung', 'Riemen', 'cyl',
         x=8, y=11, w=78, z=0, h=38, wand=8, boden=0, mass=40, materials=[['leder', 100]], color=LEDER,
         info='Zwei Lagen Leder, an den Kanten verklebt und vernäht. Tragbare Gürtel in die Altkleidersammlung.',
         marks=[mark('cyl', 4, 4, 70, fill=KANTE, zeichnung=True), mark('cyl', 8, 8, 62, fill=LEDER, zeichnung=True)]),
    teil('windung_aussen', 'leather_strap', 'Riemen, äußere Windung', 'Riemen', 'cyl',
         x=0, y=3, w=94, z=0, h=38, wand=8, boden=0, mass=55, materials=[['leder', 100]], color=LEDER, label=False,
         info='Äußere Windung bis zur Schnalle. Leder lässt sich nicht wie Kunststoff einschmelzen; '
              'Reste werden zu Lederfaserplatten verarbeitet.',
         marks=[mark('cyl', 4, 4, 86, fill=KANTE, zeichnung=True), mark('cyl', 8, 8, 78, fill=LEDER, zeichnung=True)]),
    teil('schlaufe', 'leather_strap', 'Lederschlaufe', 'Schlaufe', 'box',
         x=93, y=78, w=7, d=10, z=0, h=40, r=2, mass=4, materials=[['leder', 100]], color=KANTE, explode=[60, 4, 0],
         info='Kleine Lederschlaufe hinter der Schnalle, sie hält das freie Riemenende fest.'),
    teil('schnalle', 'belt_buckle', 'Gürtelschnalle (Rahmen)', 'Schnalle', 'box',
         x=94, y=26, w=6, d=48, z=0, h=40, r=3, mass=55, materials=[['stahl', 85], ['nickel', 15]], color=STAHL,
         explode=[60, 0, 0],
         info='Vernickelter Stahl- oder Zinkdruckguss-Rahmen. Nach dem Lösen der Schraube ab zum Altmetall.'),
    teil('dorn', 'belt_buckle', 'Dorn', 'Dorn', 'box',
         x=90, y=48, w=10, d=4, z=17, h=4, r=1, mass=4, materials=[['stahl', 85], ['nickel', 15]], color=STAHL,
         explode=[95, 0, 0],
         info='Der Dorn greift in die Löcher der Riemenspitze. Er dreht sich auf der Achse des Rahmens.'),
    teil('schraube', 'belt_buckle', 'Buchschraube', 'Schraube', 'cyl',
         x=86, y=66, w=8, z=16, h=8, mass=3, materials=[['messing', 80], ['stahl', 20]], color='#C9A24A',
         explode=[124, 0, 0],
         info='Zweiteilige Schraube, die den umgeschlagenen Riemen um die Schnallenachse hält. '
              'Mit einer Münze aufdrehen, dann lässt sich die Schnalle abnehmen.',
         marks=[mark('cyl', 2, 2, 4, fill='#8A6D2E')]),
]

explodiere(teile, abstand=22)
skaliere_masse(teile, oid='leather_belt')
schreibe('leather_belt', teile)
