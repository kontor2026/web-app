"""3D-Modell: sunglasses. Erzeugt tools/kategorien/modelle/sunglasses.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Zusammengeklappte Sonnenbrille, auf den Bügeln liegend, Gläser oben. x = Breite (140 mm), y = Glashöhe
# (y = 0 Oberkante/Stirn), z = Höhe. Die Front ist gebogen: Mitte oben, Scharnierbacken außen tiefer.
# Front aus zwei ovalen Glasrändern mit Steg, Scharnierbacken außen. Bügel liegen eingeklappt übereinander unter der
# Front. Explodiert: Ebenen nach oben, Schrauben zur Seite, Nasenpads nach vorne.
RAHMEN = '#2A2E31'
GLAS = '#3D3A2C'
STAHL = '#B8BEC4'

teile = [
    teil('glas_l', 'tinted_lenses', 'Brillenglas links', 'Glas links', 'cyl',
         x=10, y=5, w=54, d=40, z=36.5, h=2.5, mass=4.5, sortBias=1,
         info='Getöntes Polycarbonat mit UV-Filter, oft zusätzlich verspiegelt. Von innen aus der Fassung drücken.',
         color=GLAS, opacity=0.75, marks=[mark('cyl', 8, 5, 20, 9, fill='#6E6A55')]),
    teil('glas_r', 'tinted_lenses', 'Brillenglas rechts', 'Glas rechts', 'cyl',
         x=76, y=5, w=54, d=40, z=36.5, h=2.5, mass=4.5, label=False, sortBias=1,
         info='Gegenstück zum linken Glas.',
         color=GLAS, opacity=0.75, marks=[mark('cyl', 26, 5, 20, 9, fill='#6E6A55')]),
    teil('rand_l', 'plastic_frame', 'Brillenfassung (Front)', 'Fassung', 'cyl',
         x=6, y=1, w=62, d=48, z=33, h=6, mass=4,
         info='Front aus Kunststoff (Polycarbonat oder Nylon), die beiden Ränder halten die Gläser in einer Nut. '
              'Ohne Gläser und Schrauben ist sie sortenrein, aber zu klein für die Gelbe Tonne.',
         color=RAHMEN, marks=[mark('cyl', 4, 4, 54, 40, fill='#1C1F21')]),
    teil('rand_r', 'plastic_frame', 'Brillenfassung rechts', 'Fassung', 'cyl',
         x=72, y=1, w=62, d=48, z=33, h=6, mass=4, label=False,
         info='Rechter Glasrand, mit dem linken über den Steg in einem Stück gespritzt.',
         color=RAHMEN, marks=[mark('cyl', 4, 4, 54, 40, fill='#1C1F21')]),
    teil('steg', 'plastic_frame', 'Nasensteg', 'Steg', 'box',
         x=60, y=6, w=20, d=10, z=27, h=6, r=2, mass=0.8, explode=[0, -20, 100],
         info='Brücke zwischen den Gläsern, liegt auf der Nase. Bricht die Brille, dann meist hier.',
         color=RAHMEN, marks=[mark('box', 2, 3, 10, 3, 1.5, '#3A3F44')]),
    teil('backe_l', 'plastic_frame', 'Scharnierbacke links', 'Backe', 'box',
         x=0, y=12, w=11, d=14, z=10, h=23, r=3, mass=1.2, label=False,
         info='Seitlicher Fortsatz der Fassung, in dem die Scharnierhälfte eingeschmolzen ist.',
         color=RAHMEN),
    teil('backe_r', 'plastic_frame', 'Scharnierbacke rechts', 'Backe', 'box',
         x=129, y=12, w=11, d=14, z=10, h=23, r=3, mass=1.2,
         info='Seitlicher Fortsatz der Fassung mit eingeschmolzener Metall-Scharnierhälfte.',
         color=RAHMEN),
    teil('nasenpad_l', 'plastic_frame', 'Nasenauflage links', 'Nasenpads', 'cyl', material_id='silicone',
         x=55, y=24, w=8, d=14, z=26, h=6, explode=[0, 45, 0], mass=0.3, materials=[['gummi', 100]],
         info='Weiche Silikonpolster hinter dem Steg. Sie verhindern, dass die Brille rutscht und drückt.',
         color='#D5D9DC', opacity=0.85, marks=[mark('cyl', 2, 2, 4, 10, fill='#E8ECEE')]),
    teil('nasenpad_r', 'plastic_frame', 'Nasenauflage rechts', 'Nasenpads', 'cyl', material_id='silicone',
         x=77, y=24, w=8, d=14, z=26, h=6, explode=[0, 45, 0], mass=0.3, materials=[['gummi', 100]], label=False,
         info='Gegenstück zum linken Nasenpad.',
         color='#D5D9DC', opacity=0.85, marks=[mark('cyl', 2, 2, 4, 10, fill='#E8ECEE')]),
    teil('schraube_l', 'hinge_screws', 'Scharnierschraube links', 'Schraube', 'cyl',
         x=4, y=17, w=3, z=4, h=6, explode=[-30, 0, 0], mass=0.15, label=False,
         info='Gegenstück zur rechten Schraube.', color=STAHL, marks=[mark('box', 0.4, 1.2, 2.2, 0.6, 0, '#5A6268')]),
    teil('schraube_r', 'hinge_screws', 'Scharnierschraube rechts', 'Schraube', 'cyl',
         x=133, y=17, w=3, z=4, h=6, explode=[30, 0, 0], mass=0.15,
         info='Winzige Edelstahlschraube, verbindet Fassung und Bügel. Mit einem Feinmechaniker-Schraubendreher lösen; '
              'geht sie verloren, gibt es Ersatz beim Optiker.',
         color=STAHL, marks=[mark('box', 0.4, 1.2, 2.2, 0.6, 0, '#5A6268')]),
    teil('scharnier_l', 'hinge_screws', 'Scharnier links', 'Scharnier', 'box',
         x=1, y=13, w=9, d=12, z=6, h=4, r=1, mass=0.4, label=False,
         info='Gegenstück zum rechten Scharnier.', color='#8E969A', marks=[mark('cyl', 3, 4, 3, fill='#5A6268')]),
    teil('scharnier_r', 'hinge_screws', 'Scharnier rechts', 'Scharnier', 'box',
         x=130, y=13, w=9, d=12, z=6, h=4, r=1, mass=0.4,
         info='Metallgelenk aus Neusilber oder Stahl, eine Hälfte in der Backe, eine im Bügel. '
              'Es ist eingeschmolzen und lässt sich nur mit einer Zange herausbrechen.',
         color='#8E969A', marks=[mark('cyl', 3, 4, 3, fill='#5A6268')]),
    teil('buegel_l', 'plastic_frame', 'Bügel links (eingeklappt)', 'Bügel', 'box',
         x=8, y=18, w=104, d=10, z=5, h=4, r=3, mass=3.5,
         info='Bügel mit Federscharnier. Nach dem Lösen der Schraube lässt er sich abziehen.',
         color=RAHMEN, marks=[mark('box', 10, 3, 40, 4, 2, '#3A3F44')]),
    teil('buegelende_l', 'plastic_frame', 'Bügelende links', 'Bügelende', 'box', material_id='rubber',
         x=112, y=17, w=22, d=13, z=5, h=4, r=4, mass=0.8, materials=[['tpe', 100]],
         info='Weiche, nach unten gebogene Spitze hinter dem Ohr. Weicher Kunststoff, aufgesteckt.',
         color='#3A3F44'),
    teil('buegel_r', 'plastic_frame', 'Bügel rechts (eingeklappt)', 'Bügel', 'box',
         x=28, y=18, w=104, d=10, z=1, h=4, r=3, mass=3.5, label=False,
         info='Liegt eingeklappt unter dem linken Bügel.',
         color=RAHMEN, marks=[mark('box', 54, 3, 40, 4, 2, '#3A3F44')]),
    teil('buegelende_r', 'plastic_frame', 'Bügelende rechts', 'Bügelende', 'box', material_id='rubber',
         x=6, y=17, w=22, d=13, z=1, h=4, r=4, mass=0.8, materials=[['tpe', 100]], label=False,
         info='Gegenstück zum linken Bügelende.', color='#3A3F44'),
]

explodiere(teile, abstand=16, gruppen=[['glas_l', 'glas_r'], ['rand_l', 'rand_r', 'steg', 'backe_l', 'backe_r'],
                                       ['scharnier_l', 'scharnier_r'], ['buegel_l', 'buegelende_l'],
                                       ['buegel_r', 'buegelende_r']], nach_liste=True)
skaliere_masse(teile, oid='sunglasses', stellen=2)
schreibe('sunglasses', teile)
