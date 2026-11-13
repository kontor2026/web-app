"""3D-Modell: alkaline_battery. Erzeugt tools/kategorien/modelle/alkaline_battery.json.

Alkali-Mignonzelle (AA, LR6), aufrecht mit dem Minuspol nach oben, damit Deckel, Dichtung und Ableiternagel
oben herausgehoben werden können. Die langen Innenteile (Kathodenring, Separator, Zinkgel) werden in einer
Reihe seitlich herausgezogen, das Etikett nach links.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, schreibe  # noqa: E402

C = 'alkaline_cell'
teile = [
    teil('minuspol', C, 'Minuspol-Deckel', 'Minuspol', 'cyl',
         material_id='steel', x=0.4, y=0.4, w=13.4, z=49.4, h=0.6, explode=[0, 0, 32], mass=0.6,
         materials=[['stahl', 100]],
         info='Vernickeltes Stahlblech, der Minuspol. Beim Sammeln die Pole nicht mit anderen Batterien '
              'in Kontakt bringen.',
         color='#C9CDD0', marks=[mark('cyl', 4.2, 4.2, 5)]),
    teil('dichtung', C, 'Dichtung', 'Dichtung', 'cyl',
         material_id='nylon', x=0.6, y=0.6, w=13, z=46.4, h=3, explode=[0, 0, 18], mass=0.5,
         materials=[['nylon', 100]],
         info='Kunststoffscheibe, die die Zelle dicht verschließt. Hat eine Sollbruchstelle, '
              'damit bei Überdruck kein Bersten droht.',
         color='#F2EFE8', marks=[mark('cyl', 5.5, 5.5, 2), mark('cyl', 2, 2, 9)]),
    teil('nagel', C, 'Ableiternagel', 'Nagel', 'cyl',
         material_id='copper', x=6.4, y=6.4, w=1.4, z=8, h=41.4, explode=[0, -24, 0], mass=0.3,
         materials=[['messing', 100]],
         info='Nagel aus Messing (Kupfer und Zink). Steckt im Zinkgel und leitet den Strom zum Minuspol.',
         color='#D4B464'),
    teil('anode', C, 'Zinkgel (Anode)', 'Zinkgel', 'cyl',
         material_id='alkaline', x=2.8, y=2.8, w=8.6, z=4, h=41, explode=[60, 0, 0], mass=6,
         materials=[['zinkmangan', 100]],
         info='Zinkpulver in Kalilauge. Die Lauge ist ätzend: Ausgelaufene Batterien nur mit Handschuhen anfassen.',
         color='#9EA3A8'),
    teil('separator', C, 'Separator', 'Separator', 'cyl',
         material_id='paper', x=2.4, y=2.4, w=9.4, z=3.5, h=42.5, explode=[42, 0, 0], mass=0.3,
         materials=[['papier', 100]],
         info='Saugfähiges Vlies zwischen Anode und Kathode. Trennt beide, lässt aber die Lauge durch.',
         color='#ECE6D6'),
    teil('kathode', C, 'Mangandioxid-Ring (Kathode)', 'Kathode', 'cyl',
         material_id='alkaline', x=0.9, y=0.9, w=12.4, z=3, h=42, explode=[24, 0, 0], mass=10.5,
         materials=[['zinkmangan', 90], ['graphit', 10]],
         info='Schwarzer Ring aus Braunstein und Graphit, innen hohl. Liefert zusammen mit dem Zink den Strom.',
         color='#2A2B2D', marks=[mark('cyl', 1.5, 1.5, 9.4, fill='#3A3D40')]),
    teil('etikett', C, 'Etikett (Schrumpffolie)', 'Etikett', 'cyl',
         material_id='pvc', x=0, y=0, w=14.2, z=0.5, h=49, explode=[-24, 0, 0], mass=0.4,
         materials=[['pvc', 100]],
         info='Bedruckte Kunststofffolie. Isoliert den Stahlbecher und zeigt Typ, Spannung (1,5 V) und Haltbarkeit.',
         color='#C8423A', opacity=0.85, marks=[mark('cyl', 0.6, 0.6, 13)]),
    teil('becher', C, 'Stahlbecher mit Pluspol', 'Becher', 'cyl',
         material_id='steel', x=0.2, y=0.2, w=13.8, z=0, h=48.5, explode=[0, 0, 0], mass=4.2,
         materials=[['stahl', 100]],
         info='Vernickelter Stahlbecher, unten mit dem Pluspol-Knopf. Im Recycling wird daraus wieder Stahl, '
              'aus dem Inhalt Zink und Mangan.',
         color='#B7BCC0', marks=[mark('cyl', 0.3, 0.3, 13.2, fill='#5E656A')]),
]
schreibe('alkaline_battery', teile)
