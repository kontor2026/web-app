# Übergabe: 3D-Präsentation (Mockup, 3 Folien)

Ziel: testen, ob die Web-App in einer gehosteten 3D-Präsentation eingebettet und voll bedienbar ist. Nur ein Mockup, keine Details.

## Framework (so ist die Vorlage gebaut, genauso nachbauen)

Reines HTML/JS ohne Build-Framework, **Three.js** als ES-Modul, eine einzige durchgehende 3D-Welt. Folien sind **Kamerafahrten und Zustandswechsel in dieser Welt**, keine getauschten Szenen.

```
praesentation/
  index.html     Canvas für die 3D-Welt + HTML-Overlay für Folientexte, lädt <script type="module" src="app.js">
  engine.js      Renderer, Licht/Studio-Umgebung, Kamera-Regie (Fahrten mit Easing), Label-Anker
  world.js       baut die Welt (Werkstatt, Werkbank, Werkzeuge, Station mit Monitor) und definiert die Kamera-Stationen ("shots")
  models.js      einfache Geometrie-Bausteine (abgerundete Boxen etc.)
  content.js     alle Folien als Daten: export const slides = [{ id, layout, title, steps: [{ shot, name }], html, notes }]
  app.js         Navigation: Tasten, Folien/Schritte, Overlay-Text, iframe-Steuerung
  styles.css     Overlay, Folientexte, Footer
  assets/        three.module.js und Hilfsmodule lokal mitliefern (kein CDN, läuft auch offline)
tools/
  serve.cjs      kleiner lokaler Server zum Entwickeln
  shots.cjs      Screenshots aller Stationen (Playwright) zum Prüfen
```

Prinzipien aus der Vorlage:
- `content.js` enthält nur Daten. Jede Folie hat `steps`, jeder Schritt verweist auf eine Station (`shot`) in `world.js`. Ein Tastendruck geht zum nächsten Schritt, am Ende einer Folie zur nächsten Folie.
- Kamerafahrten werden in `engine.js` mit einer Easing-Funktion zwischen Stationen interpoliert, die Welt bleibt stehen.
- Tasten wie in der Vorlage: → ↓ Leertaste Bild↓ weiter, ← ↑ Bild↑ zurück, 1–9 direkt zur Folie, F Vollbild, H Hilfe, T Sprechertext, R Kamera zurücksetzen. Maus ziehen/Mausrad dreht und zoomt frei.
- Footer unten rechts zeigt den aktiven Modus.

## Folien

1. **Werkstatt:** Kamera kommt durch die Tür in die Werkstatt, schwenkt über Werkbank und Werkzeuge und fährt auf die Station mit Kamera und Monitor zu. Platzhalter-Geometrie aus `models.js` reicht.
2. **In den Bildschirm:** Kamerafahrt in den Monitor, bis er formatfüllend ist. Dann wird über dem Monitor ein **HTML-`<iframe>` mit der echten Web-App** eingeblendet, voll klickbar (Scannen, Steckbrief, Bauen). Die URL steht als eine Konstante `APP_URL` in `content.js`. Bis die öffentliche URL feststeht, dort ein Platzhalter eintragen. Umsetzung: iframe im Overlay, Position und Größe pro Frame aus den Bildschirm-Ecken des Monitors berechnen (3D-Punkte → Bildschirmkoordinaten) oder bei voller Nähe einfach vollflächig. Three.js-`CSS3DRenderer` ist die Alternative, wenn das iframe perspektivisch im Raum hängen soll.
3. **Technische Umsetzung:** schlichte Textfolie: Frontend, Backend, Inferenz (3 Container), KI-Anbieter (lokal oder Claude), Kategorie-Modelle, Rohstoff-Datenbank. Stichpunkte reichen.

## Bedienung mit eingebetteter App

- Klickt man in die App, bekommt das iframe den Fokus und die Präsentation sieht keine Tasten mehr. Deshalb: kleiner „Weiter“-Knopf am Rand, und `Esc` bzw. ein Klick außerhalb holt den Fokus zurück (`window.focus()`).
- Die Leertaste blättert nicht, solange die App den Fokus hat.

## Hosting

- Die Präsentation ist statisch und läuft auf GitHub Pages oder als Claude-Artefakt (Three.js dann als Datei mitliefern oder von einem erlaubten CDN laden).
- Die Web-App muss das Einbetten erlauben: kein `X-Frame-Options: DENY` und keine `frame-ancestors`-Sperre im nginx des Frontend-Containers. Beide Seiten über HTTPS, sonst blockiert der Browser das iframe.
- Erster Test bestanden, wenn in der gehosteten Präsentation ein Beispielfoto angeklickt werden kann und der Steckbrief erscheint.

## Ablage

Eigener Ordner `praesentation/` in diesem Repo. Kleine Commits, vor dem Push `git pull --rebase`.

## Achtung Verbrauch

Das Abo-Kontingent ist knapp. Die KI im Backend ist abgeschaltet (`LLM_MODE=mock`). Für die Präsentation reichen Beispielfotos und Kategorie-Modelle, die ohne KI funktionieren.
