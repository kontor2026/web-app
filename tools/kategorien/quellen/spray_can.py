"""3D-Modell: spray_can. Erzeugt tools/kategorien/modelle/spray_can.json.

Typische Deo-Spraydose 150 ml (Aluminium-Monoblock, 53 × 190 mm mit Kappe). Dosenabschnitte bewegen sich
gemeinsam, Ventilteile und Kappe stapeln sich darüber, Steigrohr und Druck werden seitlich herausgezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402


def scheiben(teile, pid, n):
    """Foto-Ansicht: hohes Teil in n Scheiben teilen, damit die glatte Hülle (Stapel) nur oben einzieht."""
    i = next(k for k, p in enumerate(teile) if p['id'] == pid)
    p = teile[i]
    zs = [round(p['z'] + k * p['h'] / n, 2) for k in range(n)] + [p['z'] + p['h']]
    neu = []
    for k in range(n):
        q = dict(p, z=zs[k], h=round(zs[k + 1] - zs[k], 2), mass=round(p['mass'] / n, 3))
        if k < n - 1:
            q.update(id=f'{pid}_{k + 1}', label=False, marks=None)
            q = {f: v for f, v in q.items() if v is not None}
        neu.append(q)
    teile[i:i + 1] = neu[::-1]


ALU = '#D5D8DB'
teile = [
    teil('kappe', 'pp_spray_cap', 'Schutzkappe', 'Kappe', 'cyl',
         x=0.5, y=0.5, w=52, z=135, h=55, mass=8,
         info='Polypropylen, nur aufgesteckt. Abziehen und getrennt in die Gelbe Tonne geben.',
         color='#2C5F8A', marks=[mark('cyl', 6, 6, 40, fill='#3A6F9C')]),
    teil('spruehkopf', 'spray_valve', 'Sprühkopf', 'Sprühkopf', 'cyl',
         material_id='pp', x=17.5, y=17.5, w=18, z=158, h=14, mass=1.5, materials=[['pp', 100]],
         info='Kunststoffknopf mit feiner Düse. Beim Drücken öffnet er das Ventil und das Spray zerstäubt.',
         color='#E8E8E2', marks=[mark('cyl', 4, 4, 10, fill='#D4D4CE'), mark('cyl', 7.5, 15, 3, fill='#2A2E31')]),
    teil('ventilteller', 'spray_valve', 'Ventilteller', 'Ventilteller', 'cyl',
         x=13.8, y=13.8, w=25.4, z=153, h=5, mass=2.2, materials=[['weissblech', 90], ['gummi', 10]],
         info='Weißblechteller mit Gummidichtung, auf den Dosenrand gepresst (gecrimpt). '
              'Nicht abhebeln: In der Dose kann noch Druck sein.',
         color='#B9BFC4', marks=[mark('cyl', 4.2, 4.2, 17, fill='#A3AAB0'), mark('cyl', 10.7, 10.7, 4, fill='#2A2E31')]),
    teil('ventil', 'spray_valve', 'Ventilgehäuse mit Feder', 'Ventil', 'cyl',
         material_id='pp', x=22.5, y=22.5, w=8, z=137, h=16, mass=0.8, materials=[['pp', 60], ['stahl', 25], ['gummi', 15]],
         info='Kleines Kunststoffgehäuse mit Stahlfeder. Die Feder drückt das Ventil wieder zu, wenn man loslässt.',
         color='#E4E0D2', marks=[mark('cyl', 2, 2, 4, fill='#9DA4AA')]),
    teil('dosenrand', 'aluminium_spray_can_body', 'Dosenrand (Curl)', 'Dosenrand', 'cyl',
         x=13, y=13, w=27, z=150, h=4, mass=1.5,
         info='Eingerollter Rand, auf den der Ventilteller gepresst wird.', color=ALU,
         marks=[mark('cyl', 2.5, 2.5, 22, fill='#8E959B')]),
    teil('schulter', 'aluminium_spray_can_body', 'Dosenschulter', 'Schulter', 'cyl',
         x=3.5, y=3.5, w=46, z=135, h=15, mass=4,
         info='Die Schulter wird aus dem Rohr gedrückt und zum Rand hin immer enger.', color=ALU, label=False),
    teil('rumpf', 'aluminium_spray_can_body', 'Dosenrumpf (Monoblock)', 'Dose', 'cyl',
         x=0, y=0, w=53, z=0, h=135, mass=28,
         info='Aus einem Aluminiumbutzen in einem Stück fließgepresst, der Boden ist nach innen gewölbt. '
              'Nur ganz leer in die Gelbe Tonne. Nie anstechen, zerdrücken oder erhitzen: Explosionsgefahr.',
         color=ALU, marks=[mark('cyl', 3.5, 3.5, 46)]),
    teil('steigrohr', 'spray_valve', 'Steigrohr', 'Steigrohr', 'cyl',
         material_id='ldpe', x=24.75, y=24.75, w=3.5, z=4, h=134, explode=[45, 0, 0], mass=0.3,
         materials=[['ldpe', 100]],
         info='Dünner Schlauch bis zum Boden, durch den der Inhalt zum Ventil gedrückt wird.', color='#EDEDE8'),
    teil('druck', 'aluminium_spray_can_body', 'Außenlack und Druck', 'Druck', 'cyl',
         x=-1, y=-1, w=55, z=12, h=112, explode=[110, 0, 0], mass=0.4, materials=[['druck', 100]],
         info='Direkt auf das Aluminium gedruckt. Verbrennt beim Einschmelzen, das Aluminium wird wieder zu Metall.',
         color='#2C5F8A', wand=0.3, boden=0),
]
explodiere(teile, abstand=18, nach_liste=True, gruppen=[['dosenrand', 'schulter', 'rumpf']])
scheiben(teile, 'rumpf', 3)
skaliere_masse(teile, oid='spray_can')
schreibe('spray_can', teile)
