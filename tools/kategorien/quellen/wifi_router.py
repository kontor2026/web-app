"""3D-Modell: wifi_router. Erzeugt tools/kategorien/modelle/wifi_router.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Typischer WLAN-Router mit vier Klappantennen: Gehäuse 190 × 140 × 32 mm, Anschlüsse hinten (y = 0),
# Antennen flach nach vorne umgeklappt auf dem Deckel. Rechts daneben das Steckernetzteil.
# Explosion: Ebenen nach oben, Antennen schweben über dem Deckel, Netzteil nach rechts.
GEH = '#2B2F33'
CHIP = '#3F4547'
ANT = [['pcabs', 75], ['kupfer', 15], ['messing', 10]]


def antenne(i, x):
    return teil(f'antenne_{i}', 'router_antennas', f'Antenne {i}', 'Antennen' if i == 1 else f'Antenne {i}', 'box', form='liegend_y',
                x=x, y=8, w=12, d=125, z=32, h=8, r=5, mass=12, materials=ANT, color='#23272A', label=None if i == 1 else False,
                info='Kunststoffstab mit einem Kupferstreifen als Strahler, über ein Gelenk mit Messing-Schraubanschluss. '
                     'Von Hand abschrauben.' if i == 1 else 'Gleich gebaut wie Antenne 1, sendet in einer eigenen Richtung.',
                marks=[mark('cyl', 2, 2, 8, fill='#B8A060')])


teile = [
    antenne(1, 15), antenne(2, 60), antenne(3, 118), antenne(4, 163),
    teil('oberschale', 'plastic_housing', 'Gehäuse-Oberteil', 'Oberteil', 'box',
         x=0, y=0, w=190, d=140, z=16, h=16, r=10, mass=90, color=GEH,
         info='Deckel mit Lüftungsschlitzen und Leuchtanzeigen. Schrauben stecken unter den Gummifüßen, danach ringsum aufclipsen.',
         marks=raster(45, 30, 10, 1, 4, 60, 10, r=2, fill='#1E2226') + raster(40, 130, 8, 1, 3, 3, 15, shape='cyl', fill='#7FC8F0')),
    teil('lichtleiter', 'plastic_housing', 'Lichtleiter für Anzeigen', 'Lichtleiter', 'box', material_id='pc',
         x=38, y=126, w=112, d=6, z=10, h=5, r=1, mass=3, materials=[['pcabs', 100]], color='#CFE6F2', opacity=0.75,
         info='Durchsichtiger Kunststoffkamm, der das Licht der kleinen LEDs auf der Platine nach oben zum Deckel leitet.',
         marks=raster(1, 1, 8, 1, 4, 4, 15, shape='cyl', fill='#7FC8F0')),
    teil('kuehlkoerper', 'circuit_board', 'Kühlkörper', 'Kühlkörper', 'box', material_id='aluminium',
         x=65, y=45, w=45, d=45, z=11, h=7, r=2, mass=25, materials=[['alu', 100]], color='#C9CED2',
         info='Aluminiumblock mit Rippen, leitet die Wärme vom Prozessor ab. Mit Wärmeleitpad aufgeklebt oder geklemmt.',
         marks=raster(3, 3, 8, 1, 2, 39, 5.3, r=0.5, fill='#AEB4B8')),
    teil('soc', 'circuit_board', 'Netzwerkprozessor', 'Prozessor', 'box',
         x=76, y=56, w=22, d=22, z=9.6, h=1.4, r=1, mass=2.5, materials=[['chip', 100]], color=CHIP,
         info='Leitet die Datenpakete zwischen Internet, Kabel und WLAN weiter. Wird im Betrieb warm.'),
    teil('wlan_24', 'circuit_board', 'WLAN-Chip 2,4 GHz mit Abschirmung', 'WLAN 2,4 GHz', 'box',
         x=25, y=85, w=26, d=26, z=9.6, h=3, r=1, mass=4, materials=[['stahl', 60], ['chip', 30], ['kupfer', 10]],
         color='#B7BCC0', info='Funkchip unter einem Blechdeckel, der Störungen abschirmt. Der Deckel lässt sich abhebeln.'),
    teil('wlan_5', 'circuit_board', 'WLAN-Chip 5 GHz mit Abschirmung', 'WLAN 5 GHz', 'box',
         x=135, y=85, w=26, d=26, z=9.6, h=3, r=1, mass=4, materials=[['stahl', 60], ['chip', 30], ['kupfer', 10]],
         color='#B7BCC0', info='Zweites Funkband: schneller, reicht aber weniger weit durch Wände.'),
    teil('ram', 'circuit_board', 'Arbeitsspeicher', 'RAM', 'box',
         x=120, y=55, w=10, d=14, z=9.6, h=1.2, r=0.5, mass=0.8, materials=[['chip', 100]], color=CHIP,
         info='Merkt sich im Betrieb Verbindungen und Einstellungen. Ohne Strom ist er leer.'),
    teil('buchsen', 'circuit_board', 'Netzwerk-Buchsen (LAN/WAN)', 'LAN-Buchsen', 'box', material_id='steel',
         x=40, y=4, w=90, d=18, z=9.6, h=13.5, r=1, mass=25, materials=[['stahl', 50], ['pcabs', 35], ['kupfer', 10], ['kontakte', 5]],
         color='#B7BCC0', info='Fünf RJ45-Buchsen aus Stahlblech mit Übertragern. Hier wird das Netzwerkkabel eingesteckt.',
         marks=raster(3, 4, 5, 1, 15, 10, 17.5, r=1, fill='#2A2E31')),
    teil('platine', 'circuit_board', 'Hauptplatine', 'Platine', 'box',
         x=8, y=4, w=174, d=128, z=8, h=1.6, r=3, mass=45, color='#2E6B45',
         info='Große Leiterplatte mit allen Chips. Antennenkabel abziehen, Schrauben lösen und in die Elektro-Sammlung geben.',
         marks=[mark('box', 140, 2, 12, 10, 1, '#22272B'), mark('cyl', 160, 3, 8, fill='#22272B')]),
    teil('unterschale', 'plastic_housing', 'Gehäuse-Unterteil', 'Unterteil', 'box',
         x=0, y=0, w=190, d=140, z=0, h=16, r=10, mass=90, color=GEH, wand=2,
         info='Wanne mit Füßen, Wandhalterungs-Löchern und Lüftungsschlitzen. Ohne Elektronik reiner Kunststoff.',
         marks=[dict(m, zeichnung=True) for m in raster(20, 40, 12, 1, 3, 60, 13, r=1.5, fill='#1E2226')]),
    teil('dc_kabel', 'power_adapter', 'Niedervolt-Kabel mit Hohlstecker', 'DC-Kabel', 'box', form='liegend_y', material_id='copper',
         x=210, y=0, w=6, d=50, z=0, h=6, r=3, mass=25, explode=[45, -40, 0], color='#1E2226',
         materials=[['pvc', 60], ['kupfer', 35], ['messing', 5]],
         info='Dünnes Kabel vom Netzteil zum Router, endet in einem Hohlstecker aus Messing. Kupferadern freilegen und getrennt sammeln.',
         marks=[mark('box', 0.5, 0, 5, 8, 2, '#9BA3A8')]),
    teil('netzteil', 'power_adapter', 'Steckernetzteil 12 V', 'Netzteil', 'box',
         x=196, y=50, w=40, d=60, z=0, h=30, r=5, mass=95, explode=[45, 0, 0], color='#2E3338',
         materials=[['pcabs', 35], ['kupfer', 25], ['ferrit', 15], ['stahl', 10], ['fr4', 10], ['chip', 5]],
         info='Wandelt 230 V in 12 V um, mit Trafo und Platine im verklebten Gehäuse. Nicht öffnen: Kondensatoren können geladen sein.',
         marks=[mark('box', 6, 8, 28, 20, 2, '#E8E8E2'), mark('cyl', 9, 40, 5, fill='#9BA3A8'), mark('cyl', 26, 40, 5, fill='#9BA3A8')]),
]

explodiere(teile, abstand=60, abstaende={'oberschale': 90, 'soc': 20, 'wlan_24': 20, 'wlan_5': 20, 'ram': 20, 'buchsen': 20, 'kuehlkoerper': 20},
           nach_liste=True)
skaliere_masse(teile, oid='wifi_router')
for p in teile:   # Foto-Ansicht: echte Formen (form) tragen keine aufgemalten Details
    if p.get('form') and p.get('marks'):
        p['marks'] = [dict(k, zeichnung=True) for k in p['marks']]
schreibe('wifi_router', teile)
