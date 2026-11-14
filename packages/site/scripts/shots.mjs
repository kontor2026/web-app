// Screenshots aller Seiten bei fünf Breiten (wie die Geräteansicht der Chrome-Entwicklertools) und Konsolenfehler.
// Aufruf: npm run build && npm run shots   (DUNKEL=1 zusätzlich dunkel)   → Bilder in shots/
import { createServer } from 'node:http';
import { mkdirSync, readFileSync, existsSync, statSync } from 'node:fs';
import { extname, join } from 'node:path';
import { chromium } from 'playwright';

const PORT = 4175, BASIS = `http://localhost:${PORT}/`;
const SEITEN = [
  ['start', ''], ['lebensweg-wahl', 'atlas/'], ['gegenstand', 'atlas/#kat=smartphone'], ['abbau', 'atlas/#kat=smartphone&s=abbau&r=Co'],
  ['herstellung', 'atlas/#kat=t_shirt&s=herstellung'], ['upcycling', 'atlas/#kat=pet_bottle&s=upcycling'], ['entsorgung', 'atlas/#kat=glass_bottle&s=entsorgung'],
  ['verwertung', 'atlas/#kat=pet_bottle&s=verwertung'], ['modelle', 'modelle/#kat=laptop'], ['kompass', 'kompass/'], ['kompass-n', 'kompass/#transparenz'],
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
  for (const schema of SCHEMAS) for (const [g, viewport] of Object.entries(GROESSEN)) {
    const page = await browser.newPage({ viewport, colorScheme: schema, deviceScaleFactor: 1 });
    page.on('pageerror', (e) => { fehler++; console.log(`  FEHLER ${page.url()}: ${e.message}`); });
    page.on('console', (m) => { if (m.type() === 'error') { fehler++; console.log(`  console ${page.url()}: ${m.text()}`); } });
    for (const [name, pfad] of SEITEN) {
      await page.goto(BASIS + pfad, { waitUntil: 'load', timeout: 60000 });
      await page.waitForTimeout(2200);
      await page.screenshot({ path: `shots/${name}-${g}-${schema}.png`, fullPage: +g <= 768 });
    }
    await page.close();
  }
} finally {
  await browser.close();
  server.close();
}
console.log(`Screenshots in shots/, ${fehler} Fehler`);
process.exit(fehler ? 1 : 0);
