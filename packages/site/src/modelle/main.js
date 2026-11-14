// 3D-Modelle prüfen: jedes Kategorie-Modell aus backend/seed/kategorien/ in echtem 3D (gemeinsame Ansicht viewer.js).
import { shell, esc, zahl, gramm, chip, schaetzung, repoUrl, ruhig } from '../shell.js';
import { CLASSES, MATERIALS } from '../../../../js/data/catalog.js';
import index from '../../../../backend/seed/kategorien/index.json';
import { erzeugeViewer, ladeModell, hatModell, materialVon } from '../viewer.js';
import './modelle.css';

const liste = index.filter((k) => hatModell(k.id));
const hand = liste.filter((k) => !k.platzhalter).length;
const app = shell('modelle', '../');
app.innerHTML = `
<section class="view sheet modelle">
  <div class="canvas">
    <div class="canvas-head">
      <div><p id="masse"></p></div>
      <div class="kopf-rechts">
        <div class="einstellungen">
          <button class="zahnrad" id="zahnrad" aria-label="Einstellungen" aria-expanded="false" aria-controls="menue" title="Einstellungen">
            <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M19.4 13a7.6 7.6 0 0 0 0-2l2.1-1.6-2-3.5-2.5 1a7.4 7.4 0 0 0-1.7-1L14.9 3h-4l-.4 2.9a7.4 7.4 0 0 0-1.7 1l-2.5-1-2 3.5L6.4 11a7.6 7.6 0 0 0 0 2l-2.1 1.6 2 3.5 2.5-1c.5.4 1.1.7 1.7 1l.4 2.9h4l.4-2.9c.6-.3 1.2-.6 1.7-1l2.5 1 2-3.5zM12.9 15.5a3.5 3.5 0 1 1 0-7 3.5 3.5 0 0 1 0 7z"/></svg>
          </button>
          <div class="menue" id="menue" role="menu" hidden>
            <button class="kipp" id="drehen" role="menuitemcheckbox" aria-checked="true"><span>Drehen</span><kbd>D</kbd><i></i></button>
            <button class="kipp" id="explodiert" role="menuitemcheckbox" aria-checked="true"><span>Explodiert</span><kbd>E</kbd><i></i></button>
            <button class="kipp" id="nummern" role="menuitemcheckbox" aria-checked="true"><span>Nummern</span><kbd>N</kbd><i></i></button>
          </div>
        </div>
      </div>
    </div>
    <div class="drawing" id="szene" aria-label="3D-Modell, mit der Maus drehbar"></div>
    <div class="legend" id="legende"></div>
  </div>
  <aside class="panel" id="panel"></aside>
  <div class="actionbar">
    <button class="btn ghost" id="zurueck">←</button>
    <div class="q" id="position"></div>
    <button class="btn" id="weiter">→</button>
  </div>
</section>`;

let aktuell = null;
const viewer = erzeugeViewer(document.getElementById('szene'), {
  tip: document.getElementById('tip'),
  onHover: (i) => document.querySelectorAll('#panel .prow').forEach((r) => r.classList.toggle('hot', +r.dataset.i === i)),
  onSelect: (i) => (i == null ? zeigeModell() : zeigeTeil(i)),
});

// Langsames Kreisen um das Objekt, Wahl bleibt gespeichert
const drehSchalter = document.getElementById('drehen');
function setzeDrehen(an) {
  drehSchalter.setAttribute('aria-checked', String(an));
  viewer.drehen(an); localStorage.setItem('modelle-drehen', an ? 'an' : 'aus');
}
drehSchalter.addEventListener('click', () => setzeDrehen(drehSchalter.getAttribute('aria-checked') !== 'true'));
setzeDrehen(localStorage.getItem('modelle-drehen') ? localStorage.getItem('modelle-drehen') === 'an' : !ruhig);

// Zusammengebaut oder explodiert, als Schalter im Zahnrad-Menü
const exSchalter = document.getElementById('explodiert');
exSchalter.addEventListener('click', () => {
  const an = exSchalter.getAttribute('aria-checked') !== 'true';
  exSchalter.setAttribute('aria-checked', String(an));
  viewer.explosion(an ? 1 : 0);
});
const schalter = document.getElementById('nummern');
function setzeNummern(an) {
  schalter.setAttribute('aria-checked', String(an));
  viewer.nummern(an); localStorage.setItem('modelle-nummern', an ? 'an' : 'aus');
}
schalter.addEventListener('click', () => setzeNummern(schalter.getAttribute('aria-checked') !== 'true'));
setzeNummern(localStorage.getItem('modelle-nummern') !== 'aus');
viewer.foto(true);   // immer Foto-Ansicht mit Schatten

// ---------- Prüfung wie tools/kategorien/pruefe.py ----------
const zahlAus = (s) => parseFloat(String(s).replace(/[^\d,.]/g, '').replace(',', '.'));
function pruefe(obj) {
  const h = [], summe = obj.parts.reduce((s, p) => s + p.mass, 0);
  const soll = zahlAus(obj.gewicht) * (/kg/.test(obj.gewicht) ? 1000 : 1), abw = soll ? (summe - soll) / soll : 0;
  if (obj.platzhalter) h.push({ warn: false, text: 'Automatischer Platzhalter.' });
  if (Math.abs(abw) > 0.15) h.push({ warn: true, text: `Gewicht weicht ${zahl(abw * 100, 0)} % ab.` });
  const [W, D, H] = String(obj.masse).split('×').map(zahlAus);
  const box = (p, ex) => { const e = ex ? p.explode ?? [0, 0, 0] : [0, 0, 0]; const d = p.d ?? p.w;
    return [p.x + e[0], p.y + e[1], p.z + e[2], p.x + e[0] + p.w, p.y + e[1] + d, p.z + e[2] + p.h]; };
  const b = obj.parts.map((p) => box(p, false));
  const ist = [0, 1, 2].map((i) => Math.max(...b.map((x) => x[i + 3])) - Math.min(...b.map((x) => x[i])));
  ['Breite', 'Tiefe', 'Höhe'].forEach((n, i) => { const s = [W, D, H][i]; if (s && (ist[i] > s * 1.1 + 3 || ist[i] < s * 0.85 - 3)) h.push({ warn: false, text: `${n}: ${zahl(ist[i], 0)} statt ${zahl(s, 0)} mm.` }); });
  const ex = obj.parts.map((p) => box(p, true));
  let ueber = 0;
  for (let i = 0; i < ex.length; i++) for (let j = i + 1; j < ex.length; j++) if ([0, 1, 2].every((k) => Math.min(ex[i][k + 3], ex[j][k + 3]) - Math.max(ex[i][k], ex[j][k]) > 0.05)) ueber++;
  if (ueber) h.push({ warn: true, text: `${ueber} Teilpaare überlappen explodiert.` });
  return { h, summe, soll, abw };
}

// ---------- Datenblatt ----------
const panel = document.getElementById('panel');
function setzePanel(html, crumbs) {
  panel.innerHTML = `<div class="panel-inner">${crumbs ? `<nav class="crumbs">${crumbs.map((c, i) => (i < crumbs.length - 1
    ? `<button data-c="${i}">${esc(c.label)}</button><span></span>` : `<b style="font-weight:500;color:var(--ink)">${esc(c.label)}</b>`)).join('')}</nav>` : ''}${html}</div>`;
  panel.querySelectorAll('.crumbs button').forEach((b) => b.addEventListener('click', () => crumbs[+b.dataset.c].go()));
  panel.scrollTop = 0;
}

let filter = 'alle';
function zeigeListe() {
  const q = document.getElementById('suche')?.value ?? '';
  const gruppen = new Map();
  for (const k of liste) {
    if ((filter === 'hand' && k.platzhalter) || (filter === 'platz' && !k.platzhalter)) continue;
    if (q && !`${k.name} ${k.name_en} ${k.id}`.toLowerCase().includes(q.toLowerCase())) continue;
    (gruppen.get(k.klasse) ?? gruppen.set(k.klasse, []).get(k.klasse)).push(k);
  }
  setzePanel(`
    <div class="liste-kopf">
      <input id="suche" class="suche-feld" type="search" placeholder="Modell suchen" value="${esc(q)}" autocomplete="off">
      ${hand < liste.length ? `<div class="seg" id="filter">${[['alle', 'Alle'], ['hand', 'Handgebaut'], ['platz', 'Platzhalter']].map(([f, t]) => `<button data-f="${f}" class="${filter === f ? 'on' : ''}">${t}</button>`).join('')}</div>` : ''}
    </div>
    <div class="katalog">${[...gruppen].map(([g, ks]) => `<div><h4 class="eyebrow">${esc(g)} · ${ks.length}</h4>
      <div class="kat-list">${ks.map((k) => `<a href="#kat=${k.id}" class="tag ${aktuell?.id === k.id ? 'aktiv' : ''}">${esc(k.name)}</a>`).join('')}</div></div>`).join('')
      || '<p class="leer">Nichts gefunden.</p>'}</div>`, [{ label: 'Alle Modelle', go: zeigeListe }]);
  const s = document.getElementById('suche');
  s.addEventListener('input', () => { zeigeListe(); const n = document.getElementById('suche'); n.focus(); n.setSelectionRange(n.value.length, n.value.length); });
  panel.querySelectorAll('#filter button').forEach((b) => b.addEventListener('click', () => { filter = b.dataset.f; zeigeListe(); }));
}

function zeigeModell() {
  const obj = aktuell, { h, summe, soll, abw } = pruefe(obj);
  setzePanel(`
    <div><div class="eyebrow">${esc(obj.klasse)}</div><h1 style="margin-top:8px">${esc(obj.name)}</h1></div>
    <div class="stats">
      <div><b>${obj.parts.length}</b><span>Teile</span></div>
      <div><b>${gramm(summe)}</b><span>Modell</span></div>
      <div><b>${gramm(soll)}</b><span>Typisch${schaetzung('', 'Typisches Gewicht, eigene Schätzung')}</span></div>
    </div>
    ${h.length ? `<div class="pruef">${h.map((x) => `<p class="note ${x.warn ? 'warn' : ''}">${esc(x.text)}</p>`).join('')}</div>` : ''}
    <div><h3>Teile</h3><div class="plist">${viewer.teile.map((t) => `
      <button class="prow" data-i="${t.i}"><span class="n">${t.nr ?? '–'}</span>
        <span>${esc(t.p.name)}<small>${esc(materialVon(t.p)?.name ?? '')}</small></span><span class="m">${gramm(t.p.mass)}</span></button>`).join('')}</div></div>
    <a class="btn ghost lw-link" href="../atlas/#kat=${obj.id}">Lebensweg ansehen →</a>`,
  [{ label: 'Alle Modelle', go: zeigeListe }, { label: obj.name, go: zeigeModell }]);
  panel.querySelectorAll('.prow').forEach((r) => {
    r.addEventListener('pointerenter', () => viewer.markiere(+r.dataset.i));
    r.addEventListener('pointerleave', () => viewer.markiere(null));
    r.addEventListener('click', () => { viewer.waehle(+r.dataset.i); zeigeTeil(+r.dataset.i); });
  });
}

function zeigeTeil(i) {
  const t = viewer.teile[i], p = t.p;
  setzePanel(`
    <div><div class="eyebrow">Teil ${t.nr ?? ''}</div><h1 style="margin-top:8px">${esc(p.name)}</h1>
      <div class="sub">${gramm(p.mass)} · ${zahl(p.w)} × ${zahl(p.d ?? p.w)} × ${zahl(p.h)} mm</div></div>
    <div><h3>Material</h3>${(p.materials ?? []).map(([m, a]) => `
      <div class="mrow"><i style="background:${CLASSES[MATERIALS[m]?.cls]?.color ?? '#ccc'}"></i><span>${esc(MATERIALS[m]?.name ?? m)}</span>
        <span class="pct">${a} %</span><span></span><div class="mbar"><b style="width:${a}%"></b></div></div>`).join('')}</div>
    <dl class="facts">
      <div><dt>Bauteil</dt><dd>${esc(p.component_id ?? '–')}</dd></div>
      <div><dt>Material-ID</dt><dd>${esc(p.material_id ?? '–')}</dd></div>
      <div><dt>Explosion</dt><dd>${(p.explode ?? []).map((v) => zahl(v)).join(' / ')} mm</dd></div>
    </dl>`, [{ label: 'Alle Modelle', go: zeigeListe }, { label: aktuell.name, go: () => { viewer.waehle(null); zeigeModell(); } }, { label: p.short ?? p.name }]);
}

// ---------- Laden, Blättern, Direktlink #kat=<id> ----------
async function oeffne(id) {
  if (!hatModell(id)) return;
  aktuell = await ladeModell(id);
  const i = liste.findIndex((k) => k.id === id);
  document.getElementById('masse').textContent = `${aktuell.masse}`;
  document.getElementById('position').innerHTML = `<b>${esc(aktuell.name)}</b> <span>· ${i + 1} / ${liste.length}</span>`;
  const vor = liste[(i - 1 + liste.length) % liste.length], nach = liste[(i + 1) % liste.length];
  document.getElementById('zurueck').innerHTML = `<span class="pfeil">←</span>${esc(vor.name)}`;
  document.getElementById('weiter').innerHTML = `${esc(nach.name)}<span class="pfeil">→</span>`;
  const klassen = [...new Set(aktuell.parts.map((p) => materialVon(p)?.cls).filter(Boolean))];
  document.getElementById('legende').innerHTML = klassen.map((c) => `<span><i style="background:${CLASSES[c].color}"></i>${CLASSES[c].label}</span>`).join('');
  viewer.lade(aktuell);
  zeigeModell();
}
const blaettere = (d) => {
  const i = liste.findIndex((k) => k.id === aktuell?.id);
  location.hash = `kat=${liste[(i + d + liste.length) % liste.length].id}`;
};
document.getElementById('zurueck').addEventListener('click', () => blaettere(-1));
document.getElementById('weiter').addEventListener('click', () => blaettere(1));
addEventListener('keydown', (e) => {
  if (e.target.closest('input')) return;
  if (e.key === 'ArrowRight') blaettere(1);
  if (e.key === 'ArrowLeft') blaettere(-1);
  if (e.key === 'Escape') { if (!menue.hidden) { menueAuf(false); return; } viewer.waehle(null); zeigeModell(); }
  if (e.key === 'n' || e.key === 'N') schalter.click();
  if (e.key === 'e' || e.key === 'E') exSchalter.click();
  if (e.key === 'd' || e.key === 'D') drehSchalter.click();
});
const ausHash = () => oeffne(location.hash.match(/kat=([\w-]+)/)?.[1] ?? 'smartphone');
addEventListener('hashchange', ausHash);
ausHash();
