"""3D-Modell: tea_light. Erzeugt tools/kategorien/modelle/tea_light.json.

Typisches Teelicht (38 mm, Aluminiumschale, Paraffin, Baumwolldocht mit Dochthalter). Wachs schwebt über der
Schale, Docht und Dochthalter bewegen sich gemeinsam darüber.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

teile = [
    teil('docht', 'cotton_wick', 'Docht', 'Docht', 'cyl',
         x=18, y=18, w=2, z=2, h=15.5, mass=0.05,
         info='Geflochtene Baumwolle, mit Wachs getränkt. Saugt das geschmolzene Wachs nach oben, wo es verbrennt.',
         color='#2E2A26'),
    teil('dochthalter', 'wick_holder', 'Dochthalter', 'Dochthalter', 'cyl',
         x=14, y=14, w=10, z=0.3, h=1.7, mass=0.15, materials=[['stahl', 95], ['alu', 5]],
         info='Kleines Blechplättchen, in das der Docht geklemmt ist. Es hält ihn aufrecht und löscht die Flamme, '
              'wenn das Wachs alle ist.',
         color='#B9BFC4', marks=[mark('cyl', 3.5, 3.5, 3, fill='#8E959B')]),
    teil('wachs', 'paraffin_wax', 'Wachsblock', 'Wachs', 'cyl',
         x=0.5, y=0.5, w=37, z=0.3, h=14.2, mass=11,
         info='Paraffin aus Erdöl, manchmal auch Stearin oder Rapswachs. Warm aus der Schale drücken: '
              'Reste lassen sich zu neuen Kerzen schmelzen.',
         color='#F3EFE6', marks=[mark('cyl', 16.5, 16.5, 4, fill='#E2DCCD')]),
    teil('schale', 'aluminium_cup', 'Aluminiumschale', 'Schale', 'cyl',
         x=0, y=0, w=38, z=0, h=15, mass=0.5,
         info='Dünnes Aluminium, schützt den Tisch vor heißem Wachs. Leer und ohne Wachs in die Gelbe Tonne.',
         color='#D5D8DB', wand=0.5, marks=[mark('cyl', 0.5, 0.5, 37, fill='#B9BFC4', zeichnung=True)]),
]
explodiere(teile, abstand=12, nach_liste=True, gruppen=[['docht', 'dochthalter']])
skaliere_masse(teile, oid='tea_light', stellen=2)
schreibe('tea_light', teile)
