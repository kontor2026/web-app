"""3D-Modell: tablet. Erzeugt tools/kategorien/modelle/tablet.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, schreibe  # noqa: E402

# Typisches 10,9-Zoll-Tablet im Hochformat: 178 × 248 × 7 mm, Aluminium-Unibody.
# Innen: Logikplatine längs am linken Rand, zwei Akkuzellen, vier Lautsprecher-Kammern sind hier zwei Module.
CHIP = '#3F4547'
teile = [
    teil('deckglas', 'tablet_display', 'Deckglas', 'Deckglas', 'box',
         x=0, y=0, w=178, d=248, z=6.4, h=0.6, r=12, mass=58, materials=[['glas', 100]], color='#353B40', opacity=0.8,
         info='Chemisch gehärtetes Glas, zugleich die Touch-Fläche. Mit Wärme und Kunststoff-Plektren vom Rahmen lösen, '
              'dabei Schutzbrille tragen: Es kann splittern.',
         marks=[mark('cyl', 84, 5, 10, fill='#262B2F')]),
    teil('display', 'tablet_display', 'Display-Einheit (LCD)', 'Display', 'box',
         x=1, y=1, w=176, d=246, z=5.2, h=1.2, r=11, mass=110,
         materials=[['displayglas', 50], ['folien', 30], ['led', 10], ['kupfer', 10]], color='#31373B',
         info='Flüssigkristallanzeige mit LED-Hintergrundlicht und Lichtleitfolien. Mit dünnen Flachbandkabeln an der Platine angesteckt.',
         marks=[mark('box', 9, 9, 158, 228, 4, '#3D464C')]),
    teil('soc', 'circuit_board', 'Prozessor (SoC)', 'Prozessor', 'box',
         x=12, y=70, w=16, d=16, z=2.2, h=1, r=1, mass=2.5, materials=[['chip', 100]], color=CHIP,
         info='Rechenkern, Grafik und Arbeitsspeicher in einem Gehäuse. Steckt unter einem Abschirmblech.'),
    teil('speicher', 'circuit_board', 'Speicherchip (NAND)', 'Speicher', 'box',
         x=13, y=96, w=14, d=18, z=2.2, h=1, r=1, mass=1.5, materials=[['chip', 100]], color=CHIP,
         info='Speichert Fotos, Apps und Konten. Vor dem Abgeben das Tablet auf Werkseinstellungen zurücksetzen.'),
    teil('kamera', 'circuit_board', 'Rückkamera', 'Kamera', 'box',
         x=8, y=8, w=22, d=22, z=1, h=4, r=4, mass=4, material_id='mixed_electronics',
         materials=[['chip', 35], ['alu', 30], ['glas', 20], ['ndfeb', 15]], color='#5E656A',
         info='Bildsensor mit Linsen und kleinem Magnetantrieb für den Autofokus. Mit einem Stecker auf der Platine.',
         marks=[mark('cyl', 4, 4, 14, fill='#262B2F')]),
    teil('frontkamera', 'circuit_board', 'Frontkamera', 'Frontkamera', 'box',
         x=80, y=3, w=18, d=8, z=1, h=3, r=2, mass=1.5, material_id='mixed_electronics',
         materials=[['chip', 50], ['glas', 30], ['alu', 20]], color='#5E656A',
         info='Kleine Kamera für Videoanrufe, oben mittig unter dem Glasrand.',
         marks=[mark('cyl', 5, 0.5, 7, fill='#262B2F')]),
    teil('platine', 'circuit_board', 'Logikplatine', 'Platine', 'box',
         x=8, y=36, w=24, d=176, z=1, h=1.2, r=3, mass=20, materials=[['fr4', 45], ['kupfer', 25], ['chip', 20], ['lot', 10]],
         info='Schmale Leiterplatte mit Funk-, Lade- und Audiochips. Hier stecken Gold und Kupfer: ab zur Elektro-Sammlung.',
         marks=raster(5, 130, 2, 3, 6, 6, 8, 10)),
    teil('akku1', 'li_ion_battery', 'Akkuzelle oben', 'Akku', 'box',
         x=40, y=22, w=128, d=98, z=1, h=3.8, r=3, mass=56,
         materials=[['lco', 38], ['graphit', 20], ['elektrolyt', 15], ['kupfer', 10], ['alu', 10], ['folien', 7]],
         info='Zusammen mit der zweiten Zelle etwa 7.500 mAh. Sehr fest verklebt: niemals mit Metallwerkzeug hebeln, '
              'ein beschädigter Akku kann brennen.',
         marks=[mark('box', 4, 4, 120, 90, 2)]),
    teil('akku2', 'li_ion_battery', 'Akkuzelle unten', 'Akku', 'box',
         x=40, y=124, w=128, d=98, z=1, h=3.8, r=3, mass=56, label=False,
         materials=[['lco', 38], ['graphit', 20], ['elektrolyt', 15], ['kupfer', 10], ['alu', 10], ['folien', 7]],
         info='Zweite Zelle, parallel geschaltet. Pole abkleben und zur Batterie-Sammelstelle bringen.',
         marks=[mark('box', 4, 4, 120, 90, 2)]),
    teil('lautsprecher_l', 'circuit_board', 'Lautsprecher links', 'Lautsprecher', 'box',
         x=8, y=226, w=50, d=16, z=1, h=4, r=3, mass=7, material_id='mixed_electronics',
         materials=[['pcabs', 45], ['ndfeb', 35], ['kupfer', 20]], color='#6E7579',
         info='Kleiner Neodym-Magnet mit Schwingspule in einer Kunststoffkammer. Ausgebaut weiter nutzbar.',
         marks=raster(4, 5, 8, 1, 3, 6, 5.5, shape='cyl')),
    teil('lautsprecher_r', 'circuit_board', 'Lautsprecher rechts', 'Lautsprecher', 'box',
         x=120, y=226, w=50, d=16, z=1, h=4, r=3, mass=7, material_id='mixed_electronics', label=False,
         materials=[['pcabs', 45], ['ndfeb', 35], ['kupfer', 20]], color='#6E7579',
         info='Zweiter Lautsprecher für Stereo-Ton.',
         marks=raster(4, 5, 8, 1, 3, 6, 5.5, shape='cyl')),
    teil('buchse', 'circuit_board', 'USB-C-Buchse', 'USB-C', 'box',
         x=79, y=230, w=20, d=14, z=1, h=3, r=2, mass=2, material_id='mixed_electronics',
         materials=[['stahl', 40], ['kupfer', 25], ['kontakte', 15], ['pcabs', 20]], color='#9BA3A8',
         info='Ladebuchse auf einer eigenen kleinen Platine, mit Flachbandkabel verbunden. Lässt sich einzeln tauschen.',
         marks=[mark('box', 4, 9, 12, 4, 2, '#262B2F')]),
    teil('gehaeuse', 'aluminium_housing', 'Aluminium-Gehäuse', 'Gehäuse', 'box',
         x=0, y=0, w=178, d=248, z=0, h=1, r=12, mass=150, materials=[['alu', 100]], color='#C9CCCF',
         info='Aus einem Aluminiumblock gefräst. Erst alle Bauteile ausbauen, dann ist die leere Schale reines Aluminium.',
         marks=[mark('box', 3, 3, 172, 242, 10), mark('cyl', 12, 12, 14, fill='#262B2F')]),
]

# Ebenen: Gehäuse, Innenleben, Display, Deckglas. Die Chips schweben etwas über der Platine.
chips = {'soc', 'speicher'}
explodiere([p for p in teile if p['id'] not in chips], abstand=95)
dz_platine = next(p for p in teile if p['id'] == 'platine')['explode'][2]
for p in teile:
    if p['id'] in chips:
        p['explode'] = [0, 0, dz_platine + 30]
schreibe('tablet', teile)
