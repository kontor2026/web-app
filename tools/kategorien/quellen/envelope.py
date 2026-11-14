"""3D-Modell: envelope. Erzeugt tools/kategorien/modelle/envelope.json.

Fensterbriefumschlag DIN lang (220 × 110 mm, 80-g-Papier), Vorderseite mit Fenster oben, Klappe nach hinten
umgeschlagen und noch nicht zugeklebt (liegt unter dem Umschlag). Fenster 90 × 45 mm, 20 mm vom linken Rand.
Die Lagen werden nach oben abgehoben, Kleber knapp über der Klappe.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

WEISS = '#F6F4EE'
teile = [
    teil('vorderseite', 'paper_envelope_body', 'Vorderseite mit Fensterausschnitt', 'Vorderseite', 'box',
         x=0, y=0, w=220, d=110, z=0.9, h=0.3, r=0.5, mass=2.0, materials=[['papier', 98], ['druck', 2]],
         color=WEISS,
         info='Weißes Papier mit ausgestanztem Fenster. Der ganze Umschlag darf ins Altpapier, '
              'große Fenster vorher herausreißen.',
         marks=[mark('box', 20, 50, 90, 45, 2, '#DDE7EC'), mark('box', 26, 56, 50, 3, 0, '#9AA3A8'),
                mark('box', 26, 64, 60, 4, 0, '#3A3F44'), mark('box', 26, 72, 52, 4, 0, '#3A3F44'),
                mark('box', 26, 80, 40, 4, 0, '#3A3F44'), mark('box', 180, 8, 30, 24, 1, '#E7E3D8')]),
    teil('fenster', 'window_film', 'Sichtfenster (Folie)', 'Fenster', 'box',
         x=17, y=47, w=96, d=51, z=0.8, h=0.1, r=1, mass=0.25, color='#E3F0F6', opacity=0.6,
         info='Dünne Polypropylen- oder Pergaminfolie, innen auf den Rand geklebt. Kleine Fenster '
              'stören im Altpapier nicht, man kann sie aber herausreißen und in den Restmüll geben.'),
    teil('rueckseite', 'paper_envelope_body', 'Rückseite mit Seitenlaschen', 'Rückseite', 'box',
         x=0, y=0, w=220, d=110, z=0.5, h=0.3, r=0.5, mass=2.0, materials=[['papier', 96], ['druck', 4]],
         color='#EFEDE6',
         info='Bodenteil und Seitenlaschen sind verklebt. Innen ist ein Sicherheitsdruck, damit man den Brief '
              'nicht durchscheinen sieht.',
         marks=[mark('box', 4, 44, 212, 62, 0.5, '#D3D8DF')] + [mark('box', 4, 48 + 8 * i, 212, 2, 0, '#BCC3CD') for i in range(7)]),
    teil('klebestreifen', 'paper_envelope_body', 'Gummierung', 'Gummierung', 'box',
         x=8, y=4, w=204, d=10, z=0.3, h=0.05, r=1, mass=0.1, materials=[['klebstoff', 100]], color='#E8DDB5',
         info='Wasseraktivierter Kleber am Klappenrand. Ist im Altpapier kein Problem.'),
    teil('klappe', 'paper_envelope_body', 'Verschlussklappe', 'Klappe', 'box',
         x=0, y=0, w=220, d=40, z=0, h=0.3, r=0.5, mass=0.65, color=WEISS,
         info='Wird über die Rückseite geklappt und angefeuchtet oder angedrückt.',
         marks=[mark('box', 0, 0, 220, 3, 0, '#DDDAD0')]),
]
explodiere(teile, abstand=55, abstaende={'klebestreifen': 15})
skaliere_masse(teile, oid='envelope', stellen=2)
schreibe('envelope', teile)
