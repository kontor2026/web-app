"""3D-Modell: flip_flops. Erzeugt tools/kategorien/modelle/flip_flops.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Ein Flip-Flop (Größe ca. 42), Ferse hinten (y = 0), Zehen vorne (y = 260). 100 × 260 × 25 mm.
# Der Y-Riemen ist aus Zehensteg und je zwei Armstücken pro Seite treppenförmig angenähert; seine Enden stecken als
# Pfropfen in Löchern der Sohle. Explodiert hebt sich der Riemen als Ganzes ab, die zwei Sohlenschichten trennen sich.
RIEMEN = '#2D6FA3'
DUNKEL = '#245A85'
RIEMEN_M = [['gummi', 100]]

teile = [
    teil('steg', 'rubber_strap', 'Zehensteg mit Pfropfen', 'Zehensteg', 'cyl',
         x=44, y=178, w=12, d=14, z=0, h=25, mass=4, materials=RIEMEN_M, color=DUNKEL,
         info='Der Steg zwischen großem und zweitem Zeh. Sein verdickter Pfropfen steckt von oben durch die Sohle: '
              'von unten durchdrücken, dann ist der Riemen ab.',
         marks=[mark('cyl', 3, 3, 6, 8, fill='#1C4566')]),
    teil('arm_l_vorn', 'rubber_strap', 'Riemen links, vorderer Teil', 'Riemen', 'box',
         x=28, y=148, w=16, d=36, z=15, h=10, r=5, mass=2.5, materials=RIEMEN_M, color=RIEMEN,
         info='Weicher Gummi- oder PVC-Riemen. Er hält den Fuß und ist mit dem Steg in einem Stück gespritzt.',
         marks=[mark('box', 3, 2, 10, 32, 4, DUNKEL)]),
    teil('arm_l_hinten', 'rubber_strap', 'Riemen links mit Pfropfen', 'Riemen', 'box',
         x=10, y=112, w=18, d=36, z=3, h=18, r=6, mass=3.5, materials=RIEMEN_M, color=RIEMEN, label=False,
         info='Das hintere Riemenende endet in einem Pfropfen, der in der Sohle steckt.',
         marks=[mark('box', 4, 2, 10, 32, 4, DUNKEL)]),
    teil('arm_r_vorn', 'rubber_strap', 'Riemen rechts, vorderer Teil', 'Riemen', 'box',
         x=56, y=148, w=16, d=36, z=15, h=10, r=5, mass=2.5, materials=RIEMEN_M, color=RIEMEN, label=False,
         info='Gegenstück zum linken Riemen.', marks=[mark('box', 3, 2, 10, 32, 4, DUNKEL)]),
    teil('arm_r_hinten', 'rubber_strap', 'Riemen rechts mit Pfropfen', 'Riemen', 'box',
         x=72, y=112, w=18, d=36, z=3, h=18, r=6, mass=3.5, materials=RIEMEN_M, color=RIEMEN, label=False,
         info='Gegenstück zum linken Riemenende.', marks=[mark('box', 4, 2, 10, 32, 4, DUNKEL)]),
    teil('fussbett', 'eva_sole', 'Fußbett', 'Fußbett', 'box',
         x=0, y=0, w=100, d=260, z=8, h=7, r=45, mass=35, color='#F2C14E',
         info='Weicher EVA-Schaum mit Rillen für besseren Halt. Mit der Laufsohle verklebt oder in einem Stück geschäumt.',
         marks=[mark('box', 15, 20, 70, 220, 32, '#E6B23F')] + raster(30, 40, 3, 8, 6, 3, 15, 22, r=1, fill='#D9A535')),
    teil('laufsohle', 'eva_sole', 'Laufsohle', 'Laufsohle', 'box',
         x=0, y=0, w=100, d=260, z=0, h=8, r=45, mass=48, color='#3A3F44',
         info='Festerer EVA-Schaum mit Profil. Flip-Flops lassen sich nicht sinnvoll recyceln und gehören in den Restmüll.',
         marks=raster(16, 24, 5, 15, 8, 6, 14, 14, r=2, fill='#2A2E31')),
]

explodiere(teile, abstand=40, nach_liste=True,
           gruppen=[['steg', 'arm_l_vorn', 'arm_l_hinten', 'arm_r_vorn', 'arm_r_hinten']])
skaliere_masse(teile, oid='flip_flops')
schreibe('flip_flops', teile)
