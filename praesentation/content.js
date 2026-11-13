// All slides as data. Each step points to a camera station ("shot") in world.js.
// Optional per step: `labels` (anchor ids from world.js) and `app` ('monitor' = app on the monitor,
// 'full' = app fills the screen).

// Placeholder until the public URL of the web app is fixed. Override per link with ?app=<url>.
export const APP_URL = new URLSearchParams(location.search).get('app') || 'http://localhost:8000/';

export const slides = [
  {
    id: 'werkstatt',
    layout: 'hero',
    title: 'Werkstatt',
    steps: [
      { shot: 'tuer', name: 'Ankommen' },
      { shot: 'werkbank', name: 'Werkbank', labels: ['werkbank', 'lager'] },
      { shot: 'station', name: 'Station', labels: ['kamera', 'scanflaeche', 'monitor'] },
    ],
    html: `
      <p class="kicker">Kreislauf-Station</p>
      <h1>Die Werkstatt</h1>
      <p class="lead">Mitgebrachter Müll wird hier gescannt, verstanden und weiterverbaut.</p>`,
    notes: 'Wir kommen durch die Tür in die Werkstatt. Links Werkbank, Werkzeug und Lager, rechts die Station mit Kamera über der Scan-Fläche und dem Monitor.',
  },
  {
    id: 'bildschirm',
    layout: 'app',
    title: 'In den Bildschirm',
    steps: [
      { shot: 'monitor', name: 'Monitor', app: 'monitor' },
      { shot: 'bildschirm', name: 'Live-App', app: 'full' },
    ],
    html: `
      <p class="kicker">Live</p>
      <h2>In den Bildschirm</h2>`,
    notes: 'Das ist die echte Web-App, live. Beispielfoto anklicken, Steckbrief zeigen, dann Bauen. Mit dem Weiter-Knopf am Rand oder einem Klick neben die App geht es zurück in die Präsentation.',
  },
  {
    id: 'technik',
    layout: 'text',
    title: 'Technische Umsetzung',
    steps: [{ shot: 'ueberblick', name: 'Überblick' }],
    html: `
      <p class="kicker">Technik</p>
      <h2>Technische Umsetzung</h2>
      <ul>
        <li><b>Frontend</b> Web-App ohne Build, läuft im Browser an der Station</li>
        <li><b>Backend</b> FastAPI-Pipeline, SQLite für Gegenstände, Lager und Scans</li>
        <li><b>Inferenz</b> lokales Vision-Modell mit Ollama, alles in drei Docker-Containern</li>
        <li><b>KI-Anbieter</b> lokal oder Claude, umschaltbar über <code>LLM_PROVIDER</code></li>
        <li><b>Kategorie-Modelle</b> 201 Kategorien mit 3D-Explosionszeichnung, 318 Komponenten, 41 Materialien</li>
        <li><b>Rohstoff-Datenbank</b> Metallgehalte (Öko-Institut), CO₂ (Idemat 2026), Metallpreise</li>
      </ul>`,
    notes: 'Drei Container: Frontend mit nginx, Backend mit der Pipeline, Inferenz mit dem lokalen Modell. Die KI lässt sich zwischen lokal und Claude umschalten.',
  },
];
