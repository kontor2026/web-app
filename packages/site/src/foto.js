// Fotorealistische Darstellung der Kategorie-Modelle: physikalische Materialien je Katalog-Material,
// abgerundete Kanten, Umgebungslicht aus einem Studio-Raum, weiche Schatten auf dem Boden.
// Die Geometrie bleibt die der Station (extrudierte Grundrisse), nur Licht und Oberflächen sind echt.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
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
const METALL = { m: 1, r: 0.3, tx: 'gebuerstet', b: 0.02 };
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
    transparent: opacity < 0.98, opacity, envMapIntensity: e.m ? 1.9 : 1,
    polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1,
  });
  if (e.holz) { mat.map = farbTextur('holz', farbe); mat.color.set(0xffffff); }
  if (e.tx) { mat.bumpMap = textur(e.tx); mat.bumpScale = e.b ?? 0.1; if (e.m) mat.roughnessMap = textur(e.tx); }
  // Glas und klare Kunststoffe: echte Lichtbrechung statt bloßer Transparenz
  if (durchsichtig && (e.glas || ['pet', 'ps', 'folien', 'pcabs', 'ldpe'].includes(p.materials?.[0]?.[0]))) {
    Object.assign(mat, { transmission: 1 - opacity * 0.6, opacity: 1, ior: 1.5, thickness: 1.5, roughness: e.r ?? 0.05,
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
  geo.computeVertexNormals();
  return geo;
}

export function koerperGeometrie(t) {
  if (t.wand > 0) return hohlGeometrie(t);
  const w = t.w, d = t.d ?? t.w, h = t.h;
  const b = Math.min(1.2, 0.12 * Math.min(w, d), 0.3 * h);
  const rund = t.shape === 'cyl';
  let geo;
  if (b < 0.12) {
    geo = new THREE.ExtrudeGeometry(grundriss(0, 0, w, d, t.r ?? 0, rund), { depth: h, bevelEnabled: false, curveSegments: 32 });
    geo.rotateX(Math.PI / 2);
    geo.translate(0, h, 0);
  } else {
    geo = new THREE.ExtrudeGeometry(grundriss(b, b, w - 2 * b, d - 2 * b, Math.max(0, (t.r ?? 0) - b), rund), {
      depth: h - 2 * b, bevelEnabled: true, bevelThickness: b, bevelSize: b, bevelOffset: 0, bevelSegments: 3, curveSegments: 32,
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
  sonne.shadow.mapSize.set(1024, 1024);
  sonne.shadow.bias = -0.0004;
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
  ao.blendIntensity = 0.85;
  composer.addPass(ao);
  composer.addPass(new OutputPass());
  return {
    setSize(w, h) { composer.setPixelRatio(renderer.getPixelRatio()); composer.setSize(w, h); },
    // Radius in mm passend zur Modellgröße
    radius(r) { ao.updateGtaoMaterial({ radius: Math.max(4, r * 0.06), distanceExponent: 1.5, thickness: Math.max(2, r * 0.03), scale: 1, samples: 16 }); },
    render() { composer.render(); },
  };
}
