"""Rohstoffe, CO2 und Rohstoffwert je Kategorie aus der kleinen Datenbank in data/rohstoffe/.

Rechenweg (jede Zahl trägt ihre Herkunft):
  1. Massen je Material aus dem 3D-Modell (Teile mit material_id aus classifier.json).
  2. Edelmetalle: Gerätewert aus oeko2012, sonst Leiterplattenmasse x Konzentration (oeko2012 Tab. 9/15).
  3. Kobalt: Gerätewert, sonst Akkumasse x Kobaltanteil (Schätzung, siehe elektronik.json).
  4. Kupfer, Aluminium, Eisen, Nickel: aus den Modellmassen (Schätzung).
  5. CO2: Masse x Idemat-Faktor je Material; Ersparnis = Neuware minus Recyclat, wo Idemat beides hat.
  6. Rohstoffwert: Metallmassen x Preise (westmetall, Stand in preise.json). Ohne Preis: nicht enthalten.
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / 'data' / 'rohstoffe'
MAT = json.loads((DB / 'materialien.json').read_text(encoding='utf-8'))
ELEK = json.loads((DB / 'elektronik.json').read_text(encoding='utf-8'))
PREIS = json.loads((DB / 'preise.json').read_text(encoding='utf-8'))
QUELLEN = json.loads((DB / 'quellen.json').read_text(encoding='utf-8'))

# Katalog-Material -> classifier-Material, für handgebaute Teile ohne material_id
RUECK = {'lco': 'li_ion', 'nmc': 'li_ion', 'graphit': 'li_ion', 'elektrolyt': 'li_ion', 'fr4': 'pcb', 'chip': 'pcb', 'lot': 'pcb',
         'kupfer': 'copper', 'kontakte': 'copper', 'alu': 'aluminium', 'stahl': 'steel', 'glas': 'special_glass',
         'displayglas': 'special_glass', 'behaelterglas': 'glass', 'pcabs': 'abs', 'folien': 'multilayer_plastic',
         'ndfeb': 'mixed_electronics', 'ferrit': 'mixed_electronics', 'led': 'mixed_electronics', 'gummi': 'silicone',
         'tpe': 'pvc', 'papier': 'paper', 'holz': 'wood', 'druck': 'paper', 'hdpe': 'hdpe', 'ldpe': 'ldpe', 'pp': 'pp',
         'pet': 'pet', 'ps': 'ps', 'pvc': 'pvc', 'schaum': 'pu_foam', 'nylon': 'nylon', 'polyester': 'polyester',
         'baumwolle': 'cotton', 'wolle': 'wool', 'leder': 'leather', 'kork': 'cork', 'verbund': 'composite_carton',
         'zinkmangan': 'alkaline', 'knopfzelle': 'coin_cell', 'wachs': 'paraffin_wax', 'keramik': 'ceramic',
         'grafitton': 'graphite_clay', 'nichrom': 'nickel_chrome', 'phenolharz': 'phenolic_resin', 'weissblech': 'steel',
         'textil': 'polyester'}

# Anteil der Grundmetalle je classifier-Material (Schätzung, entspricht der Zuordnung in build.py)
METALLANTEIL = {'copper': {'Cu': 1.0}, 'aluminium': {'Al': 1.0}, 'steel': {'Fe': 0.98}, 'nickel_chrome': {'Ni': 0.8},
                'pcb': {'Cu': 0.20}, 'li_ion': {'Cu': 0.10, 'Al': 0.15}, 'mixed_electronics': {'Cu': 0.30, 'Fe': 0.15}}

NAMEN = {'Au': 'Gold', 'Ag': 'Silber', 'Pd': 'Palladium', 'Pt': 'Platin', 'Co': 'Kobalt', 'Cu': 'Kupfer', 'Al': 'Aluminium',
         'Fe': 'Eisen', 'Ni': 'Nickel', 'Nd': 'Neodym', 'Pr': 'Praseodym', 'Dy': 'Dysprosium', 'Ta': 'Tantal',
         'In': 'Indium', 'Ga': 'Gallium', 'Y': 'Yttrium'}


def massen_je_material(parts):
    m = defaultdict(float)
    for p in parts:
        if p.get('material_id') in MAT:
            m[p['material_id']] += p['mass']
        else:
            for kat, anteil in p['materials']:
                m[RUECK.get(kat, 'abs')] += p['mass'] * anteil / 100
    return m


def berechne(oid, parts):
    m = massen_je_material(parts)
    metalle, herkunft = defaultdict(float), {}

    for mat, gramm in m.items():                       # Grundmetalle aus Modellmassen
        for el, a in METALLANTEIL.get(mat, {}).items():
            metalle[el] += gramm * a * 1000          # in mg
            herkunft[el] = 'Modellmassen (Schätzung)'

    geraet = ELEK['geraete'].get(oid)
    if geraet:                                         # Gerätewerte aus der Studie haben Vorrang
        for el, mg in geraet['mg'].items():
            metalle[el] = mg
            herkunft[el] = geraet['tabelle']
    else:
        pcb = m.get('pcb', 0.0)
        if pcb:
            klasse = 'it' if oid in ELEK['it_kategorien'] else 'unterhaltung'
            konz = ELEK['leiterplatte_mg_je_kg'][klasse]
            for el in ('Ag', 'Au', 'Pd'):
                metalle[el] = pcb / 1000 * konz[el]
                herkunft[el] = f'{pcb:.0f} g Leiterplatte × {konz["tabelle"]}'.replace('.', ',')
        if m.get('li_ion'):
            a = ELEK['akku_kobaltanteil']['wert']
            metalle['Co'] = m['li_ion'] * a * 1000
            herkunft['Co'] = f'{m["li_ion"]:.0f} g Akku × {a:.1%} Kobalt (Schätzung, oeko2012 Tab. 25)'.replace('.', ',')

    co2 = co2_rec = 0.0
    ohne_faktor = []
    for mat, gramm in m.items():
        f = MAT.get(mat, {})
        if f.get('co2e_primary') is None:
            ohne_faktor.append(mat)
            continue
        co2 += gramm / 1000 * f['co2e_primary']
        co2_rec += gramm / 1000 * (f['co2e_recycled'] if f.get('co2e_recycled') is not None else f['co2e_primary'])

    preise = PREIS['eur_je_g']
    wert = sum(metalle[el] / 1000 * preise[el] for el in metalle if el in preise)
    ohne_preis = sorted(el for el in metalle if el not in preise and metalle[el] >= 1 and el in ('Pd', 'Co', 'Pt'))

    metalle = {el: round(v, 2 if v < 10 else 0) for el, v in sorted(metalle.items(), key=lambda x: -x[1]) if v >= 0.01}
    return {
        'metalle_mg': metalle,
        'herkunft': {el: herkunft[el] for el in metalle},
        'materialien_g': {k: round(v, 1) for k, v in sorted(m.items(), key=lambda x: -x[1])},
        'co2_kg': round(co2, 3), 'co2_mit_recyclat_kg': round(co2_rec, 3), 'co2_ersparnis_kg': round(co2 - co2_rec, 3),
        'co2_ohne_faktor': ohne_faktor,
        'rohstoffwert_eur': round(wert, 2), 'wert_ohne_preis': ohne_preis, 'preisstand': PREIS['stand'],
        'quellen': {k: {'titel': v['titel'], 'url': v['url']} for k, v in QUELLEN.items()},
    }


def zahl(v, einheit):
    s = f'{v:.2f}' if v < 10 else f'{v:.1f}' if v < 100 else f'{v:.0f}'
    return f'≈ {s.replace(".", ",")} {einheit}'


def werte(r):
    edel = [NAMEN[e] for e in ('Au', 'Ag', 'Pd', 'Co', 'Cu') if r['metalle_mg'].get(e, 0) >= 1][:3]
    ohne = f' Ohne {", ".join(NAMEN[e] for e in r["wert_ohne_preis"])} (kein Preis).' if r['wert_ohne_preis'] else ''
    return [
        {'k': 'Rohstoffwert', 'v': zahl(r['rohstoffwert_eur'], '€') if r['rohstoffwert_eur'] >= 0.01 else '< 0,01 €',
         'hint': (f'{", ".join(edel)} zu Preisen vom {r["preisstand"][8:10]}.{r["preisstand"][5:7]}.' if edel
                  else 'Kaum Metalle enthalten.') + ohne},
        {'k': 'CO₂ der Materialien', 'v': zahl(r['co2_kg'], 'kg'), 'hint': 'Neuware, ohne Montage und Transport (Idemat 2026)'},
        {'k': 'mit Recyclat', 'v': zahl(r['co2_mit_recyclat_kg'], 'kg'),
         'hint': f'spart {zahl(r["co2_ersparnis_kg"], "kg")[2:]}, wenn recycelte Materialien eingesetzt werden'},
    ]
