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

ECKEN = [(12, 12), (248, 12), (12, 248), (248, 248)]  # linke hintere Ecke der Füße (je 40 × 40)
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
         marks=[mark('box', 108, 243, 84, 40, 4, '#1E2022'), mark('box', 114, 249, 72, 28, 2, '#55616A')]),
    teil('traegerplatte', 'plastic_housing', 'Kunststoff-Trägerplatte', 'Trägerplatte', 'box',
         x=4, y=4, w=292, d=292, z=15, h=5, r=12, mass=120, color='#E9EAE7',
         info='Dünne ABS-Platte unter dem Glas, an der Füße, Platine und Batteriefach festgeschraubt sind.',
         marks=[mark('box', 104, 239, 84, 40, 4, '#D5D6D2'), mark('box', 116, 128, 60, 38, 3, '#D5D6D2')]),
    teil('lcd', 'lcd_panel', 'LCD-Anzeige', 'LCD', 'box',
         x=115, y=249, w=70, d=28, z=12.6, h=2.4, r=1, mass=8, materials=[['glas', 70], ['folien', 20], ['displayglas', 10]],
         info='Zwei Glasplättchen mit Flüssigkristall dazwischen, zeigt Ziffern ohne Hintergrundlicht. '
              'Ein Gummistreifen verbindet sie mit der Platine. Bricht leicht.',
         color='#9AA79A', marks=raster(8, 6, 4, 1, 12, 16, 15, r=1, fill='#5D6A5D')),
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
    teil('batteriefach', 'plastic_housing', 'Batteriefach mit Klappe', 'Batteriefach', 'box',
         x=120, y=130, w=60, d=40, z=0, h=15, r=3, mass=20, color='#2B2E31',
         info='Kunststoffkasten mit Kontaktfedern aus Stahl, von unten mit einer Klappe verschlossen.',
         marks=[mark('box', 4, 4, 52, 32, 2, '#1E2022')]),
    *fuesse,
]
explodiere(teile, abstand=40, abstaende={'chip': 14, 'lcd': 30, 'traegerplatte': 70, 'glas': 70})
skaliere_masse(teile, oid='bathroom_scale')
schreibe('bathroom_scale', teile)
