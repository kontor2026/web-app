// Foto-Ansicht eines Modells über den laufenden Vite-Dev-Server (Port 5190) fotografieren.
// Aufruf: node scripts/foto-pruef.mjs <id> <ausgabeordner>  → <ordner>/<id>-ex.png und <id>-zu.png
import { mkdirSync } from 'node:fs';
import { chromium } from 'playwright';
const [id, out = '/tmp/foto-pruef'] = process.argv.slice(2);
mkdirSync(out, { recursive: true });
const env = { ...process.env }; delete env.WAYLAND_DISPLAY; delete env.DISPLAY;
const b = await chromium.launch({ env, args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
try {
  const p = await b.newPage({ viewport: { width: 1200, height: 800 }, deviceScaleFactor: 1 });
  await p.addInitScript(() => { try { localStorage.setItem('modelle-nummern', 'an'); } catch {} });
  p.on('pageerror', (e) => console.log(`FEHLER: ${e.message}`));
  await p.goto(`http://localhost:5190/modelle/?t=${Date.now()}#kat=${id}`, { waitUntil: 'networkidle' });
  await p.waitForTimeout(2500);
  await p.locator('#szene').screenshot({ path: `${out}/${id}-ex.png`, timeout: 240000 });
  await p.evaluate(() => document.getElementById('explodiert').click());
  await p.waitForTimeout(2000);
  await p.locator('#szene').screenshot({ path: `${out}/${id}-zu.png`, timeout: 240000 });
  console.log(`${out}/${id}-ex.png\n${out}/${id}-zu.png`);
} finally { await b.close(); }
