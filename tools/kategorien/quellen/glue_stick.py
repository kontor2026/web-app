"""3D-Modell: glue_stick. Erzeugt tools/kategorien/modelle/glue_stick.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Klebestift (ca. 20 g) aufrecht, 30 × 30 × 100 mm laut CSV, Kappe oben. Hülse Ø 28 mm, unten der Drehknopf mit
# Gewindespindel, darauf der Kolben (Schale), in dem die Klebemasse sitzt. Explodiert: Kappe schwebt über der Hülse,
# das Innenleben (Spindel, Kolben, Klebemasse) wird seitlich (dx > 0) herausgezogen.
WEISS = '#F3F1EC'
DECKEL = '#D9473A'
INNEN = 42

teile = [
    teil('kappe', 'pen_cap', 'Schraub-/Steckkappe', 'Kappe', 'cyl',
         x=0, y=0, w=30, z=70, h=30, mass=3.0,
         info='Dichte Kappe aus Polypropylen, damit der Kleber nicht austrocknet. Gleicher Kunststoff wie die Hülse.',
         color=DECKEL, marks=[mark('cyl', 3, 3, 24, fill='#C43F33'), mark('cyl', 7, 7, 16, fill='#B83A2F'),
                              mark('cyl', 12, 12, 6, fill='#A53428')]),
    teil('klebemasse', 'glue_stick_tube', 'Klebemasse', 'Kleber', 'cyl',
         x=4, y=4, w=22, z=30, h=44, mass=21, materials=[['klebstoff', 100]],
         info='Fester Klebstoff aus Seife, PVP-Kunststoff und Wasser, lösemittelfrei und auswaschbar. Reste herauskratzen; '
              'die Masse gehört in den Restmüll.',
         color='#FAFAF5', marks=[mark('cyl', 3, 3, 16, fill='#EDEBE4')]),
    teil('kolben', 'glue_stick_tube', 'Kolben (Schale)', 'Kolben', 'cyl',
         x=3, y=3, w=24, z=24, h=8, mass=1.0,
         info='Kleine Schale mit Innengewinde. Beim Drehen wandert sie auf der Spindel nach oben und schiebt den Kleber heraus.',
         color=WEISS, marks=[mark('cyl', 8, 8, 8, fill='#C9CDD0')]),
    teil('spindel', 'glue_stick_tube', 'Gewindespindel', 'Spindel', 'cyl',
         x=11, y=11, w=8, z=8, h=40, mass=0.8,
         info='Schraube aus Kunststoff, fest mit dem Drehknopf verbunden. Sie trägt den Kolben.',
         color=WEISS, marks=[mark('cyl', 2, 2, 4, fill='#C9CDD0')]),
    teil('huelse', 'glue_stick_tube', 'Hülse', 'Hülse', 'cyl',
         x=1, y=1, w=28, z=10, h=64, mass=4.5,
         info='Bedruckte PP-Hülse. Ganz leer gedreht und ausgekratzt darf sie in die Gelbe Tonne; mit Kleberesten in den Restmüll.',
         color=WEISS, marks=[mark('cyl', 2, 2, 24, fill='#E4E1D8')]),
    teil('etikett', 'glue_stick_tube', 'Bedrucktes Etikett', 'Etikett', 'cyl',
         x=0.7, y=0.7, w=28.6, z=22, h=48, mass=0.4, explode=[-48, 0, 0], sortBias=5,
         info='Dünne bedruckte PP-Folie, beim Spritzgießen mit der Hülse verschmolzen (In-Mould-Label). '
              'Sie muss nicht abgezogen werden, weil sie aus demselben Kunststoff ist.',
         color='#F2C230', marks=[mark('cyl', 0.4, 0.4, 27.8, fill='#D8D4CA')]),
    teil('drehknopf', 'glue_stick_tube', 'Drehknopf', 'Drehknopf', 'cyl',
         x=1, y=1, w=28, z=0, h=10, mass=1.7,
         info='Am Boden drehen, dann schraubt sich der Kleber heraus. Er ist in die Hülse eingeschnappt.',
         color=DECKEL, marks=[mark('cyl', 9, 9, 10, fill='#B83A2F')]),
]

innen = [p for p in teile if p['id'] in ('klebemasse', 'kolben', 'spindel')]
explodiere(innen, abstand=8)
for p in innen:
    p['explode'][0] = INNEN
for p in teile:
    if p['id'] in ('huelse', 'drehknopf'):
        p['explode'] = [0, 0, 0]
explodiere(teile, abstand=26)
skaliere_masse(teile, oid='glue_stick', stellen=2)
schreibe('glue_stick', teile)
