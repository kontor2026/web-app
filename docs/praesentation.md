# 3D-Präsentation

Umgesetzt in `praesentation/`. Ablauf, Zeiten, Tasten, Hosting und das Einbinden der echten App: [praesentation/README.md](../praesentation/README.md).

## Entscheidungen

- **Ein Gegenstand als roter Faden** statt Werkstatt mit Figur: Ein altes Handy führt durch alle Folien. Die Präsentation nutzt dieselben Kategorie-Modelle und Materialfunktionen wie die App (`backend/seed/kategorien`, `packages/site/src/foto.js`), Präsentation und Produkt sehen also gleich aus.
- **AIDA in 5 Minuten, 5 Folien, 15 Schritte.** Jeder Schritt ist eine Kamerafahrt plus eine Animation, die von selbst läuft. Man muss nicht durch Zwischenzustände klicken.
- **Kaum Text:** höchstens ein Satz pro Schritt, dazu Beschriftungen mit Zahlen aus dem Repo (Öko-Institut, Idemat).
- **Jury-Kriterien** (`data/rating.md`) werden gezeigt, nicht als Überschrift genannt. Zuordnung im README.
- **Live-App im Monitor:** Ein iframe liegt per Homografie exakt auf dem 3D-Bildschirm. Am Ende der Fahrt ist es unverzerrt und gestochen scharf, die 3D-Welt pausiert. **X** wechselt von jeder Folie aus in die App und zurück.
- **Mock-App** als Platzhalter, bis feststeht, welche App live läuft (`?app=` oder `APP_URL`).

## Hosting

Lokal mit `node tools/serve.cjs 5181 --public` und einem HTTPS-Tunnel (z. B. `cloudflared tunnel --url http://localhost:5181`). Läuft die echte App unter derselben Adresse (gleiche Herkunft), funktionieren X und F auch aus der App heraus ohne Änderung an der App.
