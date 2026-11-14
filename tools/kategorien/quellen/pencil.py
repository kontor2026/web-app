"""3D-Modell: pencil. Erzeugt tools/kategorien/modelle/pencil.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

# Bleistift mit Radiergummi, aufrecht (laut CSV 8 × 8 × 175 mm), Radierer unten, angespitzte Spitze oben.
# Der Holzschaft besteht aus zwei verleimten Brettchen: explodiert klappen die Hälften zur Seite und geben die Mine frei,
# Zwinge und Radierer bleiben unten, die Spitze schwebt über der Mine.
LACK = '#E8B931'
HOLZ = '#D9B07A'
SCHAFT = 40   # Anhebung des Schafts

teile = [
    teil('minenspitze', 'graphite_core', 'Minenspitze', 'Spitze', 'cyl',
         x=3, y=3, w=2, z=171, h=4, explode=[0, 0, 60], mass=0.02,
         info='Die angespitzte Mine. Weiche Minen (B) enthalten mehr Grafit, harte (H) mehr Ton.',
         color='#3A3F44'),
    teil('holzspitze_2', 'wooden_pencil_body', 'Angespitztes Holz (vorne)', 'Holzkegel', 'cyl',
         x=2, y=2, w=4, z=166, h=5, explode=[0, 0, 60], mass=0.05, label=False,
         info='Der schmale Teil des Holzkegels, den der Spitzer stehen lässt.',
         color=HOLZ, marks=[mark('cyl', 1, 1, 2, fill='#3A3F44')]),
    teil('holzspitze_1', 'wooden_pencil_body', 'Angespitztes Holz', 'Holzkegel', 'cyl',
         x=1, y=1, w=6, z=160, h=6, explode=[0, 0, 60], mass=0.15,
         info='Beim Spitzen entsteht ein Kegel aus blankem Holz. Unlackierte Späne dürfen in die Biotonne, '
              'lackierte Reste in den Restmüll.',
         color=HOLZ, marks=[mark('cyl', 2, 2, 2, fill='#3A3F44')]),
    teil('mine', 'graphite_core', 'Grafitmine', 'Mine', 'cyl',
         x=3, y=3, w=2, z=13, h=158, explode=[0, 0, SCHAFT], mass=0.5,
         info='Gebrannte Mischung aus Grafit und Ton, kein Blei. Sie ist in die Holzrille eingeleimt und lässt sich nicht herausnehmen.',
         color='#3A3F44'),
    teil('holz_links', 'wooden_pencil_body', 'Holzhälfte links', 'Holz links', 'box',
         x=0, y=0, w=4, d=8, z=13, h=147, r=1.5, explode=[-10, 0, SCHAFT], mass=1.8,
         info='Zwei Brettchen aus Zedern- oder Lindenholz mit Rille für die Mine werden verleimt und sechseckig gefräst. '
              'Der Lack macht das Holz ungeeignet für die Biotonne.',
         color=LACK, marks=[mark('box', 3, 3, 1, 2, fill=HOLZ)]),
    teil('holz_rechts', 'wooden_pencil_body', 'Holzhälfte rechts', 'Holz rechts', 'box',
         x=4, y=0, w=4, d=8, z=13, h=147, r=1.5, explode=[10, 0, SCHAFT], mass=1.8,
         info='Das zweite Brettchen. Zusammen mit der Mine macht Holz über 80 Prozent des Bleistifts aus.',
         color=LACK, marks=[mark('box', 0, 3, 1, 2, fill=HOLZ)]),
    teil('zwinge', 'pencil_ferrule', 'Zwinge', 'Zwinge', 'cyl',
         x=0.3, y=0.3, w=7.4, z=3, h=13, explode=[0, 0, 15], mass=0.25,
         info='Dünnes Aluminiumröhrchen, auf Holz und Radierer gequetscht. Mit einer Zange abdrehen, '
              'dann ist das Metall vom Holz getrennt.',
         color='#C9CDD0', marks=[mark('cyl', 0.6, 0.6, 6.2, fill='#B0B6BA')]),
    teil('radierer', 'rubber_eraser', 'Radiergummi', 'Radierer', 'cyl',
         x=0.8, y=0.8, w=6.4, z=0, h=9, explode=[0, 0, 0], mass=0.35, materials=[['gummi', 70], ['tpe', 30]],
         info='Synthetischer Kautschuk oder PVC-freier Kunststoff. Nach dem Abziehen der Zwinge lässt er sich herausziehen.',
         color='#E58A8A'),
]

skaliere_masse(teile, oid='pencil', stellen=2)
schreibe('pencil', teile)
