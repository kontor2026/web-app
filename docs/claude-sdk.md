# Übergabe: Claude über das Claude Agent SDK (Abo-Zugang)

Die Station kann Erkennung, Steckbrief und Bauideen mit Claude rechnen statt mit dem lokalen Modell. Diese Datei erklärt, wie der Zugang **sicher hinterlegt** wird, lokal und im Deployment.

## Drei Anbieter

| `LLM_PROVIDER` | Zugang | Wann |
|---|---|---|
| `lokal` | keiner, Ollama im Inferenz-Container | offline, langsam auf CPU |
| `claude` | API-Schlüssel aus der Claude Console (`ANTHROPIC_API_KEY`), Abrechnung pro Token | Standard für ein echtes Deployment |
| `claude-abo` | Token eines Claude-Abos (`CLAUDE_CODE_OAUTH_TOKEN`) über das Claude Agent SDK | nur mit Freigabe von Anthropic, z. B. privater Test |

**Wichtig zu `claude-abo`:** Anthropic erlaubt Abo-Zugänge in eigenen Produkten nur mit vorheriger Freigabe ([Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview)). Für dieses Projekt liegt laut Kontoinhaber eine Freigabe für einen privaten Test vor. Ohne Freigabe: `LLM_PROVIDER=claude` mit API-Schlüssel.

## Was die App mit dem Zugang macht

- Die App nutzt **nur** ein ausdrücklich hinterlegtes Token, nie eine persönliche Claude-Code-Anmeldung auf dem Rechner. Der SDK-Prozess bekommt ein eigenes, leeres Konfigurationsverzeichnis (`CLAUDE_CONFIG_DIR`). Getestet: Ein ungültiges Token führt zu „401 OAuth access token is invalid“, die App weicht nicht auf `~/.claude` aus.
- Alle Claude-Code-Werkzeuge (Dateien, Shell, Web) sind abgeschaltet. Einstellungen und `CLAUDE.md` des Rechners werden nicht geladen (`setting_sources=[]`). Claude bekommt nur Bild, Text und ein JSON-Schema.
- Ein gesetzter `ANTHROPIC_API_KEY` hätte in Claude Code Vorrang vor dem Token. Im Modus `claude-abo` entfernt die App ihn deshalb aus der Umgebung des SDK-Prozesses.
- Code: `backend/app/llm_claude_abo.py` (Abo), `backend/app/llm_claude.py` (API-Schlüssel), `backend/app/config.py` → `secret()`.

## Token erzeugen

Nur die Person, der das Abo gehört, macht das. Einmal, auf einem eigenen Rechner mit installiertem Claude Code:

```bash
claude setup-token
```

Der Browser öffnet die Anmeldung, danach steht das Token im Terminal. Es ist **ein Jahr gültig** und wird nirgends gespeichert. Direkt weiter zu „Hinterlegen“, nicht in Chats, Tickets, Commits oder Screenshots kopieren.

Das Token gibt Zugriff auf das Kontingent des Abos. Alles, was die Station rechnet, zählt gegen dieselben Limits wie die eigene Nutzung von Claude.

## Hinterlegen

Die App liest Zugangsdaten über `secret()` in dieser Reihenfolge:

1. `NAME_FILE`: Pfad zu einer Datei mit dem Wert (bevorzugt, z. B. Docker-Secret)
2. `NAME`: Umgebungsvariable

`NAME` ist `CLAUDE_CODE_OAUTH_TOKEN` bzw. `ANTHROPIC_API_KEY`. Nie in den Code, nie ins Image, nie in `.env` oder `docker-compose.yml` schreiben.

### Docker Compose (Station, Server)

```bash
# im Projektordner; secrets/ ist per .gitignore ausgeschlossen
printf '%s' 'HIER-DAS-TOKEN' > secrets/claude_oauth_token.txt
chmod 600 secrets/claude_oauth_token.txt          # Linux: nur der Besitzer darf lesen
```

In `.env`: `LLM_PROVIDER=claude-abo`. Dann `docker compose up -d`. Compose bindet die Datei als Secret unter `/run/secrets/claude_oauth_token` ein, die App liest sie über `CLAUDE_CODE_OAUTH_TOKEN_FILE`. Das Secret liegt nicht im Image und taucht nicht in `docker inspect` als Umgebungsvariable auf.

Prüfen, ohne das Token zu zeigen:

```bash
curl -s localhost:8080/api/health
```

Erwartet: `"ok": true, "modus": "claude-abo"`. Bei `"Kein Abo-Token hinterlegt"` fehlt die Datei oder sie ist leer.

### Lokale Entwicklung ohne Docker

Token als Datei außerhalb des Projektordners ablegen und den Pfad übergeben:

```bash
# PowerShell
$env:LLM_PROVIDER = "claude-abo"
$env:CLAUDE_CODE_OAUTH_TOKEN_FILE = "$HOME\.station\claude_oauth_token.txt"
backend/.venv/Scripts/python -m uvicorn backend.app.main:app --port 8000
```

### Andere Plattformen

| Plattform | Wo das Token hingehört |
|---|---|
| Docker Swarm | `docker secret create claude_oauth_token -` und im Stack als Secret einbinden |
| Kubernetes | `Secret`, als Datei gemountet, Pfad in `CLAUDE_CODE_OAUTH_TOKEN_FILE` |
| systemd (ohne Docker) | `EnvironmentFile=/etc/station/claude.env` mit Rechten `600`, Besitzer root |
| Cloud (Render, Fly, Railway …) | „Secrets“ bzw. „Environment“ des Dienstes, nie im Repository |
| GitHub Actions | Nicht nötig: Die Images werden **ohne** Token gebaut. Das Token kommt erst beim Start auf dem Zielrechner dazu. |

## Abschalten, wechseln, widerrufen

- **KI sofort abschalten** (z. B. wenn das Abo-Limit knapp wird): `LLM_MODE=mock`, Backend neu starten. Kategorien, Steckbriefe, Rohstoffwerte und Foto-Abgleich laufen weiter, nur neue KI-Anfragen nicht.
- **Auf API-Schlüssel wechseln:** Schlüssel nach `secrets/anthropic_api_key.txt`, `LLM_PROVIDER=claude`.
- **Token ersetzen:** neues Token erzeugen, Datei überschreiben, Container neu starten (`docker compose up -d --force-recreate backend`).
- **Token kompromittiert:** sofort ein neues erzeugen und das alte im Claude-Konto widerrufen. Kann es nicht widerrufen werden, das Passwort ändern und alle Sitzungen abmelden.

## Checkliste vor einem Deployment

- [ ] Freigabe für Abo-Nutzung vorhanden, sonst `LLM_PROVIDER=claude`
- [ ] Token nur in `secrets/` bzw. im Secret-Store der Plattform, Dateirechte `600`
- [ ] `git status` zeigt keine Token-Datei. `secrets/*` steht in `.gitignore`
- [ ] Image enthält kein Token: `docker run --rm ghcr.io/kontor2026/web-app-backend env` zeigt weder Token noch Schlüssel
- [ ] `/api/health` meldet `ok: true` mit dem richtigen Modus
- [ ] Jemand behält das Abo-Limit im Blick und weiß, wie man mit `LLM_MODE=mock` abschaltet
