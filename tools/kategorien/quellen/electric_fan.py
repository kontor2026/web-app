"""3D-Modell: electric_fan. Erzeugt tools/kategorien/modelle/electric_fan.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Tischventilator: runder Fuß (Ø 250 mm), Standrohr, darauf Motorgehäuse (hinten) und Ventilatorkopf Ø 300 mm,
# Luft bläst nach vorne (+y). Die senkrechten runden Schutzgitter sind aus drei waagerechten Scheiben angenähert
# (Mitte 300 breit, oben/unten 210 breit). Explosion entlang der Achse: Spinner, Frontgitter und Flügel nach vorne
# (dy > 0), Motorgehäuse nach hinten (dy < 0); Motor, Rückgitter, Standrohr und Fuß bleiben. Kabel nach rechts.

def gitter(teil_id, name, short, y, d, dy, mass, info, color):
    segs = [('mitte', 0, 300, 210, 180, 0.6), ('oben', 45, 210, 390, 60, 0.2), ('unten', 45, 210, 150, 60, 0.2)]
    return [teil(f'{teil_id}_{s}', 'fan_guard', name if s == 'mitte' else f'{name} ({s})', short, 'box',
                 x=x, y=y, w=w, d=d, z=z, h=h, r=6, explode=[0, dy, 0], mass=mass * f, materials=[['stahl', 95], ['pp', 5]],
                 info=info, color=color, label=s == 'mitte',
                 marks=raster(4, 2, w // 12, 1, 4, d - 4, 12, r=1, fill='#7C858C') if s == 'mitte' else None)
            for s, x, w, z, h, f in segs]


teile = [
    teil('spinner', 'fan_blades', 'Spinnerkappe', 'Spinner', 'cyl',
         x=130, y=195, w=40, d=20, z=280, h=40, explode=[0, 190, 0], mass=20, materials=[['pp', 100]],
         info='Kunststoffkappe vorne auf der Welle mit Linksgewinde. Im Uhrzeigersinn aufdrehen, dann lassen sich die Flügel abziehen.',
         color='#5DADE2'),
    *gitter('frontgitter', 'Frontgitter', 'Frontgitter', 165, 30, 130, 150,
            'Verchromter Stahldraht mit Kunststoffmitte. Die Klammern am Rand öffnen, dann lässt sich das Gitter abnehmen.', '#C9CED2'),
    teil('fluegel', 'fan_blades', 'Ventilatorflügel', 'Flügel', 'box',
         x=25, y=140, w=250, d=25, z=175, h=250, r=20, explode=[0, 70, 0], mass=120, materials=[['pp', 100]],
         info='Drei bis fünf Flügel aus Polypropylen auf einer Nabe. Reiner Kunststoff, gehört nach dem Abziehen zum Kunststoffrecycling.',
         color='#5DADE2', opacity=0.85, marks=[mark('box', 110, 4, 30, 17, 4, fill='#3C4248')]),
    *gitter('rueckgitter', 'Rückgitter', 'Rückgitter', 100, 35, 0, 160,
            'Hinterer Gitterkorb, mit einer Kunststoffmutter am Motor festgeschraubt. Mutter lösen und abnehmen.', '#B8BEC4'),
    teil('motor', 'electric_motor', 'Spaltpolmotor mit Schwenkgetriebe', 'Motor', 'box',
         x=105, y=30, w=90, d=70, z=255, h=90, r=25, explode=[0, 0, 0], mass=900,
         materials=[['kupfer', 25], ['stahl', 60], ['nylon', 5], ['alu', 5], ['pcabs', 5]],
         info='Motor mit Kupferwicklung und Eisenkern, hinten ein kleines Getriebe für das Hin- und Herschwenken. Mit vier Schrauben am Gitter befestigt.',
         marks=[mark('box', 10, 10, 70, 50, 15, fill='#B87333'), mark('cyl', 35, 25, 20, fill='#9AA2A6')]),
    teil('motorgehaeuse', 'plastic_housing', 'Motorgehäuse', 'Motorgehäuse', 'box',
         x=90, y=20, w=120, d=85, z=240, h=120, r=30, explode=[0, -100, 0], mass=200,
         info='Zwei Kunststoffschalen um den Motor, oben der Knopf zum Ein- und Ausschalten des Schwenkens. Schrauben von hinten lösen.',
         color='#E9EEF2', marks=[mark('cyl', 50, 10, 20, fill='#9AA2A6')]),
    teil('standrohr', 'plastic_housing', 'Standrohr', 'Standrohr', 'box', material_id='steel',
         x=130, y=60, w=40, d=40, z=40, h=200, r=18, explode=[0, 0, 0], mass=250, materials=[['stahl', 60], ['pcabs', 40]],
         info='Stahlrohr mit Kunststoffhülle, verstellt die Höhe und Neigung des Kopfes. Durch das Rohr läuft das Motorkabel.',
         color='#E9EEF2'),
    teil('tasten', 'plastic_housing', 'Stufenschalter', 'Schalter', 'box', material_id='mixed_electronics',
         x=100, y=200, w=100, d=35, z=40, h=12, r=3, explode=[0, 50, 0], mass=50,
         materials=[['pcabs', 60], ['kupfer', 20], ['kontakte', 10], ['stahl', 10]],
         info='Drucktasten für Aus und drei Stufen. Darunter sitzen Kontakte aus Messing und Kupferkabel.',
         color='#9AA2A6', marks=raster(6, 6, 4, 1, 18, 22, 24, r=3, fill='#E9EEF2')),
    teil('fuss', 'plastic_housing', 'Standfuß mit Gewicht', 'Standfuß', 'cyl',
         x=25, y=0, w=250, z=0, h=40, explode=[0, 0, 0], mass=700, materials=[['pcabs', 50], ['stahl', 50]],
         info='Runder Kunststofffuß mit einer Stahlplatte als Gewicht, damit der Ventilator nicht kippt. Nach dem Ausschrauben Metall und Kunststoff trennen.',
         color='#E9EEF2', marks=[mark('cyl', 25, 25, 200, fill='#D5DADE')]),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=180, y=10, w=80, d=8, z=5, h=8, r=4, explode=[100, 0, 0], mass=120, materials=[['pvc', 90], ['pp', 10]],
         info='Etwa 1,5 m PVC-Mantel mit Eurostecker. Längs aufschlitzen, um die Kupferadern freizulegen.',
         color='#2E3338', marks=[mark('box', 70, 1, 10, 6, 2, fill='#555')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=180, y=12.5, w=80, d=3, z=7.5, h=3, r=1, explode=[100, 0, 15], mass=50,
         info='Zwei Kupferadern aus feiner Litze. Kupfer lässt sich fast verlustfrei wiederverwerten.',
         color='#B87333'),
]

skaliere_masse(teile, oid='electric_fan')
schreibe('electric_fan', teile)
