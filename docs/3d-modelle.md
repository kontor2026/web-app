# Übergabe: 3D-Modelle der 201 Kategorien bauen

Diese Datei ist der Auftrag für die Session, die die Explosionszeichnungen baut. Ziel: für jede der 201 Kategorien ein **detailgetreues** 3D-Modell, so wie die beiden Vorlagen Smartphone und Laptop.

## Ausgangslage

- Die App erkennt nur noch **grobe Kategorien** („Computermaus“, nicht „Logitech MX Master“). Eine Feinklassifizierung gibt es nicht mehr.
- Die 3D-Modelle werden **einmal vorab gebaut** und zur Laufzeit nur geladen. Die KI erzeugt keine Geometrie mehr.
- Die Liste der Kategorien, ihre Komponenten und deren Materialien stehen in **`data/classifier.json`** (gepflegt von Hansehart): `objects` (201), `components` (318), `materials` (41). Diese Datei nicht ändern. Fehlt eine Komponente, mit dem Team absprechen.
- Für alle 201 Kategorien gibt es schon **automatische Platzhalter**. Jedes handgebaute Modell ersetzt seinen Platzhalter.

## Wo die Modelle hingehören

| Datei | Inhalt | Wer pflegt |
|---|---|---|
| `tools/kategorien/modelle/<id>.json` | **Das handgebaute Modell**: `{ "parts": [ ... ] }` | diese Session |
| `tools/kategorien/kategorien.csv` | deutscher Name, Entsorgungsweg, Maße, Gewicht, Grundform je Kategorie | bei Bedarf Maße und Gewicht korrigieren |
| `data/classifier.json` | Kategorien, Komponenten, Materialien | Team, nicht ändern |
| `backend/seed/kategorien/<id>.json` | **erzeugt**, nie von Hand bearbeiten | `tools/kategorien/build.py` |

`<id>` ist der Schlüssel aus `classifier.json` → `objects`, z. B. `computer_mouse`, `pet_bottle`, `electric_kettle`.

Nach jeder Änderung:

```bash
python tools/kategorien/build.py
```

Der Generator übernimmt `parts` aus `modelle/<id>.json` und ergänzt Name, Klasse, Entsorgung und Maße aus der CSV. In der Ausgabe steht `"platzhalter": false`.

## Vorlagen

- `tools/kategorien/modelle/smartphone.json` (12 Teile) und `laptop.json` (17 Teile) sind fertige Beispiele im Zielformat.
- Die Originale mit Kommentaren: `js/data/objects/smartphone.js`, `laptop.js`, `netzteil.js`, `flasche.js`. Dort sieht man auch, wie man Details wie Tastenraster per Schleife erzeugt. In JSON müssen die Werte ausgeschrieben sein, ein kleines Node-Skript darf sie aber erzeugen.

## Quellskripte und Bausteine

Jedes Modell hat ein Quellskript `tools/kategorien/quellen/<id>.py`, das `modelle/<id>.json` erzeugt und sofort mit `pruefe.py` prüft:

```bash
python tools/kategorien/quellen/<id>.py
```

Die Bausteine stehen in `tools/kategorien/bau.py` (nur Standardbibliothek):

- `teil(...)`: ein Bauteil; `material_id` kommt aus der Komponente, `materials` aus der Tabelle `MATERIAL` in `build.py`, beides überschreibbar.
- `explodiere(teile, abstand)`: setzt `explode` für alle Teile ohne eigenen Versatz, so dass explodiert nichts überlappt.
- `raster(...)`, `mark(...)`: Details wie Tastenraster, Lüftungsschlitze, Akkuzellen.
- `skaliere_masse(teile, oid=...)`, `masse(oid)`, `komponenten(oid)`: Gewicht und Maße aus `kategorien.csv`, Komponenten aus `classifier.json`.

Änderungen am Modell immer im Quellskript machen, nicht in der JSON-Datei.

## Format eines Bauteils

Koordinaten in **Millimetern**. `x` = Breite, `y` = Tiefe (nach hinten = 0, vorne = groß), `z` = Höhe über dem Tisch. Jedes Teil ist ein senkrecht extrudierter Grundriss: ein abgerundetes Rechteck (`box`) oder eine Ellipse (`cyl`). Der Gegenstand liegt so, wie man ihn auf die Station legen würde.

```json
{
  "id": "akku",
  "component_id": "li_ion_battery",
  "material_id": "li_ion",
  "name": "Lithium-Ionen-Akku",
  "short": "Akku",
  "shape": "box",
  "x": 22, "y": 60, "w": 46, "d": 64,
  "z": 3, "h": 4.2,
  "r": 3,
  "explode": [0, 0, 120],
  "mass": 46,
  "materials": [["lco", 38], ["graphit", 20], ["elektrolyt", 15], ["kupfer", 10], ["alu", 10], ["folien", 7]],
  "info": "Etwa 3.100 mAh. Mit Klebestreifen befestigt.",
  "marks": [{ "shape": "box", "x": 4, "y": 4, "w": 38, "d": 56, "r": 2 }]
}
```

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `id` | ja | eindeutig im Modell, ASCII, z. B. `deckel`, `platine` |
| `component_id` | empfohlen | Schlüssel aus `classifier.json` → `components`. Jede Komponente des Objekts muss in mindestens einem Teil vorkommen. Zusätzliche Detailteile (Chips auf der Platine, Schrauben) bekommen die `component_id` des Teils, zu dem sie gehören |
| `material_id` | empfohlen | Material laut `classifier.json` |
| `name`, `short` | ja | Deutsch. `short` (max. ca. 18 Zeichen) steht an der Positionsnummer |
| `shape` | ja | `box` (abgerundetes Rechteck, Radius `r`) oder `cyl` (Ellipse: Durchmesser `w`, optional `d`) |
| `x`, `y`, `w`, `d` | ja | Grundriss: linke hintere Ecke und Größe. Bei `cyl` ohne `d` ist es ein Kreis |
| `z`, `h` | ja | Unterkante über dem Tisch und Höhe. Zusammengebaut müssen die Teile den Gegenstand ergeben |
| `r` | nein | Eckradius bei `box` |
| `explode` | ja | Versatz `[dx, dy, dz]` in mm im explodierten Zustand. Teile mit gleichem Versatz bewegen sich zusammen |
| `mass` | ja | Gramm. Die Summe soll ungefähr dem Gewicht in `kategorien.csv` entsprechen |
| `materials` | ja | `[[katalog-id, prozent], ...]` mit IDs aus `js/data/catalog.js`, Summe 100. Umrechnung von `material_id` siehe unten |
| `info` | ja | 1–2 Sätze auf Deutsch für Schüler: was das Teil tut, wie man es löst oder worauf man achten muss |
| `marks` | nein | Details auf der Oberseite des Teils: `[{shape, x, y, w, d, r, fill}]`, Koordinaten **relativ zum Teil**. Für Tasten, Linsen, Lüftungsschlitze, Display-Fläche, Spulenwindungen |
| `color`, `opacity` | nein | Sonst automatisch nach Materialklasse. Displays z. B. `"#31373B"`, Glas `"opacity": 0.6` |
| `label` | nein | `false` = keine Positionsnummer (z. B. zweiter gleicher Lautsprecher) |
| `sortBias` | nein | korrigiert die Zeichenreihenfolge, falls ein Teil falsch verdeckt wird |

Die Reihenfolge im Array bestimmt die Positionsnummern: **oberstes Teil zuerst** (01 = Deckel oder Display).

### Material-Umrechnung (classifier → Katalog)

Steht als Tabelle `MATERIAL` in `tools/kategorien/build.py`. Für die wichtigsten Fälle:

| classifier | Katalog-`materials` |
|---|---|
| `pcb` | `[["fr4",55],["kupfer",20],["chip",15],["lot",10]]` (Chips besser als eigene Teile mit `chip`) |
| `li_ion` | `[["lco",40],["graphit",20],["elektrolyt",15],["alu",15],["kupfer",10]]` (Laptop-Akkus: `nmc` statt `lco`) |
| `mixed_electronics` | `[["chip",30],["kupfer",30],["pcabs",25],["stahl",15]]`, besser genauer aufteilen (Motor: Kupfer, Stahl, `ndfeb`) |
| `abs`, `pc` | `pcabs` · `special_glass` → `glas` · `glass` → `behaelterglas` · `steel` → `stahl` · `aluminium` → `alu` |

Fehlt ein Material im Katalog: in `js/data/catalog.js` ergänzen (nur hinzufügen, nie umbenennen), dann `node tools/export_seed.mjs` ausführen.

## Was „detailgetreu“ heißt

Maßstab sind Smartphone und Laptop:

- **8–16 Teile** bei Geräten, 3–6 bei einfachen Verpackungen. Jede Komponente aus `classifier.json` kommt vor, wichtige Unterteile sind eigene Teile: Prozessor und Speicher auf der Platine, Linsen im Kameramodul, Kondensatoren und Trafo im Netzteil.
- **Echte Proportionen**: Maße aus Datenblättern oder Teardowns (z. B. iFixit) eines typischen Vertreters der Kategorie. Kein bestimmtes Modell nachbauen, sondern das Typische.
- **Details per `marks`**: Tastenraster, Kameralinsen, Display-Fläche mit Notch, Lüftungsschlitze, Spulenwindungen, Akkuzellen.
- **Explosion, die das Innenleben zeigt**:
  - Flache Geräte: Ebenen nach oben, Abstand ca. 40–60 % der Grundflächen-Tiefe, damit jede Ebene sichtbar bleibt.
  - Große flache Geräte (Laptop, Monitor): Deckel nach hinten aufklappen (`dy` negativ), obere Schale zur Seite (`dx` negativ), Innenleben bleibt frei.
  - Hohe Gegenstände (Flaschen, Wasserkocher): Teile über dem Körper stapeln. Jedes Teil schwebt mit Abstand **über der Oberkante** des darunterliegenden.
  - Kabel, Etiketten, Griffe: seitlich herausziehen (`dx` positiv).
  - Kleine Teile auf einem Bauteil (Chips) mit eigenem, etwas größerem `dz` abheben.
- **Zusammengebaut** (Schalter „Zusammengebaut“) muss der Gegenstand wie der echte aussehen: Gehäuse oben und unten geschlossen, nichts ragt heraus.

## Foto-Ansicht (Seite „3D-Modelle“)

Die Seite unter `packages/site` zeigt die Modelle fotorealistisch (`packages/site/src/foto.js`): Material aus `materials[0]` (Metall spiegelt, Glas bricht das Licht, Stoff hat Glanz), gerundete Kanten, Schatten. Zusätzliche Felder, die nur dort wirken (die Station zeichnet weiter massiv):
- `wand` (mm) am Teil: hohl mit dieser Wandstärke, oben offen. `boden` (mm): Bodendicke, Standard = `wand`, `0` = auch unten offen (Ring, Reifen, Manschette). Für Becher, Eimer, Töpfe, Rohre, Schläuche, Etikettenbänder.
- `form` am Teil: echte Form, die den Quader des Teils ausfüllt: `kugel` (Ball, Knauf), `torus` (Ring, Kabelrolle, Reifen), `liegend_x` / `liegend_y` (liegender Zylinder entlang x bzw. y: Kabel, Rolle, Griff, Rad, Stift). Weiche Materialien bekommen runde Enden.
- Automatisch: Kanten werden nach Material gerundet (Stoff, Leder, Gummi, Kabel weich wie ein Kissen), und mindestens drei gleich aussehende, lückenlos gestapelte Scheiben mit gleicher Explosion werden zu einer glatten Hülle verbunden (Flaschenschulter, Schuh, Kegel).
- `zeichnung: true` an einem mark (`mark(..., zeichnung=True)`): nur in der Zeichnung, z. B. eine aufgemalte Öffnung, die in der Foto-Ansicht `wand` ersetzt.
- Prüfen: Vite-Dev-Server in `packages/site` (`npx vite --port 5190`), dann `node scripts/foto-pruef.mjs <id> <ordner>`.

## Prüfen

Ohne Backend: `node tools/kategorien/foto.cjs <id> [...]` fotografiert Modelle aus `modelle/` (links zusammengebaut, rechts explodiert) nach `<tmp>/modell-fotos/<id>.png`. Braucht Playwright (z. B. `npm ci` in `packages/site`). Im Browser geht dasselbe mit `/tools/kategorien/ansicht.html?static&id=<id>` über einen beliebigen statischen Server im Projektordner.

```bash
python tools/kategorien/build.py
backend/.venv/Scripts/python -m uvicorn backend.app.main:app --port 8000   # neu starten, lädt die Modelle beim Start
```

- `http://localhost:8000/?static#kat=<id>` zeigt das Modell explodiert und ohne Animation, ohne `?static` mit Animation.
- `http://localhost:8000/#katalog` listet alle 201 Kategorien, handgebaute grün umrandet.
- Checkliste je Modell: Zusammengebaut sieht es aus wie der Gegenstand? Explodiert sind alle Teile sichtbar und keines liegt hinter einem anderen? Positionsnummern überlappen nicht? Klick auf jedes Teil zeigt Material und Elemente? Gewicht stimmt ungefähr?

## Reihenfolge

Zuerst, was Schüler am häufigsten mitbringen: `pet_bottle`, `aluminium_can`, `glass_bottle`, `yogurt_cup`, `beverage_carton`, `phone_charger`, `usb_cable`, `earbuds`, `computer_mouse`, `keyboard`, `headphones`, `power_bank`, `tablet`, `remote_control`, `led_bulb`, `alkaline_battery`, `electric_toothbrush`, `hair_dryer`, `toaster`, `electric_kettle`, `game_controller`, `sneaker`, `t_shirt`. Danach der Rest der Liste in `classifier.json`.

## Nicht anfassen

- `backend/app/*`, `js/main.js`, `js/iso.js`: Pipeline und Renderer. Braucht der Renderer eine neue Fähigkeit (z. B. eine weitere Form), das bitte melden statt selbst umbauen.
- Die Felder `werte` und `rohstoffe` (Rohstoffwert, CO₂, Metallgehalte): Die berechnet `build.py` aus der Rohstoff-Datenbank in `data/rohstoffe/` (siehe dortige README). Sie rechnen mit den `mass`- und `material_id`-Angaben eurer Teile. Realistische Massen und korrekte `material_id` je Teil machen also auch die Rohstoffwerte genauer.
- `data/classifier.json` (Team).

## Git

- Arbeiten auf `main`, vor jedem Push `git pull --rebase`. Hier arbeiten mehrere Sessions und Leute parallel.
- Kleine Commits, z. B. ein Commit pro 5–10 Modelle: „3D-Modelle: Getränkeverpackungen“.
- `backend/seed/kategorien/` (erzeugt) mit committen, damit Backend und Docker-Images die Modelle haben.
