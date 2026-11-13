"""3D-Modell: usb_cable. Erzeugt tools/kategorien/modelle/usb_cable.json.

Typisches 1-m-Ladekabel USB-A auf USB-C, flach aufgerollt (drei Windungen übereinander). Die Kabelschichten
werden als ganze Rolle nach oben abgehoben, die Stecker seitlich (dx positiv) herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, schreibe  # noqa: E402

D = 100          # Durchmesser der Rolle
H = 10.5         # drei Windungen à 3,5 mm


def windungen(dm, loch, n=3, breite=3.5):
    """Konzentrische Ringe als Umrisse und dunkle Mitte: so sieht die Rolle von oben aus (Löcher kann der
    Renderer nicht, die Mitte wird als Schatten gezeichnet)."""
    out = []
    for i in range(n + 1):
        w = dm - 2 * i * breite
        out.append(mark('cyl', (dm - w) / 2, (dm - w) / 2, w))
    w = dm - 2 * n * breite - 2
    out.append(mark('cyl', (dm - w) / 2, (dm - w) / 2, w, fill=loch))
    return out


teile = [
    teil('mantel', 'cable_insulation', 'Kabelmantel', 'Mantel', 'cyl',
         x=0, y=6, w=D, z=0, h=H, mass=11,
         info='Außenhülle aus PVC mit Weichmachern. Mit einer Abisolierzange längs aufschlitzen, '
              'dann lassen sich die Drähte herausziehen.',
         color='#3A3D40', marks=windungen(D, '#26292B')),
    teil('schirm', 'cable_copper_core', 'Abschirmung (Folie und Geflecht)', 'Abschirmung', 'cyl',
         x=1.5, y=7.5, w=D - 3, z=0.5, h=H - 1, mass=3,
         materials=[['alu', 40], ['kupfer', 50], ['folien', 10]],
         info='Alufolie und ein feines Drahtgeflecht unter dem Mantel. Halten Störungen von den Datenleitungen fern.',
         color='#C2C6C9', marks=windungen(D - 3, '#8E9498')),
    teil('adern', 'cable_copper_core', 'Vier Kupferadern', 'Adern', 'cyl',
         x=3, y=9, w=D - 6, z=1, h=H - 2, mass=7,
         materials=[['kupfer', 70], ['hdpe', 30]],
         info='Rot und Schwarz leiten den Ladestrom, Grün und Weiß die Daten. Jede Ader ist einzeln isoliert, '
              'innen sind feine Kupferlitzen.',
         color='#C5803D', marks=windungen(D - 6, '#8F5A2A') + [mark('cyl', 3, 44, 5, fill='#C8423A'),
                                                    mark('cyl', 8.5, 44, 5, fill='#2B2B2B'),
                                                    mark('cyl', 14, 44, 5, fill='#3E9A57'),
                                                    mark('cyl', 19.5, 44, 5, fill='#F4F4F2')]),
    # USB-A-Stecker hinten rechts, Blechhülle zeigt nach hinten (y = 0)
    teil('huelle_a', 'plastic_housing', 'Steckergehäuse USB-A', 'Gehäuse A', 'box',
         x=103, y=12, w=16, d=28, z=0, h=8, r=3, explode=[28, 0, 0], mass=2.5,
         info='Angespritzter Kunststoff mit Knickschutz. Das Kabel direkt dahinter abschneiden, '
              'dann sind Stecker und Kabel getrennt.',
         color='#3A3D40', marks=[mark('box', 3, 24, 10, 3, 1)]),
    teil('zunge_a', 'connector_shell', 'Kontaktzunge USB-A', 'Kontakte A', 'box',
         material_id='copper', x=106, y=1, w=10, d=10, z=3, h=1.8, r=0.3, explode=[28, -16, 14], mass=0.4,
         materials=[['pcabs', 60], ['kontakte', 40]],
         info='Vier vergoldete Kontakte auf einem Kunststoffsteg. Die dünne Goldschicht schützt vor Rost.',
         color='#2C5FA8', marks=[mark('box', 1, 1, 1.4, 6, 0.3, '#E1B94F'), mark('box', 3.5, 1, 1.4, 7, 0.3, '#E1B94F'),
                                mark('box', 5.5, 1, 1.4, 7, 0.3, '#E1B94F'), mark('box', 8, 1, 1.4, 6, 0.3, '#E1B94F')]),
    teil('blech_a', 'connector_shell', 'Steckerhülse USB-A', 'Hülse A', 'box',
         x=105, y=0, w=12, d=12, z=1.75, h=4.5, r=0.3, explode=[28, -18, 0], mass=1.5,
         info='Vernickeltes Stahlblech. Lässt sich mit einem Magneten vom Kunststoff trennen.',
         color='#B7BCC0', marks=[mark('box', 2, 3, 2.5, 2, 0.3, '#5E656A'), mark('box', 7.5, 3, 2.5, 2, 0.3, '#5E656A')]),
    teil('knick_a', 'plastic_housing', 'Knickschutz USB-A', 'Knickschutz', 'box', material_id='rubber',
         x=107, y=40, w=8, d=8, z=1, h=6, r=3, explode=[28, 8, 0], mass=0.6, materials=[['tpe', 100]],
         color='#2E3134', info='Weiche Gummitülle am Steckerende. Sie verhindert, dass die Adern beim Biegen brechen.',
         marks=raster(1, 1.5, 1, 3, 6, 0.6, 0, 2, fill='#232628')),
    teil('klett', 'cable_insulation', 'Klettband', 'Klettband', 'box', material_id='nylon',
         x=44, y=4, w=12, d=14, z=0, h=11.2, r=2, explode=[0, -40, 0], mass=0.5, materials=[['nylon', 100]],
         color='#4B5560', info='Kleines Klettband, das die Rolle zusammenhält. Vor dem Recyceln abnehmen und weiterverwenden.',
         marks=raster(1, 1.5, 1, 6, 10, 0.5, 0, 2, fill='#3E4750')),
    # USB-C-Stecker vorne rechts, Hülse zeigt nach vorne
    teil('huelle_c', 'plastic_housing', 'Steckergehäuse USB-C', 'Gehäuse C', 'box',
         x=104, y=72, w=14, d=26, z=0.75, h=6.5, r=3, explode=[28, 0, 0], mass=1.8,
         info='Kleiner und flacher als USB-A. Wie beim anderen Stecker angespritzt und nicht zerlegbar.',
         color='#3A3D40', marks=[mark('box', 3, 1, 8, 3, 1)]),
    teil('knick_c', 'plastic_housing', 'Knickschutz USB-C', 'Knickschutz C', 'box', material_id='rubber',
         x=107.5, y=64, w=7, d=8, z=1.5, h=5.5, r=2.5, explode=[28, -8, 0], mass=0.5, materials=[['tpe', 100]],
         color='#2E3134', label=False, info='Gummitülle am USB-C-Ende, gleiche Aufgabe wie am anderen Stecker.',
         marks=raster(1, 1.5, 1, 3, 5, 0.6, 0, 2, fill='#232628')),
    teil('zunge_c', 'connector_shell', 'Kontaktzunge USB-C', 'Kontakte C', 'box', material_id='copper',
         x=108, y=99, w=6, d=5, z=3.5, h=0.7, r=0.3, explode=[28, 22, 8], mass=0.2, materials=[['pcabs', 60], ['kontakte', 40]],
         color='#2B2F33', info='Kunststoffzunge mit 24 winzigen vergoldeten Kontakten, je 12 oben und unten. '
                               'Deshalb passt der Stecker in beide Richtungen.',
         marks=raster(0.4, 2.5, 6, 1, 0.5, 2, 0.95, fill='#E1B94F')),
    teil('platine_c', 'connector_shell', 'Mini-Platine USB-C', 'Platine C', 'box',
         material_id='pcb', x=107, y=96, w=8, d=6, z=3, h=0.8, r=0.3, explode=[28, 14, 14], mass=0.3,
         info='Winzige Leiterplatte mit einem Widerstand. Er sagt dem Handy, wie viel Strom das Kabel verträgt.',
         color='#2E6B45', marks=[mark('box', 2, 1.5, 2, 1.2, 0.2, '#22272B')]),
    teil('blech_c', 'connector_shell', 'Steckerhülse USB-C', 'Hülse C', 'box',
         x=106.8, y=98, w=8.4, d=7, z=2.7, h=2.6, r=1.3, explode=[28, 16, 0], mass=1,
         info='Ovale Stahlhülse, beidseitig steckbar. Innen sitzen 24 Kontakte auf einer Zunge.',
         color='#B7BCC0', marks=[mark('box', 1.2, 0.8, 6, 1, 0.5, '#2A2E31')]),
]
explodiere(teile, abstand=40)
schreibe('usb_cable', teile)
