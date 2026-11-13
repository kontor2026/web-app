"""3D-Modell: shampoo_bottle. Erzeugt tools/kategorien/modelle/shampoo_bottle.json.

Typische 250-ml-Shampooflasche, stehend, ovaler Querschnitt 70 × 45 mm: HDPE-Körper aus Boden, Rumpf, Schulter
und Hals mit Gewinde, PP-Klappdeckel (Unterteil mit Ausgießer, Klappe mit Filmscharnier), PP-Folienetiketten
vorne und hinten. Deckelteile stapeln über dem Hals, Etiketten werden seitlich abgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

FLASCHE = '#F2EFEA'
DECKEL = '#3E7CB1'
teile = [
    teil('klappe', 'pp_flip_cap', 'Deckelklappe', 'Klappe', 'cyl',
         x=14, y=7.5, w=42, d=30, z=180, h=10, mass=2.2,
         info='Obere Klappe, über ein dünnes Filmscharnier mit dem Unterteil verbunden. Darauf steht die Flasche '
              'oft kopfüber, damit der Rest nach unten läuft.',
         color=DECKEL, marks=[mark('box', 15, 0, 12, 4, 2, '#2E6390'), mark('cyl', 6, 5, 30, 20, fill='#4A8AC0')]),
    teil('deckel_unterteil', 'pp_flip_cap', 'Deckel-Unterteil mit Ausgießer', 'Deckelunterteil', 'cyl',
         x=14, y=7.5, w=42, d=30, z=162, h=18, mass=4.0,
         info='Wird auf den Hals geschraubt. Zum Entsorgen darf der Deckel draufbleiben: '
              'Die Sortieranlage trennt PP und HDPE später im Wasserbad.',
         color=DECKEL, marks=[mark('cyl', 16, 10, 10, fill='#2E6390'), mark('cyl', 19, 13, 4, fill='#1F2A33')]),
    teil('hals', 'hdpe_bottle_body', 'Flaschenhals mit Gewinde', 'Hals', 'cyl',
         x=24, y=11.5, w=22, z=150, h=16, mass=2.5,
         info='Dickwandiger Hals mit Gewinde. Hier sitzt nach dem Ausspülen oft noch etwas Shampoo.',
         color=FLASCHE, marks=[mark('cyl', 4, 4, 14, fill='#D6D2CA')]),
    teil('schulter', 'hdpe_bottle_body', 'Flaschenschulter', 'Schulter', 'cyl',
         x=5, y=3, w=60, d=39, z=138, h=12, mass=3.0,
         info='Die Flasche wird aus einem Schlauch in einer Form aufgeblasen (Extrusionsblasformen).',
         color=FLASCHE),
    teil('rumpf', 'hdpe_bottle_body', 'Flaschenrumpf', 'Rumpf', 'cyl',
         x=0, y=0, w=70, d=45, z=8, h=130, mass=14.5,
         info='HDPE, Recyclingcode 2. Leer drücken reicht, dann mit Deckel in die Gelbe Tonne. HDPE wird gut '
              'recycelt, zum Beispiel zu neuen Flaschen oder Rohren.',
         color=FLASCHE),
    teil('boden', 'hdpe_bottle_body', 'Flaschenboden mit Quetschnaht', 'Boden', 'cyl',
         x=3, y=2, w=64, d=41, z=0, h=8, mass=4.0,
         info='Am Boden sieht man die Quetschnaht vom Blasformen und das Recyclingzeichen 2.',
         color=FLASCHE),
    teil('etikett_vorne', 'plastic_label', 'Etikett vorne', 'Etikett', 'box',
         x=70, y=8, w=0.3, d=29, z=25, h=100, r=0, explode=[50, 0, 0], mass=1.0, materials=[['pp', 95], ['druck', 5]],
         info='Selbstklebende PP-Folie. Sie muss nicht abgezogen werden, weil sie zum Deckel-Kunststoff passt.',
         color='#3E7CB1', sortBias=100),
    teil('etikett_hinten', 'plastic_label', 'Etikett hinten', 'Etikett', 'box',
         x=-0.3, y=8, w=0.3, d=29, z=25, h=90, r=0, explode=[-50, 0, 0], mass=0.8,
         materials=[['pp', 95], ['druck', 5]], label=False,
         info='Rückseite mit Inhaltsstoffen und Gebrauchsanweisung.',
         color='#E8EEF4'),
]
explodiere(teile, abstand=22, fest=('rumpf', 'boden', 'schulter', 'hals'), gruppen=[['klappe', 'deckel_unterteil']])
skaliere_masse(teile, oid='shampoo_bottle')
schreibe('shampoo_bottle', teile)
