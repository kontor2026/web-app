// 3D-Ansicht eines Kategorie-Modells (three.js), gemeinsam für „3D-Modelle“ und „Lebensweg“.
// Gleiche Teile, Farben und Explosion wie die Zeichnung der Station (js/iso.js), nur frei drehbar.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';
import { CLASSES, MATERIALS } from '../../../js/data/catalog.js';
import { esc, gramm, ruhig } from './shell.js';
import { etikettGeometrie, stoff, koerperGeometrie, studio, eigenschaften, nachbearbeitung, stapelSuchen, huellenMesh } from './foto.js';

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

// Etiketten, Banderolen, Manschetten, Ringe: ein rundes Teil, das zusammengebaut ein anderes rundes Teil umschließt
// (Grundriss enthält dessen Grundriss, Höhen überlappen), wird in der Foto-Ansicht als dünne, unten und oben offene
// Hülle gezeigt statt als volle Scheibe. Rückgabe: Map Teil → Teil mit wand/boden.
function umhuellungen(parts) {
  const m = new Map();
  for (const p of parts) {
    if (p.shape !== 'cyl' || p.wand > 0 || p.form) continue;
    const pd = p.d ?? p.w;
    let wand = Infinity;
    const stuecke = [];
    for (const q of parts) {
      if (q === p || q.shape !== 'cyl') continue;
      const qd = q.d ?? q.w;
      const innen = q.x >= p.x - 0.2 && q.y >= p.y - 0.2 && q.x + q.w <= p.x + p.w + 0.2 && q.y + qd <= p.y + pd + 0.2;
      const von = Math.max(p.z, q.z), bis = Math.min(p.z + p.h, q.z + q.h);
      if (!innen || q.w < p.w * 0.6 || bis <= von) continue;
      stuecke.push([von, bis]);
      wand = Math.min(wand, (p.w - q.w) / 2, (pd - qd) / 2);
    }
    // Nur echte Umhüllung: der Körper darin reicht über die ganze Höhe (sonst z. B. Deckel über dem Hals, der oben zu ist)
    stuecke.sort((a, b) => a[0] - b[0]);
    let bedeckt = 0, ende = p.z;
    for (const [von, bis] of stuecke) { if (bis > ende) { bedeckt += bis - Math.max(von, ende); ende = bis; } }
    if (wand < Infinity && bedeckt >= p.h * 0.95) m.set(p, { ...p, wand: Math.max(0.35, wand), boden: 0 });
  }
  return m;
}

// Dünne, senkrechte Etiketten (unter 1,5 mm), die zusammengebaut seitlich an einem runden Körper anliegen:
// Map Etikett → Körper. Sie werden in der Foto-Ansicht um den Körper gebogen.
function flacheEtiketten(parts) {
  const m = new Map();
  for (const p of parts) {
    const pd = p.d ?? p.w;
    if (p.shape !== 'box' || Math.min(p.w, pd) > 1.5 || p.h < 3 * Math.min(p.w, pd)) continue;
    let best = null, bestH = 0;
    for (const q of parts) {
      if (q === p || q.shape !== 'cyl') continue;
      const qd = q.d ?? q.w, tol = 2;
      const anX = (Math.abs(p.x - (q.x + q.w)) < tol || Math.abs(p.x + p.w - q.x) < tol) && p.y >= q.y - tol && p.y + pd <= q.y + qd + tol;
      const anY = (Math.abs(p.y - (q.y + qd)) < tol || Math.abs(p.y + pd - q.y) < tol) && p.x >= q.x - tol && p.x + p.w <= q.x + q.w + tol;
      const ueber = Math.min(p.z + p.h, q.z + q.h) - Math.max(p.z, q.z);
      if ((anX || anY) && ueber > bestH) { best = q; bestH = ueber; }
    }
    if (best && bestH > p.h * 0.5) m.set(p, best);
  }
  return m;
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
  // Langsam um das Objekt kreisen (eine Runde in etwa 50 s); bei „weniger Bewegung“ aus
  steuerung.autoRotate = !ruhig;
  steuerung.autoRotateSpeed = 1.2;
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
    const huellen = umhuellungen(obj.parts), etiketten = flacheEtiketten(obj.parts);
    for (const p of obj.parts) {
      const farbe = new THREE.Color(farbeVon(p)), g = new THREE.Group();
      const geo = etiketten.has(p) ? etikettGeometrie(p, etiketten.get(p)) : koerperGeometrie(huellen.get(p) ?? p);                          // Station: x Breite, y Tiefe, z Höhe → three: X, Z, Y
      const mesh = new THREE.Mesh(geo, stoff(p, farbe, p.opacity ?? 1));
      mesh.castShadow = mesh.receiveShadow = true;
      // Gegen Flimmern bei bündig aufeinanderliegenden Flächen: feste Rangfolge, das zuerst gelistete (oberste) Teil gewinnt
      const rang = obj.parts.length - teile.length;
      Object.assign(mesh.material, { polygonOffset: true, polygonOffsetFactor: 0, polygonOffsetUnits: -4 * rang });
      const kanten = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 30), new THREE.LineBasicMaterial({ color: INK, transparent: true }));
      kanten.userData.kante = true;
      g.add(mesh, kanten);
      const marks = [];
      for (const m of huellen.has(p) || etiketten.has(p) ? [] : p.marks ?? []) {   // Banderolen: aufgemalte Ringe entfallen, die Hülle ist echt
        const mg = new THREE.ShapeGeometry(grundriss(m), 24);
        mg.rotateX(Math.PI / 2); mg.translate(m.x, p.h + 0.12, m.y);
        const e = eigenschaften(p), o = p.opacity ?? 1;
        const mm = new THREE.Mesh(mg, new THREE.MeshPhysicalMaterial({ color: new THREE.Color(m.fill ?? farbe.clone().multiplyScalar(0.78)),
          metalness: e.m ?? 0, roughness: Math.max(0.25, e.r), clearcoat: e.cc ?? 0, side: THREE.DoubleSide, transparent: o < 0.98, opacity: o,
          polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -4 * rang - 2 }));
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
        b.addEventListener('pointerdown', (e) => e.stopPropagation());   // sonst fängt OrbitControls den Tap ab
        b.addEventListener('click', (e) => { e.stopPropagation(); waehle(t.i, true); });
        b.addEventListener('pointerenter', () => markiere(t.i, true));
        b.addEventListener('pointerleave', () => markiere(null, true));
        const l = new CSS2DObject(b);
        l.position.set(p.w / 2, p.h, (p.d ?? p.w) / 2);
        g.add(l);
      }
      modell.add(g); teile.push(t);
    }
    // Foto-Ansicht: gestapelte Scheiben (Flaschenschulter, Schuh, Ball) als eine glatte Hülle zeigen
    for (const kette of stapelSuchen(obj.parts, farbeVon)) {
      const unten = teile[kette[0]], p0 = unten.p;
      const h = huellenMesh(kette.map((i) => obj.parts[i]), unten.mesh.material.clone());
      h.geometry.translate(-p0.x, -p0.z, -p0.y);
      h.userData.nurFoto = true;
      unten.g.add(h);
      unten.huelle = h;
      kette.forEach((i, n) => {
        teile[i].mesh.userData.ersetzt = true;
        if (n < kette.length - 1) teile[i].marks.forEach((m) => { m.mesh.userData.ersetzt = true; });
      });
    }
    // Ausschnitt für beide Zustände messen: Mitte und Größe, damit die Kamera beim Umschalten mitgeht
    modell.position.set(0, 0, 0);
    ausschnitt = null;
    ausschnitt = [0, 1].map((x) => {
      explosion(x, false); modell.updateMatrixWorld(true);
      const b = new THREE.Box3().setFromObject(modell);
      return { mitte: b.getCenter(new THREE.Vector3()), r: b.getBoundingSphere(new THREE.Sphere()).radius, box: b };
    });
    explosion(explodiert ? 1 : 0, false);
    gezeigt = explodiert ? 1 : 0;
    const a = ausschnitt[gezeigt], r = ausschnitt[1].r;
    // Modell auf die Mitte des explodierten Zustands, die Kamera blickt auf den gezeigten Zustand
    modell.position.copy(ausschnitt[1].mitte).negate();
    ausschnitt.forEach((x) => x.blick = x.mitte.clone().sub(ausschnitt[1].mitte));
    kamera.position.set(1, 0.95, 1.25).normalize().multiplyScalar(r * 4).add(a.blick);
    kamera.zoom = 1 / (a.r * 1.08);
    kamera.near = r * 0.5; kamera.far = r * 8;                // enger Tiefenbereich für die Umgebungsverdeckung
    kamera.updateProjectionMatrix();
    modell.updateMatrixWorld(true);
    licht.passe(new THREE.Box3().setFromObject(modell));
    nach.radius(ausschnitt[0].r);                              // Kontaktschatten nach Größe des Gegenstands, nicht der Explosion
    foto(fotoAn);
    steuerung.target.copy(a.blick); steuerung.update(); steuerung.saveState();   // Doppeltippen kehrt hierher zurück
    faerbe(farbFn);
    explosion(explodiert, !ruhig);
  }

  let ausschnitt = null, gezeigt = 1;
  function explosion(ziel, animiert = true) {
    explodiert = ziel;
    // Kamera folgt: Blickpunkt und Zoom gleiten zum Ausschnitt des Zielzustands, eigener Zoom des Nutzers bleibt erhalten
    const vonZiel = steuerung.target.clone(), vonKam = kamera.position.clone(), vonZoom = kamera.zoom;
    const quelle = ausschnitt?.[gezeigt], dahin = ausschnitt?.[ziel ? 1 : 0];
    const nachZiel = dahin?.blick ? dahin.blick.clone() : vonZiel;
    const nachZoom = dahin ? vonZoom * (quelle.r / dahin.r) : vonZoom;
    if (ausschnitt?.[0].blick && animiert) gezeigt = ziel ? 1 : 0;
    // Eigene Teileliste und Laufnummer: eine neue Animation löst die alte ab (sonst Fehler beim schnellen Blättern)
    const eigene = teile, lauf = ++animationNr;
    const start = eigene.map((t) => t.g.position.clone()), t0 = performance.now(), dauer = animiert ? 900 : 0;
    const schritt = (jetzt) => {
      if (lauf !== animationNr) return;
      const k = dauer ? Math.min(1, (jetzt - t0) / dauer) : 1;
      const e = k < 0.5 ? 4 * k ** 3 : 1 - (-2 * k + 2) ** 3 / 2;
      eigene.forEach((t, i) => t.g.position.lerpVectors(start[i], t.basis.clone().addScaledVector(t.ex, ziel), e));
      if (ausschnitt?.[0].blick && animiert) {
        const d = vonZiel.clone().lerp(nachZiel, e).sub(steuerung.target);
        steuerung.target.add(d); kamera.position.add(d);
        kamera.zoom = vonZoom + (nachZoom - vonZoom) * e; kamera.updateProjectionMatrix();
      }
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
      t.huelle?.material.color.set(c ?? t.farbe);
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
    modell.traverse((o) => {
      if (o.userData.kante || o.userData.ersetzt) o.visible = !an;
      if (o.userData.nurFoto) o.visible = an;
    });
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
  let start = null;
  const treffer = (e) => {
    const r = flaeche.getBoundingClientRect();
    maus.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(maus, kamera);
    return ray.intersectObjects(teile.map((t) => t.mesh))[0]?.object.userData.teil ?? null;
  };
  flaeche.addEventListener('pointerdown', (e) => { gezogen = false; start = [e.clientX, e.clientY]; });
  flaeche.addEventListener('pointermove', (e) => {
    if (e.buttons && start && Math.hypot(e.clientX - start[0], e.clientY - start[1]) > 6) gezogen = true;
    if (e.buttons) return;
    if (e.pointerType !== 'mouse') return;
    const t = treffer(e);
    if (t !== hot) markiere(t?.i ?? null, true);
    flaeche.style.cursor = t ? 'pointer' : '';
    if (!tip) return;
    tip.hidden = !t;
    if (t) {
      tip.innerHTML = `${t.nr ? `<span class="n">${t.nr}</span>` : ''}<b>${esc(t.p.name)}</b><small>${esc(materialVon(t.p)?.name ?? '')} · ${gramm(t.p.mass)}</small>`;
      tip.style.left = `${e.clientX + 14}px`; tip.style.top = `${e.clientY + 14}px`;
    }
  });
  flaeche.addEventListener('pointerleave', () => { markiere(null, true); if (tip) tip.hidden = true; });
  flaeche.addEventListener('click', (e) => { if (!gezogen) waehle(treffer(e)?.i ?? null, true); });
  // Doppeltippen setzt die Ansicht zurück
  flaeche.addEventListener('dblclick', () => steuerung.reset());

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
    drehen: (an) => { steuerung.autoRotate = an; },
    // Standbild für Vorschauen: sofort zeichnen und im selben Schritt auslesen (sonst ist der Puffer leer)
    bild(typ = 'image/webp') { steuerung.update(); if (fotoAn) nach.render(); else renderer.render(scene, kamera); return renderer.domElement.toDataURL(typ, 0.86); },
    nummern: (an) => flaeche.classList.toggle('ohne-nummern', !an),
    get teile() { return teile; },
  };
}
