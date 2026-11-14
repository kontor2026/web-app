"""3D-Modell: drinking_glass. Erzeugt tools/kategorien/modelle/drinking_glass.json.

Typisches Wasserglas (Becherglas, ca. 250 ml) aus Kalk-Natron-Glas, nach oben leicht konisch (oben Ø 75 mm,
unten Ø 62 mm), mit dickem Boden. Das Glas ist ein Stück; die konische Wand ist aus Scheiben gestapelt.
Explodiert schweben Trinkrand, Wand und Boden mit kleinem Abstand übereinander.
Auf dem Rand ist der Blick ins Glas als Mark gezeichnet: Der Innenboden liegt in der Iso-Ansicht um seine Tiefe
nach vorn versetzt (Versatz in x und y = Höhenunterschied).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

GLAS = '#DCEAE6'
OP = 0.4
N = 4                      # Scheiben der konischen Wand
Z0, Z1 = 12, 104           # Wand von Oberkante Boden bis Unterkante Rand
D0, D1 = 63, 74.5          # Durchmesser unten / oben

wand = []
for i in range(N):
    dm = round(D0 + (D1 - D0) * (i + 0.5) / N, 2)
    h = (Z1 - Z0) / N
    wand.append(teil(f'wand_{i + 1}', 'drinking_glass_body', 'Glaswand', 'Wand', 'cyl',
                     x=round((75 - dm) / 2, 2), y=round((75 - dm) / 2, 2), w=dm, z=round(Z0 + i * h, 2),
                     h=round(h, 2), mass=36, label=i == N - 1,
                     info='Nur etwa 2 mm dünne Wand aus gepresstem oder geblasenem Kalk-Natron-Glas. Trinkglas hat '
                          'eine andere Zusammensetzung und einen höheren Schmelzpunkt als Flaschenglas.'
                          if i == N - 1 else 'Abschnitt der leicht konischen Glaswand.',
                     color=GLAS, opacity=OP + 0.01 * (i % 2), wand=2, boden=0))
# Foto-Ansicht: hohle Ringe; die Deckkraft wechselt minimal, damit die Ringe nicht zu einem massiven Körper verschmelzen
wand.reverse()  # oberste Scheibe zuerst

# Blick von oben ins Glas: dunklere Innenwand, Innenboden um die Tiefe nach vorn versetzt.
innen = [mark('cyl', 2, 2, 71, fill='#CBDCD7', zeichnung=True), mark('cyl', 14, 14, 59, fill='#D9E7E3', zeichnung=True),
         mark('cyl', 40, 18, 22, 8, fill='#F4F9F8', zeichnung=True)]

teile = [
    teil('rand', 'drinking_glass_body', 'Trinkrand', 'Rand', 'cyl',
         x=0, y=0, w=75, z=104, h=6, mass=12,
         info='Feuerpolierter Rand, nur etwa 1,5 mm dick. Angeschlagene Gläser nicht mehr benutzen: Die Kante ist '
              'scharf und kann die Lippe schneiden.',
         color=GLAS, opacity=OP, wand=1.8, boden=0, marks=innen),
    *wand,
    teil('boden', 'drinking_glass_body', 'Dicker Glasboden', 'Boden', 'cyl',
         x=6.5, y=6.5, w=62, z=0, h=12, mass=95,
         info='Massiver Boden, damit das Glas nicht umkippt. Kaputte Trinkgläser kommen in Zeitungspapier gewickelt in '
              'den Restmüll, nicht in den Altglascontainer: Schon ein Stück verdirbt eine ganze Ladung Flaschenglas.',
         color='#CFE0DB', opacity=0.7,
         marks=[mark('cyl', 3, 3, 56, fill='#C2D6D0', zeichnung=True), mark('cyl', 16, 16, 30, fill='#D5E5E0', zeichnung=True)]),
]
explodiere(teile, abstand=28, nach_liste=True, gruppen=[[p['id'] for p in wand]])
skaliere_masse(teile, oid='drinking_glass')
schreibe('drinking_glass', teile)
