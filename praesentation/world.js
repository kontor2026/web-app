// Die eine durchgehende Welt der Präsentation und ihre Regie.
// Ort: ein Kreislauf-Ring (der Lebensweg mit sieben Stationen) auf dunklem Studioboden. Am Punkt „Gegenstand“
// stehen die Kommode mit der Schublade und die Restmülltonne, daneben taucht die Scan-Station auf.
// update(k, t) setzt jeden Darsteller absolut aus Schritt k und Zeit t im Schritt. Dadurch sieht jeder Schritt
// gleich aus, egal ob man vorwärts, rückwärts oder per Sprung hinkommt.
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { ladeKategorie, baueModell } from './katalog.js';
import { sm, lerp, clamp01 } from './engine.js';
import { STEPS } from './content.js';
import { START, WERKSTAETTEN } from './werkstaetten.js';

const K = Object.fromEntries(STEPS.map((s, i) => [s.id, i]));
const TAU = Math.PI * 2;
const R = 4.2;                                   // Radius des Rings in m
const v = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const nrm = (a) => v(Math.sin(a), 0, Math.cos(a));
const tng = (a) => v(Math.cos(a), 0, -Math.sin(a));
const onRing = (a, y = 0, r = R) => v(r * Math.sin(a), y, r * Math.cos(a));
const A0 = Math.PI / 2;                          // Winkel von „Abbau“ (rechts, 3 Uhr), dort beginnt der Ring
const angOf = (u) => A0 + u * TAU;                // Ringparameter u (0..1, ab „Abbau“) → Winkel
const uOf = (a) => (((a - A0) % TAU) + TAU) % TAU / TAU;

// Feste Farbbedeutung: Teal = Kreislauf/unsere Lösung, Koralle = Verlust, Gold = Rohstoffe, Violett = KI
export const COL = { teal: '#2fd3b5', coral: '#ff6b57', gold: '#f5b942', violet: '#9a7dff', cobalt: '#5b86ff', slate: '#6b7785' };
const hdr = (hex, k) => new THREE.Color(hex).multiplyScalar(k);

const ANG = { cabinet: -0.13, bin: 0.12, station: 0.48 };

// Symbole wie in der App (packages/site/src/shell.js)
const ICON = {
  abbau: '<path d="M3 19 9 9l4 6 3-4 5 8Z"/>',
  verarbeitung: '<path d="M12 3c3 4 5 6.5 5 10a5 5 0 0 1-10 0c0-3 2-5.5 5-10Z"/><path d="M12 14a2 2 0 0 0 2-2"/>',
  herstellung: '<path d="M3 20V10l5 3v-3l5 3V6h5v14Z"/><path d="M7 17h2M12 17h2"/>',
  gegenstand: '<path d="m12 3 8 4.5v9L12 21l-8-4.5v-9Z"/><path d="m4 7.5 8 4.5 8-4.5M12 12v9"/>',
  nutzung: '<rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 18h2"/>',
  upcycling: '<path d="M14.5 5.5 18.5 9.5 9 19H5v-4Z"/><path d="m12.5 7.5 4 4"/>',
  entsorgung: '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/><path d="M10 11v6M14 11v6"/>',
  verwertung: '<path d="M20 12a8 8 0 1 1-2.3-5.7"/><path d="M20 4v4h-4"/>',
  entdecken: '<circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5"/>',
  verstehen: '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3Z"/>',
  bauen: '<path d="M14.5 5.5 18.5 9.5 9 19H5v-4Z"/><path d="m12.5 7.5 4 4"/>',
  weitergeben: '<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="m8.2 10.8 7.6-3.6M8.2 13.2l7.6 3.6"/>',
};
const LERN = [['entdecken', 'Entdecken'], ['verstehen', 'Verstehen'], ['bauen', 'Bauen'], ['weitergeben', 'Weitergeben']];
const RI = 1.9, LERN_A0 = 0.48;
const LERN_TEXT = ['Was steckt drin?', 'Material, Wert, Herkunft', 'Neues aus Altem', 'Wissen für alle Stationen'];                 // innerer Lernkreis: Radius, Startwinkel (zur Station hin)
// Lebensweg auf dem Ring: Winkel je Station. Nutzung = Kommode, Entsorgung = Tonne, danach die Lücke bis zum Abbau.
const SCHRITTE = [
  ['abbau', 'Abbau', Math.PI / 2], ['verarbeitung', 'Verarbeitung', 2.75], ['herstellung', 'Herstellung', -2.35], ['gegenstand', 'Gegenstand', -1.2],
  ['nutzung', 'Nutzung', -0.13], ['entsorgung', 'Entsorgung', 0.12], ['verwertung', 'Verwertung', Math.PI / 3],
];
const icon = (id) => `<svg viewBox="0 0 24 24" aria-hidden="true">${ICON[id]}</svg>`;

// Stimmung je Schritt: Licht, Umgebung, Nebel, Bloom (wird weich überblendet)
const MOOD = {
  schublade: { env: 0.2, key: 0.22, hemi: 0.1, spot: 1, rim: 0.15, fog: [5, 17], bloom: 0.55 },
  inhalt: { env: 0.85, key: 0.35, hemi: 0.2, spot: 0.4, rim: 0.55, fog: [5, 17], bloom: 0.45 },
  muell: { env: 0.35, key: 0.42, hemi: 0.18, spot: 0.9, rim: 0.3, fog: [6, 22], bloom: 0.5 },
  ring: { env: 0.45, key: 1.15, hemi: 0.32, spot: 0.25, rim: 0.35, fog: [14, 46], bloom: 0.65 },
  station: { env: 0.5, key: 1.25, hemi: 0.35, spot: 0.2, rim: 0.35, fog: [14, 46], bloom: 0.62 },
  energie: { env: 0.4, key: 0.85, hemi: 0.28, spot: 0.1, rim: 0.35, fog: [14, 46], bloom: 0.75 },
  lernen: { env: 0.42, key: 0.9, hemi: 0.3, spot: 0.05, rim: 0.35, fog: [12, 42], bloom: 0.72 },
  monitor: { env: 0.62, key: 1.3, hemi: 0.4, spot: 0.05, rim: 0.4, fog: [10, 40], bloom: 0.32 },
  live: { env: 0.62, key: 1.3, hemi: 0.4, spot: 0.05, rim: 0.4, fog: [10, 40], bloom: 0.32 },
  haube: { env: 0.32, key: 0.62, hemi: 0.22, spot: 0, rim: 0.5, fog: [8, 30], bloom: 0.8 },
  wahl: { env: 0.32, key: 0.62, hemi: 0.22, spot: 0, rim: 0.5, fog: [10, 36], bloom: 0.8 },
  bausatz: { env: 0.65, key: 1.0, hemi: 0.32, spot: 0, rim: 0.45, fog: [7, 26], bloom: 0.5 },
  ueberall: { env: 0.35, key: 0.85, hemi: 0.3, spot: 0, rim: 0.3, fog: [300, 900], bloom: 0.85 },
  projekte: { env: 0.7, key: 1.1, hemi: 0.32, spot: 0, rim: 0.5, fog: [8, 30], bloom: 0.55 },
  gewaehlt: { env: 0.7, key: 1.1, hemi: 0.32, spot: 0, rim: 0.5, fog: [7, 26], bloom: 0.55 },
  ende: { env: 0.35, key: 0.85, hemi: 0.3, spot: 0, rim: 0.3, fog: [300, 900], bloom: 0.85 },
};

// Bis wann (s im Schritt) sich schattenwerfende Dinge bewegen
const SCHATTEN_BIS = { gewaehlt: 1.6, projekte: 4.6, schublade: 2.5, muell: 3.6, ring: 3.5, station: 5.2, lernen: 6.0, haube: 2.6, wahl: 1.5, bausatz: 4.2, monitor: 0.5 };

// ---------- Bausteine ----------------------------------------------------------------------------
function rbox(w, h, d, r, mat, seg = 3) {
  const rr = Math.max(0.0005, Math.min(r, w / 2 - 1e-4, h / 2 - 1e-4, d / 2 - 1e-4));
  const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, seg, rr), mat);
  m.castShadow = m.receiveShadow = true;
  return m;
}
function at(parent, obj, x = 0, y = 0, z = 0) { obj.position.set(x, y, z); parent.add(obj); return obj; }
function cyl(rt, rb, h, mat, seg = 32) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(rt, rb, h, seg), mat);
  m.castShadow = m.receiveShadow = true;
  return m;
}
const basic = (color, extra = {}) => new THREE.MeshBasicMaterial({ color, ...extra });

function glowTexture() {
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const g = c.getContext('2d');
  const grd = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  grd.addColorStop(0, 'rgba(255,255,255,1)');
  grd.addColorStop(0.35, 'rgba(255,255,255,0.35)');
  grd.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = grd;
  g.fillRect(0, 0, 256, 256);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

function floor(scene, renderer) {
  const c = document.createElement('canvas');
  c.width = c.height = 512;
  const g = c.getContext('2d');
  g.fillStyle = '#25292f';
  g.fillRect(0, 0, 512, 512);
  // feines Rauschen gegen Banding, dazu ein ruhiges 1-m-Raster
  const d = g.getImageData(0, 0, 512, 512);
  let s = 7;
  for (let i = 0; i < d.data.length; i += 4) { s = (s * 16807) % 2147483647; const n = (s / 2147483647 - 0.5) * 6; d.data[i] += n; d.data[i + 1] += n; d.data[i + 2] += n; }
  g.putImageData(d, 0, 0);
  g.strokeStyle = 'rgba(255,255,255,0.045)';
  g.lineWidth = 3;
  g.strokeRect(1.5, 1.5, 509, 509);
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(3000, 3000);
  tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
  tex.colorSpace = THREE.SRGBColorSpace;
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(3000, 3000), new THREE.MeshStandardMaterial({ map: tex, roughness: 0.88, metalness: 0 }));
  mesh.rotation.x = -Math.PI / 2;
  mesh.receiveShadow = true;
  scene.add(mesh);
}

// ---------- Kommode mit Schublade ---------------------------------------------------------------
function cabinet() {
  const g = new THREE.Group();
  const W = 0.96, H = 0.78, D = 0.46;
  const wood = new THREE.MeshPhysicalMaterial({ color: '#4a3424', roughness: 0.48, clearcoat: 0.4, clearcoatRoughness: 0.35 });
  const woodIn = new THREE.MeshStandardMaterial({ color: '#6b6258', roughness: 0.8 });
  const metal = new THREE.MeshStandardMaterial({ color: '#7b7f84', metalness: 0.7, roughness: 0.55, envMapIntensity: 0.6 });
  const legM = new THREE.MeshStandardMaterial({ color: '#202326', metalness: 0.6, roughness: 0.4 });
  at(g, rbox(W, 0.025, D, 0.006, wood), 0, H - 0.0125, 0);
  for (const sx of [-1, 1]) at(g, rbox(0.025, H - 0.1, D, 0.005, wood), sx * (W / 2 - 0.0125), 0.1 + (H - 0.1) / 2 - 0.0125, 0);
  at(g, rbox(W - 0.05, 0.02, D - 0.02, 0.003, woodIn), 0, 0.11, 0);
  at(g, rbox(W - 0.05, 0.02, D - 0.02, 0.003, woodIn), 0, 0.58, 0);
  at(g, rbox(W - 0.05, H - 0.12, 0.015, 0.003, woodIn), 0, 0.1 + (H - 0.12) / 2, -D / 2 + 0.008);
  // zwei Türen unten
  for (const sx of [-1, 1]) {
    at(g, rbox(W / 2 - 0.035, 0.44, 0.02, 0.005, wood), sx * (W / 4 - 0.006), 0.345, D / 2 - 0.008);
    at(g, rbox(0.016, 0.12, 0.018, 0.006, metal), sx * 0.04, 0.42, D / 2 + 0.012);
  }
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) at(g, cyl(0.014, 0.01, 0.1, legM, 16), sx * (W / 2 - 0.06), 0.05, sz * (D / 2 - 0.06));

  // Schublade: Front, Boden, Seiten, Rückwand, Griff; fährt nach +z heraus
  const drawer = new THREE.Group();
  g.add(drawer);
  at(drawer, rbox(0.905, 0.15, 0.022, 0.005, wood), 0, 0.6725, D / 2 - 0.011);
  at(drawer, rbox(0.87, 0.012, 0.4, 0.002, woodIn), 0, 0.6, 0.0);
  for (const sx of [-1, 1]) at(drawer, rbox(0.012, 0.11, 0.4, 0.002, woodIn), sx * 0.429, 0.66, 0);
  at(drawer, rbox(0.87, 0.11, 0.012, 0.002, woodIn), 0, 0.66, -0.194);
  at(drawer, rbox(0.26, 0.018, 0.02, 0.008, metal), 0, 0.68, D / 2 + 0.012);
  const bottom = 0.606;
  return { group: g, drawer, bottom };
}

// ---------- Restmülltonne ------------------------------------------------------------------------
function bin() {
  const g = new THREE.Group();
  const body = new THREE.MeshPhysicalMaterial({ color: '#4a4f56', roughness: 0.62, clearcoat: 0.15, side: THREE.DoubleSide });
  const innen = new THREE.MeshStandardMaterial({ color: '#2c3035', roughness: 0.85 });
  const lidM = new THREE.MeshPhysicalMaterial({ color: '#3a3e44', roughness: 0.55, clearcoat: 0.2 });
  const rubber = new THREE.MeshStandardMaterial({ color: '#111315', roughness: 0.9 });
  // Grundriss als abgerundetes Rechteck; Korpus und Rand sind Ringe (außen minus innen), also wirklich hohl
  const rr = (w, d, r) => {
    const sh = new THREE.Shape(), x = -w / 2, y = -d / 2;
    sh.moveTo(x + r, y); sh.lineTo(x + w - r, y); sh.quadraticCurveTo(x + w, y, x + w, y + r); sh.lineTo(x + w, y + d - r);
    sh.quadraticCurveTo(x + w, y + d, x + w - r, y + d); sh.lineTo(x + r, y + d); sh.quadraticCurveTo(x, y + d, x, y + d - r);
    sh.lineTo(x, y + r); sh.quadraticCurveTo(x, y, x + r, y);
    return sh;
  };
  const ring = (w, d, r, wand, h) => {
    const sh = rr(w, d, r);
    sh.holes.push(rr(w - 2 * wand, d - 2 * wand, Math.max(0.005, r - wand)));
    const geo = new THREE.ExtrudeGeometry(sh, { depth: h, bevelEnabled: false, curveSegments: 12 });
    geo.rotateX(-Math.PI / 2);
    return geo;
  };
  const korpus = ring(0.5, 0.56, 0.04, 0.018, 0.86);
  const pos = korpus.attributes.position;
  for (let n = 0; n < pos.count; n++) { const y = pos.getY(n), f = 0.9 + 0.1 * (y / 0.86); pos.setX(n, pos.getX(n) * f); pos.setZ(n, pos.getZ(n) * f); }
  korpus.computeVertexNormals();
  const k = new THREE.Mesh(korpus, body);
  k.castShadow = k.receiveShadow = true;
  at(g, k, 0, 0.07, 0);
  const boden = new THREE.Mesh(new THREE.ShapeGeometry(rr(0.43, 0.49, 0.03)), innen);
  boden.rotation.x = -Math.PI / 2;
  at(g, boden, 0, 0.1, 0);
  boden.receiveShadow = true;
  const rand = new THREE.Mesh(ring(0.54, 0.6, 0.045, 0.04, 0.045), body);
  rand.castShadow = rand.receiveShadow = true;
  at(g, rand, 0, 0.9, 0);
  for (const sx of [-1, 1]) {
    const w = at(g, cyl(0.085, 0.085, 0.05, rubber, 28), sx * 0.24, 0.085, -0.2);
    w.rotation.z = Math.PI / 2;
  }
  const lid = new THREE.Group();
  lid.position.set(0, 0.95, -0.3);
  g.add(lid);
  at(lid, rbox(0.56, 0.04, 0.62, 0.014, lidM), 0, 0.02, 0.31);
  at(lid, rbox(0.2, 0.025, 0.04, 0.01, lidM), 0, 0.03, 0.62);
  return { group: g, lid };
}

// ---------- Scan-Station --------------------------------------------------------------------------
function screenTexture() {
  const c = document.createElement('canvas');
  c.width = 1600; c.height = 900;
  const g = c.getContext('2d');
  g.fillStyle = '#f4f1ea'; g.fillRect(0, 0, 1600, 900);
  g.fillStyle = '#ffffff'; g.fillRect(0, 0, 1600, 86);
  g.fillStyle = '#e4dfd4'; g.fillRect(0, 86, 1600, 2);
  g.strokeStyle = '#1d2227'; g.lineWidth = 5;
  g.beginPath(); g.arc(60, 43, 17, 0, TAU); g.stroke();
  g.fillStyle = '#1d2227'; g.font = '600 30px "IBM Plex Sans", "Segoe UI", sans-serif'; g.fillText('Kreislauf-Station', 92, 53);
  g.fillStyle = '#c9c2b4';
  for (let i = 0; i < 3; i++) g.fillRect(720 + i * 170, 34, 130, 18);
  g.fillStyle = '#ffffff'; g.strokeStyle = '#ddd7cb'; g.lineWidth = 3;
  const card = (x, y, w, h) => { g.fillRect(x, y, w, h); g.strokeRect(x, y, w, h); };
  card(80, 150, 860, 680); card(990, 150, 530, 320); card(990, 510, 530, 320);
  g.strokeStyle = '#1d2227'; g.lineWidth = 4;
  g.strokeRect(350, 330, 320, 340);
  g.strokeStyle = COL.teal; g.lineWidth = 6;
  for (const [x, y, sx, sy] of [[330, 310, 1, 1], [690, 310, -1, 1], [330, 690, 1, -1], [690, 690, -1, -1]]) {
    g.beginPath(); g.moveTo(x, y + 50 * sy); g.lineTo(x, y); g.lineTo(x + 50 * sx, y); g.stroke();
  }
  g.fillStyle = '#d9d3c7';
  for (let i = 0; i < 4; i++) g.fillRect(1030, 200 + i * 60, 420 - i * 60, 22);
  for (let i = 0; i < 4; i++) g.fillRect(1030, 560 + i * 60, 380 - i * 40, 22);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}

function station(ghostable) {
  const g = new THREE.Group();
  const reg = (m) => { ghostable.push(m); return m; };
  const desk = reg(new THREE.MeshPhysicalMaterial({ color: '#8f8a82', roughness: 0.6, clearcoat: 0.1 }));
  const steel = reg(new THREE.MeshStandardMaterial({ color: '#2b3035', metalness: 0.7, roughness: 0.38 }));
  const black = reg(new THREE.MeshPhysicalMaterial({ color: '#16191c', roughness: 0.35, metalness: 0.2, clearcoat: 0.4 }));
  const plateM = reg(new THREE.MeshPhysicalMaterial({ color: '#1b2025', roughness: 0.3, clearcoat: 0.6 }));
  const lens = reg(new THREE.MeshPhysicalMaterial({ color: '#0b0d10', roughness: 0.05, metalness: 0.3, clearcoat: 1 }));
  const edges = [];

  at(g, rbox(1.5, 0.04, 0.72, 0.012, desk), 0, 0.88, 0);
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) at(g, rbox(0.04, 0.86, 0.04, 0.008, steel), sx * 0.7, 0.43, sz * 0.31);
  at(g, rbox(1.38, 0.04, 0.02, 0.006, steel), 0, 0.2, -0.31);
  // Rechner unter dem Tisch (hier kommen später die drei Container heraus)
  const pc = at(g, rbox(0.2, 0.44, 0.44, 0.012, black), 0.48, 0.24, -0.04);
  const led = at(g, new THREE.Mesh(new THREE.BoxGeometry(0.006, 0.3, 0.004), basic(hdr(COL.teal, 2.2))), 0.43, 0.27, 0.184);
  // Monitor 16:9
  const SW = 0.912, SH = SW * 9 / 16;
  const mon = new THREE.Group();
  mon.position.set(0.2, 1.31, -0.2);
  g.add(mon);
  at(mon, rbox(SW + 0.036, SH + 0.036, 0.034, 0.012, black), 0, 0, 0);
  const screenMat = new THREE.MeshBasicMaterial({ map: screenTexture(), color: new THREE.Color(0.0, 0.0, 0.0), toneMapped: false });
  const screen = at(mon, new THREE.Mesh(new THREE.PlaneGeometry(SW, SH), screenMat), 0, 0, 0.0175);
  at(g, rbox(0.05, 0.32, 0.035, 0.01, black), 0.2, 1.05, -0.24);
  at(g, rbox(0.3, 0.014, 0.2, 0.006, black), 0.2, 0.907, -0.2);
  // Scan-Fläche mit leuchtendem Rand, Kameraarm darüber
  const PX = -0.42, PZ = 0.06;
  at(g, rbox(0.4, 0.012, 0.3, 0.004, plateM), PX, 0.906, PZ);
  const rimMat = basic(hdr(COL.teal, 1.6), { transparent: true });
  for (const [w, d, x, z] of [[0.4, 0.006, 0, 0.15], [0.4, 0.006, 0, -0.15], [0.006, 0.3, 0.2, 0], [0.006, 0.3, -0.2, 0]]) {
    at(g, new THREE.Mesh(new THREE.BoxGeometry(w, 0.004, d), rimMat), PX + x, 0.914, PZ + z);
  }
  at(g, cyl(0.016, 0.02, 0.72, steel, 20), PX, 0.9 + 0.36, -0.28);
  at(g, rbox(0.022, 0.022, 0.36, 0.008, steel), PX, 1.61, -0.1);
  const head = at(g, rbox(0.08, 0.045, 0.06, 0.012, black), PX, 1.59, PZ);
  const lensM = at(g, cyl(0.016, 0.016, 0.012, lens, 24), PX, 1.562, PZ);
  // Lichtkegel der Kamera
  const coneMat = new THREE.MeshBasicMaterial({ color: hdr(COL.teal, 0.5), transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide });
  const cone = at(g, new THREE.Mesh(new THREE.ConeGeometry(0.2, 0.64, 48, 1, true), coneMat), PX, 1.24, PZ);
  cone.rotation.y = Math.PI / 4;

  // Kanten für den Röntgenblick (wie die Zeichnung der App)
  const edgeMat = new THREE.LineBasicMaterial({ color: '#9fb6c9', transparent: true, opacity: 0 });
  g.updateMatrixWorld(true);
  g.traverse((o) => {
    if (o.isMesh && o.geometry.type === 'RoundedBoxGeometry') {
      const e = new THREE.LineSegments(new THREE.EdgesGeometry(o.geometry, 35), edgeMat);
      e.position.copy(o.position); e.rotation.copy(o.rotation); e.scale.copy(o.scale);
      edges.push([o.parent, e]);
    }
  });
  for (const [p, e] of edges) p.add(e);

  const plateSlot = new THREE.Object3D();
  plateSlot.position.set(PX, 0.912 + 0.0043, PZ);
  plateSlot.rotation.y = Math.PI / 2 + 0.12;
  g.add(plateSlot);
  return { group: g, screen, screenMat, SW, SH, plateSlot, head, pc, led, cone, coneMat, edgeMat, lensM, edges: edges.map(([, e]) => e) };
}

// ---------- Container (Docker) ---------------------------------------------------------------------
function container(color) {
  const g = new THREE.Group();
  const mat = new THREE.MeshPhysicalMaterial({ color, metalness: 0.45, roughness: 0.42, clearcoat: 0.3, emissive: new THREE.Color(color), emissiveIntensity: 0 });
  // Korpus, Rippen, Stirnseiten und Eckbeschläge als eine Geometrie: ein Draw-Call statt 35
  const teile = [];
  const add = (w, h, d, r, seg, x, y, z) => teile.push(new RoundedBoxGeometry(w, h, d, seg, r).translate(x, y, z));
  add(0.46, 0.2, 0.2, 0.008, 3, 0, 0, 0);
  for (let i = 0; i < 11; i++) for (const sz of [-1, 1]) add(0.012, 0.172, 0.008, 0.003, 1, -0.2 + i * 0.04, 0, sz * 0.101);
  for (const sx of [-1, 1]) add(0.008, 0.19, 0.19, 0.003, 1, sx * 0.231, 0, 0);
  for (const sx of [-1, 1]) for (const sy of [-1, 1]) for (const sz of [-1, 1]) add(0.026, 0.026, 0.026, 0.004, 1, sx * 0.222, sy * 0.088, sz * 0.088);
  const mesh = new THREE.Mesh(mergeGeometries(teile), mat);
  mesh.castShadow = mesh.receiveShadow = true;
  g.add(mesh);
  return { group: g, mat };
}

function tube(points, color, radius = 0.0045) {
  const curve = new THREE.CatmullRomCurve3(points, false, 'centripetal');
  const mat = new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0, depthWrite: false });
  const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, 96, radius, 8, false), mat);
  return { curve, mesh, mat };
}

// ---------- Ring -----------------------------------------------------------------------------------
function ringMaterial(color = COL.teal, pulses = 56) {
  return new THREE.ShaderMaterial({
    fog: true,
    defines: { PULSES: pulses.toFixed(1) },
    uniforms: THREE.UniformsUtils.merge([THREE.UniformsLib.fog, {
      uTime: { value: 0 }, uLit: { value: 0 }, uGap: { value: 0 }, uGold: { value: 0 }, uGapA: { value: -1 }, uGapB: { value: -1 }, uClose: { value: 0 }, uGoldEnd: { value: 0.43 }, uBright: { value: 1 },
      uTeal: { value: hdr(color, 1) }, uCoral: { value: hdr('#6b7682', 1) }, uGoldC: { value: hdr(COL.gold, 1) },
    }]),
    vertexShader: /* glsl */`
      varying vec2 vUv;
      #include <fog_pars_vertex>
      void main() {
        vUv = uv;
        vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
        gl_Position = projectionMatrix * mvPosition;
        #include <fog_vertex>
      }`,
    fragmentShader: /* glsl */`
      uniform float uTime, uLit, uGap, uGold, uGapA, uGapB, uClose, uGoldEnd, uBright;
      uniform vec3 uTeal, uCoral, uGoldC;
      varying vec2 vUv;
      #include <fog_pars_fragment>
      void main() {
        float u = vUv.x;
        if (u > uLit) discard;                                   // noch nicht gezeichnet
        vec3 col;
        // Die eine Lücke (zwischen Gegenstand und Upcycling): gestrichelt koralle, bis die Station sie schließt
        bool offen = u > uGapA && u < uGapB && u > uGapA + (uGapB - uGapA) * uClose;
        if (!offen) {
          float w = fract(u * PULSES - uTime * 0.85);
          float pulse = smoothstep(0.0, 0.06, w) * (1.0 - smoothstep(0.06, 0.45, w));
          float head = (1.0 - smoothstep(0.0, 0.035, uLit - u)) * step(uLit, 0.999);
          col = uTeal * (0.5 + 2.4 * pulse + 2.5 * head);
          // Graue Energie: Abbau bis Herstellung färbt sich gold und fließt schneller in den Gegenstand
          float g = uGold * (1.0 - smoothstep(uGoldEnd - 0.012, uGoldEnd, u));
          float wg = fract(u * 90.0 - uTime * 2.4);
          float pg = smoothstep(0.0, 0.05, wg) * (1.0 - smoothstep(0.05, 0.35, wg));
          col = mix(col, uGoldC * (0.6 + 3.0 * pg), g);
          // Schließen: heller Kopf an der Front, die in die Lücke hineinwächst
          float front = uGapA + (uGapB - uGapA) * uClose;
          col += uTeal * 3.0 * (1.0 - smoothstep(0.0, 0.012, abs(u - front))) * step(0.001, uClose) * step(uClose, 0.999);
        } else {
          if (fract(u * 150.0) > 0.5) discard;
          col = uCoral * (0.25 + 0.35 * uGap);
        }
        col *= uBright;
        gl_FragColor = vec4(col, 1.0);
        #include <fog_fragment>
      }`,
  });
}

// Bildschirminhalt für die Projekt-Handys: Musik-App oder Foto (symmetrisch, damit die Ausrichtung egal ist)
function bildschirm(art) {
  const c = document.createElement('canvas');
  c.width = 300; c.height = 600;
  const g = c.getContext('2d');
  if (art === 'musik') {
    const grd = g.createLinearGradient(0, 0, 0, 600);
    grd.addColorStop(0, '#0d2b27'); grd.addColorStop(1, '#0a1214');
    g.fillStyle = grd; g.fillRect(0, 0, 300, 600);
    g.fillStyle = '#2fd3b5';
    for (let i = 0; i < 13; i++) { const h = 40 + 110 * Math.abs(Math.sin(i * 1.7)); g.fillRect(28 + i * 19, 300 - h / 2, 11, h); }
    g.beginPath(); g.arc(150, 300, 54, 0, Math.PI * 2); g.fillStyle = '#f2f0ea'; g.fill();
    g.beginPath(); g.arc(150, 300, 18, 0, Math.PI * 2); g.fillStyle = '#0d2b27'; g.fill();
  } else {
    const grd = g.createLinearGradient(0, 0, 0, 600);
    grd.addColorStop(0, '#f6b26b'); grd.addColorStop(0.5, '#e07a5f'); grd.addColorStop(1, '#3d405b');
    g.fillStyle = grd; g.fillRect(0, 0, 300, 600);
    g.beginPath(); g.arc(150, 300, 70, 0, Math.PI * 2); g.fillStyle = '#ffe8b0'; g.fill();
    g.fillStyle = 'rgba(255, 240, 210, 0.35)';
    for (let i = 0; i < 6; i++) { g.fillRect(40 + i * 12, 300 + 95 + i * 22, 220 - i * 24, 6); g.fillRect(40 + i * 12, 300 - 101 - i * 22, 220 - i * 24, 6); }
  }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}

// Helles Rückglas und Kupferspule leuchten unter Licht zu stark: dunkler, matter
function dunklesHandy(m) {
  for (const t of m.teile) {
    if (/Rückglas/.test(t.name)) {
      t.mesh.material.color.set('#2a3036'); t.mesh.material.roughness = 0.35; t.mesh.material.envMapIntensity = 0.5;
      t.g.traverse((o) => { if (o !== t.mesh && o.isMesh) { o.material.color.set('#1b1f23'); o.material.envMapIntensity = 0.4; } });
    }
    if (/Ladespule/.test(t.name)) { t.mesh.material.color.multiplyScalar(0.55); t.mesh.material.envMapIntensity = 0.5; }
  }
}

// ---------- Welt bauen -----------------------------------------------------------------------------
export async function buildWorld(engine) {
  const { scene, renderer } = engine;
  const ghostable = [];
  floor(scene, renderer);
  const glowTex = glowTexture();

  const [phoneJ, ...drawerJ] = await Promise.all(['smartphone', 'phone_charger', 'usb_cable', 'earbuds', 'power_bank', 'remote_control', 'wired_earphones', 'computer_mouse', 'laptop', 'webcam', 'shoebox', 'pet_bottle', 'picture_frame']
    .map((id) => ladeKategorie(id)));
  const [chargerJ, , earbudsJ, powerJ, remoteJ, wiredJ, mouseJ, laptopJ, webcamJ, shoeJ, bottleJ, frameJ] = drawerJ;
  const deJ = await (await fetch(new URL('./assets/deutschland.json', import.meta.url))).json();

  // Kommode und Tonne am Punkt „Gegenstand“
  const cab = cabinet();
  cab.group.position.copy(onRing(ANG.cabinet));
  cab.group.rotation.y = ANG.cabinet;
  scene.add(cab.group);
  const drawerItems = [
    [chargerJ, 0.2, 0.1, 0.4], [earbudsJ, 0.36, 0.12, 0.2], [powerJ, -0.2, 0.06, 1.25],
    [remoteJ, -0.36, -0.02, 0.15], [wiredJ, 0.15, -0.13, 0.9], [mouseJ, -0.14, -0.12, -1.2],
  ];
  for (const [j, x, z, ry] of drawerItems) {
    const m = baueModell(j, { glasEinfach: true });
    m.root.position.set(x, cab.bottom, z);
    m.root.rotation.y = ry;
    cab.drawer.add(m.root);
  }
  const drawerSlot = new THREE.Object3D();
  drawerSlot.position.set(0.03, cab.bottom + 0.0043, 0.0);
  drawerSlot.rotation.y = -0.3 + Math.PI / 2;
  cab.drawer.add(drawerSlot);

  const tonne = bin();
  tonne.group.position.copy(onRing(ANG.bin));
  tonne.group.rotation.y = ANG.bin;
  scene.add(tonne.group);

  // Spot über der Kommode (Szene 1)
  const Pc = onRing(ANG.cabinet), nc = nrm(ANG.cabinet), tc = tng(ANG.cabinet);
  const spot = new THREE.SpotLight('#ffe6c8', 10, 0, 0.5, 0.85, 2);
  spot.position.copy(Pc).addScaledVector(nc, 1.0).add(v(0.3, 2.5, 0));
  spot.target.position.copy(Pc).addScaledVector(nc, 0.35).add(v(0.25, 0.5, 0));
  spot.castShadow = true;
  spot.shadow.autoUpdate = false;
  spot.shadow.mapSize.set(1024, 1024);
  spot.shadow.bias = -0.0003;
  spot.shadow.normalBias = 0.01;
  spot.shadow.radius = 4;
  scene.add(spot, spot.target);

  // Handy: das eine Objekt, dem die Präsentation folgt
  const phone = baueModell(phoneJ, { pivot: 'mitte', glasEinfach: true });
  scene.add(phone.root);
  const platine = phone.teil(/Hauptplatine/), soc = phone.teil(/Prozessor/), akku = phone.teil(/Akku/);
  for (const t of [platine, soc, akku, phone.teil(/Speicher/)]) t.mesh.material = t.mesh.material.clone();
  dunklesHandy(phone);

  // Ring, Spur auf dem Boden, Stationen
  const ringMat = ringMaterial();
  const U_ENTSORGUNG = uOf(0.21), U_NUTZUNG = uOf(-0.13);
  ringMat.uniforms.uGapA.value = U_ENTSORGUNG;               // nach der Tonne reißt der Weg ab …
  ringMat.uniforms.uGapB.value = 1;                          // … bis zurück zum Abbau
  ringMat.uniforms.uGoldEnd.value = U_NUTZUNG;
  const ringCurve = new THREE.Curve();
  ringCurve.getPoint = (u, out = new THREE.Vector3()) => { const a = angOf(u); return out.set(R * Math.sin(a), 0.035, R * Math.cos(a)); };
  const ringMesh = new THREE.Mesh(new THREE.TubeGeometry(ringCurve, 900, 0.03, 12, true), ringMat);
  scene.add(ringMesh);
  // Graue Energie als goldene Spirale um den Ring: wächst von Abbau bis zur Tonne, nach der Station weiter bis zum Abbau
  const spiralMat = ringMaterial(COL.gold, 160);
  const spiralCurve = new THREE.Curve();
  const WINDUNGEN = 64, RS = 0.075;
  spiralCurve.getPoint = (u, out = new THREE.Vector3()) => {
    const a = angOf(u), ph = u * WINDUNGEN * TAU;
    const radial = Math.cos(ph) * RS;
    return out.set((R + radial) * Math.sin(a), 0.035 + Math.sin(ph) * RS, (R + radial) * Math.cos(a));
  };
  const spiral = new THREE.Mesh(new THREE.TubeGeometry(spiralCurve, WINDUNGEN * 28, 0.011, 6, false), spiralMat);
  spiral.visible = false;
  scene.add(spiral);
  const trackMat = new THREE.MeshBasicMaterial({ color: '#2f353c', transparent: true, opacity: 0, polygonOffset: true, polygonOffsetFactor: -2, depthWrite: false });
  const track = new THREE.Mesh(new THREE.RingGeometry(R - 0.09, R + 0.09, 360), trackMat);
  track.rotation.x = -Math.PI / 2;
  track.position.y = 0.002;
  scene.add(track);

  const markers = [];
  const pedM = new THREE.MeshStandardMaterial({ color: '#1f2429', roughness: 0.85, metalness: 0.1, envMapIntensity: 0.4 });
  SCHRITTE.forEach(([id, name, a], i) => {
    const u = uOf(a);
    const label = engine.addLabel(`<span class="ico">${icon(id)}</span><span>${name}</span>`, 'station-tag');
    if (id === 'nutzung' || id === 'entsorgung') {
      // Kommode und Tonne sind selbst die Stationen
      const anchor = id === 'nutzung' ? onRing(ANG.cabinet, 1.06).addScaledVector(nc, 0.05) : onRing(ANG.bin, 1.28);
      markers.push({ i, u, id, group: null, label, anchor });
      return;
    }
    const grp = new THREE.Group();
    grp.position.copy(onRing(a));
    const ped = at(grp, cyl(0.28, 0.31, 0.06, pedM, 56), 0, 0.03, 0);
    ped.castShadow = false;
    const rimMat = basic(hdr(COL.teal, 1.4));
    const rim = at(grp, new THREE.Mesh(new THREE.TorusGeometry(0.29, 0.011, 8, 96), rimMat), 0, 0.062, 0);
    rim.rotation.x = Math.PI / 2;
    scene.add(grp);
    markers.push({ i, u, id, group: grp, rimMat, label, anchor: onRing(a, 0.42) });
  });

  // Lernkreislauf in der Ringmitte: Entdecken → Verstehen → Bauen → Weitergeben
  const lernMat = ringMaterial('#7cc8ff', 22);
  const innerCurve = new THREE.Curve();
  innerCurve.getPoint = (u, out = new THREE.Vector3()) => { const a = LERN_A0 + u * TAU; return out.set(RI * Math.sin(a), 0.03, RI * Math.cos(a)); };
  const innerMesh = new THREE.Mesh(new THREE.TubeGeometry(innerCurve, 500, 0.022, 10, true), lernMat);
  scene.add(innerMesh);
  const lernNodes = LERN.map(([id, name], i) => {
    const a = LERN_A0 + (i / LERN.length) * TAU;
    const grp = new THREE.Group();
    grp.position.copy(onRing(a, 0, RI));
    const ped = at(grp, cyl(0.17, 0.19, 0.05, pedM, 48), 0, 0.025, 0);
    ped.castShadow = false;
    const rim = at(grp, new THREE.Mesh(new THREE.TorusGeometry(0.18, 0.009, 8, 72), basic(hdr('#7cc8ff', 1.5))), 0, 0.052, 0);
    rim.rotation.x = Math.PI / 2;
    scene.add(grp);
    const label = engine.addLabel(`<span class="ico">${icon(id)}</span><span><b>${name}</b><small>${LERN_TEXT[i]}</small></span>`, 'station-tag learn');
    label.pos.copy(onRing(a, 0.3, RI));
    return { grp, label, i, rimMat: rim.material };
  });
  // Brücken: Was auf die Station kommt, fließt in den Lernkreis; was man gelernt hat, fließt zurück
  const mkBridge = (a, von, bis) => {
    const m = ringMaterial('#7cc8ff', 10);
    const mesh = new THREE.Mesh(new THREE.TubeGeometry(new THREE.LineCurve3(onRing(a, 0.03, von), onRing(a, 0.03, bis)), 60, 0.017, 8, false), m);
    mesh.visible = false;
    scene.add(mesh);
    return { mesh, m };
  };
  const bridgeIn = mkBridge(LERN_A0 - 0.075, R - 0.4, RI + 0.2);
  const bridgeOut = mkBridge(LERN_A0 + 0.075, RI + 0.2, R - 0.4);

  // Gehirn in der Mitte: Was an den vier Stationen gelernt wird, fließt hier zusammen
  const brainMat = new THREE.MeshStandardMaterial({ color: '#8fc0ec', emissive: new THREE.Color('#2f6fc0'), emissiveIntensity: 0.35, roughness: 0.42, metalness: 0.05, transparent: true, opacity: 0 });
  const brain = new THREE.Group();
  brain.position.set(0, 0.95, 0);
  brain.visible = false;
  scene.add(brain);
  for (const sx of [-1, 1]) {
    const geo = new THREE.SphereGeometry(0.2, 128, 96);
    const p = geo.attributes.position, n = new THREE.Vector3();
    for (let i = 0; i < p.count; i++) {
      n.set(p.getX(i), p.getY(i), p.getZ(i)).normalize();
      // Windungen: zwei verschränkte Wellen auf der Oberfläche
      const falte = Math.sin(n.x * 15 + Math.sin(n.z * 12) * 2.4) * Math.cos(n.y * 13 + Math.sin(n.x * 10) * 2.0);
      const r = 0.2 * (1 + 0.055 * falte);
      p.setXYZ(i, n.x * r * 0.8, n.y * r * 0.82, n.z * r * 1.18);
    }
    geo.computeVertexNormals();
    const half = new THREE.Mesh(geo, brainMat);
    half.position.x = sx * 0.088;
    half.castShadow = true;
    brain.add(half);
  }
  const brainGlowMat = new THREE.SpriteMaterial({ map: glowTex, color: hdr('#7cc8ff', 1.2), transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending });
  const brainGlow = new THREE.Sprite(brainGlowMat);
  brainGlow.scale.setScalar(0.9);
  brain.add(brainGlow);
  const spokes = LERN.map((_, i) => {
    const a = LERN_A0 + (i / LERN.length) * TAU;
    const von = onRing(a, 0.06, RI - 0.18), mitte = onRing(a, 0.5, RI * 0.45);
    const curve = new THREE.CatmullRomCurve3([von, mitte, v(0, 0.9, 0)], false, 'centripetal');
    const m = ringMaterial('#7cc8ff', 7);
    const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, 60, 0.012, 8, false), m);
    mesh.visible = false;
    scene.add(mesh);
    return { mesh, m };
  });
  const brainLabel = engine.addLabel('<b>Wissen</b>', 'brain');
  brainLabel.pos.set(0, 1.9, 0);
  let brainS = 0;
  const auraMat = new THREE.SpriteMaterial({ map: glowTex, color: hdr(COL.gold, 1.6), transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending });
  const aura = new THREE.Sprite(auraMat);
  aura.scale.setScalar(0.7);
  scene.add(aura);
  const co2 = (phoneJ.rohstoffe?.co2_kg ?? 1.9).toLocaleString('de-DE', { maximumFractionDigits: 1 });

  // Scan-Station, taucht in der Lücke auf
  const st = station(ghostable);
  const Ps = onRing(ANG.station), ns = nrm(ANG.station), ts = tng(ANG.station);
  st.group.position.copy(Ps);
  st.group.rotation.y = ANG.station;
  scene.add(st.group);
  const riseGlowMat = new THREE.MeshBasicMaterial({ map: glowTex, color: hdr(COL.teal, 1.2), transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending });
  const riseGlow = new THREE.Mesh(new THREE.PlaneGeometry(2.6, 2.0), riseGlowMat);
  riseGlow.rotation.x = -Math.PI / 2;
  riseGlow.position.copy(Ps).setY(0.01);
  riseGlow.rotation.z = ANG.station;
  scene.add(riseGlow);

  // Unter der Haube: drei Container, Datenwege, Prüftor, Haus, Wolke
  const L = (x, y, z) => v(x, y, z);                           // Station-lokal
  const cFront = container('#5c7c99'), cBack = container('#5b6878'), cInf = container(COL.violet);
  const contDefs = [[cFront, L(-0.56, 2.02, -0.15), 'Frontend'], [cBack, L(0.0, 2.02, -0.15), 'Backend'], [cInf, L(0.58, 2.02, -0.15), 'Inferenz']];
  for (const [c] of contDefs) st.group.add(c.group);
  const pcPos = L(0.48, 0.3, -0.04);
  const P = {
    db: L(0, 2.5, -0.15),
    cam: L(-0.42, 1.6, 0.06), front: L(-0.56, 2.02, -0.15), back: L(0, 2.02, -0.15), inf: L(0.58, 2.02, -0.15),
    screen: L(0.2, 1.31, -0.17), gate: L(0.29, 1.85, -0.07), cloud: L(1.85, 3.05, -0.95), cloudGate: L(1.05, 2.72, -0.6),
  };
  const lineCol = hdr('#8fa3b5', 0.7);
  const paths = {
    A: tube([P.cam, L(-0.5, 1.82, 0.0), P.front], lineCol),
    B: tube([P.front, L(-0.28, 2.15, -0.15), P.back], lineCol),
    C: tube([P.back, L(0.29, 2.17, -0.15), P.inf], lineCol),
    D: tube([P.inf, P.gate, P.back], lineCol),
    E: tube([P.back, L(0.12, 1.72, -0.12), P.screen], lineCol),
    DBU: tube([P.back, L(-0.03, 2.22, -0.1), P.db], lineCol),
    DBD: tube([P.db, L(0.03, 2.22, -0.2), P.back], lineCol),
    CU: tube([P.back, L(0.35, 2.55, -0.35), L(1.1, 3.0, -0.75), P.cloud], lineCol),
    CD: tube([P.cloud, P.cloudGate, L(0.4, 2.3, -0.2), P.back], lineCol),
  };
  for (const p of Object.values(paths)) st.group.add(p.mesh);
  // Datenbank: drei gestapelte Scheiben (201 Gegenstände, Bauteile, Materialien, Herkunft, Entsorgung)
  const dbMat = new THREE.MeshPhysicalMaterial({ color: '#2b5e57', roughness: 0.35, metalness: 0.3, clearcoat: 0.6, emissive: new THREE.Color(COL.teal), emissiveIntensity: 0.05 });
  const db = new THREE.Group();
  db.position.copy(P.db);
  for (let i = 0; i < 3; i++) {
    at(db, cyl(0.16, 0.16, 0.065, dbMat, 64), 0, -0.08 + i * 0.08, 0);
    const r = at(db, new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.004, 6, 96), basic(hdr(COL.teal, 1.3))), 0, -0.08 + i * 0.08 + 0.0325, 0);
    r.rotation.x = Math.PI / 2;
  }
  db.visible = false;
  st.group.add(db);
  const gateMat = basic(hdr(COL.teal, 1.0), { transparent: true, opacity: 0 });
  const mkGate = (pos, along) => {
    const m = new THREE.Mesh(new THREE.TorusGeometry(0.05, 0.006, 10, 64), gateMat);
    m.position.copy(pos);
    m.quaternion.setFromUnitVectors(v(0, 0, 1), along.clone().normalize());
    st.group.add(m);
    return m;
  };
  const gate = mkGate(P.gate, paths.D.curve.getTangentAt(0.5));
  const cloudGateM = mkGate(P.cloudGate, paths.CD.curve.getTangentAt(0.33));
  const packetMat = new THREE.MeshBasicMaterial({ color: new THREE.Color(2, 2, 2), toneMapped: false });
  const packet = new THREE.Mesh(new RoundedBoxGeometry(0.045, 0.045, 0.045, 2, 0.008), packetMat);
  packet.visible = false;
  st.group.add(packet);
  const packetGlow = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, color: 0xffffff, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.55 }));
  packetGlow.scale.setScalar(0.11);
  packet.add(packetGlow);

  // Haus (Werkstatt) als Kantenmodell und Wolke draußen
  const hx0 = -1.0, hx1 = 1.2, hz0 = -0.62, hz1 = 0.62, hy = 2.42, ridge = 2.9;
  const hp = [
    [hx0, 0, hz0], [hx1, 0, hz0], [hx1, 0, hz0], [hx1, 0, hz1], [hx1, 0, hz1], [hx0, 0, hz1], [hx0, 0, hz1], [hx0, 0, hz0],
    [hx0, 0, hz0], [hx0, hy, hz0], [hx1, 0, hz0], [hx1, hy, hz0], [hx1, 0, hz1], [hx1, hy, hz1], [hx0, 0, hz1], [hx0, hy, hz1],
    [hx0, hy, hz0], [hx1, hy, hz0], [hx0, hy, hz1], [hx1, hy, hz1],
    [hx0, hy, hz0], [hx0, ridge, 0], [hx0, hy, hz1], [hx0, ridge, 0], [hx1, hy, hz0], [hx1, ridge, 0], [hx1, hy, hz1], [hx1, ridge, 0],
    [hx0, ridge, 0], [hx1, ridge, 0],
  ].flat();
  const houseGeo = new THREE.BufferGeometry();
  houseGeo.setAttribute('position', new THREE.Float32BufferAttribute(hp, 3));
  const houseMat = new THREE.LineBasicMaterial({ color: hdr('#cfeee6', 1.1), transparent: true, opacity: 0 });
  const house = new THREE.LineSegments(houseGeo, houseMat);
  st.group.add(house);
  const houseFloorMat = new THREE.MeshBasicMaterial({ color: hdr(COL.teal, 0.25), transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending });
  const houseFloor = new THREE.Mesh(new THREE.PlaneGeometry(hx1 - hx0, hz1 - hz0), houseFloorMat);
  houseFloor.rotation.x = -Math.PI / 2;
  houseFloor.position.set((hx0 + hx1) / 2, 0.006, 0);
  st.group.add(houseFloor);
  const cloudMat = new THREE.MeshStandardMaterial({ color: '#e9eef5', roughness: 1, emissive: new THREE.Color('#b9c8de'), emissiveIntensity: 0.1, transparent: true, opacity: 0 });
  const cloud = new THREE.Group();
  cloud.position.copy(P.cloud);
  for (const [x, y, z, r] of [[0, 0, 0, 0.27], [0.3, 0.03, 0, 0.21], [-0.28, -0.03, 0.02, 0.2], [0.1, 0.17, -0.03, 0.2], [-0.12, 0.13, 0.06, 0.17], [0.05, -0.08, 0.13, 0.18]]) {
    at(cloud, new THREE.Mesh(new THREE.SphereGeometry(r, 40, 24), cloudMat), x, y, z);
  }
  st.group.add(cloud);

  // Bausatz in der Ringmitte: Sockel, Laptop, Webcam
  const sockel = new THREE.Group();
  scene.add(sockel);
  const sockelM = new THREE.MeshPhysicalMaterial({ color: '#1d2126', roughness: 0.35, metalness: 0.3, clearcoat: 0.6 });
  at(sockel, cyl(0.52, 0.56, 0.62, sockelM, 72), 0, 0.31, 0);
  const sockelRim = at(sockel, new THREE.Mesh(new THREE.TorusGeometry(0.525, 0.008, 8, 128), basic(hdr(COL.teal, 1.6))), 0, 0.62, 0);
  sockelRim.rotation.x = Math.PI / 2;
  const laptop = baueModell(laptopJ, { glasEinfach: true });
  const webcam = baueModell(webcamJ, { glasEinfach: true });
  scene.add(laptop.root);
  // Deckel als eigene Gruppe, Scharnier hinten auf Höhe 11,2 mm (Modell-mm). Die Webcam klemmt oben am Display.
  const deckel = new THREE.Group();
  deckel.position.set(0, 11.2, 0);
  laptop.inner.add(deckel);
  for (const t of [...laptop.teile]) if (t.p.z >= 11) { t.g.position.y -= 11.2; deckel.add(t.g); }
  const laptopB = Math.max(...laptopJ.parts.map((p) => p.x + p.w)), laptopT = Math.max(...laptopJ.parts.map((p) => p.y + (p.d ?? p.w)));
  deckel.add(webcam.root);
  webcam.root.position.set(laptopB / 2, 14, laptopT + 13);
  webcam.root.rotation.set(Math.PI, 0, 0);

  // Projekte (Szene „Neues bauen“): drei Sockel in der Mitte, Teile fliegen zusammen
  const projM = new THREE.MeshPhysicalMaterial({ color: '#1d2126', roughness: 0.35, metalness: 0.3, clearcoat: 0.6 });
  const quat = (x, y, z, order = 'XYZ') => new THREE.Quaternion().setFromEuler(new THREE.Euler(x, y, z, order));
  const hochkant = quat(Math.PI / 2, 0, 0);                                             // Handy steht, Display nach vorn
  // Weißes Passepartout leuchtet unter dem Bloom zu stark
  const gedaempft = (m) => { for (const t of m.teile) if (/Passepartout|Fotoabzug/.test(t.name)) t.mesh.material.color.multiplyScalar(0.6); return m; };
  const handy = (bild) => {
    const m = baueModell(phoneJ, { pivot: 'mitte', glasEinfach: true });
    dunklesHandy(m);
    if (bild) {
      const d = m.teil(/Display-Einheit/), mat = d.mesh.material;
      const tex = bildschirm(bild);
      tex.repeat.set(1 / d.p.w, 1 / (d.p.d ?? d.p.w));
      Object.assign(mat, { map: tex, emissiveMap: tex, emissiveIntensity: 0.7, roughness: 0.25, metalness: 0, clearcoat: 0.6 });
      mat.emissive.set('#ffffff'); mat.color.set('#ffffff'); mat.needsUpdate = true;
      d.g.traverse((o) => { if (o.isMesh && o !== d.mesh) o.visible = false; });   // dunkle Bildschirm-Markierung des Modells liegt sonst darüber
      m.teil(/Deckglas/)?.g.traverse((o) => { if (o.isMesh && o !== m.teil(/Deckglas/).mesh) o.visible = false; });
      const glas = m.teil(/Deckglas/)?.mesh.material;                       // Spiegelung würde den Bildschirm verdecken
      if (glas) { glas.opacity = 0.06; glas.envMapIntensity = 0.15; }
    }
    return m;
  };
  // Bilderrahmen steht leicht nach hinten geneigt, das Handy liegt hinter dem Glas statt des Fotos
  const qRahmen = quat(0, -0.18, 0).multiply(quat(Math.PI / 2 - 0.22, 0, 0));
  const nRahmen = v(0, 1, 0).applyQuaternion(qRahmen);
  const PROJ = [
    { name: 'Laterne', aus: 'Handy + Wasserflasche', lager: 'PET-Flasche', pos: v(-0.74, 0, 0.32), teile: [
      [handy(), v(0, 0.0043, 0), quat(0, 0.4, Math.PI)],                                   // Display nach unten, Lampe nach oben
      [baueModell(bottleJ, { glasEinfach: true }), v(0, 0.0087, 0), quat(0, 0.3, 0)]], licht: v(0, 0.1, 0) },
    { name: 'Musik-Box', aus: 'Handy + Schuhkarton', lager: 'Schuhkarton', pos: v(0, 0, 0.52), teile: [
      [baueModell(shoeJ, { glasEinfach: true }), v(0, 0, 0), quat(0, 0.15, 0)],
      [handy('musik'), v(0.01, 0.152, 0.01), quat(0, 0.15, 0).multiply(hochkant)]] },
    { name: 'Bilderrahmen', aus: 'Handy + Bilderrahmen', lager: 'Bilderrahmen', pos: v(0.74, 0, 0.32), teile: [
      [gedaempft(baueModell(frameJ, { glasEinfach: true, pivot: 'mitte' })), v(0, 0.118, 0.02), qRahmen],
      [handy('foto'), v(0, 0.118, 0.02).addScaledVector(nRahmen, 0.002), qRahmen]] },
  ];
  const MITTE = v(0, 0, 0.62);
  let wahlProjekt = 1;
  for (const pr of PROJ) {
    pr.sockel = new THREE.Group();
    pr.sockel.position.copy(pr.pos);
    at(pr.sockel, cyl(0.24, 0.27, 0.5, projM, 64), 0, 0.25, 0);
    pr.rimMat = basic(hdr(COL.teal, 1.5));
    const rim = at(pr.sockel, new THREE.Mesh(new THREE.TorusGeometry(0.245, 0.006, 8, 96), pr.rimMat), 0, 0.5, 0);
    rim.rotation.x = Math.PI / 2;
    scene.add(pr.sockel);
    for (const [m] of pr.teile) scene.add(m.root);
    pr.label = engine.addLabel(`<b>${pr.name}</b><span>${pr.aus}</span>`, 'project');
    pr.labelGew = engine.addLabel(`<b>${pr.name}</b><span>Handy + ${pr.lager} aus dem Lager</span>`, 'project big');
    if (pr.licht) {
      pr.glowMat = new THREE.SpriteMaterial({ map: glowTex, color: hdr('#ffd9a0', 2.2), transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending });
      pr.glow = new THREE.Sprite(pr.glowMat);
      pr.glow.scale.setScalar(0.24);
      scene.add(pr.glow);
    }
  }
  const lagerLabel = engine.addLabel('', 'stamp ok');

  // Deutschlandkarte (Szene „Überall“): Hamburg liegt im Ursprung, 1° Breite = 7,7 m
  const KM = 25, cosL = Math.cos(THREE.MathUtils.degToRad(51.2));
  const geo2w = (lon, lat, y = 0) => v((lon - START[0]) * cosL * KM, y, -(lat - START[1]) * KM);
  const karte = new THREE.Group();
  karte.visible = false;
  scene.add(karte);
  const shapes = deJ.ringe.map((r) => new THREE.Shape(r.map(([lon, lat]) => { const p = geo2w(lon, lat); return new THREE.Vector2(p.x, -p.z); })));
  const flaecheGeo = new THREE.ShapeGeometry(shapes);
  flaecheGeo.rotateX(-Math.PI / 2);
  const flaecheMat = new THREE.MeshBasicMaterial({ color: '#1c2833', transparent: true, opacity: 0, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -3 });
  const flaeche = new THREE.Mesh(flaecheGeo, flaecheMat);
  flaeche.position.y = 0.01;
  karte.add(flaeche);
  const randMat = new THREE.MeshBasicMaterial({ color: hdr(COL.teal, 0.9), transparent: true, opacity: 0 });
  for (const r of deJ.ringe) {
    const pts = r.map(([lon, lat]) => geo2w(lon, lat, 0.06));
    const linie = new THREE.Curve();
    linie.getPoint = (u, out = new THREE.Vector3()) => { const f = u * pts.length, i = Math.floor(f) % pts.length; return out.lerpVectors(pts[i], pts[(i + 1) % pts.length], f - Math.floor(f)); };
    karte.add(new THREE.Mesh(new THREE.TubeGeometry(linie, pts.length * 2, 0.32, 5, true), randMat));
  }
  const orte = WERKSTAETTEN.map(([lon, lat, name, zeige]) => {
    const p = geo2w(lon, lat);
    return { p, d: p.length(), name, label: zeige ? engine.addLabel(name, 'city') : null };
  }).sort((a, b) => a.d - b.d);
  const hhLabel = engine.addLabel(`<b>${START[2]}</b> Pilot ab Dezember · 10–15 Schüler`, 'city start');
  const hhLabel2 = engine.addLabel(`<b>${START[2]}</b> ab Februar 2027 · Schützenstraße 62`, 'city start');
  const N = orte.length;
  const miniRing = new THREE.InstancedMesh(new THREE.TorusGeometry(1.8, 0.2, 8, 48), new THREE.MeshBasicMaterial(), N);
  const miniCore = new THREE.InstancedMesh(new THREE.SphereGeometry(0.6, 16, 10), new THREE.MeshBasicMaterial({ toneMapped: false }), N);
  const miniDots = miniCore;
  const minis = orte;
  const mtx = new THREE.Matrix4(), q = new THREE.Quaternion(), sc = new THREE.Vector3(), tmpC = new THREE.Color();
  for (const m of [miniRing, miniCore]) { m.frustumCulled = false; m.visible = false; scene.add(m); }
  miniRing.instanceColor = new THREE.InstancedBufferAttribute(new Float32Array(N * 3), 3);
  miniCore.instanceColor = new THREE.InstancedBufferAttribute(new Float32Array(N * 3), 3);

  // Beschriftungen
  const lab = {
    gold: engine.addLabel('<b>30 mg</b> Gold', 'metal gold left'),
    silber: engine.addLabel('<b>305 mg</b> Silber', 'metal silver right'),
    kobalt: engine.addLabel('<b>6,3 g</b> Kobalt', 'metal cobalt right'),
    quelle: engine.addLabel('Öko-Institut 2012', 'source'),
    front: engine.addLabel('Frontend', 'tech'), back: engine.addLabel('Backend', 'tech'), inf: engine.addLabel('Inferenz', 'tech violet'),
    abgleich: engine.addLabel('Foto-Abgleich', 'event'),
    ki: engine.addLabel('KI erkennt: Smartphone', 'event violet'),
    dbTag: engine.addLabel('Datenbank', 'tech'),
    dbEvent: engine.addLabel('<b>Datenbank:</b> 16 Bauteile, Materialien, Herkunft', 'event gold'),
    pruefung: engine.addLabel('Code prüft', 'event teal'),
    entwurf: engine.addLabel('KI-Entwurf · ungeprüft', 'stamp'),
    frei: engine.addLabel('✓ Werkstatt gibt frei', 'stamp ok'),
    schalter: engine.addLabel('<span data-m="lokal">Lokal</span><span data-m="cloud">Cloud</span>', 'switch'),
    lokal: engine.addLabel('<b>Im Haus</b> Ollama · LM Studio · vLLM', 'mode'),
    cloudL: engine.addLabel('<b>Eigener Zugang</b> Claude · OpenAI', 'mode'),
    open: engine.addLabel('Open Source', 'seal'),
    terminal: engine.addLabel('', 'terminal'),
    katalog: engine.addLabel('Wissen fließt zurück · Katalog wächst', 'event teal flow'),
    energie2: engine.addLabel('<b>Graue Energie</b> bleibt im Kreislauf', 'energy small'),
    energie: engine.addLabel(`<b>Graue Energie</b><span>≈ ${co2} kg CO₂ allein im Material</span><small>landet mit in der Tonne · Idemat 2026</small>`, 'energy'),
  };
  let goldS = 0, auraS = 0, goldEndS = 0, brightS = 1;

  // ---------- Kamerastationen ----------
  const mid = Pc.clone().lerp(onRing(ANG.bin), 0.5);
  const Pshow = Pc.clone().addScaledVector(nc, 0.62).add(v(0, 1.02, 0));
  const screenCenter = new THREE.Vector3();
  st.group.updateMatrixWorld(true);
  st.screen.getWorldPosition(screenCenter);
  const shots = {
    schublade: { pos: Pc.clone().addScaledVector(nc, 0.92).addScaledVector(tc, 0.1).add(v(0, 1.32, 0)), target: Pc.clone().addScaledVector(nc, 0.42).add(v(0, 0.6, 0)) },
    inhalt: { pos: Pshow.clone().addScaledVector(nc, 1.02).addScaledVector(tc, 0.06).add(v(0, 0.26, 0)), target: Pshow.clone().add(v(0, 0.125, 0)) },
    muell: { pos: mid.clone().add(v(0.15, 1.4, 2.75)), target: mid.clone().add(v(0.05, 0.62, 0.2)) },
    ring: { pos: v(-2.6, 10.2, R + 7.6), target: v(0.2, -0.4, 0.4), arc: 1.2 },
    energie: { pos: v(-1.6, 10.6, R + 7.4), target: v(0.3, -0.4, 0.5) },
    station: { pos: v(2.2, 9.4, R + 7.2), target: v(0.6, -0.2, 0.9) },
    lernen: { pos: nrm(LERN_A0).multiplyScalar(R + 6.4).add(v(-1.8, 11.2, 0)), target: nrm(LERN_A0).multiplyScalar(1.4).add(v(-0.3, 0, 0)) },
    projekte: { pos: v(0, 1.32, 2.4), target: v(0, 0.6, 0.38) },
    gewaehlt: { pos: v(0.05, 1.18, 2.05), target: v(0, 0.74, 0.62) },
    monitor: { pos: screenCenter.clone().addScaledVector(ns, 1.42).addScaledVector(ts, -0.26).add(v(0, 0.06, 0)), target: screenCenter.clone().addScaledVector(ts, -0.2).add(v(0, -0.17, 0)), noDrift: true },
    live: null,                                                  // hängt vom Seitenverhältnis ab, siehe shot()
    haube: { pos: Ps.clone().addScaledVector(ns, 3.6).addScaledVector(ts, -1.45).add(v(0, 2.95, 0)), target: Ps.clone().addScaledVector(ts, 0.02).add(v(0, 1.92, 0)) },
    wahl: { pos: Ps.clone().addScaledVector(ns, 5.6).addScaledVector(ts, -1.0).add(v(0, 3.3, 0)), target: Ps.clone().addScaledVector(ts, 0.6).add(v(0, 1.9, 0)) },
    bausatz: { pos: v(0.12, 1.06, 0.92), target: v(0.02, 0.66, 0) },
    ueberall: { pos: v(-22, 285, 232), target: v(-22, 0, 70), arc: 8 },
    ende: { pos: v(-30, 262, 222), target: v(-30, 0, 66) },
  };
  function shot(id) {
    if (id !== 'live') return shots[id];
    // Monitor füllt das Bild genau aus (deckt das ganze Fenster ab)
    const cam = engine.camera, tHalf = Math.tan(THREE.MathUtils.degToRad(cam.fov / 2));
    const d = Math.min(st.SH / (2 * tHalf), st.SW / (2 * tHalf * cam.aspect));
    const n = v(0, 0, 1).transformDirection(st.screen.matrixWorld);
    const c = st.screen.getWorldPosition(new THREE.Vector3());
    return { pos: c.clone().addScaledVector(n, d), target: c, noDrift: true };
  }

  // ---------- Zustand je Schritt ----------
  const mood = { ...MOOD.schublade, fogN: 5, fogF: 17 };
  const tmp = v(), tmp2 = v(), qa = new THREE.Quaternion(), qb = new THREE.Quaternion(), qc = new THREE.Quaternion();
  const showQuat = new THREE.Quaternion().setFromEuler(new THREE.Euler(0, ANG.cabinet + Math.PI / 2, 0.42, 'YZX'));
  const binTop = onRing(ANG.bin, 1.28), binIn = onRing(ANG.bin, 0.55);
  const yAxis = v(0, 1, 0);
  const stepOf = (k) => STEPS[k]?.id;
  let lastK = -1;

  const arc = (out, a, b, h, k) => { out.lerpVectors(a, b, k); out.y += Math.sin(Math.PI * k) * h; return out; };
  const worldPose = (obj, pos, quat) => { obj.updateWorldMatrix(true, false); obj.getWorldPosition(pos); obj.getWorldQuaternion(quat); };

  function placePhone(k, t, time) {
    const r = phone.root;
    let f = 0, visible = true;
    const dPos = tmp, dQuat = qa;
    worldPose(drawerSlot, dPos, dQuat);
    if (k <= K.schublade) {
      r.position.copy(dPos); r.quaternion.copy(dQuat);
    } else if (k === K.inhalt) {
      const lift = sm(t, 0.9, 2.5);
      arc(r.position, dPos, Pshow, 0.22, lift);
      qb.copy(showQuat).premultiply(qc.setFromAxisAngle(yAxis, Math.sin(time * 0.45) * 0.28 * sm(t, 2.2, 4)));
      r.quaternion.slerpQuaternions(dQuat, qb, lift);
      f = sm(t, 2.3, 3.7) * 0.75;
    } else if (k === K.muell) {
      f = (1 - sm(t, 0, 1.0)) * 0.75;
      const fly = sm(t, 1.0, 2.4), drop = sm(t, 2.4, 2.95);
      if (drop <= 0) arc(r.position, Pshow, binTop, 0.3, fly);
      else r.position.lerpVectors(binTop, binIn, drop);
      qb.setFromEuler(new THREE.Euler(0, ANG.bin + 2.4, 0));
      r.quaternion.slerpQuaternions(showQuat, qb, fly);
      visible = drop < 0.98;
    } else if (k === K.ring || k === K.energie) {
      visible = false;
    } else if (k === K.station) {
      worldPose(st.plateSlot, tmp2, qb);
      const jump = sm(t, 3.1, 4.5);
      if (t < 3.1) visible = false;
      else if (jump < 0.35) r.position.lerpVectors(binIn, binTop, jump / 0.35);
      else arc(r.position, binTop, tmp2, 0.35, (jump - 0.35) / 0.65);
      qc.setFromEuler(new THREE.Euler(0, ANG.bin + 2.4, 0));
      r.quaternion.slerpQuaternions(qc, qb, sm(jump, 0.3, 1));
    } else {
      worldPose(st.plateSlot, r.position, r.quaternion);
    }
    phone.explode(f);
    r.visible = visible;
    // Rohstoffe leuchten, solange das Handy zerlegt ist
    const glow = k === K.inhalt ? sm(t, 3.4, 4.2) * (0.75 + 0.25 * Math.sin(time * 2.2)) : 0;
    platine.mesh.material.emissive.set(COL.gold); platine.mesh.material.emissiveIntensity = glow * 0.55;
    soc.mesh.material.emissive.set('#dfe6ee'); soc.mesh.material.emissiveIntensity = glow * 0.6;
    akku.mesh.material.emissive.set(COL.cobalt); akku.mesh.material.emissiveIntensity = glow * 0.65;
    return glow;
  }

  function setGhost(gh) {
    for (const m of ghostable) {
      m.userData.o0 ??= m.opacity;
      if (!m.transparent) { m.transparent = true; m.needsUpdate = true; }
      m.opacity = lerp(1, 0.07, gh);
      m.depthWrite = gh < 0.5;
    }
    st.edgeMat.opacity = gh * 0.55;
    for (const e of st.edges) e.visible = gh > 0.002;
  }

  // Ein Datenpaket entlang einer Folge von Wegen; Pausen = Paket wartet am Ende des vorherigen Wegs
  function runPacket(segs, tc) {
    let pos = null, color = segs[0].c0, seg = null;
    for (const s of segs) {
      if (tc < s.t0) break;
      seg = s;
      if (tc <= s.t1) { const k = sm(tc, s.t0, s.t1); pos = s.p.curve.getPointAt(k, tmp); color = k < 0.5 ? s.c0 : s.c1; break; }
      pos = s.p.curve.getPointAt(1, tmp); color = s.c1;
    }
    return { pos, color, seg };
  }
  const WHITE = new THREE.Color(2.2, 2.2, 2.2), VIOLET = hdr(COL.violet, 2.4), TEAL = hdr(COL.teal, 2.2);
  // Ablauf eines Scans (s im Zyklus): Foto → Frontend → Backend (Foto-Abgleich) → Inferenz (Kategorie) → Prüftor →
  // Backend → Datenbank (was steckt drin) → Backend → Bildschirm (Entwurf, Freigabe)
  const GOLD = hdr(COL.gold, 2.2);
  const SEG_HAUBE = [
    { p: paths.A, t0: 0.0, t1: 1.4, c0: WHITE, c1: WHITE }, { p: paths.B, t0: 1.4, t1: 2.6, c0: WHITE, c1: WHITE },
    { p: paths.C, t0: 3.4, t1: 4.6, c0: WHITE, c1: WHITE }, { p: paths.D, t0: 5.6, t1: 7.0, c0: VIOLET, c1: TEAL },
    { p: paths.DBU, t0: 7.0, t1: 7.7, c0: TEAL, c1: TEAL }, { p: paths.DBD, t0: 8.6, t1: 9.3, c0: GOLD, c1: GOLD },
    { p: paths.E, t0: 9.3, t1: 10.5, c0: GOLD, c1: GOLD },
  ];
  const HAUBE_CYCLE = 12.8;
  const SEG_LOKAL = [
    { p: paths.A, t0: 0.0, t1: 0.9, c0: WHITE, c1: WHITE }, { p: paths.B, t0: 0.9, t1: 1.6, c0: WHITE, c1: WHITE },
    { p: paths.C, t0: 1.6, t1: 2.5, c0: WHITE, c1: WHITE }, { p: paths.D, t0: 3.1, t1: 4.1, c0: VIOLET, c1: TEAL },
    { p: paths.E, t0: 4.1, t1: 5.0, c0: TEAL, c1: TEAL },
  ];
  const SEG_CLOUD = [
    { p: paths.A, t0: 0.0, t1: 0.9, c0: WHITE, c1: WHITE }, { p: paths.B, t0: 0.9, t1: 1.6, c0: WHITE, c1: WHITE },
    { p: paths.CU, t0: 1.6, t1: 2.9, c0: WHITE, c1: WHITE }, { p: paths.CD, t0: 3.4, t1: 4.7, c0: VIOLET, c1: TEAL },
    { p: paths.E, t0: 4.7, t1: 5.6, c0: TEAL, c1: TEAL },
  ];
  const WAHL_CYCLE = 6.4;

  const lpos = (l, local) => st.group.localToWorld(l.pos.copy(local));
  const seen = (x) => x;

  function update(k, t, time, dt) {
    const id = stepOf(k);
    // Schattenkarten nur neu zeichnen, solange sich in diesem Schritt etwas bewegt (spart ein bis zwei Szenendurchläufe)
    const bewegt = k !== lastK || t < (SCHATTEN_BIS[id] ?? 0) || id === 'inhalt' || id === 'ende';
    if (k !== lastK) lastK = k;
    engine.key.shadow.needsUpdate ||= bewegt;

    // Stimmung weich überblenden
    const m = MOOD[id];
    const a = 1 - Math.exp(-dt * 1.7);
    for (const key of ['env', 'key', 'hemi', 'spot', 'rim', 'bloom']) mood[key] = lerp(mood[key], m[key], a);
    mood.fogN = lerp(mood.fogN, m.fog[0], a); mood.fogF = lerp(mood.fogF, m.fog[1], a);
    engine.scene.environmentIntensity = mood.env;
    engine.key.intensity = mood.key * 1.4;
    engine.hemi.intensity = mood.hemi;
    engine.rim.intensity = mood.rim;
    spot.intensity = mood.spot * 8;
    // Lichter nie ein- oder ausschalten (das kompiliert alle Shader neu), nur dimmen. Der Spot-Schatten rendert die
    // Szene ein weiteres Mal und wird deshalb nur in der Schubladen-Szene erneuert, wo er zu sehen ist.
    spot.shadow.needsUpdate ||= bewegt && k <= K.muell;
    engine.bloom.strength = mood.bloom;

    // Schublade
    const open = k === K.schublade ? sm(t, 0.5, 2.3) : k > K.schublade ? 1 : 0;
    cab.drawer.position.z = open * 0.34;

    // Tonne
    let lid = 0;
    if (k === K.muell) lid = sm(t, 0.9, 1.5) - sm(t, 3.0, 3.5);
    if (k === K.station) lid = sm(t, 2.7, 3.2) - sm(t, 4.5, 5.0);
    tonne.lid.rotation.x = -lid * 1.85;

    // Handy
    const glow = placePhone(k, t, time);
    phone.root.updateMatrixWorld(true);
    phone.punkt(platine, lab.gold.pos);
    phone.punkt(soc, lab.silber.pos);
    phone.punkt(akku, lab.kobalt.pos);
    lab.quelle.pos.copy(Pshow).add(v(0, -0.075, 0));
    const metalShow = k === K.inhalt ? sm(t, 3.6, 4.3) : 0;
    lab.gold.show = metalShow;
    lab.silber.show = k === K.inhalt ? sm(t, 3.9, 4.6) : 0;
    lab.kobalt.show = k === K.inhalt ? sm(t, 4.2, 4.9) : 0;
    lab.quelle.show = k === K.inhalt ? sm(t, 4.8, 5.4) * 0.9 : 0;

    // Ring: komplett gezeichnet bis auf eine Lücke zwischen Gegenstand und Upcycling; die Station schließt sie
    let fill = 0, close = 0, reveal = 0;
    if (k === K.ring) { fill = sm(t, 0.9, 4.2); reveal = sm(t, 0.2, 1.4); }
    else if (k === K.energie) { fill = 1; reveal = 1; }
    else if (k === K.station) { fill = 1; close = sm(t, 2.3, 5.0); reveal = 1; }
    else if (k > K.station) { fill = 1; close = 1; reveal = 1; }
    const lit = fill;
    const gap = k >= K.ring ? 1 : 0;
    ringMat.uniforms.uTime.value = time;
    ringMat.uniforms.uLit.value = fill;
    ringMat.uniforms.uGap.value = gap;
    ringMat.uniforms.uClose.value = close;
    ringMesh.visible = fill > 0.0005;
    trackMat.opacity = reveal * 0.85;
    track.visible = reveal > 0.01;
    const ringLabels = k === K.ring || k === K.station || k === K.energie;

    // Graue Energie: Spirale wächst bis zur Tonne (dort geht sie verloren). Mit der Station läuft sie weiter bis zum Abbau.
    const ease = 1 - Math.exp(-dt * 2.2);
    let spir = 0;
    if (k === K.energie) spir = sm(t, 0.5, 4.0) * U_ENTSORGUNG;
    else if (k === K.station) spir = lerp(U_ENTSORGUNG, 1, sm(t, 3.0, 6.2));
    else if (k > K.station) spir = 1;
    spiralMat.uniforms.uTime.value = time;
    spiralMat.uniforms.uLit.value = spir;
    spiral.visible = spir > 0.001;
    brightS = lerp(brightS, k === K.haube || k === K.wahl ? 0.28 : 1, ease * 1.5);
    for (const m of [ringMat, lernMat, bridgeIn.m, bridgeOut.m, spiralMat]) m.uniforms.uBright.value = brightS * (m === spiralMat && k > K.station ? 0.55 : 1);
    // Verlust an der Tonne, später „bleibt im Kreislauf“ hinter der Station
    auraS = lerp(auraS, k === K.energie ? sm(t, 3.4, 4.4) : 0, ease);
    aura.position.copy(onRing(ANG.bin, 1.0));
    auraMat.opacity = auraS * (0.6 + 0.15 * Math.sin(time * 2.4));
    aura.scale.setScalar(0.9 + 0.08 * Math.sin(time * 1.7));
    aura.visible = auraS > 0.01;
    lab.energie.pos.copy(onRing(ANG.bin, 1.35));
    lab.energie.show = auraS;
    lab.energie2.pos.copy(onRing(1.3, 0.3, R + 0.9));
    lab.energie2.show = k === K.station ? sm(t, 6.0, 6.6) : 0;

    // Lernkreislauf: Brücke hinein, innerer Kreis, Brücke zurück
    const lt = k === K.lernen ? t : 99, lernAn = k >= K.lernen;
    const bIn = lernAn ? sm(lt, 0.3, 1.5) : 0, learn = lernAn ? sm(lt, 1.4, 4.8) : 0, bOut = lernAn ? sm(lt, 5.0, 6.2) : 0;
    for (const [b, val] of [[bridgeIn, bIn], [bridgeOut, bOut]]) {
      b.m.uniforms.uTime.value = time;
      b.m.uniforms.uLit.value = val;
      b.mesh.visible = val > 0.001;
    }
    lernMat.uniforms.uTime.value = time;
    lernMat.uniforms.uLit.value = learn;
    innerMesh.visible = learn > 0.001;
    for (const n of lernNodes) {
      const ap = lernAn ? sm(lt, 1.3 + n.i * 0.85, 1.9 + n.i * 0.85) : 0;
      n.grp.visible = ap > 0.01;
      n.grp.scale.set(1, Math.max(0.001, ap), 1);
      const bauenHier = k === K.projekte && n.i === 2;
      n.rimMat.color.copy(hdr('#7cc8ff', bauenHier ? 2.6 + Math.sin(time * 3) * 0.6 : 1.5));
      n.label.show = k === K.lernen ? ap : bauenHier ? sm(t, 0.2, 0.8) : 0;
    }
    // Gehirn: Wissen sammelt sich, sobald der Lernkreis steht
    brainS = lerp(brainS, k === K.lernen ? sm(lt, 3.0, 4.2) : 0, 1 - Math.exp(-dt * 3));
    brain.visible = brainS > 0.005;
    brain.scale.setScalar((0.4 + 0.6 * brainS) * 2.3);
    brainMat.opacity = brainS;
    const brainTr = brainS < 0.98;
    if (brainMat.transparent !== brainTr) { brainMat.transparent = brainTr; brainMat.depthWrite = !brainTr; }
    brainMat.emissiveIntensity = 0.3 + 0.15 * Math.sin(time * 2.2);
    brainGlowMat.opacity = brainS * 0.35;
    brain.rotation.y += dt * 0.25;
    spokes.forEach((sp, i) => {
      const val = k === K.lernen ? sm(lt, 3.3 + i * 0.15, 4.6 + i * 0.15) : 0;
      sp.m.uniforms.uTime.value = time;
      sp.m.uniforms.uLit.value = val;
      sp.mesh.visible = val > 0.001;
    });
    brainLabel.show = k === K.lernen ? sm(lt, 4.2, 4.8) : 0;
    lab.katalog.pos.copy(onRing(LERN_A0 + 0.075, 0.1, RI + 0.55));
    lab.katalog.show = k === K.lernen ? sm(lt, 5.8, 6.4) : 0;
    for (const mk of markers) {
      const appear = k === K.ring ? sm(t, 0.5 + mk.i * 0.3, 1.2 + mk.i * 0.3) : k > K.ring ? 1 : 0;
      const gruen = lit >= mk.u - 0.002 && (mk.u <= U_ENTSORGUNG || mk.u <= U_ENTSORGUNG + (1 - U_ENTSORGUNG) * close);
      if (mk.group) {
        mk.group.visible = appear > 0.01;
        mk.group.scale.set(1, Math.max(0.001, appear), 1);
        mk.rimMat.color.copy(gruen ? hdr(COL.teal, 1.5) : hdr('#59636e', 0.8));
      }
      mk.label.pos.copy(mk.anchor);
      const verdeckt = k === K.energie && mk.id === 'entsorgung';
      mk.label.show = ringLabels && !verdeckt ? appear : 0;

    }

    // Station
    const rise = k < K.station ? 0 : k === K.station ? sm(t, 0.4, 2.5) : 1;
    st.group.visible = rise > 0.001;
    st.group.position.y = -1.75 * (1 - rise);
    riseGlowMat.opacity = k === K.station ? sm(t, 0.2, 0.9) * (1 - sm(t, 2.4, 3.6)) * 0.9 : 0;
    riseGlow.visible = riseGlowMat.opacity > 0.01;
    const screenOn = k < K.station ? 0 : k === K.station ? sm(t, 2.2, 3.0) : 1;
    const gh = k === K.haube ? sm(t, 0.5, 1.6) : k === K.wahl ? 1 : k === K.bausatz ? 1 - sm(t, 0, 0.8) : 0;
    st.screenMat.color.setScalar(screenOn * lerp(0.92, 0.35, gh));
    const scanning = (k === K.station ? sm(t, 4.6, 5.0) : k === K.monitor ? 1 : 0) * (1 - gh);
    st.coneMat.opacity = scanning * (0.06 + 0.02 * Math.sin(time * 3));
    st.cone.visible = st.coneMat.opacity > 0.005;
    setGhost(gh);

    // Container und Datenwege
    const cOut = k === K.haube ? 1 : k === K.wahl ? 1 : k === K.bausatz ? 1 - sm(t, 0, 0.7) : 0;
    contDefs.forEach(([c, pos], i) => {
      const e = k === K.haube ? sm(t, 0.9 + i * 0.25, 2.1 + i * 0.25) : cOut;
      c.group.visible = e > 0.001;
      c.group.position.lerpVectors(pcPos, pos, e);
      c.group.scale.setScalar(lerp(0.2, 1, e));
    });
    const contShow = k === K.haube ? sm(t, 2.0, 2.8) : k === K.wahl ? 1 : 0;
    for (const [l, c] of [[lab.front, cFront], [lab.back, cBack], [lab.inf, cInf]]) {
      lpos(l, c.group.position.clone().add(v(0, -0.17, 0.1)));
      l.show = contShow;
    }
    const wahl = k === K.wahl ? sm(t, 0.3, 1.3) : k === K.bausatz ? 1 - sm(t, 0, 0.6) : 0;
    const tl = t - 1.3;
    const mode = k === K.wahl && tl > 0 && Math.floor(tl / WAHL_CYCLE) % 2 === 1 ? 'cloud' : 'lokal';
    const pathShow = (k === K.haube ? sm(t, 2.2, 3.0) : k === K.wahl ? 1 : 0) * (1 - (k === K.bausatz ? 1 : 0));
    for (const [name, p] of Object.entries(paths)) {
      const cloudPath = name === 'CU' || name === 'CD', localPath = name === 'C' || name === 'D';
      let o = pathShow * 0.55;
      if (k === K.wahl) o = (cloudPath ? (mode === 'cloud' ? 0.75 : 0.12) : localPath ? (mode === 'lokal' ? 0.75 : 0.12) : 0.55) * wahl;
      else if (cloudPath) o = 0;
      p.mat.opacity = o;
      p.mesh.visible = o > 0.005;
    }
    gate.visible = pathShow > 0.01;
    cloudGateM.visible = k === K.wahl && pathShow > 0.01;

    let active = null, tc = 0, segs = null;
    if (k === K.haube && t > 2.6) { tc = (t - 2.6) % HAUBE_CYCLE; segs = SEG_HAUBE; }
    if (k === K.wahl && tl > 0) { tc = tl % WAHL_CYCLE; segs = mode === 'cloud' ? SEG_CLOUD : SEG_LOKAL; }
    if (segs) active = runPacket(segs, tc);
    packet.visible = !!active?.pos;
    if (active?.pos) {
      packet.position.copy(active.pos);
      packetMat.color.copy(active.color);
      packetGlow.material.color.copy(active.color).multiplyScalar(0.4);
    }
    // Leuchten: Container, die gerade arbeiten, und das Prüftor
    const inInf = segs === SEG_HAUBE ? (tc > 4.6 && tc < 5.6) : segs === SEG_LOKAL ? (tc > 2.5 && tc < 3.1) : false;
    const inCloud = segs === SEG_CLOUD && tc > 2.9 && tc < 3.4;
    const inBack = segs === SEG_HAUBE && tc > 2.6 && tc < 3.4;
    const inDb = segs === SEG_HAUBE && tc > 7.7 && tc < 8.6;
    dbMat.emissiveIntensity = lerp(dbMat.emissiveIntensity, inDb ? 0.9 : 0.05, 1 - Math.exp(-dt * 8));
    const dbAn = k === K.haube ? sm(t, 1.6, 2.6) : k === K.wahl ? 1 : k === K.bausatz ? 1 - sm(t, 0, 0.7) : 0;
    db.visible = dbAn > 0.01;
    db.scale.setScalar(Math.max(0.001, dbAn));
    lpos(lab.dbTag, P.db.clone().add(v(0.34, -0.03, 0.12)));
    lab.dbTag.show = k === K.haube ? sm(t, 2.4, 3.0) : k === K.wahl ? 1 : 0;
    cInf.mat.emissiveIntensity = lerp(cInf.mat.emissiveIntensity, inInf ? 0.9 : (mode === 'cloud' && k === K.wahl ? 0 : 0.08), 1 - Math.exp(-dt * 10));
    cBack.mat.emissiveIntensity = lerp(cBack.mat.emissiveIntensity, inBack ? 0.7 : 0.04, 1 - Math.exp(-dt * 10));
    cFront.mat.emissiveIntensity = 0.04;
    const nearGate = active?.pos ? Math.max(0, 1 - active.pos.distanceTo(P.gate) / 0.12, 1 - active.pos.distanceTo(P.cloudGate) / 0.14) : 0;
    gateMat.color.copy(hdr(COL.teal, 0.7 + nearGate * 3));
    gateMat.opacity = pathShow;
    cloudMat.opacity = wahl;
    cloud.visible = wahl > 0.01;
    cloudMat.emissiveIntensity = lerp(cloudMat.emissiveIntensity, inCloud ? 1.2 : mode === 'cloud' ? 0.35 : 0.05, 1 - Math.exp(-dt * 8));
    houseMat.opacity = wahl * 0.7;
    house.visible = wahl > 0.01;
    houseFloorMat.opacity = wahl * (mode === 'lokal' ? 0.5 : 0.2);
    houseFloor.visible = wahl > 0.01;

    // Ereignis-Fähnchen im Ablauf
    const win = (a, b) => (segs === SEG_HAUBE ? sm(tc, a, a + 0.25) * (1 - sm(tc, b - 0.25, b)) : 0);
    lpos(lab.abgleich, P.back.clone().add(v(-0.2, 0.18, 0.05))); lab.abgleich.show = win(2.6, 3.5);
    lpos(lab.ki, P.inf.clone().add(v(0, 0.2, 0.05))); lab.ki.show = win(4.6, 5.7);
    lpos(lab.pruefung, P.gate.clone().add(v(0.02, -0.08, 0.05))); lab.pruefung.show = win(6.0, 7.1);
    lpos(lab.dbEvent, P.db.clone().add(v(0, 0.17, 0.05))); lab.dbEvent.show = win(7.6, 8.8);
    lpos(lab.entwurf, P.screen.clone().add(v(-0.05, 0.08, 0.05))); lab.entwurf.show = win(10.5, 11.6);
    lpos(lab.frei, P.screen.clone().add(v(-0.05, 0.08, 0.05))); lab.frei.show = win(11.6, 12.7);
    lpos(lab.schalter, v(0.1, ridge + 0.32, 0.0)); lab.schalter.show = wahl * (k === K.wahl ? 1 : 0);
    lab.schalter.el.dataset.mode = mode;
    lpos(lab.lokal, v(hx0 - 0.25, 1.1, hz1));                    // außen neben dem Haus
    lab.lokal.show = k === K.wahl ? wahl * (mode === 'lokal' ? sm(tc, 0, 0.4) * (1 - sm(tc, WAHL_CYCLE - 0.4, WAHL_CYCLE)) : 0) : 0;
    lpos(lab.cloudL, P.cloud.clone().add(v(0, 0.42, 0)));
    lab.cloudL.show = k === K.wahl ? wahl * (mode === 'cloud' ? sm(tc, 0, 0.4) * (1 - sm(tc, WAHL_CYCLE - 0.4, WAHL_CYCLE)) : 0) : 0;
    lpos(lab.open, v(hx0 + 0.05, ridge + 0.08, 0.0)); lab.open.show = k === K.wahl ? sm(t, 1.4, 2.2) : 0;

    // Bausatz
    const ped = k < K.bausatz ? 0 : k === K.bausatz ? sm(t, 0.2, 1.3) : 1;
    sockel.visible = ped > 0.001;
    sockel.position.y = -0.64 * (1 - ped);
    const land = k < K.bausatz ? 0 : k === K.bausatz ? sm(t, 1.0, 2.4) : 1;
    const auf = k < K.bausatz ? 0 : k === K.bausatz ? sm(t, 2.3, 3.5) : 1;
    const cam = k < K.bausatz ? 0 : k === K.bausatz ? sm(t, 3.3, 4.0) : 1;
    laptop.root.visible = land > 0.001;
    laptop.root.position.set(0, 0.62 + (1 - land) * 1.2, (1 - land) * 0.25);
    laptop.root.rotation.set((1 - land) * 0.5, -0.25 + (1 - land) * 0.9, 0);
    deckel.rotation.x = -1.85 * auf;
    webcam.root.visible = cam > 0.001;
    webcam.root.scale.setScalar(1000 * Math.max(0.001, cam));
    const cmd = 'docker compose up';
    const typed = k === K.bausatz ? Math.floor(clamp01((t - 4.2) / 1.0) * cmd.length) : cmd.length;
    const okLines = ['frontend', 'backend', 'inferenz'].map((n, i) => (k !== K.bausatz || t > 5.4 + i * 0.25 ? `<div class="ok">✓ ${n}</div>` : '')).join('');
    engine.setLabelHtml(lab.terminal, `<div class="cmd"><i>$</i> ${cmd.slice(0, typed)}<span class="caret"></span></div>${okLines}`);
    lab.terminal.pos.set(0.2, 0.84, 0.02);
    lab.terminal.show = k === K.bausatz ? sm(t, 3.9, 4.3) : 0;

    // Projekte: Sockel steigen auf, Teile fliegen zusammen. Im nächsten Schritt rückt das gewählte in die Mitte.
    PROJ.forEach((pr, i) => {
      const gew = k === K.gewaehlt && i === wahlProjekt;
      const weg = k === K.gewaehlt && !gew ? sm(t, 0, 0.9) : 0;
      const rise = k === K.projekte ? sm(t, 0.2 + i * 0.25, 1.1 + i * 0.25) : k === K.gewaehlt ? 1 - weg : 0;
      const move = gew ? sm(t, 0.2, 1.4) : 0;
      const hebe = k === K.projekte && i === wahlProjekt ? sm(t, 1.0, 1.6) * 0.06 : k === K.gewaehlt && gew ? 0.06 : 0;
      const bx = lerp(pr.pos.x, MITTE.x, move), bz = lerp(pr.pos.z, MITTE.z, move), by = -0.52 * (1 - rise) + hebe;
      pr.sockel.visible = rise > 0.001;
      pr.sockel.position.set(bx, by, bz);
      const vor = (k === K.projekte || k === K.gewaehlt) && i === wahlProjekt;
      pr.rimMat.color.copy(hdr(COL.teal, vor ? 2.6 + 0.6 * Math.sin(time * 3) : 0.9));
      pr.label.el.classList.toggle('gewaehlt', vor);
      let gelandet = 1;
      pr.teile.forEach(([m, p, qEnd], j) => {
        const land = k === K.projekte ? sm(t, 1.1 + i * 0.6 + j * 0.4, 2.2 + i * 0.6 + j * 0.4) : 1;
        gelandet = Math.min(gelandet, land);
        m.root.visible = rise > 0.001 && land > 0.001;
        if (!m.root.visible) return;
        tmp.set(bx + p.x, by + 0.5 + p.y, bz + p.z);
        tmp2.copy(tmp).add(v(0, 0.9, -0.2));
        m.root.position.lerpVectors(tmp2, tmp, land);
        m.qStart ??= qEnd.clone().premultiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(0.7, 1.4, 0.2)));
        m.root.quaternion.slerpQuaternions(m.qStart, qEnd, land);
      });
      if (pr.glow) {
        pr.glow.position.set(bx + pr.licht.x, by + 0.5 + pr.licht.y, bz + pr.licht.z);
        pr.glowMat.opacity = (rise > 0.001 ? gelandet : 0) * (0.55 + 0.08 * Math.sin(time * 5.3) * Math.sin(time * 3.1));
        pr.glow.visible = pr.glowMat.opacity > 0.01;
      }
      pr.label.pos.set(bx, 0.9 + by, bz);
      pr.label.show = k === K.projekte ? sm(t, 2.2 + i * 0.6, 2.8 + i * 0.6) : 0;
      pr.labelGew.pos.set(bx, 1.0 + by, bz);
      pr.labelGew.show = gew ? sm(t, 1.2, 1.8) : 0;
      if (gew) {
        engine.setLabelHtml(lagerLabel, `✓ ${pr.lager} aus dem Lager`);
        lagerLabel.pos.set(bx + 0.3, 0.62 + by, bz + 0.1);
      }
    });
    lagerLabel.show = k === K.gewaehlt ? sm(t, 1.9, 2.4) : 0;

    // Deutschlandkarte mit Werkstätten: Welle von Hamburg aus
    const karteAn = k === K.ueberall ? sm(t, 0.4, 1.8) : k === K.ende ? 1 : 0;
    karte.visible = karteAn > 0.002;
    flaecheMat.opacity = karteAn * 0.9;
    randMat.opacity = karteAn;
    hhLabel.pos.set(0, 1.5, -R - 1);
    hhLabel.show = k === K.ueberall ? sm(t, 1.4, 2.0) : 0;
    hhLabel2.pos.copy(hhLabel.pos);
    hhLabel2.show = k === K.ende ? sm(t, 0.3, 0.9) : 0;
    const showMini = k === K.ueberall || k === K.ende;
    for (const mm of [miniRing, miniCore]) mm.visible = showMini;
    if (showMini) {
      qc.setFromEuler(new THREE.Euler(Math.PI / 2, 0, 0));
      for (let i = 0; i < N; i++) {
        const mi = minis[i];
        const lit2 = k === K.ende ? 1 : sm(t, 1.6 + mi.d / 60, 2.2 + mi.d / 60);
        const s = Math.max(0.001, lit2);
        mtx.compose(sc.copy(mi.p).setY(0.08), qc, tmp.setScalar(s));
        miniRing.setMatrixAt(i, mtx);
        miniRing.setColorAt(i, tmpC.copy(hdr(COL.teal, 0.4 + 1.5 * lit2)));
        mtx.compose(sc.copy(mi.p).setY(0.6), q.identity(), tmp.setScalar(s));
        miniCore.setMatrixAt(i, mtx);
        miniCore.setColorAt(i, tmpC.setRGB(1, 0.97, 0.9).multiplyScalar(0.4 + 1.6 * lit2));
        if (mi.label) { mi.label.pos.copy(mi.p).setY(1.6); mi.label.show = k === K.ueberall ? sm(t, 2.2 + mi.d / 60, 2.8 + mi.d / 60) : k === K.ende ? 1 : 0; }
      }
      for (const mm of [miniRing, miniCore]) { mm.instanceMatrix.needsUpdate = true; mm.instanceColor.needsUpdate = true; }
    } else {
      for (const mi of minis) if (mi.label) mi.label.show = 0;
    }
    return { glow };
  }

  // Monitor-Ecken in Weltkoordinaten (für das iframe über dem Bildschirm)
  const corners = [v(-st.SW / 2, st.SH / 2, 0), v(st.SW / 2, st.SH / 2, 0), v(st.SW / 2, -st.SH / 2, 0), v(-st.SW / 2, -st.SH / 2, 0)];
  const cornerW = corners.map(() => v());
  function screenCorners() {
    st.screen.updateWorldMatrix(true, false);
    corners.forEach((c, i) => st.screen.localToWorld(cornerW[i].copy(c)));
    return cornerW;
  }
  const screenNormal = () => v(0, 0, 1).transformDirection(st.screen.matrixWorld);
  const screenPos = () => st.screen.getWorldPosition(v());

  // Für das Vorkompilieren: alles kurz sichtbar machen
  function allVisible(fn) {
    const hidden = [];
    scene.traverse((o) => { if (!o.visible) { hidden.push(o); o.visible = true; } });
    const r = fn();
    for (const o of hidden) o.visible = false;
    return r;
  }

  // Klick auf eine Säule: welches Projekt?
  const ray = new THREE.Raycaster();
  function pickProjekt(ndc) {
    ray.setFromCamera(ndc, engine.camera);
    const hit = ray.intersectObjects(PROJ.flatMap((pr) => [pr.sockel, ...pr.teile.map(([m]) => m.root)]), true)[0];
    if (!hit) return -1;
    return PROJ.findIndex((pr) => [pr.sockel, ...pr.teile.map(([m]) => m.root)].some((o) => { let x = hit.object; while (x) { if (x === o) return true; x = x.parent; } return false; }));
  }
  const setProjekt = (i) => { wahlProjekt = i; };

  return { update, shot, pickProjekt, setProjekt, screenCorners, screenNormal, screenPos, allVisible, seen };
}
