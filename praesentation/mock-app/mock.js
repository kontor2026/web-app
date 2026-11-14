// Mock der Stations-App für die Präsentation: Erfassen → Steckbrief → Bauen.
// Erkennung ist simuliert, alles andere sind echte Daten aus backend/seed/kategorien und dieselben 3D-Modelle wie in der App.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { ladeKategorie, baueModell } from '../katalog.js';

const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

const BEISPIELE = [
  { id: 'smartphone', name: 'Altes Handy', kandidaten: [['Smartphone', 94], ['Tablet', 4], ['E-Reader', 2]] },
  { id: 'phone_charger', name: 'Ladegerät', kandidaten: [['Ladegerät', 91], ['Powerbank', 6], ['USB-Stick', 3]] },
  { id: 'earbuds', name: 'Kopfhörer', kandidaten: [['Kabellose Kopfhörer', 88], ['Kopfhörer mit Kabel', 9], ['Fitnessarmband', 3]] },
  { id: 'power_bank', name: 'Powerbank', kandidaten: [['Powerbank', 90], ['Smartphone', 7], ['Externe Festplatte', 3]] },
];
const IDEEN = {
  smartphone: [
    ['Werkstatt-Kamera', 'Das alte Handy filmt die Werkbank, damit alle zusehen können. Halter aus einer Holzleiste.', ['Smartphone', 'Holzleiste · Lager E-04', 'Kabelbinder']],
    ['Musik-Box', 'Ein Schuhkarton wird zum Resonanzkasten und macht den kleinen Lautsprecher laut.', ['Smartphone', 'Schuhkarton · Lager P-11', 'Korken']],
    ['Fahrrad-Navi', 'Ein Stück alter Fahrradschlauch hält das Handy am Lenker.', ['Smartphone', 'Fahrradschlauch · Lager G-02', 'Klettband']],
  ],
};
const IDEEN_STANDARD = [
  ['Ausbauen und einlagern', 'Teile nach Material trennen und ins Lager legen, damit andere sie verbauen können.', ['Gegenstand', 'Sortierkiste']],
  ['Reparieren', 'Oft ist nur ein Teil kaputt. Im Steckbrief steht, wie man es löst.', ['Gegenstand', 'Werkzeug']],
  ['Weitergeben', 'Funktioniert es noch, freut sich jemand anderes darüber.', ['Gegenstand']],
];

const daten = {};
let aktuell = null;

// ---------- Ein Renderer für Vorschaubilder und Steckbrief ----------
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: false });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.toneMapping = THREE.NeutralToneMapping;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
const pmrem = new THREE.PMREMGenerator(renderer);
const umgebung = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

function szene() {
  const s = new THREE.Scene();
  s.environment = umgebung;
  s.environmentIntensity = 0.9;
  const l = new THREE.DirectionalLight('#fff6ea', 2.2);
  l.position.set(0.4, 1, 0.6);
  l.castShadow = true;
  l.shadow.mapSize.set(1024, 1024);
  Object.assign(l.shadow.camera, { left: -0.4, right: 0.4, top: 0.4, bottom: -0.4, near: 0.1, far: 4 });
  s.add(l, new THREE.HemisphereLight('#ffffff', '#c9c2b4', 0.6));
  const boden = new THREE.Mesh(new THREE.PlaneGeometry(4, 4), new THREE.ShadowMaterial({ opacity: 0.16 }));
  boden.rotation.x = -Math.PI / 2;
  boden.receiveShadow = true;
  s.add(boden);
  return s;
}

function rahmen(kamera, modell, faktor = 1.5) {
  const box = new THREE.Box3().setFromObject(modell);
  const r = box.getBoundingSphere(new THREE.Sphere()).radius;
  const c = box.getCenter(new THREE.Vector3());
  kamera.position.copy(c).add(new THREE.Vector3(0.75, 0.95, 1.1).normalize().multiplyScalar((r * faktor) / Math.tan(THREE.MathUtils.degToRad(kamera.fov / 2))));
  kamera.lookAt(c);
  kamera.near = r * 0.05; kamera.far = r * 30;
  kamera.updateProjectionMatrix();
  return c;
}

async function vorschau(b) {
  const s = szene();
  const m = baueModell(daten[b.id]);
  s.add(m.root);
  const kam = new THREE.PerspectiveCamera(30, 16 / 10, 0.01, 10);
  rahmen(kam, m.root, 1.1);
  renderer.setSize(384, 240, false);
  renderer.render(s, kam);
  return renderer.domElement.toDataURL('image/png');
}

// ---------- Erfassen ----------
async function start() {
  await Promise.all(BEISPIELE.map(async (b) => { daten[b.id] = await ladeKategorie(b.id); }));
  const bilder = [];
  for (const b of BEISPIELE) bilder.push(await vorschau(b));
  $('#beispiele').innerHTML = BEISPIELE.map((b, i) => `<button class="foto" data-id="${b.id}"><img src="${bilder[i]}" alt=""><span>${esc(b.name)}</span></button>`).join('');
  $('#beispiele').addEventListener('click', (e) => { const btn = e.target.closest('.foto'); if (btn) scanne(BEISPIELE.find((b) => b.id === btn.dataset.id), btn.querySelector('img').src); });
  steckbriefViewer();
}

function scanne(b, bild) {
  aktuell = b;
  document.querySelectorAll('.foto').forEach((f) => f.classList.toggle('aktiv', f.dataset.id === b.id));
  $('#bild').style.backgroundImage = `url(${bild})`;
  $('.kamera').classList.add('hat-bild', 'scannt');
  $('#kandidaten').hidden = true;
  setTimeout(() => {
    $('.kamera').classList.remove('scannt');
    $('#liste').innerHTML = b.kandidaten.map(([n, p], i) => `<li class="${i === 0 ? 'gewaehlt' : ''}"><span>${esc(n)}</span><b>${p} %</b><i style="--p:${p}%"></i></li>`).join('');
    $('#kandidaten').hidden = false;
  }, 1500);
}
$('#liste').addEventListener('click', (e) => {
  const li = e.target.closest('li');
  if (!li) return;
  document.querySelectorAll('#liste li').forEach((x) => x.classList.toggle('gewaehlt', x === li));
});
$('#bestaetigen').addEventListener('click', () => zeige('steckbrief'));

// ---------- Ansichten ----------
function zeige(v) {
  document.body.dataset.view = v;
  document.querySelectorAll('[data-go]').forEach((b) => {
    b.classList.toggle('aktiv', b.dataset.go === v);
    if (b.dataset.go !== 'erfassen') b.disabled = !aktuell;
  });
  if (v === 'steckbrief') viewer.lade(aktuell);
  if (v === 'bauen') bauen();
}
document.querySelectorAll('[data-go]').forEach((b) => b.addEventListener('click', () => zeige(b.dataset.go)));

// ---------- Steckbrief: Explosionszeichnung + Datenblatt ----------
let viewer;
function steckbriefViewer() {
  const el = $('#viewer');
  const r = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  r.setPixelRatio(Math.min(devicePixelRatio, 2));
  r.toneMapping = THREE.NeutralToneMapping;
  r.outputColorSpace = THREE.SRGBColorSpace;
  r.shadowMap.enabled = true;
  el.prepend(r.domElement);
  const kam = new THREE.PerspectiveCamera(30, 1, 0.01, 10);
  const steuer = new OrbitControls(kam, r.domElement);
  steuer.enableDamping = true;
  let s = szene(), modell = null, t0 = 0, gewaehlt = null;
  new ResizeObserver(() => {
    const { width: w, height: h } = el.getBoundingClientRect();
    r.setSize(w, h, false); kam.aspect = w / Math.max(1, h); kam.updateProjectionMatrix();
  }).observe(el);
  const ray = new THREE.Raycaster(), maus = new THREE.Vector2();
  let unten = null;
  r.domElement.addEventListener('pointerdown', (e) => { unten = [e.clientX, e.clientY]; });
  r.domElement.addEventListener('pointerup', (e) => {
    if (!modell || !unten || Math.hypot(e.clientX - unten[0], e.clientY - unten[1]) > 4) return;
    const b = r.domElement.getBoundingClientRect();
    maus.set(((e.clientX - b.left) / b.width) * 2 - 1, -((e.clientY - b.top) / b.height) * 2 + 1);
    ray.setFromCamera(maus, kam);
    const hit = ray.intersectObjects(modell.teile.map((t) => t.g), true)[0];
    waehle(hit ? modell.teile.find((t) => t.g === hit.object.parent || t.g === hit.object.parent?.parent) : null);
  });
  function waehle(t) {
    gewaehlt = t;
    for (const x of modell.teile) {
      x.g.traverse((o) => {
        if (!o.isMesh) return;
        o.material.transparent = !!t && x !== t ? true : (x.p.opacity ?? 1) < 0.98;
        o.material.opacity = t && x !== t ? 0.12 : (x.p.opacity ?? 1);
      });
    }
    blatt(t);
  }
  (function loop() {
    requestAnimationFrame(loop);
    if (document.body.dataset.view !== 'steckbrief' || !modell) return;
    const k = Math.min(1, (performance.now() - t0) / 1300);
    modell.explode(1 - (1 - k) ** 3);
    steuer.update();
    r.render(s, kam);
  })();
  viewer = {
    lade(b) {
      if (modell) s.remove(modell.root);
      s = szene();
      modell = baueModell(daten[b.id]);
      modell.explode(1);
      s.add(modell.root);
      modell.root.updateMatrixWorld(true);
      const c = rahmen(kam, modell.root, 1.7);
      steuer.target.copy(c);
      modell.explode(0);
      t0 = performance.now() + 250;
      gewaehlt = null;
      blatt(null);
    },
  };
}

function blatt(teil) {
  const d = daten[aktuell.id];
  const werte = (d.werte ?? []).map((w) => `<div class="wert"><span>${esc(w.k)}</span><b>${esc(w.v)}</b><small>${esc(w.hint)}</small></div>`).join('');
  const t = teil?.p;
  $('#blatt').innerHTML = `
    <p class="kicker">${esc(d.klasse)}</p>
    <h1>${esc(d.name)}</h1>
    <p class="meta">${esc(d.masse)} · ${esc(d.gewicht)} · ${d.parts.length} Bauteile</p>
    ${t ? `<div class="teil"><p class="kicker">Bauteil</p><h3>${esc(t.name)}</h3><p>${esc(t.info)}</p>
      <p class="mats">${(t.materials ?? []).map(([m, p]) => `<span>${esc(m)} ${p} %</span>`).join('')}</p></div>`
      : `<p class="hinweis">Tippe ein Bauteil an, um zu sehen, woraus es besteht.</p>`}
    <div class="werte">${werte}</div>
    ${d.entsorgung ? `<div class="entsorgung"><p class="kicker">Entsorgung</p><p>${esc(d.entsorgung.wo)}</p><p class="nicht">${esc(d.entsorgung.nicht)}</p></div>` : ''}
    <button class="primary" id="zu-bauen">Bauideen →</button>`;
  $('#zu-bauen').addEventListener('click', () => zeige('bauen'));
}

// ---------- Bauen ----------
function bauen() {
  const ideen = IDEEN[aktuell.id] ?? IDEEN_STANDARD;
  $('#bauen-titel').textContent = `Was baust du aus ${aktuell.name === 'Altes Handy' ? 'deinem alten Handy' : `„${aktuell.name}“`}?`;
  $('#ideen').innerHTML = ideen.map(([titel, text, teile], i) => `
    <article class="idee" style="--i:${i}"><p class="kicker">Idee ${i + 1}</p><h2>${esc(titel)}</h2><p>${esc(text)}</p>
    <ul>${teile.map((x) => `<li>${esc(x)}</li>`).join('')}</ul><button>Projekt starten</button></article>`).join('');
}

start();
