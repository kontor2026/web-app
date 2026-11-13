"""3D-Modell: kitchen_knife. Erzeugt tools/kategorien/modelle/kitchen_knife.json.

Typisches Küchen-/Allzweckmesser flach auf dem Tisch, Spitze hinten (y = 0), Griff vorne. Klinge 20 cm aus
Edelstahl mit Kropf und durchgehender Angel (Erl), Kunststoffgriff angespritzt. Explodiert: Griff zur Seite,
Kropf und Angel nach vorne von der Klinge abgerückt.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

STAHL = '#C3C9CE'
SCHNEIDE = '#E3E7EA'

teile = [
    teil('spitze', 'knife_blade', 'Klingenspitze', 'Spitze', 'box',
         x=9, y=0, w=16, d=24, z=9, h=2, r=8, mass=6, label=False,
         info='Die Schneide läuft hier zum Klingenrücken hoch und endet in der Spitze.',
         color=STAHL, marks=[mark('box', 0, 8, 2, 16, 1, SCHNEIDE)]),
    teil('klinge', 'knife_blade', 'Klinge', 'Klinge', 'box',
         x=0, y=24, w=25, d=172, z=9, h=2, r=3, mass=75,
         info='Rostfreier Messerstahl, an einer Kante scharf geschliffen. Vor dem Wegwerfen in dicke Pappe wickeln '
              'und festkleben, dann als Metallschrott zum Wertstoffhof.',
         color=STAHL, marks=[mark('box', 0, 0, 2.5, 172, 1, SCHNEIDE), mark('box', 8, 140, 12, 20, 2, '#B2B8BD')]),
    teil('kropf', 'knife_blade', 'Kropf', 'Kropf', 'box',
         x=0, y=196, w=25, d=10, z=5, h=10, r=3, explode=[0, 12, 0], mass=15,
         info='Verdickung zwischen Klinge und Griff. Sie schützt die Finger davor, auf die Schneide zu rutschen.',
         color='#B2B8BD'),
    teil('angel', 'knife_blade', 'Angel (Erl)', 'Angel', 'box',
         x=7, y=206, w=11, d=106, z=9, h=2.5, r=2, explode=[0, 26, 0], mass=20,
         info='Verlängerung der Klinge, die im Griff steckt. Durchgehende Angeln halten länger.',
         color=STAHL, marks=[mark('cyl', 3, 30, 5, fill='#8E959B'), mark('cyl', 3, 75, 5, fill='#8E959B')]),
    teil('griff', 'knife_handle', 'Kunststoffgriff', 'Griff', 'box',
         x=1, y=204, w=23, d=116, z=0, h=20, r=9, explode=[45, 0, 0], mass=32,
         info='Polypropylen, direkt um die Angel gespritzt. Abtrennen nur mit einer Säge, sonst das ganze Messer zum '
              'Wertstoffhof bringen.',
         color='#2E3338', marks=[mark('box', 4, 10, 15, 96, 6, '#3E444A')]),
]
explodiere(teile, abstand=12, fest=('spitze', 'klinge'))
skaliere_masse(teile, oid='kitchen_knife')
schreibe('kitchen_knife', teile)
