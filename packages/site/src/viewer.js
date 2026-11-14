// 3D-Ansicht eines Kategorie-Modells (three.js), gemeinsam für „3D-Modelle“ und „Lebensweg“.
// Gleiche Teile, Farben und Explosion wie die Zeichnung der Station (js/iso.js), nur frei drehbar.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';
import { CLASSES, MATERIALS } from '../../../js/data/catalog.js';
import { esc, gramm, ruhig } from './shell.js';
import { stoff, koerperGeometrie, studio, eigenschaften, nachbearbeitung } from './foto.js';

const LADE = import.meta.glob('../../../backend/seed/kategorien/*.json', { import: 'default' });
export const ladeModell = (id) => LADE[`../../../backend/seed/kategorien/${id}.json`]?.();
export const hatModell = (id) => !!LADE[`../../../backend/seed/kategorien/${id}.json`];
export const materialVon = (p) => MATERIALS[p.materials?.[0]?.[0]];
export const farbeVon = (p) => p.color ?? CLASSES[materialVon(p)?.cls]?.color ?? '#cccccc';

const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();

// Grundriss eines Teils: abgerundetes Rechteck oder Ellipse, Ursprung linke hintere Ecke
function grundriss(t) {
  const s = new THREE.Shape(), w = t.w, d = t.d ?? t.w;
  if (t.shape === 'cyl') { s.absellipse(w / 2, d / 2, w / 2, d / 2, 0, Math.PI * 2, false, 0); return s; }
  const r = Math.max(0, Math.min(t.r ?? 0, w / 2, d / 2));
  s.moveTo(r, 0); s.lineTo(w - r, 0); s.quadraticCurveTo(w, 0, w, r); s.lineTo(w, d - r); s.quadraticCurveTo(w, d, w - r, d);
  s.lineTo(r, d); s.quadraticCurveTo(0, d, 0, d - r); s.lineTo(0, r); s.quadraticCurveTo(0, 0, r, 0);
  return s;
}

/**
 * el: Container. Optionen: onHover(index|null), onSelect(index|null), tip (Element für Tooltip).
 * Rückgabe: lade(obj), explosion(0|1), nummern(bool), foto(bool), markiere(i), waehle(i), faerbe(fn(part)→Farbe|null)
 * Foto-Ansicht (Standard): physikalische Materialien, Studiolicht, Schatten, Umgebungsverdeckung (foto.js).
 * Gezeichnet wird nur, wenn sich etwas ändert, damit langsame Rechner flüssig bleiben.
 */
export function erzeugeViewer(el, { onHover, onSelect, tip } = {}) {
  const INK = new THREE.Color(css('--ink')), AKZENT = new THREE.Color(css('--accent'));
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  el.append(renderer.domElement);
  const labels = new CSS2DRenderer();
  labels.domElement.className = 'labels';
  el.append(labels.domElement);

  const scene = new THREE.Scene();
  const licht = studio(renderer, scene);
  const kamera = new THREE.OrthographicCamera(-1, 1, 1, -1, -10000, 10000);
  const nach = nachbearbeitung(renderer, scene, kamera);
  let geaendert = true, fotoAn = true;
  const neu = () => { geaendert = true; };
  const steuerung = new OrbitControls(kamera, labels.domElement);
  steuerung.enableDamping = true;
  const modell = new THREE.Group();
  scene.add(modell);

  new ResizeObserver(() => {
    const { width: w, height: h } = el.getBoundingClientRect();
    renderer.setSize(w, h); labels.setSize(w, h); nach.setSize(w, h); neu();
    const a = w / Math.max(h, 1);
    kamera.left = -a; kamera.right = a; kamera.top = 1; kamera.bottom = -1;
    kamera.updateProjectionMatrix();
  }).observe(el);

  let teile = [], explodiert = 1, hot = null, gewaehlt = null, animationNr = 0, farbFn = null;

  function lade(obj) {
    // Nummern selbst entfernen: CSS2DRenderer räumt nur direkte Kinder auf, unsere hängen in Gruppen
    modell.traverse((o) => { if (o.isCSS2DObject) o.element.remove(); });
    modell.traverse((o) => { o.geometry?.dispose(); o.material?.dispose?.(); });
    modell.clear();
    teile = []; hot = null; gewaehlt = null;
    let nr = 0;
    for (const p of obj.parts) {
      const farbe = new THREE.Color(farbeVon(p)), g = new THREE.Group();
      const geo = koerperGeometrie(p);                          // Station: x Breite, y Tiefe, z Höhe → three: X, Z, Y
      const mesh = new THREE.Mesh(geo, stoff(p, farbe, p.opacity ?? 1));
      mesh.castShadow = mesh.receiveShadow = true;
      const kanten = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 30), new THREE.LineBasicMaterial({ color: INK, transparent: true }));
      kanten.userData.kante = true;
      g.add(mesh, kanten);
      const marks = [];
      for (const m of p.marks ?? []) {
        const mg = new THREE.ShapeGeometry(grundriss(m), 24);
        mg.rotateX(Math.PI / 2); mg.translate(m.x, p.h + 0.04, m.y);
        const e = eigenschaften(p), o = p.opacity ?? 1;
        const mm = new THREE.Mesh(mg, new THREE.MeshPhysicalMaterial({ color: new THREE.Color(m.fill ?? farbe.clone().multiplyScalar(0.78)),
          metalness: e.m ?? 0, roughness: Math.max(0.25, e.r), clearcoat: e.cc ?? 0, side: THREE.DoubleSide, transparent: o < 0.98, opacity: o,
          polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1 }));
        mm.receiveShadow = true;
        if (m.zeichnung) mm.userData.kante = true;            // nur in der Zeichnung, z. B. aufgemalte Öffnung
        marks.push({ mesh: mm, farbe: mm.material.color.clone() });
        const ml = new THREE.LineSegments(new THREE.EdgesGeometry(mg), new THREE.LineBasicMaterial({ color: INK, transparent: true, opacity: 0.6 }));
        ml.userData.kante = true;
        g.add(mm, ml);
      }
      g.position.set(p.x, p.z, p.y);
      const t = { p, g, mesh, marks, farbe, i: teile.length, ex: new THREE.Vector3(p.explode?.[0] ?? 0, p.explode?.[2] ?? 0, p.explode?.[1] ?? 0),
        basis: new THREE.Vector3(p.x, p.z, p.y), opacity: p.opacity ?? 1, nr: p.label === false ? null : String(++nr).padStart(2, '0') };
      mesh.userData.teil = t;
      if (t.nr) {
        const b = document.createElement('button');
        b.className = 'ballon'; b.innerHTML = `<b>${t.nr}</b>`; b.title = p.name;
        b.addEventListener('click', () => waehle(t.i, true));
        b.addEventListener('pointerenter', () => markiere(t.i, true));
        b.addEventListener('pointerleave', () => markiere(null, true));
        const l = new CSS2DObject(b);
        l.position.set(p.w / 2, p.h, (p.d ?? p.w) / 2);
        g.add(l);
      }
      modell.add(g); teile.push(t);
    }
    explosion(1, false);
    modell.position.set(0, 0, 0); modell.updateMatrixWorld(true);
    const box = new THREE.Box3().setFromObject(modell);
    modell.position.copy(box.getCenter(new THREE.Vector3()).negate());
    const r = box.getBoundingSphere(new THREE.Sphere()).radius;
    kamera.position.set(1, 0.95, 1.25).normalize().multiplyScalar(r * 4);
    kamera.zoom = 1 / (r * 1.08);
    kamera.near = r * 0.5; kamera.far = r * 8;                // enger Tiefenbereich für die Umgebungsverdeckung
    kamera.updateProjectionMatrix();
    modell.updateMatrixWorld(true);
    licht.passe(new THREE.Box3().setFromObject(modell));
    nach.radius(r);
    foto(fotoAn);
    steuerung.target.set(0, 0, 0); steuerung.update();
    faerbe(farbFn);
    explosion(explodiert, !ruhig);
  }

  function explosion(ziel, animiert = true) {
    explodiert = ziel;
    // Eigene Teileliste und Laufnummer: eine neue Animation löst die alte ab (sonst Fehler beim schnellen Blättern)
    const eigene = teile, lauf = ++animationNr;
    const start = eigene.map((t) => t.g.position.clone()), t0 = performance.now(), dauer = animiert ? 900 : 0;
    const schritt = (jetzt) => {
      if (lauf !== animationNr) return;
      const k = dauer ? Math.min(1, (jetzt - t0) / dauer) : 1;
      const e = k < 0.5 ? 4 * k ** 3 : 1 - (-2 * k + 2) ** 3 / 2;
      eigene.forEach((t, i) => t.g.position.lerpVectors(start[i], t.basis.clone().addScaledVector(t.ex, ziel), e));
      neu();
      if (k < 1) requestAnimationFrame(schritt);
    };
    schritt(performance.now());
  }

  // Andere Einfärbung, z. B. nach Tonne: fn(part) → Farbe oder null (= Materialfarbe)
  function faerbe(fn) {
    farbFn = fn;
    for (const t of teile) {
      const c = fn?.(t.p);
      const m = t.mesh.material;
      m.userData.map ??= m.map;                                 // Holzmaserung nur in Materialfarbe
      if (m.map !== (c ? null : m.userData.map)) { m.map = c ? null : m.userData.map; m.needsUpdate = true; }
      m.color.set(c ?? (m.map ? 0xffffff : t.farbe));
      t.marks.forEach((m) => m.mesh.material.color.copy(c ? new THREE.Color(c).multiplyScalar(0.85) : m.farbe));
    }
    neu();
  }

  // Abblenden: nur transparent zeichnen, wenn nötig. Sonst sieht Glas (Transmission) die Teile dahinter nicht.
  function blende(m, an) {
    m.userData.o0 ??= m.opacity;
    m.opacity = m.userData.o0 * (an ? 1 : 0.22);
    const tr = m.opacity < 0.98;
    if (m.transparent !== tr) { m.transparent = tr; m.needsUpdate = true; }
  }

  // Foto (Standard) oder Zeichnung mit Kanten wie die Station
  function foto(an) {
    fotoAn = an;
    licht.an(an);
    modell.traverse((o) => { if (o.userData.kante) o.visible = !an; });
    neu();
  }

  function markiere(i, vonHier = false) {
    hot = i == null ? null : teile[i];
    const aktiv = hot ?? gewaehlt;
    for (const x of teile) {
      const an = !aktiv || x === aktiv;
      blende(x.mesh.material, an);
      x.g.children.forEach((c) => {
        if (c.isLineSegments) { c.material.color.copy(x === aktiv ? AKZENT : INK); c.material.opacity = an ? 1 : 0.2; }
        else if (c !== x.mesh && c.material) blende(c.material, an);
        if (c.isCSS2DObject) { c.element.classList.toggle('aus', !an); c.element.classList.toggle('hot', x === aktiv); }
      });
    }
    neu();
    if (vonHier) onHover?.(hot?.i ?? null);
  }
  function waehle(i, vonHier = false) {
    gewaehlt = i == null ? null : teile[i];
    markiere(null);
    if (vonHier) onSelect?.(gewaehlt?.i ?? null);
  }

  const ray = new THREE.Raycaster(), maus = new THREE.Vector2();
  let gezogen = false;
  const flaeche = labels.domElement;
  flaeche.addEventListener('pointerdown', () => { gezogen = false; });
  flaeche.addEventListener('pointermove', (e) => {
    gezogen = gezogen || e.buttons > 0;
    if (e.buttons) return;
    const r = flaeche.getBoundingClientRect();
    maus.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(maus, kamera);
    const treffer = ray.intersectObjects(teile.map((t) => t.mesh))[0]?.object.userData.teil ?? null;
    if (treffer !== hot) markiere(treffer?.i ?? null, true);
    flaeche.style.cursor = treffer ? 'pointer' : '';
    if (!tip) return;
    tip.hidden = !treffer;
    if (treffer) {
      tip.innerHTML = `${treffer.nr ? `<span class="n">${treffer.nr}</span>` : ''}<b>${esc(treffer.p.name)}</b><small>${esc(materialVon(treffer.p)?.name ?? '')} · ${gramm(treffer.p.mass)}</small>`;
      tip.style.left = `${e.clientX + 14}px`; tip.style.top = `${e.clientY + 14}px`;
    }
  });
  flaeche.addEventListener('pointerleave', () => { markiere(null, true); if (tip) tip.hidden = true; });
  flaeche.addEventListener('click', () => { if (!gezogen) waehle(hot?.i ?? null, true); });

  steuerung.addEventListener('change', neu);
  renderer.setAnimationLoop(() => {
    steuerung.update();
    if (!geaendert) return;
    geaendert = false;
    if (fotoAn) nach.render(); else renderer.render(scene, kamera);
    labels.render(scene, kamera);
  });

  return {
    lade, explosion, faerbe, markiere, waehle, foto,
    nummern: (an) => flaeche.classList.toggle('ohne-nummern', !an),
    get teile() { return teile; },
  };
}
