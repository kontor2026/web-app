"""3D-Modell: electric_kettle. Erzeugt tools/kategorien/modelle/electric_kettle.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Edelstahl-Wasserkocher (1,7 l) auf Sockel: Kanne Ø 160 mm aus drei Zylinderabschnitten, Ausguss links (x klein),
# Griff rechts (x 170..220). Explosion von unten nach oben: Sockel bleibt, darüber Bodenabdeckung, Thermostat,
# Heizelement, dann die Kanne als Ganzes, Deckel ganz oben. Griff und Kabel seitlich (dx > 0), Kalkfilter nach links.
GAP = 20

teile = [
    teil('deckel', 'stainless_steel_body', 'Klappdeckel', 'Deckel', 'cyl',
         x=40, y=30, w=100, z=236, h=12, mass=70, materials=[['stahl', 55], ['pp', 40], ['gummi', 5]],
         info='Edelstahlscheibe in Kunststoffrahmen mit Silikondichtung. Das Scharnier hat eine kleine Stahlfeder.',
         color='#C9CED2', marks=[mark('cyl', 10, 10, 80, fill='#B5BBC0'), mark('box', 70, 40, 24, 20, 6, fill='#2E3338')]),
    teil('kalkfilter', 'stainless_steel_body', 'Kalkfilter', 'Kalkfilter', 'box', material_id='nylon',
         x=20, y=70, w=6, d=20, z=188, h=36, r=1, explode=[-45, 0, 0], mass=4, materials=[['nylon', 70], ['pp', 30]],
         info='Feines Kunststoffnetz im Ausguss, hält Kalkflocken zurück. Nach oben herausziehen und ausspülen.',
         color='#E9EEF2', opacity=0.8),
    teil('ausguss', 'stainless_steel_body', 'Ausguss', 'Ausguss', 'box',
         x=4, y=70, w=16, d=20, z=186, h=42, r=6, mass=25,
         info='Angeschweißte Tülle aus Edelstahl. Gehört zur Kanne und kommt mit ihr in den Metallschrott.',
         color='#C9CED2'),
    teil('kanne_oben', 'stainless_steel_body', 'Kanne Oberteil', 'Kanne oben', 'cyl',
         x=20, y=10, w=140, z=180, h=56, mass=150,
         info='Oberer, schmaler Teil der tiefgezogenen Edelstahlkanne. Edelstahl enthält Chrom und Nickel und wird eingeschmolzen.',
         color='#C9CED2', marks=[mark('cyl', 20, 20, 100, fill='#9AA2A6')]),
    teil('kanne_mitte', 'stainless_steel_body', 'Kanne Mittelteil', 'Kanne Mitte', 'cyl',
         x=15, y=5, w=150, z=105, h=75, mass=180,
         info='Mittlerer Teil der Kanne mit eingesetzter Wasserstandsanzeige aus Kunststoff.',
         color='#C9CED2'),
    teil('kanne_unten', 'stainless_steel_body', 'Kanne Unterteil', 'Kanne unten', 'cyl',
         x=10, y=0, w=160, z=28, h=77, mass=200, materials=[['stahl', 92], ['pp', 8]],
         info='Breiter Fuß der Kanne mit Kunststoffring unten. Der Boden ist dicht mit der Heizplatte verlötet.',
         color='#C9CED2'),
    teil('griff', 'plastic_handle', 'Griff', 'Griff', 'box',
         x=170, y=65, w=50, d=30, z=62, h=168, r=12, mass=70,
         info='Hohler Kunststoffgriff, oben und unten mit je einer Schraube an der Kanne befestigt.',
         color='#2E3338', marks=[mark('box', 12, 6, 30, 18, 8, fill='#1E2226')]),
    teil('schalter', 'thermostat', 'Ein-/Aus-Schalter mit Leuchte', 'Schalter', 'box',
         x=172, y=68, w=36, d=24, z=48, h=12, r=4, mass=8, materials=[['pcabs', 60], ['kupfer', 20], ['led', 10], ['kontakte', 10]],
         info='Kippschalter mit Kontrolllampe. Eine Schubstange verbindet ihn mit dem Thermostat im Boden.',
         color='#2E3338', marks=[mark('box', 6, 6, 14, 12, 3, fill='#5DADE2')]),
    teil('thermostat', 'thermostat', 'Thermostat mit Bimetall', 'Thermostat', 'box',
         x=125, y=60, w=40, d=40, z=19, h=8, r=4, mass=25,
         materials=[['bimetall', 35], ['kupfer', 20], ['kontakte', 10], ['pcabs', 35]],
         info='Eine Bimetallscheibe schnappt um, wenn Dampf sie erhitzt, und schaltet ab. Ein zweites Bimetall schützt vor Trockengehen.',
         color='#9AA2A6', marks=[mark('cyl', 10, 10, 20, fill='#B8BEC4'), mark('box', 2, 30, 36, 6, 1, fill='#B87333')]),
    teil('heizelement', 'heating_element', 'Rohrheizkörper mit Wärmeleitplatte', 'Heizelement', 'cyl',
         x=20, y=5, w=140, d=150, z=20, h=8, mass=160, materials=[['alu', 45], ['stahl', 30], ['nichrom', 10], ['keramik', 15]],
         info='Ein Stahlrohr mit Heizdraht in Keramikpulver, angelötet an eine Aluplatte unter dem Kannenboden. Nicht zerlegbar, kommt komplett ins Metallrecycling.',
         color='#B5BBC0', marks=[mark('cyl', 15, 15, 110, 120, fill='#C4672D'), mark('cyl', 23, 23, 94, 104, fill='#B5BBC0')]),
    teil('bodenabdeckung', 'plastic_handle', 'Bodenabdeckung', 'Boden', 'cyl', material_id='pp',
         x=12, y=2, w=156, z=14, h=5, mass=45,
         info='Kunststoffdeckel unter der Kanne mit dem Steckkontakt in der Mitte. Mit Sicherheitsschrauben befestigt.',
         color='#2E3338', marks=[mark('cyl', 63, 63, 30, fill='#1E2226')]),
    teil('sockel', 'cable_insulation', 'Sockel mit Steckkontakt', 'Sockel', 'cyl', material_id='pp',
         x=10, y=0, w=160, z=0, h=14, mass=110, materials=[['pp', 75], ['kupfer', 10], ['kontakte', 10], ['stahl', 5]],
         info='Die Kanne steht drehbar auf diesem Sockel; der Mittelkontakt leitet den Strom weiter. Darunter ist das Kabel aufgewickelt.',
         color='#2E3338', marks=[mark('cyl', 65, 65, 30, fill='#9AA2A6'), mark('cyl', 75, 75, 10, fill='#1E2226')]),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=120, y=76, w=70, d=8, z=3, h=8, r=4, explode=[80, 0, 0], mass=60, materials=[['pvc', 90], ['pp', 10]],
         info='Etwa 75 cm PVC-Mantel mit Stecker. Längs aufschlitzen, um die Kupferadern freizulegen.',
         color='#2E3338', marks=[mark('box', 60, 1, 10, 6, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=120, y=78.5, w=70, d=3, z=5.5, h=3, r=1, explode=[80, 0, 15], mass=30,
         info='Drei Kupferadern für bis zu 3000 Watt, deshalb dicker als bei kleinen Geräten.',
         color='#B87333'),
]

KANNE = ('deckel', 'kalkfilter', 'ausguss', 'kanne_oben', 'kanne_mitte', 'kanne_unten', 'griff', 'schalter')
unten = [p for p in teile if p['id'] not in KANNE]
explodiere(unten, abstand=GAP, fest=('sockel',))
top = max(p['z'] + p['h'] + p['explode'][2] for p in unten if p['explode'][:2] == [0, 0])
dz = round(top + GAP - 28, 1)  # Kanne als Ganzes über den Bodenteilen
for p in teile:
    if p['id'] in ('ausguss', 'kanne_oben', 'kanne_mitte', 'kanne_unten'):
        p['explode'] = [0, 0, dz]
    elif p['id'] in ('griff', 'schalter'):
        p['explode'] = [50, 0, dz]
    elif p['id'] == 'kalkfilter':
        p['explode'] = [-45, 0, dz]
explodiere(teile, abstand=GAP)  # Deckel über die Kanne
skaliere_masse(teile, oid='electric_kettle')
schreibe('electric_kettle', teile)
