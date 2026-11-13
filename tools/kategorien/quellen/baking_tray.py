"""3D-Modell: baking_tray. Erzeugt tools/kategorien/modelle/baking_tray.json.

Typisches emailliertes Backblech (460 × 380 × 20 mm, 1,3 kg): tiefgezogenes Stahlblech (Boden und vier Wände,
gemeinsam bewegt) mit Rollrand, darin ein eingerollter Versteifungsdraht (vier Stäbe, gemeinsam bewegt), innen und
außen Emaille. Explodiert schweben Draht, Innen-Emaille, Blech und Außen-Emaille übereinander.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

EMAILLE = '#2E3134'
BLECH = '#4F555A'
DRAHT = '#9DA4AA'
B, T, H, WAND = 460, 380, 20, 6

# Versteifungsdraht: vier Stäbe im Rollrand
DRAHT_STAEBE = [('hinten', 1.5, 1.5, B - 3, 3), ('vorne', 1.5, T - 4.5, B - 3, 3),
                ('links', 1.5, 4.5, 3, T - 9), ('rechts', B - 4.5, 4.5, 3, T - 9)]
draht = [teil(f'draht_{n}', 'steel_baking_tray', 'Versteifungsdraht im Rollrand', 'Randdraht', 'box',
              x=x, y=y, w=w, d=d, z=15.5, h=3, r=1.5, mass=w * d, label=n == 'hinten',
              info=('Stahldraht, um den der obere Rand eingerollt ist. Er verhindert, dass sich das Blech in der Hitze '
                    'verzieht.') if n == 'hinten' else 'Weiteres Stück des Randdrahts.',
              color=DRAHT)
         for n, x, y, w, d in DRAHT_STAEBE]

WAENDE = [('hinten', 0, 0, B, WAND), ('vorne', 0, T - WAND, B, WAND),
          ('links', 0, WAND, WAND, T - 2 * WAND), ('rechts', B - WAND, WAND, WAND, T - 2 * WAND)]
waende = [teil(f'wand_{n}', 'steel_baking_tray', 'Rand mit Rollrand', 'Rand', 'box',
               x=x, y=y, w=w, d=d, z=1.3, h=H - 1.3, r=2, mass=w * d * 0.35, label=False,
               info='Hochgezogener Rand des Blechs, oben eingerollt um den Draht.',
               color=BLECH, marks=[mark('box', 1, 1, w - 2, d - 2, 1.5, '#656C72')])
          for n, x, y, w, d in WAENDE]

speckles = [mark('cyl', 20 + (i * 53) % 410, 20 + (i * 37) % 330, 2.5, fill='#6A7076') for i in range(60)]
teile = [
    *draht,
    teil('emaille_innen', 'steel_baking_tray', 'Emaille innen', 'Emaille innen', 'box',
         material_id='special_glass', x=WAND, y=WAND, w=B - 2 * WAND, d=T - 2 * WAND, z=1.3, h=0.3, r=3, mass=45,
         materials=[['emaille', 100]],
         info='Glasartige Schicht, bei 800 °C auf den Stahl geschmolzen. Hart und kratzfest; im Metallwerk '
              'schmilzt sie zu Schlacke. Abgeplatzte Stellen rosten.',
         color=EMAILLE, marks=[mark('box', 8, 8, B - 2 * WAND - 16, T - 2 * WAND - 16, 6, '#363A3E')] + speckles),
    teil('blech', 'steel_baking_tray', 'Stahlblech (Boden)', 'Blech', 'box',
         x=0, y=0, w=B, d=T, z=0.3, h=1, r=6, mass=1000,
         info='Tiefgezogenes Stahlblech, 1 mm dick. Zum Altmetall auf den Wertstoffhof, nicht in die Gelbe Tonne. '
              'Mit Magnet erkennbar: Stahl haftet, Aluminiumbleche nicht.',
         color='#7A8288', marks=[mark('box', 10, 10, B - 20, T - 20, 6, '#6E767C')]),
    *waende,
    teil('emaille_aussen', 'steel_baking_tray', 'Emaille außen', 'Emaille außen', 'box',
         material_id='special_glass', x=0, y=0, w=B, d=T, z=0, h=0.3, r=6, mass=45,
         materials=[['emaille', 100]],
         info='Dünnere Emailleschicht auf der Unterseite, schützt vor Rost.',
         color=EMAILLE),
]
# Massen: Draht 90 g, Rand 380 g auf vier Wände verteilt
s = sum(p['mass'] for p in draht)
for p in draht:
    p['mass'] = round(p['mass'] / s * 90, 1)
s = sum(p['mass'] for p in waende)
for p in waende:
    p['mass'] = round(p['mass'] / s * 380, 1)
teile[5]['mass'] = 1300 - 90 - 380 - 90  # Boden
explodiere(teile, abstand=170, nach_liste=True,
           gruppen=[[p['id'] for p in draht], ['blech'] + [p['id'] for p in waende]])
dz_innen = next(p['explode'][2] for p in teile if p['id'] == 'emaille_innen')
for p in draht:  # Draht liegt außerhalb des Emaille-Grundrisses, trotzdem sichtbar darüber stapeln
    p['explode'] = [0, 0, dz_innen + 150]
skaliere_masse(teile, oid='baking_tray')
schreibe('baking_tray', teile)
