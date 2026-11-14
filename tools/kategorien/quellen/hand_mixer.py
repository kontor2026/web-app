"""3D-Modell: hand_mixer. Erzeugt tools/kategorien/modelle/hand_mixer.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Handmixer steht auf seinen eingesetzten Rührbesen: Körper waagerecht entlang x (0..200, z 50..110), darüber der
# Bügelgriff (Stege vorne bei x 50..80 und hinten bei x 165..195, Griffbügel z 128..150) mit Fingerlücke.
# Besen vorne links (x 35..67) nach unten, Kabel kommt hinten rechts (x = 200) heraus.
# Explosion: Besen bleiben stehen, Unterschale, Innenleben, Oberschale und Griff schweben darüber,
# Kabel nach rechts (dx > 0). Innenleben mit sortBias, damit es zusammengebaut hinter den Schalen liegt.
WEISS = '#E9EEF2'
BESEN = [(12, 'links'), (46, 'rechts')]
INNEN = -40

teile = [
    teil('auswurftaste', 'plastic_housing', 'Auswurftaste', 'Auswurftaste', 'box',
         x=54, y=34, w=16, d=22, z=150, h=4, r=4, mass=6, materials=[['pcabs', 80], ['stahl', 20]],
         info='Drückt über eine Stahlstange die Besen aus dem Getriebe. Kappe ist nur aufgesteckt.',
         color='#9AA2A6', marks=[mark('box', 4, 9, 8, 4, 2, '#5F6B75')]),
    teil('griff', 'plastic_housing', 'Bügelgriff', 'Griff', 'box',
         x=50, y=28, w=145, d=34, z=128, h=22, r=14, mass=60, color=WEISS,
         info='Hohler Kunststoffbügel, in dem Schalter und Kabel verlaufen. Die beiden Hälften sind verschraubt.',
         marks=[mark('box', 24, 11, 34, 12, 6, '#C5CDD3'), mark('box', 34, 13, 8, 8, 2, '#5F6B75'),
                mark('box', 70, 4, 66, 26, 12, '#D5DCE1')]),
    teil('steg_vorne', 'plastic_housing', 'Griffsteg vorne', 'Griffsteg', 'box',
         x=50, y=28, w=30, d=34, z=110, h=18, r=10, mass=15, color=WEISS, label=False,
         info='Vorderer Steg zwischen Körper und Griff, innen läuft das Schalterkabel.'),
    teil('steg_hinten', 'plastic_housing', 'Griffsteg hinten', 'Griffsteg', 'box',
         x=165, y=28, w=30, d=34, z=110, h=18, r=10, mass=15, color=WEISS,
         info='Hinterer Steg zwischen Körper und Griff. Griff und Stege gehören zur Oberschale.'),
    teil('schalter', 'plastic_housing', 'Stufenschalter mit Entstörkondensator', 'Schalter', 'box',
         material_id='mixed_electronics', x=55, y=33, w=40, d=24, z=112, h=14, r=2, mass=20, sortBias=INNEN,
         materials=[['pcabs', 50], ['kupfer', 25], ['kontakte', 10], ['pp', 15]],
         info='Schiebeschalter für fünf Stufen; der Kondensator verhindert Funkstörungen. Kabel sind gelötet oder '
              'gesteckt.',
         color='#5F6B75', marks=[mark('box', 4, 5, 12, 14, 2, fill='#9AA2A6'), mark('box', 20, 3, 16, 18, 2, fill='#D9B44A')]),
    teil('oberschale', 'plastic_housing', 'Gehäuse-Oberschale', 'Oberschale', 'box',
         x=0, y=5, w=200, d=80, z=80, h=30, r=26, mass=110, color=WEISS,
         info='Obere Hälfte des Körpers. Die Schrauben sitzen von unten in der Unterschale, eine oft unter dem '
              'Typenschild.',
         marks=[mark('box', 6, 24, 30, 32, 14, '#DCE2E6')] + raster(100, 6, 5, 1, 4, 14, 9, r=1, fill='#B5BDC3')
         + raster(100, 60, 5, 1, 4, 14, 9, r=1, fill='#B5BDC3')),
    teil('kohle1', 'electric_motor', 'Kohlebürste', 'Kohlebürsten', 'box', material_id='mixed_electronics',
         x=112, y=12, w=12, d=10, z=78, h=10, r=1, mass=3, materials=[['graphit', 60], ['kupfer', 20], ['messing', 20]],
         color='#3B3B3B', sortBias=INNEN,
         info='Zwei Graphitklötze, die mit Federn auf den Kollektor drücken und den Strom zum drehenden Teil leiten. '
              'Sie nutzen sich ab.', marks=[mark('box', 3, 2, 6, 6, 1, '#B08D57')]),
    teil('kohle2', 'electric_motor', 'Kohlebürste', 'Kohlebürsten', 'box', material_id='mixed_electronics',
         x=112, y=68, w=12, d=10, z=78, h=10, r=1, mass=3, materials=[['graphit', 60], ['kupfer', 20], ['messing', 20]],
         color='#3B3B3B', label=False, sortBias=INNEN, info='Zweite Kohlebürste.',
         marks=[mark('box', 3, 2, 6, 6, 1, '#B08D57')]),
    teil('luefterrad', 'electric_motor', 'Lüfterrad', 'Lüfterrad', 'box', material_id='pp',
         x=156, y=25, w=10, d=40, z=56, h=40, r=2, mass=8, materials=[['pp', 100]], sortBias=INNEN,
         info='Sitzt auf der Motorwelle und bläst Kühlluft durch die Schlitze im Gehäuse.',
         color='#5F6B75', marks=raster(2, 3, 1, 6, 6, 3, 0, 6, r=1, fill='#4A545C')),
    teil('motor', 'electric_motor', 'Universalmotor', 'Motor', 'box',
         x=92, y=22, w=62, d=46, z=56, h=40, r=16, mass=280, sortBias=INNEN,
         materials=[['kupfer', 32], ['stahl', 55], ['graphit', 3], ['pcabs', 10]],
         info='Motor mit Kupferwicklungen, treibt über eine Schnecke beide Besen an. Mit zwei Schrauben befestigt.',
         marks=[mark('box', 8, 6, 46, 34, 12, fill='#B87333'), mark('cyl', 2, 18, 10, fill='#9AA2A6')]),
    teil('getriebe', 'electric_motor', 'Schneckengetriebe', 'Getriebe', 'box', material_id='nylon',
         x=25, y=15, w=62, d=60, z=58, h=18, r=6, mass=60, materials=[['nylon', 55], ['stahl', 45]], sortBias=INNEN,
         info='Zwei Kunststoffzahnräder mit Stahlbuchsen drehen die Besen gegenläufig. Sie sind gefettet; Fett mit '
              'Papier abwischen.',
         color=WEISS, marks=[mark('cyl', 10, 3, 24, fill='#D5DADE'), mark('cyl', 10, 33, 24, fill='#D5DADE')]
         + [mark('box', 36, 25, 26, 10, 3, fill='#9AA2A6')] + raster(12, 5, 4, 1, 2, 2, 5, fill='#B5BDC3')),
    *[teil(f'schraube{i}', 'plastic_housing', 'Gehäuseschraube', 'Schrauben', 'cyl', material_id='steel',
           x=x, y=y, w=6, z=54, h=3, mass=1, materials=[['stahl', 100]], color='#C9CDD0', label=i == 0,
           sortBias=INNEN, info='Drei Schrauben mit Sonderkopf (Dreiflügel) halten Ober- und Unterschale zusammen.',
           marks=[mark('box', 1, 2.5, 4, 1), mark('box', 2.5, 1, 1, 4)])
      for i, (x, y) in enumerate([(8, 42), (184, 14), (184, 70)])],
    teil('unterschale', 'plastic_housing', 'Gehäuse-Unterschale', 'Unterschale', 'box',
         x=0, y=5, w=200, d=80, z=50, h=30, r=26, mass=120, color=WEISS,
         info='Untere Hälfte mit den beiden Öffnungen für die Besen und Lüftungsschlitzen. Kommt zum Kunststoff, '
              'wenn alle Metallteile entfernt sind.',
         marks=[mark('cyl', 42, 14, 18, fill='#9AA2A6'), mark('cyl', 42, 48, 18, fill='#9AA2A6')]
         + raster(150, 15, 5, 1, 4, 50, 9, r=1, fill='#9AA2A6')),
]
besen_ids = []
for y, seite in BESEN:
    teile.append(teil(f'schaft_{seite}', 'mixer_beaters', f'Besenschaft {seite}', 'Schaft', 'cyl',
                      x=47, y=y + 12, w=8, z=44, h=24, mass=12, materials=[['stahl', 100]], sortBias=INNEN,
                      info='Edelstahlschaft mit Nut, rastet im Getriebe ein. Auswurftaste drücken, dann lösen sich '
                           'die Besen.', color='#B8BEC4', label=seite == 'links'))
    for k, (w, z, h) in enumerate([(18, 38, 6), (30, 8, 30), (20, 0, 8)]):
        teile.append(teil(f'besen_{seite}{k}', 'mixer_beaters', f'Rührbesen {seite}', 'Besen', 'cyl',
                          x=51 - w / 2, y=y + 16 - w / 2, w=w, z=z, h=h, mass=12, materials=[['stahl', 100]],
                          info='Vier gebogene Edelstahldrähte, die einen Korb bilden. Reiner Stahl: kommt zum Altmetall.'
                          if seite == 'links' and k == 1 else 'Teil des Rührbesens.',
                          color='#C9CED2', opacity=0.8, label=seite == 'links' and k == 1,
                          marks=[mark('box', 1, w / 2 - 1, w - 2, 2, 1, fill='#7C858C'),
                                 mark('box', w / 2 - 1, 1, 2, w - 2, 1, fill='#7C858C')]))
        besen_ids.append(f'besen_{seite}{k}')
teile += [
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=150, y=41, w=50, d=8, z=60, h=8, r=4, explode=[90, 0, 0], mass=60, materials=[['pvc', 90], ['pp', 10]],
         info='Etwa 1,2 m PVC-Mantel mit Eurostecker. Längs aufschlitzen, um die Kupferadern freizulegen.',
         color='#2E3338', marks=[mark('box', 40, 1, 10, 6, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=150, y=43.5, w=50, d=3, z=62.5, h=3, r=1, explode=[90, 0, 15], mass=25,
         info='Zwei Kupferadern aus feiner Litze. Kupfer lässt sich fast verlustfrei wiederverwerten.',
         color='#B87333'),
]

explodiere(teile, abstand=22, fest=besen_ids, gruppen=[['griff', 'steg_vorne', 'steg_hinten']],
           abstaende={'oberschale': 80, 'schaft_links': 10, 'schaft_rechts': 10, 'kohle1': 12, 'kohle2': 12,
                      **{f'schraube{i}': 12 for i in range(3)}})
# Foto-Ansicht: echte Formen (Kabel liegend, Spulen als Ring); Details darauf nur in der Zeichnung
FORMEN = {'kabel': ('liegend_x', 1), 'kupferadern': ('liegend_x', 1), 'griff': ('liegend_x', 1)}
for p in teile:
    if p['id'] in FORMEN:
        p['form'], nur_zeichnung = FORMEN[p['id']]
        p.pop('wand', None)
        p.pop('boden', None)
        for m in (p.get('marks') or []) if nur_zeichnung else []:
            m['zeichnung'] = True
skaliere_masse(teile, oid='hand_mixer')
schreibe('hand_mixer', teile)
