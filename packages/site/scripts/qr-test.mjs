// Prüft src/qr/qrcode.js gegen den QR-Encoder von Kazuhiko Arase (liegt npm bei: qrcode-terminal/vendor/QRCode).
// Gleiche Version, gleiche Maske → die Matrix muss Modul für Modul übereinstimmen.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { qrMatrix } from '../src/qr/qrcode.js';

const npm = execSync('npm root -g').toString().trim();
const require = createRequire(import.meta.url);
const QRCode = require(`${npm}/npm/node_modules/qrcode-terminal/vendor/QRCode`);
const M = require(`${npm}/npm/node_modules/qrcode-terminal/vendor/QRCode/QRErrorCorrectLevel`).M;

let fehler = 0, faelle = 0;
const basis = 'https://kontor2026.github.io/web-app/modelle/#kat=';
for (let v = 1; v <= 10; v++) for (const laenge of [1, 7, 20, 40, 80, 120, 180, 213]) for (let maske = 0; maske < 8; maske++) {
  const text = (basis + 'x'.repeat(300)).slice(0, laenge);
  const ref = new QRCode(v, M);
  ref.addData(text);
  try { ref.makeImpl(false, maske); } catch { continue; }   // passt nicht in diese Version
  let mein;
  try { mein = qrMatrix(text, { version: v, maske }); } catch { continue; }
  if (mein.length !== ref.getModuleCount()) { fehler++; console.log('Größe', v, laenge); continue; }
  faelle++;
  const n = mein.length;
  let diff = 0;
  for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) if (mein[y][x] !== ref.isDark(y, x)) diff++;
  if (diff) { fehler++; console.log(`v${v} Länge ${laenge} Maske ${maske}: ${diff} Module weichen ab`); }
}
// Automatische Wahl von Version und Maske muss für alle Kategorie-Links klappen
const index = JSON.parse((await import('node:fs')).readFileSync(new URL('../../../backend/seed/kategorien/index.json', import.meta.url)));
for (const k of index) qrMatrix(basis + k.id);
console.log(`${faelle} Vergleiche, ${fehler} Fehler, ${index.length} Kategorie-Links erzeugt`);
process.exit(fehler ? 1 : 0);
