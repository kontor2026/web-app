"""3D-Modell: paint_brush. Erzeugt tools/kategorien/modelle/paint_brush.json.

Flachpinsel 45 mm (2"), flach auf dem Tisch: Stiel hinten (y 0), Borsten vorn. Lackierter Buchenholzstiel, Zwinge aus
verzinntem Stahlblech mit zwei Nägeln am Stiel befestigt, Kunstborsten in Epoxidharz mit einer Einlage (Keil) eingeklebt.
Explodiert entlang der Achse: Stiel nach hinten, Borstenpaket mit Klebepfropfen nach vorn, Einlage und Nägel darüber.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

HOLZ = '#B5683A'
BLECH = '#C4CACE'
BORSTE = '#3B3530'

teile = [
    teil('naegel', 'steel_ferrule', 'Zwingennägel', 'Nägel', 'box',
         x=17, y=150, w=11, d=3, z=13.6, h=1.6, r=0.5, explode=[0, 0, 22], mass=0.4,
         info='Zwei kleine Nägel halten die Zwinge am Stiel. Mit einer Zange herausziehen.',
         color='#7D858B', marks=[mark('cyl', 0, 0, 3, fill='#5A6268'), mark('cyl', 8, 0, 3, fill='#5A6268')]),
    teil('zwinge', 'steel_ferrule', 'Zwinge', 'Zwinge', 'box',
         x=0, y=146, w=45, d=36, z=0, h=15, r=5, explode=[0, 0, 0], mass=8,
         material_id='steel', materials=[['stahl', 97], ['lot', 3]],
         info='Verzinntes Stahlblech, um Stiel und Borsten gequetscht. Zum Trennen mit einer Zange aufbiegen; '
              'die Zwinge gehört zum Altmetall.',
         color=BLECH, marks=raster(3, 8, 1, 3, 39, 1.2, 0, 8, r=0.5, fill='#A9B0B5')),
    teil('einlage', 'synthetic_bristles', 'Einlage (Keil)', 'Einlage', 'box',
         material_id='wood', x=6, y=158, w=33, d=20, z=6.5, h=2, r=1, explode=[0, 48, 18], mass=1,
         materials=[['holz', 100]],
         info='Dünnes Holzplättchen mitten im Borstenpaket. Es spreizt die Borsten und macht den Pinsel dicker.',
         color='#C9A27A'),
    teil('klebepfropfen', 'synthetic_bristles', 'Klebepfropfen (Epoxid)', 'Klebepfropfen', 'box',
         material_id='polyester', x=2, y=156, w=41, d=24, z=1.5, h=12, r=3, explode=[0, 48, 0], mass=4,
         materials=[['klebstoff', 60], ['polyester', 40]],
         info='Harter Kleber hält die Borstenenden in der Zwinge fest. Er lässt sich nicht von den Borsten lösen.',
         color='#8F7A52', marks=[mark('box', 1, 2, 39, 20, 2, '#A68E62')]),
    teil('borsten', 'synthetic_bristles', 'Kunstborsten', 'Borsten', 'box',
         x=1, y=180, w=43, d=50, z=1.5, h=12, r=2, explode=[0, 80, 0], mass=9,
         info='Feine Polyesterfasern mit gespaltenen Spitzen. Pinsel auswaschen und wiederverwenden; '
              'mit eingetrockneter Farbe gehört er in den Restmüll, nie Farbreste in den Ausguss.',
         color=BORSTE, marks=raster(2, 2, 10, 1, 2, 46, 4.2, r=1, fill='#4E4740')),
    teil('stiel', 'wooden_handle', 'Holzstiel', 'Stiel', 'box',
         x=10, y=0, w=25, d=160, z=1.5, h=12, r=6, explode=[0, -40, 0], mass=18,
         info='Buchenholz, farbig lackiert, mit Loch zum Aufhängen. Nach dem Abtrennen der Zwinge kann das Holz '
              'wiederverwendet werden.',
         color=HOLZ, marks=[mark('cyl', 9, 10, 7, fill='#5A3A22'), mark('box', 3, 30, 19, 110, 6, '#C27646')]),
]

skaliere_masse(teile, oid='paint_brush')
schreibe('paint_brush', teile)
