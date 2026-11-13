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
         x=0, y=0, w=250, d=160, z=20, h=170, r=22, mass=330,
         info='Ein gebogenes Edelstahlblech mit zwei Brotschlitzen. Nach Lösen der Bodenschrauben nach oben abziehen; Kanten sind scharf.',
         color='#C9CED2', marks=[mark('box', 25, y, 200, 35, 6, fill='#2A2D30') for _, y in SLOT]),
    teil('heizplatte_vorne', 'heating_element', 'Heizplatte vorne', 'Heizplatte vorne', 'box',
         x=25, y=129, w=200, d=4, z=40, h=130, r=0.5, mass=40, materials=[['nichrom', 40], ['glimmer', 60]],
         info='Glimmerplatte, um die ein flaches Nickel-Chrom-Band gewickelt ist. Glüht rot und röstet das Brot von einer Seite.',
         color='#8C7B6B', marks=raster(4, 0.5, 20, 1, 4, 3, 10, r=0.5, fill='#C4672D')),
    teil('heizplatte_mitte', 'heating_element', 'Heizplatte Mitte (doppelseitig)', 'Heizplatte Mitte', 'box',
         x=25, y=77, w=200, d=6, z=40, h=130, r=0.5, mass=55, materials=[['nichrom', 45], ['glimmer', 55]],
         info='Heizt beide Schlitze gleichzeitig, deshalb doppelt bewickelt. Der Draht ist dünn und bricht leicht.',
         color='#8C7B6B', marks=raster(4, 1, 20, 1, 4, 4, 10, r=0.5, fill='#C4672D')),
    teil('heizplatte_hinten', 'heating_element', 'Heizplatte hinten', 'Heizplatte hinten', 'box',
         x=25, y=27, w=200, d=4, z=40, h=130, r=0.5, mass=40, materials=[['nichrom', 40], ['glimmer', 60]],
         info='Wie die vordere Platte. Die Glimmerplatten isolieren den heißen Draht vom Blechgehäuse.',
         color='#8C7B6B', marks=raster(4, 0.5, 20, 1, 4, 3, 10, r=0.5, fill='#C4672D')),
    teil('brotschlitten', 'stainless_steel_body', 'Brotschlitten mit Führungsgittern', 'Brotschlitten', 'box',
         x=25, y=35, w=200, d=90, z=26, h=8, r=2, mass=90,
         info='Verzinktes Stahlgestell, das die Scheiben hebt und senkt. Eine Feder zieht es nach dem Toasten wieder nach oben.',
         color='#9AA2A6', marks=[mark('box', 4, y - 35 + 4, 192, 27, 2, fill='#7C858C') for _, y in SLOT]),
    teil('steuerplatine', 'heating_element', 'Steuerplatine mit Haltemagnet', 'Steuerplatine', 'box', material_id='pcb',
         x=236, y=20, w=12, d=120, z=30, h=110, r=1, mass=35,
         materials=[['fr4', 30], ['kupfer', 30], ['stahl', 25], ['chip', 10], ['lot', 5]],
         info='Zeitschaltung mit Elektromagnet: Er hält den Schlitten unten, bis die Bräunungszeit um ist. Enthält Kupferspule und Lötstellen.',
         color='#2F6B3A', marks=[mark('box', 2, 10, 8, 20, 1, fill='#B87333'), mark('box', 2, 50, 8, 12, 1, fill='#222')]),
    teil('seitenteil', 'stainless_steel_body', 'Seitenteil mit Bedienfeld', 'Seitenteil', 'box', material_id='pp',
         x=250, y=0, w=20, d=160, z=0, h=190, r=8, explode=[60, 0, 0], mass=90, materials=[['pp', 100]],
         info='Hitzefester Kunststoff, trägt Hebelschlitz, Regler und Tasten. Ist eingeclipst und mit zwei Schrauben gesichert.',
         color='#2E3338', marks=[mark('box', 6, 60, 8, 40, 3, fill='#1E2226')]),
    teil('hebel', 'plastic_knobs', 'Absenkhebel', 'Hebel', 'box',
         x=270, y=62, w=12, d=36, z=150, h=14, r=4, explode=[95, 0, 0], mass=8,
         info='Kunststoffgriff auf dem Hebelblech. Gerade abziehen, darunter ist Metall.',
         color='#2E3338'),
    teil('stopptaste', 'plastic_knobs', 'Stopp-Taste', 'Stopp-Taste', 'box',
         x=270, y=112, w=6, d=14, z=100, h=10, r=2, explode=[95, 0, 0], mass=2,
         info='Unterbricht das Toasten sofort. Die Kappe ist nur aufgesteckt.',
         color='#C0392B'),
    teil('drehregler', 'plastic_knobs', 'Bräunungsregler', 'Regler', 'cyl',
         x=270, y=105, w=10, d=28, z=55, h=28, explode=[95, 0, 0], mass=6,
         info='Stellt die Röstzeit von 1 bis 7 ein. Lässt sich von der Achse abziehen.',
         color='#2E3338'),
    teil('kruemelschublade', 'crumb_tray', 'Krümelschublade', 'Krümelschublade', 'box',
         x=20, y=10, w=215, d=145, z=13, h=4, r=2, explode=[0, 175, 0], mass=45,
         info='Aluminiumblech, das herabfallende Krümel auffängt. Nach vorne herausziehen und regelmäßig leeren, sonst kann es brennen.',
         color='#D4D8DB', marks=[mark('box', 90, 137, 35, 8, 2, fill='#2E3338')]),
    teil('bodenplatte', 'stainless_steel_body', 'Bodenplatte mit Füßen', 'Bodenplatte', 'box',
         x=0, y=0, w=250, d=160, z=0, h=12, r=22, mass=220, materials=[['stahl', 85], ['gummi', 5], ['pp', 10]],
         info='Verzinktes Stahlblech mit Gummifüßen und Kabelaufwicklung. Nach dem Ausschrauben liegen Heizplatten und Mechanik frei.',
         color='#7C858C', marks=raster(12, 12, 2, 2, 16, 16, 210, 120, shape='cyl', fill='#2E3338')),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=170, y=0, w=80, d=8, z=2, h=8, r=4, explode=[110, -40, 0], mass=60, materials=[['pvc', 90], ['pp', 10]],
         info='Etwa 1 m PVC-Mantel mit Schutzkontaktstecker. Längs aufschlitzen, um Kupfer und PVC zu trennen.',
         color='#2E3338', marks=[mark('box', 0, 1, 10, 6, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=170, y=2.5, w=80, d=3, z=4.5, h=3, r=1, explode=[110, -65, 0], mass=30,
         info='Drei Kupferadern (Phase, Neutralleiter, Schutzleiter). Wertvollster Rohstoff des Toasters nach Gewicht.',
         color='#B87333'),
]

innen = [p for p in teile if p['id'] != 'mantel']
explodiere(innen, abstand=20, fest=('bodenplatte',))
oben = max(p['z'] + p['h'] + p['explode'][2] for p in innen if p['explode'][:2] == [0, 0])
teile[0]['explode'] = [0, 0, round(oben + 25 - teile[0]['z'], 1)]  # Mantel nach oben abziehen
skaliere_masse(teile, oid='toaster')
schreibe('toaster', teile)
