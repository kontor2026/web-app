// Tipp-Test wie auf einem Handy (390 × 844, Touch): jede wichtige Bedienung muss etwas bewirken.
// Aufruf: npm run build && node scripts/tipptest.mjs
import { createServer } from 'node:http';
import { readFileSync, existsSync, statSync } from 'node:fs';
import { extname, join } from 'node:path';
import { chromium } from 'playwright';

const DIST = new URL('../dist/', import.meta.url).pathname, PORT = 4179, BASIS = `http://localhost:${PORT}/`;
const TYP = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json' };
const server = createServer((req, res) => {
  let f = join(DIST, decodeURIComponent(req.url.split('?')[0]));
  if (existsSync(f) && statSync(f).isDirectory()) f = join(f, 'index.html');
  if (!existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': TYP[extname(f)] ?? 'application/octet-stream' }); res.end(readFileSync(f));
}).listen(PORT);
const env = { ...process.env }; delete env.WAYLAND_DISPLAY; delete env.DISPLAY;
const browser = await chromium.launch({ env, args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });

let ok = 0, schlecht = 0;
async function test(name, fn) {
  const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true });
  page.on('pageerror', (e) => console.log(`    Fehler: ${e.message}`));
  try { await fn(page); ok++; console.log(`  ✓ ${name}`); }
  catch (e) { schlecht++; console.log(`  ✗ ${name}: ${e.message.split('\n')[0]}`); }
  await page.close();
}
const warte = (p, ms = 1500) => p.waitForTimeout(ms);
const erwarte = (bed, text) => { if (!bed) throw new Error(text); };
// Wischen über einem Element (Touch-Ereignisse wie vom Finger)
async function wische(page, sel, dx) {
  await page.evaluate(([sel, dx]) => {
    const el = document.querySelector(sel), r = el.getBoundingClientRect(), x = r.left + r.width / 2, y = r.top + 80;
    const t = (cx) => new Touch({ identifier: 1, target: el, clientX: cx, clientY: y });
    el.dispatchEvent(new TouchEvent('touchstart', { touches: [t(x)], changedTouches: [t(x)], bubbles: true }));
    el.dispatchEvent(new TouchEvent('touchend', { touches: [], changedTouches: [t(x + dx)], bubbles: true }));
  }, [sel, dx]);
}

await test('Start: Beispiel antippen öffnet den Lebensweg', async (p) => {
  await p.goto(BASIS, { waitUntil: 'load' }); await warte(p, 800);
  await p.tap('.beispiel >> text=Smartphone'); await warte(p);
  erwarte(p.url().includes('atlas/#kat=smartphone'), p.url());
});
await test('Lebensweg: Nummer im 3D-Modell antippen wählt das Teil', async (p) => {
  await p.goto(`${BASIS}atlas/#kat=smartphone`, { waitUntil: 'load' }); await warte(p, 3000);
  await p.tap('.ballon >> nth=0'); await warte(p, 500);
  erwarte(await p.locator('#panel .crumbs').count(), 'keine Teil-Ansicht');
});
await test('Lebensweg: Station in der Leiste antippen', async (p) => {
  await p.goto(`${BASIS}atlas/#kat=smartphone`, { waitUntil: 'load' }); await warte(p, 2000);
  await p.tap('.lw-schritte a[data-s="abbau"]'); await warte(p);
  erwarte(p.url().includes('s=abbau'), p.url());
});
await test('Lebensweg: Wischen nach links geht zur nächsten Station', async (p) => {
  await p.goto(`${BASIS}atlas/#kat=smartphone&s=gegenstand`, { waitUntil: 'load' }); await warte(p, 2000);
  await wische(p, '#panel', -160); await warte(p, 800);
  erwarte(p.url().includes('s=upcycling'), p.url());
});
await test('Lebensweg: Materialfluss aufklappen', async (p) => {
  await p.goto(`${BASIS}atlas/#kat=smartphone&s=abbau`, { waitUntil: 'load' }); await warte(p, 2000);
  await p.tap('#strom-auf'); await warte(p, 800);
  erwarte(await p.locator('.lw.strom-offen .strom-svg').count(), 'Materialfluss nicht sichtbar');
});
await test('Lebensweg: Rohstoff antippen zeigt Länder', async (p) => {
  await p.goto(`${BASIS}atlas/#kat=smartphone&s=abbau`, { waitUntil: 'load' }); await warte(p, 2000);
  await p.tap('.lw-chip >> text=Kobalt'); await warte(p);
  erwarte(p.url().includes('r=Co') && (await p.locator('.lw-land >> text=DR Kongo').count()), p.url());
});
await test('Lebensweg: „Hab ich“ legt auf die Werkbank', async (p) => {
  await p.goto(`${BASIS}atlas/#kat=laptop`, { waitUntil: 'load' }); await warte(p, 2500);
  await p.tap('#habich'); await warte(p, 500);
  erwarte((await p.locator('.steps .zaehler').textContent()) === '1', 'Zähler nicht 1');
});
await test('Tab-Leiste: Werkbank antippen', async (p) => {
  await p.goto(BASIS, { waitUntil: 'load' }); await warte(p, 800);
  await p.tap('.steps a[href*="werkbank"]'); await warte(p);
  erwarte(p.url().includes('werkbank/'), p.url());
});
await test('Werkbank: Gegenstand suchen und hinzufügen', async (p) => {
  await p.goto(`${BASIS}werkbank/`, { waitUntil: 'load' }); await warte(p, 800);
  await p.tap('#suche'); await p.fill('#suche', 'Föhn'); await warte(p, 300);
  await p.tap('#treffer button >> nth=0'); await warte(p, 500);
  erwarte(await p.locator('.wb-zeile >> text=Föhn').count(), 'Föhn nicht im Bestand');
});
await test('3D-Modelle: Nummer antippen öffnet das Teil', async (p) => {
  await p.goto(`${BASIS}modelle/#kat=laptop`, { waitUntil: 'load' }); await warte(p, 3000);
  await p.tap('.ballon >> nth=2'); await warte(p, 500);
  erwarte((await p.locator('#panel .eyebrow').first().textContent()).startsWith('Teil'), 'kein Teil gewählt');
});
await test('KI-Kompass: Richtung antippen', async (p) => {
  await p.goto(`${BASIS}kompass/`, { waitUntil: 'load' }); await warte(p, 800);
  await p.tap('.richtung[data-id="datenschutz"]'); await warte(p, 500);
  erwarte(p.url().includes('#datenschutz'), p.url());
});

await browser.close(); server.close();
console.log(`${ok} bestanden, ${schlecht} fehlgeschlagen`);
process.exit(schlecht ? 1 : 0);
