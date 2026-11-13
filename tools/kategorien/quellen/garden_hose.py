"""3D-Modell: garden_hose. Erzeugt tools/kategorien/modelle/garden_hose.json.

Typischer 1/2-Zoll-Gartenschlauch (20 m, Außen-Ø 19 mm), flach aufgerollt zu einer Rolle von Ø 400 mm mit
drei Windungen übereinander (60 mm). Wie bei usb_cable werden die drei Schichten (Außenmantel, Gewebe,
Innenschlauch) als Rolle nach oben abgehoben. Die Anschlussteile liegen zusammengebaut im Loch der Rolle und
werden seitlich (dx positiv) herausgezogen: Schlauchstück mit Überwurfmutter und O-Ring, Hahnanschluss.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

D = 400
LOCH = 250
GRUEN = '#3E8E4A'


def windungen(dm, n=7, breite=10.5, fill=None):
    """Konzentrische Ringe als Umrisse der Windungen, außen beginnend."""
    out = []
    for i in range(n + 1):
        w = dm - 2 * i * breite
        out.append(mark('cyl', (dm - w) / 2, (dm - w) / 2, w, fill=fill if i == n else None))
    return out


teile = [
    teil('mantel', 'pvc_hose', 'Außenmantel', 'Außenmantel', 'cyl',
         x=0, y=0, w=D, z=0, h=60, mass=950,
         info='Grünes Weich-PVC mit Weichmachern und UV-Schutz. Für den Wertstoffhof in Stücke schneiden; '
              'alte Stücke taugen als Kantenschutz oder Griffpolster.',
         color=GRUEN, marks=windungen(D, fill='#5E6B60')),
    teil('gewebe', 'pvc_hose', 'Polyestergewebe', 'Gewebe', 'cyl',
         material_id='polyester', x=2, y=2, w=D - 4, z=1, h=58, mass=110, materials=[['polyester', 100]],
         info='Kreuzgewebe aus Polyesterfäden zwischen den PVC-Schichten. Es verhindert, dass der Schlauch unter '
              'Wasserdruck platzt oder abknickt. Lässt sich nicht vom PVC trennen.',
         color='#E9E3C8', marks=windungen(D - 4, fill='#5E6B60')),
    teil('seele', 'pvc_hose', 'Innenschlauch', 'Innenschlauch', 'cyl',
         x=4, y=4, w=D - 8, z=2, h=56, mass=880,
         info='Glatte Innenschicht aus PVC, durch die das Wasser fließt. Kein Trinkwasser aus Gartenschläuchen '
              'trinken: Weichmacher können sich lösen.',
         color='#2F3A33', marks=windungen(D - 8, fill='#5E6B60')),
    # Schlauchstück (Schnellkupplung) liegt waagerecht im Loch der Rolle, Schlauchseite links
    teil('ueberwurf', 'hose_connector', 'Überwurfmutter', 'Überwurf', 'box',
         x=108, y=133, w=30, d=32, z=14, h=32, r=6, explode=[312, 0, 0], mass=12,
         info='Wird über die Spreizkrallen geschraubt und presst sie auf den Schlauch. Aufdrehen und abziehen, '
              'dann ist der Anschluss vom Schlauch getrennt.',
         color='#F2A23A', marks=[mark('box', 4, 2, 2, 28, 1, '#D5892A'), mark('box', 10, 2, 2, 28, 1, '#D5892A'),
                                 mark('box', 16, 2, 2, 28, 1, '#D5892A'), mark('box', 22, 2, 2, 28, 1, '#D5892A')]),
    teil('kupplung', 'hose_connector', 'Schlauchstück mit Spreizkrallen', 'Schlauchstück', 'box',
         x=138, y=136, w=50, d=26, z=17, h=26, r=5, explode=[330, 0, 0], mass=18,
         info='PP-Kupplung, die auf Wasserhahn, Brause oder Spritze klickt. Die Krallen greifen in den Schlauch. '
              'Ganz aus Kunststoff, aber keine Verpackung: zum Wertstoffhof.',
         color='#5B6066', marks=[mark('box', 2, 4, 14, 18, 2, '#F2A23A'), mark('box', 30, 3, 18, 20, 4, '#464B50')]),
    teil('oring', 'hose_connector', 'O-Ring-Dichtung', 'O-Ring', 'box',
         material_id='rubber', x=188, y=141, w=3, d=16, z=22, h=16, r=1, explode=[345, 0, 0], mass=0.5,
         materials=[['gummi', 100]],
         info='Gummiring vorn in der Kupplung, er dichtet zum Gegenstück ab. Tropft der Anschluss, '
              'reicht oft ein neuer O-Ring.',
         color='#1F2224'),
    # Hahnanschluss für 3/4-Zoll-Wasserhahn, zweites Teil im Loch
    teil('hahnstueck', 'hose_connector', 'Hahnanschluss 3/4 Zoll', 'Hahnanschluss', 'cyl',
         x=150, y=225, w=36, z=10, h=30, explode=[300, 20, 0], mass=22, materials=[['pp', 85], ['gummi', 15]],
         info='Wird auf den Wasserhahn geschraubt, innen sitzt eine Flachdichtung aus Gummi. Am Hahn lassen, '
              'wenn nur der Schlauch entsorgt wird.',
         color='#5B6066', marks=[mark('cyl', 4, 4, 28, fill='#F2A23A'), mark('cyl', 11, 11, 14, fill='#2B2E31')]),
]
explodiere(teile, abstand=45, nach_liste=True)
skaliere_masse(teile, oid='garden_hose')
schreibe('garden_hose', teile)
