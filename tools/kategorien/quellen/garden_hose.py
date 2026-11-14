"""3D-Modell: garden_hose. Erzeugt tools/kategorien/modelle/garden_hose.json.

Typischer 1/2-Zoll-Gartenschlauch (20 m, Außen-Ø 19 mm), flach aufgerollt zu einer Rolle von Ø 400 mm mit
drei Windungen übereinander (60 mm). Wie bei usb_cable werden die drei Schichten (Außenmantel, Gewebe,
Innenschlauch) als Rolle nach oben abgehoben. Die Anschlussteile liegen zusammengebaut hinten im Loch der Rolle und
schweben explodiert über der obersten Schicht: Schlauchstück mit Überwurfmutter und O-Ring, Hahnanschluss.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

D = 400
LOCH = 250
GRUEN = '#3E8E4A'


BODEN = '#DCD8CE'  # Tisch, durch das Loch gesehen


def windungen(dm, n=7, breite=10.5, fill=None, tiefe=60):
    """Konzentrische Ringe als Umrisse der Windungen, außen beginnend; innen das Loch mit Innenwand und Tisch.
    Nur für die Zeichnung: in der Foto-Ansicht ist jede Schicht ein echter Ring (form='torus')."""
    out = []
    for i in range(n + 1):
        w = dm - 2 * i * breite
        out.append(mark('cyl', (dm - w) / 2, (dm - w) / 2, w, fill=fill if i == n else None, zeichnung=True))
    innen = dm - 2 * n * breite
    k = innen - tiefe * 1.41
    v = (dm - k) / 2 + tiefe / 2
    out.append(mark('cyl', round(v, 1), round(v, 1), round(k, 1), fill=BODEN, zeichnung=True))
    return out


teile = [
    # Schlauchstück (Schnellkupplung) liegt waagerecht im Loch der Rolle, Schlauchseite links
    teil('ueberwurf', 'hose_connector', 'Überwurfmutter', 'Überwurf', 'box',
         x=125, y=130, w=30, d=32, z=0, h=32, r=6, sortBias=60, mass=12, form='liegend_x',
         info='Wird über die Spreizkrallen geschraubt und presst sie auf den Schlauch. Aufdrehen und abziehen, '
              'dann ist der Anschluss vom Schlauch getrennt.',
         color='#F2A23A', marks=[mark('box', 4, 2, 2, 28, 1, '#D5892A', zeichnung=True), mark('box', 10, 2, 2, 28, 1, '#D5892A', zeichnung=True),
                                 mark('box', 16, 2, 2, 28, 1, '#D5892A', zeichnung=True), mark('box', 22, 2, 2, 28, 1, '#D5892A', zeichnung=True)]),
    teil('kupplung', 'hose_connector', 'Schlauchstück mit Spreizkrallen', 'Schlauchstück', 'box',
         x=155, y=133, w=50, d=26, z=3, h=26, r=5, sortBias=60, mass=18, form='liegend_x',
         info='PP-Kupplung, die auf Wasserhahn, Brause oder Spritze klickt. Die Krallen greifen in den Schlauch. '
              'Ganz aus Kunststoff, aber keine Verpackung: zum Wertstoffhof.',
         color='#5B6066', marks=[mark('box', 2, 4, 14, 18, 2, '#F2A23A', zeichnung=True), mark('box', 30, 3, 18, 20, 4, '#464B50', zeichnung=True)]),
    teil('oring', 'hose_connector', 'O-Ring-Dichtung', 'O-Ring', 'box',
         material_id='rubber', x=205, y=138, w=3, d=16, z=8, h=16, r=1, sortBias=60, mass=0.5, form='liegend_x',
         materials=[['gummi', 100]],
         info='Gummiring vorn in der Kupplung, er dichtet zum Gegenstück ab. Tropft der Anschluss, '
              'reicht oft ein neuer O-Ring.',
         color='#1F2224'),
    # Hahnanschluss für 3/4-Zoll-Wasserhahn, zweites Teil im Loch
    teil('hahnstueck', 'hose_connector', 'Hahnanschluss 3/4 Zoll', 'Hahnanschluss', 'cyl',
         x=230, y=120, w=36, z=0, h=30, sortBias=60, mass=22, materials=[['pp', 85], ['gummi', 15]],
         info='Wird auf den Wasserhahn geschraubt, innen sitzt eine Flachdichtung aus Gummi. Am Hahn lassen, '
              'wenn nur der Schlauch entsorgt wird.',
         color='#5B6066', marks=[mark('cyl', 4, 4, 28, fill='#F2A23A'), mark('cyl', 11, 11, 14, fill='#2B2E31')]),
    teil('mantel', 'pvc_hose', 'Außenmantel', 'Außenmantel', 'cyl',
         x=0, y=0, w=D, z=0, h=60, mass=950, form='torus',
         info='Grünes Weich-PVC mit Weichmachern und UV-Schutz. Für den Wertstoffhof in Stücke schneiden; '
              'alte Stücke taugen als Kantenschutz oder Griffpolster.',
         color=GRUEN, marks=windungen(D, fill='#24522C')),
    teil('gewebe', 'pvc_hose', 'Polyestergewebe', 'Gewebe', 'cyl',
         material_id='polyester', x=2, y=2, w=D - 4, z=2, h=56, mass=110, form='torus', materials=[['polyester', 100]],
         info='Kreuzgewebe aus Polyesterfäden zwischen den PVC-Schichten. Es verhindert, dass der Schlauch unter '
              'Wasserdruck platzt oder abknickt. Lässt sich nicht vom PVC trennen.',
         color='#E9E3C8', marks=windungen(D - 4, fill='#A9A388', tiefe=56)),
    teil('seele', 'pvc_hose', 'Innenschlauch', 'Innenschlauch', 'cyl',
         x=4, y=4, w=D - 8, z=4, h=52, mass=880, form='torus',
         info='Glatte Innenschicht aus PVC, durch die das Wasser fließt. Kein Trinkwasser aus Gartenschläuchen '
              'trinken: Weichmacher können sich lösen.',
         color='#2F3A33', marks=windungen(D - 8, fill='#1C231F', tiefe=52)),
]
rolle = [p for p in teile if p['id'] in ('mantel', 'gewebe', 'seele')]
explodiere(rolle, abstand=45, nach_liste=True)
dz = rolle[0]['explode'][2] + 60 + 40  # Anschlussteile über der obersten Schicht, in Reihe auseinandergezogen
for i, dx in (('ueberwurf', -40), ('kupplung', 0), ('oring', 30), ('hahnstueck', 70)):
    next(p for p in teile if p['id'] == i)['explode'] = [dx, 0, dz]
skaliere_masse(teile, oid='garden_hose')
schreibe('garden_hose', teile)
