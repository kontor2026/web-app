"""3D-Modell: scissors. Erzeugt tools/kategorien/modelle/scissors.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Geschlossene Bastel-/Haushaltsschere flach auf dem Tisch, Spitze hinten (y = 0), Griffe vorne. 70 × 198 × 9.5 mm.
# Zwei Edelstahlklingen übereinander, Drehpunkt bei y = 100, Kunststoffgriffe um die Klingenenden gespritzt.
# Explodiert: Griffe zur Seite, Klingen, Schraube und Mutter übereinander.
STAHL = '#C3C9CE'
GRIFF = '#D9473A'

teile = [
    teil('schraube', 'steel_blades', 'Gelenkschraube', 'Schraube', 'cyl',
         x=31.5, y=96.5, w=7, z=7.5, h=2, mass=2,
         info='Hält beide Klingen zusammen und ist die Drehachse. Mit einem Schraubendreher lösen, '
              'dann fallen die Klingen auseinander.',
         color='#9AA2A6', marks=[mark('box', 0.75, 3, 5.5, 1, fill='#5A6268')]),
    teil('klinge_oben', 'steel_blades', 'Obere Klinge', 'Klinge oben', 'box',
         x=27, y=0, w=16, d=135, z=5, h=2.5, r=4, mass=26,
         info='Rostfreier Edelstahl, nur eine Seite ist geschliffen. Vor dem Wegwerfen die Spitze mit Klebeband oder Pappe sichern.',
         color=STAHL, marks=[mark('box', 13, 4, 2, 92, 1, '#E3E7EA'), mark('cyl', 4.5, 96.5, 7, fill='#9AA2A6')]),
    teil('klinge_unten', 'steel_blades', 'Untere Klinge', 'Klinge unten', 'box',
         x=27, y=2, w=16, d=133, z=2.5, h=2.5, r=4, mass=26,
         info='Gleitet beim Schneiden an der oberen Klinge vorbei. Die Klingen sind wertvoller Stahlschrott für den Wertstoffhof.',
         color=STAHL, marks=[mark('box', 1, 4, 2, 90, 1, '#E3E7EA'), mark('cyl', 4.5, 94.5, 7, fill='#9AA2A6')]),
    teil('mutter', 'steel_blades', 'Mutter', 'Mutter', 'cyl',
         x=32, y=97, w=6, z=0.5, h=2, mass=1,
         info='Gegenstück zur Gelenkschraube unter der unteren Klinge.',
         color='#9AA2A6', marks=[mark('cyl', 2, 2, 2, fill='#5A6268')]),
    teil('griff_links', 'plastic_handles', 'Griff (kleines Auge)', 'Griff links', 'box',
         x=0, y=126, w=35, d=72, z=0.5, h=9, r=15, explode=[-30, 0, 0], mass=12, materials=[['pp', 80], ['tpe', 20]],
         info='Polypropylen mit weicher Griffzone, fest um das Klingenende gespritzt. Lässt er sich nicht abziehen, '
              'mit einer Zange aufbrechen, dann Kunststoff und Stahl getrennt entsorgen.',
         color=GRIFF, marks=[mark('box', 7, 12, 21, 48, 10, '#F3F1EC')]),
    teil('griff_rechts', 'plastic_handles', 'Griff (großes Auge)', 'Griff rechts', 'box',
         x=35, y=126, w=35, d=72, z=0.5, h=9, r=15, explode=[30, 0, 0], mass=14, materials=[['pp', 80], ['tpe', 20]],
         info='Das größere Auge ist für zwei bis drei Finger. Es gehört zur unteren Klinge.',
         color=GRIFF, marks=[mark('box', 7, 8, 21, 56, 10, '#F3F1EC')]),
]

explodiere(teile, abstand=18)
skaliere_masse(teile, oid='scissors')
schreibe('scissors', teile)
