"""3D-Modell: thermos_flask. Erzeugt tools/kategorien/modelle/thermos_flask.json.

Typische Edelstahl-Isolierflasche (ca. 0,5 l, Ø 75 mm): doppelwandig mit Vakuum zwischen Außenmantel und
Innenflasche, Verschlussstopfen mit Silikondichtung, aufgeschraubter Trinkbecher als Deckel. Explodiert: Becher,
Stopfen und Dichtung über dem Mantel gestapelt, die Innenflasche seitlich herausgezogen (in Wirklichkeit ist sie
am Hals mit dem Mantel verschweißt).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

STAHL = '#C9CED2'
INNEN = '#B5BBC0'
PP = '#2E3338'

teile = [
    teil('becher', 'pp_lid', 'Trinkbecher (Deckel)', 'Becher', 'cyl',
         x=0, y=0, w=75, z=205, h=65, mass=45,
         info='Polypropylen-Becher, wird über den Hals geschraubt und dient unterwegs als Tasse. Kunststoffteile '
              'abschrauben und getrennt entsorgen.',
         color=PP, marks=[mark('cyl', 4, 4, 67, fill='#3E444A')]),
    teil('stopfen', 'pp_lid', 'Verschlussstopfen', 'Stopfen', 'cyl',
         x=16.5, y=16.5, w=42, z=212, h=26, mass=30,
         info='Schraubstopfen aus PP mit Druckknopf und Ausgießöffnung. Innen ist er hohl, damit wenig Wärme '
              'entweicht.',
         color='#454B51', marks=[mark('cyl', 11, 11, 20, fill='#D9473A'), mark('box', 17, 2, 8, 6, 2, '#1E2226')]),
    teil('dichtung', 'silicone_seal', 'Silikondichtring', 'Dichtung', 'cyl',
         x=14.5, y=14.5, w=46, z=214, h=3, mass=4,
         info='Weicher Ring um den Stopfen, hält die Flasche dicht. Zum Reinigen abziehen, am Ende in den Restmüll.',
         color='#E8E4DA', marks=[mark('cyl', 4, 4, 38, fill='#454B51')]),
    teil('innen_hals', 'stainless_steel_body', 'Hals der Innenflasche', 'Innenhals', 'cyl',
         x=17.5, y=17.5, w=40, z=205, h=17, explode=[100, 0, 0], mass=10, label=False,
         info='Hier sind Innenflasche und Außenmantel miteinander verschweißt. Die Öffnung hat Platz für den Stopfen.',
         color=INNEN, marks=[mark('cyl', 3, 3, 34, fill='#8E959B')]),
    teil('innenflasche', 'stainless_steel_body', 'Innenflasche', 'Innenflasche', 'cyl',
         x=4, y=4, w=67, z=8, h=197, explode=[100, 0, 0], mass=160,
         info='Dünnwandiger Edelstahl, außen oft verkupfert oder verspiegelt. Zwischen ihr und dem Mantel ist ein '
              'Vakuum: Ohne Luft kann kaum Wärme hindurch. Nicht aufbohren!',
         color=INNEN),
    teil('schulter', 'stainless_steel_body', 'Schulter mit Gewinde', 'Schulter', 'cyl',
         x=9.5, y=9.5, w=56, z=200, h=12, mass=20,
         info='Gewinde, auf das der Becher geschraubt wird.', color=STAHL, label=False,
         marks=[mark('cyl', 8, 8, 40, fill='#8E959B')]),
    teil('mantel', 'stainless_steel_body', 'Außenmantel', 'Außenmantel', 'cyl',
         x=0, y=0, w=75, z=4, h=196, mass=150,
         info='Edelstahlrohr, außen gebürstet oder lackiert. Ohne Kunststoffteile gehört die Flasche als Metallschrott '
              'zum Wertstoffhof.',
         color=STAHL),
    teil('bodenkappe', 'stainless_steel_body', 'Bodenkappe', 'Boden', 'cyl',
         x=1.5, y=1.5, w=72, z=0, h=4, mass=15,
         info='Deckt die Stelle ab, an der die Luft beim Herstellen abgesaugt und die Flasche dann verschlossen wurde.',
         color='#B5BBC0', marks=[mark('cyl', 26, 26, 20, fill='#9AA2A6')]),
]
explodiere(teile, abstand=20, nach_liste=True, gruppen=[['schulter', 'mantel']])
skaliere_masse(teile, oid='thermos_flask')
schreibe('thermos_flask', teile)
