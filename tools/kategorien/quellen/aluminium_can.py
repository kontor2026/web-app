"""3D-Modell: aluminium_can. Erzeugt tools/kategorien/modelle/aluminium_can.json.

0,33-l-Getränkedose: Ø 66 mm, 115 mm hoch, ca. 13 g. Rumpf aus einem Stück tiefgezogen, unten eingezogener
Standring mit Dom, oben eingezogener Hals, aufgefalzter Deckel mit Aufreißlasche und Niete.
Rumpfabschnitte bleiben stehen, Deckel, Niete und Lasche schweben darüber, der Druck wird nach rechts gezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, skaliere_masse, schreibe  # noqa: E402

ALU = '#DDE1E4'
DEK = '#CDD3D8'
A = dict(material_id='aluminium', materials=[['alu', 100]])
C = 33


def rund(w, z, h, cx=C, cy=C):
    return dict(x=cx - w / 2, y=cy - w / 2, w=w, z=z, h=h)


INFO_R = 'Gehört zum Rumpf aus Aluminium, in einem Stück gezogen.'
teile = [
    teil('lasche', 'aluminium_can_body', 'Aufreißlasche', 'Lasche', 'box', x=26.5, y=19, w=13, d=22, z=115.6,
         h=0.6, r=5, mass=0.25, **A, color=DEK,
         info='Hebel zum Öffnen, mit der Niete am Deckel befestigt. Dranlassen: Lose fällt sie in der '
              'Sortieranlage durch und geht verloren.',
         marks=[mark('box', 3, 2.5, 7, 8, 3.5, '#8E959B')]),
    teil('niete', 'aluminium_can_body', 'Niete', 'Niete', 'cyl', **rund(4.5, 115, 0.6, cy=31), mass=0.02, **A,
         color='#A9B0B6', info='Aus dem Deckelblech selbst gedrückt, hält die Lasche. So braucht die Dose kein '
                               'zusätzliches Material.'),
    teil('deckel', 'aluminium_can_body', 'Deckel mit Falz', 'Deckel', 'cyl', **rund(57, 111, 4), mass=2.4, **A,
         color=ALU,
         info='Härtere Legierung mit Magnesium. Nach dem Befüllen wird sein Rand mit dem Rumpf zum Falz '
              'zusammengerollt, das macht die Dose dicht.',
         marks=[mark('cyl', 3.5, 3.5, 50, fill=DEK),
                mark('box', 17.5, 34, 22, 15, 7, '#AEB5BB'),
                mark('cyl', 34, 10, 6)]),
    teil('hals', 'aluminium_can_body', 'Eingezogener Hals', 'Hals', 'cyl', **rund(56, 107, 4), mass=0.25, **A,
         color=ALU, info='Der Rumpf wird oben in mehreren Stufen enger gerollt, damit ein kleinerer Deckel passt. '
                         'Das spart Aluminium.'),
    teil('hals2', 'aluminium_can_body', 'Eingezogener Hals', 'Hals', 'cyl', **rund(60, 103.5, 3.5), mass=0.25,
         **A, color=ALU, label=False, info=INFO_R),
    teil('hals3', 'aluminium_can_body', 'Eingezogener Hals', 'Hals', 'cyl', **rund(63.5, 100, 3.5), mass=0.3,
         **A, color=ALU, label=False, info=INFO_R),
    # Rumpf in vier gleich breiten Abschnitten, damit die Foto-Ansicht die glatte Hülle gerade hält (kein Fass)
    *[teil('rumpf' if k == 0 else f'rumpf{k + 1}', 'aluminium_can_body', 'Dosenrumpf', 'Rumpf', 'cyl',
           **rund(66, 8 + 23 * k, 23), mass=2.15, **A, color=ALU, label=k == 0,
           info='Aus einer Aluminiumscheibe tiefgezogen und gestreckt, die Wand ist dünner als ein Haar. '
                'Innen schützt ein Lack das Getränk vor dem Metall.' if k == 0 else INFO_R)
      for k in range(4)],
    teil('schraege', 'aluminium_can_body', 'Bodenschräge', 'Boden', 'cyl', **rund(60, 3.5, 4.5), mass=0.4, **A,
         color=ALU, label=False, info=INFO_R),
    teil('boden', 'aluminium_can_body', 'Standring mit Dom', 'Boden', 'cyl', **rund(50, 0, 3.5), mass=0.5, **A,
         color=ALU,
         info='Der Boden ist nach innen gewölbt (Dom). So hält die dünne Dose den Druck der Kohlensäure aus.'),
    teil('druck', 'aluminium_can_body', 'Außenlack und Druck', 'Druck', 'cyl', **rund(66.4, 10, 88), mass=0.25,
         materials=[['druck', 100]], color='#C8362F', sortBias=3,
         wand=0.2, boden=0, marks=[mark('cyl', 1.2, 1.2, 64, fill=ALU, zeichnung=True)],
         info='Farbe und Lack verbrennen beim Einschmelzen. Das Aluminium lässt sich danach ohne Qualitätsverlust '
              'immer wieder recyceln.'),
]
for p in teile:
    p['explode'] = {'lasche': [0, 0, 42], 'niete': [0, 0, 32], 'deckel': [0, 0, 20],
                    'druck': [100, 0, 0]}.get(p['id'], [0, 0, 0])
skaliere_masse(teile, oid='aluminium_can', stellen=2)
schreibe('aluminium_can', teile)
