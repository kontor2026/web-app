#!/usr/bin/env node
'use strict';

// Screenshots of every camera station of the presentation, for checking (Playwright).
// Usage: node tools/shots.cjs [url] [outDir]
//   url     default http://localhost:5181/praesentation/ (start tools/serve.cjs first)
//   outDir  default <tmp>/praesentation-shots
// Needs Playwright: `npm i -D playwright && npx playwright install chromium`,
// or `playwright-core` plus an installed Chrome (set PW_CHANNEL=chrome).
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

let playwright;
try { playwright = require('playwright'); } catch { playwright = require('playwright-core'); }

const url = process.argv[2] || 'http://localhost:5181/praesentation/';
const outDir = process.argv[3] || path.join(os.tmpdir(), 'praesentation-shots');

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await playwright.chromium.launch({ channel: process.env.PW_CHANNEL || undefined, args: ['--ignore-gpu-blocklist', '--enable-gpu-rasterization', '--use-angle=d3d11'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  await page.goto(url, { waitUntil: 'load' });
  await page.waitForFunction(() => window.__praesi?.state.ready, null, { timeout: 60000 });
  const steps = await page.evaluate(() => window.__praesi.steps);

  // Jeden Schritt im Endzustand: hinspringen, einige Bilder rechnen lassen, fotografieren
  for (const [k, id] of steps.entries()) {
    if (id === 'live') continue;
    await page.evaluate((x) => { window.__praesi.go(x); window.__praesi.tick(90); }, k);
    await page.waitForTimeout(id === 'haube' || id === 'energie' ? 3000 : 900);
    const file = path.join(outDir, `${String(k + 1).padStart(2, '0')}-${id}.png`);
    await page.screenshot({ path: file });
    console.log(file);
    if (id === 'ende') {                                     // Finale: Text dreht durch, dann Name und QR-Code
      await page.waitForTimeout(10000);
      const f2 = file.replace('.png', '-schluss.png');
      await page.screenshot({ path: f2 });
      console.log(f2);
    }
  }
  await browser.close();
  if (errors.length) {
    console.error('Fehler auf der Seite:\n' + errors.join('\n'));
    process.exit(1);
  }
})();
