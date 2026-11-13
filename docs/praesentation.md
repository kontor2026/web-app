# Übergabe: 3D-Präsentation (Mockup, 3 Folien)

Ziel: testen, ob die Web-App in einer gehosteten 3D-Präsentation eingebettet und voll bedienbar ist. Nur ein Mockup, keine Details.

## Vorlagen (zuerst ansehen)

- Lokal: `C:\Users\maxim\Documents\Studium\Kuka\3D-Praesentation` (`site/`, `tools/`, `Spickzettel.md`, `screenshots/`)
- GitHub: https://github.com/bpachniewsk1/waste_management/tree/main/modules/m5_docs_pitch/pitch/3d-deck

Technik und Aufbau von dort übernehmen, nicht neu erfinden.

## Folien

1. **Werkstatt:** Kamera geht in die Werkstatt hinein, schwenkt über Werkbank und Werkzeuge, fährt auf die Station mit dem Bildschirm zu. Einfache Platzhalter-Geometrie reicht.
2. **In den Bildschirm:** Kamera zoomt in den Monitor. Dort läuft die **echte Web-App per iframe**, voll klickbar (Scannen, Steckbrief, Bauen). Die URL ist konfigurierbar (eine Konstante, z. B. `APP_URL`). Bis die öffentliche URL feststeht: Platzhalter `https://example.org`, lokal `http://localhost:8080`.
3. **Technische Umsetzung:** eine schlichte Folie: Frontend, Backend, Inferenz (3 Container), KI-Anbieter (lokal / Claude), Kategorie-Modelle, Rohstoff-Datenbank. Stichpunkte reichen, Details in `docs/backend.md`.

## Bedienung

- **Pfeil rechts / Leertaste:** nächste Folie, **Pfeil links:** zurück.
- Solange die Maus über der eingebetteten App ist oder sie den Fokus hat, darf die Leertaste nicht weiterblättern. Deshalb zusätzlich einen kleinen „Weiter“-Knopf am Rand und `Esc`, um den Fokus aus dem iframe zu holen.

## Hosting

- Die Präsentation muss öffentlich im Internet laufen (z. B. GitHub Pages oder Claude-Artefakt).
- Die Web-App muss das Einbetten erlauben: kein `X-Frame-Options: DENY` und keine `frame-ancestors`-Sperre im nginx (`docker/frontend/nginx.conf`). Beide Seiten über HTTPS, sonst blockiert der Browser das iframe.
- Der erste Test ist bestanden, wenn in der gehosteten Präsentation ein Beispielfoto angeklickt werden kann und der Steckbrief erscheint.

## Ablage

Eigener Ordner `praesentation/` in diesem Repo. Kleine Commits, vor dem Push `git pull --rebase`.

## Achtung Verbrauch

Das Abo-Kontingent ist knapp. Die KI im Backend ist abgeschaltet (`LLM_MODE=mock`). Für die Präsentation reichen die Beispielfotos und Kategorie-Modelle, die ohne KI funktionieren.
