# 3D-Präsentation (Mockup)

Drei Folien in einer durchgehenden Three.js-Welt: Werkstatt, Flug in den Monitor mit der echten Web-App, technische Umsetzung. Auftrag und Aufbau: [docs/praesentation.md](../docs/praesentation.md).

## Starten

```bash
node tools/serve.cjs            # http://localhost:5181/
```

Die Web-App kommt aus `APP_URL` in `content.js` (Platzhalter `http://localhost:8000/`). Für einen anderen Ort ohne Codeänderung: `http://localhost:5181/?app=https://…/`.

Prüfen mit Screenshots aller Stationen (Playwright): `node tools/shots.cjs`.

## Bedienung

→ ↓ Leertaste Bild↓ weiter, ← ↑ Bild↑ zurück, 1–9 Folie, F Vollbild, H Hilfe, T Sprechertext, R Kamera zurücksetzen, Maus ziehen und Mausrad frei. Klickt man in die App, bekommt sie die Tasten. Ein Klick daneben oder der Knopf „Weiter“ am Rand gibt sie der Präsentation zurück. Unten rechts steht der aktive Modus.

## Dateien

| Datei | Inhalt |
|---|---|
| `index.html` | Canvas, Overlay, Import-Map für Three.js |
| `engine.js` | Renderer, Licht, Kamerafahrten, Label-Anker |
| `world.js` | Werkstatt, Werkbank, Lager, Station mit Kamera und Monitor, Kamera-Stationen |
| `models.js` | Geometrie-Bausteine |
| `content.js` | Folien als Daten, `APP_URL` |
| `app.js` | Navigation, Overlay, Steuerung der eingebetteten App |
| `styles.css` | Overlay, Folientexte, Footer |
| `assets/` | Three.js r170 mit OrbitControls, RoundedBoxGeometry, RoomEnvironment (lokal, läuft offline) |
