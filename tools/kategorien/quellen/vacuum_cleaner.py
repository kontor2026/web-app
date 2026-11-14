"""3D-Modell: vacuum_cleaner. Erzeugt tools/kategorien/modelle/vacuum_cleaner.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Bodenstaubsauger, Saugöffnung vorne (y = 400), Abluft hinten (y = 0). Große Räder links und rechts (x 0..25, 275..300),
# Lenkrolle vorne unten. Hinten links Kabeltrommel, hinten rechts Motor, vorne Staubraum mit Beutel und Motorschutzfilter.
# Explosion: Unterschale und Lenkrolle bleiben, Innenleben schwebt darüber, Oberschale und Staubraumdeckel ganz oben.
# Räder seitlich, Abluftfilter nach hinten, Schlauch nach vorne, Kabel nach rechts (dx > 0).
# Der Schlauch ist nur als Anschlussstück mit kurzem Schlauchstück dargestellt.

def rad(seite, x, dx):
    return teil(f'rad_{seite}', 'plastic_housing', f'Laufrad {seite}', f'Rad {seite}', 'box', material_id='pp',
                x=x, y=20, w=25, d=180, z=0, h=180, r=8, explode=[dx, 0, 0], form='liegend_x', mass=150, materials=[['pp', 85], ['gummi', 10], ['stahl', 5]],
                info='Großes Kunststoffrad mit Gummilauffläche auf einer Stahlachse. Abhebeln und zum Kunststoff geben.',
                color='#2E3338', label=seite == 'links', marks=[mark('box', 4, 70, 17, 40, 4, fill='#9AA2A6')])


teile = [
    teil('deckel', 'plastic_housing', 'Staubraumdeckel mit Tragegriff', 'Deckel', 'box',
         x=40, y=200, w=220, d=195, z=205, h=65, r=50, mass=250,
         info='Klappdeckel über dem Staubbeutel mit Tragegriff und Beutelfüllanzeige. Am Scharnier hinten aushaken.',
         color='#C0392B', marks=[mark('box', 80, 40, 60, 110, 20, fill='#922B21'), mark('cyl', 95, 165, 30, fill='#2E3338')]),
    teil('oberschale', 'plastic_housing', 'Gehäuse-Oberschale', 'Oberschale', 'box',
         x=25, y=0, w=250, d=400, z=130, h=100, r=60, mass=700,
         info='Obere Gehäusehälfte mit Ein-Taste, Kabeltaste und Leistungsregler. Schrauben sitzen unten am Gehäuse.',
         color='#C0392B', marks=[mark('cyl', 30, 50, 40, fill='#2E3338'), mark('cyl', 180, 50, 40, fill='#2E3338'),
                                 mark('box', 40, 10, 170, 20, 6, fill='#922B21')]),
    teil('staubbeutel', 'dust_bag', 'Staubbeutel', 'Staubbeutel', 'box',
         x=50, y=215, w=200, d=170, z=45, h=145, r=20, mass=120, materials=[['papier', 80], ['polyester', 15], ['pcabs', 5]],
         info='Mehrlagiger Beutel aus Papier oder Vlies mit Kunststoffplatte. Voll in den Restmüll, gebrauchte Beutel sind nicht recycelbar.',
         color='#E8DCC0', marks=[mark('box', 70, 140, 60, 25, 4, fill='#3C4248'), mark('cyl', 85, 145, 30, 15, fill='#1E2226')]),
    teil('motorschutzfilter', 'hepa_filter', 'Motorschutzfilter', 'Motorfilter', 'box',
         x=50, y=198, w=200, d=12, z=50, h=140, r=3, mass=30, materials=[['polyester', 70], ['pp', 30]],
         info='Vlies im Kunststoffrahmen, schützt den Motor vor Staub. Über dem Mülleimer ausklopfen; verstaubt in den Restmüll.',
         color='#F2F4F5', marks=raster(4, 2, 24, 1, 4, 8, 8, r=1, fill='#D5DADE')),
    teil('motor', 'electric_motor', 'Saugmotor', 'Motor', 'cyl',
         x=140, y=40, w=130, z=30, h=130, mass=1400,
         materials=[['stahl', 45], ['kupfer', 25], ['alu', 10], ['pcabs', 15], ['graphit', 5]],
         info='Schnell drehender Motor mit Kupferwicklung, Kohlebürsten und Lüfterrad aus Aluminium. Sitzt in Gummilagern, die Kabel sind gesteckt.',
         color='#C3C8CC', marks=[mark('cyl', 15, 15, 100, fill='#B87333'), mark('cyl', 45, 45, 40, fill='#9AA2A6')]),
    teil('kabeltrommel', 'cable_insulation', 'Kabeltrommel', 'Kabeltrommel', 'cyl', material_id='pp',
         x=35, y=30, w=95, z=40, h=70, mass=350, materials=[['pp', 80], ['stahl', 15], ['kupfer', 5]],
         info='Rolle mit Federmotor, die das Kabel aufwickelt. Vorsicht: Die gespannte Stahlfeder kann herausschnellen.',
         color='#3C4248', marks=[mark('cyl', 10, 10, 75, fill='#2E3338'), mark('cyl', 37, 37, 21, fill='#B87333')]),
    teil('unterschale', 'plastic_housing', 'Gehäuse-Unterschale', 'Unterschale', 'box',
         x=25, y=0, w=250, d=400, z=20, h=110, r=60, mass=900,
         info='Tragendes Unterteil, in dem Motor, Kabeltrommel und Staubraum sitzen. Kommt zum Kunststoff, wenn alles ausgebaut ist.',
         color='#3C4248', marks=[mark('box', 25, 200, 200, 190, 40, fill='#2E3338')]),
    teil('lenkrolle', 'plastic_housing', 'Lenkrolle', 'Lenkrolle', 'cyl', material_id='pp',
         x=130, y=330, w=40, z=0, h=20, mass=40, materials=[['pp', 80], ['stahl', 20]],
         info='Drehbare Rolle vorne unter dem Gerät. Aus dem Boden herausziehen.',
         color='#2E3338'),
    rad('links', 0, -50),
    rad('rechts', 275, 50),
    teil('abluftfilter', 'hepa_filter', 'HEPA-Abluftfilter', 'HEPA-Filter', 'box',
         x=150, y=0, w=110, d=12, z=40, h=120, r=3, explode=[0, -60, 0], mass=60, materials=[['polyester', 60], ['pp', 40]],
         info='Gefaltetes Feinstaubvlies hinten am Luftauslass. Ausklopfen; verbrauchte Filter gehören in den Restmüll.',
         color='#F2F4F5', marks=raster(5, 2, 13, 1, 3, 8, 8, r=1, fill='#D5DADE')),
    teil('schlauch', 'vacuum_hose', 'Saugschlauch mit Anschlussstück', 'Schlauch', 'box',
         x=125, y=380, w=50, d=50, z=140, h=50, r=20, explode=[0, 80, 0], mass=450,
         info='Gerippter Kunststoffschlauch (etwa 1,8 m, hier verkürzt) mit Drehanschluss. Drehen und abziehen; ohne Metallspirale gehört er zum Kunststoff.',
         color='#5A6670', wand=5, boden=0, marks=[mark('cyl', 10, 10, 30, fill='#1E2226', zeichnung=True)]),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=150, y=210, w=100, d=8, z=30, h=8, r=4, explode=[180, 0, 0], form='liegend_x', mass=350, materials=[['pvc', 90], ['pp', 10]],
         info='Etwa 7 m PVC-Kabel auf der Trommel. Am Stecker herausziehen und längs aufschlitzen, um die Kupferadern freizulegen.',
         color='#2E3338', marks=[mark('box', 90, 1, 10, 6, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=150, y=212.5, w=100, d=3, z=32.5, h=3, r=1, explode=[180, 0, 15], form='liegend_x', mass=250,
         info='Zwei Kupferadern über die ganze Kabellänge. Kupfer lässt sich fast verlustfrei wiederverwerten.',
         color='#B87333'),
]

explodiere(teile, abstand=30, fest=('unterschale', 'lenkrolle'))
skaliere_masse(teile, oid='vacuum_cleaner')
for p in teile:  # gerundete Formen (form): marks nur in der Zeichnung, oben flach würden sie schweben
    if p.get('form'):
        p['marks'] = [dict(m, zeichnung=True) for m in p.get('marks') or []]
schreibe('vacuum_cleaner', teile)
