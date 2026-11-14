"""3D-Modell: inkjet_printer. Erzeugt tools/kategorien/modelle/inkjet_printer.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Einfacher Tintenstrahldrucker ohne Scanner (430 × 360 × 150 mm). Papier wird hinten oben eingelegt (y klein)
# und kommt vorne (y groß) auf das Ausgabefach. Der Druckkopfschlitten mit zwei Patronen fährt auf einer
# Stahlschiene quer (x) hin und her, angetrieben über einen Zahnriemen; ein zweiter Motor treibt die Papierwalze.
# Links unten das Tintenauffangvlies unter der Parkstation, rechts unten Haupt- und Netzteilplatine.
# Explosion: Unterschale bleibt, das Innenleben schwebt schichtweise darüber, die Oberschale ganz oben
# (nach_liste). Ausgabefach nach vorn (dy > 0), Netzkabel nach rechts (dx > 0).
GEH = '#E4E6E8'
DUNKEL = '#3A3F44'
PCB = '#2E6B45'
CHIP = '#22272B'

teile = [
    teil('oberschale', 'plastic_housing', 'Oberschale mit Deckel und Bedienfeld', 'Oberschale', 'box',
         x=0, y=0, w=430, d=360, z=40, h=110, r=8, mass=1100, color=GEH, explode=[0, -430, 120],
         info='Große Kunststoffhaube mit Klappe zu den Patronen. Schrauben sitzen meist hinten und unter Abdeckkappen, dann rundum aufclipsen.',
         marks=[mark('box', 60, 8, 310, 18, 3, DUNKEL), mark('box', 20, 110, 390, 150, 6, '#D5D8DB'),
                mark('box', 330, 290, 80, 50, 4, DUNKEL), mark('cyl', 345, 305, 14, fill='#5DADE2'),
                mark('cyl', 375, 305, 14, fill='#C9CED2')]),
    teil('patrone_schwarz', 'ink_cartridge', 'Tintenpatrone schwarz', 'Patrone schwarz', 'box',
         x=160, y=135, w=22, d=48, z=88, h=55, r=2, mass=35, materials=[['pp', 70], ['schaum', 10], ['druck', 10], ['kupfer', 5], ['chip', 5]],
         color='#2B2F33',
         info='Kunststoffbehälter mit Schwamm, Tintenrest und Kontaktchip. Zum Herausnehmen nach unten drücken; '
              'viele Läden nehmen leere Patronen zurück.',
         marks=[mark('box', 4, 6, 14, 36, 2, '#1E2226')]),
    teil('patrone_farbe', 'ink_cartridge', 'Tintenpatrone dreifarbig', 'Patrone Farbe', 'box',
         x=186, y=135, w=44, d=48, z=88, h=55, r=2, mass=45, materials=[['pp', 70], ['schaum', 10], ['druck', 10], ['kupfer', 5], ['chip', 5]],
         color='#C9CED2',
         info='Drei Kammern für Cyan, Magenta und Gelb. Tintenreste färben stark: nicht schütteln, in Tüte verpacken.',
         marks=[mark('box', 4, 6, 10, 36, 2, '#2AA7C9'), mark('box', 17, 6, 10, 36, 2, '#C9307A'), mark('box', 30, 6, 10, 36, 2, '#E8C547')]),
    teil('druckkopf', 'ink_cartridge', 'Druckkopf mit Düsen', 'Druckkopf', 'box', material_id='mixed_electronics',
         x=160, y=140, w=70, d=40, z=64, h=6, r=2, mass=12,
         materials=[['pcabs', 50], ['chip', 20], ['kupfer', 15], ['stahl', 15]], color='#5E656A',
         info='Hunderte haarfeine Düsen spritzen winzige Tintentropfen aufs Papier. Eingetrocknete Düsen erzeugen Streifen.',
         marks=raster(6, 6, 4, 1, 12, 28, 16, r=1, fill='#22272B')),
    teil('schlitten', 'steel_rail', 'Druckkopfschlitten', 'Schlitten', 'box', material_id='abs',
         x=150, y=125, w=90, d=70, z=70, h=30, r=4, mass=120, materials=[['pcabs', 80], ['kupfer', 10], ['stahl', 5], ['chip', 5]],
         color=DUNKEL,
         info='Hält die Patronen und gleitet auf der Schiene. Ein Flachbandkabel versorgt die winzigen Düsen mit Strom.',
         marks=[mark('box', 8, 8, 74, 50, 3, '#2B2F33')]),
    teil('encoder', 'steel_rail', 'Encoder-Streifen', 'Encoder', 'box', material_id='pet',
         x=20, y=176, w=390, d=2, z=100, h=12, r=0.5, mass=2, materials=[['pet', 95], ['druck', 5]],
         color='#C9DEDF', opacity=0.6,
         info='Durchsichtiger Folienstreifen mit feinen Strichen. Ein Lichtsensor am Schlitten zählt sie und weiß so, wo er ist.'),
    teil('zahnriemen', 'electric_motor', 'Zahnriemen', 'Zahnriemen', 'box', material_id='rubber',
         x=40, y=196, w=350, d=4, z=92, h=6, r=2, mass=10, materials=[['gummi', 85], ['polyester', 15]], color='#1E2226',
         info='Gummiriemen mit Gewebeeinlage, der den Schlitten hin und her zieht. Lässt sich einfach abnehmen.'),
    teil('schiene', 'steel_rail', 'Führungsschiene', 'Schiene', 'box',
         x=20, y=180, w=390, d=14, z=78, h=14, r=3, mass=420, color='#B5BBC0',
         info='Polierte Stahlstange, auf der der Schlitten fährt. An den Seitenteilen verschraubt; reiner Stahl fürs Altmetall.'),
    teil('motor_schlitten', 'electric_motor', 'Schlittenmotor', 'Schlittenmotor', 'cyl',
         x=392, y=200, w=28, z=55, h=38, mass=90, materials=[['stahl', 45], ['kupfer', 30], ['ferrit', 20], ['pcabs', 5]],
         color='#C9CDD0',
         info='Gleichstrommotor mit Kupferwicklung und Magnet, treibt den Zahnriemen an. Drähte abschneiden, ausschrauben.',
         marks=[mark('cyl', 9, 9, 10, fill='#5E656A')]),
    teil('walze', 'steel_rail', 'Papiereinzugswalze', 'Walze', 'box', material_id='steel',
         x=40, y=230, w=350, d=20, z=48, h=20, r=10, mass=320, materials=[['stahl', 70], ['gummi', 30]], color='#5E656A',
         info='Stahlwelle mit Gummirollen, die das Blatt Zeile für Zeile vorschieben. Gummi und Stahl lassen sich trennen.',
         marks=raster(30, 2, 5, 1, 30, 16, 65, r=8, fill='#2B2F33')),
    teil('motor_papier', 'electric_motor', 'Papiervorschubmotor', 'Vorschubmotor', 'cyl',
         x=14, y=270, w=34, z=15, h=40, mass=150, materials=[['stahl', 45], ['kupfer', 30], ['ferrit', 20], ['pcabs', 5]],
         color='#C9CDD0',
         info='Schrittmotor mit Zahnrad, dreht die Papierwalze in genauen kleinen Schritten.',
         marks=[mark('cyl', 11, 11, 12, fill='#F2F2F2')]),
    teil('parkstation', 'ink_cartridge', 'Reinigungs- und Parkstation', 'Parkstation', 'box', material_id='abs',
         x=40, y=150, w=90, d=50, z=34, h=16, r=3, mass=60, materials=[['pcabs', 70], ['gummi', 20], ['stahl', 10]],
         color='#5E656A',
         info='Hier parkt der Schlitten. Gummikappen verschließen die Düsen, eine kleine Pumpe saugt alte Tinte ins Vlies.',
         marks=[mark('box', 10, 10, 30, 28, 4, '#2B2F33'), mark('box', 48, 10, 30, 28, 4, '#2B2F33')]),
    teil('hauptplatine', 'circuit_board', 'Hauptplatine', 'Hauptplatine', 'box',
         x=300, y=30, w=110, d=140, z=12, h=1.6, r=2, mass=110,
         materials=[['fr4', 50], ['kupfer', 20], ['chip', 18], ['stahl', 5], ['lot', 7]], color=PCB,
         info='Steuert Motoren und Druckkopf, mit USB- und WLAN-Chip. Flachbandkabel vorsichtig abziehen.',
         marks=[mark('box', 30, 40, 24, 24, 1, CHIP), mark('box', 62, 40, 14, 14, 1, CHIP), mark('box', 80, 4, 22, 14, 1, '#B7BCC0')]),
    teil('netzteil', 'circuit_board', 'Netzteilplatine', 'Netzteil', 'box',
         x=300, y=262, w=110, d=85, z=12, h=1.6, r=2, mass=140,
         materials=[['fr4', 35], ['kupfer', 25], ['ferrit', 15], ['alu', 10], ['chip', 10], ['elektrolyt', 5]], color=PCB,
         info='Eingebautes Netzteil mit Trafo und Kondensatoren. Auch ausgesteckt nicht an die Lötstellen fassen.',
         marks=[mark('box', 10, 10, 30, 26, 2, '#C5803D'), mark('cyl', 60, 14, 18, fill='#2F4F7A')]),
    teil('tintenvlies', 'ink_cartridge', 'Tintenauffangvlies', 'Tintenvlies', 'box', material_id='pu_foam',
         x=30, y=30, w=100, d=120, z=10, h=12, r=3, mass=80, materials=[['schaum', 80], ['druck', 20]], color='#3B3550',
         info='Saugt die Tinte auf, die beim Reinigen der Düsen verspritzt. Ist es voll, meldet der Drucker einen Fehler. Nass und färbend: in eine Tüte packen.'),
    teil('ausgabefach', 'plastic_housing', 'Papierausgabefach', 'Ausgabefach', 'box',
         x=90, y=320, w=250, d=70, z=20, h=8, r=3, explode=[0, 90, 0], mass=180, color='#D5D8DB', sortBias=25,
         info='Ausziehbares Fach, das die bedruckten Blätter auffängt. Steckt in Führungen und lässt sich herausziehen.',
         marks=[mark('box', 100, 52, 50, 8, 3, '#C2C6CA'), mark('box', 6, 42, 238, 2, 1, '#C2C6CA')]),
    teil('unterschale', 'plastic_housing', 'Unterschale mit Chassis', 'Unterschale', 'box',
         x=0, y=0, w=430, d=360, z=0, h=40, r=8, mass=1600, materials=[['pcabs', 75], ['stahl', 25]], color='#CDD1D4', wand=3,
         info='Kunststoffwanne mit eingelegtem Stahlblech als Rahmen. Trägt alle Teile; zuletzt Stahl und Kunststoff trennen.',
         marks=[dict(m, zeichnung=True) for m in raster(15, 15, 2, 2, 20, 20, 380, 310, shape='cyl', fill='#9AA2A8')]),
    teil('kabel', 'cable_insulation', 'Netzkabel (Isolierung)', 'Kabel', 'box',
         x=260, y=340, w=150, d=10, z=0, h=8, r=4, explode=[200, 60, 0], mass=110, materials=[['pvc', 90], ['pp', 10]],
         color=DUNKEL, info='1,5 m Netzkabel mit PVC-Mantel. Stecker abschneiden und längs aufschlitzen.',
         marks=[mark('box', 0, 0, 25, 10, 2, '#4A5156')]),
    teil('kupferadern', 'cable_copper_core', 'Kupferadern', 'Kupferadern', 'box',
         x=260, y=322, w=150, d=4, z=0, h=4, r=1, explode=[200, 60, 0], mass=45, color='#B87333',
         info='Zwei Kupferadern im Kabel. Reines Kupfer lohnt sich beim Schrotthändler.'),
]

explodiere(teile, abstand=60, nach_liste=True,
           abstaende={'patrone_schwarz': 20, 'patrone_farbe': 20, 'zahnriemen': 15, 'encoder': 15, 'druckkopf': 15})
# Foto-Ansicht: echte Formen (Kabel liegend, Spulen als Ring); Details darauf nur in der Zeichnung
FORMEN = {'kabel': ('liegend_x', 1), 'kupferadern': ('liegend_x', 1), 'walze': ('liegend_x', 1)}
for p in teile:
    if p['id'] in FORMEN:
        p['form'], nur_zeichnung = FORMEN[p['id']]
        p.pop('wand', None)
        p.pop('boden', None)
        for m in (p.get('marks') or []) if nur_zeichnung else []:
            m['zeichnung'] = True
skaliere_masse(teile, oid='inkjet_printer')
schreibe('inkjet_printer', teile)
