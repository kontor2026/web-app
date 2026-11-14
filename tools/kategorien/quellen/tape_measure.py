"""3D-Modell: tape_measure. Erzeugt tools/kategorien/modelle/tape_measure.json.

Maßband 3 m × 19 mm, auf der Seite liegend (Achse senkrecht, z). Bandaustritt vorn (y groß) unten links, Feststeller
oben rechts (x groß), Gürtelclip hinten (y 0). Im Gehäuse: Trommel auf der Achse, darin die Rückholfeder, darum das
aufgewickelte Stahlband. Explodiert: Ebenen nach oben (Unterschale unten), Haken, Clip und Feststeller seitlich.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

GEH = '#F2C230'
GUMMI = '#2E3236'
BAND = '#F4D24A'

teile = [
    teil('schraube', 'plastic_housing', 'Gehäuseschraube', 'Schraube', 'cyl',
         material_id='steel', x=28, y=29, w=5, z=27.5, h=2, mass=0.6, materials=[['stahl', 100]],
         info='Hält beide Gehäusehälften zusammen. Vorsicht: Beim Öffnen kann die Feder herausspringen.',
         color='#9AA2A6', marks=[mark('box', 0.5, 2, 4, 1, fill='#5A6268')]),
    teil('deckel', 'plastic_housing', 'Gehäusehälfte oben', 'Gehäuse oben', 'box',
         x=0, y=2, w=60, d=60, z=15, h=15, r=16, mass=24, materials=[['pcabs', 80], ['tpe', 20]],
         info='ABS mit gummierter Griffzone. Schraube lösen, dann die Hälften vorsichtig auseinanderziehen.',
         color=GEH, sortBias=4,
         marks=[mark('box', 4, 4, 52, 52, 14, GUMMI), mark('cyl', 14, 13, 32, fill=GEH),
                mark('cyl', 17, 16, 26, fill='#F6F2E6'), mark('box', 21, 22, 18, 4, 1, '#C8322B'),
                mark('box', 22, 29, 16, 2.5, 1, '#3A3F44'), mark('box', 24, 33, 12, 2, 1, '#8A8F94'),
                mark('box', 52, 22, 4, 16, 2, '#4A4F55')]),
    teil('band', 'steel_tape', 'Stahlmaßband (3 m)', 'Maßband', 'cyl',
         x=6, y=8, w=48, z=5, h=19, mass=55, materials=[['stahl', 93], ['druck', 7]],
         info='Gewölbtes, lackiertes Federstahlband mit aufgedruckter Skala. Das Band ist scharfkantig: '
              'Handschuhe tragen, es gehört zum Altmetall.',
         color=BAND, wand=10, boden=0,
         marks=[mark('cyl', 2, 2, 44, fill='#E6C23C', zeichnung=True), mark('cyl', 10, 10, 28, fill='#2B2B2B', zeichnung=True)]),
    teil('feder', 'steel_spring', 'Rückholfeder (Spiralfeder)', 'Feder', 'cyl',
         x=17, y=20, w=26, z=7, h=15, mass=18,
         info='Aufgewickeltes Federstahlband, das das Maßband zurückzieht. Steht unter Spannung und kann '
              'herausschnellen. Mit einer Zange herausziehen, Schutzbrille tragen.',
         color='#3C4247', marks=[mark('cyl', 3, 3, 20, fill='#596168'), mark('cyl', 7, 7, 12, fill='#3C4247'),
                                  mark('cyl', 10, 10, 6, fill='#596168')]),
    teil('trommel', 'plastic_housing', 'Trommel mit Achse', 'Trommel', 'cyl',
         x=16, y=19, w=28, z=4, h=22, mass=5,
         info='Kunststoffspule, auf die das Band gewickelt ist. Innen ist die Feder an der Achse eingehängt.',
         color='#D9D4C8', marks=[mark('cyl', 9, 9, 10, fill='#B3AE9F')]),
    teil('unterschale', 'plastic_housing', 'Gehäusehälfte unten', 'Gehäuse unten', 'box',
         x=0, y=2, w=60, d=60, z=0, h=15, r=16, mass=24, materials=[['pcabs', 80], ['tpe', 20]],
         info='Hier sitzen Achse und Bandführung. Sortenrein bleibt das Gehäuse nur ohne Band und Feder.',
         color=GEH, sortBias=12,
         marks=[mark('box', 3, 3, 54, 54, 14, '#E2B024'), mark('cyl', 14, 14, 32, fill='#C99C1C'),
                mark('box', 4, 50, 14, 8, 2, '#B98F18')]),
    teil('bremsklotz', 'plastic_housing', 'Bremsklotz', 'Bremsklotz', 'box',
         x=46, y=44, w=8, d=12, z=6, h=8, r=1.5, explode=[42, 0, 0], mass=1, materials=[['pcabs', 70], ['tpe', 30]],
         info='Kleiner Klotz unter dem Feststeller, der das Band gegen das Gehäuse drückt. Fällt beim Öffnen leicht heraus.',
         color='#3A3F44', marks=[mark('box', 1, 2, 6, 8, 1, '#55595E')]),
    teil('feststeller', 'plastic_housing', 'Feststeller', 'Feststeller', 'box',
         x=60, y=38, w=4, d=20, z=10, h=10, r=1.5, explode=[22, 0, 0], sortBias=16, mass=4, materials=[['pcabs', 100]],
         info='Schieber, der das Band mit einem Bremsklotz festklemmt. Drückt man ihn, bleibt das Band draußen.',
         color='#C8322B'),
    teil('haken', 'steel_tape', 'Endhaken', 'Haken', 'box',
         x=1, y=62, w=10, d=3, z=4, h=22, r=0.5, explode=[0, 26, 0], mass=3,
         materials=[['stahl', 90], ['messing', 10]],
         info='Vernieteter Stahlhaken am Bandanfang. Er sitzt bewusst locker, damit innen und außen richtig gemessen wird.',
         color='#8C949A'),
    teil('clip', 'plastic_housing', 'Gürtelclip', 'Clip', 'box',
         material_id='steel', x=12, y=0, w=36, d=2, z=6, h=18, r=1, explode=[0, -26, 0], mass=8,
         materials=[['stahl', 100]],
         info='Federstahlclip, an der Rückseite angeschraubt. Abschrauben und zum Altmetall geben.',
         color='#B5BCC1'),
]

explodiere(teile, abstand=20, nach_liste=True)
skaliere_masse(teile, oid='tape_measure')
schreibe('tape_measure', teile)
