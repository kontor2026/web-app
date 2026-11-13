"""3D-Modell: button_cell_battery. Erzeugt tools/kategorien/modelle/button_cell_battery.json.

Lithium-Knopfzelle CR2032 (20 × 3,2 mm), liegt mit dem kleinen Minuspol-Deckel nach oben. Die Schichten werden in
Bauteilreihenfolge nach oben abgehoben: Deckel, Dichtring, Lithium-Anode, Separator, Braunstein-Kathode, Becher.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

C = 'button_cell'
STAHL = '#C9CDD0'
teile = [
    teil('deckel', C, 'Minuspol-Deckel', 'Minuspol', 'cyl',
         material_id='steel', x=1.6, y=1.6, w=16.8, z=2.6, h=0.6, mass=0.5, materials=[['stahl', 90], ['nickel', 10]],
         info='Vernickeltes Stahlblech, der Minuspol. Vor dem Abgeben beide Seiten mit Klebeband abkleben, '
              'damit es keinen Kurzschluss gibt.',
         color=STAHL, marks=[mark('cyl', 2, 2, 12.8), mark('cyl', 5.4, 5.4, 6)]),
    teil('dichtung', C, 'Dichtring', 'Dichtring', 'cyl',
         material_id='pp', x=0.8, y=0.8, w=18.4, z=0.4, h=2.8, mass=0.1, materials=[['pp', 100]],
         info='Kunststoffring zwischen Deckel und Becher. Er isoliert die beiden Pole und hält den Elektrolyten dicht.',
         color='#2E3236', marks=[mark('cyl', 1, 1, 16.4, fill='#5E656A')]),
    teil('anode', C, 'Lithium-Anode', 'Lithium', 'cyl',
         material_id='coin_cell', x=2.5, y=2.5, w=15, z=2, h=0.6, mass=0.12, materials=[['knopfzelle', 100]],
         info='Dünne Scheibe aus Lithium-Metall. Lithium reagiert heftig mit Wasser, darum die Zelle nie aufschneiden.',
         color='#B4B8BC'),
    teil('separator', C, 'Separator mit Elektrolyt', 'Separator', 'cyl',
         material_id='coin_cell', x=2, y=2, w=16, z=1.8, h=0.2, mass=0.2,
         materials=[['pp', 50], ['knopfzelle', 50]],
         info='Vlies aus Kunststoff, getränkt mit organischem Elektrolyten. Trennt Anode und Kathode.',
         color='#ECE6D6'),
    teil('kathode', C, 'Braunstein-Kathode', 'Kathode', 'cyl',
         material_id='coin_cell', x=2.25, y=2.25, w=15.5, z=0.4, h=1.4, mass=1.0,
         materials=[['knopfzelle', 85], ['graphit', 15]],
         info='Gepresste Tablette aus Mangandioxid und Graphit. Zusammen mit dem Lithium liefert sie 3 Volt.',
         color='#2A2B2D'),
    teil('becher', C, 'Pluspol-Becher', 'Pluspol', 'cyl',
         material_id='steel', x=0, y=0, w=20, z=0, h=3.2, mass=0.9, materials=[['stahl', 90], ['nickel', 10]],
         info='Flacher Becher aus vernickeltem Stahl, der Pluspol mit der Aufschrift „CR2032“. Knopfzellen gehören '
              'in die Batteriesammlung und außer Reichweite kleiner Kinder: Verschluckt sind sie lebensgefährlich.',
         color=STAHL, marks=[mark('cyl', 0.8, 0.8, 18.4, fill='#5E656A')]),
]
explodiere(teile, abstand=9, nach_liste=True)
skaliere_masse(teile, oid='button_cell_battery', stellen=2)
schreibe('button_cell_battery', teile)
