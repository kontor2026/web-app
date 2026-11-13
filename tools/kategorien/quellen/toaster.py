"""3D-Modell: toaster. Erzeugt tools/kategorien/modelle/toaster.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Zwei-Schlitz-Toaster: Schlitze laufen entlang x, liegen hintereinander in y. Rechts (x 250..270) das
# Kunststoff-Seitenteil mit Bedienelementen, Hebel und Regler ragen bis x 282 heraus.
# Explosion: Bodenplatte bleibt, Heizplatten und Brotschlitten schweben darüber, Blechmantel ganz oben.
# Krümelschublade nach vorne (dy > 0) herausgezogen, Seitenteil und Bedienteile nach rechts, Kabel nach rechts hinten.
SLOT = [(0, 35), (0, 90)]  # y-Anfang der Schlitze, je 35 mm breit

teile = [
    teil('mantel', 'stainless_steel_body', 'Gehäusemantel (Edelstahl)', 'Mantel', 'box',
         x=0, y=0, w=250, d=160, z=12, h=178, r=22, mass=330,
         info='Ein gebogenes Edelstahlblech mit zwei Brotschlitzen. Nach Lösen der Bodenschrauben nach oben abziehen; Kanten sind scharf.',
         color='#C9CED2', marks=[mark('box', 25, y, 200, 35, 6, fill='#2A2D30') for _, y in SLOT]
         + [mark('box', 31, y + 15, 188, 5, 2, fill='#5A4A3C') for _, y in SLOT]),
    teil('heizplatte_vorne', 'heating_element', 'Heizplatte vorne', 'Heizplatte vorne', 'box',
         x=25, y=129, w=200, d=4, z=40, h=130, r=0.5, mass=40, materials=[['nichrom', 40], ['glimmer', 60]],
         info='Glimmerplatte, um die ein flaches Nickel-Chrom-Band gewickelt ist. Glüht rot und röstet das Brot von einer Seite.',
         color='#8C7B6B', marks=raster(4, 0.5, 20, 1, 4, 3, 10, r=0.5, fill='#C4672D')),
    teil('heizplatte_mitte', 'heating_element', 'Heizplatte Mitte (doppelseitig)', 'Heizplatte Mitte', 'box',
         x=25, y=77, w=200, d=6, z=40, h=130, r=0.5, mass=55, materials=[['nichrom', 45], ['glimmer', 55]],
         info='Heizt beide Schlitze gleichzeitig, deshalb doppelt bewickelt. Der Draht ist dünn und bricht leicht.',
         color='#8C7B6B', marks=raster(4, 1, 20, 1, 4, 4, 10, r=0.5, fill='#C4672D')),
    teil('heizplatte_hinten', 'heating_element', 'Heizplatte hinten', 'Heizpl. hinten', 'box',
         x=25, y=27, w=200, d=4, z=40, h=130, r=0.5, mass=40, materials=[['nichrom', 40], ['glimmer', 60]],
         info='Wie die vordere Platte. Die Glimmerplatten isolieren den heißen Draht vom Blechgehäuse.',
         color='#8C7B6B', marks=raster(4, 0.5, 20, 1, 4, 3, 10, r=0.5, fill='#C4672D')),
    teil('brotschlitten', 'stainless_steel_body', 'Brotschlitten mit Führungsgittern', 'Brotschlitten', 'box',
         x=25, y=35, w=200, d=90, z=26, h=8, r=2, mass=90,
         info='Verzinktes Stahlgestell, das die Scheiben hebt und senkt. Eine Feder zieht es nach dem Toasten wieder nach oben.',
         color='#9AA2A6', marks=[mark('box', 4, y - 35 + 4, 192, 27, 2, fill='#7C858C') for _, y in SLOT]),
    teil('feder', 'stainless_steel_body', 'Rückholfeder', 'Feder', 'cyl',
         x=230, y=36, w=6, z=30, h=90, mass=4, materials=[['stahl', 100]],
         info='Federstahl-Zugfeder, die den Brotschlitten nach oben schnellen lässt. Steht unter Spannung, beim Ausbau festhalten.',
         color='#8A9399', marks=[mark('cyl', 1.5, 1.5, 3, fill='#5E666C')]),
    teil('magnet', 'heating_element', 'Haltemagnet', 'Haltemagnet', 'box', material_id='steel',
         x=228, y=86, w=8, d=20, z=36, h=22, r=1, mass=18, materials=[['stahl', 60], ['kupfer', 40]],
         info='Elektromagnet aus Eisenkern und Kupferwicklung. Hält den Hebel unten, bis die Steuerung den Strom abschaltet.',
         color='#6C7378', marks=[mark('box', 1, 3, 6, 14, 1, fill='#B87333')]),
    teil('steuerplatine', 'heating_element', 'Steuerplatine', 'Steuerplatine', 'box', material_id='pcb',
         x=236, y=20, w=12, d=120, z=30, h=110, r=1, mass=35,
         materials=[['fr4', 50], ['kupfer', 25], ['chip', 15], ['lot', 10]],
         info='Zeitschaltung mit Kondensator und Chip: Sie schaltet nach der eingestellten Röstzeit den Haltemagneten ab. Mit Kupferleiterbahnen und Lötstellen.',
         color='#2F6B3A', marks=[mark('cyl', 2, 10, 8, 8, fill='#2B4A8C'), mark('box', 2, 50, 8, 12, 1, fill='#222'),
                                  mark('box', 3, 80, 6, 20, 1, fill='#D9D2BE')]),
    teil('seitenteil', 'stainless_steel_body', 'Seitenteil mit Bedienfeld', 'Seitenteil', 'box', material_id='pp',
         x=250, y=8, w=14, d=144, z=12, h=172, r=6, explode=[120, 0, 0], sortBias=10, mass=90, materials=[['pp', 100]],
         info='Hitzefester Kunststoff, trägt Hebelschlitz, Regler und Tasten. Ist eingeclipst und mit zwei Schrauben gesichert.',
         color='#5B6268', marks=[mark('box', 4, 56, 6, 48, 3, fill='#1E2226')]),
    teil('hebel', 'plastic_knobs', 'Absenkhebel', 'Hebel', 'box',
         x=264, y=60, w=16, d=40, z=140, h=16, r=5, explode=[200, 0, 0], sortBias=150, mass=8,
         info='Kunststoffgriff auf dem Hebelblech. Gerade abziehen, darunter ist Metall.',
         color='#1E2226', marks=[mark('box', 3, 4, 10, 32, 4, fill='#2E3338')]),
    teil('stopptaste', 'plastic_knobs', 'Stopp-Taste', 'Stopp-Taste', 'box',
         x=264, y=58, w=6, d=16, z=95, h=12, r=3, explode=[200, 0, 0], sortBias=150, mass=2,
         info='Unterbricht das Toasten sofort. Die Kappe ist nur aufgesteckt.',
         color='#C0392B'),
    teil('drehregler', 'plastic_knobs', 'Bräunungsregler', 'Regler', 'cyl',
         x=264, y=96, w=12, d=30, z=45, h=30, explode=[200, 0, 0], sortBias=150, mass=6,
         info='Stellt die Röstzeit von 1 bis 7 ein. Lässt sich von der Achse abziehen.',
         color='#B9BEC2', marks=[mark('box', 4, 13, 4, 4, 1, fill='#1E2226')]),
    teil('kruemelschublade', 'crumb_tray', 'Krümelschublade', 'Krümelschublade', 'box',
         x=20, y=10, w=215, d=145, z=13, h=4, r=2, explode=[0, 175, 0], mass=45,
         info='Aluminiumblech, das herabfallende Krümel auffängt. Nach vorne herausziehen und regelmäßig leeren, sonst kann es brennen.',
         color='#D4D8DB', marks=[mark('box', 90, 137, 35, 8, 2, fill='#2E3338')]),
    teil('bodenplatte', 'stainless_steel_body', 'Bodenplatte mit Füßen', 'Bodenplatte', 'box',
         x=0, y=0, w=250, d=160, z=0, h=12, r=22, mass=220, materials=[['stahl', 85], ['gummi', 5], ['pp', 10]],
         info='Verzinktes Stahlblech mit Gummifüßen und Kabelaufwicklung. Nach dem Ausschrauben liegen Heizplatten und Mechanik frei.',
         color='#7C858C', marks=raster(12, 12, 2, 2, 16, 16, 210, 120, shape='cyl', fill='#2E3338')),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=170, y=0, w=80, d=8, z=2, h=8, r=4, explode=[60, -110, 0], mass=60, materials=[['pvc', 90], ['pp', 10]],
         info='Etwa 1 m PVC-Mantel mit Schutzkontaktstecker. Längs aufschlitzen, um Kupfer und PVC zu trennen.',
         color='#2E3338', marks=[mark('box', 0, 1, 10, 6, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=170, y=2.5, w=80, d=3, z=4.5, h=3, r=1, explode=[60, -135, 0], mass=30,
         info='Drei Kupferadern (Phase, Neutralleiter, Schutzleiter). Wertvollster Rohstoff des Toasters nach Gewicht.',
         color='#B87333'),
]

innen = [p for p in teile if p['id'] != 'mantel']
explodiere(innen, abstand=35, fest=('bodenplatte',))
# Heizplatten auffächern: hintere nach hinten oben, vordere nach vorne, damit alle drei sichtbar sind
for pid, dy, dz in (('heizplatte_hinten', -55, 30), ('heizplatte_vorne', 55, -15), ('feder', -70, 60)):
    q = next(p for p in teile if p['id'] == pid)
    q['explode'] = [0, dy, q['explode'][2] + dz]
oben = max(p['z'] + p['h'] + p['explode'][2] for p in innen if p['explode'][:2] == [0, 0])
teile[0]['explode'] = [0, -230, round(oben + 40 - teile[0]['z'], 1)]  # Mantel nach hinten oben abziehen
skaliere_masse(teile, oid='toaster')
schreibe('toaster', teile)
