"""3D-Modell: compact_disc. Erzeugt tools/kategorien/modelle/compact_disc.json.

CD in der klassischen Jewel-Case-Box (142 × 125 × 10 mm), liegt mit dem Deckel nach oben, Scharnier links (x = 0).
Unterteil aus klarem PS, darin die Rückseiten-Karte (Inlay) und der schwarze Einsatz (Tray) mit Haltestern.
Die Scheibe ist in ihre Schichten zerlegt: Polycarbonat-Träger, Aluminium-Spiegel, Schutzlack, Druck.
Explosion: Deckel klappt nach hinten auf (dy negativ), das Booklet schwebt darüber. Im Unterteil werden
Inlay, Tray und die Schichten der Scheibe nach oben abgehoben.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

KLAR = '#E4ECF0'
LOCH = '#5B6166'
CX, CY = 71, 62.5  # Mitte der Scheibe


def loch(w, d_loch=15, fill=LOCH):
    return mark('cyl', (w - d_loch) / 2, (w - d_loch) / 2, d_loch, fill=fill)


def rosette(px, py, n=12, rad=9, groesse=3):
    """Haltestern in der Tray-Mitte: n Zähne im Kreis um (CX, CY), relativ zum Teil bei (px, py)."""
    zaehne = [mark('box', round(CX - px + rad * math.cos(2 * math.pi * i / n) - groesse / 2, 2),
                   round(CY - py + rad * math.sin(2 * math.pi * i / n) - groesse / 2, 2), groesse, groesse, 0.8, '#3A3F44')
              for i in range(n)]
    return [mark('cyl', CX - px - 13, CY - py - 13, 26, fill='#2A2E31')] + zaehne


teile = [
    teil('deckel', 'cd_case', 'Deckel', 'Deckel', 'box',
         x=0, y=0, w=142, d=125, z=6, h=4, r=1, mass=30, color=KLAR, opacity=0.45,
         info='Glasklares Polystyrol, am linken Rand mit zwei Zapfen eingehängt. Etwas aufbiegen, dann lässt er sich '
              'abnehmen. Bricht leicht und splittert scharfkantig.',
         marks=[mark('box', 0, 2, 5, 121, 0.5, '#D3DDE2'), mark('box', 6, 4, 6, 12, 1, '#C9D3D8'),
                mark('box', 6, 109, 6, 12, 1, '#C9D3D8'), mark('box', 134, 20, 6, 16, 1, '#C9D3D8'),
                mark('box', 134, 89, 6, 16, 1, '#C9D3D8')]),
    teil('booklet', 'paper_booklet', 'Booklet', 'Booklet', 'box',
         x=11, y=2.5, w=120, d=120, z=6.6, h=1, r=0.5, mass=8, materials=[['papier', 93], ['druck', 7]],
         color='#E9D9B8',
         info='Geheftetes Heftchen mit Liedtexten, von Laschen im Deckel gehalten. Unter den Laschen herausziehen, '
              'die Heftklammern stören im Altpapier nicht.',
         marks=[mark('box', 8, 8, 104, 70, 2, '#C8423A'), mark('box', 8, 88, 70, 6, 1, '#3A3F44'),
                mark('box', 8, 100, 50, 4, 1, '#3A3F44')]),
    teil('druck', 'disc_body', 'Etikettendruck', 'Druck', 'cyl', material_id='paper',
         x=CX - 58, y=CY - 58, w=116, z=5.95, h=0.05, mass=0.1, materials=[['druck', 100]], color='#F0F0EA',
         info='Farbe, direkt auf die Scheibe gedruckt (kein Papier). Wird beim Recycling mit dem Lack abgelöst.',
         marks=[mark('cyl', 16, 16, 84, fill='#4A7BB7'), loch(116, 34)]),
    teil('lack', 'disc_body', 'Schutzlack', 'Schutzlack', 'cyl', material_id='pc',
         x=CX - 59, y=CY - 59, w=118, z=5.9, h=0.05, mass=0.3, materials=[['pcabs', 100]], color='#E6ECEF', opacity=0.7,
         info='Hauchdünne Lackschicht aus Acrylharz. Sie schützt die Spiegelschicht, denn die Daten liegen direkt darunter: '
              'Ein Kratzer auf der Oberseite zerstört die CD eher als einer unten.',
         marks=[loch(118, 34)]),
    teil('spiegel', 'disc_body', 'Aluminium-Spiegelschicht', 'Alu-Schicht', 'cyl', material_id='aluminium',
         x=CX - 59, y=CY - 59, w=118, z=5.85, h=0.05, mass=0.1, materials=[['alu', 100]], color='#D5DADE',
         info='Weniger als ein Tausendstel Millimeter Aluminium. Es spiegelt den Laser des CD-Spielers zurück.',
         marks=[mark('cyl', 10, 10, 98, fill='#C2C8CD'), loch(118, 40)]),
    teil('scheibe', 'disc_body', 'Polycarbonat-Scheibe', 'Scheibe', 'cyl',
         x=CX - 60, y=CY - 60, w=120, z=4.7, h=1.15, mass=15.5, materials=[['pcabs', 100]], color='#DDE6EA', opacity=0.75,
         info='Glasklarer Kunststoff, in den die Daten als winzige Vertiefungen (Pits) gepresst sind. '
              'Zum Unlesbarmachen zerkratzen; manche Wertstoffhöfe sammeln CDs getrennt.',
         marks=[mark('cyl', 38, 38, 44, fill='#C9D3D8'), loch(120)]),
    teil('tray', 'cd_case', 'Einsatz (Tray) mit Haltestern', 'Tray', 'box', material_id='ps',
         x=3, y=2, w=136, d=121, z=1.3, h=4.7, r=1, mass=20, color='#2F3438',
         info='Schwarzer PS-Einsatz. Der Stern in der Mitte hält die CD am Loch fest: zum Herausnehmen in der Mitte drücken. '
              'Der Tray lässt sich aus dem Unterteil heraushebeln.',
         marks=[mark('cyl', CX - 3 - 61, CY - 2 - 60.5, 122, 121, fill='#262A2E')] + rosette(3, 2)
         + [mark('box', 2, 50, 4, 22, 1, '#3A3F44'), mark('box', 130, 50, 4, 22, 1, '#3A3F44')]),
    teil('inlay', 'paper_booklet', 'Rückseiten-Karte (Inlay)', 'Inlay', 'box',
         x=2, y=1.5, w=138, d=122, z=1, h=0.3, r=0.5, mass=3, materials=[['papier', 93], ['druck', 7]], color='#D9C9A8',
         info='Papierkarte unter dem Tray mit der Titelliste und dem Rücken. Erst nach dem Tray herausnehmen, dann ins Altpapier.',
         marks=[mark('box', 0, 0, 6, 122, 0.3, '#C8423A'), mark('box', 132, 0, 6, 122, 0.3, '#C8423A')]
         + raster(20, 20, 1, 8, 90, 4, 0, 10, fill='#5B6166')),
    teil('unterteil', 'cd_case', 'Unterteil', 'Unterteil', 'box',
         x=0, y=0, w=142, d=125, z=0, h=6, r=1, mass=22, color=KLAR, opacity=0.45,
         info='Klare PS-Schale mit Scharnier. Ganze, saubere Hüllen nehmen manche Wertstoffhöfe an, sonst Restmüll: '
              'Die Gelbe Tonne ist nur für Verpackungen.',
         marks=[mark('box', 2, 1.5, 138, 122, 0.5, '#D3DDE2')]),
]

by = {p['id']: p for p in teile}
# Deckel nach hinten aufgeklappt, auf dem Tisch; Booklet darüber
oben = [by['booklet'], by['deckel']]
explodiere(oben, abstand=45, nach_liste=True)
for p in oben:
    p['explode'] = [0, -(125 + 25), round(p['explode'][2] - 6, 1)]
# Unterteil bleibt, darüber Inlay, Tray und die Schichten der Scheibe (dünne Schichten enger)
unten = [p for p in teile if p not in oben]
explodiere(unten, abstand=45, abstaende={'spiegel': 25, 'lack': 25, 'druck': 25})
skaliere_masse(teile, oid='compact_disc')
schreibe('compact_disc', teile)
