"""3D-Modell: blender. Erzeugt tools/kategorien/modelle/blender.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Standmixer: Motorsockel 170 × 170 mm (z 0..140), darauf der Mixbehälter (z 140..372) mit Griff rechts (x 155..180),
# Deckel mit Messbecher bis z 380. Bedienknopf vorne (y groß).
# Explosion nach Liste (letztes Teil unten): Bodenplatte bleibt, Lüfter, Motor, Kupplung, darüber das Sockelgehäuse,
# dann Behälterfuß, Dichtring, Messer, Behälter (mit Griff als Gruppe), Deckel.
# Drehknopf nach vorne (dy > 0), Kabel nach rechts (dx > 0).

teile = [
    teil('deckel', 'blender_jar', 'Behälterdeckel', 'Deckel', 'box', material_id='pp',
         x=15, y=15, w=140, d=140, z=360, h=20, r=24, mass=80, materials=[['pp', 55], ['tpe', 45]],
         info='Weicher Deckel mit Dichtlippe und eingesetztem Messbecher zum Nachfüllen. Wird nur aufgedrückt; Messbecher herausdrehen und beides zum Kunststoff.',
         color='#2E3338', marks=[mark('cyl', 40, 40, 60, fill='#C5D3DC'), mark('cyl', 50, 50, 40, fill='#E9EEF2')]),
    teil('behaelter_oben', 'blender_jar', 'Mixbehälter Oberteil', 'Behälter oben', 'box',
         x=15, y=15, w=140, d=140, z=260, h=100, r=24, mass=300,
         info='Bruchfester Kunststoff (Copolyester oder Polycarbonat) mit Skala. Den Materialcode findet man am Behälterboden.',
         color='#DDE6EC', opacity=0.6, marks=[mark('box', 10, 10, 120, 120, 20, fill='#C5D3DC')]),
    teil('griff', 'blender_jar', 'Behältergriff', 'Griff', 'box',
         x=155, y=70, w=25, d=30, z=200, h=140, r=8, mass=60,
         info='Angespritzter Griff des Behälters. Er gehört zum Behälter und wird nicht abgetrennt.',
         color='#2E3338'),
    teil('behaelter_unten', 'blender_jar', 'Mixbehälter Unterteil', 'Behälter unten', 'box',
         x=25, y=25, w=120, d=120, z=160, h=100, r=20, mass=220,
         info='Der Behälter wird nach unten schmaler, damit das Mixgut immer wieder zum Messer fällt.',
         color='#DDE6EC', opacity=0.6),
    teil('messer', 'blender_blade', 'Messereinheit', 'Messer', 'cyl',
         x=40, y=40, w=90, z=160, h=18, mass=110, materials=[['stahl', 90], ['messing', 5], ['gummi', 5]],
         info='Vier Edelstahlklingen auf einer kugelgelagerten Welle. Sehr scharf: vor dem Entsorgen in Zeitungspapier wickeln.',
         color='#B8BEC4', marks=[mark('box', 5, 39, 80, 12, 4, fill='#D5DADE'), mark('box', 39, 5, 12, 80, 4, fill='#D5DADE'),
                                 mark('cyl', 35, 35, 20, fill='#7C858C')]),
    teil('dichtring', 'blender_blade', 'Dichtring', 'Dichtring', 'cyl', material_id='rubber',
         x=40, y=40, w=90, z=156, h=4, mass=8, materials=[['gummi', 100]],
         info='Silikonring zwischen Messereinheit und Behälter. Er hält dicht und lässt sich mit den Fingern abziehen.',
         color='#5A6670', marks=[mark('cyl', 12, 12, 66, fill='#3A444C')]),
    teil('behaelterfuss', 'blender_jar', 'Behälterfuß mit Kupplung', 'Behälterfuß', 'box', material_id='pp',
         x=20, y=20, w=130, d=130, z=140, h=16, r=20, mass=90, materials=[['pp', 85], ['stahl', 15]],
         info='Schraubring unter dem Behälter, hält die Messereinheit und trägt das Gegenstück der Antriebskupplung. Gegen den Uhrzeigersinn abschrauben.',
         color='#2E3338', marks=[mark('cyl', 45, 45, 40, fill='#9AA2A6')]),
    teil('gehaeuse', 'plastic_housing', 'Sockelgehäuse', 'Gehäuse', 'box',
         x=0, y=0, w=170, d=170, z=12, h=128, r=24, mass=420,
         info='Kunststoffgehäuse des Motorsockels. Die Schrauben sitzen unter den Gummifüßen der Bodenplatte.',
         color='#3C4248', marks=[mark('box', 20, 20, 130, 130, 18, fill='#2E3338'), mark('cyl', 60, 60, 50, fill='#1E2226')]),
    teil('kupplung', 'electric_motor', 'Antriebskupplung', 'Kupplung', 'cyl', material_id='rubber',
         x=65, y=65, w=40, z=120, h=22, mass=30, materials=[['gummi', 50], ['stahl', 50]],
         info='Gezahntes Gummi-Metall-Teil auf der Motorwelle, das den Behälter antreibt. Mit einem Schlüssel von der Welle drehen.',
         color='#2E3338', marks=[mark('cyl', 12, 12, 16, fill='#9AA2A6')]),
    teil('motor', 'electric_motor', 'Universalmotor', 'Motor', 'cyl',
         x=35, y=35, w=100, z=30, h=90, mass=800,
         materials=[['kupfer', 30], ['stahl', 55], ['graphit', 3], ['pcabs', 7], ['alu', 5]],
         info='Kräftiger Motor mit Kupferwicklungen und Kohlebürsten, bis 1000 Watt. Ist mit vier Schrauben am Gehäuse befestigt.',
         marks=[mark('cyl', 10, 10, 80, fill='#B87333'), mark('cyl', 35, 35, 30, fill='#7C858C')]),
    teil('schalter', 'electric_motor', 'Drehzahlschalter mit Entstörteilen', 'Schalter', 'box', material_id='mixed_electronics',
         x=20, y=148, w=130, d=14, z=30, h=80, r=1, mass=40,
         materials=[['pcabs', 45], ['kupfer', 25], ['kontakte', 10], ['fr4', 15], ['chip', 5]],
         info='Stufenschalter mit Kondensator gegen Funkstörungen. Kabel sind gesteckt und lassen sich abziehen.',
         color='#2F6B3A', marks=[mark('box', 50, 3, 30, 8, 1, fill='#9AA2A6')]),
    teil('drehknopf', 'plastic_housing', 'Drehknopf', 'Drehknopf', 'box',
         x=65, y=168, w=40, d=14, z=50, h=40, r=4, explode=[0, 50, 0], mass=15,
         info='Stellt die Stufen und die Puls-Funktion ein. Gerade von der Achse abziehen.',
         color='#9AA2A6'),
    teil('luefter', 'electric_motor', 'Lüfterrad', 'Lüfter', 'cyl', material_id='pp',
         x=45, y=45, w=80, z=14, h=14, mass=30, materials=[['pp', 100]],
         info='Sitzt unten auf der Motorwelle und kühlt den Motor. Lässt sich nach dem Lösen der Mutter abziehen.',
         color='#5F6B75', marks=raster(10, 37, 6, 1, 8, 6, 10, r=1, fill='#4A545C')),
    teil('bodenplatte', 'plastic_housing', 'Bodenplatte mit Saugfüßen', 'Bodenplatte', 'box',
         x=0, y=0, w=170, d=170, z=0, h=12, r=24, mass=150, materials=[['pcabs', 85], ['gummi', 15]],
         info='Unterseite mit Lüftungsschlitzen und Saugfüßen. Unter den Füßen verstecken sich die Gehäuseschrauben.',
         color='#2E3338', marks=raster(14, 14, 2, 2, 16, 16, 126, shape='cyl', fill='#1E2226') + raster(40, 80, 6, 1, 8, 10, 16, r=1, fill='#1E2226')),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=100, y=10, w=70, d=8, z=2, h=8, r=4, explode=[80, 0, 0], mass=80, materials=[['pvc', 90], ['pp', 10]],
         info='Etwa 1 m PVC-Mantel mit Stecker. Längs aufschlitzen, um Kupfer und PVC zu trennen.',
         color='#2E3338', marks=[mark('box', 60, 1, 10, 6, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=100, y=12.5, w=70, d=3, z=4.5, h=3, r=1, explode=[80, 0, 15], mass=40,
         info='Drei Kupferadern. Kupfer ist der wertvollste Rohstoff im Kabel und wird fast vollständig recycelt.',
         color='#B87333'),
]

explodiere(teile, abstand=25, fest=('bodenplatte',), gruppen=[['behaelter_oben', 'griff', 'behaelter_unten']], nach_liste=True)
skaliere_masse(teile, oid='blender')
schreibe('blender', teile)
