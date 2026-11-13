# Machbarkeit (Stand Hackathon, Tag 1)

Kurzbewertung der drei KI-Schritte. Ziel je Schritt: unter 1 Minute an der Station.

| Schritt | Machbar? | Wie | Dauer (geschätzt) |
|---|---|---|---|
| Bild rein, Gegenstand erkennen | Ja | Vision-Sprachmodell (Claude, Gemini, GPT) über API. Ausgabe: Objektklasse plus Top-3 Modellkandidaten mit Wahrscheinlichkeit. Schüler bestätigt per Klick. | 2–5 s |
| Explosionszeichnung erzeugen | Ja, als Daten statt als Bild | LLM erzeugt JSON nach `docs/objekt-schema.md` (Bauteile, Lage, grobe Maße, Materialien). Der generische Renderer (`js/iso.js`) zeichnet daraus die isometrische Explosionszeichnung. Ergebnis wird pro Modell gecacht. | 10–30 s, danach 0 s |
| Drei Bauideen mit Lagerbestand | Ja | LLM bekommt Lagerliste plus neues Objekt. Pflicht „neues Teil wird verwendet“ wird per Schema geprüft. Empfehlung: kuratierter Projektkatalog (30–50 erprobte Projekte), aus dem die KI auswählt und anpasst. | 5–15 s |

## Was nicht funktioniert

- **Bild-zu-3D-Modelle** (TRELLIS, Hunyuan3D u. a.) erzeugen nur die Außenhülle, kein Innenleben, und brauchen GPU-Zeit im Minutenbereich.
- **Graustufenfoto mit Hotspots** funktioniert nur für sichtbare Teile. Akku, Platine usw. sieht man auf dem Foto nicht. Taugt höchstens als Fallback-Ansicht.
- **Exaktes Modell aus einem Foto** (iPhone 15 vs. 16) ist unsicher. Deshalb Kandidatenliste plus Bestätigung. Später zusätzlich Modellnummer, Etikett oder NIR-Messung.

## Gegen erfundene Fakten

- Bauteillisten pro Gerätemodell aus der iFixit-API (öffentlich, ohne Schlüssel): https://www.ifixit.com/api
- Materialanteile aus Ökobilanzen, z. B. Fairphone 3 LCA (Fraunhofer IZM): https://www.fairphone.com/wp-content/uploads/2020/07/Fairphone_3_LCA.pdf
- Jede Angabe im Schema trägt ein Feld `quelle`. Werte ohne Quelle werden in der UI als „Schätzung“ markiert.
- Mengenangaben qualitativ halten (hoch / mittel / gering), wo keine belastbaren Zahlen vorliegen.

## Hardware

Jetson Xavier NX reicht für Bildklassifikation (z. B. YOLO), nicht für die LLM-Schritte in dieser Qualität. Für das MVP: Cloud-API, Station braucht Internet.
