// Stoffgraph: Gegenstand → Bauteil → Material als 3D-Kraftgraph.
// Materialien liegen im Kern, Bauteile in der mittleren Schale, Gegenstände außen.
import ForceGraph3D from '3d-force-graph';
import { forceRadial } from 'd3-force-3d';
import * as THREE from 'three';
import daten from './daten.json';
import './style.css';

const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
const FARBE = {
  elektro: css('--elektro'), verpackung: css('--verpackung'), textil: css('--textil'), alltag: css('--alltag'),
  bauteil: css('--bauteil'), ink: css('--ink'), card: css('--card'), rule: css('--rule'),
};
const TYP = { objekt: 'Gegenstand', bauteil: 'Bauteil', material: 'Material' };
const GRUPPE = { elektro: 'Elektro', verpackung: 'Verpackung', textil: 'Textil', alltag: 'Alltag' };
const SCHALE = { material: 40, bauteil: 190, objekt: 360 };

// ---------- Daten und Nachbarschaften ----------
const knoten = new Map(daten.nodes.map((n) => [n.id, n]));
const kanten = daten.links.map((l) => ({ ...l, von: l.source, nach: l.target }));
const raus = new Map(), rein = new Map();
for (const l of kanten) {
  (raus.get(l.von) ?? raus.set(l.von, []).get(l.von)).push(l);
  (rein.get(l.nach) ?? rein.set(l.nach, []).get(l.nach)).push(l);
}
for (const n of daten.nodes) {
  n.grad = (raus.get(n.id)?.length ?? 0) + (rein.get(n.id)?.length ?? 0);
  n.farbe = n.typ === 'objekt' ? FARBE[n.gruppe] : n.typ === 'bauteil' ? FARBE.bauteil : n.farbe;
  n.radius = n.typ === 'objekt' ? 3 + 1.3 * Math.log10(n.gramm + 1)
    : n.typ === 'bauteil' ? 1.7 : 3 + 0.9 * Math.sqrt(rein.get(n.id)?.length ?? 1);
}
const materialVon = (cid) => knoten.get(raus.get(cid)[0].nach);
const zahl = (v, s = 1) => v.toLocaleString('de-DE', { maximumFractionDigits: s });
const gramm = (g) => (g >= 1000 ? `${zahl(g / 1000)} kg` : g >= 10 ? `${zahl(g, 0)} g` : `${zahl(g)} g`);

// Gramm eines Materials je Gegenstand (über die Bauteile)
function materialJeObjekt(mid) {
  const summe = new Map();
  for (const lc of rein.get(mid) ?? [])
    for (const lo of rein.get(lc.von) ?? []) summe.set(lo.von, (summe.get(lo.von) ?? 0) + (lo.gramm ?? 0));
  return summe;
}

function umfeld(n) {
  const ids = new Set([n.id]), links = new Set();
  const add = (l) => { links.add(l); ids.add(l.von); ids.add(l.nach); };
  if (n.typ === 'objekt') for (const l of raus.get(n.id) ?? []) { add(l); raus.get(l.nach).forEach(add); }
  if (n.typ === 'bauteil') { raus.get(n.id).forEach(add); (rein.get(n.id) ?? []).forEach(add); }
  if (n.typ === 'material') for (const l of rein.get(n.id) ?? []) { add(l); (rein.get(l.von) ?? []).forEach(add); }
  return { ids, links };
}

// ---------- Darstellung der Knoten: Kugel plus Beschriftung ----------
function beschriftung(text, fett) {
  const px = 44, pad = 16;
  const c = document.createElement('canvas'), g = c.getContext('2d');
  const font = `${fett ? 600 : 500} ${px}px "IBM Plex Sans", system-ui, sans-serif`;
  g.font = font;
  c.width = Math.ceil(g.measureText(text).width) + pad * 2;
  c.height = px + pad;
  g.font = font;
  g.fillStyle = FARBE.card;
  g.globalAlpha = 0.86;
  g.beginPath(); g.roundRect(0, 0, c.width, c.height, c.height / 2); g.fill();
  g.globalAlpha = 1;
  g.fillStyle = FARBE.ink;
  g.textBaseline = 'middle';
  g.fillText(text, pad, c.height / 2 + 2);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, depthWrite: false, transparent: true }));
  const h = fett ? 6.5 : 5.2;
  s.scale.set((h * c.width) / c.height, h, 1);
  s.renderOrder = 10;
  return s;
}

const kugel = new THREE.SphereGeometry(1, 20, 14);
function knotenObjekt(n) {
  const gruppe = new THREE.Group();
  const mat = new THREE.MeshLambertMaterial({ color: n.farbe, transparent: true, opacity: 0.95 });
  const mesh = new THREE.Mesh(kugel, mat);
  mesh.scale.setScalar(n.radius);
  gruppe.add(mesh);
  if (n.typ === 'objekt' && n.handgebaut) {      // Ring: Gegenstand hat schon ein handgebautes 3D-Modell
    const ring = new THREE.Mesh(new THREE.TorusGeometry(n.radius + 1.6, 0.35, 8, 40),
      new THREE.MeshBasicMaterial({ color: n.farbe, transparent: true }));
    gruppe.add(ring);
    n.__ring = ring;
  }
  const label = beschriftung(n.name, n.typ !== 'bauteil');
  label.position.y = n.radius + 4.5;
  gruppe.add(label);
  n.__mat = mat; n.__label = label;
  stil(n);
  return gruppe;
}

// ---------- Graph ----------
let auswahl = null, aktiv = null;   // gewählter Knoten und sein Umfeld { ids, links }
const el = document.getElementById('graph');
const graph = new ForceGraph3D(el, { controlType: 'orbit' })
  .backgroundColor('rgba(0,0,0,0)')
  .showNavInfo(false)
  .nodeId('id')
  .nodeThreeObject(knotenObjekt)
  .nodeLabel((n) => `<div class="tip">${n.name}<small>${TYP[n.typ]}${n.typ === 'objekt' ? ' · ' + gramm(n.gramm) : ''}</small></div>`)
  .linkColor((l) => linkFarbe(l))
  .linkOpacity(1)
  .linkWidth((l) => (aktiv?.links.has(l) ? 0.9 : 0))
  .linkDirectionalParticles((l) => (aktiv?.links.has(l) ? 2 : 0))
  .linkDirectionalParticleWidth(1.6)
  .linkDirectionalParticleSpeed(0.006)
  .linkDirectionalParticleColor((l) => knoten.get(l.von).farbe)
  .onNodeClick((n) => waehle(n, true))
  .onNodeHover((n) => { el.style.cursor = n ? 'pointer' : ''; })
  .onBackgroundClick(() => waehle(null, true))
  .warmupTicks(60)
  .cooldownTime(9000);

graph.d3Force('radial', forceRadial((n) => SCHALE[n.typ]).strength(0.55));
graph.d3Force('charge').strength((n) => (n.typ === 'bauteil' ? -14 : -40));
graph.d3Force('link').distance((l) => (l.typ === 'material' ? 120 : 90)).strength(0.08);

const steuerung = graph.controls();
steuerung.autoRotate = true;
steuerung.autoRotateSpeed = 0.5;
steuerung.enableDamping = true;
el.addEventListener('pointerdown', () => {
  steuerung.autoRotate = false;
  document.getElementById('hinweis').style.opacity = 0;
}, { once: true });
graph.cameraPosition({ x: 0, y: 140, z: 820 });
addEventListener('resize', () => graph.width(innerWidth).height(innerHeight));

// ---------- Filter ----------
let gruppe = 'alle';
function setzeDaten() {
  const objekte = daten.nodes.filter((n) => n.typ === 'objekt' && (gruppe === 'alle' || n.gruppe === gruppe));
  const ids = new Set(objekte.map((n) => n.id)), links = [];
  for (const o of objekte) for (const l of raus.get(o.id) ?? []) { links.push(l); ids.add(l.nach); }
  for (const id of [...ids]) if (knoten.get(id).typ === 'bauteil') for (const l of raus.get(id)) { links.push(l); ids.add(l.nach); }
  graph.graphData({ nodes: daten.nodes.filter((n) => ids.has(n.id)), links: links.map((l) => Object.assign(l, { source: l.von, target: l.nach })) });
  document.getElementById('zahlen').textContent =
    `${objekte.length} Gegenstände · ${[...ids].filter((i) => i[0] === 'c').length} Bauteile · ${[...ids].filter((i) => i[0] === 'm').length} Materialien`;
  return ids;
}
let sichtbar = setzeDaten();

for (const b of document.querySelectorAll('#filter button')) {
  b.addEventListener('click', () => {
    gruppe = b.dataset.gruppe;
    document.querySelectorAll('#filter button').forEach((x) => x.setAttribute('aria-checked', String(x === b)));
    sichtbar = setzeDaten();
    if (auswahl && !sichtbar.has(auswahl.id)) waehle(null, true); else faerbe();
  });
}

// ---------- Auswahl und Hervorhebung ----------
function linkFarbe(l) {
  if (aktiv?.links.has(l)) return knoten.get(l.von).farbe;
  return aktiv ? 'rgba(141,145,138,0.04)' : 'rgba(141,145,138,0.16)';
}
function stil(n) {                         // Deckkraft und Beschriftung eines Knotens nach der aktuellen Auswahl
  if (!n.__mat) return;
  const an = !aktiv || aktiv.ids.has(n.id);
  n.__mat.opacity = an ? 0.95 : 0.1;
  if (n.__ring) n.__ring.material.opacity = an ? 1 : 0.1;
  n.__label.visible = aktiv ? aktiv.ids.has(n.id) && (n.typ !== 'bauteil' || auswahl.typ !== 'material' || n === auswahl)
    : n.typ === 'material';
}
function faerbe() {
  daten.nodes.forEach(stil);
  graph.linkColor(graph.linkColor()).linkWidth(graph.linkWidth()).linkDirectionalParticles(graph.linkDirectionalParticles());
}

function fokus(n) {
  if (n.x === undefined) return;
  const abstand = n.typ === 'objekt' ? 190 : 260;
  const r = Math.hypot(n.x, n.y, n.z) || 1;
  const f = 1 + abstand / r;
  graph.cameraPosition({ x: n.x * f, y: n.y * f, z: n.z * f }, { x: 0, y: 0, z: 0 }, 1100);
}

function waehle(n, hash) {
  auswahl = n;
  aktiv = n ? umfeld(n) : null;
  steuerung.autoRotate = false;
  faerbe();
  zeigeDetail(n);
  if (n) fokus(n);
  if (hash) history.replaceState(null, '', n ? `#${n.id[0]}=${n.key}` : location.pathname + location.search);
}

// ---------- Detailansicht ----------
const detail = document.getElementById('detail');
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
const punkt = (farbe, k = 'mittel') => `<i class="punkt ${k}" style="--c:${farbe}"></i>`;
const zeile = (n, wert, unter, anteil, farbe) => `
  <button class="zeile" data-id="${n.id}">
    <span class="name">${punkt(n.farbe, n.typ === 'bauteil' ? 'klein' : 'mittel')}<span>${esc(n.name)}</span></span>
    <span class="wert">${wert ?? ''}</span>
    ${unter ? `<span class="unter">${unter}</span>` : ''}
    ${anteil !== undefined ? `<span class="balken"><i style="width:${Math.max(2, anteil * 100)}%;--c:${farbe ?? n.farbe}"></i></span>` : ''}
  </button>`;
const fakt = (wert, text) => `<div class="fakt"><b>${wert}</b><span>${text}</span></div>`;

function zeigeDetail(n) {
  if (!n) { detail.hidden = true; return; }
  let kopf = '', liste = '';
  if (n.typ === 'objekt') {
    const teile = (raus.get(n.id) ?? []).map((l) => ({ c: knoten.get(l.nach), g: l.gramm ?? 0 })).sort((a, b) => b.g - a.g);
    const proMat = new Map();
    for (const { c, g } of teile) { const m = materialVon(c.id); proMat.set(m, (proMat.get(m) ?? 0) + g); }
    const mats = [...proMat].sort((a, b) => b[1] - a[1]);
    const summe = teile.reduce((s, t) => s + t.g, 0) || 1;
    kopf = `<p class="en">${esc(n.en)}</p>
      <div class="fakten">${fakt(gramm(n.gramm), 'Gewicht')}${fakt(teile.length, 'Bauteile')}${fakt(mats.length, 'Materialien')}</div>
      <p class="text"><span class="marke">${GRUPPE[n.gruppe]}</span> <span class="marke ${n.handgebaut ? 'gut' : ''}">${n.handgebaut ? '3D-Modell handgebaut' : '3D-Modell Platzhalter'}</span></p>`;
    liste = `<h3>Zusammensetzung</h3>${mats.map(([m, g]) => zeile(m, `${zahl((g / summe) * 100, 0)} %`, '', g / summe)).join('')}
      <h3>Bauteile</h3>${teile.map(({ c, g }) => { const m = materialVon(c.id); return zeile(c, g ? gramm(g) : '', `${punkt(m.farbe, 'klein')}${esc(m.name)}`); }).join('')}`;
  } else if (n.typ === 'bauteil') {
    const m = materialVon(n.id);
    const objs = (rein.get(n.id) ?? []).map((l) => ({ o: knoten.get(l.von), g: l.gramm ?? 0 })).sort((a, b) => b.g - a.g);
    kopf = `<div class="fakten">${fakt(objs.length, 'Gegenstände')}${fakt(esc(m.klasse), 'Klasse')}${fakt(m.recycling || '–', 'Recycling')}</div>
      <p class="text">${esc(n.hint ?? '')}</p>`;
    liste = `<h3>Material</h3>${zeile(m, '', esc(m.klasse))}
      <h3>Steckt in</h3>${objs.map(({ o, g }) => zeile(o, g ? gramm(g) : '', GRUPPE[o.gruppe])).join('')}`;
  } else {
    const jeObj = [...materialJeObjekt(n.id)].map(([id, g]) => ({ o: knoten.get(id), g })).sort((a, b) => b.g - a.g);
    const max = jeObj[0]?.g || 1;
    const teile = (rein.get(n.id) ?? []).map((l) => knoten.get(l.von));
    kopf = `<p class="en">${esc(n.en)}</p>
      <div class="fakten">${fakt(jeObj.length, 'Gegenstände')}${fakt(teile.length, 'Bauteile')}${fakt(n.recycling || '–', 'Recycling')}</div>
      <p class="text"><span class="marke">${esc(n.klasse)}</span> ${esc(n.text)}</p>`;
    liste = `<h3>Am meisten in</h3>${jeObj.map(({ o, g }) => zeile(o, g ? gramm(g) : '', '', g / max, n.farbe)).join('')}
      <h3>Bauteile aus ${esc(n.name)}</h3>${teile.map((c) => zeile(c, '', '')).join('')}`;
  }
  detail.innerHTML = `<div class="oben">
      <div class="pfad">${punkt(n.farbe, 'klein')}${TYP[n.typ]}<button class="zu" aria-label="Schließen">×</button></div>
      <h2>${esc(n.name)}</h2>${kopf}</div>
    <div class="liste">${liste}</div>`;
  detail.hidden = false;
}
detail.addEventListener('click', (e) => {
  if (e.target.closest('.zu')) return waehle(null, true);
  const z = e.target.closest('.zeile');
  if (z) {
    const n = knoten.get(z.dataset.id);
    if (!sichtbar.has(n.id)) document.querySelector('#filter [data-gruppe="alle"]').click();
    waehle(n, true);
  }
});

// ---------- Suche ----------
const suche = document.getElementById('suche'), treffer = document.getElementById('treffer');
const RANG = { objekt: 0, material: 1, bauteil: 2 };
let liste = [], markiert = -1;
function zeigeTreffer() {
  const q = suche.value.trim().toLowerCase();
  if (!q) { treffer.hidden = true; suche.setAttribute('aria-expanded', 'false'); return; }
  liste = daten.nodes
    .map((n) => {
      const a = n.name.toLowerCase(), b = (n.en ?? '').toLowerCase();
      const p = a.startsWith(q) ? 0 : b.startsWith(q) ? 1 : a.includes(q) ? 2 : b.includes(q) ? 3 : -1;
      return { n, p };
    })
    .filter((x) => x.p >= 0)
    .sort((x, y) => x.p - y.p || RANG[x.n.typ] - RANG[y.n.typ] || x.n.name.localeCompare(y.n.name, 'de'))
    .slice(0, 12).map((x) => x.n);
  markiert = liste.length ? 0 : -1;
  treffer.innerHTML = liste.length
    ? liste.map((n, i) => `<li role="option" id="t${i}" aria-selected="${i === markiert}" data-i="${i}">${punkt(n.farbe, n.typ === 'bauteil' ? 'klein' : 'mittel')}${esc(n.name)}<span class="typ">${TYP[n.typ]}</span></li>`).join('')
    : '<li class="leer">Nichts gefunden</li>';
  treffer.hidden = false;
  suche.setAttribute('aria-expanded', 'true');
}
function nimm(i) {
  const n = liste[i];
  if (!n) return;
  suche.value = '';
  treffer.hidden = true;
  if (!sichtbar.has(n.id)) document.querySelector('#filter [data-gruppe="alle"]').click();
  waehle(n, true);
  suche.blur();
}
suche.addEventListener('input', zeigeTreffer);
suche.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
    e.preventDefault();
    markiert = (markiert + (e.key === 'ArrowDown' ? 1 : -1) + liste.length) % Math.max(1, liste.length);
    treffer.querySelectorAll('li').forEach((li, i) => li.setAttribute('aria-selected', String(i === markiert)));
    suche.setAttribute('aria-activedescendant', `t${markiert}`);
  } else if (e.key === 'Enter') nimm(markiert);
  else if (e.key === 'Escape') { suche.value = ''; treffer.hidden = true; }
});
treffer.addEventListener('mousedown', (e) => { const li = e.target.closest('li[data-i]'); if (li) { e.preventDefault(); nimm(+li.dataset.i); } });
suche.addEventListener('blur', () => setTimeout(() => { treffer.hidden = true; }, 100));
addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && document.activeElement !== suche) waehle(null, true);
  if (e.key === '/' && document.activeElement !== suche) { e.preventDefault(); suche.focus(); }
});

// ---------- Legende ----------
const klassen = new Map(daten.nodes.filter((n) => n.typ === 'material').map((n) => [n.klasse, n.farbe]));
document.getElementById('klassen').innerHTML = [...klassen].map(([k, f]) => `<li>${punkt(f, 'mittel')}${esc(k)}</li>`).join('');

// ---------- Direktlink #o=smartphone, #c=li_ion_battery, #m=aluminium ----------
function ausHash() {
  const m = location.hash.match(/^#([ocm])=(.+)$/);
  const n = m && knoten.get(`${m[1]}:${decodeURIComponent(m[2])}`);
  if (n) setTimeout(() => waehle(n, false), 1500);   // Layout erst etwas einschwingen lassen
}
addEventListener('hashchange', ausHash);
ausHash();
