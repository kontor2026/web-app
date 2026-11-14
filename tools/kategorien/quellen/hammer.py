"""3D-Modell: hammer. Erzeugt tools/kategorien/modelle/hammer.json.

Schlosserhammer 500 g (DIN 1041) mit Eschenstiel, flach auf dem Tisch: Kopf quer (x) hinten, Stiel nach vorn (y).
Der Kopf ist als Finne, Mittelteil mit Auge und Bahn modelliert (bewegen sich gemeinsam). Der Stiel steckt im Auge
und ist oben mit einem Holzkeil und einem Ringkeil verkeilt. Explodiert: Stiel bleibt liegen, Kopf schwebt darüber,
die Keile darüber.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

STAHL = '#A3AAB0'
BLANK = '#B9C0C5'
HOLZ = '#C99A62'

teile = [
    teil('holzkeil', 'wooden_handle', 'Holzkeil', 'Holzkeil', 'box',
         x=42, y=0, w=26, d=14, z=14, h=2, r=0.5, mass=3,
         info='Hartholzkeil, mit Leim in den Schlitz am Stielende getrieben. Er spreizt das Holz im Auge, '
              'damit der Kopf nicht abfliegt.',
         color='#B0824A'),
    teil('ringkeil', 'steel_hammer_head', 'Ringkeil', 'Ringkeil', 'cyl',
         x=51, y=2, w=8, d=8, z=13, h=4, mass=4,
         info='Kleiner Stahlkeil mit Ring, quer zum Holzkeil eingeschlagen. Mit Durchschlag und Hammer heraustreiben.',
         color='#8C949A', marks=[mark('cyl', 2, 2, 4, fill='#5E666C')]),
    teil('finne', 'steel_hammer_head', 'Finne', 'Finne', 'box',
         x=18, y=2, w=14, d=22, z=0, h=30, r=1, mass=60,
         info='Die keilförmige schmale Seite zum Strecken und Treiben von Blech.',
         color=STAHL, marks=[mark('box', 1, 1, 12, 20, 1, '#687076')]),
    teil('finne_mitte', 'steel_hammer_head', 'Finne (Mitte)', 'Finne', 'box',
         x=8, y=6, w=10, d=14, z=0, h=30, r=1, mass=35, label=False,
         info='Die Finne wird zur Spitze hin schmaler.', color=STAHL),
    teil('finne_spitze', 'steel_hammer_head', 'Finne (Schneide)', 'Finne', 'box',
         x=0, y=10, w=8, d=6, z=0, h=30, r=1, mass=15, label=False,
         info='Abgerundete Schneide der Finne.', color=STAHL, marks=[mark('box', 0.5, 1.5, 7, 3, 1, BLANK)]),
    teil('kopf', 'steel_hammer_head', 'Hammerkopf mit Auge', 'Kopf', 'box',
         x=32, y=0, w=48, d=26, z=0, h=30, r=3, mass=260,
         info='Geschmiedeter, gehärteter Werkzeugstahl. Das ovale Auge nimmt den Stiel auf. '
              'Erst Keile heraustreiben, dann den Kopf vom Stiel schlagen: Er gehört zum Altmetall.',
         color=STAHL, marks=[mark('box', 2, 2, 44, 22, 2, '#687076')]),
    teil('bahn', 'steel_hammer_head', 'Bahn (Schlagfläche)', 'Bahn', 'box',
         x=80, y=0, w=26, d=26, z=0, h=30, r=3, mass=135,
         info='Quadratische, gehärtete Schlagfläche. Hat sie Grate oder Risse, kann Stahl absplittern.',
         color=STAHL, marks=[mark('box', 2, 2, 22, 22, 2, '#687076')]),
    teil('fase', 'steel_hammer_head', 'Bahn mit Fase', 'Bahn', 'box',
         x=106, y=2, w=4, d=22, z=2, h=26, r=2, mass=15, label=False,
         info='Abgeschrägte Kante der Schlagfläche, damit sie nicht ausbricht.', color=BLANK),
    teil('stiel_kopf', 'wooden_handle', 'Stielende im Auge', 'Stielende', 'box',
         x=41, y=0, w=28, d=26, z=7, h=16, r=6, mass=8,
         info='Das obere Stielende ist geschlitzt und steckt im Auge. Hier sitzen die Keile.',
         color=HOLZ, marks=[mark('box', 1, 6, 26, 2, 1, '#9C7442')]),
    teil('stiel_hals', 'wooden_handle', 'Stielhals', 'Stielhals', 'box',
         x=43, y=26, w=24, d=100, z=5, h=20, r=8, mass=30, form='liegend_y',
         info='Dünnere Stelle unter dem Kopf, federt Schläge ab. Bricht ein Stiel, dann meist hier.',
         color=HOLZ, marks=[mark('box', 4, 10, 16, 80, 6, '#C99C60', zeichnung=True)]),
    teil('stiel_griff', 'wooden_handle', 'Holzstiel (Griff)', 'Stiel', 'box',
         x=40, y=126, w=30, d=194, z=3, h=24, r=11, mass=60, form='liegend_y',
         info='Eschenholz, zäh und elastisch. Unbehandeltes Holz kann wiederverwendet oder als Altholz abgegeben werden.',
         color=HOLZ, marks=[mark('box', 5, 20, 20, 160, 9, '#C99C60', zeichnung=True), mark('cyl', 11, 182, 8, fill='#8E6A3E')]),
]

explodiere(teile, abstand=35, gruppen=[['finne', 'finne_mitte', 'finne_spitze', 'kopf', 'bahn', 'fase']],
           fest=('stiel_kopf', 'stiel_hals', 'stiel_griff'))
for p in teile:  # Foto-Ansicht: flache marks schweben über runden Formen, dort nur in der Zeichnung
    if p.get('form'):
        p['marks'] = [dict(m, zeichnung=True) for m in p.get('marks') or []]
skaliere_masse(teile, oid='hammer')
schreibe('hammer', teile)
