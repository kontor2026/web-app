// Fotorealistische Darstellung der Kategorie-Modelle: physikalische Materialien je Katalog-Material,
// abgerundete Kanten, Umgebungslicht aus einem Studio-Raum, weiche Schatten auf dem Boden.
// Die Geometrie bleibt die der Station (extrudierte Grundrisse), nur Licht und Oberflächen sind echt.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { mergeGeometries, mergeVertices } from 'three/addons/utils/BufferGeometryUtils.js';
import { MATERIALS } from '../../../js/data/catalog.js';

// ---------- Oberflächen-Texturen (prozedural, einmal erzeugt, in mm gekachelt) ----------
function leinwand(n, mal) {
  const c = document.createElement('canvas');
  c.width = c.height = n;
  const g = c.getContext('2d');
  mal(g, n);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.colorSpace = THREE.NoColorSpace;
  return t;
}
const zufall = (s) => () => ((s = (s * 16807) % 2147483647) / 2147483647);
function rauschen(g, n, staerke, seed = 7, basis = 128) {
  const r = zufall(seed), d = g.createImageData(n, n);
  for (let i = 0; i < n * n; i++) { const v = basis + (r() - 0.5) * staerke; d.data.set([v, v, v, 255], i * 4); }
  g.putImageData(d, 0, 0);
}
const TEX = {};
function textur(art) {
  if (TEX[art]) return TEX[art];
  let t, mm;
  if (art === 'gebuerstet') {            // gebürstetes Metall: feine Längsriefen
    t = leinwand(256, (g, n) => { const r = zufall(3); rauschen(g, n, 30, 3);
      for (let i = 0; i < 900; i++) { g.fillStyle = `rgba(${r() > 0.5 ? 255 : 0},0,0,0)`; g.globalAlpha = 0.08 + r() * 0.1;
        g.fillStyle = r() > 0.5 ? '#fff' : '#000'; g.fillRect(0, r() * n, n, 0.6 + r()); } });
    mm = 40;
  } else if (art === 'gewebe') {         // Stoff: Leinwandbindung
    t = leinwand(64, (g, n) => { g.fillStyle = '#808080'; g.fillRect(0, 0, n, n);
      for (let i = 0; i < n; i += 4) for (let j = 0; j < n; j += 4) { const a = ((i + j) / 4) % 2;
        g.fillStyle = a ? '#b0b0b0' : '#505050'; g.fillRect(i, j, 4, 2); g.fillStyle = a ? '#505050' : '#b0b0b0'; g.fillRect(i, j + 2, 4, 2); } });
    mm = 6;
  } else if (art === 'holz') {           // Holzmaserung: gewellte Jahresringe
    t = leinwand(256, (g, n) => { const r = zufall(11); const d = g.createImageData(n, n);
      for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) {
        const w = Math.sin((y / n) * 6 * Math.PI + Math.sin((x / n) * 2 * Math.PI) * 1.4) * 0.5 + 0.5;
        const v = 110 + w * 90 + (r() - 0.5) * 18; d.data.set([v, v, v, 255], (y * n + x) * 4); }
      g.putImageData(d, 0, 0); });
    mm = 120;
  } else if (art === 'papier') {         // Papier, Pappe: feines Faserrauschen
    t = leinwand(128, (g, n) => rauschen(g, n, 60, 5));
    mm = 25;
  } else {                               // Kunststoff: ganz leichte Struktur
    t = leinwand(128, (g, n) => rauschen(g, n, 26, 9));
    mm = 30;
  }
  t.repeat.set(1 / mm, 1 / mm);
  return (TEX[art] = t);
}

// ---------- Materialeigenschaften je Katalog-Material ----------
// r = Rauheit, m = metallisch, cc = Klarlack, sh = Glanz bei Stoffen, tx = Textur, b = Relieftiefe
const METALL = { m: 0.85, r: 0.34, tx: 'gebuerstet', b: 0.02 };
const EIGEN = {
  alu: { ...METALL, r: 0.34 }, stahl: { ...METALL, r: 0.26 }, weissblech: { ...METALL, r: 0.22 },
  kupfer: { ...METALL, r: 0.3 }, messing: { ...METALL, r: 0.28 }, nickel: { ...METALL, r: 0.25 },
  zink: { ...METALL, r: 0.4 }, lot: { ...METALL, r: 0.45 }, kontakte: { m: 1, r: 0.2 },
  nichrom: { ...METALL, r: 0.5 }, bimetall: { ...METALL, r: 0.35 },
  glas: { glas: true, r: 0.04 }, displayglas: { glas: true, r: 0.03 }, behaelterglas: { glas: true, r: 0.06 },
  keramik: { r: 0.3, cc: 0.8 }, emaille: { r: 0.2, cc: 1 }, glimmer: { r: 0.4 },
  folien: { r: 0.15, cc: 0.6 }, pet: { r: 0.18, cc: 0.6 }, ps: { r: 0.22, cc: 0.5 }, pcabs: { r: 0.32, cc: 0.35, tx: 'kunststoff', b: 0.05 },
  hdpe: { r: 0.5, tx: 'kunststoff', b: 0.05 }, ldpe: { r: 0.45 }, pp: { r: 0.42, tx: 'kunststoff', b: 0.05 },
  pvc: { r: 0.4, cc: 0.2 }, tpe: { r: 0.8 }, tpu: { r: 0.55 }, gummi: { r: 0.9, tx: 'kunststoff', b: 0.1 },
  schaum: { r: 0.95, tx: 'papier', b: 0.3 }, wachs: { r: 0.55, cc: 0.2 }, nylon: { r: 0.6 }, ptfe: { r: 0.45 },
  phenolharz: { r: 0.35, cc: 0.4 }, kunstleder: { r: 0.6, sh: 0.3 }, verbundfolie: { r: 0.3, cc: 0.4 },
  klebstoff: { r: 0.5 }, tinte: { r: 0.3, cc: 0.5 }, polyester: { r: 0.9, sh: 0.6, tx: 'gewebe', b: 0.25 },
  fr4: { r: 0.35, cc: 0.7 }, chip: { r: 0.45 }, led: { r: 0.2, cc: 0.6 },
  ndfeb: { m: 0.7, r: 0.3 }, ferrit: { m: 0.2, r: 0.7 },
  papier: { r: 0.92, tx: 'papier', b: 0.2 }, druck: { r: 0.6, cc: 0.15, tx: 'papier', b: 0.1 }, verbund: { r: 0.7, tx: 'papier', b: 0.15 },
  holz: { r: 0.62, tx: 'holz', b: 0.25, holz: true }, kork: { r: 0.95, tx: 'papier', b: 0.5 },
  textil: { r: 1, sh: 0.8, tx: 'gewebe', b: 0.3 }, baumwolle: { r: 1, sh: 0.8, tx: 'gewebe', b: 0.3 },
  wolle: { r: 1, sh: 1, tx: 'gewebe', b: 0.45 }, leder: { r: 0.55, sh: 0.3, tx: 'papier', b: 0.2 }, organisch: { r: 0.9 },
};
const KLASSE = { metall: METALL, glas: { r: 0.3, cc: 0.5 }, kunststoff: { r: 0.45 }, elektronik: { r: 0.4, cc: 0.5 },
  akku: { r: 0.5 }, magnet: { m: 0.6, r: 0.35 }, papier: { r: 0.85, tx: 'papier', b: 0.2 } };

export function eigenschaften(p) {
  const id = p.materials?.[0]?.[0];
  return EIGEN[id] ?? KLASSE[MATERIALS[id]?.cls] ?? { r: 0.5 };
}

export function stoff(p, farbe, opacity) {
  const e = eigenschaften(p);
  const durchsichtig = opacity < 0.98;
  const mat = new THREE.MeshPhysicalMaterial({
    color: farbe, metalness: e.m ?? 0, roughness: e.r, clearcoat: e.cc ?? 0, clearcoatRoughness: 0.15,
    sheen: e.sh ?? 0, sheenRoughness: 0.6, sheenColor: farbe.clone().lerp(new THREE.Color(1, 1, 1), 0.4),
    transparent: opacity < 0.98, opacity, envMapIntensity: e.m ? 2.4 : 1,
    polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1,
  });
  // Dunkle Metalle (eloxiert, brüniert) spiegeln sonst fast nur Schwarz: Mindesthelligkeit
  if (e.m) { const hsl = {}; mat.color.getHSL(hsl); if (hsl.l < 0.22) mat.color.setHSL(hsl.h, hsl.s, 0.22); }
  if (e.holz) { mat.map = farbTextur('holz', farbe); mat.color.set(0xffffff); }
  if (e.tx) { mat.bumpMap = textur(e.tx); mat.bumpScale = e.b ?? 0.1; if (e.m) mat.roughnessMap = textur(e.tx); }
  // Glas und klare Kunststoffe: echte Lichtbrechung statt bloßer Transparenz
  if (durchsichtig && (e.glas || ['pet', 'ps', 'folien', 'pcabs', 'ldpe', 'pp', 'hdpe', 'pvc'].includes(p.materials?.[0]?.[0]))) {
    Object.assign(mat, { transmission: 1 - opacity * 0.6, opacity: 1, ior: 1.5, thickness: 1.5, roughness: e.glas ? e.r : Math.min(e.r ?? 0.1, 0.08),
      specularIntensity: 1, attenuationColor: farbe, attenuationDistance: 60 });
    mat.userData.glas = true;
    mat.transparent = false;
  }
  mat.userData.o0 = mat.opacity;
  return mat;
}

const FARBTEX = {};
function farbTextur(art, farbe) {
  const k = `${art}${farbe.getHexString()}`;
  if (FARBTEX[k]) return FARBTEX[k];
  const graustufen = textur(art).image;
  const c = document.createElement('canvas');
  c.width = c.height = graustufen.width;
  const g = c.getContext('2d');
  g.drawImage(graustufen, 0, 0);
  g.globalCompositeOperation = 'multiply';
  g.fillStyle = `#${farbe.getHexString(THREE.SRGBColorSpace)}`;
  g.fillRect(0, 0, c.width, c.height);
  g.globalCompositeOperation = 'source-over';
  g.globalAlpha = 0.55;
  g.fillStyle = `#${farbe.getHexString(THREE.SRGBColorSpace)}`;
  g.fillRect(0, 0, c.width, c.height);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.colorSpace = THREE.SRGBColorSpace;
  t.repeat.copy(textur(art).repeat);
  return (FARBTEX[k] = t);
}

// ---------- Geometrie mit gerundeten Kanten, gleiche Außenmaße wie die Zeichnung ----------
function grundriss(x0, y0, w, d, r, rund) {
  const s = new THREE.Shape();
  if (rund) { s.absellipse(x0 + w / 2, y0 + d / 2, w / 2, d / 2, 0, Math.PI * 2, false, 0); return s; }
  r = Math.max(0, Math.min(r, w / 2, d / 2));
  s.moveTo(x0 + r, y0); s.lineTo(x0 + w - r, y0); s.quadraticCurveTo(x0 + w, y0, x0 + w, y0 + r);
  s.lineTo(x0 + w, y0 + d - r); s.quadraticCurveTo(x0 + w, y0 + d, x0 + w - r, y0 + d);
  s.lineTo(x0 + r, y0 + d); s.quadraticCurveTo(x0, y0 + d, x0, y0 + d - r); s.lineTo(x0, y0 + r); s.quadraticCurveTo(x0, y0, x0 + r, y0);
  return s;
}
// Hohles Teil (Feld wand, mm): Wände oben offen, Boden mit Dicke boden (Standard = wand, 0 = unten offen)
function hohlGeometrie(t) {
  const w = t.w, d = t.d ?? t.w, h = t.h, rund = t.shape === 'cyl', r = t.r ?? 0;
  const wa = Math.min(t.wand, w / 2 - 0.1, d / 2 - 0.1), bo = Math.min(t.boden ?? wa, h - 0.1);
  const aussen = grundriss(0, 0, w, d, r, rund);
  aussen.holes.push(grundriss(wa, wa, w - 2 * wa, d - 2 * wa, Math.max(0, r - wa), rund));
  const teile = [];
  const wand = new THREE.ExtrudeGeometry(aussen, { depth: h - bo, bevelEnabled: false, curveSegments: 48 });
  wand.rotateX(Math.PI / 2); wand.translate(0, h, 0);
  teile.push(wand);
  if (bo > 0) {
    const boden = new THREE.ExtrudeGeometry(grundriss(0, 0, w, d, r, rund), { depth: bo, bevelEnabled: false, curveSegments: 48 });
    boden.rotateX(Math.PI / 2); boden.translate(0, bo, 0);
    teile.push(boden);
  }
  const geo = mergeGeometries(teile);
  if (t.offen === 'unten') { geo.rotateX(Math.PI); geo.translate(0, h, d); }   // Schale nach unten offen (Helm, Kappe, Deckel)
  geo.computeVertexNormals();
  return geo;
}

const WEICH = new Set(['textil', 'baumwolle', 'wolle', 'polyester', 'leder', 'kunstleder', 'gummi', 'schaum', 'tpe', 'tpu']);
const SCHARF = new Set(['metall', 'glas', 'elektronik', 'magnet']);
export function haerte(t) {
  const id = t.materials?.[0]?.[0], cls = MATERIALS[id]?.cls;
  const w = t.w, d = t.d ?? t.w;
  // Kabel und Schnüre: dünn und lang, rund wie ein Schlauch
  if (Math.max(w, d) > 6 * Math.min(w, d) && t.h <= Math.min(w, d) * 1.6 && ['pvc', 'tpe', 'gummi', 'kupfer', 'nylon', 'polyester'].includes(id)) return 'weich';
  if (WEICH.has(id)) return 'weich';
  if (SCHARF.has(cls) || id === 'papier' || id === 'druck' || id === 'verbund') return 'scharf';
  return 'mittel';
}

// Echte Formen nur für die Foto-Ansicht (Feld form), füllen den Quader des Teils aus:
// kugel (Ball, Knauf), torus (Kabelrolle, Reifen, Ring), liegend_x / liegend_y (Kabel, Rolle, Griff, Rad, Stift)
function formGeometrie(t) {
  const w = t.w, d = t.d ?? t.w, h = t.h, weich = haerte(t) === 'weich';
  let geo;
  if (t.form === 'kugel') {
    geo = new THREE.SphereGeometry(0.5, 64, 40);
    geo.scale(w, h, d);
  } else if (t.form === 'torus') {
    const rohr = Math.min(h / 2, Math.min(w, d) / 4), R = Math.min(w, d) / 2 - rohr;
    geo = new THREE.TorusGeometry(R, rohr, 32, 96);
    geo.rotateX(Math.PI / 2);
    geo.scale((w / 2) / (R + rohr), (h / 2) / rohr, (d / 2) / (R + rohr));
  } else {
    const entlangX = t.form === 'liegend_x', L = entlangX ? w : d, q1 = entlangX ? d : w;
    // Kreisquerschnitt (Breite quer × Höhe); weiche Teile mit halbrunden Enden wie ein Kabel
    geo = weich ? new THREE.CapsuleGeometry(0.5, Math.max(0.01, L / Math.min(q1, h) - 1), 16, 48) : new THREE.CylinderGeometry(0.5, 0.5, L / Math.min(q1, h), 64, 1);
    if (entlangX) geo.rotateZ(Math.PI / 2); else geo.rotateX(Math.PI / 2);
    geo.computeBoundingBox();
    const b = geo.boundingBox, f = [w / (b.max.x - b.min.x), h / (b.max.y - b.min.y), d / (b.max.z - b.min.z)];
    geo.scale(...f);
  }
  geo.translate(w / 2, h / 2, d / 2);
  return geo;
}

export function koerperGeometrie(t) {
  if (t.form) return formGeometrie(t);
  if (t.wand > 0) return hohlGeometrie(t);
  const w = t.w, d = t.d ?? t.w, h = t.h;
  const k = haerte(t), m = Math.min(w, d);
  // Kantenradius nach Material: weich (Stoff, Leder, Gummi, Kabel) wie ein Kissen, Kunststoff mittel, Metall/Glas scharf
  const b = k === 'weich' ? Math.min(0.45 * m, 0.48 * h, 30) : k === 'mittel' ? Math.min(0.18 * m, 0.3 * h, 6) : Math.min(0.08 * m, 0.25 * h, 2);
  const rund = t.shape === 'cyl';
  let geo;
  if (b < 0.12) {
    geo = new THREE.ExtrudeGeometry(grundriss(0, 0, w, d, t.r ?? 0, rund), { depth: h, bevelEnabled: false, curveSegments: 32 });
    geo.rotateX(Math.PI / 2);
    geo.translate(0, h, 0);
  } else {
    const ri = k === 'weich' ? Math.max((t.r ?? 0) - b, 0.25 * Math.min(w - 2 * b, d - 2 * b)) : Math.max(0, (t.r ?? 0) - b);
    geo = new THREE.ExtrudeGeometry(grundriss(b, b, w - 2 * b, d - 2 * b, ri, rund), {
      depth: Math.max(0.01, h - 2 * b), bevelEnabled: true, bevelThickness: b, bevelSize: b, bevelOffset: 0,
      bevelSegments: k === 'weich' ? 8 : 4, curveSegments: 32,
    });
    geo.rotateX(Math.PI / 2);
    geo.translate(0, h - b, 0);
  }
  geo.computeVertexNormals();
  return geo;
}

// ---------- Licht, Umgebung, Schatten ----------
export function studio(renderer, scene) {
  renderer.toneMapping = THREE.NeutralToneMapping;
  renderer.toneMappingExposure = 0.92;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFShadowMap;
  const pmrem = new THREE.PMREMGenerator(renderer);
  const umgebung = pmrem.fromScene(new RoomEnvironment(), 0.03).texture;
  const hemi = new THREE.HemisphereLight(0xffffff, 0x6f6a60, 0.25);
  const sonne = new THREE.DirectionalLight(0xfff6ea, 2.2);
  sonne.castShadow = true;
  sonne.shadow.mapSize.set(2048, 2048);
  sonne.shadow.bias = -0.0004;
  sonne.shadow.radius = 4;                                  // weiche Kanten, flimmern beim Drehen weniger
  const fuell = new THREE.DirectionalLight(0xe8f0ff, 0.35);
  const boden = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.ShadowMaterial({ opacity: 0.22 }));
  boden.rotation.x = -Math.PI / 2;
  boden.receiveShadow = true;
  scene.add(hemi, sonne, sonne.target, fuell, boden);

  return {
    an(foto) {
      scene.environment = foto ? umgebung : null;
      scene.environmentIntensity = 0.7;
      hemi.intensity = foto ? 0.25 : 1.6;
      sonne.intensity = foto ? 2.6 : 1.2;
      sonne.castShadow = foto;
      fuell.visible = foto;
      boden.visible = foto;
    },
    // Licht und Schattenkamera an die Modellgröße anpassen (Einheit mm)
    passe(box) {
      const m = box.getCenter(new THREE.Vector3()), r = box.getBoundingSphere(new THREE.Sphere()).radius;
      sonne.position.copy(m).add(new THREE.Vector3(0.45, 1, 0.6).normalize().multiplyScalar(r * 3));
      sonne.target.position.copy(m);
      const c = sonne.shadow.camera;
      c.left = c.bottom = -r * 1.4; c.right = c.top = r * 1.4; c.near = r * 0.5; c.far = r * 6;
      c.updateProjectionMatrix();
      sonne.shadow.normalBias = r * 0.004;
      fuell.position.copy(m).add(new THREE.Vector3(-1, 0.4, -0.3).multiplyScalar(r * 3));
      boden.scale.set(r * 10, r * 10, 1);
      boden.position.set(m.x, box.min.y - 0.3, m.z);
    },
  };
}

// ---------- Umgebungsverdeckung (Kontaktschatten zwischen Teilen) ----------
export function nachbearbeitung(renderer, scene, kamera) {
  const composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, kamera));
  const ao = new GTAOPass(scene, kamera, 1, 1);
  ao.blendIntensity = 0.7;
  composer.addPass(ao);
  composer.addPass(new OutputPass());
  return {
    setSize(w, h) { composer.setPixelRatio(renderer.getPixelRatio()); composer.setSize(w, h); },
    // Radius in mm passend zur Modellgröße
    radius(r) { ao.updateGtaoMaterial({ radius: r * 0.05, distanceExponent: 1.5, thickness: r * 0.025, scale: 1, samples: 24 }); },
    render() { composer.render(); },
  };
}


// ---------- Rundung: übereinander gestapelte Scheiben zu einer glatten Hülle verbinden ----------
// Die Modelle bauen runde Formen (Flaschenschulter, Schuh, Ball, Kegel) aus waagrechten Scheiben. In der Foto-Ansicht
// wird so ein Stapel durch eine glatte Fläche ersetzt: Umrisse der Scheiben werden gleich abgetastet und senkrecht
// mit Catmull-Rom interpoliert. Die Scheiben bleiben für Zeichnung, Klicks und Prüfung erhalten.
const N_UM = 72;
function umriss(t) {           // N_UM Punkte auf dem Umriss, nach Winkel um die Mitte (für konvexe Grundrisse)
  const w = t.w, d = t.d ?? t.w, cx = t.x + w / 2, cy = t.y + d / 2;
  const pts = [];
  for (let i = 0; i < N_UM; i++) {
    const a = (i / N_UM) * Math.PI * 2, c = Math.cos(a), s = Math.sin(a);
    if (t.shape === 'cyl') { pts.push([cx + c * w / 2, cy + s * d / 2]); continue; }
    // Strahl aus der Mitte gegen ein abgerundetes Rechteck (Superellipse als gute Näherung)
    const r = Math.max(0, Math.min(t.r ?? 0, w / 2, d / 2)), n = 2 + 18 * (1 - r / Math.max(1e-6, Math.min(w, d) / 2)) ** 2;
    const k = 1 / ((Math.abs(c) / (w / 2)) ** n + (Math.abs(s) / (d / 2)) ** n) ** (1 / n);
    pts.push([cx + c * k, cy + s * k]);
  }
  return pts;
}
const cr = (p0, p1, p2, p3, u) => 0.5 * (2 * p1 + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (-p0 + 3 * p1 - 3 * p2 + p3) * u * u * u);

function huelle(stapel) {      // stapel: Teile von unten nach oben
  // Ebenen an Unter- und Oberkante jeder Scheibe; an Fugen wird der Mittelwert genommen. So bleiben gerade Wände gerade
  // (kein Fass-Bauch) und Stufen werden zu weichen Übergängen.
  const roh = [];
  for (const t of stapel) { const u = umriss(t); roh.push({ z: t.z, pts: u }, { z: t.z + t.h, pts: u }); }
  const ebenen = [];
  for (const e of roh) {
    const l = ebenen.at(-1);
    if (l && Math.abs(l.z - e.z) < 0.05) l.pts = l.pts.map((p, j) => [(p[0] + e.pts[j][0]) / 2, (p[1] + e.pts[j][1]) / 2]);
    else ebenen.push({ z: e.z, pts: e.pts.map((p) => [...p]) });
  }
  const fein = [];
  const SCHRITT = 5;
  for (let i = 0; i < ebenen.length - 1; i++) {
    const a = ebenen[Math.max(0, i - 1)], b = ebenen[i], c = ebenen[i + 1], e = ebenen[Math.min(ebenen.length - 1, i + 2)];
    for (let k = 0; k < SCHRITT; k++) {
      const u = k / SCHRITT;
      fein.push({ z: b.z + (c.z - b.z) * u, pts: b.pts.map((_, j) => [0, 1].map((q) => cr(a.pts[j][q], b.pts[j][q], c.pts[j][q], e.pts[j][q], u))) });
    }
  }
  fein.push(ebenen.at(-1));
  const pos = [];
  const v = (x, y, z) => pos.push(x, z, y);              // Station x, y, z → three X, Z(=Tiefe), Y(=Höhe)
  const mantel = (F, innen) => {
    for (let i = 0; i < F.length - 1; i++) {
      const A = F[i], B = F[i + 1];
      for (let j = 0; j < N_UM; j++) {
        const j2 = (j + 1) % N_UM;
        const q = [[A.pts[j], A.z], [B.pts[j], B.z], [A.pts[j2], A.z], [A.pts[j2], A.z], [B.pts[j], B.z], [B.pts[j2], B.z]];
        if (innen) [q[1], q[2]] = [q[2], q[1]], [q[4], q[5]] = [q[5], q[4]];
        for (const [p, z] of q) v(p[0], p[1], z);
      }
    }
  };
  const deckel = (E, oben) => {
    const mx = E.pts.reduce((s, p) => s + p[0], 0) / N_UM, my = E.pts.reduce((s, p) => s + p[1], 0) / N_UM;
    for (let j = 0; j < N_UM; j++) {
      const j2 = (j + 1) % N_UM;
      if (oben) { v(mx, my, E.z); v(E.pts[j2][0], E.pts[j2][1], E.z); v(E.pts[j][0], E.pts[j][1], E.z); }
      else { v(mx, my, E.z); v(E.pts[j][0], E.pts[j][1], E.z); v(E.pts[j2][0], E.pts[j2][1], E.z); }
    }
  };
  mantel(fein, false);
  const wand = stapel[0].wand;
  if (wand > 0) {
    // Hohl: Innenwand um wand nach innen versetzt, oben ein Rand, unten Boden (Dicke boden, Standard = wand, 0 = offen)
    const ein = (E) => {
      const mx = E.pts.reduce((s, p) => s + p[0], 0) / N_UM, my = E.pts.reduce((s, p) => s + p[1], 0) / N_UM;
      return E.pts.map(([x, y]) => { const dx = x - mx, dy = y - my, l = Math.hypot(dx, dy) || 1, k = Math.max(0, l - wand) / l; return [mx + dx * k, my + dy * k]; });
    };
    const boden = stapel[0].boden ?? wand, z0 = fein[0].z + boden;
    const innen = fein.filter((E) => E.z >= z0 - 1e-6).map((E) => ({ z: E.z, pts: ein(E) }));
    if (boden > 0 && innen[0].z > z0 + 1e-6) innen.unshift({ z: z0, pts: ein(fein.find((E) => E.z >= z0) ?? fein[0]) });
    mantel(innen, true);
    const O = fein.at(-1), I = innen.at(-1);
    for (let j = 0; j < N_UM; j++) {                      // Rand oben
      const j2 = (j + 1) % N_UM;
      v(O.pts[j][0], O.pts[j][1], O.z); v(O.pts[j2][0], O.pts[j2][1], O.z); v(I.pts[j][0], I.pts[j][1], O.z);
      v(I.pts[j][0], I.pts[j][1], O.z); v(O.pts[j2][0], O.pts[j2][1], O.z); v(I.pts[j2][0], I.pts[j2][1], O.z);
    }
    if (boden > 0) { deckel(fein[0], false); deckel(innen[0], true); }
  } else {
    deckel(fein[0], false); deckel(fein.at(-1), true);
  }
  let geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  geo = mergeVertices(geo, 0.01);
  geo.computeVertexNormals();
  return geo;
}

// Stapel finden: gleiche Explosion, gleiche Farbe und Oberfläche, lückenlos übereinander, Grundrisse überlappen
export function stapelSuchen(parts, farbeVon) {
  const schluessel = (p) => [JSON.stringify(p.explode ?? [0, 0, 0]), farbeVon(p), p.materials?.[0]?.[0], p.opacity ?? 1, p.wand ?? 0, p.form ?? ''].join('|');
  const gruppen = new Map();
  parts.forEach((p, i) => { const k = schluessel(p); if (!gruppen.has(k)) gruppen.set(k, []); gruppen.get(k).push(i); });
  const stapel = [];
  for (const [k, idx] of gruppen) {
    if (idx.length < 3 || !k.endsWith('|')) continue;          // Teile mit eigener form nicht verbinden
    const frei = new Set(idx);
    for (const start of [...idx].sort((a, b) => parts[a].z - parts[b].z)) {
      if (!frei.has(start)) continue;
      const kette = [start]; frei.delete(start);
      for (;;) {
        const o = parts[kette.at(-1)], oben = o.z + o.h;
        const ox = o.x + o.w / 2, oy = o.y + (o.d ?? o.w) / 2;
        const naechste = [...frei].find((j) => {
          const q = parts[j], qx = q.x + q.w / 2, qy = q.y + (q.d ?? q.w) / 2;
          return Math.abs(q.z - oben) < 0.6 && Math.abs(qx - ox) < Math.min(o.w, q.w) * 0.35 && Math.abs(qy - oy) < Math.min(o.d ?? o.w, q.d ?? q.w) * 0.35;
        });
        if (naechste == null) break;
        kette.push(naechste); frei.delete(naechste);
      }
      if (kette.length >= 3) stapel.push(kette);
    }
  }
  return stapel;
}

export function huellenMesh(stapelTeile, material) {
  const mesh = new THREE.Mesh(huelle(stapelTeile), material);
  mesh.castShadow = mesh.receiveShadow = true;
  return mesh;
}

// ---------- Flache Etiketten an runden Körpern als gebogener Streifen ----------
// p: dünnes, senkrechtes Etikett (Quader), q: runder Körper, an dem es anliegt. Ergebnis in Teil-Koordinaten von p.
export function etikettGeometrie(p, q) {
  const qd = q.d ?? q.w, rx = q.w / 2, ry = qd / 2, cx = q.x + rx, cy = q.y + ry;
  const pd = p.d ?? p.w, px = p.x + p.w / 2, py = p.y + pd / 2;
  const mitte = Math.atan2((py - cy) / ry, (px - cx) / rx);         // Richtung, in der das Etikett liegt
  const breite = Math.max(p.w, pd), t = Math.max(0.3, Math.min(p.w, pd));
  const span = Math.min(Math.PI * 0.95, breite / ((rx + ry) / 2));
  const s = new THREE.Shape(), N = 48;
  for (let i = 0; i <= N; i++) { const a = mitte - span / 2 + (span * i) / N; const pt = [cx + Math.cos(a) * (rx + t), cy + Math.sin(a) * (ry + t)]; i ? s.lineTo(...pt) : s.moveTo(...pt); }
  for (let i = N; i >= 0; i--) { const a = mitte - span / 2 + (span * i) / N; s.lineTo(cx + Math.cos(a) * (rx + 0.05), cy + Math.sin(a) * (ry + 0.05)); }
  const geo = new THREE.ExtrudeGeometry(s, { depth: p.h, bevelEnabled: false, curveSegments: 4 });
  geo.rotateX(Math.PI / 2);
  geo.translate(-p.x, p.h, -p.y);                                   // Gruppe von p sitzt bei (p.x, p.z, p.y)
  geo.computeVertexNormals();
  return geo;
}
