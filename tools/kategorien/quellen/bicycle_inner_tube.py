"""3D-Modell: bicycle_inner_tube. Erzeugt tools/kategorien/modelle/bicycle_inner_tube.json.

Typischer Fahrradschlauch 28 Zoll mit Autoventil (Schrader), zusammengelegt zu einem Ring (Ø 300 mm,
etwa 22 mm hoch; in der Foto-Ansicht ein echter Ring, form='torus'). Das Ventil steht senkrecht aus dem Ring. Explodiert stapeln Kappe,
Ventileinsatz, Rändelmutter, Ventilschaft und Gummifuß über dem Schlauch.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

D = 300
GUMMI = '#2B2D2F'
MESSING = '#C9A548'
VX, VY = 150, 12   # Mitte des Ventils auf dem Ring (über der Rohrmitte des Torus)


def nur_zeichnung(ms):
    """marks nur für die Zeichnung (in der Foto-Ansicht ist der Schlauch ein echter Ring, form='torus')."""
    return [{**m, 'zeichnung': True} for m in ms]


def rund(w, cx=VX, cy=VY):
    """Linke hintere Ecke eines Kreises mit Durchmesser w um (cx, cy)."""
    return dict(x=cx - w / 2, y=cy - w / 2, w=w)


teile = [
    teil('kappe', 'tube_valve', 'Ventilkappe', 'Kappe', 'cyl',
         material_id='pp', materials=[['pp', 100]], **rund(9), z=24, h=10, mass=0.5,
         info='Kunststoffkappe gegen Schmutz und Wasser. Abschrauben, sie gehört in den Restmüll.',
         color='#1F2224', marks=[mark('cyl', 1.5, 1.5, 6, fill='#33373A')]),
    teil('einsatz', 'tube_valve', 'Ventileinsatz', 'Einsatz', 'cyl',
         material_id='copper', materials=[['messing', 80], ['stahl', 12], ['gummi', 8]], **rund(4), z=19, h=12,
         mass=1,
         info='Kleines Rückschlagventil mit Feder und Gummidichtung, eingeschraubt in den Schaft. Mit einem '
              'Ventilschlüssel herausdrehen, dann entweicht die Luft ganz.',
         color=MESSING, marks=[mark('cyl', 1.25, 1.25, 1.5, fill='#8F7430')]),
    teil('mutter', 'tube_valve', 'Rändelmutter', 'Mutter', 'cyl',
         material_id='copper', materials=[['messing', 90], ['nickel', 10]], **rund(14), z=20, h=4, mass=2,
         info='Vernickelte Messingmutter, hält das Ventil im Felgenloch. Abschrauben, bevor man den Schlauch '
              'aus der Felge zieht.',
         color='#C6CBCF', marks=[mark('cyl', 3, 3, 8, fill='#8E969A')]),
    teil('schaft', 'tube_valve', 'Ventilschaft', 'Ventilschaft', 'cyl',
         material_id='copper', materials=[['messing', 100]], **rund(8), z=6, h=26, mass=6,
         info='Messingrohr mit Gewinde, unten in den Gummifuß einvulkanisiert. Mit einem scharfen Messer '
              'samt Fuß herausschneiden: Messing ist wertvoller Metallschrott.',
         color=MESSING, marks=[mark('cyl', 2, 2, 4, fill='#8F7430')]),
    teil('ventilfuss', 'butyl_tube', 'Gummifuß des Ventils', 'Ventilfuß', 'cyl',
         **rund(24), z=21, h=2, mass=3,
         info='Verstärkte Gummiplatte, mit der das Ventil fest mit dem Schlauch verbunden ist.',
         color='#3A3D40'),
    teil('schlauch', 'butyl_tube', 'Butylschlauch', 'Schlauch', 'cyl',
         x=0, y=0, w=D, z=0, h=21, mass=130,
         info='Luftdichter Butylkautschuk mit Ruß, zusammengelegt. Ein Loch lässt sich flicken. Alte Schläuche '
              'eignen sich als Spanngummi oder Bastelmaterial, sonst Wertstoffhof oder Fahrradladen.',
         color=GUMMI, form='torus', marks=nur_zeichnung([mark('cyl', 8, 8, 284, fill='#323538'), mark('cyl', 20, 20, 260, fill='#2B2D2F'),
                             mark('cyl', 42, 42, 216, fill='#323538'),
                             mark('cyl', 50, 50, 200, fill='#1C1E20'),  # Innenwand des Lochs
                             mark('cyl', 75.5, 75.5, 170, fill='#DCD8CE'),  # Tisch, durch das Loch gesehen
                             mark('box', 126, 280, 48, 6, 2, '#8E969A'), mark('box', 120, 4, 8, 4, 1, '#8E969A')])),
]
explodiere(teile, abstand=25, nach_liste=True)
skaliere_masse(teile, oid='bicycle_inner_tube')
schreibe('bicycle_inner_tube', teile)
