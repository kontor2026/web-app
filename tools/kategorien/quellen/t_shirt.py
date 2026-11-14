"""3D-Modell: t_shirt. Erzeugt tools/kategorien/modelle/t_shirt.json.

Kurzarm-T-Shirt flach ausgebreitet, Kragen hinten (y = 0), Saum vorne. 300 × 400 × 11 mm.
Vorderteil und Ärmel sind aus wenigen, nach oben schmaleren Scheiben gebaut: In der Foto-Ansicht werden sie zu
einer weich gewölbten Stofflage verbunden. Der Kragen ist ein echter Ring.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, schreibe  # noqa: E402

STOFF = '#2D5684'
SAUM = '#244A73'
BW = [['baumwolle', 98], ['polyester', 2]]


def schichten(pid, comp, name, short, z0, lagen, mass, info, marks=None, **kw):
    """Scheiben (x, y, w, d, h, r) von unten nach oben, lückenlos ab z0. Die oberste trägt Nummer und marks."""
    vol = sum(w * d * h for _, _, w, d, h, _ in lagen)
    out, z = [], z0
    for i, (x, y, w, d, h, r) in enumerate(lagen):
        oben = i == len(lagen) - 1
        out.append(teil(f'{pid}_{i}', comp, name, short, 'box', x=x, y=y, w=w, d=d, z=round(z, 2), h=h, r=r,
                        mass=round(mass * w * d * h / vol, 2), info=info, label=None if oben else False,
                        marks=marks if oben else None, **kw))
        z += h
    return out[::-1]


vorder = schichten('vorderteil', 'cotton_fabric', 'Vorderteil', 'Vorderteil', 2, [
    (35, 20, 230, 380, 2.5, 8),
    (38, 23, 224, 373, 2.5, 16),
    (44, 30, 212, 360, 2, 30),
    (56, 44, 188, 334, 1.5, 50),
], 52,
    'Baumwoll-Single-Jersey. Tragbare Shirts in die Altkleidersammlung, kaputte zum Textilrecycling: '
    'Daraus werden Putzlappen oder Dämmstoff.', materials=BW, color=STOFF,
    marks=[mark('box', 59, 54, 70, 50, 10, '#E3E0D8')])


def aermel(seite, x, ex):
    # Ärmel: flach gedrückter Schlauch, an der Schulter breit, zum Saum hin leicht gewölbt
    return schichten(f'aermel_{seite}', 'cotton_fabric', f'Ärmel {"links" if seite == "l" else "rechts"}', 'Ärmel', 0, [
        (x, 26, 56, 140, 2.5, 14),
        (x + 2, 29, 52, 134, 2.5, 18),
        (x + 5, 34, 46, 124, 2, 20),
    ], 16, 'Doppellagiger Ärmel, an der Schulter angesetzt. Der umgenähte Saum verhindert, dass der Stoff ausfranst.',
        materials=BW, color=STOFF, explode=ex)


al, ar = aermel('l', 0, [-90, 170, 0]), aermel('r', 244, [90, 0, 0])
for p in ar:
    p['label'] = False

teile = [
    teil('kragen', 'cotton_fabric', 'Kragenbündchen', 'Kragen', 'cyl', form='torus',
         x=108, y=12, w=84, d=50, z=6, h=5, mass=7, materials=[['baumwolle', 95], ['polyester', 5]], color=SAUM,
         info='Elastischer Rippstrick, rund an den Halsausschnitt genäht. Etwas Elasthan sorgt dafür, dass er nicht ausleiert.',
         marks=[mark('cyl', 7, 6, 70, 38, fill='#2E5277', zeichnung=True)]),
] + vorder + [
    teil('etikett', 'care_label', 'Pflegeetikett', 'Etikett', 'box',
         x=140, y=24, w=20, d=20, z=2, h=0.3, r=1, mass=0.5, materials=[['polyester', 100]], color='#F4F2EE',
         info='Polyester-Etikett mit Waschsymbolen und Fasergehalt. Vor dem Recycling an der Naht abschneiden, '
              'weil es ein anderes Material ist.',
         marks=[mark('box', 3, 4, 14, 2, 0, '#8E969A'), mark('box', 3, 8, 14, 2, 0, '#8E969A'),
                mark('box', 3, 12, 10, 2, 0, '#8E969A')]),
    teil('rueckenteil', 'cotton_fabric', 'Rückenteil', 'Rückenteil', 'box',
         x=35, y=20, w=230, d=380, z=0, h=2, r=8, mass=56, materials=BW, color=STOFF,
         info='Gleicher Stoff wie vorne, an Schultern und Seiten mit Polyestergarn vernäht. Zum Trennen die Nähte aufschneiden.',
         marks=[mark('box', 0, 366, 230, 3, 0, SAUM, zeichnung=True)]),
] + al + ar

explodiere(teile, abstand=90, gruppen=[[p['id'] for p in vorder]])
schreibe('t_shirt', teile)
