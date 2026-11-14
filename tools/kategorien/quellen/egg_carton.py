"""3D-Modell: egg_carton. Erzeugt tools/kategorien/modelle/egg_carton.json.

Typischer Eierkarton für 6 Eier (3 × 2) aus Faserguss: Unterschale aus Rand und sechs nach unten gewölbten
Eiermulden, zwei Stützkegel zwischen den Mulden, hinten angeformter Deckel (unten breit, oben schmaler, mit
Rippen), vorne die Verschlusslasche, Preisetikett auf dem Deckel. Deckel hebt nach oben ab, Lasche klappt nach
vorne weg, die Mulden bleiben mit dem Rand zusammen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

FASER = '#B9AE9C'
DUNKEL = '#9C907C'
MULDE = '#857A68'
MITTE_X = (30, 80, 130)
MITTE_Y = (28, 77)
teile = [
    teil('etikett', 'molded_pulp_tray', 'Preisetikett', 'Etikett', 'box',
         material_id='paper', x=40, y=30, w=80, d=45, z=70, h=0.2, r=1, mass=0.4,
         materials=[['papier', 85], ['druck', 8], ['klebstoff', 7]],
         info='Papieraufkleber mit Haltbarkeitsdatum, Gewichtsklasse und Erzeugercode. Darf am Karton bleiben.',
         color='#F4F2EE', marks=[mark('box', 5, 5, 50, 6, 0, '#3A3F44'), mark('box', 5, 15, 35, 5, 0, '#3A3F44'),
                                 mark('box', 5, 30, 70, 9, 0, '#5C9E5A'), mark('cyl', 60, 4, 15, fill='#E3B23C')]),
    teil('deckel_oben', 'molded_pulp_tray', 'Deckel, Oberseite mit Rippen', 'Deckel', 'box',
         x=8, y=8, w=144, d=89, z=56, h=14, r=12, mass=5,
         info='Hinten mit der Unterschale verbunden. Die Rippen und Schrägen machen den dünnen Faserguss stabil.',
         color=FASER, marks=[mark('box', 4, 4, 136, 81, 10, DUNKEL, zeichnung=True), mark('box', 7, 7, 130, 75, 8, FASER, zeichnung=True)]
                            + raster(10, 2, 3, 1, 26, 3, 46, fill=DUNKEL) + raster(10, 84, 3, 1, 26, 3, 46, fill=DUNKEL)),
    teil('deckel', 'molded_pulp_tray', 'Deckel, Seitenwände', 'Deckelwand', 'box',
         x=0, y=0, w=160, d=103, z=34, h=22, r=12, mass=6, label=False,
         info='Die schrägen Wände des Deckels; zusammen mit der Oberseite ein Pressteil.',
         color=FASER, marks=[mark('box', 6, 6, 148, 91, 10, DUNKEL)]),
    teil('kegel_links', 'molded_pulp_tray', 'Stützkegel links', 'Stützkegel', 'cyl',
         x=48, y=45, w=15, z=34, h=22, mass=0.8,
         info='Stützt den Deckel, damit die Eier beim Stapeln nicht zerdrückt werden.',
         color=FASER, marks=[mark('cyl', 4, 4, 7, fill=DUNKEL)]),
    teil('kegel_rechts', 'molded_pulp_tray', 'Stützkegel rechts', 'Stützkegel', 'cyl',
         x=97, y=45, w=15, z=34, h=22, mass=0.8, label=False,
         info='Gegenstück zum linken Kegel.',
         color=FASER, marks=[mark('cyl', 4, 4, 7, fill=DUNKEL)]),
    teil('schale', 'molded_pulp_tray', 'Unterschale (Rand)', 'Unterschale', 'box',
         x=2, y=2, w=156, d=101, z=28, h=6, r=8, mass=5,
         info='Aus Altpapier gepresst und getrocknet. Sauber ins Altpapier, zerrissen auch in den Kompost.',
         color=FASER, marks=[mark('box', 2, 2, 152, 97, 6, DUNKEL, zeichnung=True)]
                            + [mark('cyl', cx - 2 - 21, cy - 2 - 20, 42, 40, fill=MULDE) for cy in MITTE_Y for cx in MITTE_X]),
]
# Jede Mulde als Stapel von Scheiben, unten schmal, oben breit: in der Foto-Ansicht eine runde Schale
PROFIL = ((26, 4), (36, 5), (42, 6), (46, 11))   # (Breite, Höhe) von unten nach oben, zusammen z = 2 … 28
MULDEN = []
n = 0
for cy in MITTE_Y:
    for cx in MITTE_X:
        n += 1
        z = 2
        for k, (w, h) in enumerate(PROFIL):
            d = w * 44 / 46
            MULDEN.append(teil(f'mulde_{n}' if k == len(PROFIL) - 1 else f'mulde_{n}_{k}', 'molded_pulp_tray',
                               'Eiermulde', 'Eiermulde', 'cyl', x=cx - w / 2, y=cy - d / 2, w=w, d=d, z=z, h=h,
                               mass=1.5 * w * d * h / (46 * 44 * 26),
                               label=None if (n == 1 and k == len(PROFIL) - 1) else False,
                               info='Eine von sechs Mulden. Sie federt Stöße ab, weil die Fasern leicht nachgeben.'
                               if n == 1 else 'Weitere Mulde.', color=FASER))
            z += h
teile += MULDEN
teile.append(teil('lasche', 'molded_pulp_tray', 'Verschlusslasche', 'Lasche', 'box',
                  x=62, y=103, w=36, d=2, z=30, h=18, r=1, explode=[0, 70, 0], mass=0.8, sortBias=25,
                  info='Hängt vorne am Deckel. Ihre Nasen rasten in Schlitze der Unterschale ein und halten den Karton zu.',
                  color=FASER, marks=[mark('box', 8, 0, 20, 2, 1, DUNKEL)]))
explodiere(teile, abstand=40, fest=[p['id'] for p in MULDEN] + ['schale'],
           gruppen=[['deckel_oben', 'deckel']])
skaliere_masse(teile, oid='egg_carton')
schreibe('egg_carton', teile)
