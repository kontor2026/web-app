// Renderer, Licht, Nachbearbeitung (MSAA + Bloom), Kamera-Regie und Beschriftungen.
// Ziel: ruckelfrei. Deshalb: Pixelbudget, das sich selbst nachregelt, keine Objekte pro Frame neu anlegen,
// Kamerafahrten mit Smootherstep (Geschwindigkeit und Beschleunigung an beiden Enden null).
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

export const clamp01 = (x) => Math.min(1, Math.max(0, x));
export const smoother = (x) => { x = clamp01(x); return x * x * x * (x * (x * 6 - 15) + 10); };
/** Weicher Übergang von 0 auf 1 zwischen Zeitpunkt a und b. */
export const sm = (t, a, b) => smoother((t - a) / (b - a));
export const lerp = (a, b, k) => a + (b - a) * k;

const PIXEL_BUDGET = 6.2e6;          // höchstens so viele Pixel pro Frame (bei 1080p: Faktor ≈ 1,8)
const BG = new THREE.Color('#0a0c0f');

export function createEngine(canvas) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: 'high-performance', stencil: false });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.NeutralToneMapping;
  renderer.toneMappingExposure = 1;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFShadowMap;      // günstiger als PCFSoft, weich genug mit radius

  const scene = new THREE.Scene();
  scene.background = BG;
  scene.fog = new THREE.Fog(BG, 14, 55);
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.5;

  const camera = new THREE.PerspectiveCamera(32, innerWidth / innerHeight, 0.01, 1500);

  // Licht: ein Schlüssellicht mit feiner Schattenkarte, ein Spot für die Schublade, schwaches Himmelslicht.
  const hemi = new THREE.HemisphereLight('#dfe8ff', '#1a1612', 0.35);
  const key = new THREE.DirectionalLight('#fff3e2', 1.4);
  key.position.set(7, 13, 10);
  key.target.position.set(0.6, 0, 2.2);
  key.castShadow = true;
  key.shadow.autoUpdate = false;     // world.js fordert neue Schatten nur an, wenn sich etwas bewegt
  key.shadow.mapSize.set(2048, 2048);
  Object.assign(key.shadow.camera, { left: -8, right: 8, top: 8, bottom: -8, near: 2, far: 40 });
  key.shadow.bias = -0.0002;
  key.shadow.normalBias = 0.012;
  key.shadow.radius = 3;
  const rim = new THREE.DirectionalLight('#9fc4ff', 0.35);
  rim.position.set(-8, 6, -9);
  scene.add(hemi, key, key.target, rim);

  // Nachbearbeitung: Szene in ein HalfFloat-Ziel mit 4× MSAA, darauf Bloom, dann Tonemapping
  const target = new THREE.WebGLRenderTarget(1, 1, { type: THREE.HalfFloatType, samples: 4 });
  const composer = new EffectComposer(renderer, target);
  composer.addPass(new RenderPass(scene, camera));
  const bloom = new UnrealBloomPass(new THREE.Vector2(1, 1), 0.5, 0.55, 1.0);
  composer.addPass(bloom);
  composer.addPass(new OutputPass());

  // ---- Größe und Pixelbudget ----------------------------------------------------------------
  let quality = 1;
  function resize() {
    const w = innerWidth, h = innerHeight;
    const ratio = Math.min(devicePixelRatio || 1, 2, Math.sqrt(PIXEL_BUDGET / (w * h))) * quality;
    renderer.setPixelRatio(ratio);
    renderer.setSize(w, h, false);
    composer.setPixelRatio(ratio);
    composer.setSize(w, h);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  addEventListener('resize', resize);
  resize();

  // ---- Freie Kamera (Maus) -----------------------------------------------------------------
  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.enabled = true;
  let free = false;
  controls.addEventListener('start', () => { free = true; flight = null; onFree?.(); });
  let onFree = null;

  // ---- Kamera-Regie --------------------------------------------------------------------------
  const pose = { pos: new THREE.Vector3(0, 2, 10), target: new THREE.Vector3() };
  let flight = null;              // { p0, t0, p1, t1, start, dur, arc, resolve }
  let restPose = null;            // Ziel der letzten Fahrt (für Drift und R)
  let arrivedAt = 0, drift = true;
  const tmpA = new THREE.Vector3(), tmpB = new THREE.Vector3(), tmpC = new THREE.Vector3();

  function flyTo(shot, dur = 1.6, { arc = 0, noDrift = false } = {}) {
    free = false;
    flight?.resolve?.(false);
    return new Promise((resolve) => {
      flight = {
        p0: camera.position.clone(), t0: pose.target.clone(),
        p1: shot.pos.clone(), t1: shot.target.clone(),
        start: performance.now(), dur: dur * 1000, arc, resolve, noDrift,
      };
      restPose = { pos: shot.pos.clone(), target: shot.target.clone(), noDrift };
    });
  }
  function jumpTo(shot, { noDrift = false } = {}) {
    free = false;
    flight?.resolve?.(false);
    flight = null;
    pose.pos.copy(shot.pos); pose.target.copy(shot.target);
    camera.position.copy(shot.pos); camera.lookAt(shot.target);
    tiefe();
    restPose = { pos: shot.pos.clone(), target: shot.target.clone(), noDrift };
    arrivedAt = performance.now();
  }

  function updateCamera(now) {
    if (free) { controls.update(); pose.target.copy(controls.target); tiefe(); return; }
    if (flight) {
      const k = Math.min(1, (now - flight.start) / flight.dur);
      const e = smoother(k);
      tmpA.lerpVectors(flight.p0, flight.p1, e);
      if (flight.arc) tmpA.y += Math.sin(Math.PI * e) * flight.arc;
      pose.target.lerpVectors(flight.t0, flight.t1, e);
      camera.position.copy(tmpA);
      camera.lookAt(pose.target);
      if (k >= 1) { const r = flight.resolve; flight = null; arrivedAt = now; r(true); }
    } else if (restPose) {
      // sehr ruhige Drift: ±0,35° Gieren, Periode 26 s, blendet nach der Ankunft weich ein
      const w = drift && !restPose.noDrift ? sm((now - arrivedAt) / 1000, 0.2, 3.5) : 0;
      const yaw = Math.sin(((now - arrivedAt) / 1000) * (Math.PI * 2 / 26)) * THREE.MathUtils.degToRad(0.35) * w;
      tmpB.subVectors(restPose.pos, restPose.target).applyAxisAngle(THREE.Object3D.DEFAULT_UP, yaw);
      camera.position.copy(restPose.target).add(tmpB);
      pose.target.copy(restPose.target);
      camera.lookAt(pose.target);
    }
    controls.target.copy(pose.target);
    tiefe();
  }
  const fogBase = { near: 1.2, far: 4 };
  function tiefe() {
    const d = camera.position.distanceTo(pose.target);
    const near = Math.min(4, Math.max(0.02, d * 0.025)), far = Math.min(2000, Math.max(60, d * 14));
    if (Math.abs(near - camera.near) > camera.near * 0.02 || Math.abs(far - camera.far) > camera.far * 0.02) {
      camera.near = near; camera.far = far; camera.updateProjectionMatrix();
    }
    scene.fog.near = d * fogBase.near + 3;
    scene.fog.far = d * fogBase.far + 12;
  }

  // ---- Beschriftungen: HTML an 3D-Punkten --------------------------------------------------
  const labels = [];
  const layer = document.getElementById('labels');
  function addLabel(html, cls = '') {
    const el = document.createElement('div');
    el.className = `label ${cls}`;
    el.innerHTML = `<div class="label-in">${html}</div>`;
    layer.append(el);
    const l = { el, pos: new THREE.Vector3(), show: 0, cur: -1, html };
    labels.push(l);
    return l;
  }
  function setLabelHtml(l, html) { if (l.html !== html) { l.html = html; l.el.firstElementChild.innerHTML = html; } }
  const proj = new THREE.Vector3();
  function updateLabels() {
    const w = innerWidth, h = innerHeight;
    for (const l of labels) {
      const vis = l.show > 0.01;
      if (!vis) { if (l.cur !== 0) { l.el.style.opacity = '0'; l.el.style.visibility = 'hidden'; l.cur = 0; } continue; }
      proj.copy(l.pos).project(camera);
      const behind = proj.z > 1;
      const x = (proj.x * 0.5 + 0.5) * w, y = (-proj.y * 0.5 + 0.5) * h;
      l.el.style.transform = `translate3d(${x.toFixed(2)}px, ${y.toFixed(2)}px, 0)`;
      const o = behind ? 0 : l.show;
      if (Math.abs(o - l.cur) > 0.004) { l.el.style.opacity = o.toFixed(3); l.el.style.visibility = o > 0 ? 'visible' : 'hidden'; l.cur = o; }
    }
  }

  function project(v, out = { x: 0, y: 0, behind: false }) {
    proj.copy(v).applyMatrix4(camera.matrixWorldInverse);
    out.behind = proj.z > -camera.near;
    proj.copy(v).project(camera);
    out.x = (proj.x * 0.5 + 0.5) * innerWidth;
    out.y = (-proj.y * 0.5 + 0.5) * innerHeight;
    return out;
  }

  // ---- Bildschleife --------------------------------------------------------------------------
  const frameHooks = [];
  let paused = false, last = performance.now(), ema = 16.7, slowFor = 0, settle = 0;
  function loop(now) {
    requestAnimationFrame(loop);
    const dt = Math.min(0.05, (now - last) / 1000);
    const frameMs = now - last;
    last = now;
    if (paused) return;
    // Leistung nachregeln: dauerhaft unter ~45 fps → weniger Pixel. Nach einer Absenkung höchstens wieder bis
    // knapp unter die Stufe, die zu langsam war (kein Pendeln). Kurze Hänger (Tab-Wechsel, Shader) zählen nicht.
    if (settle > 0) { settle -= dt; } else {
      ema = ema * 0.94 + Math.min(frameMs, 60) * 0.06;
      if (ema > 22) slowFor += dt; else slowFor = 0;
      if (slowFor > 3 && quality > 0.7) { quality = Math.max(0.7, quality - 0.15); slowFor = 0; settle = 2; resize(); }
    }

    updateCamera(now);
    for (const f of frameHooks) f(dt, now);
    camera.updateMatrixWorld();
    updateLabels();
    composer.render(dt);
  }

  return {
    renderer, scene, camera, controls, composer, bloom, key, hemi, rim,
    flyTo, jumpTo, project, addLabel, setLabelHtml,
    isFlying: () => !!flight,
    isFree: () => free,
    onFrame: (f) => frameHooks.push(f),
    onFree: (f) => { onFree = f; },
    setPaused: (p) => { paused = p; last = performance.now(); settle = 1; },
    setDrift: (d) => { drift = d; },
    start: () => requestAnimationFrame((t) => { last = t; settle = 1.5; quality = 1; resize(); loop(t); }),
    renderOnce: () => { camera.updateMatrixWorld(); composer.render(0.016); },
    get quality() { return quality; },
  };
}
