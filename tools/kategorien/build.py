"""Erzeugt die 3D-Modelle der Kategorien (Explosionszeichnungen) für Backend und Frontend.

Eingaben
  data/classifier.json            Objekte, Komponenten, Materialien (Team-Datenbank)
  tools/kategorien/kategorien.csv deutscher Name, Entsorgungsweg, Maße (mm), Gewicht (g), Grundform
  tools/kategorien/modelle/       <id>.json mit handgebauten, detaillierten "parts" (siehe docs/3d-modelle.md).
                                  Ohne Datei entsteht ein einfacher Platzhalter aus den Komponenten.

Ausgabe
  backend/seed/kategorien/<id>.json   ein Objekt im Format von docs/objekt-schema.md
  backend/seed/kategorien/index.json  Übersicht

Aufruf (Projektordner):  python tools/kategorien/build.py
"""
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rohstoffe  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'tools' / 'kategorien'
OUT = ROOT / 'backend' / 'seed' / 'kategorien'

# Team-Materialien (classifier.json) -> Materialien des Katalogs (js/data/catalog.js) mit Anteilen in %
MATERIAL = {
    'pet': [['pet', 100]], 'hdpe': [['hdpe', 100]], 'pvc': [['pvc', 100]], 'ldpe': [['ldpe', 100]], 'pp': [['pp', 100]],
    'ps': [['ps', 100]], 'eps': [['ps', 100]], 'abs': [['pcabs', 100]], 'pc': [['pcabs', 100]],
    'multilayer_plastic': [['verbundfolie', 100]], 'silicone': [['gummi', 100]], 'rubber': [['gummi', 100]],
    'pu_foam': [['schaum', 100]], 'eva_foam': [['schaum', 100]], 'polyurethane': [['schaum', 100]],
    'nylon': [['nylon', 100]], 'polyester': [['polyester', 100]], 'cotton': [['baumwolle', 100]], 'wool': [['wolle', 100]],
    'leather': [['leder', 100]], 'wood': [['holz', 100]], 'cork': [['kork', 100]], 'paper': [['papier', 100]],
    'cardboard': [['papier', 100]], 'composite_carton': [['verbund', 100]],
    'paper_plastic_composite': [['papier', 85], ['ldpe', 15]], 'aluminium': [['alu', 100]], 'steel': [['stahl', 100]],
    'copper': [['kupfer', 100]], 'nickel_chrome': [['nichrom', 100]], 'glass': [['behaelterglas', 100]],
    'special_glass': [['glas', 100]], 'ceramic': [['keramik', 100]], 'phenolic_resin': [['phenolharz', 100]],
    'paraffin_wax': [['wachs', 100]], 'graphite_clay': [['grafitton', 100]],
    'pcb': [['fr4', 55], ['kupfer', 20], ['chip', 15], ['lot', 10]],
    'mixed_electronics': [['chip', 30], ['kupfer', 30], ['pcabs', 25], ['stahl', 15]],
    'li_ion': [['lco', 40], ['graphit', 20], ['elektrolyt', 15], ['alu', 15], ['kupfer', 10]],
    'alkaline': [['zinkmangan', 80], ['stahl', 20]], 'coin_cell': [['knopfzelle', 100]],
}

KLASSE = {
    'EK': 'Elektroschrott · Kleingerät', 'EB': 'Elektroschrott · Bildschirmgerät', 'EG': 'Elektroschrott · Großgerät',
    'BAT': 'Batterien', 'LM': 'Leuchtmittel', 'VK': 'Verpackung · Gelbe Tonne', 'VG': 'Verpackung · Glas',
    'VP': 'Verpackung · Papier', 'PF': 'Pfandverpackung', 'TX': 'Textilien und Schuhe', 'HO': 'Holz',
    'RM': 'Restmüll', 'WM': 'Metall · Wertstoffhof', 'WH': 'Wertstoffhof', 'BIO': 'Bioabfall',
}

# Entsorgung in Deutschland (regional können Details abweichen). Grundlagen: ElektroG, BattG, VerpackG.
ENTSORGUNG = {
    'EK': ('Recyclinghof oder Rücknahme im Handel. Kleine Elektrogeräte bis 25 cm nehmen auch große Supermärkte kostenlos zurück.',
           'Nicht in Restmüll oder Gelbe Tonne', 'Kabel und Stecker dranlassen.'),
    'EB': ('Recyclinghof (Bildschirmgeräte) oder Rücknahme im Elektrohandel.', 'Nicht in Restmüll oder Sperrmüll',
           'Bildschirm nicht zerbrechen. Persönliche Daten vorher löschen.'),
    'EG': ('Recyclinghof oder Abholung als Elektro-Großgerät.', 'Nicht in Restmüll oder Sperrmüll', 'Nicht selbst ausschlachten.'),
    'BAT': ('Batterie-Sammelbox im Handel oder Recyclinghof.', 'Nicht in Restmüll oder Gelbe Tonne',
            'Pole von Lithium-Batterien mit Klebeband abkleben.'),
    'LM': ('Recyclinghof oder Sammelbox im Handel.', 'Nicht in Restmüll oder Altglas', 'Nicht zerbrechen.'),
    'VK': ('Gelbe Tonne oder Gelber Sack.', 'Nicht in Restmüll oder Altpapier',
           'Restentleert reicht, nicht ausspülen. Teile aus verschiedenen Materialien trennen.'),
    'VG': ('Altglascontainer, nach Farben getrennt (weiß, grün, braun; andere Farben zu Grün).',
           'Keine Trinkgläser, Keramik oder Glühbirnen', 'Deckel abnehmen und in die Gelbe Tonne geben.'),
    'VP': ('Papiertonne oder Altpapiercontainer.', 'Nicht in Restmüll, wenn sauber',
           'Kartons flach falten. Stark verschmutzte Teile in den Restmüll.'),
    'PF': ('Pfandautomat im Handel.', 'Nicht in die Gelbe Tonne, sonst ist das Pfand weg', 'Pfandlogo nicht abreißen.'),
    'TX': ('Altkleidercontainer oder Recyclinghof, sauber und in einem Beutel.', 'Tragbares nicht in den Restmüll',
           'Schuhe paarweise zusammenbinden.'),
    'HO': ('Recyclinghof (Altholz). Kleine Holzteile in den Restmüll.', 'Nicht in die Biotonne', 'Lackiertes Holz ist Altholz, kein Brennholz.'),
    'RM': ('Restmüll.', 'Nicht in die Gelbe Tonne: keine Verpackung', 'Gut Erhaltenes lieber verschenken oder in der Werkstatt abgeben.'),
    'WM': ('Recyclinghof (Altmetall).', 'Nicht in die Gelbe Tonne: keine Verpackung', 'Scharfe Klingen vorher einwickeln.'),
    'WH': ('Recyclinghof.', 'Nicht in die Gelbe Tonne', 'Reste von Farben, Klebern oder Chemikalien gehören zur Schadstoffsammlung.'),
    'BIO': ('Biotonne.', 'Nicht in die Gelbe Tonne', 'Metallklammer und Faden vorher entfernen.'),
}

KREISLAUF = {
    'elektro': ['Erze für Kupfer, Gold, Zinn und Seltene Erden aus vielen Ländern', 'Platinen und Akkus in Asien, sehr energieintensiv',
                'Oft nur wenige Jahre', 'Liegt in der Schublade oder landet im Restmüll', 'Reparieren, weitergeben, dann Elektro-Sammlung'],
    'verpackung': ['Erdöl, Holz, Bauxit oder Quarzsand', 'Wenige Sekunden Formgebung in der Fabrik', 'Oft nur Minuten bis Tage',
                   'Falsch getrennt und dann verbrannt', 'Richtig trennen oder in der Werkstatt neu formen'],
    'alltag': ['Erdöl, Metallerze, Holz oder Baumwolle', 'Industrielle Fertigung', 'Jahre, wenn man es pflegt',
               'Landet im Restmüll und wird verbrannt', 'Reparieren, weitergeben oder Teile in der Werkstatt nutzen'],
}
WERT = {'elektro': 'Elektrogeräte enthalten Metalle wie Kupfer, Gold und Kobalt, die sich zurückgewinnen lassen. Noch mehr spart, wer sie repariert und weiternutzt.',
        'verpackung': 'Sortenrein getrennt wird aus Verpackung wieder Rohstoff. Jede richtig getrennte Verpackung spart neues Material.',
        'alltag': 'Je länger ein Gegenstand genutzt wird, desto weniger Rohstoffe und Energie braucht es für Ersatz.'}

ROLLEN = [  # Reihenfolge zählt: erste passende Rolle gewinnt
    ('seite', r'label|sleeve|strap|cable|cord|lace|handle|hose|string|band|tag|antenna|_net|mesh|rings|grip_tape|booklet|tape$|packing_tape'),
    ('anzeige', r'display|screen|lcd|platform|watch_glass|e_ink|frame_glass|front_panel|turntable|pot_lid_glass'),
    ('oben', r'cap|lid|cork|stopper|nozzle|valve|pump|trigger|_tap|button|wheel|tip|clip|knob|roller|keycap|keypad|thumbstick|'
             r'shade|cover_film|window_film|insert|visor|cushion|ear_tips|foil|diffuser|grille|guard|rose|propeller|nib'),
    ('innen', r'sim_|battery|cell|circuit|board|motor|speaker|driver|led_|thermostat|heat|element|magnetron|fan|chip|movement|'
              r'load_cell|buzzer|switch|filament|refill|ink|core|wick|bullet|drive|supply|adapter|camera|memory|solar|jack|'
              r'backlight|bladder|fill|padding|sponge|_pad|pieces|axle|bearing|cpu|cooler|bristles|beaters|blade|spring|'
              r'mechanism|gearbox|chuck|lens|seal|bead_wire|casing_fabric|lining|ball|bulb_|tube_valve|spiral|staple'),
]
GEWICHT = {'koerper': 5.0, 'anzeige': 2.0, 'oben': 0.6, 'seite': 0.6, 'innen': 1.2}
SCHWER = r'battery|cell|motor|magnetron|transformer|gearbox|blade|heat|cavity|soleplate|plates|body|glass'
LANG = r'cable|cord|hose|lace|strap|string|band|antenna|handle'


def rolle(cid):
    for name, muster in ROLLEN:
        if re.search(muster, cid):
            return name
    return 'koerper'


def baue_teile(obj_id, comps, W, D, H, form):
    rund = form == 'rund'
    hoch = H > 1.3 * max(W, D)                 # stehender Behälter (Flasche, Dose, Lampe)
    gap = max(12.0, 0.2 * (W + D), 0.12 * H)
    gruppen = {r: [c for c in comps if c['rolle'] == r] for r in ('koerper', 'innen', 'anzeige', 'oben', 'seite')}
    if not gruppen['koerper']:                 # ohne Gehäuse: erstes Nicht-Anbauteil trägt das Objekt
        kandidat = next((c for c in comps if c['rolle'] != 'seite'), comps[0])
        kandidat['rolle'] = 'koerper'
        for g in gruppen.values():
            if kandidat in g:
                g.remove(kandidat)
        gruppen['koerper'] = [kandidat]

    teile, ebene = [], 0
    oben_z = 0.0

    def teil(c, name, shape, x, y, w, d, h, z, ex, anteil=1.0):
        return {'comp': c, 'name': name, 'shape': shape, 'x': x, 'y': y, 'w': w, 'd': d, 'h': max(h, 0.3), 'z': z,
                'explode': ex, 'anteil': anteil}

    footprint = 'cyl' if rund else 'box'
    # Mehrere Gehäuseteile von unten nach oben: Sohle, Boden, Rückseite zuerst, Oberteil und Front zuletzt.
    lage = lambda c: (0 if re.search(r'outsole|base|bottom|back|stand|cavity|tray|deck|disc_body', c['id'])
                      else 1 if re.search(r'midsole|sole|frame|casing', c['id'])
                      else 3 if re.search(r'upper|top|front|cover|shell|case', c['id']) else 2)
    gruppen['koerper'].sort(key=lage)
    koerper = gruppen['koerper']
    innen = gruppen['innen']
    teilen = len(koerper) == 1 and innen and not hoch
    if teilen:                                  # ein Gehäuse mit Innenleben: in Unter- und Oberteil teilen
        k = koerper[0]
        teile.append(teil(k, f'{k["name"]} (Unterteil)', footprint, 0, 0, W, D, 0.6 * H, 0, [0, 0, 0], 0.7))
        oben_z = 0.6 * H
    else:
        hk = (0.85 if (gruppen['oben'] and hoch) else 0.8 if gruppen['anzeige'] else 1.0) * H / max(1, len(koerper))
        for i, k in enumerate(koerper):
            teile.append(teil(k, k['name'], footprint, 0, 0, W, D, hk, i * hk, [0, 0, ebene * gap]))
            ebene += 1
        oben_z = hk * len(koerper)
        ebene -= 1

    # Innenteile: nebeneinander im Gehäuse, in der Explosion je eine eigene Ebene
    plaetze = [(0.5, 0.5)] if len(innen) == 1 else [(0.25, 0.3), (0.75, 0.3), (0.25, 0.75), (0.75, 0.75), (0.5, 0.5)]
    for i, c in enumerate(innen):
        fx, fy = plaetze[i % len(plaetze)]
        s = 0.7 if len(innen) == 1 else 0.42
        w, d = W * s, D * s
        shape = 'cyl' if re.search(r'motor|speaker|driver|fan|cell|coil|lens|magnetron|bladder|ball|chuck|bulb_|wheel', c['id']) else 'box'
        if shape == 'cyl':
            w = d = min(w, d)
        z_in = 0.12 * H if teilen else oben_z * 0.2
        ebene += 1
        teile.append(teil(c, c['name'], shape, fx * W - w / 2, fy * D - d / 2, w, d, min(0.35 * H, 0.45 * oben_z or H), z_in,
                          [0, 0, ebene * gap]))
    if teilen:
        k = koerper[0]
        ebene += 1
        teile.append(teil(k, f'{k["name"]} (Oberteil)', footprint, 0, 0, W, D, 0.2 * H, 0.6 * H, [0, 0, ebene * gap], 0.3))
        oben_z = 0.8 * H

    for c in gruppen['anzeige']:                # Display, Glas, Frontplatte: dünne Platte obenauf
        ebene += 1
        h = max(0.5, 0.06 * H)
        teile.append(teil(c, c['name'], footprint, W * 0.02, D * 0.02, W * 0.96, D * 0.96, h, oben_z, [0, 0, ebene * gap]))
        oben_z += h

    for i, c in enumerate(gruppen['oben']):     # Deckel, Kappen, Tasten: auf der Oberseite
        ebene += 1
        flaechig = re.search(r'keycap|keypad|cushion|shade|foil|film|insert|visor|lid|grille|guard|diffuser', c['id']) and not hoch
        if flaechig:
            w, d, x, y, h, shape = W * 0.9, D * 0.9, W * 0.05, D * 0.05, max(0.5, 0.08 * H), footprint
        else:
            s = 0.45 if hoch else 0.22
            w = d = min(W, D) * s
            x, y = (W - w) / 2 + (i % 2) * W * 0.2, (D - d) / 2
            h = max(1.0, (0.12 if hoch else 0.15) * H)
            shape = 'cyl' if (rund or re.search(r'cap|cork|stopper|knob|wheel|button|nozzle|roller', c['id'])) else 'box'
        teile.append(teil(c, c['name'], shape, x, y, w, d, h, oben_z, [0, 0, ebene * gap]))

    # Explosion: Jedes Teil schwebt mit Abstand über dem darunterliegenden, egal wie hoch dieses ist.
    # (teile ist von unten nach oben aufgebaut; Innenteile auf gleicher Höhe bekommen je eine eigene Stufe.)
    oberkante = None
    for t in teile:
        if oberkante is None:
            t['explode'] = [0, 0, 0]
        else:
            t['explode'] = [0, 0, round(max(0.0, oberkante + gap - t['z']), 1)]
        oberkante = t['z'] + t['explode'][2] + t['h']

    for i, c in enumerate(gruppen['seite']):    # Etiketten, Kabel, Griffe: seitlich, explodieren zur Seite
        if re.search(LANG, c['id']):
            w, d, h = max(3.0, 0.05 * W), D * 0.9, max(3.0, 0.08 * H)
            x, y, z = W * 1.06 + i * w * 2, D * 0.05, 0.1 * H
        else:
            w, d, h = max(1.0, 0.03 * W), D * 0.6, (0.55 if hoch else 0.6) * H
            x, y, z = W * 1.01 + i * 3, D * 0.2, 0.2 * H
        teile.append(teil(c, c['name'], 'box', x, y, w, d, h, z, [0.35 * W + 15 + i * 0.15 * W, 0, 0.3 * gap]))
    return teile


def main():
    cls = json.loads((ROOT / 'data' / 'classifier.json').read_text(encoding='utf-8'))
    katalog = json.loads((ROOT / 'backend' / 'seed' / 'catalog.json').read_text(encoding='utf-8'))
    fehlend = {m for m in cls['materials'] if m not in MATERIAL}
    assert not fehlend, f'Materialien ohne Zuordnung: {fehlend}'
    assert all(mid in katalog['materials'] for v in MATERIAL.values() for mid, _ in v), 'Katalog-ID fehlt'

    zeilen = {r['id']: r for r in csv.DictReader((SRC / 'kategorien.csv').open(encoding='utf-8'), delimiter=';')}
    ohne = set(cls['objects']) - set(zeilen)
    assert not ohne, f'Kategorien ohne Maße in kategorien.csv: {sorted(ohne)}'

    OUT.mkdir(parents=True, exist_ok=True)
    index = []
    for oid, o in cls['objects'].items():
        z = zeilen[oid]
        W, D, H, gramm = float(z['breite']), float(z['tiefe']), float(z['hoehe']), float(z['gramm'])
        comps = [{'id': cid, **cls['components'][cid], 'rolle': rolle(cid)} for cid in o['components']]
        modell = SRC / 'modelle' / f'{oid}.json'
        platzhalter = not modell.exists()
        if not platzhalter:
            parts = json.loads(modell.read_text(encoding='utf-8'))['parts']
        else:
            roh = baue_teile(oid, comps, W, D, H, z['form'])
            gew = [GEWICHT[t['comp']['rolle']] * (2 if re.search(SCHWER, t['comp']['id']) else 1) * t['anteil'] for t in roh]
            parts, ids = [], set()
            for t, g in zip(roh, gew):
                pid = t['comp']['id'] + ('_ober' if '(Oberteil)' in t['name'] else '')
                while pid in ids:
                    pid += '_2'
                ids.add(pid)
                p = {'id': pid, 'component_id': t['comp']['id'], 'name': t['name'], 'short': t['name'][:18],
                     'shape': t['shape'], 'x': round(t['x'], 1), 'y': round(t['y'], 1), 'w': round(t['w'], 1),
                     'd': round(t['d'], 1), 'h': round(t['h'], 2), 'z': round(t['z'], 2), 'r': round(min(t['w'], t['d']) * 0.12, 1),
                     'explode': [round(v, 1) for v in t['explode']], 'mass': round(gramm * g / sum(gew), 2),
                     'materials': MATERIAL[t['comp']['material_id']], 'material_id': t['comp']['material_id'],
                     'info': t['comp']['hint']}
                if p['shape'] == 'cyl':
                    del p['d'], p['r']
                parts.append(p)
            # Oberste Teile zuerst nummerieren, wie bei den handgebauten Modellen
            parts.sort(key=lambda p: -(p['z'] + p['explode'][2]))

        rs = rohstoffe.berechne(oid, parts)
        code = z['entsorgung']
        art = 'elektro' if code in ('EK', 'EB', 'EG', 'BAT', 'LM') else 'verpackung' if code in ('VK', 'VG', 'VP', 'PF') else 'alltag'
        wo, nicht, warnung = ENTSORGUNG[code]
        mats = {c['material_id'] for c in comps}
        if mats & {'li_ion', 'coin_cell', 'alkaline'} and code in ('EK', 'EB', 'EG'):
            warnung = 'Akku oder Batterie nicht beschädigen. Wenn möglich herausnehmen und getrennt abgeben, fest verbaute Akkus drinlassen.'
        if oid == 'compact_fluorescent_lamp':
            warnung = 'Enthält etwas Quecksilber: nicht zerbrechen.'

        fmt = lambda v: f'{v:g}'.replace('.', ',')
        obj = {
            'id': oid, 'name': z['name'], 'name_en': o['name'], 'klasse': KLASSE[code], 'kategorie': True,
            'platzhalter': platzhalter,
            'photo': None,
            'erkennung': {'conf': 1.0, 'modelle': [[z['name'], 1.0]], 'hinweis': 'Kategorie-Modell, kein bestimmtes Produkt.'},
            'masse': f'{fmt(W)} × {fmt(D)} × {fmt(H)} mm',
            'gewicht': f'≈ {fmt(round(gramm / 1000, 1))} kg' if gramm >= 1000 else f'≈ {fmt(gramm)} g',
            'werte': rohstoffe.werte(rs),
            'rohstoffe': rs,
            'wertvoll': WERT[art],
            'kreislauf': [{'t': t, 'd': d, **({'tone': tone} if tone else {})}
                          for (t, tone), d in zip([('Rohstoffe', None), ('Herstellung', None), ('Nutzung', None),
                                                   ('Heute oft', 'bad'), ('Besser', 'good')], KREISLAUF[art])],
            'entsorgung': {'wo': wo, 'nicht': nicht, 'warnung': warnung},
            'quelle': ('Bauteile und Materialien: data/classifier.json. Maße und Gewicht: typische Werte (Schätzung). '
                       + ('Geometrie: automatischer Platzhalter. ' if platzhalter else 'Geometrie: handgebautes Modell. ')
                       + 'Metallgehalte: Öko-Institut 2012. CO2: Idemat 2026. Preise: Westmetall ' + rs['preisstand'] + '.'),
            'parts': parts,
        }
        (OUT / f'{oid}.json').write_text(json.dumps(obj, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        index.append({'id': oid, 'name': z['name'], 'name_en': o['name'], 'klasse': obj['klasse'], 'teile': len(parts),
                      'platzhalter': platzhalter})
    (OUT / 'index.json').write_text(json.dumps(index, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    fertig = sum(not i['platzhalter'] for i in index)
    print(f'{len(index)} Kategorie-Modelle geschrieben nach {OUT.relative_to(ROOT)} ({fertig} handgebaut, {len(index) - fertig} Platzhalter)')


if __name__ == '__main__':
    main()
