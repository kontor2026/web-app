"""3D-Modell: rain_jacket. Erzeugt tools/kategorien/modelle/rain_jacket.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, explodiere, skaliere_masse, schreibe  # noqa: E402

# Leichte Regenjacke gefaltet, Vorderseite oben, Kragen mit eingerollter Kapuze hinten (y = 0). 300 × 400 × 30 mm.
# Explodiert heben sich Kapuze, Vorderteile und Reißverschluss vom Rückenteil ab, die eingeschlagenen Ärmel
# werden zur Seite gezogen.
GELB = '#E8B83A'
NAHT = '#C99A22'
STOFF = [['polyester', 85], ['tpu', 15]]

teile = [
    teil('kordelstopper', 'coated_polyester_fabric', 'Kordelstopper der Kapuze', 'Kordelstopper', 'cyl',
         material_id='pp', x=60, y=12, w=10, d=14, z=30, h=5, mass=1.5, materials=[['pp', 80], ['stahl', 20]],
         color='#22272B',
         info='Kunststoffklemme mit Stahlfeder für den Kapuzenzug. Vor dem Recycling abschneiden.',
         marks=[mark('cyl', 2.5, 4, 5, fill='#555C62')]),
    teil('kapuze', 'coated_polyester_fabric', 'Kapuze, im Kragen eingerollt', 'Kapuze', 'box',
         x=75, y=0, w=150, d=45, z=20, h=10, r=12, mass=35, materials=STOFF, color=GELB,
         info='Die Kapuze steckt eingerollt im Kragen und wird bei Regen herausgezogen. Mit Gummizug am Gesicht.',
         marks=[mark('box', 6, 20, 138, 2, 1, NAHT)]),
    teil('reissverschluss', 'metal_zipper', 'Reißverschluss mit Abdeckleiste', 'Reißverschluss', 'box',
         x=143, y=40, w=14, d=360, z=24, h=3, r=1, mass=25, materials=[['messing', 45], ['polyester', 50], ['stahl', 5]],
         color='#2A2E31',
         info='Metallreißverschluss unter einer Stoffleiste, die den Regen abhält. Seitlich am Band abschneiden.',
         marks=[mark('box', 5, 0, 4, 360, 0.5, '#B7BCC0'), mark('box', 3, 20, 8, 14, 2, '#B7BCC0')]),
    teil('vorne_l', 'coated_polyester_fabric', 'Vorderteil links', 'Vorderteil', 'box',
         x=0, y=40, w=143, d=360, z=17, h=7, r=6, mass=45, materials=STOFF, color=GELB,
         info='Polyestergewebe mit einer wasserdichten Polyurethan-Beschichtung innen. Die Beschichtung lässt sich nicht '
              'ablösen: Stoff lieber für Taschen oder Beutel weiterverwenden.',
         marks=[mark('box', 25, 230, 80, 5, 2, NAHT), mark('box', 0, 352, 143, 3, 0, NAHT)]),
    teil('vorne_r', 'coated_polyester_fabric', 'Vorderteil rechts', 'Vorderteil', 'box',
         x=157, y=40, w=143, d=360, z=17, h=7, r=6, mass=45, materials=STOFF, color=GELB, label=False,
         info='Gegenstück zur linken Vorderseite, mit Tasche hinter einer Regenklappe.',
         marks=[mark('box', 38, 230, 80, 5, 2, NAHT), mark('box', 0, 352, 143, 3, 0, NAHT)]),
    teil('etikett', 'care_label', 'Pflegeetikett', 'Etikett', 'box',
         x=200, y=10, w=25, d=32, z=16.7, h=0.3, r=1, mass=1, explode=[130, -70, 0], color='#F4F2EE',
         info='Etikett mit Waschsymbolen: nicht in den Trockner, sonst leidet die Beschichtung. Abschneiden vor dem Recycling.',
         marks=[mark('box', 4, 5, 17, 3, 0, '#8E969A'), mark('box', 4, 12, 17, 3, 0, '#8E969A')]),
    teil('ruecken', 'coated_polyester_fabric', 'Rückenteil mit Nahtband', 'Rückenteil', 'box',
         x=0, y=0, w=300, d=400, z=8, h=9, r=6, mass=100, materials=STOFF, color=GELB,
         info='Alle Nähte sind innen mit einem aufgeschweißten Kunststoffband abgedichtet, damit kein Wasser durch die Stiche dringt.',
         marks=[mark('box', 0, 120, 300, 8, 0, NAHT), mark('box', 0, 392, 300, 3, 0, NAHT)]),
    teil('aermel_l', 'coated_polyester_fabric', 'Ärmel links (eingeschlagen)', 'Ärmel', 'box',
         x=15, y=30, w=125, d=350, z=0, h=8, r=10, mass=60, materials=STOFF, color=GELB, explode=[-190, 0, 0],
         info='Ärmel mit Klettriegel am Handgelenk, beim Falten unter den Rücken geschlagen.',
         marks=[mark('box', 20, 320, 85, 22, 3, NAHT)]),
    teil('aermel_r', 'coated_polyester_fabric', 'Ärmel rechts (eingeschlagen)', 'Ärmel', 'box',
         x=160, y=30, w=125, d=350, z=0, h=8, r=10, mass=60, materials=STOFF, color=GELB, explode=[190, 0, 0],
         label=False, info='Gegenstück zum linken Ärmel.', marks=[mark('box', 20, 320, 85, 22, 3, NAHT)]),
]

explodiere(teile, abstand=80, nach_liste=True, abstaende={'kordelstopper': 25})
skaliere_masse(teile, oid='rain_jacket')
schreibe('rain_jacket', teile)
