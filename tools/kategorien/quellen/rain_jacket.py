"""3D-Modell: rain_jacket. Erzeugt tools/kategorien/modelle/rain_jacket.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Leichte Regenjacke flach hingelegt, Vorderseite oben, Kragen mit eingerollter Kapuze hinten (y = 0).
# 300 × 400 × 30 mm: Rumpf 180 mm breit in der Mitte, Ärmel links und rechts daneben, Klettriegel am Handgelenk.
# Explodiert: Ärmel zur Seite, vom Rückenteil heben sich Vorderteile, Reißverschluss, Abdeckleiste und Kapuze ab.
GELB = '#E8B83A'
NAHT = '#C99A22'
KLETT = '#2A2E31'
STOFF = [['polyester', 85], ['tpu', 15]]
RV = [['messing', 45], ['polyester', 50], ['stahl', 5]]


def aermel(seite, x, dx, dy):
    links = seite == 'l'
    return [
        teil(f'klett_{seite}', 'coated_polyester_fabric', 'Klettriegel am Ärmel', 'Klettriegel', 'box',
             material_id='nylon', x=x + 10, y=338, w=40, d=18, z=20, h=2, r=4, mass=3,
             materials=[['nylon', 100]], color=KLETT, explode=[dx, dy, 20], label=links,
             info='Klettverschluss aus Polyamid: Haken- und Flauschband. Damit wird der Ärmel am Handgelenk enger '
                  'gestellt. Vor dem Recycling abschneiden.' if links else 'Zweiter Klettriegel.',
             marks=raster(4, 4, 6, 1, 3, 10, 6, fill='#3A3F44')),
        teil(f'aermel_{seite}', 'coated_polyester_fabric', f'Ärmel {"links" if links else "rechts"}', 'Ärmel', 'box',
             x=x, y=50, w=60, d=320, z=0, h=20, r=12, mass=55, materials=STOFF, color=GELB, explode=[dx, dy, 0],
             label=links,
             info='Ärmel aus beschichtetem Polyester, am Handgelenk mit Gummizug. Die Naht zum Rumpf ist innen '
                  'mit Nahtband abgedichtet.' if links else 'Gegenstück zum linken Ärmel.',
             marks=[mark('box', 0, 290, 60, 3, 0, NAHT), mark('box', 4, 296, 52, 20, 4, NAHT)]),
    ]


teile = [
    teil('kordelstopper', 'coated_polyester_fabric', 'Kordelstopper der Kapuze', 'Kordelstopper', 'cyl',
         material_id='pp', x=86, y=13, w=10, d=14, z=24, h=5, mass=1.5, materials=[['pp', 80], ['stahl', 20]],
         color='#22272B',
         info='Kunststoffklemme mit Stahlfeder für den Kapuzenzug. Vor dem Recycling abschneiden.',
         marks=[mark('cyl', 2.5, 4, 5, fill='#555C62')]),
    teil('kapuze', 'coated_polyester_fabric', 'Kapuze, im Kragen eingerollt', 'Kapuze', 'box', form='liegend_x',
         x=95, y=2, w=110, d=36, z=12, h=18, r=14, mass=30, materials=STOFF, color=GELB,
         info='Die Kapuze steckt eingerollt im Kragen und wird bei Regen herausgezogen. Mit Kordelzug am Gesicht.',
         marks=[mark('box', 6, 17, 98, 2, 1, NAHT, zeichnung=True), mark('box', 70, 8, 28, 8, 3, '#D6A82E', zeichnung=True)]),
    teil('leiste', 'coated_polyester_fabric', 'Abdeckleiste mit Druckknöpfen', 'Abdeckleiste', 'box',
         x=139, y=40, w=24, d=360, z=23.5, h=2.5, r=2, mass=12, materials=[['polyester', 80], ['tpu', 10], ['stahl', 10]],
         color=GELB,
         info='Stoffleiste über dem Reißverschluss, die den Regen abhält. Mit Druckknöpfen aus Metall geschlossen.',
         marks=[mark('box', 2, 0, 1.5, 360, 0, NAHT)]
         + [mark('cyl', 7, y, 10, fill='#B7BCC0') for y in (30, 110, 190, 270, 340)]),
    teil('reissverschluss', 'metal_zipper', 'Reißverschluss', 'Reißverschluss', 'box',
         x=143, y=40, w=14, d=360, z=21.5, h=2, r=1, mass=22, materials=RV, color='#2A2E31',
         info='Metallreißverschluss unter der Abdeckleiste. Seitlich am Band abschneiden: Metall gehört nicht ins '
              'Textilrecycling.',
         marks=[mark('box', 5, 0, 4, 360, 0.5, '#B7BCC0'), mark('box', 3, 24, 8, 14, 2, '#B7BCC0')]),
    teil('vorne_l', 'coated_polyester_fabric', 'Vorderteil links', 'Vorderteil', 'box',
         x=60, y=30, w=90, d=370, z=10, h=11.5, r=6, mass=40, materials=STOFF, color=GELB,
         info='Polyestergewebe mit einer wasserdichten Polyurethan-Beschichtung innen. Die Beschichtung lässt sich nicht '
              'ablösen: Stoff lieber für Taschen oder Beutel weiterverwenden.',
         marks=[mark('box', 15, 230, 55, 22, 3, NAHT), mark('box', 15, 230, 55, 3, 1, '#B88A1E'),
                mark('box', 0, 360, 90, 3, 0, NAHT)]),
    teil('vorne_r', 'coated_polyester_fabric', 'Vorderteil rechts', 'Vorderteil', 'box',
         x=150, y=30, w=90, d=370, z=10, h=11.5, r=6, mass=40, materials=STOFF, color=GELB, label=False,
         info='Gegenstück zur linken Vorderseite, mit Tasche hinter einer Regenklappe.',
         marks=[mark('box', 20, 230, 55, 22, 3, NAHT), mark('box', 20, 230, 55, 3, 1, '#B88A1E'),
                mark('box', 0, 360, 90, 3, 0, NAHT)]),
    teil('etikett', 'care_label', 'Pflegeetikett', 'Etikett', 'box',
         x=135, y=30, w=25, d=32, z=9.7, h=0.3, r=1, mass=1, explode=[0, -110, 0], color='#F4F2EE',
         info='Etikett mit Waschsymbolen: nicht in den Trockner, sonst leidet die Beschichtung. Abschneiden vor dem Recycling.',
         marks=[mark('box', 4, 5, 17, 3, 0, '#8E969A'), mark('box', 4, 12, 17, 3, 0, '#8E969A')]),
    teil('ruecken', 'coated_polyester_fabric', 'Rückenteil mit Nahtband', 'Rückenteil', 'box',
         x=60, y=20, w=180, d=380, z=0, h=9.7, r=6, mass=90, materials=STOFF, color=GELB,
         info='Alle Nähte sind innen mit einem aufgeschweißten Kunststoffband (TPU) abgedichtet, damit kein Wasser '
              'durch die Stiche dringt.',
         marks=[mark('box', 0, 90, 180, 6, 0, '#EDE6CF'), mark('box', 2, 0, 6, 380, 0, '#EDE6CF'),
                mark('box', 172, 0, 6, 380, 0, '#EDE6CF'), mark('box', 0, 368, 180, 3, 0, NAHT)]),
] + aermel('l', 0, -120, 170) + aermel('r', 240, 120, 0)

explodiere(teile, abstand=55, nach_liste=True, abstaende={'kordelstopper': 20, 'reissverschluss': 30, 'leiste': 30})
skaliere_masse(teile, oid='rain_jacket')
schreibe('rain_jacket', teile)
