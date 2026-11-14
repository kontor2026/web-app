"""3D-Modell: compact_fluorescent_lamp. Erzeugt tools/kategorien/modelle/compact_fluorescent_lamp.json.

Typische Energiesparlampe mit Spiralrohr (E27, etwa 11 W, 46 × 130 mm), steht auf dem Sockel.
Im Kunststoffgehäuse sitzt das elektronische Vorschaltgerät (Platine mit Elko, Drossel, Transistoren).
Explosion senkrecht gestapelt wie bei der LED-Lampe: jede Gruppe schwebt über der Oberkante der darunter,
die Elektroden-Enden des Rohrs werden seitlich (dx > 0) herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

GLAS = '#F2F4F2'
GEH = '#F1F1EC'
QUECKSILBER = ('Das Rohr enthält wenige Milligramm giftiges Quecksilber: nicht zerbrechen und die ganze Lampe '
               'zur Sammelstelle bringen.')


def spirale(dm, n=4, schritt=4):
    """Gemalte Windungen, nur in der Zeichnung: in der Foto-Ansicht ist das Rohr ein hohler Ring (wand)."""
    return [mark('cyl', i * schritt, i * schritt, dm - 2 * i * schritt, zeichnung=True) for i in range(n)]


teile = [
    teil('rohr_kuppe', 'fluorescent_tube', 'Glasrohr (Spiralspitze)', 'Spiralspitze', 'cyl',
         x=7, y=7, w=32, z=118, h=12, mass=4, form='torus', color=GLAS,
         info='Oberes Ende der Glasspirale. ' + QUECKSILBER,
         marks=spirale(32, 3, 5)),
    # Die Glasspirale als vier übereinanderliegende Windungen (Foto-Ansicht: je ein Ring, form='torus')
    *[teil('rohr' if i == 0 else f'rohr_{i + 1}', 'fluorescent_tube', 'Leuchtstoffröhre (Glasspirale)',
           'Glasrohr', 'cyl', x=1, y=1, w=44, z=62 + i * 14, h=14, mass=6, form='torus', color=GLAS, label=i == 0,
           info='Gewundenes Glasrohr, innen mit weißem Leuchtstoff beschichtet. Strom bringt Quecksilberdampf zum '
                'Leuchten, der Leuchtstoff macht daraus sichtbares Licht. ' + QUECKSILBER if i == 0
           else 'Weitere Windung der Glasspirale. ' + QUECKSILBER,
           marks=spirale(44) if i == 3 else None) for i in range(4)],
    teil('elektroden', 'fluorescent_tube', 'Rohrenden mit Glühwendeln', 'Elektroden', 'box',
         material_id='copper', x=8, y=18, w=30, d=10, z=56, h=8, r=4, explode=[48, 0, 0], mass=1.5,
         materials=[['glas', 50], ['nickel', 25], ['kupfer', 20], ['stahl', 5]],
         info='Die beiden Enden des Rohrs mit je einer kleinen Glühwendel. Sie stecken im Halter und sind mit '
              'Drähten an die Platine gelötet. Hier sitzt oft auch das Quecksilber-Amalgam.',
         color='#E8EAE8', opacity=0.75, marks=[mark('cyl', 3, 2, 6, fill='#9EA3A8'), mark('cyl', 21, 2, 6, fill='#9EA3A8')]),
    teil('halter', 'plastic_housing', 'Rohrhalter (Gehäusedeckel)', 'Rohrhalter', 'cyl',
         x=1, y=1, w=44, z=50, h=12, mass=6, color=GEH,
         info='Kunststoffring aus PBT, hält die Glasspirale. Mit dem Unterteil verrastet; nicht aufbrechen, '
              'sonst kann das Glas splittern.',
         marks=[mark('cyl', 6, 6, 32, fill='#E0E0DA'), mark('cyl', 11, 18, 8, fill='#D0D0CA'),
                mark('cyl', 25, 18, 8, fill='#D0D0CA')]),
    teil('elko', 'circuit_board', 'Elektrolytkondensator', 'Elko', 'cyl',
         material_id='mixed_electronics', x=8, y=16, w=10, z=33.6, h=14, mass=2,
         materials=[['alu', 55], ['papier', 20], ['pcabs', 10], ['gummi', 5], ['kupfer', 10]],
         info='Glättet die gleichgerichtete Netzspannung. Kann kurz nach dem Ausschalten noch geladen sein.',
         color='#2F4F7A', marks=[mark('cyl', 2, 2, 6, fill='#B9C0C6')]),
    teil('drossel', 'circuit_board', 'Drossel (Ferritkern)', 'Drossel', 'box',
         material_id='mixed_electronics', x=21, y=14, w=12, d=11, z=33.6, h=10, r=1, mass=4,
         materials=[['ferrit', 55], ['kupfer', 40], ['pcabs', 5]],
         info='Kupferspule auf Ferritkern. Begrenzt den Strom durch das Rohr, sobald es leuchtet.',
         color='#3A3F44', marks=[mark('box', 2, 2, 8, 7, 1, '#C5803D')]),
    teil('transistoren', 'circuit_board', 'Transistoren und Ringkern', 'Transistoren', 'box',
         material_id='mixed_electronics', x=14, y=28, w=18, d=6, z=33.6, h=9, r=0.5, mass=1.5,
         materials=[['chip', 45], ['ferrit', 25], ['kupfer', 30]],
         info='Zwei Schalttransistoren und ein kleiner Ringkern-Übertrager. Sie erzeugen die hohe Frequenz, '
              'mit der das Rohr flackerfrei leuchtet.',
         color='#22272B', marks=[mark('cyl', 12, 1, 4, fill='#3A6B9A')]),
    teil('platine', 'circuit_board', 'Platine (Vorschaltgerät)', 'Platine', 'cyl',
         x=4, y=4, w=38, z=32, h=1.6, mass=3,
         info='Runde Leiterplatte mit dem elektronischen Vorschaltgerät. Gehört mit der Lampe zur Sammelstelle.',
         color='#C9A35A', marks=[mark('cyl', 4, 4, 30, fill='#B8924A')]),
    teil('gehaeuse_oben', 'plastic_housing', 'Gehäuse (oberer Teil)', 'Gehäuse', 'cyl',
         x=2, y=2, w=42, z=34, h=16, mass=5, color=GEH,
         info='Schwer entflammbarer Kunststoff, umschließt die Elektronik. Wird beim Betrieb warm.',
         marks=[mark('cyl', 3, 3, 36, fill='#E6E6E0')]),
    teil('gehaeuse_unten', 'plastic_housing', 'Gehäuse (Hals)', 'Gehäusehals', 'cyl',
         x=6, y=6, w=34, z=24, h=10, mass=3, color=GEH, label=False,
         info='Verjüngt sich zum Sockel hin. Der Sockel ist eingepresst oder eingeklebt.'),
    teil('sockel', 'plastic_housing', 'Schraubsockel E27', 'Sockel', 'cyl',
         material_id='aluminium', x=9.5, y=9.5, w=27, z=3, h=21, mass=4, materials=[['alu', 100]],
         info='Gewinde aus Aluminiumblech, passt in jede normale Lampenfassung.', color='#E2E5E7',
         marks=[mark('cyl', 1.5, 1.5, 24), mark('cyl', 3, 3, 21)]),
    teil('fusskontakt', 'plastic_housing', 'Fußkontakt mit Isolierglas', 'Fußkontakt', 'cyl',
         material_id='copper', x=17, y=17, w=12, z=0, h=3, mass=2,
         materials=[['messing', 45], ['behaelterglas', 40], ['lot', 15]],
         info='Messingkontakt mit Lötpunkt, durch schwarzes Glas vom Gewinde getrennt.',
         color='#2A2B2D', marks=[mark('cyl', 3, 3, 6, fill='#D4B464')]),
]

# Senkrecht stapeln: Gruppen von unten nach oben, jede schwebt ABSTAND über der explodierten Oberkante der darunter.
ABSTAND = 14
gruppen = [['fusskontakt'], ['sockel'], ['gehaeuse_unten', 'gehaeuse_oben'], ['platine'],
           ['elko', 'drossel', 'transistoren'], ['halter'], ['rohr', 'rohr_2', 'rohr_3', 'rohr_4', 'rohr_kuppe']]
nach_id = {p['id']: p for p in teile}
oben = None
for g in gruppen:
    ps = [nach_id[i] for i in g]
    unten = min(p['z'] for p in ps)
    dz = 0 if oben is None else round(oben + ABSTAND - unten, 1)
    for p in ps:
        p['explode'] = [0, 0, dz]
    oben = max(p['z'] + p['h'] for p in ps) + dz

skaliere_masse(teile, oid='compact_fluorescent_lamp')
schreibe('compact_fluorescent_lamp', teile)
