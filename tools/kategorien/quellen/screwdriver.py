"""3D-Modell: screwdriver. Erzeugt tools/kategorien/modelle/screwdriver.json.

Schlitz-Schraubendreher 6,5 mm, flach auf dem Tisch: Griff hinten (y 0), Klinge vorn (y groß). Griff aus PP mit
TPE-Weichzone, Rundschaft aus Chrom-Vanadium-Stahl, im Griff mit angestauchten Flügeln gegen Verdrehen gesichert.
Explodiert: Griffteile bleiben liegen, Schaft mit Flügeln und Klinge schwebt als Einheit darüber.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

ROT = '#C8322B'
GELB = '#F1C232'
STAHL = '#B5BCC1'

teile = [
    teil('klinge', 'steel_shaft', 'Schlitzklinge', 'Klinge', 'box',
         x=11.75, y=203, w=6.5, d=17, z=14, h=2, r=0.3, mass=3,
         info='Flach geschmiedete, gehärtete Spitze, schwarz brüniert. Sie greift in den Schlitz der Schraube.',
         color='#33383C'),
    teil('schaft', 'steel_shaft', 'Rundschaft', 'Schaft', 'box',
         x=12, y=60, w=6, d=143, z=12, h=6, r=3, mass=36, form='liegend_y',
         info='Chrom-Vanadium-Stahl, verchromt. Ist fest in den Griff gespritzt: Zum Trennen den Griff '
              'mit einer Säge aufschneiden. Der Stahl gehört zum Altmetall.',
         color=STAHL, marks=[mark('box', 1.5, 50, 3, 80, 1.5, '#DCE1E4', zeichnung=True)]),
    teil('fluegel', 'steel_shaft', 'Verdrehsicherung (Flügel)', 'Flügel', 'box',
         x=9, y=46, w=12, d=14, z=14, h=2, r=1, mass=3,
         info='Angestauchte Flügel am Schaftende. Sie verhindern, dass sich der Schaft im Griff dreht.',
         color=STAHL),
    teil('tpe_oben', 'plastic_handle', 'Weichgriff-Zone oben', 'Weichgriff', 'box',
         material_id='rubber', x=9.5, y=20, w=11, d=66, z=28, h=2, r=5, mass=4, materials=[['tpe', 100]],
         info='Weiche TPE-Streifen, im Zwei-Komponenten-Spritzguss auf den harten Kern gespritzt, damit die Hand nicht '
              'abrutscht. Lassen sich nicht sortenrein trennen: Griff in den Restmüll.',
         color=GELB, marks=raster(2.5, 4, 1, 8, 6, 4, 0, 8, r=2, fill='#C99A1E')),
    teil('tpe_rechts', 'plastic_handle', 'Weichgriff-Zone rechts', 'Weichgriff', 'box',
         material_id='rubber', x=28, y=20, w=2, d=66, z=9, h=12, r=1, explode=[16, 0, 0], mass=3,
         materials=[['tpe', 100]], label=False, info='Seitlicher TPE-Streifen.', color=GELB, sortBias=6),
    teil('tpe_links', 'plastic_handle', 'Weichgriff-Zone links', 'Weichgriff', 'box',
         material_id='rubber', x=0, y=20, w=2, d=66, z=9, h=12, r=1, explode=[-16, 0, 0], mass=3,
         materials=[['tpe', 100]], label=False, info='Seitlicher TPE-Streifen.', color=GELB),
    teil('griff_oben', 'plastic_handle', 'Griffkörper oben', 'Griff', 'box',
         x=6, y=8, w=18, d=84, z=24, h=5, r=8, mass=5, label=False,
         info='Obere Rundung des Griffkörpers.', color=ROT),
    teil('griff_mitte', 'plastic_handle', 'Griffkörper (PP)', 'Griff', 'box',
         x=1, y=8, w=28, d=84, z=6, h=18, r=12, mass=14,
         info='Harter Kern aus Polypropylen, in einem Stück um den Schaft gespritzt. Zum Trennen mit einer Säge '
              'aufschneiden.', color=ROT),
    teil('griff_unten', 'plastic_handle', 'Griffkörper unten', 'Griff', 'box',
         x=6, y=8, w=18, d=84, z=1, h=5, r=8, mass=5, label=False,
         info='Untere Rundung des Griffkörpers.', color=ROT),
    teil('griff_kappe', 'plastic_handle', 'Griffende', 'Griffende', 'box',
         x=4, y=0, w=22, d=8, z=4, h=22, r=8, mass=3, form='liegend_y',
         info='Abgerundetes Griffende mit Aufhängeloch, Teil des Griffkörpers.',
         color=ROT, marks=[mark('box', 3, 2, 16, 6, 3, '#D8443C', zeichnung=True)]),
    teil('griff_hals', 'plastic_handle', 'Griffhals', 'Griffhals', 'box',
         x=4, y=92, w=22, d=16, z=4, h=22, r=9, mass=4, form='liegend_y',
         info='Verjüngter Übergang zum Schaft, hier tritt der Stahl aus dem Griff.',
         color=ROT, marks=[mark('box', 3, 3, 16, 10, 5, '#D8443C', zeichnung=True)]),
]

GRIFF = ['griff_oben', 'griff_mitte', 'griff_unten', 'griff_kappe', 'griff_hals']
for p in teile:
    if p['id'] in ('klinge', 'schaft', 'fluegel'):
        p['explode'] = [0, 66, 0]  # Schaft in Achsrichtung aus dem Griff ziehen
explodiere(teile, abstand=40, fest=GRIFF)
for p in teile:  # Foto-Ansicht: flache marks schweben über runden Formen, dort nur in der Zeichnung
    if p.get('form'):
        p['marks'] = [dict(m, zeichnung=True) for m in p.get('marks') or []]
skaliere_masse(teile, oid='screwdriver')
schreibe('screwdriver', teile)
