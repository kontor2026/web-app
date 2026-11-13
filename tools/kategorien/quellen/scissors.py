"""3D-Modell: scissors. Erzeugt tools/kategorien/modelle/scissors.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Geschlossene Bastel-/Haushaltsschere flach auf dem Tisch, Spitze hinten (y = 0), Griffe vorne. 70 × 198 × 10 mm.
# Zwei Edelstahlklingen übereinander (je drei Abschnitte, damit sie zur Spitze schmal zulaufen), Drehpunkt bei
# (35, 100), Kunststoffgriffe (Schaft + Auge) um die Klingenenden gespritzt. Grifflöcher in Tischfarbe.
# Explodiert: Griffe zur Seite, Schraube, Scheibe, Klingen und Mutter übereinander.
STAHL = '#C3C9CE'
STAHL_DUNKEL = '#B2B8BD'
SCHLIFF = '#E3E7EA'
GRIFF = '#D9473A'
SOFT = '#2E3338'
LOCH = '#EEECE5'


def klinge(name, z, dx, info, kurz):
    """Klinge aus drei Abschnitten: Spitze, Mitte, Klingenwurzel mit Angel (steckt im Griff)."""
    pid = f'klinge_{name}'
    oben = name == 'oben'
    segs = [  # (x, y, w, d, r)
        (33 + dx, 0, 4, 40, 2),
        (30.5 + dx, 40, 9, 40, 3),
        (27 + dx, 80, 16, 70, 4),
    ]
    out = []
    for i, (x, y, w, d, r) in enumerate(segs):
        marks = [mark('box', 0 if oben else w - 1.5, 1, 1.5, (d if i < 2 else 30) - 2, 0.5, SCHLIFF)]
        if i == 2:
            marks.append(mark('cyl', 35 - x - 4.5, 100 - y - 4.5, 9, fill='#8E959B'))
        out.append(teil(pid if i == 2 else f'{pid}_{i + 1}', 'steel_blades',
                        f'{"Obere" if oben else "Untere"} Klinge', kurz, 'box',
                        x=x, y=y, w=w, d=d, z=z, h=2.5, r=r, mass=[3, 7, 16][i], label=i == 2,
                        info=info if i == 2 else 'Abschnitt der Klinge, der zur Spitze hin immer schmaler wird.',
                        color=STAHL if oben else STAHL_DUNKEL, marks=marks))
    return out


teile = [
    teil('schraube', 'steel_blades', 'Gelenkschraube', 'Schraube', 'cyl',
         x=31.5, y=96.5, w=7, z=8, h=2, mass=1.5,
         info='Hält beide Klingen zusammen und ist die Drehachse. Mit einem Schraubendreher lösen, '
              'dann fallen die Klingen auseinander.',
         color='#9AA2A6', marks=[mark('box', 0.75, 3, 5.5, 1, fill='#5A6268')]),
    teil('scheibe', 'steel_blades', 'Unterlegscheibe', 'Scheibe', 'cyl',
         x=30.5, y=95.5, w=9, z=7.5, h=0.5, mass=0.3,
         info='Dünne Stahlscheibe unter dem Schraubenkopf. Sie sorgt dafür, dass sich die Klinge leicht dreht.',
         color='#D0D5D9', marks=[mark('cyl', 2.5, 2.5, 4, fill='#5A6268')]),
    *klinge('oben', 5, 0, 'Rostfreier Edelstahl, nur eine Seite ist geschliffen. Vor dem Wegwerfen die Spitze mit '
                          'Klebeband oder Pappe sichern.', 'Klinge oben'),
    *klinge('unten', 2.5, 1.5, 'Gleitet beim Schneiden an der oberen Klinge vorbei. Die Klingen sind wertvoller '
                               'Stahlschrott für den Wertstoffhof.', 'Klinge unten'),
    teil('mutter', 'steel_blades', 'Gewindemutter', 'Mutter', 'cyl',
         x=32, y=97, w=6, z=0.5, h=2, mass=0.8,
         info='Gegenstück zur Gelenkschraube, sitzt versenkt unter der unteren Klinge.',
         color='#9AA2A6', marks=[mark('cyl', 2, 2, 2, fill='#5A6268')]),
    # linker Griff (kleines Auge) gehört zur oberen Klinge
    teil('griff_links', 'plastic_handles', 'Griff mit kleinem Auge', 'Griff links', 'box',
         x=2, y=135, w=33, d=62, z=0.5, h=9, r=14, explode=[-46, 0, 0], mass=9, materials=[['pp', 80], ['tpe', 20]],
         info='Polypropylen mit weicher Griffzone, fest um das Klingenende gespritzt. Lässt er sich nicht abziehen, '
              'mit einer Zange aufbrechen, dann Kunststoff und Stahl getrennt entsorgen.',
         color=GRIFF, marks=[mark('box', 4, 4, 25, 54, 11, SOFT), mark('box', 7, 8, 19, 46, 9, LOCH)]),
    teil('schaft_links', 'plastic_handles', 'Griffschaft links', 'Schaft', 'box',
         x=21, y=114, w=14, d=21, z=0.5, h=9, r=3, explode=[-46, 0, 0], mass=3, label=False,
         materials=[['pp', 100]],
         info='Hier ist die obere Klinge im Kunststoff eingegossen.', color=GRIFF,
         marks=[mark('box', 3, 5, 8, 1, fill='#B53A2F'), mark('box', 3, 9, 8, 1, fill='#B53A2F'),
                mark('box', 3, 13, 8, 1, fill='#B53A2F')]),
    # rechter Griff (großes Auge) gehört zur unteren Klinge
    teil('griff_rechts', 'plastic_handles', 'Griff mit großem Auge', 'Griff rechts', 'box',
         x=36, y=128, w=33, d=70, z=0.5, h=9, r=14, explode=[40, 0, 0], mass=11, materials=[['pp', 80], ['tpe', 20]],
         info='Das größere Auge ist für zwei bis drei Finger und gehört zur unteren Klinge.',
         color=GRIFF, marks=[mark('box', 4, 4, 25, 62, 11, SOFT), mark('box', 7, 8, 19, 54, 9, LOCH)]),
    teil('schaft_rechts', 'plastic_handles', 'Griffschaft rechts', 'Schaft', 'box',
         x=35, y=114, w=14, d=14, z=0.5, h=9, r=3, explode=[40, 0, 0], mass=3, label=False,
         materials=[['pp', 100]],
         info='Hier ist die untere Klinge im Kunststoff eingegossen.', color=GRIFF,
         marks=[mark('box', 3, 4, 8, 1, fill='#B53A2F'), mark('box', 3, 8, 8, 1, fill='#B53A2F')]),
]

explodiere(teile, abstand=14, gruppen=[['klinge_oben', 'klinge_oben_1', 'klinge_oben_2'],
                                       ['klinge_unten', 'klinge_unten_1', 'klinge_unten_2']])
skaliere_masse(teile, oid='scissors')
schreibe('scissors', teile)
