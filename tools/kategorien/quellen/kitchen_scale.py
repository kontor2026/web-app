"""3D-Modell: kitchen_scale. Erzeugt tools/kategorien/modelle/kitchen_scale.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Typische flache digitale Küchenwaage mit Glasplatte, 150 × 200 × 20 mm. Display vorne (y groß) unter dem Glas.
# Vier Wägezellen in den Ecken tragen die Glasplatte und stehen auf den Füßen. Zwei Knopfzellen CR2032 im
# Batteriefach im Boden; Fach und Zellen werden nach rechts herausgezogen.
GEH = '#2E3338'
CHIP = '#3F4547'
ZELLE_INFO = ('Biegebalken aus Aluminium mit aufgeklebten Dehnungsmessstreifen. Wird er durch das Gewicht ein winziges Stück '
              'gebogen, ändert sich der elektrische Widerstand. Abschrauben, die dünnen Drähte abknipsen.')


def waegezelle(i, x, y):
    return teil(f'waegezelle_{i}', 'load_cell', f'Wägezelle {i}', 'Wägezellen' if i == 1 else f'Wägezelle {i}', 'box',
                x=x, y=y, w=34, d=34, z=3, h=8, r=3, mass=12, materials=[['alu', 95], ['kupfer', 3], ['folien', 2]],
                color='#C9CED2', label=None if i == 1 else False,
                info=ZELLE_INFO if i == 1 else 'Gleich gebaut wie Wägezelle 1. Zusammen messen die vier Zellen das Gesamtgewicht.',
                marks=[mark('box', 4, 12, 26, 10, 1, '#AEB4B8'), mark('box', 12, 14, 10, 6, 0.5, '#C5803D'),
                       mark('cyl', 3, 3, 5, fill='#5E656A')])


teile = [
    teil('glasplatte', 'glass_platform', 'Glasplatte (Sicherheitsglas)', 'Glasplatte', 'box',
         x=0, y=0, w=150, d=200, z=15, h=4.5, r=10, mass=320, color='#C9DEDF', opacity=0.65,
         info='Gehärtetes Glas, auf die Wägezellen geklebt oder geschraubt. Zerspringt bei einem Schlag auf die Kante in viele Krümel.',
         marks=[mark('box', 45, 164, 60, 30, 3, '#1E2226'), mark('cyl', 24, 174, 10, fill='#3A3F44'),
                mark('cyl', 116, 174, 10, fill='#3A3F44')]),
    teil('lcd', 'lcd_panel', 'Flüssigkristall-Anzeige (LCD)', 'LCD', 'box',
         x=50, y=168, w=50, d=22, z=12.5, h=2.5, r=1, mass=6, color='#A9B4A2', materials=[['glas', 85], ['folien', 15]],
         info='Zeigt das Gewicht in Gramm. Zwei dünne Glasplatten mit Flüssigkristall, flach anfassen.',
         marks=raster(4, 5, 4, 1, 9, 12, 11, r=0.5, fill='#7E897A')),
    teil('mikrocontroller', 'circuit_board', 'Steuerchip', 'Steuerchip', 'box',
         x=42.5, y=166, w=6.5, d=8, z=11.7, h=1, r=0.3, mass=0.3, materials=[['chip', 100]], color=CHIP,
         info='Rechnet das Messsignal in Gramm um, steuert Anzeige und Tara-Taste.'),
    teil('adc', 'circuit_board', 'Messverstärker (A/D-Wandler)', 'A/D-Wandler', 'box',
         x=101, y=166, w=6.5, d=8, z=11.7, h=1, r=0.3, mass=0.2, materials=[['chip', 100]], color=CHIP,
         info='Verstärkt die winzige Spannung der Wägezellen und wandelt sie in Zahlen um.'),
    teil('platine', 'circuit_board', 'Platine mit Sensortasten', 'Platine', 'box',
         x=42, y=160, w=66, d=36, z=10.5, h=1.2, r=2, mass=10, color='#2E6B45',
         info='Die Tasten sind Kupferflächen, die einen Finger durch das Glas spüren. Mit Drähten zu den Wägezellen; Elektro-Sammlung.',
         marks=[mark('box', 9, 4, 50, 28, 1, '#3E7D55')]),
    waegezelle(1, 6, 6), waegezelle(2, 110, 6), waegezelle(3, 6, 156), waegezelle(4, 110, 156),
    teil('knopfzelle_1', 'button_cell', 'Knopfzelle CR2032', 'Knopfzellen', 'cyl',
         x=54, y=80, w=20, z=2, h=3.2, mass=3, explode=[120, 0, 8], color='#B9BEC2',
         info='Lithium-Knopfzelle mit 3 V. Beide Seiten abkleben, zur Batterie-Sammelbox, und von kleinen Kindern fernhalten.',
         marks=[mark('cyl', 3, 3, 14, fill='#D0D4D7')]),
    teil('knopfzelle_2', 'button_cell', 'Knopfzelle CR2032', 'Knopfzelle', 'cyl',
         x=76, y=80, w=20, z=2, h=3.2, mass=3, explode=[120, 0, 8], color='#B9BEC2', label=False,
         info='Zweite Zelle, in Reihe geschaltet.', marks=[mark('cyl', 3, 3, 14, fill='#D0D4D7')]),
    teil('batteriedeckel', 'plastic_housing', 'Batteriefachdeckel', 'Batteriedeckel', 'box',
         x=50, y=75, w=50, d=30, z=0, h=1.5, r=3, mass=4, explode=[120, 0, 0], color=GEH,
         info='Im Boden, mit einer Rastnase. Zum Öffnen auf die Rillen drücken und schieben.',
         marks=raster(18, 24, 1, 2, 14, 1.2, 0, 2.5, r=0.5, fill='#1E2226')),
    teil('gehaeuse', 'plastic_housing', 'Gehäuse-Wanne mit Füßen', 'Gehäuse', 'box',
         x=0, y=0, w=150, d=200, z=0, h=15, r=10, mass=110, color=GEH,
         info='Flache Kunststoffwanne. Die Wägezellen stehen auf vier Gummifüßen, die durch den Boden ragen.',
         marks=[mark('box', 50, 75, 50, 30, 3, '#1E2226')] + [mark('cyl', x, y, 10, fill='#1E2226')
                                                               for x, y in ((18, 18), (122, 18), (18, 168), (122, 168))]),
]

explodiere(teile, abstand=80, abstaende={'mikrocontroller': 20, 'adc': 20}, nach_liste=True)
skaliere_masse(teile, oid='kitchen_scale')
schreibe('kitchen_scale', teile)
