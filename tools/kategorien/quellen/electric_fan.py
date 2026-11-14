"""3D-Modell: electric_fan. Erzeugt tools/kategorien/modelle/electric_fan.json."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Tischventilator: runder Fuß (Ø 250 mm), Standrohr, darauf Motorgehäuse (hinten) und Ventilatorkopf Ø 300 mm,
# Mitte bei z = 290, Luft bläst nach vorne (+y). Die senkrechten runden Schutzgitter bestehen aus waagerechten
# Drahtringen (dünne Scheiben mit Lücken, Breite = Kreissehne), dazwischen sieht man die Flügel. Die Flügel sind
# eine gestufte Kreisscheibe. Explosion entlang der Achse: Spinner, Frontgitter, Flügel nach vorne (dy > 0),
# Motorgehäuse nach hinten (dy < 0), Rückgitter und Motor bleiben. Gewicht aus dem Fuß nach links, Kabel nach rechts.
# Malerreihenfolge über sortBias: Fuß < Motor/Gehäuse < Rückgitter < Flügel < Frontgitter.
ZM, XM = 290, 150
WEISS = '#E9EEF2'
CHROM = '#E2E5E8'


def sehne(radius, dz):
    return 2 * math.sqrt(max(radius * radius - dz * dz, 0))


def gitter(gid, name, short, y, d, dy, mass, info, bias, woelbung):
    teile, n = [], 15
    for k in range(n):
        zc = 150 + k * 20
        w = round(sehne(148, zc - ZM), 1)
        yk = round(y + woelbung * w / 296, 1)  # Gitterkorb gewölbt: Mitte steht weiter vor bzw. zurück
        teile.append(teil(f'{gid}{k}', 'fan_guard', name, short, 'box',
                          x=round(XM - w / 2, 1), y=yk, w=w, d=d, z=zc - 2, h=4, r=2, explode=[0, dy, 0],
                          mass=mass / n, materials=[['stahl', 95], ['pp', 5]], color=CHROM, label=k == 7,
                          sortBias=bias, info=info if k == 7 else f'Drahtring des {name}s.'))
    return teile


front = gitter('frontgitter', 'Frontgitter', 'Frontgitter', 170, 8, 220, 150,
               'Verchromter Stahldraht mit Kunststoffmitte. Die Klammern am Rand öffnen, dann lässt sich das Gitter '
               'abnehmen.', 0, 16)
rueck = gitter('rueckgitter', 'Rückgitter', 'Rückgitter', 122, 8, 0, 160,
               'Hinterer Gitterkorb, mit der Gittermutter am Motor festgeschraubt. Mutter lösen und abnehmen.', -400, -18)
fluegel = []
for k in range(10):
    z0 = 165 + k * 25
    w = round(sehne(125, z0 + 12.5 - ZM), 1)
    fluegel.append(teil(f'fluegel{k}', 'fan_blades', 'Ventilatorflügel', 'Flügel', 'box',
                        x=round(XM - w / 2, 1), y=140, w=w, d=22, z=z0, h=25, r=8, explode=[0, 100, 0], mass=12,
                        materials=[['pp', 100]], color='#5DADE2', opacity=0.85, label=k == 4, sortBias=-300,
                        info='Drei bis fünf Flügel aus Polypropylen auf einer Nabe. Reiner Kunststoff, gehört nach dem '
                             'Abziehen zum Kunststoffrecycling.' if k == 4 else 'Teil des Flügelrads.'))

teile = [
    teil('spinner', 'fan_blades', 'Spinnerkappe', 'Spinner', 'cyl',
         x=130, y=192, w=40, d=22, z=272, h=36, explode=[0, 300, 0], mass=20, materials=[['pp', 100]],
         info='Kunststoffkappe vorne auf der Welle mit Linksgewinde. Im Uhrzeigersinn aufdrehen, dann lassen sich die '
              'Flügel abziehen.', color='#3F8FC4', marks=[mark('cyl', 12, 5, 16, 12, fill='#5DADE2')]),
    *front,
    teil('nabe', 'fan_blades', 'Flügelnabe', 'Nabe', 'box',
         x=128, y=138, w=44, d=28, z=268, h=44, r=10, explode=[0, 150, 0], mass=25, materials=[['pp', 100]],
         color='#2F7BB0', sortBias=-299,
         info='Mitte des Flügelrads mit einer Messinghülse, die auf die Motorwelle gesteckt wird.',
         marks=[mark('cyl', 17, 9, 10, fill='#B08D57')]),
    *fluegel,
    teil('gittermutter', 'fan_guard', 'Gittermutter', 'Gittermutter', 'box', material_id='pp',
         x=120, y=88, w=60, d=12, z=260, h=60, r=6, explode=[0, 45, 0], mass=15, materials=[['pp', 100]],
         color='#9AA2A6', sortBias=-450,
         info='Große Kunststoffmutter, die das Rückgitter gegen den Motor drückt. Von Hand abdrehen.',
         marks=raster(4, 2, 7, 1, 4, 8, 7.4, r=1, fill='#7E868C')),
    *rueck,
    teil('schwenkknopf', 'plastic_housing', 'Schwenkknopf', 'Schwenkknopf', 'cyl', material_id='pp',
         x=140, y=40, w=20, z=360, h=18, explode=[0, -110, 60], mass=8, materials=[['pp', 100]],
         color='#9AA2A6', sortBias=-480,
         info='Herunterdrücken koppelt das Schwenkgetriebe an: dann dreht sich der Kopf hin und her.',
         marks=[mark('cyl', 5, 5, 10, fill='#7E868C')]),
    teil('kondensator', 'electric_motor', 'Anlaufkondensator', 'Kondensator', 'box', material_id='mixed_electronics',
         x=175, y=35, w=22, d=30, z=300, h=34, r=4, explode=[0, 0, 150], mass=25,
         materials=[['pp', 40], ['alu', 30], ['pcabs', 25], ['kupfer', 5]], color='#3B3F44', sortBias=-480,
         info='Gibt dem Motor beim Einschalten den Anstoß in die richtige Drehrichtung. Kann noch Ladung haben: '
              'Anschlüsse nicht berühren.', marks=[mark('box', 3, 4, 16, 22, 2, '#5E656A')]),
    teil('motorgehaeuse', 'plastic_housing', 'Motorgehäuse', 'Motorgehäuse', 'box',
         x=90, y=20, w=120, d=82, z=240, h=120, r=34, explode=[0, -110, 0], mass=200, sortBias=-490,
         info='Zwei Kunststoffschalen um den Motor, oben der Schwenkknopf. Schrauben von hinten lösen.',
         color=WEISS, marks=[mark('cyl', 50, 20, 20, fill='#C9CED2')] + raster(16, 46, 6, 1, 6, 26, 15, r=3,
                                                                                   fill='#C2C8CD')),
    teil('motor', 'electric_motor', 'Spaltpolmotor mit Schwenkgetriebe', 'Motor', 'box',
         x=105, y=30, w=90, d=70, z=255, h=90, r=25, explode=[0, 0, 0], mass=900, sortBias=-500,
         materials=[['kupfer', 25], ['stahl', 60], ['nylon', 5], ['alu', 5], ['pcabs', 5]],
         info='Motor mit Kupferwicklung und Eisenkern, hinten ein kleines Getriebe aus Nylon für das Hin- und '
              'Herschwenken. Mit vier Schrauben am Gitter befestigt.',
         marks=[mark('box', 10, 10, 70, 50, 15, fill='#B87333'), mark('cyl', 35, 25, 20, fill='#9AA2A6')]),
    teil('neigegelenk', 'plastic_housing', 'Neigegelenk', 'Neigegelenk', 'box', material_id='steel',
         x=125, y=55, w=50, d=50, z=215, h=25, r=8, explode=[0, -110, -40], mass=60, sortBias=-520,
         materials=[['stahl', 70], ['pcabs', 30]], color='#C9CDD0',
         info='Gelenk mit Rastscheibe und Flügelschraube, damit man den Kopf nach oben oder unten neigen kann.',
         marks=[mark('cyl', 15, 15, 20, fill='#5E656A')]),
    teil('standrohr', 'plastic_housing', 'Standrohr', 'Standrohr', 'cyl', material_id='steel',
         x=132, y=62, w=36, z=40, h=175, explode=[0, 0, 0], mass=250, materials=[['stahl', 60], ['pcabs', 40]],
         info='Stahlrohr mit Kunststoffhülle, verstellt die Höhe des Kopfes. Durch das Rohr läuft das Motorkabel.',
         color=WEISS, sortBias=-530, marks=[mark('cyl', 10, 10, 16, fill='#B8BEC4')]),
    teil('tasten', 'plastic_housing', 'Stufenschalter', 'Schalter', 'box', material_id='mixed_electronics',
         x=100, y=200, w=100, d=30, z=40, h=10, r=4, explode=[0, 70, 0], mass=50, sortBias=-560,
         materials=[['pcabs', 60], ['kupfer', 20], ['kontakte', 10], ['stahl', 10]],
         info='Drucktasten für Aus und drei Stufen. Darunter sitzen Kontakte aus Messing und Kupferkabel.',
         color='#9AA2A6', marks=raster(5, 5, 4, 1, 19, 20, 23.5, r=3, fill=WEISS)),
    teil('gewicht', 'plastic_housing', 'Stahlgewicht im Fuß', 'Gewicht', 'cyl', material_id='steel',
         x=55, y=30, w=190, z=6, h=14, explode=[0, 300, 0], mass=450, materials=[['stahl', 100]],
         color='#B3B9BE', sortBias=-590,
         info='Schwere Stahlscheibe, damit der Ventilator nicht kippt. Nach dem Ausschrauben reines Altmetall.',
         marks=[mark('cyl', 80, 80, 30, fill='#4A5156')]),
    teil('fuss', 'plastic_housing', 'Standfuß', 'Standfuß', 'cyl',
         x=25, y=0, w=250, z=0, h=40, explode=[0, 0, 0], mass=250, materials=[['pcabs', 100]],
         info='Runder Kunststofffuß; innen liegt die Stahlscheibe. Von unten verschraubt, Kunststoff und Metall trennen.',
         color=WEISS, sortBias=-600, marks=[mark('cyl', 25, 25, 200, fill='#DDE2E6'), mark('cyl', 107, 37, 36, fill='#C9CED2')]),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=180, y=10, w=80, d=8, z=5, h=8, r=4, explode=[140, 0, 0], mass=120, materials=[['pvc', 90], ['pp', 10]],
         info='Etwa 1,5 m PVC-Mantel mit Eurostecker. Längs aufschlitzen, um die Kupferadern freizulegen.',
         color='#2E3338', marks=[mark('box', 70, 1, 10, 6, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=180, y=12.5, w=80, d=3, z=7.5, h=3, r=1, explode=[140, 0, 15], mass=50,
         info='Zwei Kupferadern aus feiner Litze. Kupfer lässt sich fast verlustfrei wiederverwerten.',
         color='#B87333'),
]

# Foto-Ansicht: echte Formen (Kabel liegend, Spulen als Ring); Details darauf nur in der Zeichnung
FORMEN = {'kabel': ('liegend_x', 1), 'kupferadern': ('liegend_x', 1), 'spinner': ('kugel', 1)}
for p in teile:
    if p['id'] in FORMEN:
        p['form'], nur_zeichnung = FORMEN[p['id']]
        p.pop('wand', None)
        p.pop('boden', None)
        for m in (p.get('marks') or []) if nur_zeichnung else []:
            m['zeichnung'] = True
skaliere_masse(teile, oid='electric_fan')
schreibe('electric_fan', teile)
