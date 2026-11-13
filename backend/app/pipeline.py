"""Die drei KI-Schritte mit Prüfung, Wiederholung und Cache.

Reihenfolge pro Scan:
  1. Qualitätscheck (Helligkeit, Schärfe)           ohne KI
  2. Foto-Abgleich mit bekannten Fotos (dHash)       ohne KI, sofort
  3. Erkennung mit Vision-Modell                     KI, Ausgabe nach Schema
  4. Steckbrief: Cache nach Modellname, sonst KI     KI liefert Struktur, Code rechnet Geometrie
  5. Bauideen: Lagerbestand + KI, Lager-IDs im Schema erzwungen
"""
import json
import time

from . import config, db, images, llm, schemas
from .layout import build_object, slug

SYSTEM = ('Du arbeitest an einer Scan-Station in einer offenen Upcycling-Werkstatt für Schülerinnen und Schüler. '
          'Antworte auf Deutsch, in kurzen, klaren Sätzen ohne Fachjargon. Erfinde keine genauen Zahlen: '
          'Schätzungen kennzeichnest du mit "≈". Wenn du etwas nicht sicher weißt, sag es.')


class PipelineError(Exception):
    pass


# Kleine Modelle kennen die IDs nicht: Liste mit Klarnamen in den Prompt.
MATERIAL_LISTE = 'Erlaubte Material-IDs: ' + '; '.join(
    f'{mid} = {m["name"]}' for mid, m in schemas.CATALOG['materials'].items())


def _with_retry(call, validate, repair=None):
    """Ein Versuch, bei Prüffehlern ein zweiter mit der Fehlerliste als Hinweis.
    Schlägt auch der fehl, repariert repair() die Antwort deterministisch, sofern möglich."""
    fehler = None
    for _ in range(2):
        data, info = call(fehler)
        fehler = validate(data)
        if not fehler:
            return data, info
    if repair:
        return repair(data), info
    raise PipelineError('Die KI-Antwort hat die Prüfung zweimal nicht bestanden: ' + '; '.join(fehler))


# ---------------------------------------------------------------- 1–3 Scan

def scan(data_url):
    t0 = time.perf_counter()
    img = images.decode(data_url)
    q = images.quality(img)
    h = images.dhash(img)
    # Gegenstand freistellen: Die KI sieht dann nur das Objekt, nicht Tisch oder Hintergrund.
    box = images.find_object(img)
    obj_img = images.crop(img, box) if box else img

    hit = db.find_photo(h)
    if hit:
        o = db.get_object(hit[1])
        result = {
            'quelle': 'foto-abgleich', 'objekt': o['name'], 'kategorie': o['klasse'], 'conf': o['erkennung']['conf'],
            'kandidaten': [{'name': n, 'conf': c, 'object_id': o['id']} for n, c in o['erkennung']['modelle']],
            'hinweis': o['erkennung'].get('hinweis'), 'material_vermutung': [], 'sichtbarer_text': '',
            'schritte': [{'name': 'Qualität geprüft', 'ms': 0}, {'name': f'Foto-Abgleich: Treffer (Abstand {hit[0]})', 'ms': 0}],
        }
    elif config.LLM_MODE == 'mock':
        objs = db.list_objects()
        result = {
            'quelle': 'mock', 'objekt': 'Unbekannt', 'kategorie': 'Sonstiges', 'conf': 0.0,
            'kandidaten': [{'name': o['name'], 'conf': None, 'object_id': o['id']} for o in objs][:4],
            'hinweis': 'Mock-Modus: keine KI aktiv. Bitte Gegenstand auswählen.',
            'material_vermutung': [], 'sichtbarer_text': '', 'schritte': [{'name': 'Foto-Abgleich: kein Treffer', 'ms': 0}],
        }
    else:
        user = ('Was für ein Gegenstand liegt auf diesem Foto? Bewerte nur den Gegenstand selbst, '
                'nicht den Untergrund (Tisch, Boden) und nicht den Hintergrund.\n'
                '- objekt: was für ein Gegenstand es ist, als allgemeiner Begriff ohne Marke.\n'
                '- kandidaten: bis zu drei konkrete Modelle oder Produkte mit Marke, mit deiner Sicherheit (0 bis 1).\n'
                '- sichtbarer_text: abgelesener Text wie Marke oder Typenschild.\n'
                '- material_vermutung: die Hauptmaterialien, jedes nur einmal. Achte auf Glas gegenüber Kunststoff.\n'
                '- ist_gegenstand: false, wenn kein Gegenstand zu sehen ist.\n' + MATERIAL_LISTE)
        data, info = _with_retry(
            lambda f: llm.chat_json(model=config.VISION_MODEL, system=SYSTEM, user=user + (f'\nKorrigiere: {f}' if f else ''),
                                    schema=schemas.SCAN, name='scan', images=[images.to_data_url(obj_img)], max_tokens=600),
            lambda d: [] if d.get('kandidaten') else ['mindestens ein Kandidat'])
        kands = sorted(data['kandidaten'], key=lambda k: -k['sicherheit'])
        result = {
            'quelle': 'ki', 'objekt': data['objekt'], 'kategorie': data['kategorie'], 'conf': data['sicherheit'],
            'ist_gegenstand': data['ist_gegenstand'],
            'kandidaten': [{'name': k['name'], 'conf': round(k['sicherheit'], 2),
                            'object_id': db.find_alias(k['name'])} for k in kands],
            'hinweis': 'Die Sicherheit ist eine Selbsteinschätzung des Modells. Bitte prüfen.',
            'material_vermutung': list(dict.fromkeys(data['material_vermutung'])), 'sichtbarer_text': data['sichtbarer_text'],
            'schritte': [{'name': 'Qualität geprüft', 'ms': 0}, {'name': 'Foto-Abgleich: kein Treffer', 'ms': 0},
                         {'name': 'Gegenstand freigestellt' if box else 'Freistellen: ganzes Bild', 'ms': 0},
                         {'name': f'Erkennung mit {info["modell"]}', 'ms': info['ms']}],
        }
    result['qualitaet'] = q
    result['bbox'] = [round(v, 3) for v in box] if box else None
    result['dauer_ms'] = round((time.perf_counter() - t0) * 1000)
    result['scan_id'] = db.save_scan(result, h, img, obj_img if box else None)
    return result


# ---------------------------------------------------------------- 4 Steckbrief

def _check_steckbrief(d):
    f = []
    m = d.get('masse_mm', {})
    if min(m.get('breite', 0), m.get('tiefe', 0), m.get('hoehe', 0)) <= 0:
        f.append('alle Maße müssen größer als 0 sein')
    namen = [t['name'] for t in d.get('bauteile', [])]
    if len(set(namen)) < len(namen):
        f.append('jedes Bauteil braucht einen eigenen Namen')
    teile = d.get('bauteile', [])
    if not any(t['breite_anteil'] > 0.8 and t['tiefe_anteil'] > 0.8 for t in teile):
        f.append('mindestens ein Bauteil muss die ganze Grundfläche einnehmen (Gehäuse, Körper oder Platte)')
    ebenen = {t['ebene'] for t in teile}
    if len(teile) >= 3 and len(ebenen) < 3:
        f.append('verteile die Bauteile auf mindestens 3 Ebenen: Unterteil unten, Innenteile in der Mitte, Deckel oben')
    for t in teile:
        if sum(m['anteil'] for m in t['materialien']) < 50:
            f.append(f'Materialanteile von {t["name"]} müssen zusammen etwa 100 ergeben')
    return f


def steckbrief(scan_id, modell, objekt=None):
    t0 = time.perf_counter()
    cached = db.find_alias(modell) if modell else None
    if cached:
        return {'object': db.get_object(cached), 'quelle': 'cache', 'dauer_ms': 0}
    if config.LLM_MODE == 'mock':
        raise PipelineError('Mock-Modus: Für unbekannte Gegenstände ist kein Modell aktiv.')

    row, img = db.get_scan(scan_id) if scan_id else (None, None)
    scan_res = row['result'] if row else {}
    name = modell or scan_res.get('objekt') or objekt or 'Gegenstand'
    user = (f'Gegenstand: {name}\n'
            f'Allgemein: {scan_res.get("objekt") or objekt or "unbekannt"}\n'
            f'Sichtbarer Text auf dem Foto: {scan_res.get("sichtbarer_text") or "keiner"}\n'
            'Erstelle einen Material-Steckbrief für diesen Gegenstand. Das Feld name ist nur der Gegenstand, ohne Zusätze.\n'
            'Zerlege den Gegenstand gedanklich in 4 bis 10 Bauteile, wie bei einer Explosionszeichnung:\n'
            '- ebene 0 ist ganz unten, höhere Ebenen liegen darüber. Teile auf derselben Ebene liegen nebeneinander.\n'
            '- Teile das Gehäuse in Unterteil (ebene 0) und Deckel oder Oberteil (oberste Ebene). '
            'Innenteile wie Akku, Platine, Magnete liegen auf den Ebenen dazwischen.\n'
            '- form: "platte" für flache, durchgehende Schichten, "block" für Kästen, "rund" für Zylinder.\n'
            '- breite_anteil und tiefe_anteil: Anteil an der Grundfläche (1 = ganze Breite).\n'
            '- materialien nur aus der erlaubten Liste, anteil in Prozent.\n'
            '- masse_mm in Millimetern für den ganzen Gegenstand, liegend wie auf dem Foto.\n'
            + MATERIAL_LISTE + '\n'
            'Nenne bei Entsorgung, wohin der Gegenstand in Deutschland gehört. Geräte mit Akku nie selbst öffnen oder den Akku ausbauen, '
            'sondern als Elektroaltgerät abgeben. Schreibe jede Warnung nur einmal. '
            'rohstoffwert, gebrauchtwert und co2_kg als kurze Schätzung mit "≈".')
    imgs = [images.to_data_url(img)] if img else []
    data, info = _with_retry(
        lambda f: llm.chat_json(model=config.VISION_MODEL if imgs else config.TEXT_MODEL, system=SYSTEM,
                                user=user + (f'\nDeine letzte Antwort hatte Fehler, korrigiere: {f}' if f else ''),
                                schema=schemas.STECKBRIEF, name='steckbrief', images=imgs, max_tokens=3500),
        _check_steckbrief)

    oid = slug(name)
    if db.get_object(oid):
        oid = f'{oid}-{int(time.time()) % 100000}'
    quelle = f'KI-Entwurf mit {info["modell"]}, noch nicht von der Werkstatt geprüft. Werte sind Schätzungen.'
    obj = build_object(data, oid=oid, modell=name, scan=scan_res, quelle=quelle)
    db.put_object(obj, 'entwurf', info['modell'], aliases=[name], photo_hash=row['hash'] if row else None)
    obj['status'] = 'entwurf'
    return {'object': obj, 'quelle': 'ki', 'dauer_ms': round((time.perf_counter() - t0) * 1000), 'llm_ms': info['ms']}


# ---------------------------------------------------------------- 5 Bauideen

WERKZEUG = ('Säge, Akkuschrauber, Bohrer, Cutter, Heißklebepistole, Lötkolben, Abisolierzange, Schleifpapier, '
            'Fahrrad-Schredder für Kunststoff, Spritzgussmaschine mit Karabinerform, Plattenpresse')


def ideen(object_id, neu=False):
    obj = db.get_object(object_id)
    if not obj:
        raise PipelineError('Unbekanntes Objekt')
    if obj.get('projekte') and not neu:
        return {'projekte': obj['projekte'], 'quelle': 'cache', 'dauer_ms': 0}
    if config.LLM_MODE == 'mock':
        raise PipelineError('Mock-Modus: Bauideen brauchen ein aktives Modell.')

    t0 = time.perf_counter()
    inv = [i for i in db.inventory() if i['menge'] > 0 and i['object_id'] != object_id]
    bestand = {i['id']: i for i in inv}
    beispiele = [p for f in sorted((config.SEED / 'objects').glob('*.json'))
                 for p in json.loads(f.read_text(encoding='utf-8')).get('projekte', [])][:2]
    teile = '; '.join(f"{p['name']} ({', '.join(schemas.CATALOG['materials'][m]['name'] for m, _ in p['materials'])})"
                      for p in obj['parts'])
    user = (f'Ein Schüler hat gerade abgegeben: {obj["name"]}. Bauteile: {teile}.\n'
            f'Lager der Werkstatt (id: Name, Bestand): '
            + '; '.join(f"{i['id']}: {i['name']}, {i['menge']:g} {i['einheit']}" for i in inv) + '\n'
            f'Werkzeug in der Werkstatt: {WERKZEUG}.\n'
            'Schlage genau drei unterschiedliche Upcycling-Projekte vor, die Schüler in einer Werkstattstunde bauen können. '
            'Jedes Projekt verwendet ein Teil des neuen Gegenstands (neu_teil) und kann Material aus dem Lager nutzen. '
            'Keine Projekte, bei denen Akkus geöffnet werden oder an Netzspannung gearbeitet wird. '
            'Ein Projekt soll leicht sein (stufe 1). lernziel: was man über Material oder Kreislauf lernt.\n'
            f'Beispiele für Stil und Umfang: {json.dumps(beispiele, ensure_ascii=False)}')

    teil_woerter = {w for p in obj['parts'] for w in p['name'].lower().split() if len(w) > 3} | {
        w for w in obj['name'].lower().split() if len(w) > 3}

    def check(d):
        f = []
        titel = [p['titel'] for p in d['projekte']]
        if len(set(titel)) < 3:
            f.append('drei verschiedene Projekte')
        for p in d['projekte']:
            neu = p['neu_teil'].lower()
            if neu in bestand or not any(w in neu for w in teil_woerter):
                f.append(f'"{p["titel"]}": neu_teil muss ein Bauteil des abgegebenen Gegenstands sein '
                         f'({", ".join(x["name"] for x in obj["parts"])}), kein Lagerartikel')
            for u in p['lager']:
                if u['id'] in bestand and u['menge'] > min(10, bestand[u['id']]['menge']):
                    f.append(f"{u['id']}: höchstens {min(10, bestand[u['id']]['menge']):g} Stück pro Projekt")
        return f

    def repair(d):
        # Letzter Ausweg statt Fehlermeldung: Mengen begrenzen, unpassendes neu_teil durch den ganzen Gegenstand ersetzen.
        for p in d['projekte']:
            neu = p['neu_teil'].lower()
            if neu in bestand or not any(w in neu for w in teil_woerter):
                p['neu_teil'] = f'{obj["name"]} (ganzer Gegenstand)'
            for u in p['lager']:
                if u['id'] in bestand:
                    u['menge'] = max(1, min(u['menge'], 10, int(bestand[u['id']]['menge'])))
        return d

    schema = schemas.projekte_schema(list(bestand) or ['keins'])
    data, info = _with_retry(
        lambda f: llm.chat_json(model=config.TEXT_MODEL, system=SYSTEM, user=user + (f'\nKorrigiere: {f}' if f else ''),
                                schema=schema, name='projekte', max_tokens=2500, temperature=0.5),
        check, repair)
    projekte = []
    for p in data['projekte']:
        lager = {}
        for u in p['lager']:
            if u['id'] in bestand:
                lager[u['id']] = lager.get(u['id'], 0) + u['menge']
        projekte.append({
            'titel': p['titel'], 'kurz': p['kurz'], 'stufe': p['stufe'], 'dauer': p['dauer'], 'lernziel': p['lernziel'],
            'nutzt': [{'neu': True, 'name': p['neu_teil']}] + [{'inv': k, 'menge': v} for k, v in lager.items()],
            'werkzeug': p['werkzeug'], 'schritte': p['schritte'],
        })
    obj['projekte'] = projekte
    status = obj.pop('status', 'entwurf')
    db.put_object(obj, status, info['modell'])
    return {'projekte': projekte, 'quelle': 'ki', 'dauer_ms': round((time.perf_counter() - t0) * 1000)}
