# Backend und KI

Ein Python-Prozess (FastAPI) führt die Pipeline aus. Die KI kommt wahlweise von

- **lokal:** OpenAI-kompatibler Modellserver, standardmäßig Ollama mit dem Stationsmodell `station-vl` (Qwen3-VL 4B, siehe `backend/Modelfile`), oder
- **Claude:** Anthropic-API über das offizielle Python-SDK (`backend/app/llm_claude.py`), Modell `claude-opus-5-5`.

Umschalten mit `LLM_PROVIDER=lokal` bzw. `LLM_PROVIDER=claude`.

## Docker (drei Container)

```bash
cp .env.example .env          # LLM_PROVIDER wählen; Zugangsdaten als Secrets, siehe claude-sdk.md
docker compose up -d --build  # oder: docker compose pull && docker compose up -d
```

| Container | Inhalt | Port |
|---|---|---|
| `frontend` | nginx mit der Web-App, leitet `/api` an das Backend | 8080 |
| `backend` | FastAPI-Pipeline, SQLite im Volume `station-daten` | intern 8000 |
| `inferenz` | Ollama, lädt beim ersten Start `qwen3-vl:4b` (ca. 3,3 GB) ins Volume `ollama-modelle` und legt `station-vl` an | intern 11434 |

Bei jedem Push auf `main` baut GitHub Actions die drei Images und veröffentlicht sie als Packages: `ghcr.io/kontor2026/web-app-frontend`, `-backend`, `-inferenz` (Tags `latest` und Commit-SHA). GPU: im `docker-compose.yml` den `deploy`-Block beim Inferenz-Container einkommentieren.

## Claude statt lokalem Modell

- Braucht einen **API-Schlüssel aus der Claude Console** (https://platform.claude.com), abgerechnet pro Token. Ein claude.ai-Abo (Pro/Max) ist kein API-Zugang: Anthropic erlaubt nicht, den Abo-Login oder dessen Kontingent für eigene Produkte zu nutzen.
- Kosten grob: Erkennung ca. 0,5–1 Cent, Steckbrief ca. 3–6 Cent, Bauideen ca. 1–2 Cent pro Gegenstand (Claude Opus 5.5, 4 $/20 $ pro Million Token, Schätzung).
- Denktiefe pro Schritt (`EFFORT` in `llm_claude.py`): Erkennung und Bauideen `low`, Steckbrief `medium`.
- Strukturierte Ausgaben kennen keine Zahlen- und Längengrenzen. `claude_schema()` verschiebt sie in die Feldbeschreibung, geprüft wird danach wie beim lokalen Modell.
- Lehnt ein Sicherheitsfilter eine Anfrage ab, übernimmt serverseitig ein Ersatzmodell (`fallbacks: "default"`).

## Claude mit Abo-Zugang (`claude-abo`)

Über das Claude Agent SDK (`backend/app/llm_claude_abo.py`) statt der API. Anthropic erlaubt das für eigene Produkte nur mit vorheriger Freigabe. Hier: privater Test mit Freigabe.

- Zugang nur über ein ausdrücklich hinterlegtes Token aus `claude setup-token`, als Docker-Secret in `secrets/claude_oauth_token.txt`. Persönliche Anmeldungen auf dem Rechner werden nie genutzt. Anleitung und Deployment: [claude-sdk.md](claude-sdk.md).
- Alle Claude-Code-Werkzeuge sind abgeschaltet, `setting_sources=[]` verhindert, dass Einstellungen oder CLAUDE.md des Rechners geladen werden.
- Gemessen (AirPods-Foto, Claude Opus 5.5): Erkennung 8 s, Steckbrief 34 s, Bauideen 37 s. Ergebnisse deutlich genauer als das lokale 4B-Modell.

## Vorausrechnen (parallel ab Upload)

Steckbrief und Bauideen brauchen nur das Bild. Mit Claude (`claude`, `claude-abo`) starten sie deshalb beim Upload sofort parallel zur Erkennung, als Hintergrund-Jobs im Backend. Wählt der Schüler den wahrscheinlichsten Kandidaten (Normalfall), wird der vorbereitete Steckbrief übernommen. Wählt er einen anderen, wird für diesen neu gerechnet. Beim lokalen Modell (nur eine Anfrage gleichzeitig) starten die Bauideen direkt nach dem Steckbrief im Hintergrund. Steuerung: `VORAUSRECHNEN=auto|an|aus`. Stand der Jobs: `GET /api/scans/{id}/jobs`, im Frontend als „Bauideen bereit“ neben den Buttons.

Gemessen (AirPods-Foto, Claude-Abo, Opus 5.5):

| ab Upload | |
|---|---|
| 8,7 s | Erkennung fertig, Steckbrief und Ideen laufen schon |
| 38 s | Steckbrief fertig (nach dem Bestätigen nur noch 22 s Wartezeit) |
| sofort | Bauideen beim Öffnen fertig |

Ein kompletter neuer Gegenstand kostet beim Pro-Abo etwa 2 Prozentpunkte des 5-Stunden-Kontingents.

## Ohne Docker starten

```bash
ollama pull qwen3-vl:4b
ollama create station-vl -f backend/Modelfile
python -m venv backend/.venv
backend/.venv/Scripts/pip install -r backend/requirements.txt      # Linux: backend/.venv/bin/pip
backend/.venv/Scripts/python -m uvicorn backend.app.main:app --port 8000
```

Dann http://localhost:8000 öffnen. In der Kopfzeile steht „KI lokal · qwen3-vl:4b“. Ohne Backend (z. B. `python -m http.server`) läuft die App im Demo-Modus mit simulierten Daten.

## KI-Proxy für die Entwicklung

Nur für Entwickler, nicht Teil der App und nicht in den Containern. Der Proxy (`tools/ki_proxy.py`) fragt beim Start, welche KI er nutzen soll (`lokal`, `claude` oder `claude-abo`), und bietet sie als OpenAI-kompatiblen Server an. Das Backend läuft dabei immer mit `LLM_PROVIDER=lokal` und spricht nur mit dem Proxy. Zum Wechseln der KI wird nur der Proxy neu gestartet, das Backend läuft weiter.

```bash
backend/.venv/bin/python tools/ki_proxy.py               # fragt nach der KI (Windows: backend/.venv/Scripts/python)
backend/.venv/bin/python tools/ki_proxy.py --ki claude   # ohne Rückfrage
LLM_PROVIDER=lokal LLM_BASE_URL=http://127.0.0.1:4000/v1 backend/.venv/bin/python -m uvicorn backend.app.main:app --port 8000
```

Backend unter Windows (PowerShell):

```powershell
$env:LLM_PROVIDER="lokal"; $env:LLM_BASE_URL="http://127.0.0.1:4000/v1"; backend/.venv/Scripts/python -m uvicorn backend.app.main:app --port 8000
```

- `lokal` leitet unverändert an einen OpenAI-kompatiblen Server weiter, standardmäßig Ollama auf `localhost:11434` (ändern mit `--upstream`).
- `claude` und `claude-abo` nutzen dieselben Module wie das Backend (`llm_claude.py`, `llm_claude_abo.py`) und dieselben Einstellungen (`ANTHROPIC_API_KEY`, `CLAUDE_MODEL`, Abo-Anmeldung des Rechners).
- Der Proxy hört standardmäßig nur auf `127.0.0.1:4000` (`--host`, `--port`). Das Abo ist persönlich: den Proxy im Modus `claude-abo` nicht für andere Rechner freigeben.
- Weil das Backend „lokal“ sieht, rechnet es nicht voraus und zeigt in der Kopfzeile „KI lokal · station-vl“. Mit Claude hinter dem Proxy `VORAUSRECHNEN=an` setzen.

## Einstellungen (Umgebungsvariablen)

| Variable | Standard | Zweck |
|---|---|---|
| `LLM_BASE_URL` | `http://localhost:11434/v1` | Jeder OpenAI-kompatible Server: Ollama, llama.cpp-Server, vLLM, Cloud |
| `VISION_MODEL` | `qwen3-vl:4b` | Erkennung und Steckbrief (mit Bild) |
| `TEXT_MODEL` | wie `VISION_MODEL` | Bauideen |
| `LLM_REASONING` | `none` | schaltet das „Nachdenken“ von Qwen3 ab, auf CPU 5–10× schneller |
| `LLM_MODE` | `openai` | `mock` = ohne Modell, nur Foto-Abgleich |
| `IMAGE_MAX_PX` | `896` | Bildgröße für das Modell |
| `STATION_DATA` | `backend/data` | SQLite-Datenbank und Scan-Fotos |

Auf der Station mit GPU: `VISION_MODEL=qwen3-vl:8b`.

## Pipeline

```
POST /api/scan          Bild → Qualitätscheck → Foto-Abgleich (dHash) → sonst Vision-Modell
                        Ausgabe: Gattung, Kategorie, Top-3-Kandidaten, gelesener Text, Materialvermutung
POST /api/steckbrief    bestätigter Kandidat → Cache (Modellname) → sonst KI-Entwurf
                        KI liefert Bauteile mit Ebene, Form, Anteilen, Materialien (feste ID-Liste)
                        layout.py rechnet daraus die Geometrie der Explosionszeichnung
POST /api/objects/{id}/ideen    Lagerbestand + Objekt → 3 Projekte, Lager-IDs im Schema erzwungen
POST /api/inventory/einlagern   freies Fach E-xx und Inventarnummer
POST /api/projekte/start        Material ausbuchen, bricht bei zu wenig Bestand ab (409)
POST /api/objects/{id}/freigeben  Werkstatt hat den KI-Entwurf geprüft
GET  /api/objects?status=entwurf  Prüf-Warteschlange
```

Stabilität:

- **Schema statt Freitext.** Jede KI-Antwort wird per `response_format: json_schema` erzwungen. Material- und Lager-IDs sind Aufzählungen im Schema.
- **KI beschreibt, Code rechnet.** Das Modell nennt Ebenen und grobe Anteile, keine Koordinaten. Jede gültige Antwort ist zeichenbar.
- **Prüfen und einmal wiederholen.** Fachliche Prüfungen (z. B. „ein Teil muss die ganze Grundfläche einnehmen“, „Lagerbestand reicht“) gehen bei Fehlern als Korrekturhinweis zurück an das Modell.
- **Cache wächst mit.** Bestätigte Steckbriefe werden unter dem Modellnamen gespeichert. Der nächste Scan desselben Modells braucht keine KI.
- **Ehrlich markiert.** KI-Steckbriefe tragen den Status `entwurf` und erscheinen in der App als „KI-Entwurf · ungeprüft“.

## Gemessen auf dem Entwicklungs-Laptop (i7-13700H, nur CPU, qwen3-vl:4b)

| Schritt | Dauer |
|---|---|
| Foto-Abgleich bekanntes Foto | 0,1 s |
| Erkennung neues Objekt | ca. 19 s |
| Steckbrief / Bauideen aus dem Cache | unter 0,1 s |

Neue Steckbriefe und Bauideen brauchen auf CPU mehrere Minuten. Mit GPU (RTX-Klasse oder Jetson AGX Orin) sind es grob 10–30 s.

## Daten

`backend/seed/` wird mit `node tools/export_seed.mjs` aus `js/data/` erzeugt. Nach Änderungen am Katalog neu exportieren und `backend/data/station.db` löschen, damit sie neu befüllt wird.

## Ausbaustufen

- Foto-Abgleich mit SigLIP-Bildvektoren statt dHash: erkennt auch neue Fotos desselben Gegenstands.
- NIR-Sensor: Kunststoffsorte per klassischem Klassifikator (LDA/SVM) als zusätzlicher Pipeline-Schritt.
- Wissensbasis (iFixit-Teardowns, Ökobilanzen, Entsorgungsregeln vor Ort) per RAG in den Steckbrief-Prompt.
