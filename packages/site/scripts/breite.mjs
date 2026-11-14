// Prüft auf dem Handy (390 px), ob irgendetwas seitlich übersteht (kein horizontales Scrollen erlaubt).
import { createServer } from 'node:http';
import { readFileSync, existsSync, statSync } from 'node:fs';
import { extname, join } from 'node:path';
import { chromium } from 'playwright';
const DIST = new URL('../dist/', import.meta.url).pathname, PORT = 4180;
const server = createServer((q, r) => { let f = join(DIST, decodeURIComponent(q.url.split('?')[0])); if (existsSync(f) && statSync(f).isDirectory()) f = join(f, 'index.html');
  if (!existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': { '.js': 'text/javascript', '.html': 'text/html', '.css': 'text/css' }[extname(f)] ?? 'application/octet-stream' }); r.end(readFileSync(f)); }).listen(PORT);
const env = { ...process.env }; delete env.WAYLAND_DISPLAY; delete env.DISPLAY;
const b = await chromium.launch({ env, args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const SEITEN = ['', 'atlas/#kat=smartphone&s=abbau', 'atlas/#kat=smartphone&s=gegenstand', 'atlas/#kat=smartphone&s=entsorgung', 'atlas/#kat=pet_bottle&s=verwertung', 'atlas/#kat=t_shirt&s=herstellung', 'atlas/#kat=pet_bottle&s=upcycling', 'werkbank/', 'werkbank/#bauen', 'modelle/#kat=laptop', 'kompass/', 'kompass/#transparenz'];
let schlecht = 0;
for (const s of SEITEN) {
  const p = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  await p.goto(`http://localhost:${PORT}/${s}`, { waitUntil: 'load', timeout: 90000 }); await p.waitForTimeout(2500);
  const r = await p.evaluate(() => {
    const W = document.documentElement.clientWidth, zu = [];
    for (const el of document.querySelectorAll('body *')) {
      const b = el.getBoundingClientRect();
      if (b.width && (b.right > W + 1 || b.left < -1) && getComputedStyle(el).position !== 'fixed' && !el.closest('.vorschau-buehne, .labels, canvas'))
        zu.push(`${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''}.${[...el.classList].join('.')} ${Math.round(b.left)}…${Math.round(b.right)}`);
    }
    return { scroll: document.documentElement.scrollWidth > W, zu: zu.slice(0, 6) };
  });
  if (r.scroll || r.zu.length) { schlecht++; console.log(`✗ /${s}  scrollWidth>${390}: ${r.scroll}\n    ${r.zu.join('\n    ')}`); } else console.log(`✓ /${s}`);
  await p.close();
}
await b.close(); server.close();
console.log(schlecht ? `${schlecht} Seiten mit Überstand` : 'kein Überstand');
