# Rohstoff-Datenbank der 201 Kategorien

Eigene kleine Datenbank, damit Edelmetalle, CO₂ und Rohstoffwert nicht geschätzt, sondern aus Quellen kommen. Jeder Wert im Steckbrief trägt seine Herkunft (Feld `rohstoffe.herkunft`).

| Datei | Inhalt | Quelle |
|---|---|---|
| `quellen.json` | vollständige Zitate | |
| `elektronik.json` | Metallgehalte je Gerät (Smartphone, Notebook, Monitor, Fernseher) und je kg Leiterplatte | Öko-Institut 2012, Tab. 9, 12, 13, 15, 23, 25 |
| `materialien.json` | CO₂ je kg für alle 41 Materialien aus `data/classifier.json`, Neuware und Recyclat, mit Datensatz-Nummer | Idemat 2026 (TU Delft) |
| `preise.json` | Metallpreise in €/g mit Stand | Westmetall, 13.11.2026 |

## Rechenweg (`tools/kategorien/rohstoffe.py`)

1. **Massen je Material** aus dem 3D-Modell der Kategorie (`mass` und `material_id` der Teile).
2. **Edelmetalle (Au, Ag, Pd):** Gerätewert aus der Studie, wenn vorhanden. Sonst Masse der Leiterplatten × Konzentration: IT-Geräte mit Notebook-Motherboard-Werten (Umicore 2011), übrige mit Fernseher-Leiterplatten-Werten (FEM & IUTA 2011).
3. **Kobalt:** Gerätewert, sonst Akkumasse × 13,7 % (Schätzung, abgeleitet aus Tab. 25).
4. **Kupfer, Aluminium, Eisen, Nickel:** aus den Modellmassen. Das sind Schätzungen, so genau wie das Modell.
5. **CO₂:** Masse × Idemat-Faktor. „Mit Recyclat“ setzt den Recyclat-Faktor ein, wo Idemat einen hat.
6. **Rohstoffwert:** Metallmassen × Preis. Palladium, Kobalt und Platin haben noch keinen Preis und fehlen im Wert. Das steht im Steckbrief dabei.

Neu berechnet wird mit `python tools/kategorien/build.py`. Genauere Modelle (siehe `docs/3d-modelle.md`) verbessern die Werte automatisch.

## Grenzen

- Die Studie stammt von 2012. Neuere Geräte enthalten oft weniger Gold und Silber.
- CO₂ umfasst nur die Materialien, nicht Montage, Chips und Transport. Herstellerangaben für ganze Geräte liegen deshalb höher (Smartphone laut Apple etwa 70 kg).
- Ohne Faktor: Knopfzelle, Paraffin, Grafit-Ton-Mine (`null` in `materialien.json`).
- Idemat steht unter CC BY-NC: frei für Bildung und Forschung, Quelle nennen.

## Herkunft der Rohstoffe (`herkunft.json`, `laender.json`)

Länderanteile je Rohstoff für zwei Stufen: `abbau` (Bergwerk, Feld, Wald) und `verarbeitung` (Raffination, Schmelze, Trennung). Jede Stufe nennt `quelle` (Schlüssel in `quellen.json`), `jahr`, `seite` und in `was`, was genau gezählt wird. Anteile in %, `rest` = übrige Länder, zusammen 100. `kritisch` folgt Verordnung (EU) 2024/1252, Anhang II.

Quellen: USGS Mineral Commodity Summaries 2026 (Förderung 2025), EU-Studie zu kritischen Rohstoffen 2023 (Anhang 7, Mittel 2016–2020), USDA PSD (Baumwolle). Ohne Quelle bleibt eine Stufe leer, es wird nichts geschätzt. Noch offen: Erdöl, Erdgas, Wolle, Leder, Zellstoff sowie die Verarbeitung von Silber, Gold, Tantal, Graphit.

`laender.json` ordnet ISO-3-Codes deutsche Namen und die ISO-Nummer zu (= `id` in world-atlas, für den Globus im Rohstoff-Atlas, `packages/site`).
