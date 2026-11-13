// Screenshots aller Seiten zum Prüfen (hell/dunkel, Desktop/Handy) und Konsolenfehler.
// Aufruf: npm run build && npm run shots   → Bilder in shots/
import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { chromium } from 'playwright';

const PORT = 4173, BASIS = `http://localhost:${PORT}/`;
const SEITEN = [
  ['start', ''], ['atlas', 'atlas/'], ['atlas-smartphone', 'atlas/#kat=smartphone'], ['atlas-kobalt', 'atlas/#kat=smartphone&r=Co'],
  ['atlas-flasche', 'atlas/#kat=pet_bottle'], ['modelle', 'modelle/#kat=smartphone'], ['modelle-flasche', 'modelle/#kat=pet_bottle'],
  ['kompass', 'kompass/'], ['kompass-transparenz', 'kompass/#transparenz'],
];
const GROESSEN = { desktop: { width: 1440, height: 900 }, handy: { width: 390, height: 844 } };

mkdirSync(new URL('../shots/', import.meta.url), { recursive: true });
const server = spawn('npx', ['vite', 'preview', '--port', String(PORT), '--strictPort'], { cwd: new URL('..', import.meta.url), stdio: 'ignore' });
await new Promise((r) => setTimeout(r, 2500));
// Ohne WAYLAND_DISPLAY/DISPLAY (z. B. aus VS Code) verlangt ANGLE sonst Wayland und WebGL fällt aus.
const env = { ...process.env };
delete env.WAYLAND_DISPLAY; delete env.DISPLAY;
const browser = await chromium.launch({ env, args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
let fehler = 0;
try {
  for (const schema of ['light', 'dark']) for (const [g, viewport] of Object.entries(GROESSEN)) {
    const page = await browser.newPage({ viewport, colorScheme: schema, deviceScaleFactor: 1 });
    page.on('pageerror', (e) => { fehler++; console.log(`  FEHLER ${page.url()}: ${e.message}`); });
    page.on('console', (m) => { if (m.type() === 'error') { fehler++; console.log(`  console ${page.url()}: ${m.text()}`); } });
    for (const [name, pfad] of SEITEN) {
      await page.goto(BASIS + pfad, { waitUntil: 'networkidle' });
      await page.waitForTimeout(2200);
      await page.screenshot({ path: `shots/${name}-${g}-${schema}.png`, fullPage: g === 'handy' });
    }
    await page.close();
  }
} finally {
  await browser.close();
  server.kill();
}
console.log(`Screenshots in shots/, ${fehler} Fehler`);
process.exit(fehler ? 1 : 0);
