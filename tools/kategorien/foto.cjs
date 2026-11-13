#!/usr/bin/env node
'use strict';

// Fotografiert Modelle aus tools/kategorien/modelle/ (links zusammengebaut, rechts explodiert).
// Aufruf (Projektordner):  node tools/kategorien/foto.cjs <id> [<id> ...] [--out <ordner>]
// Ausgabe: <ordner>/<id>.png, Standard <tmp>/modell-fotos. Braucht Playwright mit Chromium,
// z. B. aus packages/site (npm ci dort) oder per PLAYWRIGHT_PATH=<pfad zu node_modules/playwright>.
const fs = require('node:fs');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');

const root = path.resolve(__dirname, '..', '..');
const args = process.argv.slice(2);
const oi = args.indexOf('--out');
const outDir = oi >= 0 ? args.splice(oi, 2)[1] : path.join(os.tmpdir(), 'modell-fotos');
const ids = args.length ? args : fs.readdirSync(path.join(__dirname, 'modelle')).map((f) => f.replace(/\.json$/, ''));

function ladePlaywright() {
  const kandidaten = [process.env.PLAYWRIGHT_PATH, 'playwright', 'playwright-core',
    path.join(root, 'packages/site/node_modules/playwright'), '/home/ubuntu/projects/web-app/packages/site/node_modules/playwright'];
  for (const k of kandidaten.filter(Boolean)) {
    try { return require(k); } catch { /* nächster */ }
  }
  throw new Error('Playwright nicht gefunden (siehe Kopf dieser Datei).');
}

const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  const p = path.join(root, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!p.startsWith(root)) { res.writeHead(403); res.end(); return; }
  fs.readFile(p, (e, data) => {
    if (e) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': types[path.extname(p)] || 'application/octet-stream' });
    res.end(data);
  });
});

(async () => {
  const { chromium } = ladePlaywright();
  fs.mkdirSync(outDir, { recursive: true });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const port = server.address().port;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 800 } });
  let fehler = 0;
  for (const id of ids) {
    const errs = [];
    page.removeAllListeners('pageerror');
    page.on('pageerror', (e) => errs.push(e.message));
    await page.goto(`http://127.0.0.1:${port}/tools/kategorien/ansicht.html?static&id=${id}`);
    await page.waitForFunction(() => window.__fertig, null, { timeout: 15000 });
    const f = await page.evaluate(() => window.__fehler);
    if (f || errs.length) { console.error(`${id}: ${f || errs.join('; ')}`); fehler++; continue; }
    const file = path.join(outDir, `${id}.png`);
    await page.screenshot({ path: file });
    console.log(file);
  }
  await browser.close();
  server.close();
  process.exit(fehler ? 1 : 0);
})();
