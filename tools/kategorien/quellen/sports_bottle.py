"""3D-Modell: sports_bottle. Erzeugt tools/kategorien/modelle/sports_bottle.json.

Typische 750-ml-Sporttrinkflasche zum Quetschen: LDPE-Körper Ø 70 mm mit Griffmulde (Taille), Schraubdeckel aus PP
mit Push-Pull-Mundstück, Silikon-Dichtring und durchsichtiger Staubschutzkappe. Höhe 250 mm, ca. 100 g.
Körperabschnitte bewegen sich gemeinsam, die Verschlussteile stapeln über dem Hals.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

KOERPER, KOERPER_D = '#3E8FC9', '#2F78AD'
DECKEL, DECKEL_D = '#2B2F33', '#1C1F22'
teile = [
    teil('schutzkappe', 'pp_flip_cap', 'Staubschutzkappe', 'Schutzkappe', 'cyl',
         x=20, y=20, w=30, z=226, h=24, mass=3, materials=[['pp', 100]], color='#D9E4EA', opacity=0.6,
         info='Durchsichtige Kappe über dem Mundstück, damit kein Schmutz an den Trinkbereich kommt. Nur aufgesteckt.',
         marks=[mark('cyl', 5, 5, 20, fill='#C3D1D8')]),
    teil('mundstueck', 'pp_flip_cap', 'Push-Pull-Mundstück', 'Mundstück', 'cyl',
         material_id='ldpe', x=24, y=24, w=22, z=222, h=16, mass=4, materials=[['ldpe', 100]], color='#ECEDEE',
         info='Weiches Ventil zum Herausziehen mit den Zähnen. Es ist nur aufgeschnappt und lässt sich zum Reinigen '
              'mit etwas Kraft abziehen.',
         marks=[mark('cyl', 6, 6, 10, fill='#BFC3C6'), mark('cyl', 9, 9, 4, fill='#3A3F44')]),
    teil('deckel_kuppe', 'pp_flip_cap', 'Deckelkuppe', 'Deckel', 'cyl',
         x=15, y=15, w=40, z=220, h=6, mass=4, color=DECKEL, label=False,
         info='Abgeschrägte Oberseite des Deckels, in der das Mundstück steckt.',
         marks=[mark('cyl', 6, 6, 28, fill=DECKEL_D)]),
    teil('deckel', 'pp_flip_cap', 'Schraubdeckel', 'Deckel', 'cyl',
         x=11, y=11, w=48, z=205, h=15, mass=12, color=DECKEL,
         info='Schraubdeckel aus PP mit Griffrippen. Abschrauben, Mundstück abziehen: Beides ist PP bzw. PE.',
         marks=[mark('box', 22.5, 0.5, 3, 4, 1, '#43484E'), mark('box', 22.5, 43.5, 3, 4, 1, '#43484E'),
                mark('box', 0.5, 22.5, 4, 3, 1, '#43484E'), mark('box', 43.5, 22.5, 4, 3, 1, '#43484E'),
                mark('box', 7, 7, 3, 3, 1, '#43484E'), mark('box', 38, 7, 3, 3, 1, '#43484E'),
                mark('box', 7, 38, 3, 3, 1, '#43484E'), mark('box', 38, 38, 3, 3, 1, '#43484E')]),
    teil('dichtring', 'pp_flip_cap', 'Dichtring', 'Dichtring', 'cyl',
         material_id='silicone', x=16, y=16, w=38, z=212, h=3, mass=1, materials=[['gummi', 100]], color='#E8E4DA',
         info='Silikonring im Deckel, der den Hals abdichtet. Mit einem Fingernagel herausziehen und gut abspülen.',
         marks=[mark('cyl', 4, 4, 30, fill='#8A8F94')]),
    teil('hals', 'ldpe_squeeze_body', 'Flaschenhals mit Gewinde', 'Hals', 'cyl',
         x=15, y=15, w=40, z=198, h=16, mass=4, color=KOERPER,
         info='Breites Gewinde, damit Eiswürfel hineinpassen.', marks=[mark('cyl', 4, 4, 32, fill=KOERPER_D)]),
] + [
    teil(f'schulter_{i}', 'ldpe_squeeze_body', 'Flaschenschulter', 'Schulter', 'cyl',
         x=(70 - w) / 2, y=(70 - w) / 2, w=w, z=z, h=h, mass=m, color=KOERPER, label=False,
         info='Gerundeter Übergang vom Körper zum Hals.')
    for i, (w, z, h, m) in enumerate(((48, 194, 4, 1), (58, 188, 6, 2), (66, 180, 8, 3)))
] + [
    teil('rumpf_oben', 'ldpe_squeeze_body', 'Flaschenkörper oben', 'Körper oben', 'cyl',
         x=0, y=0, w=70, z=142, h=38, mass=16, color=KOERPER, label=False,
         info='Oberer Teil des Flaschenkörpers.'),
    teil('taille_oben', 'ldpe_squeeze_body', 'Griffmulde', 'Griffmulde', 'cyl',
         x=2, y=2, w=66, z=134, h=8, mass=3, color=KOERPER, label=False,
         info='Übergang zur Griffmulde.'),
    teil('taille', 'ldpe_squeeze_body', 'Griffmulde', 'Griffmulde', 'cyl',
         x=4.5, y=4.5, w=61, z=104, h=30, mass=10, color=KOERPER, label=False,
         info='Schmalere Taille, damit die Flasche gut in der Hand liegt.',
         marks=[mark('cyl', 3, 3, 55, fill=KOERPER_D)]),
    teil('taille_unten', 'ldpe_squeeze_body', 'Griffmulde', 'Griffmulde', 'cyl',
         x=2, y=2, w=66, z=96, h=8, mass=3, color=KOERPER, label=False,
         info='Übergang von der Griffmulde zum Körper.'),
    teil('rumpf', 'ldpe_squeeze_body', 'Flaschenkörper aus LDPE', 'Flasche', 'cyl',
         x=0, y=0, w=70, z=6, h=90, mass=26, color=KOERPER,
         info='Weiches LDPE, das man zum Trinken zusammendrückt. Lange weiterverwenden. Kaputt gehört sie in den '
              'Restmüll, denn eine Trinkflasche ist keine Verpackung.'),
    teil('boden', 'ldpe_squeeze_body', 'Flaschenboden', 'Boden', 'cyl',
         x=3, y=3, w=64, z=0, h=6, mass=5, color=KOERPER, label=False,
         info='Standboden mit Recyclingzeichen 4 für LDPE.'),
]
koerper = [p['id'] for p in teile if p['component_id'] == 'ldpe_squeeze_body']
explodiere(teile, abstand=22, nach_liste=True, gruppen=[koerper, ['deckel', 'deckel_kuppe']])
skaliere_masse(teile, oid='sports_bottle')
schreibe('sports_bottle', teile)
