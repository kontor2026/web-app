"""Deterministische Geometrie: aus der KI-Beschreibung (Ebenen, Anteile, Position) wird ein
zeichenbares Objekt im Format von docs/objekt-schema.md. Die KI muss keine Koordinaten rechnen,
deshalb ist jede gültige Antwort auch eine saubere Explosionszeichnung."""
import re

ANKER = {
    'hinten-links': (0, 0), 'hinten': (0.5, 0), 'hinten-rechts': (1, 0),
    'links': (0, 0.5), 'mitte': (0.5, 0.5), 'rechts': (1, 0.5),
    'vorne-links': (0, 1), 'vorne': (0.5, 1), 'vorne-rechts': (1, 1),
}


def slug(text):
    s = text.lower()
    for a, b in [('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('ß', 'ss')]:
        s = s.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:40] or 'teil'


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def build_parts(spec):
    W = clamp(float(spec['masse_mm']['breite']), 10, 2000)
    D = clamp(float(spec['masse_mm']['tiefe']), 10, 2000)
    H = clamp(float(spec['masse_mm']['hoehe']), 1, 2000)
    teile = spec['bauteile']

    # Ebenen auf 0..n verdichten, damit keine leeren Lücken entstehen.
    ebenen = sorted({t['ebene'] for t in teile})
    index = {e: i for i, e in enumerate(ebenen)}

    # Dicken: pro Ebene das dickste Teil. Summe wird auf die Gesamthöhe skaliert.
    dicke = {i: 0.0 for i in index.values()}
    for t in teile:
        i = index[t['ebene']]
        dicke[i] = max(dicke[i], clamp(float(t['dicke_mm']), 0.3, H))
    summe = sum(dicke.values()) or 1
    f = min(1.0, H / summe) if summe > H * 1.2 else 1.0
    z_ebene, z = {}, 0.0
    for i in sorted(dicke):
        z_ebene[i] = z
        z += dicke[i] * f

    gap = max(12.0, 0.2 * (W + D), 0.12 * H)    # Abstand der Ebenen in der Explosionsansicht
    parts, ids = [], set()
    for t in sorted(teile, key=lambda t: -t['ebene']):      # oberste Ebene bekommt Nummer 01
        i = index[t['ebene']]
        voll = t['form'] in ('platte', 'block') and t['breite_anteil'] > 0.85 and t['tiefe_anteil'] > 0.85
        if voll:
            w, d, x, y = W, D, 0.0, 0.0
        else:
            w = clamp(W * t['breite_anteil'], 3, W)
            d = clamp(D * t['tiefe_anteil'], 3, D)
            if t['form'] == 'rund':
                w = d = min(w, d)
            ax, ay = ANKER.get(t['position'], (0.5, 0.5))
            x, y = ax * (W - w), ay * (D - d)
        h = clamp(float(t['dicke_mm']), 0.3, H) * f
        r = min(w, d) * (0.08 if t['form'] == 'platte' else 0.15)
        pid = slug(t['name'])
        while pid in ids:
            pid += '-2'
        ids.add(pid)

        mats = [m for m in t['materialien'] if m.get('anteil', 0) > 0]
        total = sum(m['anteil'] for m in mats) or 1
        materials = [[m['id'], round(m['anteil'] * 100 / total)] for m in mats]

        part = {
            'id': pid, 'name': t['name'], 'short': t.get('kurz') or t['name'],
            'shape': 'cyl' if t['form'] == 'rund' else 'box',
            'x': round(x, 1), 'y': round(y, 1), 'w': round(w, 1), 'd': round(d, 1),
            'h': round(h, 2), 'z': round(z_ebene[i], 2), 'r': round(r, 1),
            'explode': [0, 0, round(i * gap, 1)],
            'mass': round(float(t['masse_g']), 1), 'materials': materials, 'info': t['info'],
        }
        if part['shape'] == 'cyl':
            del part['d'], part['r']
        parts.append(part)
    return parts, (W, D, H)


def dedupe(text):
    """Kleine Modelle wiederholen sich gern. Doppelte Sätze entfernen, abgeschnittene Reste kappen."""
    saetze, seen = re.split(r'(?<=[.!?])\s+', text.strip()), set()
    out = []
    for s in saetze:
        k = s.lower().strip()
        if k and k not in seen:
            seen.add(k)
            out.append(s)
    if len(out) > 1 and not re.search(r'[.!?]$', out[-1]):
        out.pop()
    return ' '.join(out)


def gewicht_text(g, gewogen=False):
    """Gewicht für die Anzeige: geschätzt mit "≈", von der Waage exakt."""
    fmt = lambda v: f'{v:g}'.replace('.', ',')
    if gewogen:
        return (f'{fmt(round(g / 1000, 2))} kg' if g >= 1000 else f'{fmt(round(g))} g') + ' gewogen'
    return f'≈ {fmt(round(g / 1000, 1))} kg' if g >= 1000 else f'≈ {fmt(round(g))} g'


def build_object(spec, *, oid, modell, scan, quelle):
    for key in ('wertvoll',):
        spec[key] = dedupe(spec[key])
    spec['entsorgung'] = {k: dedupe(v) for k, v in spec['entsorgung'].items()}
    for t in spec['bauteile']:
        t['info'] = dedupe(t['info'])
    parts, (W, D, H) = build_parts(spec)
    k = spec['kreislauf']
    fmt = lambda v: f'{v:g}'.replace('.', ',')
    gewicht = spec['gewicht_g']
    return {
        'id': oid, 'name': spec['name'], 'klasse': spec['kategorie'],
        'photo': None,
        'erkennung': {
            'conf': scan.get('conf', 0.5),
            'modelle': [[c['name'], c['conf']] for c in scan.get('kandidaten', [])] or [[modell, 0.5]],
            'hinweis': 'Von der KI erstellt. Werte sind Schätzungen und noch nicht von der Werkstatt geprüft.',
        },
        'masse': f'{fmt(round(W))} × {fmt(round(D))} × {fmt(round(H, 1))} mm',
        'gewicht': gewicht_text(gewicht),
        'werte': [
            {'k': 'Rohstoffwert', 'v': spec['rohstoffwert'], 'hint': 'Schätzung der KI'},
            {'k': 'Gebrauchtwert', 'v': spec['gebrauchtwert'], 'hint': 'Schätzung der KI'},
            {'k': 'CO₂ Herstellung', 'v': spec['co2_kg'], 'hint': 'Schätzung der KI'},
        ],
        'wertvoll': spec['wertvoll'],
        'kreislauf': [
            {'t': 'Rohstoffe', 'd': k['rohstoffe']}, {'t': 'Herstellung', 'd': k['herstellung']},
            {'t': 'Nutzung', 'd': k['nutzung']}, {'t': 'Heute oft', 'd': k['heute_oft'], 'tone': 'bad'},
            {'t': 'Besser', 'd': k['besser'], 'tone': 'good'},
        ],
        'entsorgung': spec['entsorgung'],
        'quelle': quelle,
        'parts': parts,
    }
