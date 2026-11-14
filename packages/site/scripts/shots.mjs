// Screenshots aller Seiten bei fünf Breiten (wie die Geräteansicht der Chrome-Entwicklertools) und Konsolenfehler.
// Aufruf: npm run build && npm run shots   (DUNKEL=1 zusätzlich dunkel)   → Bilder in shots/
import { createServer } from 'node:http';
import { mkdirSync, readFileSync, existsSync, statSync } from 'node:fs';
import { extname, join } from 'node:path';
import { chromium } from 'playwright';

const PORT = 4175, BASIS = `http://localhost:${PORT}/`;
const SEITEN = [
  ['start', ''], ['lebensweg-wahl', 'atlas/'], ['gegenstand', 'atlas/#kat=smartphone'], ['abbau', 'atlas/#kat=smartphone&s=abbau&r=Co'],
  ['herstellung', 'atlas/#kat=t_shirt&s=herstellung'], ['upcycling', 'atlas/#kat=pet_bottle&s=upcycling'], ['entsorgung', 'atlas/#kat=glass_bottle&s=entsorgung'], ['entsorgung-handy', 'atlas/#kat=smartphone&s=entsorgung'],
  ['verwertung', 'atlas/#kat=pet_bottle&s=verwertung'], ['modelle', 'modelle/#kat=laptop'], ['kompass', 'kompass/'], ['kompass-n', 'kompass/#transparenz'], ['werkbank', 'werkbank/'], ['quelle', 'quelle/?u=https%3A%2F%2Fpubs.usgs.gov%2Fperiodicals%2Fmcs2026%2Fmcs2026.pdf%23page%3D75&t=Mineral%20Commodity%20Summaries%202026&w=Kobalt%20%C2%B7%20Abbau%3A%20DR%20Kongo%2074%20%25&h=U.S.%20Geological%20Survey&j=2025&s=S.%2071'], ['qr', 'qr/'],
];
const GROESSEN = { 390: { width: 390, height: 844 }, 768: { width: 768, height: 1024 }, 1024: { width: 1024, height: 768 },
  1440: { width: 1440, height: 900 }, 1920: { width: 1920, height: 1080 } };
const SCHEMAS = process.env.DUNKEL ? ['light', 'dark'] : ['light'];
// Auswahl zum schnellen Prüfen: NUR=abbau,kompass BREITEN=1024,1440
if (process.env.NUR) SEITEN.splice(0, SEITEN.length, ...SEITEN.filter(([n]) => process.env.NUR.split(',').includes(n)));
if (process.env.BREITEN) for (const g of Object.keys(GROESSEN)) if (!process.env.BREITEN.split(',').includes(g)) delete GROESSEN[g];

mkdirSync(new URL('../shots/', import.meta.url), { recursive: true });
// Kleiner statischer Server für dist/ (ohne Abhängigkeiten, liest jede Datei frisch)
const DIST = new URL('../dist/', import.meta.url).pathname;
const TYP = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png' };
const server = createServer((req, res) => {
  let f = join(DIST, decodeURIComponent(req.url.split('?')[0]));
  if (existsSync(f) && statSync(f).isDirectory()) f = join(f, 'index.html');
  if (!existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': TYP[extname(f)] ?? 'application/octet-stream' });
  res.end(readFileSync(f));
}).listen(PORT);
// Ohne WAYLAND_DISPLAY/DISPLAY (z. B. aus VS Code) verlangt ANGLE sonst Wayland und WebGL fällt aus.
const env = { ...process.env };
delete env.WAYLAND_DISPLAY; delete env.DISPLAY;
const browser = await chromium.launch({ env, args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
let fehler = 0;
try {
  // Je Bild ein neuer Tab: viele WebGL-Seiten in einem Tab erschöpfen den Software-Renderer
  for (const schema of SCHEMAS) for (const [g, viewport] of Object.entries(GROESSEN)) for (const [name, pfad] of SEITEN) {
    const handy = +g <= 768;   // wie ein echtes Gerät: Touch, mobiler Modus
    const page = await browser.newPage({ viewport, colorScheme: schema, deviceScaleFactor: handy ? 2 : 1, isMobile: handy, hasTouch: handy });
    // Beispiel-Werkbank, damit Shop und Zähler gefüllt sind
    await page.addInitScript(() => localStorage.setItem('werkbank', JSON.stringify({ smartphone: 1, pet_bottle: 3, laptop: 1, yogurt_cup: 4, hair_dryer: 1 })));
    page.on('pageerror', (e) => { fehler++; console.log(`  FEHLER ${page.url()}: ${e.message}`); });
    page.on('console', (m) => { if (m.type() === 'error') { fehler++; console.log(`  console ${page.url()}: ${m.text()}`); } });
    await page.goto(BASIS + pfad, { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(+(process.env.WARTE ?? 2200));
    await page.screenshot({ path: `shots/${name}-${g}-${schema}.png`, fullPage: +g <= 768, timeout: 120000 });
    await page.close();
  }
} finally {
  await browser.close();
  server.close();
}
console.log(`Screenshots in shots/, ${fehler} Fehler`);
process.exit(fehler ? 1 : 0);
