"""3D-Modell: board_game. Erzeugt tools/kategorien/modelle/board_game.json.

Familien-Brettspiel in quadratischer Stülpdeckelschachtel 270 × 270 × 60 mm. Innen ein Papp-Einsatz mit Fächern
für zwei Kartenstapel, vier Holzfiguren und zwei Holzwürfel, darüber der einmal geviertelte Spielplan
(520 × 520 mm, gefaltet 260 × 260 × 8 mm) und die Spielanleitung.
Explosion: Deckel nach hinten abgenommen (dy negativ, auf dem Tisch). Im Unterteil werden Einsatz, Spielmaterial,
Spielplan und Anleitung nach oben abgehoben.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

PAPPE = '#3E6FA8'
GRAU = '#B9A98C'
KARTON_DRUCK = [['papier', 95], ['druck', 5]]
FIGUR = ('#C8423A', '#2F8F5B', '#E2B33C', '#3E6FA8')

teile = [
    teil('deckel', 'cardboard_box_body', 'Schachteldeckel', 'Deckel', 'box',
         x=0, y=0, w=270, d=270, z=3, h=57, r=1, mass=135, materials=KARTON_DRUCK, color=PAPPE,
         info='Graupappe mit bedrucktem Papier kaschiert, an den Ecken verklebt. Er wird über das Unterteil gestülpt. '
              'Leer und flach gedrückt kommt er ins Altpapier.',
         marks=[mark('box', 20, 20, 230, 150, 4, '#E2B33C'), mark('cyl', 85, 40, 100, 100, fill='#C8423A'),
                mark('box', 30, 190, 210, 24, 3, '#F2E6C8'), mark('box', 60, 228, 150, 12, 3, '#F2E6C8')]),
    teil('anleitung', 'paper_sheets', 'Spielanleitung', 'Anleitung', 'box',
         x=30, y=20, w=210, d=230, z=53, h=1, r=0.5, mass=20, materials=[['papier', 92], ['druck', 8]], color='#F4F2EE',
         info='Gefaltetes Heft aus Papier. Ins Altpapier, oder besser im Spiel lassen, sonst ist es unvollständig.',
         marks=[mark('box', 15, 15, 180, 20, 2, '#C8423A')] + raster(15, 50, 1, 9, 180, 6, 0, 18, fill='#5B6166')),
    teil('spielplan', 'game_board', 'Spielplan (gefaltet)', 'Spielplan', 'box',
         x=5, y=5, w=260, d=260, z=45, h=8, r=1, mass=320, materials=KARTON_DRUCK, color='#7FB069',
         info='Vier Felder aus Graupappe, mit Papier kaschiert und mit Gewebestreifen gefaltet. Ins Altpapier; '
              'Plan mit Folienbeschichtung in den Restmüll.',
         marks=[mark('box', 0, 129, 260, 2, 0, '#5E8A4D'), mark('box', 129, 0, 2, 260, 0, '#5E8A4D')]
         + raster(16, 16, 10, 1, 18, 18, 23.5, fill='#F2E6C8') + raster(16, 226, 10, 1, 18, 18, 23.5, fill='#F2E6C8')
         + raster(16, 39, 1, 8, 18, 18, 0, 23.5, fill='#F2E6C8') + raster(226, 39, 1, 8, 18, 18, 0, 23.5, fill='#F2E6C8')),
    teil('karten_1', 'paper_sheets', 'Ereigniskarten', 'Karten', 'box', material_id='cardboard',
         x=22, y=25, w=58, d=88, z=27, h=18, r=3, mass=100, materials=KARTON_DRUCK, color='#E9E4D8',
         info='Rund 60 Karten aus bedrucktem Karton. Unbeschichtet ins Altpapier, beschichtet in den Restmüll.',
         marks=[mark('box', 4, 4, 50, 80, 2, '#C8423A'), mark('cyl', 17, 32, 24, fill='#F2E6C8')]),
    teil('karten_2', 'paper_sheets', 'Fragekarten', 'Karten', 'box', material_id='cardboard', label=False,
         x=22, y=150, w=58, d=88, z=27, h=18, r=3, mass=100, materials=KARTON_DRUCK, color='#E9E4D8',
         info='Zweiter Kartenstapel.',
         marks=[mark('box', 4, 4, 50, 80, 2, '#3E6FA8'), mark('cyl', 17, 32, 24, fill='#F2E6C8')]),
]
for n, f in enumerate(FIGUR):
    teile.append(teil(f'figur_{n + 1}', 'wooden_pieces', 'Spielfiguren (4 Stück)' if n == 0 else f'Spielfigur {n + 1}',
                      'Figuren', 'cyl', x=110 + 26 * n, y=40, w=16, z=20, h=25, mass=4, color=f,
                      materials=[['holz', 98], ['druck', 2]], label=None if n == 0 else False,
                      info='Gedrechseltes, farbig lackiertes Buchenholz. Als Ersatzfiguren für andere Spiele aufheben.'
                      if n == 0 else 'Weitere Figur.',
                      marks=[mark('cyl', 3, 3, 10, fill='#FFFFFF')]))
for n in range(2):
    teile.append(teil(f'wuerfel_{n + 1}', 'wooden_pieces', 'Würfel (2 Stück)' if n == 0 else 'Würfel 2', 'Würfel', 'box',
                      x=120 + 40 * n, y=150, w=16, d=16, z=29, h=16, r=2, mass=3, color='#F2E6C8',
                      materials=[['holz', 97], ['druck', 3]], label=None if n == 0 else False,
                      info='Holzwürfel mit eingeprägten, gefärbten Augen. Gehören zu den Ersatzteilen, nicht in den Müll.'
                      if n == 0 else 'Zweiter Würfel.',
                      marks=[mark('cyl', 3, 3, 3, fill='#22272B'), mark('cyl', 6.5, 6.5, 3, fill='#22272B'),
                             mark('cyl', 10, 10, 3, fill='#22272B')]))
teile += [
    teil('einsatz', 'cardboard_box_body', 'Einsatz mit Fächern', 'Einsatz', 'box',
         x=4, y=4, w=262, d=262, z=1, h=44, r=1, mass=60, materials=[['papier', 100]], color=GRAU,
         info='Gefalteter Karton, der das Spielmaterial in Fächern ordnet. Ins Altpapier; Einsätze aus Kunststoff '
              'gehören in den Restmüll.',
         marks=[mark('box', 14, 17, 66, 96, 2, '#9E8E72'), mark('box', 14, 142, 66, 96, 2, '#9E8E72'),
                mark('box', 98, 30, 120, 36, 2, '#9E8E72'), mark('box', 108, 140, 70, 36, 2, '#9E8E72')]),
    teil('unterteil', 'cardboard_box_body', 'Schachtelunterteil', 'Unterteil', 'box',
         x=2, y=2, w=266, d=266, z=0, h=56, r=1, mass=130, materials=KARTON_DRUCK, color='#E6E1D6',
         info='Gleicher Aufbau wie der Deckel, innen oft weiß. Flach drücken und ins Altpapier.',
         marks=[mark('box', 2, 2, 262, 262, 1, '#CFC8B8')]),
]

by = {p['id']: p for p in teile}
by['deckel']['explode'] = [0, -(270 + 40), -3]
unten = [p for p in teile if p['id'] != 'deckel']
klein = {p['id']: 30 for p in unten if p['id'].startswith(('figur', 'wuerfel', 'karten'))}
explodiere(unten, abstand=70, abstaende=klein)
skaliere_masse(teile, oid='board_game')
schreibe('board_game', teile)
