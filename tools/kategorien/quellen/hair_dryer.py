"""3D-Modell: hair_dryer. Erzeugt tools/kategorien/modelle/hair_dryer.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Föhn steht auf dem Griff: Lauf (Luftweg) waagerecht entlang x oben, hinten (x = 0) Ansauggitter,
# vorne (x = 230) Düse. Griff unten, Kabel kommt unten aus dem Griff.
# Explosion: Unterschale und Griff bleiben, Innenleben schwebt darüber, Oberschale ganz oben,
# Ansauggitter nach hinten (dx < 0), Düse nach vorne, Kabel seitlich (dx > 0).

teile = [
    teil('oberschale', 'plastic_housing', 'Gehäuse-Oberschale', 'Oberschale', 'box',
         x=8, y=0, w=192, d=90, z=175, h=45, r=40, mass=70,
         info='Obere Hälfte des Laufs aus hitzefestem Kunststoff. Schrauben sitzen oft unter dem Typenschild oder im Griff.',
         color='#3C4248', marks=[mark('box', 150, 25, 30, 40, 8, fill='#2E3338')]),
    teil('thermoschutz', 'heating_element', 'Überhitzungsschutz (Bimetall)', 'Bimetall', 'box', material_id='steel',
         x=160, y=38, w=12, d=14, z=166, h=6, r=1, mass=3, materials=[['bimetall', 60], ['kupfer', 30], ['pcabs', 10]],
         info='Zwei verschweißte Metallstreifen biegen sich bei Hitze und schalten die Heizung ab. Schützt vor Brand, wenn das Gitter verstopft ist.',
         color='#B8BEC4'),
    teil('heizelement', 'heating_element', 'Heizdraht auf Glimmerträger', 'Heizelement', 'box',
         x=72, y=15, w=84, d=60, z=145, h=60, r=26, mass=45, materials=[['nichrom', 55], ['glimmer', 45]],
         info='Gewendelter Nickel-Chrom-Draht auf einem Kreuz aus Glimmer, glüht mit bis zu 2000 Watt. Vor dem Öffnen ganz abkühlen lassen.',
         color='#8C7B6B', marks=raster(4, 6, 10, 1, 4, 48, 8, r=1, fill='#C4672D')),
    teil('motor', 'electric_motor', 'Gleichstrommotor mit Gleichrichter', 'Motor', 'box',
         x=34, y=28, w=32, d=34, z=158, h=34, r=14, mass=60,
         materials=[['kupfer', 30], ['stahl', 40], ['ferrit', 15], ['chip', 5], ['pcabs', 10]],
         info='Kleiner Motor mit Kupferwicklung und Ferritmagneten, davor Dioden, die den Wechselstrom gleichrichten. Steckt in einer Gummihalterung.',
         marks=[mark('box', 4, 4, 24, 26, 10, fill='#B87333'), mark('cyl', 12, 13, 8, fill='#9AA2A6')]),
    teil('luefterrad', 'electric_motor', 'Lüfterrad', 'Lüfterrad', 'box', material_id='pc',
         x=16, y=10, w=12, d=70, z=140, h=70, r=5, mass=10, materials=[['pcabs', 100]],
         info='Saugt die Luft hinten an und drückt sie über den Heizdraht. Sitzt auf der Motorwelle und lässt sich abziehen.',
         color='#5F6B75', marks=raster(2, 4, 1, 8, 8, 4, 0, 8, r=1, fill='#4A545C')),
    teil('ansauggitter', 'plastic_housing', 'Ansauggitter mit Flusensieb', 'Ansauggitter', 'box',
         x=0, y=5, w=8, d=80, z=135, h=80, r=3, explode=[-35, 0, 0], mass=12, materials=[['pcabs', 80], ['stahl', 20]],
         info='Abnehmbares Gitter mit feinem Metallsieb. Regelmäßig von Haaren befreien, sonst überhitzt der Föhn.',
         color='#2E3338', marks=raster(2, 6, 1, 10, 4, 4, 0, 7, r=1, fill='#1E2226')),
    teil('duese', 'plastic_housing', 'Stylingdüse', 'Düse', 'box',
         x=200, y=15, w=30, d=60, z=150, h=60, r=8, explode=[40, 0, 0], mass=25,
         info='Bündelt den Luftstrom. Nur aufgesteckt und schnell abgezogen; sie ist reiner Kunststoff.',
         color='#3C4248', marks=[mark('box', 20, 22, 9, 16, 3, fill='#1E2226')]),
    teil('unterschale', 'plastic_housing', 'Gehäuse-Unterschale', 'Unterschale', 'box',
         x=8, y=0, w=192, d=90, z=130, h=45, r=40, mass=70,
         info='Untere Hälfte des Laufs, trägt Motor und Heizelement. Die Schalen sind verschraubt und zusätzlich verclipst.',
         color='#3C4248'),
    teil('schalter', 'plastic_housing', 'Stufenschalter', 'Schalter', 'box', material_id='mixed_electronics',
         x=60, y=62, w=14, d=6, z=70, h=36, r=2, explode=[0, 30, 0], mass=8,
         materials=[['pcabs', 55], ['kupfer', 25], ['kontakte', 10], ['stahl', 10]],
         info='Schiebeschalter für Gebläse- und Heizstufen mit Messing-Kontakten. Kabel sind angelötet oder gesteckt.',
         color='#9AA2A6', marks=[mark('box', 2, 1, 10, 4, 1, fill='#E0E4E7')]),
    teil('griff', 'plastic_housing', 'Griff', 'Griff', 'box',
         x=45, y=25, w=44, d=37, z=0, h=130, r=16, mass=55,
         info='Hohler Griff, durch den das Kabel zum Schalter läuft. Unten sitzt der Knickschutz und eine Aufhängeöse.',
         color='#3C4248', marks=[mark('cyl', 14, 10, 16, 16, fill='#2E3338')]),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=89, y=39, w=80, d=9, z=2, h=9, r=4, explode=[60, 0, 0], mass=70, materials=[['pvc', 90], ['pp', 10]],
         info='1,8 m Gummi- oder PVC-Mantel mit Stecker. Mit einem Kabelschäler längs aufschlitzen, um die Kupferadern freizulegen.',
         color='#2E3338', marks=[mark('box', 70, 1, 10, 7, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=89, y=42, w=80, d=3, z=5, h=3, r=1, explode=[60, 0, 20], mass=25,
         info='Zwei Adern aus feinen Kupferlitzen. Kupfer lässt sich fast verlustfrei wiederverwerten.',
         color='#B87333'),
]

explodiere(teile, abstand=25, fest=('unterschale', 'griff'))
skaliere_masse(teile, oid='hair_dryer')
schreibe('hair_dryer', teile)
