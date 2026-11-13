"""3D-Modell: flashlight. Erzeugt tools/kategorien/modelle/flashlight.json.

Typische Aluminium-LED-Taschenlampe für zwei AA-Batterien, steht aufrecht (Kopf oben, Ø 30 mm, 150 mm hoch).
Körper aus gestapelten Zylinderabschnitten. Explosion: Rohr bleibt stehen, Kopfteile werden darüber gestapelt,
die Batterien nach rechts (dx positiv) und die Endkappe mit Schalter und Feder nach links (dx negativ) gezogen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

ALU = '#3B4147'      # schwarz eloxiertes Aluminium
ALU_HELL = '#C9CED2'
GAP = 14
M = 15  # Mittelachse x = y = 15


def rund(w):
    """x/y für einen Kreis mit Durchmesser w auf der Mittelachse."""
    return dict(x=M - w / 2, y=M - w / 2, w=w)


AA = [['zinkmangan', 80], ['stahl', 20]]
teile = [
    teil('lunette', 'aluminium_housing', 'Frontring (Lünette)', 'Frontring', 'cyl', **rund(30), z=145, h=5, mass=6,
         materials=[['alu', 100]], color=ALU,
         info='Aufgeschraubter Aluminiumring, der Glas und Reflektor festhält. Gegen den Uhrzeigersinn abdrehen.',
         marks=[mark('cyl', 3, 3, 24, fill='#1F2327')]),
    teil('linse', 'lens_glass', 'Schutzglas', 'Glas', 'cyl', **rund(26), z=143, h=2, mass=3,
         materials=[['glas', 100]], color='#C9DEDF', opacity=0.65,
         info='Flache, gehärtete Glasscheibe mit Gummi-Dichtring. Kommt nicht ins Altglas, weil es anders zusammengesetzt ist.'),
    teil('reflektor', 'aluminium_housing', 'Reflektor', 'Reflektor', 'cyl', **rund(26), z=124, h=19, mass=4,
         materials=[['alu', 90], ['pcabs', 10]], color=ALU_HELL,
         info='Spiegelnder Trichter aus bedampftem Aluminium, bündelt das Licht der LED zu einem Strahl.',
         marks=[mark('cyl', 1, 1, 24, fill='#E4E8EB'), mark('cyl', 6, 6, 14, fill='#D3D8DC'), mark('cyl', 10.5, 10.5, 5, fill='#3A3F44')]),
    teil('led', 'led_module', 'LED auf Alu-Platine', 'LED', 'cyl', **rund(16), z=121, h=3, mass=2,
         materials=[['led', 25], ['alu', 45], ['kupfer', 15], ['lot', 5], ['keramik', 10]], color='#ECECE6',
         info='Eine Hochleistungs-LED auf einer runden Aluminiumplatine (Star), die die Wärme an den Kopf abgibt. '
              'Aus dem Reflektor herausschrauben.',
         marks=[mark('box', 5.5, 5.5, 5, 5, 0.5, '#F6D86B'), mark('box', 1.5, 7, 2, 2, 0.3, '#B87333'),
                mark('box', 12.5, 7, 2, 2, 0.3, '#B87333')]),
    teil('treiber', 'led_module', 'Treiberplatine', 'Treiber', 'cyl', **rund(18), z=117, h=4, mass=2,
         material_id='pcb', materials=[['fr4', 50], ['kupfer', 20], ['chip', 20], ['lot', 10]], color='#2E6B45',
         info='Kleine runde Platine, die den Strom für die LED regelt. Mit Gold und Kupfer: zur Elektro-Sammlung.',
         marks=[mark('box', 6, 6, 6, 6, 0.3, '#22272B'), mark('cyl', 2, 7, 3, fill='#3A3F44')]),
    teil('kontaktfeder', 'steel_spring', 'Kontaktfeder vorn', 'Feder vorn', 'cyl', **rund(7), z=114, h=3, mass=0.5,
         materials=[['stahl', 90], ['nickel', 10]], color='#B7BCC0',
         info='Kleine vernickelte Stahlfeder unter der Treiberplatine, drückt auf den Pluspol der Batterie.',
         marks=[mark('cyl', 1.5, 1.5, 4, fill='#8A9095')]),
    teil('kopf', 'aluminium_housing', 'Lampenkopf', 'Kopf', 'cyl', **rund(30), z=112, h=33, mass=16,
         materials=[['alu', 100]], color=ALU,
         info='Breiterer Kopf mit Kühlrippen, auf das Rohr geschraubt. Nimmt Reflektor, LED und Treiber auf.',
         marks=[mark('cyl', 2, 2, 26, fill='#2B3035')]),
    teil('rohr', 'aluminium_housing', 'Batterierohr', 'Rohr', 'cyl', **rund(24), z=14, h=98, explode=[0, 0, 0], mass=24,
         materials=[['alu', 100]], color=ALU,
         info='Eloxiertes Aluminiumrohr mit Gewinde an beiden Enden und geriffeltem Griff. Leer ist es reines Aluminium.',
         marks=[mark('cyl', 2, 2, 20, fill='#1F2327')]),
    teil('batterie_1', 'alkaline_cell', 'Batterie AA (vorn)', 'Batterie 1', 'cyl', **rund(14.5), z=67, h=50.5, mass=23,
         materials=AA, color='#C8423A',
         info='Alkali-Mangan-Batterie, 1,5 Volt. Immer herausnehmen, bevor die Lampe entsorgt wird. '
              'Leere Batterien in die Sammelbox.',
         marks=[mark('cyl', 4.75, 4.75, 5, fill='#B7BCC0')]),
    teil('batterie_2', 'alkaline_cell', 'Batterie AA (hinten)', 'Batterie 2', 'cyl', **rund(14.5), z=16.5, h=50.5, mass=23,
         materials=AA, color='#C8423A', label=False,
         info='Zweite Batterie in Reihe: zusammen 3 Volt. Plus zeigt zum Kopf.',
         marks=[mark('cyl', 4.75, 4.75, 5, fill='#B7BCC0')]),
    teil('endfeder', 'steel_spring', 'Endfeder', 'Feder hinten', 'cyl', **rund(11), z=10, h=6.5, mass=1,
         materials=[['stahl', 100]], color='#B7BCC0',
         info='Kräftige Stahlfeder in der Endkappe, drückt die Batterien nach vorn. Mit einer Zange herausziehen.',
         marks=[mark('cyl', 1.5, 1.5, 8, fill='#8A9095'), mark('cyl', 3, 3, 5, fill='#B7BCC0')]),
    teil('schalter', 'aluminium_housing', 'Druckschalter', 'Schalter', 'cyl', **rund(16), z=4, h=6,
         material_id='mixed_electronics', mass=3, materials=[['messing', 40], ['pcabs', 40], ['stahl', 20]],
         color='#5E656A',
         info='Klickschalter mit Messingkontakten, rastet bei jedem Druck ein oder aus. In die Endkappe geschraubt.',
         marks=[mark('cyl', 4, 4, 8, fill='#B08D57')]),
    teil('endkappe', 'aluminium_housing', 'Endkappe', 'Endkappe', 'cyl', **rund(26), z=1, h=13, mass=8,
         materials=[['alu', 100]], color=ALU,
         info='Abschraubbarer Deckel am Ende. Hier werden die Batterien gewechselt.',
         marks=[mark('cyl', 2, 2, 22, fill='#2B3035')]),
    teil('gummikappe', 'aluminium_housing', 'Gummikappe', 'Gummikappe', 'cyl', **rund(12), z=0, h=3,
         material_id='rubber', mass=1, materials=[['gummi', 100]], color='#22262A',
         info='Weiche Gummikappe über dem Schalter, hält Wasser und Staub draußen.'),
]

KOPF = ['lunette', 'linse', 'reflektor', 'led', 'treiber', 'kontaktfeder', 'kopf']
BATT = ['batterie_1', 'batterie_2']
ENDE = ['endfeder', 'schalter', 'endkappe', 'gummikappe']
by = {p['id']: p for p in teile}

# Batterien rechts neben dem Rohr, untereinander mit Abstand
b = [by[i] for i in BATT]
explodiere(b, abstand=GAP)
for p in b:
    p['explode'] = [34, 0, round(p['explode'][2] - 16.5, 1)]
# Endkappe mit Schalter und Feder links neben dem Rohr, auf dem Tisch beginnend
e = [by[i] for i in ENDE]
explodiere(e, abstand=GAP)
for p in e:
    p['explode'] = [-36, 0, p['explode'][2]]
# Kopfteile über dem Rohr stapeln (Rohr steht fest)
explodiere([by['rohr']] + [by[i] for i in KOPF], abstand=GAP, nach_liste=True)

skaliere_masse(teile, oid='flashlight')
schreibe('flashlight', teile)
