"""3D-Modell: bottle_crate. Erzeugt tools/kategorien/modelle/bottle_crate.json.

Typischer Mehrweg-Getränkekasten für 20 × 0,5 l (40 × 30 × 30 cm) aus HDPE, ein einziges Spritzgussteil.
Zur Erklärung in Ebenen zerlegt: Oberrand mit Griffen, Gefache mit 5 × 4 Zellen, Außenwand, Boden mit
Ablauflöchern, dazu das In-Mould-Etikett. Ebenen nach oben gestapelt, Etikett nach vorne.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

KASTEN = '#2F6E3B'
DUNKEL = '#1F4A27'
teile = [
    teil('oberrand', 'hdpe_crate_body', 'Oberrand mit Griffen', 'Oberrand', 'box',
         x=0, y=0, w=400, d=300, z=262, h=38, r=8, mass=380,
         info='Verstärkter Rand mit Griffmulden an den Schmalseiten. Der Kasten ist ein einziges Spritzgussteil.',
         color=KASTEN, marks=[mark('box', 10, 10, 380, 280, 5, DUNKEL), mark('box', 2, 110, 6, 80, 3, '#163A1E'),
                              mark('box', 392, 110, 6, 80, 3, '#163A1E')]),
    teil('gefache', 'hdpe_crate_body', 'Gefache', 'Gefache', 'box',
         x=10, y=10, w=380, d=280, z=12, h=160, r=4, mass=430,
         info='Trennstege für 20 Flaschen, damit sie nicht aneinanderschlagen und zerbrechen.',
         color=KASTEN, marks=raster(4, 4, 5, 4, 68, 62, 75, 69, r=6, fill=DUNKEL)),
    teil('wand', 'hdpe_crate_body', 'Außenwand', 'Außenwand', 'box',
         x=3, y=3, w=394, d=294, z=12, h=250, r=8, mass=650,
         info='Rippen und Durchbrüche sparen Material und halten den Kasten trotzdem stabil.',
         color=KASTEN, marks=[mark('box', 7, 7, 380, 280, 4, DUNKEL)]),
    teil('boden', 'hdpe_crate_body', 'Boden mit Ablauflöchern', 'Boden', 'box',
         x=0, y=0, w=400, d=300, z=0, h=12, r=8, mass=235,
         info='Gitterboden, damit Wasser ablaufen kann. Die Füße greifen beim Stapeln in den Kasten darunter.',
         color=KASTEN, marks=raster(18, 18, 9, 6, 22, 22, 42, 46, r=3, fill=DUNKEL)),
    teil('etikett', 'hdpe_crate_body', 'In-Mould-Etikett', 'Etikett', 'box',
         material_id='pp', x=120, y=299.7, w=160, d=0.3, z=150, h=80, r=0, explode=[0, 70, 0], mass=5,
         materials=[['pp', 95], ['druck', 5]],
         info='Bedrucktes PP-Etikett, beim Spritzgießen eingeschmolzen. Nicht abreißen: Kästen haben Pfand, werden '
              'über Jahre wiederbefüllt und am Ende zu neuen Kästen gemahlen.',
         color='#F2F0EA', sortBias=100),
]
explodiere(teile, abstand=55)
skaliere_masse(teile, oid='bottle_crate')
schreibe('bottle_crate', teile)
