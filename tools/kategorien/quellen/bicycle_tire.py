"""3D-Modell: bicycle_tire. Erzeugt tools/kategorien/modelle/bicycle_tire.json."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# 26-Zoll-Fahrradreifen (26 × 2,0, ETRTO 50-559) flach liegend: Außendurchmesser 650 mm, Reifenbreite 50 mm = Höhe.
# Die Schichten liegen als konzentrische Ringe übereinander: Seitenwände oben und unten, dazwischen Lauffläche,
# Pannenschutzgürtel und Karkasse, an der Innenkante die beiden Wulstkerne (Ø 559 mm Felgensitz).
# In der Foto-Ansicht sind alle Schichten echte Ringe (form='torus'), ineinander geschachtelt; die Lochmarken gelten nur für die Zeichnung.
# Explodiert: alle Schichten werden nach oben abgehoben.
D = 650
GUMMI = '#2B2D2F'
LOCH = '#45484B'


BODEN = '#DCD8CE'  # Tisch, durch das Loch gesehen


def ring(aussen, innen, fill=LOCH, tiefe=None):
    """Loch eines Rings als marks: Innenwand (fill) und, um die Tiefe versetzt, der Tisch darunter."""
    o = (aussen - innen) / 2
    wand = [mark('cyl', o, o, innen, fill=fill, zeichnung=True)]
    if not tiefe:
        return wand
    k = innen - tiefe * 1.41
    v = o + (innen - k) / 2 + tiefe / 2
    return wand + [mark('cyl', round(v, 1), round(v, 1), round(k, 1), fill=BODEN, zeichnung=True)]


def stollen(aussen, radius, n, gr=10):
    """n Profilstollen auf einem Kreis mit radius um die Teilmitte."""
    c = aussen / 2
    return [mark('box', round(c + radius * math.cos(2 * math.pi * i / n) - gr / 2, 1),
                 round(c + radius * math.sin(2 * math.pi * i / n) - gr / 2, 1), gr, gr, 2, '#1E2022', zeichnung=True)
            for i in range(n)]


def mitte(w):
    return (D - w) / 2


teile = [
    teil('seitenwand_oben', 'tire_rubber', 'Seitenwand oben', 'Seitenwand', 'cyl',
         x=mitte(644), y=mitte(644), w=644, z=1, h=48, mass=85, form='torus',
         info='Dünne Gummischicht über der Karkasse. Hier stehen Größe (z. B. 50-559) und der erlaubte Luftdruck. '
              'Alte Reifen nimmt der Fahrradladen oder der Wertstoffhof an.',
         color='#3A3D40', marks=[*ring(646, 566, '#232527', 50), mark('box', 290, 10, 66, 8, 2, '#8E969A', zeichnung=True),
                                 mark('box', 290, 628, 66, 8, 2, '#8E969A', zeichnung=True)]),
    teil('wulst_oben', 'steel_bead_wire', 'Wulstkern oben', 'Wulstkern', 'cyl',
         x=mitte(574), y=mitte(574), w=574, z=42, h=4, mass=32, form='torus',
         info='Ring aus mehreren Windungen Stahldraht an der Innenkante. Er hält den Reifen auf der Felge. '
              'Faltreifen haben stattdessen einen Kern aus Aramidfasern.',
         color='#B8BEC2', marks=ring(574, 558, '#5A6268', 4)),
    teil('laufflaeche', 'tire_rubber', 'Lauffläche mit Profil', 'Lauffläche', 'cyl',
         x=0, y=0, w=D, z=0, h=50, mass=300, form='torus',
         info='Dicke Gummimischung aus Natur- und Synthesekautschuk mit Ruß, außen mit Stollenprofil. '
              'Sie nutzt sich ab; ist das Profil weg, wird der Reifen getauscht.',
         color=GUMMI, sortBias=4, marks=ring(D, 600, '#1E2022', 40) + stollen(D, 312, 48) + stollen(D, 302, 48, 6)),
    teil('pannenschutz', 'tire_casing_fabric', 'Pannenschutzgürtel', 'Pannenschutz', 'cyl',
         x=mitte(640), y=mitte(640), w=640, z=8, h=34, mass=40, form='torus',
         info='Ein Streifen aus dichtem Gewebe oder Spezialgummi unter der Lauffläche. Er hält Scherben und Dornen vom Schlauch fern.',
         color='#C9B98A', marks=ring(640, 606, '#A89A70', 34)),
    teil('karkasse', 'tire_casing_fabric', 'Karkasse (Gewebeunterbau)', 'Karkasse', 'cyl',
         x=mitte(642), y=mitte(642), w=642, z=2, h=46, mass=110, form='torus', materials=[['nylon', 70], ['gummi', 30]],
         info='Nylongewebe, das dem Reifen seine Form gibt, mit Gummi getränkt und einvulkanisiert. '
              'Von Hand lässt es sich nicht vom Gummi trennen.',
         color='#D8CBA6', marks=ring(642, 562, '#B3A57E', 44) + [mark('box', 316, 4, 10, 38, 1, '#BFAF84', zeichnung=True),
                                                    mark('box', 316, 600, 10, 38, 1, '#BFAF84', zeichnung=True)]),
    teil('wulst_unten', 'steel_bead_wire', 'Wulstkern unten', 'Wulstkern', 'cyl',
         x=mitte(574), y=mitte(574), w=574, z=4, h=4, mass=32, label=False, form='torus',
         info='Zweiter Wulstkern an der unteren Reifenkante.',
         color='#B8BEC2', marks=ring(574, 558, '#5A6268', 4)),
    teil('seitenwand_unten', 'tire_rubber', 'Seitenwand unten', 'Seitenwand', 'cyl',
         x=mitte(644), y=mitte(644), w=644, z=1, h=48, mass=85, label=False, form='torus',
         info='Gegenstück zur oberen Seitenwand.',
         color='#3A3D40', marks=ring(646, 566, '#232527', 5)),
]

explodiere(teile, abstand=80, nach_liste=True)
skaliere_masse(teile, oid='bicycle_tire')
schreibe('bicycle_tire', teile)
