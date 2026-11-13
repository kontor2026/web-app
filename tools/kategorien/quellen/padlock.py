"""3D-Modell: padlock. Erzeugt tools/kategorien/modelle/padlock.json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bau import teil, mark, raster, skaliere_masse, schreibe  # noqa: E402

# Messing-Vorhängeschloss aufrecht (laut CSV 40 × 20 × 70 mm): Körper 40 × 20 × 45 mm, darüber der Stahlbügel.
# Im Körper sitzt senkrecht der Schließzylinder (Kern Ø 11 mm, Schlüsselloch unten) mit vier waagrechten
# Stiftzuhaltungen: Kernstift, Gehäusestift, Feder. Zwei Stahlkugeln sperren den Bügel.
# Explodiert: Körper zur Seite, Bügel nach oben, Kugeln leicht angehoben, Stifte und Federn reihenweise nach rechts.
MESSING = '#C9A74C'
STAHL = '#B8BEC4'
STIFTE = [(8, 3.5), (14, 5), (20, 4), (26, 4.5)]   # (z, Länge Kernstift)
X0 = 24          # Kernstifte beginnen im Kern
ENDE = 37        # Ende der Stiftbohrung


def stifte():
    teile = []
    for n, (z, kl) in enumerate(STIFTE):
        erst = n == 0
        teile.append(teil(f'kernstift_{n + 1}', 'padlock_body', 'Kernstifte', 'Kernstift', 'box',
                          material_id='copper', x=X0, y=8.75, w=kl, d=2.5, z=z, h=2.5, r=1.2,
                          explode=[6, 0, 0], mass=0.15, materials=[['messing', 100]], label=erst,
                          info=('Unterschiedlich lange Messingstifte. Nur der passende Schlüssel schiebt jeden genau '
                                'bis an den Rand des Kerns.') if erst else 'Weiterer Kernstift, andere Länge.',
                          color='#D8B85A'))
    for n, (z, kl) in enumerate(STIFTE):
        erst = n == 0
        teile.append(teil(f'gehaeusestift_{n + 1}', 'padlock_body', 'Gehäusestifte', 'Gehäusestift', 'box',
                          material_id='copper', x=X0 + kl, y=8.75, w=3.5, d=2.5, z=z, h=2.5, r=1.2,
                          explode=[14, 0, 0], mass=0.12, materials=[['messing', 100]], label=erst,
                          info=('Ohne Schlüssel ragen sie in den Kern und blockieren ihn. Mit dem richtigen Schlüssel '
                                'liegt ihre Trennstelle genau am Kernrand und der Kern dreht sich.') if erst
                          else 'Weiterer Gehäusestift.',
                          color='#B8963E'))
    for n, (z, kl) in enumerate(STIFTE):
        erst = n == 0
        x = X0 + kl + 3.5
        teile.append(teil(f'feder_{n + 1}', 'padlock_body', 'Zuhaltungsfedern', 'Feder', 'box',
                          material_id='steel', x=x, y=8.75, w=ENDE - x, d=2.5, z=z, h=2.5, r=1,
                          explode=[22, 0, 0], mass=0.05, materials=[['stahl', 100]], label=erst,
                          info='Winzige Stahlfedern drücken die Stifte in den Kern zurück.' if erst
                          else 'Weitere Zuhaltungsfeder.',
                          color=STAHL, marks=raster(0.3, 0.3, int((ENDE - x) // 1.2), 1, 0.5, 1.9, 1.2,
                                                    fill='#7E868C')))
    return teile


teile = [
    teil('buegel_bogen', 'steel_shackle', 'Bügel', 'Bügel', 'box',
         x=5, y=7, w=30, d=6, z=64, h=6, r=3, explode=[0, 0, 35], mass=9,
         info='Gehärteter, verchromter Stahl, damit man ihn nicht durchsägen kann. Nur mit einem Bolzenschneider '
              'aufknipsen, wenn der Schlüssel fehlt.',
         color=STAHL),
    teil('buegel_lang', 'steel_shackle', 'Langer Bügelschenkel', 'Schenkel', 'cyl',
         x=5, y=7, w=6, z=18, h=46, explode=[0, 0, 35], mass=11, label=False,
         info='Der lange Schenkel bleibt beim Öffnen im Körper; um ihn dreht sich der Bügel.',
         color=STAHL, marks=[mark('cyl', 1, 1, 4, fill='#9AA2A6')]),
    teil('buegel_kurz', 'steel_shackle', 'Kurzer Bügelschenkel', 'Schenkel', 'cyl',
         x=29, y=7, w=6, z=36, h=28, explode=[0, 0, 35], mass=6, label=False,
         info='Der kurze Schenkel hat eine Kerbe, in die die Sperrkugel greift.',
         color=STAHL, marks=[mark('cyl', 1, 1, 4, fill='#9AA2A6')]),
    teil('kugel_l', 'steel_shackle', 'Sperrkugeln', 'Sperrkugeln', 'cyl', x=11, y=7.5, w=5, z=37, h=5,
         explode=[0, 0, 10], mass=0.5,
         info='Zwei Stahlkugeln, die in Kerben der Bügelschenkel greifen. Dreht der Schlüssel, fallen sie zurück '
              'und der Bügel springt auf.', color='#9AA2A6'),
    teil('kugel_r', 'steel_shackle', 'Sperrkugel rechts', 'Sperrkugel', 'cyl', x=24, y=7.5, w=5, z=37, h=5,
         explode=[0, 0, 10], mass=0.5, label=False, info='Zweite Sperrkugel.', color='#9AA2A6'),
    teil('kern', 'padlock_body', 'Zylinderkern', 'Kern', 'cyl', material_id='copper',
         x=14.5, y=4.5, w=11, z=3, h=34, explode=[0, 0, 0], mass=8, materials=[['messing', 100]],
         info='Drehbarer Messingkern mit dem Schlüsselkanal. Er lässt sich nur drehen, wenn alle Stifte richtig stehen.',
         color=MESSING, marks=[mark('box', 4.5, 2, 2, 7, 0.5, '#4A3B1E'), mark('cyl', 3.5, 3.5, 4, fill='#B8963E')]),
    *stifte(),
    teil('koerper', 'padlock_body', 'Schlosskörper', 'Körper', 'box',
         x=0, y=0, w=40, d=20, z=0, h=45, r=3, explode=[-60, 0, 0], mass=110, materials=[['messing', 100]],
         info='Massiver Messingblock mit Bohrungen für Zylinder, Stifte und Bügel. Messing ist wertvoller Schrott: '
              'alte Schlösser beim Schrotthändler oder Wertstoffhof abgeben.',
         color=MESSING, marks=[mark('cyl', 5, 7, 6, fill='#4A3B1E'), mark('cyl', 29, 7, 6, fill='#4A3B1E')]),
]

skaliere_masse(teile, oid='padlock')
schreibe('padlock', teile)
