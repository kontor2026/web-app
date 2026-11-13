"""3D-Modell: cosmetic_jar. Erzeugt tools/kategorien/modelle/cosmetic_jar.json.

Typischer 50-ml-Cremetiegel aus PP (Ø 60 mm, 45 mm hoch) mit doppelter Wand: dicker Außentiegel, eingesetzter
Innentiegel mit Gewinde, Schutzscheibe auf der Creme, Schraubdeckel mit Dichteinlage.
Alle Teile stapeln sich übereinander.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

WEISS = '#F7F5F2'
teile = [
    teil('deckel', 'pp_lid', 'Schraubdeckel', 'Deckel', 'cyl',
         x=0, y=0, w=60, z=30, h=15, mass=22,
         info='Dickwandiger PP-Deckel mit Innengewinde. Abschrauben, beides kommt in die Gelbe Tonne.',
         color='#C9A646', marks=[mark('cyl', 4, 4, 52, fill='#D8B85A')]),
    teil('einlage', 'pp_lid', 'Dichteinlage im Deckel', 'Einlage', 'cyl',
         material_id='ldpe', x=3, y=3, w=54, z=43, h=1, mass=1,
         info='Weiche PE-Scheibe innen im Deckel, die den Tiegel dicht macht. Bleibt im Deckel.',
         color='#ECECE8'),
    teil('schutzscheibe', 'pp_jar_body', 'Schutzscheibe', 'Schutzscheibe', 'cyl',
         material_id='ldpe', x=8, y=8, w=44, z=35, h=0.5, mass=1,
         info='Dünne PE-Scheibe mit Lasche, die direkt auf der Creme liegt. In die Gelbe Tonne.',
         color='#FFFFFF', marks=[mark('box', 18, 0, 8, 6, 2, '#E2E2DC')]),
    teil('innentiegel', 'pp_jar_body', 'Innentiegel mit Gewinde', 'Innentiegel', 'cyl',
         x=5, y=5, w=50, z=3, h=34, mass=22,
         info='Eigentlicher Behälter für die Creme. Mit einem Spatel leer kratzen, Cremereste gehören in den '
              'Restmüll.',
         color=WEISS, marks=[mark('cyl', 3, 3, 44, fill='#E9E6E0')]),
    teil('aussentiegel', 'pp_jar_body', 'Außentiegel', 'Außentiegel', 'cyl',
         x=1, y=1, w=58, z=0, h=31, mass=34,
         info='Dicke Außenwand, die den Tiegel größer und wertiger wirken lässt als den Inhalt. '
              'Mit dem Innentiegel verklebt oder verrastet, beide PP, also gemeinsam in die Gelbe Tonne.',
         color='#E9E2D8', marks=[mark('cyl', 3, 3, 52, fill='#D9D1C4')]),
]
explodiere(teile, abstand=12, nach_liste=True)
skaliere_masse(teile, oid='cosmetic_jar')
schreibe('cosmetic_jar', teile)
