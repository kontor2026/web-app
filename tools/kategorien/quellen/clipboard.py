"""3D-Modell: clipboard. Erzeugt tools/kategorien/modelle/clipboard.json.

Klemmbrett A4 aus 3-mm-Hartfaserplatte (230 × 320 mm), Klemme hinten oben (y = 0): Grundplatte aus Stahlblech,
mit zwei Nieten durch die Platte befestigt, darauf der Klemmhebel mit Aufhängeloch und darunter die Spiralfeder.
Explodiert: Teile der Klemme nach oben über der Platte, die Nieten knapp darunter.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

STAHL = '#B5BCC2'
teile = [
    teil('hebel', 'steel_clip', 'Klemmhebel', 'Klemmhebel', 'box',
         x=65, y=4, w=100, d=52, z=6, h=9, r=6, mass=45, color='#C3C9CE',
         info='Vernickeltes Stahlblech. Drückt man hinten, öffnet sich die Klemme vorne. '
              'Das Loch dient zum Aufhängen.',
         marks=[mark('cyl', 44, 6, 12, 8, fill='#5A6268'), mark('box', 4, 38, 92, 10, 4, '#D3D8DC'),
                mark('box', 10, 24, 80, 2, 0, '#9AA2A6')]),
    teil('feder', 'steel_clip', 'Spiralfeder', 'Feder', 'box',
         x=95, y=14, w=40, d=12, z=4.5, h=6, r=5, mass=6, color='#8A9298',
         info='Drückt die Klemme zu. Steht unter Spannung, beim Aufbiegen kann sie wegspringen.',
         marks=raster(2, 1, 10, 1, 1.2, 10, 4, fill='#5A6268')),
    teil('grundplatte', 'steel_clip', 'Grundplatte', 'Grundplatte', 'box',
         x=70, y=6, w=90, d=28, z=3, h=1.5, r=3, mass=20, color=STAHL,
         info='Trägt das Gelenk des Hebels und ist mit der Platte vernietet.',
         marks=[mark('cyl', 7, 11, 6, fill='#8A9298'), mark('cyl', 77, 11, 6, fill='#8A9298')]),
    teil('niete_links', 'steel_clip', 'Niete', 'Nieten', 'cyl',
         x=77.5, y=17.5, w=5, z=0, h=4.8, mass=1, material_id='steel', color='#9AA2A6',
         info='Zwei Hohlnieten halten die Klemme. Zum Trennen mit einem 5-mm-Bohrer den Kopf abbohren.'),
    teil('niete_rechts', 'steel_clip', 'Niete', 'Niete rechts', 'cyl',
         x=147.5, y=17.5, w=5, z=0, h=4.8, mass=1, color='#9AA2A6', label=False,
         info='Zweite Niete.'),
    teil('platte', 'hardboard_panel', 'Hartfaserplatte', 'Platte', 'box',
         x=0, y=0, w=230, d=320, z=0, h=3, r=8, mass=210, color='#8B5E3C',
         info='Gepresste Holzfasern mit glatter Oberfläche. Ohne Klemme gehört sie zum Altholz im Wertstoffhof.',
         marks=[mark('cyl', 75, 15, 10, fill='#6E4A2F'), mark('cyl', 145, 15, 10, fill='#6E4A2F'),
                mark('box', 4, 4, 222, 312, 6, '#94664A')]),
]
for p in teile:
    if p['id'] == 'platte':
        p['explode'] = [0, 0, 0]
explodiere(teile, abstand=28, gruppen=[['niete_links', 'niete_rechts']], abstaende={'hebel': 55})
skaliere_masse(teile, oid='clipboard')
schreibe('clipboard', teile)
