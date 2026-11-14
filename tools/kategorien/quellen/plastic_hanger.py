"""3D-Modell: plastic_hanger. Erzeugt tools/kategorien/modelle/plastic_hanger.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Kunststoff-Kleiderbügel mit Hosenstange und drehbarem Stahlhaken, flach liegend (laut CSV 420 × 200 × 10 mm),
# Haken hinten (y = 0). Der Körper ist ein Spritzgussteil aus Polystyrol; die schrägen Schultern sind als Treppe
# aus Stücken gebaut, die sich an den Ecken berühren. Explodiert: Haken herausgedreht und angehoben,
# Schultern, Enden und Hosenstange in der Ebene auseinandergezogen.
PS = '#33373B'
STAHL = '#C3C9CE'
LOCH = '#45484B'
N = 14
BAND = 14  # Breite des Schulterbogens in der Ebene


def schulter(seite, dx):
    """Schräge Schulter vom Hals (y = 75) bis zum Schulterende (y = 150) als N Stücke."""
    w, d = 183 / N, (75 - BAND + 4) / N
    teile = []
    for i in range(N):
        x = 195 - (i + 1) * w if seite == 'l' else 225 + i * w
        erstes = i == 0 and seite == 'l'
        teile.append(teil(f'schulter_{seite}_{i + 1}', 'ps_hanger_body',
                          'Schulterbogen links' if seite == 'l' else 'Schulterbogen rechts', 'Schulter', 'box',
                          x=round(x, 3), y=round(72 + i * d, 3), w=round(w, 3), d=BAND, z=0, h=10, r=2,
                          explode=[dx, 0, 0], mass=0.9, label=erstes, form='liegend_x',
                          info=('Die schrägen Arme tragen Hemd oder Jacke. Polystyrol ist hart, kann aber bei Kälte '
                                'brechen.') if erstes else 'Abschnitt des Schulterbogens.',
                          color=PS, marks=[mark('box', 1, 3, round(w - 2, 3), 1.2, 0.5, '#454A4F', zeichnung=True)]))
    return teile


teile = [
    teil('haken', 'steel_hook', 'Haken', 'Haken', 'box',
         x=183, y=4, w=24, d=5, z=3, h=4, r=1, explode=[0, -35, 20], mass=3, form='liegend_x',
         info='Verchromter Stahldraht, im Hals eingedreht, damit er sich drehen lässt. Mit einer Zange '
              'herausdrehen; der Stahl gehört zum Altmetall.',
         color=STAHL, marks=[mark('box', 2, 1.5, 20, 1, 0.5, '#E6EAED', zeichnung=True)]),
    teil('haken_bogen', 'steel_hook', 'Hakenbogen', 'Hakenbogen', 'box',
         x=178, y=4, w=5, d=30, z=3, h=4, r=2.5, explode=[0, -35, 20], mass=2, label=False, form='liegend_y',
         info='Herabgebogenes Ende des Hakens, das über die Kleiderstange greift.', color=STAHL),
    teil('hakenschaft', 'steel_hook', 'Hakenschaft mit Gewinde', 'Hakenschaft', 'box',
         x=207, y=4, w=5, d=72, z=3, h=4, r=2.5, explode=[0, -35, 20], mass=3, label=False, form='liegend_y',
         info='Gerades Ende des Hakens mit Gewinde, das im Kunststoff steckt.', color=STAHL,
         marks=raster(0.5, 58, 1, 5, 4, 1, 0, 2.4, fill='#8E969A')),
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
         x=0, y=186, w=420, d=12, z=1, h=8, r=4, explode=[0, 20, 0], mass=8, form='liegend_x',
         info='Gerippte Stange, auf der Hosen nicht rutschen. Kleiderbügel sind keine Verpackung: '
              'weiterverwenden oder beim Modehändler abgeben, sonst Restmüll.',
         color=PS, marks=[dict(m, zeichnung=True) for m in raster(40, 3, 23, 1, 3, 6, 15, r=1, fill='#3A3F44')]),
]

skaliere_masse(teile, oid='plastic_hanger', stellen=2)
schreibe('plastic_hanger', teile)
