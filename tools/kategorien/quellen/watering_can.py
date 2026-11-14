"""3D-Modell: watering_can. Erzeugt tools/kategorien/modelle/watering_can.json.

Typische 10-l-Gießkanne aus HDPE (450 × 150 × 300 mm): geblasener Kanister mit Bügelgriff, Einfüllöffnung und
schräg ansteigendem Ausgussrohr (Stapel dünner Scheiben, in der Foto-Ansicht ein glattes Rohr), oben eine aufgesteckte Brause mit
Lochplatte. Kanne, Griff und Rohr sind ein Stück und bleiben stehen; die Brause wird seitlich abgezogen.
Der Griff ist ein Bügel aus Griffstange und zwei Stegen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

KANNE = '#3F8F5A'
DUNKEL = '#347A4C'
N_ROHR = 18
ROHR_INFO = 'Das Ausgussrohr ist mit der Kanne aus einem Stück geblasen.'

teile = [
    teil('lochplatte', 'watering_rose', 'Lochplatte der Brause', 'Lochplatte', 'cyl',
         x=375, y=40, w=70, z=270, h=3, explode=[90, 0, 70], mass=8,
         info='Gelochte Platte, die das Wasser in feine Strahlen teilt. Verstopfte Löcher mit einer Nadel '
              'freimachen statt die Brause wegzuwerfen.',
         color='#2F6DB5', marks=[mark('cyl', 3, 3, 64, fill='#285E9C')]
         + raster(13, 13, 6, 6, 3, 3, 8, shape='cyl', fill='#173B66')),
    teil('brause', 'watering_rose', 'Brausekopf', 'Brause', 'cyl',
         x=375, y=40, w=70, z=248, h=22, explode=[90, 0, 20], mass=25,
         info='Aufgesteckter Kopf aus PP. Vor dem Entsorgen vom Rohr abziehen: Er ist oft aus anderem '
              'Kunststoff und nützlich als Ersatzteil.',
         color='#2F6DB5', marks=[mark('cyl', 22, 22, 26, fill='#285E9C')]),
    teil('griff', 'watering_can_body', 'Bügelgriff', 'Griff', 'box',
         x=20, y=60, w=130, d=30, z=275, h=25, r=12, mass=40, form='liegend_x',
         info='Hohl geblasener Griff, zum Tragen der vollen Kanne. Er ist mit der Kanne aus einem Stück.',
         color=KANNE, marks=[mark('box', 30, 8, 70, 14, 6, DUNKEL, zeichnung=True)]),
    teil('steg_hinten', 'watering_can_body', 'Griffsteg', 'Griffsteg', 'box',
         x=20, y=60, w=25, d=30, z=242, h=33, r=10, mass=8, label=False,
         info='Hinterer Steg des Griffs, hier hält man die Kanne zum Kippen.', color=KANNE),
    teil('steg_vorn', 'watering_can_body', 'Griffsteg', 'Griffsteg', 'box',
         x=125, y=60, w=25, d=30, z=242, h=33, r=10, mass=8, label=False,
         info='Vorderer Steg des Griffs neben der Einfüllöffnung.', color=KANNE),
    teil('einfuellung', 'watering_can_body', 'Einfüllöffnung', 'Einfüllöffnung', 'cyl',
         x=152, y=40, w=80, d=70, z=242, h=12, mass=15,
         info='Breite Öffnung zum Füllen am Wasserhahn oder in der Regentonne.',
         color=KANNE, marks=[mark('cyl', 6, 6, 68, 58, fill='#1F3B2A')]),
    # Ausgussrohr als schräger Stapel dünner Scheiben: in der Foto-Ansicht wird daraus ein glattes Rohr
    *[teil(f'rohr_{i}', 'watering_can_body', 'Ausgussrohr', 'Ausgussrohr', 'box',
           x=round(240 + i * 150 / (N_ROHR - 1), 2), y=57, w=40, d=36, z=round(20 + i * 228 / N_ROHR, 3),
           h=round(228 / N_ROHR, 3), r=14, mass=round(96 / N_ROHR, 2), info=ROHR_INFO, color=KANNE,
           label=i == N_ROHR - 1,
           marks=[mark('box', 6, 6, 28, 24, 10, DUNKEL, zeichnung=True)] if i == N_ROHR - 1 else None)
      for i in range(N_ROHR - 1, -1, -1)],
    teil('kanne', 'watering_can_body', 'Kannenkörper', 'Kanne', 'box',
         x=0, y=0, w=240, d=150, z=0, h=242, r=35, mass=430,
         info='Blasgeformtes HDPE, Recyclingcode 2. Keine Verpackung, also nicht in die Gelbe Tonne: kaputte '
              'Kannen zum Wertstoffhof. Risse lassen sich oft verschweißen.',
         color=KANNE, marks=[mark('box', 8, 8, 224, 134, 30, DUNKEL)]),
]
for p in teile:
    if p['explode'] is None:
        p['explode'] = [0, 0, 0]
skaliere_masse(teile, oid='watering_can')
schreibe('watering_can', teile)
