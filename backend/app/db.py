"""SQLite-Speicher für Objekte (Cache), Lager, Scans und Buchungen. Eine Datei, kein Server."""
import json
import re
import sqlite3
import threading
import time

from PIL import Image

from . import config, images

_lock = threading.RLock()  # Hintergrund-Jobs greifen parallel zu: jeder Zugriff geht durch die Sperre
_conn = None

SCHEMA = """
CREATE TABLE IF NOT EXISTS objects (id TEXT PRIMARY KEY, status TEXT, data TEXT, modell TEXT, created REAL);
CREATE TABLE IF NOT EXISTS aliases (key TEXT PRIMARY KEY, object_id TEXT);
CREATE TABLE IF NOT EXISTS photo_hashes (hash TEXT, object_id TEXT);
CREATE TABLE IF NOT EXISTS inventory (id TEXT PRIMARY KEY, name TEXT, fach TEXT, menge REAL, einheit TEXT,
                                      cls TEXT, object_id TEXT, nr INTEGER, created REAL);
CREATE TABLE IF NOT EXISTS scans (id INTEGER PRIMARY KEY AUTOINCREMENT, created REAL, result TEXT, hash TEXT);
CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, created REAL, object_id TEXT, data TEXT);
"""


def key(text):
    return re.sub(r'[^a-z0-9]', '', (text or '').lower())


def conn():
    global _conn
    if _conn is None:
        config.DATA.mkdir(parents=True, exist_ok=True)
        (config.DATA / 'scans').mkdir(exist_ok=True)
        _conn = sqlite3.connect(config.DATA / 'station.db', check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.executescript(SCHEMA)
        if not _conn.execute('SELECT 1 FROM objects LIMIT 1').fetchone():
            _seed(_conn)
        _seed_kategorien(_conn)
    return _conn


def _seed_kategorien(c):
    """Kategorie-Modelle (tools/kategorien/build.py) bei jedem Start nachtragen und aktualisieren.
    Ersetzt Demo-Objekte gleicher ID (smartphone, laptop), behält deren Bauideen. KI-Entwürfe bleiben unberührt."""
    ordner = config.SEED / 'kategorien'
    if not ordner.exists():
        return
    for f in sorted(ordner.glob('*.json')):
        if f.name == 'index.json':
            continue
        o = json.loads(f.read_text(encoding='utf-8'))
        row = c.execute('SELECT status, data FROM objects WHERE id = ?', (o['id'],)).fetchone()
        if row and row['status'] == 'entwurf':
            continue
        if row and not o.get('projekte'):        # Bauideen eines älteren Objekts gleicher ID behalten
            alt = json.loads(row['data']).get('projekte')
            if alt:
                o['projekte'] = alt
        _put_object(c, o, 'kategorie', 'kategorie')
        for n in (o['name'], o.get('name_en'), o['id']):
            c.execute('INSERT OR IGNORE INTO aliases VALUES (?, ?)', (key(n), o['id']))
    c.commit()


def _seed(c):
    """Erster Start: geprüfte Demo-Objekte, Lagerbestand und Foto-Hashes der Beispielfotos."""
    for f in sorted((config.SEED / 'objects').glob('*.json')):
        o = json.loads(f.read_text(encoding='utf-8'))
        _put_object(c, o, 'geprueft', 'seed')
        # Nur konkrete Namen als Alias, keine Gattung wie "Flasche": sonst falsche Cache-Treffer.
        names = [o['name']] + [m for m, _ in o['erkennung']['modelle']]
        for n in names:
            c.execute('INSERT OR IGNORE INTO aliases VALUES (?, ?)', (key(n), o['id']))
        photo = config.ROOT / o['photo']
        if photo.exists():
            c.execute('INSERT INTO photo_hashes VALUES (?, ?)', (images.dhash(Image.open(photo)), o['id']))
    inv = json.loads((config.SEED / 'inventory.json').read_text(encoding='utf-8'))
    for i, it in enumerate(inv):
        c.execute('INSERT INTO inventory VALUES (?,?,?,?,?,?,?,?,?)',
                  (it['id'], it['name'], it['fach'], it['menge'], it['einheit'], it['cls'], None, 400 + i, time.time()))
    c.commit()


def _put_object(c, o, status, modell):
    c.execute('INSERT OR REPLACE INTO objects VALUES (?, ?, ?, ?, ?)',
              (o['id'], status, json.dumps(o, ensure_ascii=False), modell, time.time()))


def _all(sql, args=()):
    with _lock:
        return conn().execute(sql, args).fetchall()


def _one(sql, args=()):
    with _lock:
        return conn().execute(sql, args).fetchone()


def put_object(o, status, modell, aliases=(), photo_hash=None):
    with _lock:
        c = conn()
        _put_object(c, o, status, modell)
        for a in aliases:
            if key(a):
                c.execute('INSERT OR REPLACE INTO aliases VALUES (?, ?)', (key(a), o['id']))
        if photo_hash:
            c.execute('INSERT INTO photo_hashes VALUES (?, ?)', (photo_hash, o['id']))
        c.commit()


def get_object(oid):
    row = _one('SELECT * FROM objects WHERE id = ?', (oid,))
    if not row:
        return None
    o = json.loads(row['data'])
    o['status'] = row['status']
    return o


def list_objects(status=None):
    q = 'SELECT id, status, modell, created, json_extract(data, "$.name") AS name FROM objects'
    rows = _all(q + (' WHERE status = ?' if status else '') + ' ORDER BY created DESC', (status,) if status else ())
    return [dict(r) for r in rows]


def delete_object(oid):
    """KI-Entwurf verwerfen: Objekt, Aliase und Foto-Hashes entfernen, damit neu erzeugt wird."""
    with _lock:
        c = conn()
        for table in ('objects', 'aliases', 'photo_hashes'):
            col = 'id' if table == 'objects' else 'object_id'
            c.execute(f'DELETE FROM {table} WHERE {col} = ?', (oid,))
        c.commit()


def set_status(oid, status):
    with _lock:
        conn().execute('UPDATE objects SET status = ? WHERE id = ?', (status, oid))
        conn().commit()


def find_alias(*names):
    for n in names:
        row = _one('SELECT object_id FROM aliases WHERE key = ?', (key(n),))
        if row:
            return row['object_id']
    return None


def find_photo(h):
    best = None
    for row in _all('SELECT hash, object_id FROM photo_hashes'):
        d = images.hamming(h, row['hash'])
        if best is None or d < best[0]:
            best = (d, row['object_id'])
    return best if best and best[0] <= config.HASH_THRESHOLD else None


def save_scan(result, h, img, crop=None):
    with _lock:
        c = conn()
        cur = c.execute('INSERT INTO scans (created, result, hash) VALUES (?, ?, ?)',
                        (time.time(), json.dumps(result, ensure_ascii=False), h))
        c.commit()
        sid = cur.lastrowid
    img.save(config.DATA / 'scans' / f'{sid}.jpg', quality=85)
    if crop is not None:
        crop.save(config.DATA / 'scans' / f'{sid}_crop.jpg', quality=90)
    return sid


def update_scan(sid, result):
    with _lock:
        conn().execute('UPDATE scans SET result = ? WHERE id = ?', (json.dumps(result, ensure_ascii=False), sid))
        conn().commit()


def add_alias(name, oid):
    with _lock:
        if key(name):
            conn().execute('INSERT OR REPLACE INTO aliases VALUES (?, ?)', (key(name), oid))
            conn().commit()


def get_scan(sid):
    """Scan-Ergebnis und das Bild für die KI (freigestellt, falls vorhanden)."""
    row = _one('SELECT * FROM scans WHERE id = ?', (sid,))
    if not row:
        return None, None
    path = config.DATA / 'scans' / f'{sid}_crop.jpg'
    if not path.exists():
        path = config.DATA / 'scans' / f'{sid}.jpg'
    return dict(row, result=json.loads(row['result'])), (Image.open(path) if path.exists() else None)


def inventory():
    return [dict(r) for r in _all('SELECT * FROM inventory ORDER BY fach')]


def store_item(obj, modell):
    """Neuen Gegenstand einlagern: freies E-Fach und fortlaufende Inventarnummer vergeben."""
    with _lock:
        c = conn()
        used = {r['fach'] for r in c.execute("SELECT fach FROM inventory WHERE fach LIKE 'E-%'")}
        fach = next(f'E-{i:02d}' for i in range(1, 100) if f'E-{i:02d}' not in used)
        nr = (c.execute('SELECT MAX(nr) FROM inventory').fetchone()[0] or 400) + 1
        from .schemas import CATALOG
        mid = obj['parts'][-1]['materials'][0][0] if obj.get('parts') else None
        cls = CATALOG['materials'].get(mid, {}).get('cls')
        iid = f"{obj['id']}-{nr}"
        c.execute('INSERT INTO inventory VALUES (?,?,?,?,?,?,?,?,?)',
                  (iid, modell or obj['name'], fach, 1, 'Stk', cls, obj['id'], nr, time.time()))
        c.commit()
        return dict(c.execute('SELECT * FROM inventory WHERE id = ?', (iid,)).fetchone())


def book(object_id, projekt):
    """Material für ein Projekt ausbuchen. Bricht ab, wenn der Bestand nicht reicht."""
    with _lock:
        c = conn()
        fehlt = []
        for u in projekt['nutzt']:
            if u.get('inv'):
                row = c.execute('SELECT name, menge FROM inventory WHERE id = ?', (u['inv'],)).fetchone()
                if not row or row['menge'] < u['menge']:
                    fehlt.append(row['name'] if row else u['inv'])
        if fehlt:
            return {'ok': False, 'fehlt': fehlt}
        for u in projekt['nutzt']:
            if u.get('inv'):
                c.execute('UPDATE inventory SET menge = menge - ? WHERE id = ?', (u['menge'], u['inv']))
        c.execute('INSERT INTO bookings (created, object_id, data) VALUES (?, ?, ?)',
                  (time.time(), object_id, json.dumps(projekt, ensure_ascii=False)))
        c.commit()
        return {'ok': True}
