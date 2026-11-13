# Secrets (nicht im Git)

Hier liegen die Zugangsdaten als einzelne Textdateien, nur für Docker Compose:

- `claude_oauth_token.txt`: Token aus `claude setup-token`
- `anthropic_api_key.txt`: API-Schlüssel aus der Claude Console (leer lassen, wenn nicht genutzt)

Anleitung: `docs/claude-sdk.md`. Alles außer dieser README ist per `.gitignore` ausgeschlossen.
