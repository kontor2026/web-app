"""3D-Modell: soldering_iron. Erzeugt tools/kategorien/modelle/soldering_iron.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Einfacher Stift-Lötkolben (30 W), liegt flach entlang y: hinten (y 0) das Kabel mit Knickschutz, dann der Griff,
# vorne (y groß) Heizhülse, Überwurfhülse und die Lötspitze. Alle runden Teile als abgerundete Boxen (Radius = halbe Breite).
# Explosion entlang der Achse: Spitze, Überwurfhülse und Heizhülse nach vorn (dy > 0), Heizelement aus der Hülse
# nach oben, Kabel und Knickschutz nach hinten, Kupferadern daneben (dx > 0).
SCHWARZ = '#2B2F33'
BLAU, BLAU_D = '#3F6E9C', '#2F577C'
GRIFF_INFO = 'Hitzebeständiger Kunststoffgriff mit gummierter Griffzone. Innen sind die Kabeladern angeschraubt.'


def griff_scheiben():
    """Runder Griff als fünf liegende Scheiben (der Renderer kennt nur senkrechte Körper)."""
    lagen = [(0, 3, 15), (3, 5, 22), (8, 9, 25), (17, 5, 22), (22, 3, 15)]
    out = []
    for i, (z, h, w) in enumerate(lagen):
        oben = i == len(lagen) - 1
        out.append(teil(f'griff_{i + 1}', 'plastic_handle', 'Griff', 'Griff', 'box', material_id='pp',
                        x=12.5 - w / 2, y=45, w=w, d=83, z=z, h=h, r=w / 2, explode=[0, 0, 0], mass=5,
                        materials=[['pp', 85], ['tpe', 15]], color=BLAU, label=oben,
                        info=GRIFF_INFO if oben else 'Teil des Griffs.',
                        marks=([mark('box', 1, 20, w - 2, 44, w / 2 - 1, '#2B2F33')]
                               + raster(2, 24, 1, 9, w - 4, 1.5, 0, 4.5, r=0.7, fill='#3A3F44')
                               + raster(1, 71, 1, 3, w - 2, 1.5, 0, 3.5, r=0.7, fill=BLAU_D)) if oben else None))
    return out


def fingerschutz():
    """Wulst vorne am Griff, etwas dicker als der Griff, damit die Finger nicht nach vorne rutschen."""
    lagen = [(0, 4, 18), (4, 17, 28), (21, 4, 18)]
    return [teil(f'wulst_{i + 1}', 'plastic_handle', 'Fingerschutz', 'Fingerschutz', 'box', material_id='pp',
                 x=12.5 - w / 2, y=128, w=w, d=7, z=z, h=h, r=3, explode=[0, 0, 0], mass=1,
                 materials=[['pp', 100]], color=BLAU_D, label=i == 2,
                 info='Dicker Ring vorne am Griff. Er schützt die Finger vor der heißen Heizhülse.' if i == 2 else 'Teil des Fingerschutzes.')
            for i, (z, h, w) in enumerate(lagen)]



teile = [
    teil('spitze', 'soldering_tip', 'Lötspitze', 'Spitze', 'box',
         x=10, y=155, w=5, d=65, z=10, h=5, r=2.5, explode=[0, 105, 0], mass=6,
         materials=[['kupfer', 85], ['stahl', 10], ['nickel', 5]], color='#A8AEB2',
         info='Kupferkern mit Eisen- und Nickelschicht, damit das Lot nicht das Kupfer auflöst. Abkühlen lassen, dann nach vorn herausziehen.',
         marks=[mark('box', 0.5, 52, 4, 12, 2, '#C8CDD0')]),
    teil('ueberwurf', 'soldering_tip', 'Überwurfhülse mit Mutter', 'Überwurfhülse', 'box', material_id='steel',
         x=7.5, y=165, w=10, d=25, z=7.5, h=10, r=5, explode=[0, 65, 0], mass=6, materials=[['stahl', 100]], color='#9AA2A8',
         info='Edelstahlhülse, die die Spitze festhält. Die Rändelmutter am Griff aufschrauben, erst wenn alles kalt ist.',
         marks=[mark('box', 1, 20, 8, 5, 2, '#7D858B')]),
    teil('heizelement', 'heating_element', 'Heizelement', 'Heizelement', 'box',
         x=9.5, y=135, w=6, d=45, z=9.5, h=6, r=3, explode=[0, 35, 22], mass=8,
         materials=[['nichrom', 30], ['keramik', 50], ['glimmer', 20]], color='#C4672D',
         info='Nickel-Chrom-Draht auf einem Keramikrohr, mit Glimmer isoliert. Wird über 350 Grad heiß.',
         marks=raster(0.5, 2, 1, 10, 5, 2, 0, 4.2, r=1, fill='#8C7B6B')),
    teil('heizhuelse', 'heating_element', 'Heizhülse (Schaft)', 'Heizhülse', 'box', material_id='steel',
         x=8.5, y=130, w=8, d=55, z=8.5, h=8, r=4, explode=[0, 35, 0], mass=10, materials=[['stahl', 100]], color='#B5BBC0',
         info='Dünnes Edelstahlrohr um das Heizelement. Nicht anfassen, solange der Kolben eingesteckt ist.'),
    *griff_scheiben(),
    *fingerschutz(),
    teil('klemme', 'plastic_handle', 'Anschlussklemme mit Schrauben', 'Klemme', 'box', material_id='mixed_electronics',
         x=7, y=60, w=11, d=16, z=8, h=8, r=1, explode=[0, 0, 40], mass=3,
         materials=[['messing', 50], ['stahl', 20], ['keramik', 30]], color='#E8E2C8',
         marks=[mark('cyl', 1.5, 3, 4, fill='#B7BCC0'), mark('cyl', 5.5, 9, 4, fill='#B7BCC0')],
         info='Keramikklemme im Griff: Hier sind die Kabeladern mit kleinen Schrauben an den Drähten des Heizelements befestigt.'),
    teil('knickschutz', 'plastic_handle', 'Knickschutz', 'Knickschutz', 'box', material_id='pvc',
         x=7.5, y=22, w=10, d=28, z=7.5, h=10, r=5, explode=[0, -30, 0], mass=4, materials=[['pvc', 100]], color=SCHWARZ,
         info='Weiche Tülle, damit das Kabel am Griff nicht bricht. Wird mit dem Kabel abgezogen.'),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=9, y=0, w=7, d=25, z=9, h=7, r=3.5, explode=[0, -50, 0], mass=14, materials=[['pvc', 90], ['pp', 10]],
         color=SCHWARZ,
         info='Etwa 1,5 m Kabel, hier als Stück gezeigt. PVC-Mantel längs aufschlitzen; der Eurostecker ist eingespritzt.'),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=10.5, y=0, w=4, d=40, z=10.5, h=4, r=1, explode=[25, -50, 0], mass=7, color='#B87333',
         info='Zwei Kupferadern versorgen das Heizelement. Kupfer ist wertvoll.'),
]

skaliere_masse(teile, oid='soldering_iron')
schreibe('soldering_iron', teile)
