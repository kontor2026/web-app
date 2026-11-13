"""3D-Modell: disposable_razor. Erzeugt tools/kategorien/modelle/disposable_razor.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Einwegrasierer mit zwei Klingen flach liegend, Klingen nach oben (laut CSV 35 × 140 × 20 mm), Kopf hinten (y = 0).
# Im Kunststoffkopf liegen zwei Stahlklingen, gehalten von zwei Aluminiumklammern; davor ein Gleitstreifen,
# dahinter der gerippte Schutzsteg. Explodiert: Griff nach vorne abgezogen, Klingen und Kleinteile über dem Kopf.
PP = '#2F6DB5'
STAHL = '#C3C9CE'

teile = [
    teil('gleitstreifen', 'razor_blade_head', 'Gleitstreifen', 'Gleitstreifen', 'box', material_id='ps',
         x=3, y=1, w=29, d=4.5, z=14, h=3, r=1.5, mass=0.4, materials=[['ps', 100]],
         info='Kunststoffstreifen mit Gleitmittel (z. B. Aloe Vera), das sich beim Nassrasieren löst. '
              'Wird er hell, ist der Rasierer verbraucht.',
         color='#7FC7A8', marks=raster(1, 1, 7, 1, 3, 2.5, 4, r=1, fill='#A8DCC4')),
    teil('klammer_l', 'razor_blade_head', 'Halteklammer links', 'Klammer', 'box', material_id='aluminium',
         x=0.5, y=5, w=2.5, d=10, z=13.5, h=3.5, r=0.8, mass=0.05,
         info='Dünner Aluminiumbügel, der die Klingen im Kopf festhält.', color='#B0B6BA'),
    teil('klammer_r', 'razor_blade_head', 'Halteklammer rechts', 'Klammer', 'box', material_id='aluminium',
         x=32, y=5, w=2.5, d=10, z=13.5, h=3.5, r=0.8, mass=0.05, label=False,
         info='Gegenstück zur linken Halteklammer.', color='#B0B6BA'),
    teil('klinge_1', 'razor_blade_head', 'Klinge vorne', 'Klinge', 'box',
         x=3, y=6, w=29, d=3.5, z=14, h=0.6, r=0.3, mass=0.25,
         info='Hauchdünne Edelstahlklinge, extrem scharf. Den Rasierer nie zerlegen, sondern mit Schutzkappe '
              'oder in Klebeband gewickelt in den Restmüll geben.',
         color=STAHL, marks=[mark('box', 0, 0, 29, 0.8, fill='#E8ECEE')]),
    teil('klinge_2', 'razor_blade_head', 'Klinge hinten', 'Klinge', 'box',
         x=3, y=10, w=29, d=3.5, z=14, h=0.6, r=0.3, mass=0.25, label=False,
         info='Zweite Klinge, sie schneidet das Haar ein zweites Mal etwas tiefer.',
         color=STAHL, marks=[mark('box', 0, 0, 29, 0.8, fill='#E8ECEE')]),
    teil('schutzsteg', 'razor_blade_head', 'Schutzsteg mit Rippen', 'Schutzsteg', 'box', material_id='pp',
         x=3, y=15, w=29, d=4, z=14, h=2, r=1, mass=0.3, materials=[['pp', 100]],
         info='Gerippter Kunststoffsteg vor den Klingen. Er spannt die Haut, damit die Klingen nicht einschneiden.',
         color='#1F4F86', marks=raster(1, 0.5, 14, 1, 1, 3, 2)),
    teil('kopf', 'razor_blade_head', 'Klingenkopf', 'Kopf', 'box', material_id='pp',
         x=0, y=0, w=35, d=20, z=8, h=6, r=3, mass=1.6, materials=[['pp', 100]],
         info='Kunststoffrahmen, in dem Klingen, Klammern und Gleitstreifen stecken. Er ist mit dem Griff verschweißt '
              'oder aufgesteckt.',
         color=PP, marks=[mark('box', 3, 5.5, 29, 8.5, 1, '#1F4F86')]),
    teil('griff', 'razor_handle', 'Griff', 'Griff', 'box',
         x=11.5, y=16, w=12, d=124, z=0, h=9, r=6, explode=[0, 30, 0], mass=11,
         info='Griff aus Polypropylen. Einwegrasierer erzeugen viel Müll; Rasierer mit Wechselklingen '
              'oder aus Metall halten jahrelang.',
         color=PP, marks=[mark('box', 2, 20, 8, 40, 4, '#E8ECEE')] + raster(3, 24, 1, 6, 6, 2, 0, 6, r=1, fill='#C3C9CE')),
]

explodiere(teile, abstand=10)
skaliere_masse(teile, oid='disposable_razor', stellen=2)
schreibe('disposable_razor', teile)
