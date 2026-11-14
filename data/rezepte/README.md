# Rezepte

Upcycling- und Recycling-Rezepte für die Kreislauf-Station (Werkstatt mit Precious-Plastic-Maschinen, Schülerinnen und Schüler 12–18).
Für jedes Rezept gibt es eine JSON-Datei. Der Dateiname ist die Rezept-ID (ASCII, kebab-case).

## Einordnung

Die Rezepte gehören zu den oberen Stufen der Abfallhierarchie nach § 6 Abs. 1 KrWG:
Vermeidung, Vorbereitung zur Wiederverwendung, Recycling, sonstige Verwertung, Beseitigung.
Ausgebaute Bauteile (Motor, Lautsprecher, LED, Magnete, Stoff) entsprechen der *Wiederverwendung*.
Geschredderter und neu geformter Kunststoff entspricht dem *Recycling*.
Quelle: https://www.gesetze-im-internet.de/krwg/__6.html (abgerufen 2026-11-14)

## Format

| Feld | Bedeutung |
|---|---|
| `titel` | Name des Rezepts |
| `kurz` | ein Satz |
| `braucht` | 1–4 Einträge: `component_id` (aus `data/classifier.json`), `menge` (Stückzahl), optional `oder` (austauschbare Komponenten aus demselben Material), `gramm` (nur wenn die Quelle eine Grammzahl nennt) und `hinweis` |
| `werkzeug` | Methoden-IDs aus `processing_methods` / `manufacturing_methods` der verwendeten Materialien |
| `dauer`, `stufe` | Zeitbedarf, Schwierigkeit 1–3 |
| `schritte` | max. 5 Schritte, je max. 12 Wörter |
| `sicherheit` | ein Satz oder `null` |
| `quelle` | `titel`, `url`, `abgerufen`: eine Anleitung, die abgerufen wurde und den Kern des Rezepts belegt |

Stückzahlen für geschredderten Kunststoff sind Schätzungen. Alternativen aus `oder` werden nach Gewicht abgewogen.

## Sicherheitsregeln (gelten für alle Rezepte)

- Lithium- und Alkaline-Batterien nie öffnen und nie wiederverwenden. Akkus entfernt nur die Lehrkraft.
- Nie an Netzspannung arbeiten. Schaltungen laufen nur mit 5 V (USB) oder einer neuen 9-V-Blockbatterie.
- PVC nie verbrennen oder schmelzen. Kabelisolierung wird nur mechanisch abgezogen.
- Beheizte Maschinen (Spritzguss, Extruder, 3D-Druck-Filament) nur mit Lehrkraft, Hitzeschutzhandschuhen, Schutzbrille und Absaugung bedienen.
