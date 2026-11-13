"""3D-Modell: wired_earphones. Erzeugt tools/kategorien/modelle/wired_earphones.json.

Typische In-Ear-Kopfhörer mit 3,5-mm-Klinkenstecker, 1,2 m Kabel. Das Kabel liegt flach aufgerollt (links),
rechts daneben die beiden Ohrhörer (Ohrstöpsel nach oben), Y-Verteiler und Klinkenstecker.
Explosion: Kupferadern über dem Mantel, linker Ohrhörer zerlegt nach oben gestapelt, Steckerstift nach vorne.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

D = 60  # Durchmesser der Kabelrolle
SCHWARZ = '#2B2E31'


def windungen(dm, n=4, breite=2.2):
    return [mark('cyl', round(i * breite, 2), round(i * breite, 2), round(dm - 2 * i * breite, 2)) for i in range(n)]


teile = [
    # Linker Ohrhörer, zerlegt (Ohrstöpsel oben)
    teil('ohrstoepsel', 'silicone_ear_tips', 'Silikon-Ohrstöpsel', 'Ohrstöpsel', 'cyl',
         x=65.5, y=4.5, w=11, z=11, h=4, mass=0.3, color='#3A3D40',
         info='Weiche Silikonkappe, lässt sich von Hand abziehen und waschen. Gehört in den Restmüll.',
         marks=[mark('cyl', 3.5, 3.5, 4, fill='#1E2022')]),
    teil('vorderschale', 'plastic_housing', 'Vorderschale mit Schallrohr', 'Vorderschale', 'cyl',
         x=63.5, y=2.5, w=15, z=8, h=3, mass=0.4, color=SCHWARZ,
         info='Kunststoffschale mit kurzem Röhrchen, auf dem der Ohrstöpsel steckt. Mit der Rückschale verklebt.',
         marks=[mark('cyl', 4, 4, 7, fill='#3A3D40'), mark('cyl', 5.5, 5.5, 4, fill='#1E2022')]),
    teil('treiber', 'speaker_driver', 'Lautsprecher (10 mm)', 'Lautsprecher', 'cyl',
         x=64.5, y=3.5, w=13, z=5, h=3, mass=0.8,
         materials=[['ndfeb', 30], ['kupfer', 15], ['stahl', 30], ['folien', 10], ['pcabs', 15]],
         info='Winziger Lautsprecher mit Neodym-Magnet und Schwingspule aus Kupferdraht. '
              'Der Magnet ist stark, nicht an Bankkarten halten.',
         color='#C9CDD1', marks=[mark('cyl', 2, 2, 9, fill='#C98F62'), mark('cyl', 4, 4, 5, fill='#5A6066')]),
    teil('rueckschale', 'plastic_housing', 'Rückschale mit Knickschutz', 'Rückschale', 'cyl',
         x=63, y=2, w=16, z=0, h=5, mass=0.6, color=SCHWARZ,
         info='Hier kommt das Kabel an, die Adern sind am Lautsprecher angelötet. Zum Trennen das Kabel abschneiden.',
         marks=[mark('cyl', 2, 2, 12, fill='#3A3D40')]),
    # Rechter Ohrhörer im Ganzen
    teil('ohrhoerer_r', 'speaker_driver', 'Ohrhörer rechts (komplett)', 'Ohrhörer rechts', 'cyl',
         x=63, y=21, w=16, z=0, h=15, mass=2.1,
         materials=[['pcabs', 45], ['ndfeb', 12], ['stahl', 13], ['kupfer', 10], ['gummi', 15], ['folien', 5]],
         info='Genauso aufgebaut wie der linke: Ohrstöpsel, zwei verklebte Schalen und ein kleiner Lautsprecher.',
         color=SCHWARZ, marks=[mark('cyl', 2.5, 2.5, 11, fill='#3A3D40'), mark('cyl', 6, 6, 4, fill='#1E2022')]),
    teil('y_verteiler', 'plastic_housing', 'Y-Verteiler', 'Y-Verteiler', 'box',
         x=65, y=39, w=12, d=6, z=0, h=5, r=2.5, mass=0.5, color=SCHWARZ,
         info='Hier teilt sich das Kabel in einen linken und rechten Strang. Kunststoff, um das Kabel gespritzt.',
         marks=[mark('box', 2, 2, 8, 2, 1, '#3A3D40')]),
    # Klinkenstecker: Gehäuse und Metallstift, liegt längs (Stift zeigt nach vorne)
    teil('stecker_gehaeuse', 'audio_jack', 'Steckergehäuse', 'Steckergehäuse', 'box',
         material_id='pvc', x=65, y=46, w=8, d=20, z=0, h=8, r=3.5, mass=1.0, materials=[['pvc', 85], ['lot', 15]],
         info='Angespritzter Kunststoff mit Knickschutz. Innen sind die drei Adern an den Stift gelötet. '
              'Direkt dahinter abschneiden.',
         color=SCHWARZ, marks=[mark('box', 1.5, 2, 5, 12, 2, '#3A3D40')]),
    teil('klinkenstift', 'audio_jack', '3,5-mm-Klinkenstift', 'Klinkenstift', 'box',
         x=67.25, y=66, w=3.5, d=14, z=2.25, h=3.5, r=1.7, explode=[0, 14, 0], mass=0.8,
         materials=[['messing', 85], ['nickel', 10], ['ptfe', 5]],
         info='Vernickeltes Messing mit drei Kontakten (links, rechts, Masse), getrennt durch schwarze Isolierringe.',
         color='#C9CDD0', marks=[mark('box', 0.5, 3, 2.5, 0.8, 0.3, '#22272B'), mark('box', 0.5, 7, 2.5, 0.8, 0.3, '#22272B')]),
    # Kabel als flache Rolle
    teil('adern', 'cable_copper_core', 'Kupferlitzen (Lackdraht)', 'Adern', 'cyl',
         x=1, y=1, w=D - 2, z=0.5, h=3, mass=2.5, materials=[['kupfer', 80], ['polyester', 20]],
         info='Hauchdünne Kupferlitzen, mit farbigem Lack isoliert (rot, grün, kupferfarben). Lack und Kupfer '
              'trennt erst die Recyclinganlage.',
         color='#C5803D', marks=windungen(D - 2) + [mark('cyl', 2, 27, 2, fill='#C8423A'),
                                                    mark('cyl', 4.5, 27, 2, fill='#3E9A57')]),
    teil('mantel', 'cable_insulation', 'Kabelmantel', 'Mantel', 'cyl',
         x=0, y=0, w=D, z=0, h=4, mass=4.5, materials=[['tpe', 100]],
         info='Dünner, weicher Mantel aus thermoplastischem Elastomer (früher PVC). Ein Kabel von 1,2 m wiegt nur wenige Gramm.',
         color=SCHWARZ, marks=windungen(D)),
]
explodiere(teile, abstand=8, abstaende={'adern': 28})
skaliere_masse(teile, oid='wired_earphones', stellen=2)
schreibe('wired_earphones', teile)
