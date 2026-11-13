// 3D-Modelle prüfen: jedes Kategorie-Modell aus backend/seed/kategorien/ in echtem 3D (three.js).
// Gleiche Teile, Farben und Explosion wie die Zeichnung der Station (js/iso.js), nur frei drehbar.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';
import { shell, esc, zahl, gramm, ruhig } from '../shell.js';
import { CLASSES, MATERIALS } from '../../../../js/data/catalog.js';
import index from '../../../../backend/seed/kategorien/index.json';
import './modelle.css';

const LADE = import.meta.glob('../../../../backend/seed/kategorien/*.json', { import: 'default' });
const datei = (id) => LADE[`../../../../backend/seed/kategorien/${id}.json`];
const liste = index.filter((k) => datei(k.id));
const hand = liste.filter((k) => !k.platzhalter).length;

const app = shell('modelle', '../', `<span class="stock">Handgebaut <b>${hand}</b> / ${liste.length}</span>`);
app.innerHTML = `
<section class="view sheet modelle">
  <div class="canvas">
    <div class="canvas-head">
      <div><h2 id="titel">…</h2><p id="masse"></p></div>
      <div class="seg" role="group" aria-label="Ansicht">
        <button data-x="0">Zusammengebaut</button><button data-x="1" class="on">Explodiert</button>
      </div>
    </div>
    <div class="drawing" id="szene" aria-label="3D-Modell, mit der Maus drehbar"></div>
    <div class="legend" id="legende"></div>
    <div class="titleblock" id="titelblock"></div>
    <div class="hint-hover" id="hinweis">Ziehen dreht · Scrollen zoomt · Teil antippen zeigt Details</div>
  </div>
  <aside class="panel" id="panel"></aside>
  <div class="actionbar">
    <div class="q" id="position"></div>
    <button class="btn ghost" id="zurueck">← Vorheriges</button>
    <button class="btn" id="weiter">Nächstes →</button>
  </div>
</section>`;

// ---------- Szene ----------
const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const INK = new THREE.Color(css('--ink')), AKZENT = new THREE.Color(css('--accent'));
const szeneEl = document.getElementById('szene');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
szeneEl.append(renderer.domElement);
const labels = new CSS2DRenderer();
labels.domElement.className = 'labels';
szeneEl.append(labels.domElement);

const scene = new THREE.Scene();
scene.add(new THREE.AmbientLight(0xffffff, 1.9));
const sonne = new THREE.DirectionalLight(0xffffff, 1.5);
sonne.position.set(0.4, 1, 0.25);
scene.add(sonne);
const kamera = new THREE.OrthographicCamera(-1, 1, 1, -1, -10000, 10000);
const steuerung = new OrbitControls(kamera, labels.domElement);
steuerung.enableDamping = true;
const modell = new THREE.Group();
scene.add(modell);

function groesse() {
  const { width: w, height: h } = szeneEl.getBoundingClientRect();
  renderer.setSize(w, h);
  labels.setSize(w, h);
  const a = w / Math.max(h, 1);
  kamera.left = -a; kamera.right = a; kamera.top = 1; kamera.bottom = -1;
  kamera.updateProjectionMatrix();
}
new ResizeObserver(groesse).observe(szeneEl);

// Grundriss eines Teils: abgerundetes Rechteck oder Ellipse, Ursprung linke hintere Ecke
function grundriss(t) {
  const s = new THREE.Shape(), w = t.w, d = t.d ?? t.w;
  if (t.shape === 'cyl') { s.absellipse(w / 2, d / 2, w / 2, d / 2, 0, Math.PI * 2, false, 0); return s; }
  const r = Math.max(0, Math.min(t.r ?? 0, w / 2, d / 2));
  s.moveTo(r, 0); s.lineTo(w - r, 0); s.quadraticCurveTo(w, 0, w, r); s.lineTo(w, d - r); s.quadraticCurveTo(w, d, w - r, d);
  s.lineTo(r, d); s.quadraticCurveTo(0, d, 0, d - r); s.lineTo(0, r); s.quadraticCurveTo(0, 0, r, 0);
  return s;
}
// Station: x = Breite, y = Tiefe (vorne groß), z = Höhe → three: X, Z, Y
function koerper(t, farbe, opacity) {
  const geo = new THREE.ExtrudeGeometry(grundriss(t), { depth: t.h, bevelEnabled: false, curveSegments: 24 });
  geo.rotateX(Math.PI / 2);
  geo.translate(0, t.h, 0);
  const mat = new THREE.MeshLambertMaterial({ color: farbe, transparent: true, opacity, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const mesh = new THREE.Mesh(geo, mat);
  const kanten = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 30), new THREE.LineBasicMaterial({ color: INK, transparent: true }));
  return { mesh, kanten };
}
const farbeVon = (p) => p.color ?? CLASSES[MATERIALS[p.materials?.[0]?.[0]]?.cls]?.color ?? '#cccccc';

let teile = [], aktuell = null, explodiert = 1, hot = null, gewaehlt = null, animationNr = 0;

function baue(obj) {
  // Alte Nummern-Ballons selbst entfernen: CSS2DRenderer räumt nur direkte Kinder auf, unsere hängen in Gruppen
  modell.traverse((o) => { if (o.isCSS2DObject) o.element.remove(); });
  modell.traverse((o) => { o.geometry?.dispose(); o.material?.dispose?.(); });
  modell.clear();
  teile = [];
  let nr = 0;
  for (const p of obj.parts) {
    const farbe = new THREE.Color(farbeVon(p));
    const g = new THREE.Group();
    const { mesh, kanten } = koerper(p, farbe, p.opacity ?? 1);
    g.add(mesh, kanten);
    for (const m of p.marks ?? []) {             // Details auf der Oberseite, relativ zum Teil
      const mg = new THREE.ShapeGeometry(grundriss(m), 24);
      mg.rotateX(Math.PI / 2);
      mg.translate(m.x, p.h + 0.04, m.y);
      const mf = new THREE.Color(m.fill ?? farbe.clone().multiplyScalar(0.78));
      g.add(new THREE.Mesh(mg, new THREE.MeshBasicMaterial({ color: mf, side: THREE.DoubleSide, transparent: true, opacity: p.opacity ?? 1 })));
      g.add(new THREE.LineSegments(new THREE.EdgesGeometry(mg), new THREE.LineBasicMaterial({ color: INK, transparent: true, opacity: 0.6 })));
    }
    g.position.set(p.x, p.z, p.y);
    const ex = new THREE.Vector3(p.explode?.[0] ?? 0, p.explode?.[2] ?? 0, p.explode?.[1] ?? 0);
    const t = { p, g, mesh, ex, basis: new THREE.Vector3(p.x, p.z, p.y), opacity: p.opacity ?? 1, nr: p.label === false ? null : String(++nr).padStart(2, '0') };
    mesh.userData.teil = t;
    if (t.nr) {
      const el = document.createElement('button');
      el.className = 'ballon';
      el.innerHTML = `<b>${t.nr}</b>`;
      el.title = p.name;
      el.addEventListener('click', () => waehleTeil(t));
      el.addEventListener('pointerenter', () => markiere(t));
      el.addEventListener('pointerleave', () => markiere(null));
      const l = new CSS2DObject(el);
      l.position.set(p.w / 2, p.h, (p.d ?? p.w) / 2);
      g.add(l);
    }
    modell.add(g);
    teile.push(t);
  }
  // Modell mittig auf den Ursprung, Kamera passend zum explodierten Zustand
  setzeExplosion(1, false);
  modell.position.set(0, 0, 0);
  modell.updateMatrixWorld(true);
  const box = new THREE.Box3().setFromObject(modell);
  modell.position.copy(box.getCenter(new THREE.Vector3()).negate());
  const r = box.getBoundingSphere(new THREE.Sphere()).radius;
  kamera.position.set(1, 0.95, 1.25).normalize().multiplyScalar(r * 4);
  kamera.zoom = 1 / (r * 1.08);
  kamera.updateProjectionMatrix();
  steuerung.target.set(0, 0, 0);
  steuerung.update();
  setzeExplosion(explodiert, !ruhig);
}

function setzeExplosion(ziel, animiert = true) {
  explodiert = ziel;
  document.querySelectorAll('.modelle .seg button').forEach((b) => b.classList.toggle('on', +b.dataset.x === ziel));
  // Eigene Teileliste festhalten und laufende Animation ablösen: beim Blättern kommt sonst
  // die Animation des alten Modells mit den Teilen des neuen durcheinander.
  const eigene = teile, lauf = ++animationNr;
  const start = eigene.map((t) => t.g.position.clone()), t0 = performance.now(), dauer = animiert ? 900 : 0;
  const schritt = (jetzt) => {
    if (lauf !== animationNr) return;
    const k = dauer ? Math.min(1, (jetzt - t0) / dauer) : 1;
    const e = k < 0.5 ? 4 * k ** 3 : 1 - (-2 * k + 2) ** 3 / 2;       // inOutCubic wie in der Station
    eigene.forEach((t, i) => t.g.position.lerpVectors(start[i], t.basis.clone().addScaledVector(t.ex, ziel), e));
    if (k < 1) requestAnimationFrame(schritt);
  };
  schritt(performance.now());
}
document.querySelectorAll('.modelle .seg button').forEach((b) => b.addEventListener('click', () => setzeExplosion(+b.dataset.x)));

// ---------- Hervorheben wie .has-hot in der Station ----------
function markiere(t) {
  hot = t;
  const aktiv = t ?? gewaehlt;
  for (const x of teile) {
    const an = !aktiv || x === aktiv;
    x.mesh.material.opacity = x.opacity * (an ? 1 : 0.22);
    x.g.children.forEach((c) => {
      if (c.isLineSegments) { c.material.color.copy(x === aktiv ? AKZENT : INK); c.material.opacity = an ? 1 : 0.2; }
      else if (c !== x.mesh && c.material) c.material.opacity = x.opacity * (an ? 1 : 0.22);
      if (c.isCSS2DObject) c.element.classList.toggle('aus', !an);
      if (c.isCSS2DObject) c.element.classList.toggle('hot', x === aktiv);
    });
  }
  document.querySelectorAll('#panel .prow').forEach((r) => r.classList.toggle('hot', aktiv && +r.dataset.i === teile.indexOf(aktiv)));
}

const ray = new THREE.Raycaster(), maus = new THREE.Vector2();
let gezogen = false;
labels.domElement.addEventListener('pointerdown', () => { gezogen = false; document.getElementById('hinweis').hidden = true; });
labels.domElement.addEventListener('pointermove', (e) => {
  gezogen = gezogen || e.buttons > 0;
  if (e.buttons) return;
  const r = labels.domElement.getBoundingClientRect();
  maus.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
  ray.setFromCamera(maus, kamera);
  const treffer = ray.intersectObjects(teile.map((t) => t.mesh))[0]?.object.userData.teil ?? null;
  if (treffer !== hot) markiere(treffer);
  labels.domElement.style.cursor = treffer ? 'pointer' : '';
  const tip = document.getElementById('tip');
  if (treffer) {
    tip.hidden = false;
    tip.innerHTML = `${treffer.nr ? `<span class="n">${treffer.nr}</span>` : ''}<b>${esc(treffer.p.name)}</b><small>${esc(MATERIALS[treffer.p.materials?.[0]?.[0]]?.name ?? '')} · ${gramm(treffer.p.mass)}</small>`;
    tip.style.left = `${e.clientX + 14}px`; tip.style.top = `${e.clientY + 14}px`;
  } else tip.hidden = true;
});
labels.domElement.addEventListener('pointerleave', () => { markiere(null); document.getElementById('tip').hidden = true; });
labels.domElement.addEventListener('click', () => { if (!gezogen) waehleTeil(hot); });

renderer.setAnimationLoop(() => { steuerung.update(); renderer.render(scene, kamera); labels.render(scene, kamera); });

// ---------- Prüfhinweise (wie tools/kategorien/pruefe.py) ----------
const zahlAus = (s) => parseFloat(String(s).replace(/[^\d,.]/g, '').replace(',', '.'));
function pruefe(obj) {
  const h = [];
  const summe = obj.parts.reduce((s, p) => s + p.mass, 0);
  const soll = zahlAus(obj.gewicht) * (/kg/.test(obj.gewicht) ? 1000 : 1);
  const abw = soll ? (summe - soll) / soll : 0;
  if (obj.platzhalter) h.push({ warn: false, text: 'Automatischer Platzhalter. Ein handgebautes Modell fehlt noch.' });
  if (Math.abs(abw) > 0.15) h.push({ warn: true, text: `Teile wiegen zusammen ${gramm(summe)}, laut Tabelle ${gramm(soll)} (${abw > 0 ? '+' : ''}${zahl(abw * 100, 0)} %).` });
  const [W, D, H] = String(obj.masse).split('×').map(zahlAus);
  const box = (p, ex) => { const e = ex ? p.explode ?? [0, 0, 0] : [0, 0, 0]; const d = p.d ?? p.w;
    return [p.x + e[0], p.y + e[1], p.z + e[2], p.x + e[0] + p.w, p.y + e[1] + d, p.z + e[2] + p.h]; };
  const b = obj.parts.map((p) => box(p, false));
  const ist = [0, 1, 2].map((i) => Math.max(...b.map((x) => x[i + 3])) - Math.min(...b.map((x) => x[i])));
  ['Breite', 'Tiefe', 'Höhe'].forEach((n, i) => {
    const s = [W, D, H][i];
    if (s && (ist[i] > s * 1.1 + 3 || ist[i] < s * 0.85 - 3)) h.push({ warn: false, text: `${n} zusammengebaut ${zahl(ist[i], 0)} mm, laut Tabelle ${zahl(s, 0)} mm.` });
  });
  const ex = obj.parts.map((p) => box(p, true)), ueber = [];
  for (let i = 0; i < ex.length; i++) for (let j = i + 1; j < ex.length; j++)
    if ([0, 1, 2].every((k) => Math.min(ex[i][k + 3], ex[j][k + 3]) - Math.max(ex[i][k], ex[j][k]) > 0.05)) ueber.push(`${obj.parts[i].name} / ${obj.parts[j].name}`);
  if (ueber.length) h.push({ warn: true, text: `Explodiert überlappen sich ${ueber.length} Teilpaare, z. B. ${ueber.slice(0, 2).join(', ')}.` });
  if (!h.length) h.push({ warn: false, ok: true, text: 'Keine Auffälligkeiten: Gewicht, Maße und Explosion passen.' });
  return { h, summe, soll, abw };
}

// ---------- Panel ----------
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
    if (filter === 'hand' && k.platzhalter) continue;
    if (filter === 'platz' && !k.platzhalter) continue;
    if (q && !`${k.name} ${k.name_en} ${k.id}`.toLowerCase().includes(q.toLowerCase())) continue;
    (gruppen.get(k.klasse) ?? gruppen.set(k.klasse, []).get(k.klasse)).push(k);
  }
  setzePanel(`
    <div><div class="eyebrow">3D-Modelle</div><h1 style="margin-top:8px">Welches Modell willst du prüfen?</h1>
      <p class="sub">Grün umrandet: handgebaut. Grau: automatischer Platzhalter.</p></div>
    <div class="liste-kopf">
      <input id="suche" class="suche-feld" type="search" placeholder="Suchen, z. B. Föhn" value="${esc(q)}" autocomplete="off">
      <div class="seg" id="filter">
        <button data-f="alle" class="${filter === 'alle' ? 'on' : ''}">Alle</button>
        <button data-f="hand" class="${filter === 'hand' ? 'on' : ''}">Handgebaut</button>
        <button data-f="platz" class="${filter === 'platz' ? 'on' : ''}">Platzhalter</button>
      </div>
    </div>
    <div class="katalog">${[...gruppen].map(([g, ks]) => `<div><h4 class="eyebrow">${esc(g)} · ${ks.length}</h4>
      <div class="kat-list">${ks.map((k) => `<a href="#kat=${k.id}" class="tag ${k.platzhalter ? '' : 'hoch'} ${aktuell?.id === k.id ? 'aktiv' : ''}">${esc(k.name)}</a>`).join('')}</div></div>`).join('')
      || '<p class="leer">Nichts gefunden.</p>'}</div>`, null);
  const s = document.getElementById('suche');
  s.addEventListener('input', () => { zeigeListe(); const n = document.getElementById('suche'); n.focus(); n.setSelectionRange(n.value.length, n.value.length); });
  panel.querySelectorAll('#filter button').forEach((b) => b.addEventListener('click', () => { filter = b.dataset.f; zeigeListe(); }));
}

function zeigeModell() {
  const obj = aktuell, { h, summe, soll, abw } = pruefe(obj);
  gewaehlt = null; markiere(null);
  setzePanel(`
    <div><div class="eyebrow">${esc(obj.klasse)}</div><h1 style="margin-top:8px">${esc(obj.name)}</h1>
      <div class="sub">${esc(obj.name_en)} · <span class="tag ${obj.platzhalter ? '' : 'hoch'}">${obj.platzhalter ? 'Platzhalter' : 'handgebaut'}</span></div></div>
    <div class="stats">
      <div><b>${obj.parts.length}</b><span>Teile</span><small>so viele Teile hat die Zeichnung</small></div>
      <div><b>${gramm(summe)}</b><span>Masse der Teile</span><small>laut Tabelle ${gramm(soll)}</small></div>
      <div><b>${Math.round(abw * 100) > 0 ? '+' : ''}${Math.round(abw * 100) || 0} %</b><span>Abweichung</span><small>bis ±15 % ist in Ordnung</small></div>
    </div>
    <div><h3>Prüfhinweise</h3><div class="pruef">${h.map((x) => `<p class="note ${x.warn ? 'warn' : ''} ${x.ok ? 'ok' : ''}">${esc(x.text)}</p>`).join('')}</div></div>
    <div><h3>Teile · antippen für Details</h3><div class="plist">${teile.map((t, i) => `
      <button class="prow" data-i="${i}"><span class="n">${t.nr ?? '–'}</span>
        <span>${esc(t.p.name)}<small>${esc(MATERIALS[t.p.materials?.[0]?.[0]]?.name ?? '')}</small></span>
        <span class="m">${gramm(t.p.mass)}</span></button>`).join('')}</div></div>
    <p class="source">${esc(obj.quelle)}</p>`, [{ label: 'Alle Modelle', go: zeigeListe }, { label: obj.name, go: zeigeModell }]);
  panel.querySelectorAll('.prow').forEach((r) => {
    const t = teile[+r.dataset.i];
    r.addEventListener('pointerenter', () => markiere(t));
    r.addEventListener('pointerleave', () => markiere(null));
    r.addEventListener('click', () => waehleTeil(t));
  });
}

function waehleTeil(t) {
  if (!t) { if (gewaehlt) zeigeModell(); return; }
  gewaehlt = t; markiere(null);
  const p = t.p;
  setzePanel(`
    <div><div class="eyebrow">Teil ${t.nr ?? ''}</div><h1 style="margin-top:8px">${esc(p.name)}</h1>
      <div class="sub">${gramm(p.mass)} · ${zahl(p.w)} × ${zahl(p.d ?? p.w)} × ${zahl(p.h)} mm</div></div>
    <p>${esc(p.info ?? '')}</p>
    <div><h3>Materialien</h3>${(p.materials ?? []).map(([m, a]) => `
      <div class="mrow"><i style="background:${CLASSES[MATERIALS[m]?.cls]?.color ?? '#ccc'}"></i><span>${esc(MATERIALS[m]?.name ?? m)}</span>
        <span class="pct">${a} %</span><span class="go">${gramm((p.mass * a) / 100)}</span><div class="mbar"><b style="width:${a}%"></b></div></div>`).join('')}</div>
    <dl class="facts">
      <div><dt>Bauteil</dt><dd>${esc(p.component_id ?? '–')}</dd></div>
      <div><dt>Material-ID</dt><dd>${esc(p.material_id ?? '–')}</dd></div>
      <div><dt>Form</dt><dd>${p.shape === 'cyl' ? 'Zylinder' : 'Quader'}${p.marks?.length ? `, ${p.marks.length} Details` : ''}</dd></div>
      <div><dt>Explosion</dt><dd>${(p.explode ?? []).map((v) => zahl(v)).join(' / ')} mm</dd></div>
    </dl>`, [{ label: 'Alle Modelle', go: zeigeListe }, { label: aktuell.name, go: zeigeModell }, { label: p.short ?? p.name, go: () => waehleTeil(t) }]);
  markiere(null);
}

// ---------- Laden, Blättern, Direktlink #kat=<id> (wie in der Station) ----------
async function oeffne(id) {
  const lader = datei(id);
  if (!lader) return;
  aktuell = await lader();
  const i = liste.findIndex((k) => k.id === id);
  document.getElementById('titel').textContent = aktuell.name;
  document.getElementById('masse').textContent = `${aktuell.masse} · ${aktuell.gewicht}`;
  document.getElementById('position').innerHTML = `Modell ${i + 1} von ${liste.length} <span>· Pfeiltasten ← → blättern</span>`;
  const klassen = [...new Set(aktuell.parts.map((p) => MATERIALS[p.materials?.[0]?.[0]]?.cls).filter(Boolean))];
  document.getElementById('legende').innerHTML = klassen.map((c) => `<span><i style="background:${CLASSES[c].color}"></i>${CLASSES[c].label}</span>`).join('');
  document.getElementById('titelblock').innerHTML = `<div>Kategorie</div><div>${esc(aktuell.id)}</div><div>Modell</div><div>${aktuell.platzhalter ? 'Platzhalter' : 'handgebaut'}</div>`;
  baue(aktuell);
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
  if (e.key === 'Escape') waehleTeil(null);
});
const ausHash = () => oeffne(location.hash.match(/kat=([\w-]+)/)?.[1] ?? 'smartphone');
addEventListener('hashchange', ausHash);
ausHash();
