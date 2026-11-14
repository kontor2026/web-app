"""3D-Modell: wire_hanger. Erzeugt tools/kategorien/modelle/wire_hanger.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Drahtkleiderbügel aus der Reinigung, flach liegend (laut CSV 400 × 200 × 5 mm), Haken hinten (y = 0).
# Ein einziger Stahldraht (Ø ca. 2,2 mm): Haken, verdrillter Hals, zwei schräge Schultern, Unterstange.
# Da es nur achsparallele Formen gibt, sind die Schultern als feine Treppe aus 30 Drahtstücken gebaut, die sich an
# den Ecken berühren. Hakeninneres in Tischfarbe. Explodiert: Abschnitte in der Ebene auseinandergezogen, Haken leicht angehoben.
STAHL = '#AEB5BA'
LOCH = '#EEECE5'
DRAHT = 3
N = 30


def schulter(seite, dx):
    """Schräge Schulter von der Verdrillung (y = 78) bis zur Ecke (y = 192) als N Drahtstücke."""
    w, d = 194 / N, 114 / N
    teile = []
    for i in range(N):
        x = 198 - (i + 1) * w if seite == 'l' else 202 + i * w
        erstes = i == 0
        teile.append(teil(f'schulter_{seite}_{i + 1}', 'steel_wire',
                          'Schulter links' if seite == 'l' else 'Schulter rechts', 'Schulter', 'box',
                          x=round(x, 3), y=round(78 + i * d, 3), w=round(w, 3), d=round(d, 3), z=0, h=DRAHT, r=0.5, form='liegend_x',
                          explode=[dx, 0, 0], mass=0.3, label=erstes,
                          info=('Die schrägen Schultern geben dem Kleidungsstück seine Form. Der Draht ist dünn '
                                'verzinkt oder lackiert gegen Rost.') if erstes else 'Abschnitt der schrägen Schulter.',
                          color=STAHL))
    return teile


teile = [
    teil('haken', 'steel_wire', 'Haken', 'Haken', 'cyl',
         x=184, y=0, w=34, d=30, z=1, h=DRAHT, explode=[0, -30, 10], mass=3,
         info='Der Haken ist das Drahtende, zu einem Bogen gebogen. Viele Reinigungen nehmen Drahtbügel zurück '
              'und verwenden sie wieder.',
         color=STAHL, form='torus', marks=[mark('cyl', 3, 3, 28, 24, fill=LOCH, zeichnung=True), mark('box', 0, 17, 10, 13, 2, LOCH, zeichnung=True)]),
    teil('hakenschaft', 'steel_wire', 'Hakenschaft', 'Hakenschaft', 'box',
         x=199.5, y=30, w=3, d=26, z=1, h=DRAHT, r=1.5, form='liegend_y', explode=[0, -30, 10], mass=1, label=False,
         info='Gerades Drahtstück zwischen Haken und Verdrillung.', color=STAHL),
    teil('verdrillung', 'steel_wire', 'Verdrillter Hals', 'Verdrillung', 'box',
         x=196, y=56, w=10, d=22, z=0, h=5, r=3, form='liegend_y', explode=[0, -14, 5], mass=2,
         info='Hier sind Anfang und Ende des Drahts mehrfach umeinander gedreht. So hält der Bügel ohne Schweißen '
              'oder Kleben zusammen.',
         color=STAHL, marks=raster(1, 1.5, 1, 5, 8, 2, 0, 4, r=1, fill='#7E868C')),
    *schulter('l', -15),
    *schulter('r', 15),
    teil('unterstange', 'steel_wire', 'Unterstange', 'Unterstange', 'box',
         x=2, y=192, w=396, d=4, z=0, h=DRAHT, r=2, form='liegend_x', explode=[0, 20, 0], mass=16,
         info='Gerade Stange für Hosen, an den Enden zu den Schultern umgebogen. Ausgediente Bügel gehören '
              'zum Altmetall, nicht in die Gelbe Tonne.',
         color=STAHL),
]

for p in teile:  # Foto-Ansicht: flache marks schweben über runden Formen, dort nur in der Zeichnung
    if p.get('form'):
        p['marks'] = [dict(m, zeichnung=True) for m in p.get('marks') or []]
skaliere_masse(teile, oid='wire_hanger', stellen=2)
schreibe('wire_hanger', teile)
