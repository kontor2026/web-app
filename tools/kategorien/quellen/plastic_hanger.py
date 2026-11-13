"""3D-Modell: plastic_hanger. Erzeugt tools/kategorien/modelle/plastic_hanger.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Kunststoff-Kleiderbügel mit Hosenstange und drehbarem Stahlhaken, flach liegend (laut CSV 420 × 200 × 10 mm),
# Haken hinten (y = 0). Der Körper ist ein Spritzgussteil aus Polystyrol; die schrägen Schultern sind als Treppe
# aus Stücken gebaut, die sich an den Ecken berühren. Explodiert: Haken herausgedreht und angehoben,
# Schultern, Enden und Hosenstange in der Ebene auseinandergezogen.
PS = '#2B2D2F'
STAHL = '#C3C9CE'
LOCH = '#45484B'
N = 8


def schulter(seite, dx):
    """Schräge Schulter vom Hals (y = 75) bis zum Schulterende (y = 150) als N Stücke."""
    w, d = 183 / N, 75 / N
    teile = []
    for i in range(N):
        x = 195 - (i + 1) * w if seite == 'l' else 225 + i * w
        erstes = i == 0
        teile.append(teil(f'schulter_{seite}_{i + 1}', 'ps_hanger_body',
                          'Schulterbogen links' if seite == 'l' else 'Schulterbogen rechts', 'Schulter', 'box',
                          x=round(x, 3), y=round(75 + i * d, 3), w=round(w, 3), d=round(d, 3), z=0, h=10, r=3,
                          explode=[dx, 0, 0], mass=1.6, label=erstes,
                          info=('Die schrägen Arme tragen Hemd oder Jacke. Polystyrol ist hart, kann aber bei Kälte '
                                'brechen.') if erstes else 'Abschnitt des Schulterbogens.',
                          color=PS))
    return teile


teile = [
    teil('haken', 'steel_hook', 'Haken', 'Haken', 'cyl',
         x=185, y=0, w=50, d=46, z=3, h=4, explode=[0, -35, 20], mass=6,
         info='Verchromter Stahldraht, im Hals eingedreht, damit er sich drehen lässt. Mit einer Zange '
              'herausdrehen; der Stahl gehört zum Altmetall.',
         color=STAHL, marks=[mark('cyl', 4, 4, 42, 38, fill=LOCH), mark('box', 0, 26, 12, 20, 4, LOCH)]),
    teil('hakenschaft', 'steel_hook', 'Hakenschaft mit Gewinde', 'Hakenschaft', 'box',
         x=208, y=46, w=4, d=30, z=3, h=4, r=2, explode=[0, -35, 20], mass=2, label=False,
         info='Gerades Ende des Hakens, das im Kunststoff steckt.', color=STAHL,
         marks=raster(0, 18, 1, 5, 4, 1, 0, 2.4, fill='#8E969A')),
    teil('hals', 'ps_hanger_body', 'Hals mit Hakenaufnahme', 'Hals', 'box',
         x=195, y=62, w=30, d=26, z=0, h=10, r=5, explode=[0, -10, 0], mass=4,
         info='Verdickter Mittelteil mit Bohrung für den Haken. Oft ist hier die Kunststoffsorte eingeprägt (PS 6).',
         color=PS, marks=[mark('cyl', 12, 1, 6, fill=LOCH), mark('box', 7, 14, 16, 6, 2, '#3A3F44')]),
    *schulter('l', -12),
    *schulter('r', 12),
    teil('ende_l', 'ps_hanger_body', 'Schulterende links mit Kerben', 'Schulterende', 'box',
         x=0, y=150, w=22, d=36, z=0, h=10, r=6, explode=[-24, 0, 0], mass=4,
         info='Breites Ende mit Kerben, in die man Träger von Kleidern hängt.',
         color=PS, marks=raster(3, 6, 1, 3, 16, 3, 0, 5, r=1, fill=LOCH)),
    teil('ende_r', 'ps_hanger_body', 'Schulterende rechts mit Kerben', 'Schulterende', 'box',
         x=398, y=150, w=22, d=36, z=0, h=10, r=6, explode=[24, 0, 0], mass=4, label=False,
         info='Gegenstück zum linken Schulterende.',
         color=PS, marks=raster(3, 6, 1, 3, 16, 3, 0, 5, r=1, fill=LOCH)),
    teil('hosenstange', 'ps_hanger_body', 'Hosenstange', 'Hosenstange', 'box',
         x=0, y=186, w=420, d=12, z=1, h=8, r=4, explode=[0, 20, 0], mass=8,
         info='Gerippte Stange, auf der Hosen nicht rutschen. Kleiderbügel sind keine Verpackung: '
              'weiterverwenden oder beim Modehändler abgeben, sonst Restmüll.',
         color=PS, marks=raster(40, 3, 23, 1, 3, 6, 15, r=1, fill='#3A3F44')),
]

skaliere_masse(teile, oid='plastic_hanger', stellen=2)
schreibe('plastic_hanger', teile)
