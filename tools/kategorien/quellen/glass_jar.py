"""3D-Modell: glass_jar. Erzeugt tools/kategorien/modelle/glass_jar.json.

Typisches Schraubglas (z. B. für Marmelade oder Gurken, etwa 300 ml, Twist-off-Deckel TO 66). Glasabschnitte
bewegen sich gemeinsam, Deckel und Dichtung schweben darüber, das Etikett wird seitlich herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

GLAS = '#DCE8E4'
OP = 0.6
teile = [
    teil('deckel', 'twist_off_lid', 'Twist-off-Deckel', 'Deckel', 'cyl',
         x=4, y=4, w=67, z=91, h=9, mass=14, materials=[['weissblech', 96], ['druck', 4]],
         info='Weißblech, innen lackiert. Vier Nocken greifen ins Gewinde. Abschrauben und in die Gelbe Tonne geben.',
         color='#C9A646', marks=[mark('cyl', 4, 4, 59, fill='#D8B85A'), mark('cyl', 22.5, 22.5, 22, fill='#B8963A')]),
    teil('dichtung', 'twist_off_lid', 'Dichtungsmasse', 'Dichtung', 'cyl',
         material_id='pvc', x=5.5, y=5.5, w=64, z=94, h=1.5, mass=1,
         info='Weicher Kunststoffring innen im Deckel. Er macht das Glas luftdicht, beim Öffnen hört man es ploppen. '
              'Bleibt am Deckel.',
         color='#E4E0D2', marks=[mark('cyl', 5, 5, 54, fill='#C9A646')]),
    teil('gewinde', 'glass_container', 'Gewindehals', 'Gewinde', 'cyl',
         x=6, y=6, w=63, z=88, h=8, mass=14,
         info='Kurze Gewindegänge aus Glas, auf denen der Deckel greift.', color=GLAS, opacity=OP,
         marks=[mark('cyl', 4, 4, 55)]),
    teil('schulter', 'glass_container', 'Schulter', 'Schulter', 'cyl',
         x=3, y=3, w=69, z=80, h=8, mass=16,
         info='Übergang vom Körper zum Gewinde.', color=GLAS, opacity=OP, label=False),
    teil('koerper', 'glass_container', 'Glaskörper', 'Glaskörper', 'cyl',
         x=0, y=0, w=75, z=0, h=80, mass=150,
         info='Weißglas (farblos). Leer, aber ungespült in den Weißglas-Container. Der Deckel gehört nicht ins Altglas.',
         color=GLAS, opacity=OP, marks=[mark('cyl', 4, 4, 67)]),
    teil('etikett', 'paper_label', 'Papieretikett', 'Etikett', 'box',
         x=75, y=12.5, w=0.3, d=50, z=15, h=55, r=0, explode=[50, 0, 0], mass=1.5,
         info='Papier mit Leim. Darf beim Altglas dranbleiben, es verbrennt in der Schmelze.',
         color='#E8DDC0', sortBias=100),
]
explodiere(teile, abstand=18, nach_liste=True, gruppen=[['gewinde', 'schulter', 'koerper']])
skaliere_masse(teile, oid='glass_jar')
schreibe('glass_jar', teile)
