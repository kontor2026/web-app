#!/usr/bin/env node
'use strict';

// Screenshots of every camera station of the presentation, for checking (Playwright).
// Usage: node tools/shots.cjs [url] [outDir]
//   url     default http://localhost:5181/ (start tools/serve.cjs first)
//   outDir  default <tmp>/praesentation-shots
// Needs Playwright: `npm i -D playwright && npx playwright install chromium`,
// or `playwright-core` plus an installed Chrome (set PW_CHANNEL=chrome).
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

let playwright;
try { playwright = require('playwright'); } catch { playwright = require('playwright-core'); }

const url = process.argv[2] || 'http://localhost:5181/';
const outDir = process.argv[3] || path.join(os.tmpdir(), 'praesentation-shots');

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await playwright.chromium.launch({ channel: process.env.PW_CHANNEL || undefined });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  await page.goto(url, { waitUntil: 'load' });
  await page.waitForFunction(() => window.__praesi);
  const slides = await page.evaluate(() => window.__praesi.slides);

  let n = 0;
  for (const [s, slide] of slides.entries()) {
    for (const [st, shot] of slide.steps.entries()) {
      await page.evaluate(([a, b]) => window.__praesi.go(a, b), [s, st]);
      await page.waitForFunction(() => !window.__praesi.busy());
      await page.waitForTimeout(900); // fades and the app on the monitor
      const file = path.join(outDir, `${String(++n).padStart(2, '0')}-${slide.id}-${shot}.png`);
      await page.screenshot({ path: file });
      console.log(file);
    }
  }
  await browser.close();
  if (errors.length) {
    console.error('Fehler auf der Seite:\n' + errors.join('\n'));
    process.exit(1);
  }
})();
