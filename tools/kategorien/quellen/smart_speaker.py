"""3D-Modell: smart_speaker. Erzeugt tools/kategorien/modelle/smart_speaker.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, explodiere, skaliere_masse, schreibe  # noqa: E402

# Zylindrischer Smart Speaker (Ø 100 mm, 150 mm hoch) mit Stoffbezug. Innen ein Kunststoffrohr als Gehäuse:
# unten der nach unten abstrahlende Tieftöner mit Magnet, darüber Hauptplatine und Hochtöner, oben
# Mikrofonplatine mit LED-Ring unter dem Deckel mit Tasten. Externes Steckernetzteil.
# Explosion: Sockel bleibt, das Innengehäuse schwebt knapp darüber, alle Innenteile über dessen Oberkante
# gestapelt, Deckel ganz oben. Stoffbezug nach rechts (dx > 0, dy < 0), Netzteil und Kabel nach links.
GEH = '#2B2F33'
PCB = '#2E6B45'

teile = [
    teil('deckel', 'plastic_housing', 'Deckel mit Tasten', 'Deckel', 'cyl',
         x=0, y=0, w=100, z=140, h=10, mass=40, color=GEH,
         info='Oberer Abschluss mit Laut-, Leise- und Mikrofon-Taste. Nach dem Abnehmen des Stoffbezugs abschrauben.',
         marks=[mark('cyl', 3, 3, 94, fill='#5DADE2'), mark('cyl', 6, 6, 88, fill='#3A3F44'), mark('cyl', 22, 44, 12, fill='#1E2226'),
                mark('cyl', 44, 44, 12, fill='#1E2226'), mark('cyl', 66, 44, 12, fill='#C0392B')]),
    teil('ledring', 'circuit_board', 'LED-Ring', 'LED-Ring', 'cyl',
         x=5, y=5, w=90, z=138, h=2, mass=8, materials=[['fr4', 45], ['led', 25], ['kupfer', 20], ['pcabs', 10]], color='#DDE6EA',
         info='Ringförmige Platine mit kleinen LEDs. Leuchtet, wenn der Lautsprecher zuhört oder antwortet.',
         marks=[mark('cyl', 6, 6, 78, fill='#5DADE2'), mark('cyl', 10, 10, 70, fill='#DDE6EA')]),
    teil('mikrofonplatine', 'circuit_board', 'Mikrofonplatine', 'Mikrofone', 'cyl',
         x=10, y=10, w=80, z=136, h=1.6, mass=10, color=PCB,
         info='Mit mehreren winzigen Mikrofonen, die hören, aus welcher Richtung gesprochen wird. Die Stummtaste trennt sie ab.',
         marks=[mark('cyl', 36, 4, 8, fill='#22272B'), mark('cyl', 36, 68, 8, fill='#22272B'),
                mark('cyl', 4, 36, 8, fill='#22272B'), mark('cyl', 68, 36, 8, fill='#22272B')]),
    teil('hochtoener', 'speaker_driver', 'Hochtöner', 'Hochtöner', 'cyl',
         x=30, y=30, w=40, z=108, h=22, mass=40, materials=[['ndfeb', 30], ['stahl', 30], ['kupfer', 15], ['pcabs', 15], ['textil', 10]],
         color='#5E656A',
         info='Kleiner Lautsprecher für hohe Töne mit Neodym-Magnet. Hält sich an Stahl fest; von Bankkarten fernhalten.',
         marks=[mark('cyl', 8, 8, 24, fill='#C9CED2')]),
    teil('soc', 'circuit_board', 'Prozessor mit WLAN', 'Prozessor', 'box',
         x=38, y=38, w=14, d=14, z=101.6, h=1.2, r=1, mass=3, materials=[['chip', 100]], color='#22272B',
         info='Verarbeitet Sprache und Musik und funkt per WLAN und Bluetooth. Die Spracherkennung läuft meist im Internet.'),
    teil('hauptplatine', 'circuit_board', 'Hauptplatine', 'Hauptplatine', 'box',
         x=20, y=20, w=60, d=60, z=100, h=1.6, r=6, mass=35, color=PCB,
         info='Mit Verstärker, Speicher und Stromanschluss. Steckverbinder abziehen, zwei Schrauben lösen.',
         marks=[mark('box', 40, 4, 14, 10, 1, '#22272B'), mark('box', 4, 44, 12, 10, 1, '#B7BCC0')]),
    teil('magnet', 'speaker_driver', 'Tieftöner-Magnet', 'Magnet', 'cyl',
         x=27.5, y=27.5, w=45, z=72, h=20, mass=150, materials=[['ferrit', 70], ['stahl', 25], ['kupfer', 5]], color='#5E656A',
         info='Schwerer Ferritmagnet mit Stahlpolplatten und Schwingspule. Kommt mit dem Stahl ins Altmetall.',
         marks=[mark('cyl', 12.5, 12.5, 20, fill='#9AA2A8')]),
    teil('tieftoener', 'speaker_driver', 'Tieftöner (Korb und Membran)', 'Tieftöner', 'cyl',
         x=12, y=12, w=76, z=30, h=42, mass=120, materials=[['stahl', 45], ['papier', 25], ['gummi', 15], ['kupfer', 10], ['pcabs', 5]],
         color='#3A3F44',
         info='Großer Lautsprecher für den Bass, strahlt nach unten. Stahlkorb mit Papiermembran und Gummisicke.',
         marks=[mark('cyl', 6, 6, 64, fill='#2B2F33'), mark('cyl', 26, 26, 24, fill='#9AA2A8')]),
    teil('innengehaeuse', 'plastic_housing', 'Innengehäuse', 'Innengehäuse', 'cyl',
         x=2, y=2, w=96, z=10, h=128, mass=250, color='#3A3F44', wand=3, boden=0,
         info='Stabiles Kunststoffrohr, in dem alle Teile verschraubt sind. Es bildet den Resonanzraum für den Bass.',
         marks=[mark('cyl', 4, 4, 88, fill='#2B2F33', zeichnung=True)]),
    teil('stoffbezug', 'speaker_fabric_cover', 'Stoffbezug', 'Stoffbezug', 'cyl',
         x=0, y=0, w=100, z=10, h=130, explode=[130, -130, 0], mass=25, color='#8A9096', wand=1.5, boden=0,
         info='Polyestergewebe über einem dünnen Gitter. Sockel abhebeln, dann den Stoff nach oben abrollen. Waschbar und wiederverwendbar.',
         marks=[mark('cyl', 2, 2, 96, fill='#5E656A', zeichnung=True)]),
    teil('netzteil', 'power_adapter', 'Steckernetzteil', 'Netzteil', 'box',
         x=30, y=30, w=40, d=40, z=14, h=30, r=6, explode=[-130, 130, 0], mass=90,
         materials=[['pcabs', 35], ['kupfer', 25], ['ferrit', 15], ['fr4', 15], ['chip', 5], ['elektrolyt', 5]], color='#F2F2F2',
         info='Wandelt 230 Volt in 15 Volt um. Nicht öffnen; zusammen mit dem Lautsprecher als Elektroschrott abgeben.',
         marks=[mark('box', 8, 8, 24, 24, 4, '#E4E6E8')]),
    teil('kabel', 'power_adapter', 'Anschlusskabel', 'Kabel', 'box', form='liegend_x', material_id='pvc',
         x=10, y=74, w=80, d=6, z=12, h=6, r=3, explode=[-150, 200, 0], mass=40, materials=[['pvc', 60], ['kupfer', 35], ['pcabs', 5]],
         color='#F2F2F2', info='1,5 m Kabel mit Rundstecker. PVC-Mantel längs aufschlitzen, um die Kupferadern zu gewinnen.'),
    teil('sockel', 'plastic_housing', 'Sockel mit Gummifuß', 'Sockel', 'cyl',
         x=0, y=0, w=100, z=0, h=10, mass=60, materials=[['pcabs', 80], ['gummi', 20]], color=GEH,
         info='Bodenteil mit rutschfestem Gummiring und Strombuchse. Mit einem flachen Werkzeug abhebeln.',
         marks=[mark('cyl', 6, 6, 88, fill='#1E2226'), mark('cyl', 12, 12, 76, fill=GEH)]),
]

explodiere(teile, abstand=32, fest=('sockel',), abstaende={'soc': 10, 'innengehaeuse': 45})
skaliere_masse(teile, oid='smart_speaker')
for p in teile:   # Foto-Ansicht: echte Formen (form) tragen keine aufgemalten Details
    if p.get('form') and p.get('marks'):
        p['marks'] = [dict(k, zeichnung=True) for k in p['marks']]
schreibe('smart_speaker', teile)
