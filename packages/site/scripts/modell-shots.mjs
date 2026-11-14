// Screenshots einzelner 3D-Modelle zum Prüfen. Aufruf: npm run build && node scripts/modell-shots.mjs toaster pet_bottle
import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { chromium } from 'playwright';

const PORT = 4174, BASIS = `http://localhost:${PORT}/modelle/#kat=`;
const ids = process.argv.slice(2);
mkdirSync(new URL('../shots/', import.meta.url), { recursive: true });
const server = spawn(process.execPath, ['node_modules/vite/bin/vite.js', 'preview', '--port', String(PORT), '--strictPort'], { cwd: new URL('..', import.meta.url), stdio: 'ignore' });
await new Promise((r) => setTimeout(r, 2500));
const env = { ...process.env };
delete env.WAYLAND_DISPLAY; delete env.DISPLAY;
const browser = await chromium.launch({ env, args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  await page.addInitScript(() => { try { localStorage.setItem('modelle-nummern', 'aus'); } catch {} });
  page.on('pageerror', (e) => console.log(`FEHLER: ${e.message}`));
  page.on('console', (m) => { if (m.type() === 'error') console.log(`console: ${m.text()}`); });
  for (const id of ids) for (const x of ['1', '0']) {
    await page.goto('about:blank');
    await page.goto(BASIS + id, { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);
    if (x === '0') { await page.evaluate(() => document.getElementById('explodiert').click()); await page.waitForTimeout(2500); }
    const f = `shots/modell-${id}-${x === '1' ? 'ex' : 'zu'}.png`;
    await page.locator('#szene').screenshot({ path: f, timeout: 180000 });
    console.log(f);
  }
} finally { await browser.close(); server.kill(); }
