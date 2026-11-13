"""3D-Modell: bicycle_tire. Erzeugt tools/kategorien/modelle/bicycle_tire.json."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# 26-Zoll-Fahrradreifen (26 × 2,0, ETRTO 50-559) flach liegend: Außendurchmesser 650 mm, Reifenbreite 50 mm = Höhe.
# Die Schichten liegen als konzentrische Ringe übereinander: Seitenwände oben und unten, dazwischen Lauffläche,
# Pannenschutzgürtel und Karkasse, an der Innenkante die beiden Wulstkerne (Ø 559 mm Felgensitz).
# Ringe sind gefüllte Ellipsen; das Loch in der Mitte ist als dunklere Innenfläche markiert.
# Explodiert: alle Schichten werden nach oben abgehoben.
D = 650
GUMMI = '#2B2D2F'
LOCH = '#45484B'


def ring(aussen, innen, fill=LOCH):
    """Innenfläche eines Rings als mark, relativ zu einem Teil mit Durchmesser aussen."""
    o = (aussen - innen) / 2
    return mark('cyl', o, o, innen, fill=fill)


def stollen(aussen, radius, n, gr=10):
    """n Profilstollen auf einem Kreis mit radius um die Teilmitte."""
    c = aussen / 2
    return [mark('box', round(c + radius * math.cos(2 * math.pi * i / n) - gr / 2, 1),
                 round(c + radius * math.sin(2 * math.pi * i / n) - gr / 2, 1), gr, gr, 2, '#1E2022')
            for i in range(n)]


def mitte(w):
    return (D - w) / 2


teile = [
    teil('seitenwand_oben', 'tire_rubber', 'Seitenwand oben', 'Seitenwand', 'cyl',
         x=mitte(646), y=mitte(646), w=646, z=45, h=5, mass=85,
         info='Dünne Gummischicht über der Karkasse. Hier stehen Größe (z. B. 50-559) und der erlaubte Luftdruck. '
              'Alte Reifen nimmt der Fahrradladen oder der Wertstoffhof an.',
         color='#3A3D40', marks=[ring(646, 566), mark('box', 290, 10, 66, 8, 2, '#8E969A'),
                                 mark('box', 290, 628, 66, 8, 2, '#8E969A')]),
    teil('wulst_oben', 'steel_bead_wire', 'Wulstkern oben', 'Wulstkern', 'cyl',
         x=mitte(574), y=mitte(574), w=574, z=42, h=4, mass=32,
         info='Ring aus mehreren Windungen Stahldraht an der Innenkante. Er hält den Reifen auf der Felge. '
              'Faltreifen haben stattdessen einen Kern aus Aramidfasern.',
         color='#9AA2A6', marks=[ring(574, 558, '#5A6268')]),
    teil('laufflaeche', 'tire_rubber', 'Lauffläche mit Profil', 'Lauffläche', 'cyl',
         x=0, y=0, w=D, z=5, h=40, mass=300,
         info='Dicke Gummimischung aus Natur- und Synthesekautschuk mit Ruß, außen mit Stollenprofil. '
              'Sie nutzt sich ab; ist das Profil weg, wird der Reifen getauscht.',
         color=GUMMI, marks=[ring(D, 600)] + stollen(D, 312, 48) + stollen(D, 302, 48, 6)),
    teil('pannenschutz', 'tire_casing_fabric', 'Pannenschutzgürtel', 'Pannenschutz', 'cyl',
         x=mitte(640), y=mitte(640), w=640, z=8, h=34, mass=40,
         info='Ein Streifen aus dichtem Gewebe oder Spezialgummi unter der Lauffläche. Er hält Scherben und Dornen vom Schlauch fern.',
         color='#C9B98A', marks=[ring(640, 606)]),
    teil('karkasse', 'tire_casing_fabric', 'Karkasse (Gewebeunterbau)', 'Karkasse', 'cyl',
         x=mitte(642), y=mitte(642), w=642, z=3, h=44, mass=110, materials=[['nylon', 70], ['gummi', 30]],
         info='Nylongewebe, das dem Reifen seine Form gibt, mit Gummi getränkt und einvulkanisiert. '
              'Von Hand lässt es sich nicht vom Gummi trennen.',
         color='#D8CBA6', marks=[ring(642, 562)] + [mark('box', 316, 4, 10, 38, 1, '#BFAF84'),
                                                    mark('box', 316, 600, 10, 38, 1, '#BFAF84')]),
    teil('wulst_unten', 'steel_bead_wire', 'Wulstkern unten', 'Wulstkern', 'cyl',
         x=mitte(574), y=mitte(574), w=574, z=4, h=4, mass=32, label=False,
         info='Zweiter Wulstkern an der unteren Reifenkante.',
         color='#9AA2A6', marks=[ring(574, 558, '#5A6268')]),
    teil('seitenwand_unten', 'tire_rubber', 'Seitenwand unten', 'Seitenwand', 'cyl',
         x=mitte(646), y=mitte(646), w=646, z=0, h=5, mass=85, label=False,
         info='Gegenstück zur oberen Seitenwand.',
         color='#3A3D40', marks=[ring(646, 566)]),
]

explodiere(teile, abstand=70, nach_liste=True)
skaliere_masse(teile, oid='bicycle_tire')
schreibe('bicycle_tire', teile)
