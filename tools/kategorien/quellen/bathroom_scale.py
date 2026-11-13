"""3D-Modell: bathroom_scale. Erzeugt tools/kategorien/modelle/bathroom_scale.json.

Typische digitale Glas-Personenwaage (300 × 300 × 25 mm): 5-mm-Sicherheitsglas auf einer dünnen Kunststoff-
Trägerplatte, in den vier Ecken je ein Fuß mit Wägezelle, vorne (y groß) Platine und LCD-Anzeige,
in der Mitte das Batteriefach mit zwei AAA-Zellen.
Explosion: Ebenen nach oben (Füße und Batteriefach unten, dann Wägezellen, Batterien, Elektronik, Trägerplatte, Glas).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

ECKEN = [(248, 248), (248, 12), (12, 248), (12, 12)]  # linke hintere Ecke der Füße (je 40 × 40)
ALU = '#C9CDD0'
AAA = [['zinkmangan', 80], ['stahl', 20]]

zellen, fuesse = [], []
for i, (x, y) in enumerate(ECKEN):
    erste = i == 0
    zellen.append(teil(f'waegezelle_{i + 1}', 'load_cell', 'Wägezelle', 'Wägezelle', 'box',
                       x=x + 3, y=y + 3, w=34, d=34, z=9, h=6, r=2, mass=18, color=ALU,
                       info='Aluminiumplatte mit aufgeklebten Dehnungsmessstreifen. Sie verbiegt sich unter dem '
                            'Gewicht minimal, daraus berechnet die Waage die Kilos. Drei dünne Drähte führen zur Platine.'
                       if erste else 'Eine von vier gleichen Wägezellen, eine in jeder Ecke.',
                       marks=[mark('box', 4, 4, 26, 6, 1, '#AEB3B7'), mark('box', 4, 24, 26, 6, 1, '#AEB3B7'),
                              mark('box', 13, 12, 8, 10, 0.5, '#C5803D')],
                       **({} if erste else {'label': False})))
    fuesse.append(teil(f'fuss_{i + 1}', 'plastic_housing', 'Fuß mit Gummikappe', 'Fuß', 'cyl',
                       material_id='abs', x=x, y=y, w=40, z=0, h=9, mass=8,
                       materials=[['pcabs', 75], ['gummi', 25]], color='#2B2E31',
                       info='Kunststofffuß, in dem die Wägezelle sitzt, unten eine rutschfeste Gummikappe. '
                            'Mit zwei Schrauben an der Trägerplatte befestigt.'
                       if erste else 'Gleicher Fuß wie die anderen drei.',
                       marks=[mark('cyl', 5, 5, 30, fill='#3A3D40')], **({} if erste else {'label': False})))

teile = [
    teil('glas', 'glass_platform', 'Sicherheitsglas-Platte', 'Glasplatte', 'box',
         x=0, y=0, w=300, d=300, z=20, h=5, r=14, mass=1120, color='#DCE6EA', opacity=0.65,
         materials=[['glas', 98], ['druck', 2]],
         info='5 mm dickes Einscheiben-Sicherheitsglas, von unten verschraubt oder verklebt. Gehört nicht ins '
              'Altglas! An den Kanten ist es empfindlich und kann in viele Krümel zerspringen.',
         marks=[mark('box', 108, 243, 84, 40, 4, '#1E2022'), mark('box', 114, 249, 72, 28, 2, '#9AA79A')]
         + [m for i in range(3) for m in (mark('box', 121 + i * 16, 253, 2, 20, 0.5, '#2B302C'),
                                          mark('box', 131 + i * 16, 253, 2, 20, 0.5, '#2B302C'),
                                          mark('box', 121 + i * 16, 253, 12, 2, 0.5, '#2B302C'),
                                          mark('box', 121 + i * 16, 271, 12, 2, 0.5, '#2B302C'))]
         + [mark('cyl', 169, 268, 3, fill='#2B302C'), mark('box', 175, 262, 7, 10, 0.5, '#2B302C'),
            mark('box', 140, 22, 20, 3, 1.5, '#B5C2C8')]),
    teil('traegerplatte', 'plastic_housing', 'Kunststoff-Trägerplatte', 'Trägerplatte', 'box',
         x=4, y=4, w=292, d=292, z=15, h=5, r=12, mass=120, color='#E9EAE7',
         info='Dünne ABS-Platte unter dem Glas, an der Füße, Platine und Batteriefach festgeschraubt sind.',
         marks=[mark('box', 104, 239, 84, 40, 4, '#D5D6D2'), mark('box', 116, 128, 60, 38, 3, '#D5D6D2')]),
    teil('lcd', 'lcd_panel', 'LCD-Anzeige', 'LCD', 'box',
         x=115, y=249, w=70, d=28, z=12.6, h=2.4, r=1, mass=8, materials=[['glas', 70], ['folien', 20], ['displayglas', 10]],
         info='Zwei Glasplättchen mit Flüssigkristall dazwischen, zeigt Ziffern ohne Hintergrundlicht. '
              'Ein Gummistreifen verbindet sie mit der Platine. Bricht leicht.',
         color='#9AA79A', marks=raster(8, 6, 4, 1, 12, 16, 15, r=1, fill='#5D6A5D')),
    teil('leitgummi', 'lcd_panel', 'Leitgummi (Zebrastreifen)', 'Leitgummi', 'box',
         material_id='rubber', x=115, y=272, w=70, d=4, z=11.6, h=1, r=0.5, mass=1,
         materials=[['gummi', 90], ['graphit', 10]], color='#E0DCD2',
         marks=raster(1, 0.5, 34, 1, 1, 3, 2, fill='#3A3D40'),
         info='Gummistreifen mit vielen leitenden Schichten. Er drückt die Kontakte der Anzeige auf die Platine, ganz ohne Löten.'),
    teil('chip', 'circuit_board', 'Wägechip', 'Chip', 'box',
         material_id='pcb', x=106, y=237, w=9, d=9, z=11.6, h=1, r=0.3, mass=0.5, materials=[['chip', 100]],
         info='Misst die winzigen Spannungen der vier Wägezellen und rechnet sie in Kilogramm um.',
         color='#22272B', marks=[mark('cyl', 0.6, 0.6, 1)]),
    teil('platine', 'circuit_board', 'Platine', 'Platine', 'box',
         x=102, y=234, w=96, d=48, z=10, h=1.6, r=2, mass=15,
         info='Leiterplatte mit Chip und Kontakten für die Wägezellen-Drähte. Zur Elektro-Sammlung geben.',
         color='#2E6B45', marks=raster(4, 40, 4, 1, 4, 4, 6, r=0.5, fill='#C9A74A')),
    teil('batterie_1', 'alkaline_cell', 'Micro-Batterie (AAA)', 'Batterie AAA', 'box',
         x=128, y=138, w=44.5, d=10.5, z=4, h=10.5, r=5, mass=11.5, materials=AAA,
         info='Zwei 1,5-Volt-Zellen, von unten durch eine Klappe zugänglich. Herausnehmen und in die Batteriesammlung geben.',
         color='#2F6FB0', marks=[mark('box', 0, 0, 5, 10.5, 2.5, '#B7BCC0')]),
    teil('batterie_2', 'alkaline_cell', 'Micro-Batterie (AAA)', 'Batterie AAA', 'box',
         x=128, y=151, w=44.5, d=10.5, z=4, h=10.5, r=5, mass=11.5, materials=AAA, label=False,
         info='Zweite Zelle, liegt umgekehrt zur ersten.', color='#2F6FB0',
         marks=[mark('box', 39.5, 0, 5, 10.5, 2.5, '#B7BCC0')]),
    *zellen,
    teil('kabel', 'load_cell', 'Drähte der Wägezellen', 'Drähte', 'box',
         material_id='copper', x=40, y=200, w=220, d=4, z=9, h=1, r=1, mass=4,
         materials=[['kupfer', 60], ['pvc', 40]], color='#C8423A',
         marks=[mark('box', 0, 0, 220, 1, 0.3, '#E8E2C8'), mark('box', 0, 2.5, 220, 1, 0.3, '#3E9A57')],
         info='Je drei dünne Litzen (rot, weiß, grün) führen von jeder Wägezelle zur Platine. Kupfer, einfach abknipsen.'),
    teil('kontakte', 'plastic_housing', 'Kontaktfedern', 'Kontaktfedern', 'box',
         material_id='steel', x=124, y=136, w=4, d=28, z=4, h=10, r=0.5, mass=2, materials=[['stahl', 90], ['nickel', 10]],
         color='#C9CDD0', marks=[mark('cyl', 0.5, 4, 3, fill='#9AA0A6'), mark('cyl', 0.5, 17, 3, fill='#9AA0A6')],
         info='Spiralfedern und Bleche aus vernickeltem Stahl, die die Batterien verbinden.'),
    teil('batteriefach', 'plastic_housing', 'Batteriefach mit Klappe', 'Batteriefach', 'box',
         x=120, y=130, w=60, d=40, z=1.5, h=13.5, r=3, mass=16, color='#2B2E31',
         info='Kunststoffkasten mit Kontaktfedern aus Stahl, von unten mit einer Klappe verschlossen.',
         marks=[mark('box', 4, 4, 52, 32, 2, '#1E2022')]),
    teil('klappe', 'plastic_housing', 'Batterieklappe', 'Klappe', 'box',
         x=122, y=132, w=56, d=36, z=0, h=1.5, r=3, mass=4, color='#1E2022',
         marks=raster(22, 26, 1, 3, 12, 1.2, 0, 2.5, r=0.5, fill='#34383C'),
         info='Deckel unten an der Waage. Rastnase drücken und abheben, dann die Batterien herausnehmen.'),
    *fuesse,
]
# Glas und Trägerplatte nach hinten (dy < 0) wegschieben, damit das Innenleben frei liegt; der Rest hebt leicht ab.
EX = {'glas': [0, -320, 70], 'traegerplatte': [0, -320, 0], 'lcd': [0, 60, 110], 'leitgummi': [0, 60, 88],
      'chip': [0, 60, 70], 'platine': [0, 60, 50], 'batterie_1': [0, 0, 80], 'batterie_2': [0, 0, 80],
      'kontakte': [-40, 0, 50], 'kabel': [0, 0, 40], 'batteriefach': [0, 0, 25], 'klappe': [0, 0, 0]}
for p in teile:
    if p['id'].startswith('waegezelle'):
        p['explode'] = [0, 0, 45]
    elif p['id'].startswith('fuss'):
        p['explode'] = [0, 0, 0]
    else:
        p['explode'] = EX[p['id']]
skaliere_masse(teile, oid='bathroom_scale')
schreibe('bathroom_scale', teile)
