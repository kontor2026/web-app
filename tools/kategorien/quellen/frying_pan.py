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
AUSSEN = '#45464B'   # außen hitzefest lackiert (Foto-Ansicht)
BESCH = '#2B2B2E'
GRIFF = '#1F2124'

LOCH = '#EEECE5'
STIEL_DY = 80

teile = [
    teil('beschichtung', 'nonstick_pan_body', 'Antihaftbeschichtung', 'Beschichtung', 'cyl', material_id='aluminium',
         x=22, y=22, w=192, z=5, h=0.5, mass=12, materials=[['ptfe', 100]],
         info='Hauchdünne Schicht aus PTFE (Teflon), eingebrannt auf das Aluminium. Sie lässt sich nicht ablösen: '
              'Zerkratzte Pfannen komplett als Metallschrott abgeben.',
         color=BESCH, marks=[mark('cyl', 30, 30, 132, fill='#36363A'), mark('cyl', 70, 70, 52, fill='#3A3A3F')]),
    teil('rand', 'nonstick_pan_body', 'Pfannenrand', 'Rand', 'cyl',
         x=0, y=0, w=236, z=35, h=10, mass=120,
         info='Oberer Rand der Pfanne mit leicht nach außen gebogener Kante, damit beim Ausgießen nichts tropft.',
         color=AUSSEN, wand=8, boden=0,
         marks=[dict(m, zeichnung=True) for m in (
             mark('cyl', 3, 3, 230, fill='#3A3A3F'), mark('cyl', 12, 12, 212, fill='#333337'),
             mark('cyl', 22, 22, 192, fill=BESCH), mark('cyl', 50, 50, 136, fill='#2F2F33'),
             mark('cyl', 54, 54, 128, fill=BESCH), mark('cyl', 90, 90, 56, fill='#2F2F33'),
             mark('cyl', 94, 94, 48, fill=BESCH))]),
    teil('wand_oben', 'nonstick_pan_body', 'Pfannenwand oben', 'Wand', 'cyl',
         x=4, y=4, w=228, z=20, h=15, mass=150, label=False,
         info='Schräge Wand aus gepresstem Aluminium, außen hitzefest lackiert.', color=AUSSEN, wand=8, boden=0),
    teil('wand_unten', 'nonstick_pan_body', 'Pfannenwand unten', 'Wand unten', 'cyl',
         x=10, y=10, w=216, z=5, h=15, mass=160, label=False,
         info='Unterer Teil der schrägen Pfannenwand.', color=AUSSEN, wand=8, boden=0),
    teil('boden', 'nonstick_pan_body', 'Pfannenkörper aus Aluminium', 'Pfannenkörper', 'cyl',
         x=18, y=18, w=200, z=1, h=4, mass=330,
         info='Gepresstes Aluminium mit etwa 4 mm dickem Boden, damit er sich beim Erhitzen nicht verzieht. '
              'Aluminium ist leicht und leitet Wärme sehr gut.',
         color=BESCH, marks=[mark('cyl', 25, 25, 150, fill='#AEB3B8', zeichnung=True)]),
    teil('induktion', 'nonstick_pan_body', 'Induktionsscheibe', 'Induktion', 'cyl', material_id='steel',
         x=33, y=33, w=170, z=0, h=1.2, mass=130,
         info='Gelochte Scheibe aus magnetischem Edelstahl, in den Boden eingepresst. Nur damit funktioniert die Pfanne '
              'auf dem Induktionsherd.',
         color='#9EA5AA', marks=[mark('cyl', 10 + 30 * i, 80, 8, fill='#B9BEC3') for i in range(6)]
                                 + [mark('cyl', 80, 10 + 30 * i, 8, fill='#B9BEC3') for i in range(6) if i != 2]),
    teil('griffhalter', 'nonstick_pan_body', 'Griffhalter', 'Halter', 'box', material_id='aluminium',
         x=106, y=226, w=24, d=22, z=30, h=13, r=5, mass=30,
         info='Angegossener Aluminiumzapfen an der Pfannenwand. Darauf wird der Stiel gesteckt und verschraubt.',
         color=ALU, marks=[mark('cyl', 9, 8, 6, fill='#6E757A')]),
    teil('schraube', 'bakelite_handle', 'Stielschraube', 'Schraube', 'box', material_id='steel',
         x=115, y=240, w=6, d=66, z=34, h=6, r=3, explode=[0, STIEL_DY, 30], mass=12, form='liegend_y',
         info='Lange Stahlschraube, die durch den hohlen Stiel in den Halter greift. Am Stielende mit einem '
              'Schraubendreher lösen, dann geht der Stiel ab.',
         color='#9AA2A6', marks=[mark('box', 0.5, 62, 5, 4, 1, fill='#5A6268')]),
    teil('huelse', 'bakelite_handle', 'Flammschutz-Hülse', 'Hülse', 'box', material_id='steel',
         x=105, y=236, w=26, d=12, z=28, h=20, r=6, explode=[0, STIEL_DY / 2, 0], mass=15, form='liegend_y',
         info='Edelstahlring zwischen Pfanne und Stiel. Er schützt den Kunststoff vor der Gasflamme.',
         color='#C9CED2', marks=[mark('box', 3, 3, 20, 6, 3, fill='#B5BBC0')]),
    teil('stiel', 'bakelite_handle', 'Bakelit-Stiel', 'Stiel', 'box',
         x=106, y=248, w=24, d=26, z=28, h=20, r=6, explode=[0, STIEL_DY, 0], mass=45, form='liegend_y',
         info='Phenolharz (Bakelit) wird beim Erhitzen nicht weich und kann nicht recycelt werden. Abgeschraubt kommt '
              'er in den Restmüll, die Pfanne zum Metallschrott.',
         color=GRIFF, marks=[mark('box', 6, 3, 12, 22, 5, fill='#2E3136')]),
    teil('stiel_ende', 'bakelite_handle', 'Stielende mit Aufhängeloch', 'Stielende', 'box',
         x=102, y=274, w=32, d=34, z=29, h=21, r=12, explode=[0, STIEL_DY, 0], mass=65, label=False, form='liegend_y',
         info='Das breite Ende liegt gut in der Hand. Durch das Loch kann man die Pfanne aufhängen.',
         color=GRIFF, marks=[mark('box', 6, 0, 20, 14, 5, fill='#2E3136'), mark('cyl', 9, 17, 14, 11, fill=LOCH, zeichnung=True)]),
]
explodiere(teile, abstand=18, nach_liste=True, gruppen=[['rand', 'wand_oben', 'wand_unten', 'boden']],
           fest=('griffhalter', 'schraube', 'huelse', 'stiel', 'stiel_ende'),
           abstaende={'beschichtung': 70, 'boden': 60})
for p in teile:  # Halter gehört zum Pfannenkörper, wird aber etwas nach vorne gezogen
    if p['id'] == 'griffhalter':
        p['explode'] = [0, 25, next(q['explode'][2] for q in teile if q['id'] == 'rand')]
for p in teile:  # Foto-Ansicht: flache marks schweben über runden Formen, dort nur in der Zeichnung
    if p.get('form'):
        p['marks'] = [dict(m, zeichnung=True) for m in p.get('marks') or []]
skaliere_masse(teile, oid='frying_pan')
schreibe('frying_pan', teile)
