"""3D-Modell: winter_jacket. Erzeugt tools/kategorien/modelle/winter_jacket.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Gesteppte Winterjacke flach hingelegt, Vorderseite oben, Kragen hinten (y = 0), Saum vorne. 400 × 500 × 80 mm.
# Rumpf 240 mm breit in der Mitte, die Ärmel liegen links und rechts daneben, Strickbündchen an den Enden.
# Explodiert: Ärmel samt Bündchen zur Seite, vorne heben sich Reißverschluss, Obermaterial, Wattierung und Futter
# als Ebenen vom Rückenteil ab, damit man den Schichtaufbau sieht.
HUELLE = '#2E5B4A'
NAHT = '#244A3C'
FUTTER = '#3A3F44'
WATTE = '#F2F0EA'
STRICK = '#22302A'
SCHALE = [['nylon', 100]]
KOMPLETT = [['nylon', 55], ['polyester', 45]]
RV = [['messing', 55], ['polyester', 40], ['stahl', 5]]


def stepp(w, d, y0=30, abstand=62):
    """Steppnähte quer über das Teil: hier sind Außenstoff, Watte und Futter zusammengenäht."""
    return [mark('box', 0, y, w, 2.5, 0, NAHT) for y in range(y0, int(d) - 10, abstand)]


def aermel(seite, x, dx, dy):
    links = seite == 'l'
    return [
        teil(f'aermel_{seite}', 'nylon_fabric', f'Ärmel {"links" if links else "rechts"}', 'Ärmel', 'box',
             x=x, y=60, w=80, d=405, z=0, h=55, r=18, mass=160, materials=KOMPLETT, color=HUELLE, explode=[dx, dy, 0],
             label=links,
             info='Gesteppter Ärmel mit Nylon außen, Polyesterwatte und Futter innen, wie der Rumpf aufgebaut.'
             if links else 'Gegenstück zum linken Ärmel.',
             marks=stepp(80, 405, 40, 62)),
        teil(f'buendchen_{seite}', 'nylon_fabric', 'Strickbündchen', 'Bündchen', 'box', material_id='polyester',
             x=x + 8, y=465, w=64, d=32, z=6, h=42, r=10, mass=12, materials=[['polyester', 95], ['tpu', 5]],
             color=STRICK, explode=[dx, dy, 0], label=links,
             info='Gestricktes Rippenbündchen mit Elasthan, hält die Kälte am Handgelenk draußen. Abschneiden vor dem Recycling.'
             if links else 'Zweites Bündchen.',
             marks=raster(4, 2, 10, 1, 2.5, 28, 6, fill='#1A241F')),
    ]


teile = [
    teil('kragen', 'nylon_fabric', 'Stehkragen mit Fleece', 'Kragen', 'box',
         x=135, y=0, w=130, d=55, z=50, h=30, r=18, mass=45, materials=KOMPLETT, color=HUELLE,
         info='Hochgestellter, wattierter Kragen, innen mit Fleece. In manchen Krägen ist eine Kapuze eingerollt.',
         marks=[mark('box', 8, 24, 114, 2.5, 1, NAHT), mark('box', 10, 4, 110, 14, 6, '#3A4A44')]),
    teil('kordelstopper_1', 'nylon_fabric', 'Kordelstopper', 'Kordelstopper', 'cyl', material_id='pp',
         x=92, y=482, w=12, d=16, z=70, h=6, mass=2, materials=[['pp', 80], ['stahl', 20]], color='#22272B',
         explode=[0, 90, 0],
         info='Klemme aus Kunststoff mit Stahlfeder für die Saumkordel. Vor dem Textilrecycling abschneiden.',
         marks=[mark('cyl', 3, 5, 6, fill='#555C62')]),
    teil('kordelstopper_2', 'nylon_fabric', 'Kordelstopper', 'Kordelstopper', 'cyl', material_id='pp',
         x=296, y=482, w=12, d=16, z=70, h=6, mass=2, materials=[['pp', 80], ['stahl', 20]], color='#22272B',
         explode=[0, 90, 0], label=False, info='Zweiter Kordelstopper auf der anderen Seite.',
         marks=[mark('cyl', 3, 5, 6, fill='#555C62')]),
    teil('taschen_rv_l', 'metal_zipper', 'Taschenreißverschluss', 'Taschen-RV', 'box',
         x=118, y=290, w=8, d=120, z=70, h=1.5, r=1, mass=6, materials=RV, color='#2A2E31',
         info='Kleiner Reißverschluss an der Eingrifftasche. Wie der große mit der Schere am Band entlang heraustrennen.',
         marks=[mark('box', 3, 0, 2, 120, 0, '#C9A24A'), mark('box', 1, 6, 6, 12, 2, '#B7BCC0')]),
    teil('taschen_rv_r', 'metal_zipper', 'Taschenreißverschluss', 'Taschen-RV', 'box',
         x=274, y=290, w=8, d=120, z=70, h=1.5, r=1, mass=6, materials=RV, color='#2A2E31', label=False,
         info='Zweite Eingrifftasche.',
         marks=[mark('box', 3, 0, 2, 120, 0, '#C9A24A'), mark('box', 1, 6, 6, 12, 2, '#B7BCC0')]),
    teil('reissverschluss', 'metal_zipper', 'Reißverschluss mit Schieber', 'Reißverschluss', 'box',
         x=190, y=40, w=20, d=460, z=66, h=6, r=1, mass=35, materials=RV, color='#2A2E31',
         info='Metallzähne auf zwei Polyesterbändern, mit Schieber und Zipper. Rechts und links neben dem Band '
              'abschneiden: Das Metall darf nicht ins Textilrecycling.',
         marks=[mark('box', 8, 0, 4, 460, 0.5, '#C9A24A'), mark('box', 5, 30, 10, 18, 2, '#B7BCC0'),
                mark('box', 8, 48, 4, 22, 1, '#8E969A')]),
    teil('aussen_l', 'nylon_fabric', 'Vorderteil links (Obermaterial)', 'Obermaterial', 'box',
         x=80, y=30, w=113, d=470, z=30, h=40, r=10, mass=60, materials=SCHALE, color=HUELLE,
         info='Wasserabweisendes Nylon-Gewebe, das die Wattierung umschließt und in Kammern abgesteppt ist. '
              'Tragbare Jacken in die Altkleidersammlung.',
         marks=stepp(113, 470) + [mark('box', 70, 60, 26, 14, 3, '#C9D3CE')]),
    teil('aussen_r', 'nylon_fabric', 'Vorderteil rechts (Obermaterial)', 'Obermaterial', 'box',
         x=207, y=30, w=113, d=470, z=30, h=40, r=10, mass=60, materials=SCHALE, color=HUELLE, label=False,
         info='Gegenstück zur linken Vorderseite, mit Eingrifftasche.', marks=stepp(113, 470)),
    teil('wattierung', 'polyester_fill', 'Wattierung', 'Wattierung', 'box',
         x=85, y=35, w=230, d=460, z=30, h=32, r=10, mass=110, color=WATTE,
         info='Polyester-Hohlfasern halten die warme Luft fest. Futter aufschneiden und die Watte als Füllmaterial '
              'für Kissen weiterverwenden.',
         marks=[mark('box', 0, y, 230, 3, 0, '#DCD8CE') for y in range(25, 450, 62)]),
    teil('futter', 'nylon_fabric', 'Innenfutter vorne', 'Futter', 'box',
         x=85, y=35, w=230, d=460, z=26, h=4, r=10, mass=50, materials=[['nylon', 60], ['polyester', 40]], color=FUTTER,
         info='Glattes Futter aus Nylon-Taft, damit die Jacke leicht über den Pullover gleitet. Mit Innentasche.',
         marks=[mark('box', 140, 110, 70, 4, 2, '#2A2E31'), mark('box', 135, 100, 80, 70, 4, '#33383D'),
                mark('box', 140, 110, 70, 4, 2, '#2A2E31')]),
    teil('etikett', 'care_label', 'Pflegeetikett', 'Etikett', 'box',
         x=185, y=40, w=30, d=40, z=25.7, h=0.3, r=1, mass=2, explode=[0, -160, 0], color='#F4F2EE',
         info='Etikett mit Waschsymbolen und Materialangaben, innen am Kragen. Abschneiden: anderes Material.',
         marks=[mark('box', 4, 5, 22, 3, 0, '#8E969A'), mark('box', 4, 12, 22, 3, 0, '#8E969A'),
                mark('box', 4, 19, 14, 3, 0, '#8E969A')]),
    teil('ruecken', 'nylon_fabric', 'Rückenteil (Obermaterial, Wattierung, Futter)', 'Rückenteil', 'box',
         x=80, y=30, w=240, d=470, z=0, h=26, r=10, mass=330, materials=KOMPLETT, color=HUELLE,
         info='Der Rücken ist genauso aufgebaut wie die Vorderseite: Nylon außen, Polyesterwatte, Futter innen.',
         marks=stepp(240, 470) + [mark('box', 0, 450, 240, 20, 4, NAHT)]),
] + aermel('l', 0, -150, 230) + aermel('r', 320, 150, 0)

explodiere(teile, abstand=70, nach_liste=True, abstaende={'taschen_rv_l': 20, 'taschen_rv_r': 20})
skaliere_masse(teile, oid='winter_jacket')
schreibe('winter_jacket', teile)
