# Kreislauf-Station (Mockup)

Web-App für eine Scan-Station in der Werkstatt: Gegenstand scannen, Explosionszeichnung mit Materialsteckbrief ansehen, dann einlagern oder daraus etwas bauen.

## Starten

Kein Build nötig, nur ein statischer Server:

```bash
python -m http.server 5173
```

Dann http://localhost:5173 öffnen.

Direkteinstiege für Demo und Entwicklung:

- `#sheet=smartphone` öffnet den Steckbrief (auch `laptop`, `netzteil`, `flasche`)
- `#craft=flasche` öffnet die Bauideen
- `?static` zeigt die Explosionszeichnung ohne Animation

## Drei Zustände

1. **Erfassen**: Kamera, Bild-Upload oder Beispielfoto. Erkennung ist simuliert, mit Kandidatenliste zum Bestätigen.
2. **Steckbrief**: interaktive Explosionszeichnung. Hover zeigt das Bauteil, Klick führt bis zum Element: Gegenstand → Bauteil → Material → Element.
3. **Bauen**: drei Ideen, die den neuen Gegenstand plus Material aus dem Lager nutzen.

## Aufbau

```
index.html
css/app.css
js/main.js            Zustände, Ansichten, Dialoge
js/iso.js             generischer Renderer für isometrische Explosionszeichnungen
js/data/catalog.js    Materialklassen, Materialien, Elemente
js/data/inventory.js  Lager (Mock)
js/data/objects/      ein File pro Gegenstand
vendor/               anime.js 4.5.0
docs/                 Machbarkeit und Objekt-Schema
```

Neue Gegenstände: siehe [docs/objekt-schema.md](docs/objekt-schema.md). Alle Zahlen sind Richtwerte für das Mockup und noch nicht verifiziert.
