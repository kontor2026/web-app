"""3D-Modell: frying_pan. Erzeugt tools/kategorien/modelle/frying_pan.json.

Typische beschichtete Aluminium-Bratpfanne (Ø 24 cm) mit eingepresster Induktionsscheibe aus Stahl und
angeschraubtem Bakelit-Stiel. Die CSV (280 × 280 mm) lässt nur einen kurzen Stiel zu (y 236..308), der echte
Stiel wäre etwa 20 cm lang. Körper aus vier Zylinderabschnitten (schräge Wand), Beschichtung schwebt darüber,
Induktionsscheibe liegt unten; Stiel, Schraube und Griffhalter werden nach vorne herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

ALU = '#B9BEC3'
BESCH = '#2B2B2E'
GRIFF = '#1F2124'

teile = [
    teil('beschichtung', 'nonstick_pan_body', 'Antihaftbeschichtung', 'Beschichtung', 'cyl', material_id='aluminium',
         x=22, y=22, w=192, z=5, h=0.5, mass=12, materials=[['ptfe', 100]],
         info='Hauchdünne Schicht aus PTFE (Teflon), eingebrannt auf das Aluminium. Sie lässt sich nicht ablösen: '
              'Zerkratzte Pfannen komplett als Metallschrott abgeben.',
         color=BESCH, marks=[mark('cyl', 30, 30, 132, fill='#36363A'), mark('cyl', 70, 70, 52, fill='#3A3A3F')]),
    teil('rand', 'nonstick_pan_body', 'Pfannenrand', 'Rand', 'cyl',
         x=0, y=0, w=236, z=35, h=10, mass=120,
         info='Oberer Rand der Pfanne mit leicht nach außen gebogener Kante, damit beim Ausgießen nichts tropft.',
         color=ALU, marks=[mark('cyl', 3, 3, 230, fill=BESCH)]),
    teil('wand_oben', 'nonstick_pan_body', 'Pfannenwand oben', 'Wand', 'cyl',
         x=4, y=4, w=228, z=20, h=15, mass=150, label=False,
         info='Schräge Wand aus gepresstem Aluminium, außen hitzefest lackiert.', color=ALU),
    teil('wand_unten', 'nonstick_pan_body', 'Pfannenwand unten', 'Wand unten', 'cyl',
         x=10, y=10, w=216, z=5, h=15, mass=160, label=False,
         info='Unterer Teil der schrägen Pfannenwand.', color=ALU),
    teil('boden', 'nonstick_pan_body', 'Pfannenboden', 'Boden', 'cyl',
         x=18, y=18, w=200, z=1, h=4, mass=330,
         info='Dicker Aluminiumboden, etwa 4 mm stark, damit er sich beim Erhitzen nicht verzieht. Aluminium ist '
              'leicht und leitet Wärme sehr gut.',
         color=ALU, marks=[mark('cyl', 25, 25, 150, fill='#AEB3B8')]),
    teil('induktion', 'nonstick_pan_body', 'Induktionsscheibe', 'Induktion', 'cyl', material_id='steel',
         x=33, y=33, w=170, z=0, h=1.2, mass=130,
         info='Gelochte Scheibe aus magnetischem Edelstahl, in den Boden eingepresst. Nur damit funktioniert die Pfanne '
              'auf dem Induktionsherd.',
         color='#9EA5AA', marks=[mark('cyl', 10 + 30 * i, 80, 8, fill='#B9BEC3') for i in range(6)]
                                 + [mark('cyl', 80, 10 + 30 * i, 8, fill='#B9BEC3') for i in range(6) if i != 2]),
    teil('griffhalter', 'nonstick_pan_body', 'Griffhalter', 'Halter', 'box', material_id='aluminium',
         x=106, y=226, w=24, d=22, z=30, h=13, r=5, explode=[0, 40, 0], mass=30,
         info='Angegossener Aluminiumzapfen an der Pfannenwand. Darauf wird der Stiel gesteckt und verschraubt.',
         color=ALU, marks=[mark('cyl', 9, 8, 6, fill='#6E757A')]),
    teil('schraube', 'bakelite_handle', 'Stielschraube', 'Schraube', 'box', material_id='steel',
         x=115, y=236, w=6, d=66, z=33.5, h=6, r=3, explode=[0, 70, 25], mass=12,
         info='Lange Stahlschraube, die durch den hohlen Stiel in den Halter greift. Am Stielende mit einem '
              'Schraubendreher lösen, dann geht der Stiel ab.',
         color='#9AA2A6', marks=[mark('box', 0.5, 62, 5, 4, 1, fill='#5A6268')]),
    teil('stiel', 'bakelite_handle', 'Bakelit-Stiel', 'Stiel', 'box',
         x=104, y=236, w=28, d=72, z=28, h=22, r=10, explode=[0, 70, 0], mass=110,
         info='Phenolharz (Bakelit) wird beim Erhitzen nicht weich und kann nicht recycelt werden. Abgeschraubt kommt '
              'er in den Restmüll, die Pfanne zum Metallschrott.',
         color=GRIFF, marks=[mark('box', 8, 10, 12, 50, 6, fill='#2E3136'), mark('cyl', 10, 60, 8, fill='#45494E')]),
]
explodiere(teile, abstand=18, nach_liste=True, gruppen=[['rand', 'wand_oben', 'wand_unten', 'boden']])
skaliere_masse(teile, oid='frying_pan')
schreibe('frying_pan', teile)
