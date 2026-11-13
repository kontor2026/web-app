"""3D-Modell: winter_jacket. Erzeugt tools/kategorien/modelle/winter_jacket.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Gesteppte Winterjacke gefaltet, Vorderseite oben, Kragen hinten (y = 0), Saum vorne. 400 × 500 × 80 mm.
# Die Ärmel liegen eingeschlagen unter dem Rücken und werden zur Seite gezogen. Vorne sind Obermaterial,
# Wattierung und Futter als eigene Ebenen abgehoben, damit man den Schichtaufbau sieht.
HUELLE = '#2E5B4A'
NAHT = '#244A3C'
FUTTER = '#3A3F44'
WATTE = '#F2F0EA'
SCHALE = [['nylon', 100]]
KOMPLETT = [['nylon', 55], ['polyester', 45]]
STEPP = [mark('box', 0, y, 186, 2, 0, NAHT) for y in range(60, 460, 70)]

teile = [
    teil('kragen', 'nylon_fabric', 'Stehkragen', 'Kragen', 'box',
         x=110, y=0, w=180, d=50, z=60, h=20, r=12, mass=50, materials=KOMPLETT, color=HUELLE,
         info='Hochgestellter, wattierter Kragen mit Fleece innen. In den Kragen ist manchmal eine Kapuze eingerollt.',
         marks=[mark('box', 10, 22, 160, 2, 1, NAHT)]),
    teil('kordelstopper_1', 'nylon_fabric', 'Kordelstopper', 'Kordelstopper', 'cyl', material_id='pp',
         x=24, y=478, w=12, d=16, z=77, h=6, mass=2, materials=[['pp', 80], ['stahl', 20]], color='#22272B',
         info='Klemme aus Kunststoff mit Stahlfeder für die Saumkordel. Vor dem Textilrecycling abschneiden.',
         marks=[mark('cyl', 3, 5, 6, fill='#555C62')]),
    teil('kordelstopper_2', 'nylon_fabric', 'Kordelstopper', 'Kordelstopper', 'cyl', material_id='pp',
         x=364, y=478, w=12, d=16, z=77, h=6, mass=2, materials=[['pp', 80], ['stahl', 20]], color='#22272B',
         label=False, info='Zweiter Kordelstopper auf der anderen Seite.', marks=[mark('cyl', 3, 5, 6, fill='#555C62')]),
    teil('reissverschluss', 'metal_zipper', 'Reißverschluss mit Schieber', 'Reißverschluss', 'box',
         x=193, y=40, w=14, d=460, z=70, h=10, r=1, mass=35, materials=[['messing', 55], ['polyester', 40], ['stahl', 5]],
         color='#2A2E31',
         info='Metallzähne auf zwei Polyesterbändern, mit Schieber und Zipper. Rechts und links neben dem Band '
              'abschneiden: Das Metall darf nicht ins Textilrecycling.',
         marks=[mark('box', 5, 0, 4, 460, 0.5, '#C9A24A'), mark('box', 3, 30, 8, 16, 2, '#B7BCC0')]),
    teil('aussen_l', 'nylon_fabric', 'Obermaterial vorne links', 'Obermaterial', 'box',
         x=0, y=40, w=193, d=460, z=70, h=7, r=8, mass=70, materials=SCHALE, color=HUELLE,
         info='Wasserabweisendes Nylon-Gewebe, mit der Wattierung in Kammern abgesteppt. Tragbare Jacken in die Altkleidersammlung.',
         marks=STEPP + [mark('box', 30, 300, 90, 6, 2, NAHT)]),
    teil('aussen_r', 'nylon_fabric', 'Obermaterial vorne rechts', 'Obermaterial', 'box',
         x=207, y=40, w=193, d=460, z=70, h=7, r=8, mass=70, materials=SCHALE, color=HUELLE, label=False,
         info='Gegenstück zur linken Vorderseite, mit Eingrifftasche.',
         marks=STEPP + [mark('box', 73, 300, 90, 6, 2, NAHT)]),
    teil('wattierung', 'polyester_fill', 'Wattierung', 'Wattierung', 'box',
         x=5, y=45, w=390, d=450, z=50, h=20, r=8, mass=120, color=WATTE,
         info='Polyester-Hohlfasern halten die warme Luft fest. Futter aufschneiden und die Watte als Füllmaterial '
              'für Kissen weiterverwenden.',
         marks=[mark('box', 0, y, 390, 3, 0, '#DCD8CE') for y in range(55, 450, 70)]),
    teil('futter', 'nylon_fabric', 'Innenfutter vorne', 'Futter', 'box',
         x=5, y=45, w=390, d=450, z=46, h=4, r=8, mass=60, materials=[['nylon', 60], ['polyester', 40]], color=FUTTER,
         info='Glattes Futter aus Nylon-Taft, damit die Jacke leicht über den Pullover gleitet. Mit Innentasche.',
         marks=[mark('box', 230, 120, 110, 4, 2, '#2A2E31')]),
    teil('etikett', 'care_label', 'Pflegeetikett', 'Etikett', 'box',
         x=230, y=10, w=30, d=40, z=45.7, h=0.3, r=1, mass=2, explode=[200, -90, 0], color='#F4F2EE',
         info='Etikett mit Waschsymbolen und Materialangaben, innen an der Seitennaht. Abschneiden: anderes Material.',
         marks=[mark('box', 4, 5, 22, 3, 0, '#8E969A'), mark('box', 4, 12, 22, 3, 0, '#8E969A'),
                mark('box', 4, 19, 14, 3, 0, '#8E969A')]),
    teil('ruecken', 'nylon_fabric', 'Rückenteil (Obermaterial, Wattierung, Futter)', 'Rückenteil', 'box',
         x=0, y=0, w=400, d=500, z=20, h=26, r=8, mass=380, materials=KOMPLETT, color=HUELLE,
         info='Der Rücken ist genauso aufgebaut wie die Vorderseite: Nylon außen, Polyesterwatte, Futter innen.',
         marks=[mark('box', 0, y, 400, 2, 0, NAHT) for y in range(60, 500, 70)]),
    teil('aermel_l', 'nylon_fabric', 'Ärmel links (eingeschlagen)', 'Ärmel', 'box',
         x=15, y=30, w=180, d=440, z=0, h=20, r=12, mass=170, materials=KOMPLETT, color=HUELLE, explode=[-260, 0, 0],
         info='Wattierter Ärmel mit Strickbündchen am Handgelenk, beim Falten unter den Rücken geschlagen.',
         marks=[mark('box', 0, y, 180, 2, 0, NAHT) for y in range(40, 380, 70)] + [mark('box', 20, 400, 140, 40, 4, FUTTER)]),
    teil('aermel_r', 'nylon_fabric', 'Ärmel rechts (eingeschlagen)', 'Ärmel', 'box',
         x=205, y=30, w=180, d=440, z=0, h=20, r=12, mass=170, materials=KOMPLETT, color=HUELLE, explode=[260, 0, 0],
         label=False, info='Gegenstück zum linken Ärmel.',
         marks=[mark('box', 0, y, 180, 2, 0, NAHT) for y in range(40, 380, 70)] + [mark('box', 20, 400, 140, 40, 4, FUTTER)]),
]

explodiere(teile, abstand=90, nach_liste=True, abstaende={'kordelstopper_1': 25, 'kordelstopper_2': 25})
skaliere_masse(teile, oid='winter_jacket')
schreibe('winter_jacket', teile)
