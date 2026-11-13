"""3D-Modell: sunglasses. Erzeugt tools/kategorien/modelle/sunglasses.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Zusammengeklappte Sonnenbrille, auf den Bügeln liegend, Gläser oben. x = Breite (140 mm), y = Glashöhe
# (y = 0 Oberkante/Stirn), z = Höhe. Die Front ist gebogen: Mitte oben, Scharnierbacken außen tiefer.
# Bügel liegen eingeklappt übereinander unter der Front. Explodiert: Ebenen nach oben, Schrauben zur Seite.
RAHMEN = '#2A2E31'
GLAS = '#3D3A2C'

teile = [
    teil('glas_l', 'tinted_lenses', 'Brillenglas links', 'Glas links', 'cyl',
         x=8, y=4, w=58, d=42, z=34, h=2.5, mass=4.5,
         info='Getöntes Polycarbonat mit UV-Filter, oft zusätzlich verspiegelt. Von innen aus der Fassung drücken.',
         color=GLAS, opacity=0.7, marks=[mark('cyl', 8, 6, 22, 10, fill='#6E6A55')]),
    teil('glas_r', 'tinted_lenses', 'Brillenglas rechts', 'Glas rechts', 'cyl',
         x=74, y=4, w=58, d=42, z=34, h=2.5, mass=4.5, label=False,
         info='Gegenstück zum linken Glas.',
         color=GLAS, opacity=0.7, marks=[mark('cyl', 28, 6, 22, 10, fill='#6E6A55')]),
    teil('rahmen', 'plastic_frame', 'Brillenfassung (Front)', 'Fassung', 'box',
         x=0, y=0, w=140, d=50, z=33, h=7, r=14, mass=9,
         info='Front aus Kunststoff (Polycarbonat oder Nylon) mit Steg über der Nase. '
              'Ohne Gläser und Schrauben ist sie sortenrein, aber zu klein für die Gelbe Tonne.',
         color=RAHMEN, marks=[mark('cyl', 8, 4, 58, 42, fill=GLAS), mark('cyl', 74, 4, 58, 42, fill=GLAS)]),
    teil('backe_l', 'plastic_frame', 'Scharnierbacke links', 'Backe', 'box',
         x=0, y=12, w=9, d=20, z=10, h=23, r=2, mass=1.5,
         info='Seitlicher Fortsatz der Fassung mit eingeschmolzenem Metallscharnier.',
         color=RAHMEN, marks=[mark('box', 2, 4, 5, 12, 1, '#8E969A')]),
    teil('backe_r', 'plastic_frame', 'Scharnierbacke rechts', 'Backe', 'box',
         x=131, y=12, w=9, d=20, z=10, h=23, r=2, mass=1.5, label=False,
         info='Gegenstück zur linken Scharnierbacke.',
         color=RAHMEN, marks=[mark('box', 2, 4, 5, 12, 1, '#8E969A')]),
    teil('nasenpads', 'plastic_frame', 'Nasenauflagen', 'Nasenpads', 'box', material_id='silicone',
         x=61, y=24, w=18, d=16, z=22, h=11, r=3, mass=0.6, materials=[['gummi', 100]],
         info='Weiche Silikonpolster am Steg. Sie verhindern, dass die Brille rutscht.',
         color='#C9CDD0', opacity=0.85, marks=[mark('box', 1, 2, 5, 12, 2), mark('box', 12, 2, 5, 12, 2)]),
    teil('schraube_l', 'hinge_screws', 'Scharnierschraube links', 'Schraube', 'box',
         x=3, y=10, w=3, d=6, z=6, h=3, r=1, explode=[-25, 0, 0], mass=0.15,
         info='Winzige Edelstahlschraube, verbindet Fassung und Bügel. Mit einem Feinmechaniker-Schraubendreher lösen; '
              'geht sie verloren, gibt es Ersatz beim Optiker.',
         color='#B8BEC4', marks=[mark('box', 1, 1, 1, 4, 0, '#5A6268')]),
    teil('schraube_r', 'hinge_screws', 'Scharnierschraube rechts', 'Schraube', 'box',
         x=134, y=10, w=3, d=6, z=0, h=3, r=1, explode=[25, 0, 0], mass=0.15, label=False,
         info='Gegenstück zur linken Schraube.', color='#B8BEC4', marks=[mark('box', 1, 1, 1, 4, 0, '#5A6268')]),
    teil('buegel_l', 'plastic_frame', 'Bügel links (eingeklappt)', 'Bügel links', 'box',
         x=4, y=16, w=132, d=12, z=6, h=4, r=3, mass=4,
         info='Bügel mit Federscharnier. Nach dem Lösen der Schraube lässt er sich abziehen.',
         color=RAHMEN, marks=[mark('box', 10, 4, 40, 4, 2, '#3A3F44')]),
    teil('buegelende_l', 'plastic_frame', 'Bügelende links', 'Bügelende', 'box', material_id='rubber',
         x=120, y=28, w=14, d=16, z=6, h=4, r=4, mass=0.8, materials=[['tpe', 100]],
         info='Weiche, nach unten gebogene Spitze hinter dem Ohr. Weicher Kunststoff, aufgesteckt.',
         color='#3A3F44'),
    teil('buegel_r', 'plastic_frame', 'Bügel rechts (eingeklappt)', 'Bügel rechts', 'box',
         x=4, y=16, w=132, d=12, z=0, h=4, r=3, mass=4, label=False,
         info='Liegt eingeklappt unter dem linken Bügel.',
         color=RAHMEN, marks=[mark('box', 82, 4, 40, 4, 2, '#3A3F44')]),
    teil('buegelende_r', 'plastic_frame', 'Bügelende rechts', 'Bügelende', 'box', material_id='rubber',
         x=6, y=28, w=14, d=16, z=0, h=4, r=4, mass=0.8, materials=[['tpe', 100]], label=False,
         info='Gegenstück zum linken Bügelende.', color='#3A3F44'),
]

explodiere(teile, abstand=18, gruppen=[['rahmen', 'backe_l', 'backe_r'], ['buegel_l', 'buegelende_l'],
                                       ['buegel_r', 'buegelende_r']], nach_liste=True)
skaliere_masse(teile, oid='sunglasses', stellen=2)
schreibe('sunglasses', teile)
