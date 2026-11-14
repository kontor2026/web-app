"""3D-Modell: clothes_iron. Erzeugt tools/kategorien/modelle/clothes_iron.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Dampfbügeleisen auf der Sohle, Spitze vorne (y = 270), Kabel hinten (y = 0). Sohle, Gehäuse und Wassertank sind aus
# Abschnitten entlang y aufgebaut, die nach vorne schmaler werden (spitze Bügeleisenform). Darüber der Bügelgriff mit
# Heck und vorderem Steg, darunter eine Lücke für die Hand.
# Explosion: Sohle bleibt, darüber Heizelement, Hitzeschutzblech, Thermostat und Dampfventil, Gehäuse, Griff, Regler.
# Wassertank und Sprühdüse nach vorne (dy > 0), Heckkappe nach hinten (dy < 0), Kabel nach rechts (dx > 0).
BLAU = '#5DADE2'
DUNKEL = '#2E3338'
SOHLE = [(0, 110, 120, 18), (110, 60, 112, 4), (170, 50, 96, 4), (220, 35, 72, 4), (255, 15, 40, 7)]


def abschnitte(pid, comp, name, short, segs, z, h, mass, info, **kw):
    teile = []
    for i, (y, d, w, r) in enumerate(segs):
        teile.append(teil(f'{pid}{i}', comp, name, short, 'box', x=round(60 - w / 2, 1), y=y, w=w, d=d, z=z, h=h,
                          r=r, mass=mass * w * d / sum(s[1] * s[2] for s in segs), label=i == 0,
                          info=info if i == 0 else f'Abschnitt: {name}.', **kw))
    return teile


sohle = abschnitte('sohle', 'iron_soleplate', 'Bügelsohle', 'Sohle', SOHLE, 0, 14, 450,
                   'Aluminiumguss mit Keramikbeschichtung und Dampflöchern. Wertvolles Aluminium für den Metallschrott.',
                   materials=[['alu', 95], ['keramik', 5]], color='#E2E5E8')
sohle[0]['marks'] = raster(14, 50, 6, 4, 4, 4, 16, 15, shape='cyl', fill='#7C858C')
sohle[1]['marks'] = raster(14, 8, 6, 3, 4, 4, 15, 18, shape='cyl', fill='#7C858C')
sohle[2]['marks'] = raster(16, 8, 5, 2, 4, 4, 15, 20, shape='cyl', fill='#7C858C')
gehaeuse = abschnitte('gehaeuse', 'plastic_housing', 'Gehäuseunterteil', 'Gehäuse',
                      [(5, 105, 112, 18), (110, 45, 104, 4)], 23, 50, 120,
                      'Hitzefester Kunststoff über Thermostat und Heizung. Mit Schrauben von unten durch die Sohle '
                      'befestigt.', color=BLAU)
gehaeuse[0]['marks'] = [mark('cyl', 36, 50, 40, fill='#4A9BD0')]
tank = abschnitte('tank', 'water_tank', 'Wassertank', 'Wassertank',
                  [(155, 40, 100, 4), (195, 35, 80, 4), (230, 27, 56, 10)], 23, 46, 90,
                  'Durchsichtiger Kunststofftank für etwa 300 ml Wasser, vorne im Gehäuse. Eingeklipst; ohne Metall '
                  'gehört er zum Kunststoff.', color='#D6E6EC', opacity=0.4)
tank[0]['marks'] = raster(12, 14, 4, 1, 12, 2, 20, r=1, fill='#9FB8C2')
tank[1]['marks'] = [mark('box', 22, 8, 36, 18, 8, '#3C4248')]

teile = [
    teil('regler', 'thermostat', 'Temperaturregler', 'Regler', 'cyl', material_id='abs',
         x=40, y=60, w=40, z=73, h=8, mass=10, materials=[['pcabs', 100]],
         info='Drehknopf, der über eine Achse den Thermostat verstellt. Lässt sich mit einem flachen Schraubendreher '
              'abhebeln.', color='#E9EEF2',
         marks=[mark('box', 18, 3, 4, 14, 1, fill=DUNKEL)] + raster(4, 18, 3, 1, 3, 3, 13, shape='cyl', fill=BLAU)),
    teil('griff', 'plastic_housing', 'Bügelgriff', 'Griff', 'box',
         x=44, y=30, w=32, d=180, z=110, h=28, r=15, mass=60, color=BLAU,
         info='Hohler Griff aus Kunststoff, innen die Dampftasten. Gehört zum Gehäuse und wird mit ihm entsorgt.',
         marks=[mark('box', 6, 20, 20, 110, 9, '#4A9BD0'), mark('cyl', 9, 140, 14, fill='#E9EEF2'),
                mark('cyl', 9, 158, 14, fill='#E9EEF2')]),
    teil('griffsteg', 'plastic_housing', 'Vorderer Griffsteg', 'Griffsteg', 'box',
         x=44, y=180, w=32, d=30, z=69, h=41, r=12, mass=15, color=BLAU, label=False,
         info='Verbindet den Griff mit dem Gehäuse vorne, darin die Stange der Sprühpumpe.'),
    teil('heck', 'plastic_housing', 'Heckteil', 'Heck', 'box',
         x=24, y=8, w=72, d=40, z=73, h=37, r=16, mass=40, color=BLAU,
         info='Hinterer Teil mit Stellfläche, auf dem man das Bügeleisen abstellt. Darin laufen die Kabeladern.'),
    *gehaeuse,
    teil('dampfventil', 'water_tank', 'Dampfventil', 'Dampfventil', 'box', material_id='pp',
         x=52, y=150, w=16, d=16, z=23, h=12, r=4, mass=8, materials=[['pp', 60], ['stahl', 25], ['gummi', 15]],
         color='#E9EEF2', info='Lässt Wasser aus dem Tank tropfenweise auf die heiße Sohle, wo es zu Dampf wird. '
                                 'Mit Gummidichtung; kann verkalken.',
         marks=[mark('cyl', 4, 4, 8, fill='#9AA2A6')]),
    teil('thermostat', 'thermostat', 'Thermostat (Bimetall)', 'Thermostat', 'box',
         x=45, y=95, w=30, d=30, z=23, h=10, r=3, mass=30,
         materials=[['bimetall', 40], ['keramik', 20], ['kupfer', 20], ['kontakte', 20]],
         info='Ein Bimetallstreifen schaltet die Heizung aus, wenn die eingestellte Temperatur erreicht ist. Klickt '
              'beim Aufheizen hörbar.',
         color='#B8BEC4', marks=[mark('cyl', 10, 10, 10, fill='#D5DADE'), mark('box', 2, 2, 6, 26, 1, '#B87333')]),
    teil('thermosicherung', 'thermostat', 'Thermosicherung', 'Sicherung', 'box', material_id='mixed_electronics',
         x=80, y=70, w=8, d=16, z=23, h=4, r=2, mass=2, materials=[['keramik', 40], ['kupfer', 40], ['stahl', 20]],
         color='#C4672D', info='Brennt einmalig durch, wenn das Thermostat versagt und die Sohle zu heiß wird. Danach '
                               'heizt das Bügeleisen nicht mehr.'),
    teil('hitzeschild', 'iron_soleplate', 'Hitzeschutzblech', 'Hitzeschild', 'box', material_id='steel',
         x=12, y=10, w=96, d=200, z=20, h=3, r=30, mass=60, materials=[['stahl', 100]],
         info='Dünnes Stahlblech zwischen heißer Sohle und Kunststoffteilen. Kommt zum Altmetall.',
         color='#C9CDD0', marks=[mark('box', 40, 145, 16, 16, 4, '#7C858C')]),
    teil('heizelement', 'heating_element', 'Rohrheizkörper', 'Heizelement', 'box',
         x=15, y=25, w=90, d=200, z=14, h=6, r=30, mass=150, materials=[['stahl', 50], ['nichrom', 20], ['keramik', 30]],
         info='U-förmiges Heizrohr mit Nickel-Chrom-Draht, in die Sohle eingegossen. Lässt sich nicht von der Sohle '
              'trennen.',
         color='#8C7B6B', marks=[mark('box', 4, 4, 10, 170, 5, fill='#C4672D'), mark('box', 76, 4, 10, 170, 5, fill='#C4672D'),
                                 mark('box', 4, 160, 82, 14, 7, fill='#C4672D'), mark('cyl', 2, 2, 8, fill='#B87333'),
                                 mark('cyl', 80, 2, 8, fill='#B87333')]),
    *[teil(f'schraube{i}', 'iron_soleplate', 'Sohlenschraube', 'Schrauben', 'cyl', material_id='steel',
           x=x, y=y, w=6, z=14, h=4, mass=1, materials=[['stahl', 100]], color='#C9CDD0', label=i == 0,
           info='Schrauben halten Sohle und Gehäuse zusammen; die hintere sitzt oft unter der Heckkappe.',
           marks=[mark('box', 1, 2.5, 4, 1), mark('box', 2.5, 1, 1, 4)])
      for i, (x, y) in enumerate([(57, 12), (57, 228)])],
    *sohle,
    *tank,
    teil('spruehduese', 'water_tank', 'Sprühdüse', 'Sprühdüse', 'box', material_id='pp',
         x=50, y=246, w=20, d=14, z=58, h=12, r=4, explode=[0, 160, 0], mass=5, materials=[['pp', 100]],
         info='Kleine Pumpdüse, die Wasser aus dem Tank auf die Wäsche sprüht. Reiner Kunststoff.',
         color='#E9EEF2', marks=[mark('cyl', 7, 2, 6, fill='#9AA2A6')]),
    teil('heckkappe', 'plastic_housing', 'Heckkappe mit Kabelgelenk', 'Heckkappe', 'box',
         x=25, y=0, w=70, d=8, z=14, h=59, r=4, explode=[0, -60, 0], mass=40, color=DUNKEL,
         info='Rückwand mit Stellfläche und Kabelgelenk. Hinter ihr liegen die Kabelanschlüsse; zwei Schrauben lösen.'),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=40, y=0, w=80, d=8, z=30, h=8, r=4, explode=[80, -70, 0], mass=100, materials=[['pvc', 85], ['textil', 15]],
         info='Etwa 2 m Kabel mit Stoffummantelung oder PVC. Längs aufschlitzen, um die Kupferadern freizulegen.',
         color=DUNKEL, marks=[mark('box', 70, 1, 10, 6, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=40, y=2.5, w=80, d=3, z=32.5, h=3, r=1, explode=[80, -70, 15], mass=50,
         info='Drei Kupferadern für bis zu 2400 Watt. Kupfer lässt sich fast verlustfrei wiederverwerten.',
         color='#B87333'),
]
for p in tank:
    p['explode'] = [0, 110, 0]

explodiere(teile, abstand=22, fest=[p['id'] for p in sohle],
           gruppen=[[p['id'] for p in gehaeuse], ['griff', 'griffsteg', 'heck']],
           abstaende={'gehaeuse0': 55, 'gehaeuse1': 55, 'schraube0': 12, 'schraube1': 12, 'thermosicherung': 12})
# Foto-Ansicht: echte Formen (Kabel liegend, Spulen als Ring); Details darauf nur in der Zeichnung
FORMEN = {'kabel': ('liegend_x', 1), 'kupferadern': ('liegend_x', 1), 'griff': ('liegend_y', 0)}
for p in teile:
    if p['id'] in FORMEN:
        p['form'], nur_zeichnung = FORMEN[p['id']]
        p.pop('wand', None)
        p.pop('boden', None)
        for m in (p.get('marks') or []) if nur_zeichnung else []:
            m['zeichnung'] = True
skaliere_masse(teile, oid='clothes_iron')
schreibe('clothes_iron', teile)
