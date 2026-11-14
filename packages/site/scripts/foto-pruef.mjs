// Foto-Ansicht eines Modells über den laufenden Vite-Dev-Server (Port 5190) fotografieren.
// Aufruf: node scripts/foto-pruef.mjs <id> <ausgabeordner>  → <ordner>/<id>-ex.png und <id>-zu.png
import { mkdirSync } from 'node:fs';
import { chromium } from 'playwright';
const [id, out = '/tmp/foto-pruef'] = process.argv.slice(2);
// Seitenfoto mit Ausschnitt statt Element-Foto: wartet nicht darauf, dass die (drehende) Ansicht stillsteht
const bereich = (p) => p.evaluate(() => { const r = document.getElementById('szene').getBoundingClientRect(); return { x: r.x, y: r.y, width: r.width, height: r.height }; });
mkdirSync(out, { recursive: true });
const env = { ...process.env }; delete env.WAYLAND_DISPLAY; delete env.DISPLAY;
const b = await chromium.launch({ env, args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
try {
  const p = await b.newPage({ viewport: { width: 1200, height: 800 }, deviceScaleFactor: 1 });
  await p.addInitScript(() => { try { localStorage.setItem('modelle-nummern', 'an'); localStorage.setItem('modelle-drehen', 'aus'); } catch {} });
  p.on('pageerror', (e) => console.log(`FEHLER: ${e.message}`));
  await p.goto(`http://localhost:5190/modelle/?t=${Date.now()}#kat=${id}`, { waitUntil: 'networkidle' });
  await p.waitForTimeout(2500);
  await p.screenshot({ path: `${out}/${id}-ex.png`, clip: await bereich(p), timeout: 600000, animations: 'disabled' });
  await p.evaluate(() => document.getElementById('explodiert').click());
  await p.waitForTimeout(3500);
  await p.screenshot({ path: `${out}/${id}-zu.png`, clip: await bereich(p), timeout: 600000, animations: 'disabled' });
  console.log(`${out}/${id}-ex.png\n${out}/${id}-zu.png`);
} finally { await b.close(); }
