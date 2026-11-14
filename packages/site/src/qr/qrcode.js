// QR-Code-Erzeuger ohne Abhängigkeiten (ISO/IEC 18004): Byte-Modus (UTF-8), Fehlerkorrektur M, Versionen 1–10.
// Reicht für URLs bis 213 Bytes. Aufbau nach Nayukis Referenzimplementierung; geprüft gegen den Encoder
// von Kazuhiko Arase (scripts/qr-test.mjs).

const ECC = [0, 10, 16, 26, 18, 24, 16, 18, 22, 22, 26];   // Fehlerkorrektur-Codewörter je Block, Stufe M
const BLOECKE = [0, 1, 1, 1, 2, 2, 4, 4, 4, 5, 5];        // Anzahl Blöcke, Stufe M
const FORMAT_M = 0;                                       // Formatbits der Stufe M

const rohModule = (v) => {
  let r = (16 * v + 128) * v + 64;
  if (v >= 2) { const n = Math.floor(v / 7) + 2; r -= (25 * n - 10) * n - 55; if (v >= 7) r -= 36; }
  return r;
};
const datenCodewoerter = (v) => Math.floor(rohModule(v) / 8) - ECC[v] * BLOECKE[v];

// Reed-Solomon über GF(256), Polynom 0x11D
const mal = (x, y) => {
  let z = 0;
  for (let i = 7; i >= 0; i--) { z = (z << 1) ^ ((z >>> 7) * 0x11d); z ^= ((y >>> i) & 1) * x; }
  return z;
};
function divisor(grad) {
  const r = new Array(grad).fill(0);
  r[grad - 1] = 1;
  let wurzel = 1;
  for (let i = 0; i < grad; i++) {
    for (let j = 0; j < grad; j++) { r[j] = mal(r[j], wurzel); if (j + 1 < grad) r[j] ^= r[j + 1]; }
    wurzel = mal(wurzel, 2);
  }
  return r;
}
function rest(daten, div) {
  const r = new Array(div.length).fill(0);
  for (const b of daten) {
    const f = b ^ r.shift();
    r.push(0);
    div.forEach((d, i) => { r[i] ^= mal(d, f); });
  }
  return r;
}

// Bytes → Codewörter mit Fehlerkorrektur, verschränkt
function codewoerter(bytes, v) {
  const bits = [];
  const schreibe = (wert, n) => { for (let i = n - 1; i >= 0; i--) bits.push((wert >>> i) & 1); };
  schreibe(0b0100, 4);
  schreibe(bytes.length, v < 10 ? 8 : 16);
  bytes.forEach((b) => schreibe(b, 8));
  const kapazitaet = datenCodewoerter(v) * 8;
  schreibe(0, Math.min(4, kapazitaet - bits.length));
  schreibe(0, (8 - (bits.length % 8)) % 8);
  for (let pad = 0xec; bits.length < kapazitaet; pad ^= 0xec ^ 0x11) schreibe(pad, 8);
  const daten = [];
  for (let i = 0; i < bits.length; i += 8) daten.push(bits.slice(i, i + 8).reduce((a, b) => (a << 1) | b, 0));

  const n = BLOECKE[v], ecc = ECC[v], roh = Math.floor(rohModule(v) / 8);
  const kurz = n - (roh % n), kurzLaenge = Math.floor(roh / n);
  const div = divisor(ecc);
  const bloecke = [];
  for (let i = 0, k = 0; i < n; i++) {
    const d = daten.slice(k, k + kurzLaenge - ecc + (i < kurz ? 0 : 1));
    k += d.length;
    const e = rest(d, div);
    if (i < kurz) d.push(0);
    bloecke.push(d.concat(e));
  }
  const aus = [];
  for (let i = 0; i < bloecke[0].length; i++) {
    bloecke.forEach((b, j) => { if (i !== kurzLaenge - ecc || j >= kurz) aus.push(b[i]); });
  }
  return aus;
}

const MASKEN = [
  (x, y) => (x + y) % 2 === 0,
  (x, y) => y % 2 === 0,
  (x) => x % 3 === 0,
  (x, y) => (x + y) % 3 === 0,
  (x, y) => (Math.floor(x / 3) + Math.floor(y / 2)) % 2 === 0,
  (x, y) => ((x * y) % 2) + ((x * y) % 3) === 0,
  (x, y) => (((x * y) % 2) + ((x * y) % 3)) % 2 === 0,
  (x, y) => (((x + y) % 2) + ((x * y) % 3)) % 2 === 0,
];

function matrix(v, cw, maske) {
  const n = v * 4 + 17;
  const m = Array.from({ length: n }, () => new Array(n).fill(false));
  const fest = Array.from({ length: n }, () => new Array(n).fill(false));
  const setze = (x, y, dunkel) => { m[y][x] = dunkel; fest[y][x] = true; };

  for (let i = 0; i < n; i++) { setze(6, i, i % 2 === 0); setze(i, 6, i % 2 === 0); }
  for (const [cx, cy] of [[3, 3], [n - 4, 3], [3, n - 4]]) {
    for (let dy = -4; dy <= 4; dy++) for (let dx = -4; dx <= 4; dx++) {
      const x = cx + dx, y = cy + dy, d = Math.max(Math.abs(dx), Math.abs(dy));
      if (x >= 0 && x < n && y >= 0 && y < n) setze(x, y, d !== 2 && d !== 4);
    }
  }
  if (v > 1) {
    const anzahl = Math.floor(v / 7) + 2;
    const schritt = Math.ceil((v * 4 + 4) / (anzahl * 2 - 2)) * 2;
    const pos = [6];
    for (let p = n - 7; pos.length < anzahl; p -= schritt) pos.splice(1, 0, p);
    pos.forEach((a, i) => pos.forEach((b, j) => {
      if ((i === 0 && j === 0) || (i === 0 && j === anzahl - 1) || (i === anzahl - 1 && j === 0)) return;
      for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) setze(a + dx, b + dy, Math.max(Math.abs(dx), Math.abs(dy)) !== 1);
    }));
  }
  // Formatbits (erst reservieren, nach der Maske richtig setzen)
  const format = () => {
    const d = (FORMAT_M << 3) | maske;
    let r = d;
    for (let i = 0; i < 10; i++) r = (r << 1) ^ ((r >>> 9) * 0x537);
    const b = ((d << 10) | r) ^ 0x5412, bit = (i) => ((b >>> i) & 1) === 1;
    for (let i = 0; i <= 5; i++) setze(8, i, bit(i));
    setze(8, 7, bit(6)); setze(8, 8, bit(7)); setze(7, 8, bit(8));
    for (let i = 9; i < 15; i++) setze(14 - i, 8, bit(i));
    for (let i = 0; i < 8; i++) setze(n - 1 - i, 8, bit(i));
    for (let i = 8; i < 15; i++) setze(8, n - 15 + i, bit(i));
    setze(8, n - 8, true);
  };
  format();
  if (v >= 7) {
    let r = v;
    for (let i = 0; i < 12; i++) r = (r << 1) ^ ((r >>> 11) * 0x1f25);
    const b = (v << 12) | r;
    for (let i = 0; i < 18; i++) {
      const dunkel = ((b >>> i) & 1) === 1, a = n - 11 + (i % 3), c = Math.floor(i / 3);
      setze(a, c, dunkel); setze(c, a, dunkel);
    }
  }
  // Daten im Zickzack von unten rechts
  let i = 0;
  for (let rechts = n - 1; rechts >= 1; rechts -= 2) {
    if (rechts === 6) rechts = 5;
    for (let s = 0; s < n; s++) for (let j = 0; j < 2; j++) {
      const x = rechts - j, hoch = ((rechts + 1) & 2) === 0, y = hoch ? n - 1 - s : s;
      if (!fest[y][x] && i < cw.length * 8) { m[y][x] = ((cw[i >>> 3] >>> (7 - (i & 7))) & 1) === 1; i++; }
    }
  }
  const f = MASKEN[maske];
  for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) if (!fest[y][x] && f(x, y)) m[y][x] = !m[y][x];
  format();
  return m;
}

// Strafpunkte nach Norm (N1–N4), die Maske mit den wenigsten gewinnt
function strafe(m) {
  const n = m.length;
  let p = 0, dunkel = 0;
  const linie = (get) => {
    let lauf = 1;
    for (let i = 1; i <= n; i++) {
      if (i < n && get(i) === get(i - 1)) lauf++;
      else { if (lauf >= 5) p += lauf - 2; lauf = 1; }
    }
    const muster = [1, 0, 1, 1, 1, 0, 1];
    for (let i = 0; i + 7 <= n; i++) {
      if (!muster.every((b, k) => get(i + k) === !!b)) continue;
      const hell = (a, b) => { for (let k = a; k < b; k++) if (k >= 0 && k < n && get(k)) return false; return true; };
      if (hell(i - 4, i) || hell(i + 7, i + 11)) p += 40;
    }
  };
  for (let y = 0; y < n; y++) { linie((x) => m[y][x]); linie((x) => m[x][y]); }
  for (let y = 0; y < n - 1; y++) for (let x = 0; x < n - 1; x++) {
    const c = m[y][x];
    if (c === m[y][x + 1] && c === m[y + 1][x] && c === m[y + 1][x + 1]) p += 3;
  }
  m.forEach((z) => z.forEach((c) => { if (c) dunkel++; }));
  return p + 10 * Math.floor(Math.abs((dunkel * 100) / (n * n) - 50) / 5);
}

// text → boolesche Matrix (true = dunkel). maske nur für Tests erzwingen.
export function qrMatrix(text, { version, maske } = {}) {
  const bytes = [...new TextEncoder().encode(text)];
  const v = version ?? [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].find((x) => datenCodewoerter(x) * 8 >= 4 + (x < 10 ? 8 : 16) + bytes.length * 8);
  if (!v) throw new Error(`Text zu lang für QR-Code (${bytes.length} Bytes, höchstens 213)`);
  const cw = codewoerter(bytes, v);
  if (maske != null) return matrix(v, cw, maske);
  let beste = null, punkte = Infinity;
  for (let k = 0; k < 8; k++) {
    const m = matrix(v, cw, k), s = strafe(m);
    if (s < punkte) { beste = m; punkte = s; }
  }
  return beste;
}

// Als SVG mit 4 Modulen Ruhezone; crispEdges, damit es scharf druckt
export function qrSvg(text, { titel = text } = {}) {
  const m = qrMatrix(text), n = m.length, q = 4;
  let pfad = '';
  m.forEach((z, y) => z.forEach((c, x) => { if (c) pfad += `M${x + q} ${y + q}h1v1h-1z`; }));
  const t = String(titel).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  return `<svg class="qr" viewBox="0 0 ${n + 2 * q} ${n + 2 * q}" role="img" aria-label="QR-Code: ${t}" shape-rendering="crispEdges"><rect width="100%" height="100%" fill="#fff"/><path d="${pfad}" fill="#000"/></svg>`;
}
