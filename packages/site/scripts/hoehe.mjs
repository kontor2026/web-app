// Prüft, ob Seiten vertikal scrollen (Handy 390×844 und Bildschirm 1440×900).
import { createServer } from 'node:http';
import { readFileSync, existsSync, statSync } from 'node:fs';
import { extname, join } from 'node:path';
import { chromium } from 'playwright';
const DIST = new URL('../dist/', import.meta.url).pathname, PORT = 4181;
const server = createServer((q, r) => { let f = join(DIST, decodeURIComponent(q.url.split('?')[0])); if (existsSync(f) && statSync(f).isDirectory()) f = join(f, 'index.html');
  if (!existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': { '.js': 'text/javascript', '.html': 'text/html', '.css': 'text/css' }[extname(f)] ?? 'application/octet-stream' }); r.end(readFileSync(f)); }).listen(PORT);
const env = { ...process.env }; delete env.WAYLAND_DISPLAY; delete env.DISPLAY;
const b = await chromium.launch({ env, args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const SEITEN = (process.env.SEITEN ?? 'atlas/#kat=smartphone&s=abbau,atlas/#kat=smartphone&s=gegenstand,atlas/#kat=smartphone&s=upcycling,atlas/#kat=smartphone&s=entsorgung,atlas/#kat=pet_bottle&s=verwertung,atlas/#kat=t_shirt&s=herstellung').split(',');
for (const [w, h, mobil] of [[390, 844, true], [1440, 900, false]]) for (const s of SEITEN) {
  const p = await b.newPage({ viewport: { width: w, height: h }, isMobile: mobil, hasTouch: mobil });
  await p.goto(`http://localhost:${PORT}/${s}`, { waitUntil: 'load', timeout: 90000 }); await p.waitForTimeout(2500);
  const r = await p.evaluate(() => {
    const doc = document.scrollingElement, zu = [];
    for (const el of document.querySelectorAll('main *')) { const cs = getComputedStyle(el); if (/(auto|scroll)/.test(cs.overflowY) && el.scrollHeight > el.clientHeight + 2) zu.push(`${el.tagName.toLowerCase()}.${[...el.classList].join('.')} ${el.scrollHeight}>${el.clientHeight}`); }
    return { seite: doc.scrollHeight - innerHeight, innen: zu };
  });
  console.log(`${w} /${s}: Seite ${r.seite > 1 ? `scrollt ${r.seite}px` : 'ok'}${r.innen.length ? ` · innen: ${r.innen.join('; ')}` : ''}`);
  await p.close();
}
await b.close(); server.close();
