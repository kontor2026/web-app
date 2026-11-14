"""3D-Modell: flip_flops. Erzeugt tools/kategorien/modelle/flip_flops.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Ein Flip-Flop (Größe ca. 42), Ferse hinten (y = 0), Zehen vorne (y = 260). 100 × 260 × 25 mm.
# Der Y-Riemen ist aus Zehensteg und je drei Armstücken pro Seite treppenförmig angenähert; seine Enden stecken als
# Pfropfen in Löchern der Sohle. Explodiert hebt sich der Riemen als Ganzes ab, die zwei Sohlenschichten trennen sich.
RIEMEN = '#2D6FA3'
DUNKEL = '#245A85'
RIEMEN_M = [['gummi', 100]]

# Riemenarme: je Seite fünf Stücke vom Steg (vorne Mitte) schräg nach hinten außen, auf dem Fußbett liegend. Die Stücke
# stoßen in y lückenlos aneinander und überlappen sich in x, so wirkt der Riemen wie ein durchgehendes Band; in der
# Foto-Ansicht werden sie weich gerundet.
N_ARM = 5
arme = []
for seite, sx in (('l', -1), ('r', 1)):
    for k in range(N_ARM):
        erst = seite == 'l' and k == 0
        cx, w, d, h = 50 + sx * (7 + 7.5 * k), 14, 18, 7
        arme.append(teil(
            f'arm_{seite}{k + 1}', 'rubber_strap',
            'Y-Riemen (Gummi)' if erst else f'Riemen {seite} {k + 1}', 'Riemen', 'box',
            x=round(cx - w / 2, 1), y=176 - d * (k + 1), w=w, d=d, z=18 - 0.75 * k, h=h, r=5, mass=1.2,
            materials=RIEMEN_M, color=RIEMEN,
            label=None if erst else False,
            info='Weicher Gummi- oder PVC-Riemen, mit dem Steg in einem Stück gespritzt. Die hinteren Enden stecken '
                 'als Pfropfen in der Sohle und lassen sich von unten durchdrücken.' if erst
            else 'Weiteres Stück des Y-Riemens.',
            marks=[mark('box', 3, 3, w - 6, d - 6, 4, DUNKEL, zeichnung=True)]))
teile = [
    teil('steg', 'rubber_strap', 'Zehensteg mit Pfropfen', 'Zehensteg', 'cyl',
         x=44, y=176, w=12, d=14, z=0, h=25, mass=4, materials=RIEMEN_M, color=RIEMEN,
         info='Der Steg zwischen großem und zweitem Zeh. Sein verdickter Pfropfen steckt von oben durch die Sohle: '
              'von unten durchdrücken, dann ist der Riemen ab.',
         marks=[mark('cyl', 3, 3, 6, 8, fill='#1C4566')]),
] + arme + [
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
           gruppen=[['steg'] + [p['id'] for p in arme]])
skaliere_masse(teile, oid='flip_flops')
schreibe('flip_flops', teile)
