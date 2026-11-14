# 3D-Präsentation: Kreislauf-Station

Fünf Minuten nach AIDA in einer durchgehenden Three.js-Welt. Ein altes Handy ist der rote Faden: Schublade → was drin steckt → Restmüll → der Weg reißt ab → graue Energie geht verloren → der Scanner schließt den Kreis → Lernkreis mit Gehirn → **Live-App im Monitor** → Bauideen → unter der Haube mit Datenbank und Messwerten → deine Wahl der KI → Bausatz mit Kosten → Deutschlandkarte ab Lübeck → Name, Schlusssatz und QR-Code.

## Starten

```bash
node tools/serve.cjs            # http://localhost:5181/  (leitet auf /praesentation/ weiter)
```

Der Server liefert das ganze Repo aus, weil die Präsentation die **echten Kategorie-Modelle** (`backend/seed/kategorien`) und die Material- und Formfunktionen der App (`packages/site/src/foto.js`, `js/data/catalog.js`) lädt. Präsentation und App zeigen damit dieselben Modelle. Die Stations-App liegt unter `/index.html`, Anfragen an `/api/` gehen an das Backend (`API_URL`, Standard `http://127.0.0.1:8000`). Läuft kein Backend, zeigt die App ihren Demo-Modus.

### Mit Backend und öffentlich per HTTPS

```bash
backend/.venv/bin/python -m uvicorn backend.app.main:app --port 8000     # Backend mit KI, siehe docs/backend.md
node tools/serve.cjs 5181 --tunnel                                       # Präsentation + App + /api, dazu Cloudflare-Tunnel
```

`--tunnel` startet `cloudflared` (macOS `brew install cloudflared`, Windows `winget install Cloudflare.cloudflared`) und gibt eine zufällige Adresse `https://….trycloudflare.com/` aus. Präsentation, App und API laufen über diese eine Adresse, also gleiche Herkunft: Die Tasten X und F wirken auch aus der App heraus, und die Kamera in der App funktioniert, weil die Seite HTTPS hat. Der Server sperrt `.git`, `.env`, `secrets/`, `node_modules/`, `.claude/`, `.venv/` und `backend/data/` (Datenbank und gescannte Fotos). Alles andere im Repo ist öffentlich lesbar, solange er läuft. Wer die Adresse kennt, kann auch scannen und damit die KI des Backends nutzen.

## Ablauf (AIDA, 5:00)

| AIDA | Zeit | Schritt | Was passiert | Text auf dem Bild |
|---|---|---|---|---|
| **A** | 0:00–0:35 | 1 Schublade | Schublade öffnet sich: Handy, Ladegerät, Kopfhörer, Powerbank (Katalogmodelle) | – |
| | | 2 Was drin steckt | Handy schwebt heraus, zerfällt in 16 Teile, Platine und Akku leuchten | 30 mg Gold · 305 mg Silber · 6,3 g Kobalt |
| | | 3 Weggeworfen | Teile fallen zusammen, Handy landet in der Restmülltonne | Was drin steckt, sieht man nicht. |
| **I** | 0:35–1:50 | 4 Der Weg | Ring ab Abbau (3 Uhr): Verarbeitung, Herstellung, Gegenstand, Nutzung (Kommode), Entsorgung (Tonne) grün; danach eine Lücke über Verwertung (4 Uhr) bis zum Abbau | – |
| | | 5 Graue Energie | Goldene Spirale windet sich um den Ring bis zur Tonne, dort leuchtet der Verlust | Die Energie steckt schon drin. |
| | | 6 Die Station | Station taucht in der Lücke auf, der Ring schließt sich, die Spirale läuft weiter bis zum Abbau: „Graue Energie bleibt im Kreislauf“ | Wir schließen die Lücke. |
| | | 7 Lernkreislauf | Brücke von der Station in den inneren Kreis, Wissen fließt in ein Gehirn, Brücke zurück („Katalog wächst“) | Was man versteht, wirft man nicht weg. |
| **I** | 1:50–3:30 | 8 Station | Kamera vor den Monitor, die App liegt perspektivisch genau auf dem Bildschirm | – |
| | | 9 **Live** | Flug in den Bildschirm, die App füllt das Bild und ist bedienbar (ca. 1:10) | – |
| | | 10 Bauideen | Nach der Demo (X): eine Säule in der Mitte steigt auf, die Musik-Box (Handy + Schuhkarton) baut sich zusammen, „Schuhkarton aus dem Lager“ | Aus Altem wird Neues. |
| **D** | 3:30–4:20 | 11 Unter der Haube | Container und Datenbank, Paket: Foto-Abgleich → KI erkennt die Kategorie → Prüftor → Datenbank → Bildschirm. Rechts oben **93 % · 28 von 30** und **≤ 5 s** | Die KI erkennt. Die Datenbank weiß. Der Mensch entscheidet. |
| | | 12 Deine Wahl | Haus um die Station, Schalter Lokal ↔ Cloud | Du entscheidest, wohin dein Foto geht. |
| **A** | 4:20–5:00 | 13 Bausatz | Laptop klappt auf, Webcam oben, `docker compose up` | Ein Laptop. Eine Kamera. Ein Befehl. · ca. 100 € Hardware, unter 1 € am Tag |
| | | 14 Überall | Deutschlandkarte, Welle von Lübeck aus („Pilot ab Dezember · 10–15 Schüler“), **QR-Code oben links** | Eine Station. Dann jede Werkstatt. |
| | | 15 Bring es mit | „Bring dein altes Handy mit.“ kippt durch Laptop, Powerbank, Kopfhörer, Ladekabel, dann zu Name und Schlusssatz; Lübeck: „ab Februar 2027 · Schützenstraße 62“; QR bleibt | ReSource Scanner · KI für die Kreislaufwirtschaft von morgen. |

Sprechertext je Schritt: Taste **T** (steht in `content.js`). Die Jury-Kriterien aus `data/rating.md` werden gezeigt, aber nicht benannt:

| Kriterium | Wo |
|---|---|
| New Approach | 4–7: der Weg reißt ab, graue Energie geht verloren, die Station schließt den Kreis, Lernkreis |
| Usability | 9–10: Live-App und Bauideen |
| Technical Solution | 11 (Container, Datenbank, Messwerte gegen das Ziel) |
| Responsible Use of AI | 11 (KI nur für die Kategorie, Wissen aus der Datenbank mit Quellen, Mensch gibt frei) und 12 (lokal oder Cloud, Open Source) |
| Makeability | 13–15 (Kosten, Pilot in Lübeck, Regelbetrieb ab Februar) |
| Pitch | durchgehend ein Gegenstand, kaum Text |

## Tasten

| Taste | Wirkung |
|---|---|
| → ↓ Leertaste Bild↓ (Clicker) | weiter |
| ← ↑ Bild↑ | zurück (Schritt im Endzustand) |
| **X** | in die App und wieder heraus. In Schritt 9 führt X weiter zu den Bauideen. Von jeder anderen Folie springt X in die App und mit X wieder genau dorthin zurück (für Rückfragen). |
| **F** | Vollbild ohne Browserleiste |
| 1–5 | direkt zur Folie |
| Z | Animation des Schritts von vorn |
| B oder . | Bild schwarz |
| T / H | Sprechertext / Hilfe |
| R | Kamera zurück, nachdem man mit der Maus frei gedreht hat |

In der laufenden App gehen Pfeiltasten und Leertaste an die App. **X, F, Bild↓, Bild↑** wirken auch, wenn man in die App geklickt hat, außer beim Tippen in ein Eingabefeld. Oben rechts liegt zusätzlich ein unauffälliger Knopf „X zurück“.

## Die echte App einbinden

Im Monitor läuft die **echte Stations-App** aus diesem Repo (`APP_URL = '../index.html'`), mit Backend live, sonst im Demo-Modus. Die frühere Platzhalter-App (`mock-app/`) bleibt als Rückfall. Umstellen ohne Codeänderung:

```text
http://localhost:5181/praesentation/?app=./mock-app/          (Platzhalter-App)
http://localhost:5181/praesentation/?app=https://adresse-der-app/
```

Dauerhaft: `APP_URL` in `content.js`. Damit **X** und **F** auch aus der App heraus funktionieren:

- **Gleiche Herkunft** (App über denselben Server oder Tunnel): funktioniert automatisch.
- **Andere Herkunft:** Die App muss diese Tasten weiterreichen:
  ```js
  addEventListener('keydown', (e) => {
    if (['x', 'X', 'f', 'F', 'PageDown', 'PageUp'].includes(e.key) && !/INPUT|TEXTAREA/.test(e.target.tagName))
      parent.postMessage({ type: 'praesi-key', key: e.key }, '*');
  });
  ```
  Ohne das hilft der Knopf „X zurück“ oben rechts. Die App darf nicht mit `X-Frame-Options: DENY` oder `frame-ancestors` das Einbetten verbieten, und beide Seiten brauchen HTTPS.

## Technik

| Datei | Inhalt |
|---|---|
| `engine.js` | Renderer, MSAA + Bloom, Kamerafahrten (Smootherstep), sehr ruhige Drift, HTML-Beschriftungen, Pixelbudget mit automatischer Anpassung |
| `world.js` | die ganze Welt und die Regie: `update(k, t)` setzt jeden Darsteller absolut aus Schritt und Zeit. Vorwärts, rückwärts und Sprünge sehen deshalb immer gleich aus. |
| `katalog.js` | baut Kategorie-Modelle mit den Funktionen der App (`foto.js`) |
| `content.js` | Folien, Texte, Sprechertext, `APP_URL`, `PRODUKTNAME`, QR-Ziel, Gegenstände für das Finale |
| `app.js` | Navigation, Tasten, iframe per Homografie (CSS `matrix3d`) exakt auf dem Monitor |
| `werkstaetten.js` | Orte auf der Deutschlandkarte, Start (Lübeck) |
| `mock-app/` | frühere Platzhalter-App (Rückfall per `?app=./mock-app/`) |
| `assets/` | Three.js r170 mit Addons (lokal, kein CDN), Deutschland-Umriss (Natural Earth über `world-atlas`), QR-Code |

Damit nichts ruckelt:

- Alle Szenen werden beim Laden einmal gerendert, damit alle Shader kompiliert sind.
- Lichter werden nie ein- oder ausgeschaltet, nur gedimmt (sonst würden alle Shader neu kompiliert).
- Schattenkarten werden nur neu gezeichnet, solange sich etwas bewegt.
- Glas ohne echte Lichtbrechung, Container als eine Geometrie.
- Während die App läuft, pausiert die 3D-Welt.

Gemessen auf Intel Iris Xe: 60 fps in allen Schritten bei 1280 × 720.

Prüfen: `node tools/shots.cjs` fotografiert jeden Schritt (braucht Playwright, z. B. `PW_CHANNEL=chrome` mit installiertem Chrome).

## Offen

- **Produktname** „ReSource Scanner“ aus dem Pitch-Training (`PRODUKTNAME` in `content.js`). In den Unterlagen steht er auch als „RessourceScanner“ und „ResourceScanner“: einheitlich festlegen.
- **„Keine Speicherung von Bildern“** steht im Pitch-Entwurf, ist aber **nicht** auf einer Folie: Das Backend speichert Scans und Fotos laut `docs/backend.md` in SQLite und `STATION_DATA`. Erst klären, dann aufnehmen.
- **QR-Code** zeigt auf die GitHub-Pages-Seite (`kontor2026.github.io/web-app`: Lebensweg, Rohstoff-Atlas, 3D-Modelle). Neues Ziel: `QR_URL` ändern und `assets/qr-app.svg` neu erzeugen.
- **Werkstätten auf der Karte** sind Platzhalter (Großstädte). Echte Liste in `werkstaetten.js` eintragen.
- **Open Source:** Im Repo fehlt noch eine `LICENSE`-Datei. Ohne sie ist der Code zwar öffentlich, aber rechtlich nicht offen. Folie 12 sagt „Open Source“.
- Metallgehalte (Öko-Institut 2012) und CO₂ (Idemat 2026) kommen aus `data/rohstoffe/`. Neuere Handys enthalten oft weniger Gold.
- Für die Live-Demo bleiben etwa 1:10. Braucht sie mehr, ist Schritt 6 (graue Energie) der Kandidat zum Kürzen.
