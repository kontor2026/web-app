# Objekt-Schema

Ein Gegenstand ist eine reine Datendatei. Der Renderer (`js/iso.js`) zeichnet daraus die Explosionszeichnung, der Steckbrief und die Bauideen lesen dieselben Daten. Für ein neues Objekt muss kein Code geändert werden.

## Neues Objekt in unter einer Minute

1. Foto plus dieses Schema an ein Sprachmodell geben (Prompt unten).
2. Antwort als `js/data/objects/<id>.js` speichern (oder später: Backend liefert JSON).
3. Import und Eintrag in `js/data/objects/index.js` ergänzen.
4. Prüfen unter `http://localhost:5173/#sheet=<id>` (mit `?static` ohne Animation).

## Felder

```js
{
  id: 'smartphone',                 // URL-tauglich
  name: 'Smartphone',
  klasse: 'Elektroschrott · Kleingerät',
  photo: 'assets/samples/smartphone.jpg',
  erkennung: { conf: 0.97, modelle: [['Apple iPhone 11', 0.61], ...], hinweis: '...' },
  masse: '151 × 76 × 8,3 mm', gewicht: '≈ 194 g',
  werte: [{ k: 'Rohstoffwert', v: '≈ 2 €', hint: '...' }, ...],   // genau 3
  wertvoll: 'Ein Satz, warum das wertvoll ist.',
  kreislauf: [{ t: 'Rohstoffe', d: '...' }, ..., { t: 'Heute oft', d: '...', tone: 'bad' }, { t: 'Besser', d: '...', tone: 'good' }],
  entsorgung: { wo: '...', nicht: '...', warnung: '...' },
  quelle: 'Woher die Zahlen stammen',
  parts: [ /* siehe unten */ ],
  projekte: [ /* siehe unten */ ],
}
```

### Bauteil (`parts[]`)

Maße in Millimetern. `x` = Breite, `y` = Tiefe, `z` = Höhe über dem Tisch. Ein Bauteil ist ein extrudierter Grundriss.

| Feld | Bedeutung |
|---|---|
| `id`, `name`, `short` | `short` erscheint an der Positionsnummer |
| `shape` | `'box'` (abgerundetes Rechteck, Radius `r`) oder `'cyl'` (Ellipse, Durchmesser `w`, optional `d`) |
| `x, y, w, d` | Grundriss: linke hintere Ecke und Größe |
| `z, h` | Unterkante und Dicke |
| `explode` | `[dx, dy, dz]` Versatz im explodierten Zustand. Teile mit gleichem Versatz bewegen sich als Gruppe |
| `materials` | `[['materialId', anteilProzent], ...]`, IDs aus `js/data/catalog.js` |
| `mass` | Gramm, für den Materialmix |
| `info` | 1–2 Sätze für Schüler |
| `color`, `opacity` | optional, sonst Farbe der Materialklasse |
| `marks` | optional, Details auf der Oberseite: `[{ shape, x, y, w, d, r, fill }]` relativ zum Bauteil |
| `label: false` | keine Positionsnummer (z. B. zweiter Lautsprecher) |
| `sortBias` | optional, korrigiert die Zeichenreihenfolge |

Faustregel für `explode`: Ebenen um etwa 40 % der Grundriss-Tiefe in `z` auseinanderziehen. Große flache Objekte (Laptop) lieber seitlich auffächern, damit das Innenleben frei liegt.

### Bauidee (`projekte[]`)

```js
{ titel, kurz, stufe: 1|2|3, dauer: '40 min', lernziel,
  nutzt: [{ neu: true, name: 'Lüfter' }, { inv: 'usb-kabel', menge: 1 }],   // inv-IDs aus js/data/inventory.js
  werkzeug: ['Lötkolben'], schritte: ['...', '...', '...'] }
```

Pflicht: mindestens ein Eintrag mit `neu: true`, damit der mitgebrachte Gegenstand verwendet wird.

## Prompt-Vorlage

```
Du bekommst ein Foto eines Gegenstands aus einer Upcycling-Werkstatt.
Gib ein JavaScript-Objekt nach dem Schema in objekt-schema.md zurück.
- Nutze nur Material-IDs aus dieser Liste: <IDs aus catalog.js>
- Nutze nur Lager-IDs aus dieser Liste: <IDs aus inventory.js>
- 8 bis 14 Bauteile, realistische Maße in mm, Teile innerhalb des Gehäuses.
- Wenn du ein Modell nicht sicher erkennst, nenne 3 Kandidaten mit Wahrscheinlichkeit.
- Schreibe kurze Sätze für Schüler, keine Fachbegriffe ohne Erklärung.
- Erfinde keine Zahlen: Wo du unsicher bist, schreibe „Schätzung“ in hint oder quelle.
```
