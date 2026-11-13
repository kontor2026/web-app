// Renderer, light and studio environment, camera direction (eased flights between stations)
// and label anchors that follow 3D points on screen.
import * as THREE from 'three';
import { OrbitControls } from './assets/OrbitControls.js';
import { RoomEnvironment } from './assets/RoomEnvironment.js';

const easeInOutCubic = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

export function createEngine(canvas, labelLayer) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#14171a');
  scene.fog = new THREE.Fog('#14171a', 18, 40);
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

  scene.add(new THREE.HemisphereLight('#ffffff', '#3a3a3a', 0.55));
  const sun = new THREE.DirectionalLight('#fff4e6', 1.8);
  sun.position.set(5, 9, 6);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -9, right: 9, top: 9, bottom: -9, near: 1, far: 30 });
  sun.shadow.bias = -0.0004;
  scene.add(sun);
  const lamp = new THREE.PointLight('#ffe2c4', 6, 6, 1.6);
  lamp.position.set(2.0, 2.6, -2.0);
  scene.add(lamp);

  const camera = new THREE.PerspectiveCamera(45, 1, 0.05, 80);
  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.maxDistance = 25;

  // ---- Camera direction ---------------------------------------------------------------------
  let flight = null;

  /** Fly from the current view to a station. Resolves when the camera has arrived. */
  function flyTo(shot, duration = 1800) {
    if (flight) flight.resolve(false);
    controls.enabled = false;
    return new Promise((resolve) => {
      flight = {
        fromPos: camera.position.clone(), fromTarget: controls.target.clone(),
        toPos: shot.pos.clone(), toTarget: shot.target.clone(),
        start: performance.now(), duration, resolve,
      };
    });
  }

  /** Put the camera at a station without a flight. */
  function jumpTo(shot) {
    if (flight) flight.resolve(false);
    flight = null;
    camera.position.copy(shot.pos);
    controls.target.copy(shot.target);
    camera.lookAt(controls.target);
    controls.enabled = true;
    controls.update();
  }

  function stepFlight(now) {
    const t = Math.min(1, (now - flight.start) / flight.duration);
    const e = easeInOutCubic(t);
    camera.position.lerpVectors(flight.fromPos, flight.toPos, e);
    controls.target.lerpVectors(flight.fromTarget, flight.toTarget, e);
    camera.lookAt(controls.target);
    if (t >= 1) {
      const done = flight;
      flight = null;
      controls.enabled = true;
      controls.update();
      done.resolve(true);
    }
  }

  // ---- Label anchors ------------------------------------------------------------------------
  const labels = new Map();
  const tmp = new THREE.Vector3();

  function addLabel(id, text, position) {
    const el = document.createElement('div');
    el.className = 'label';
    el.textContent = text;
    labelLayer.appendChild(el);
    labels.set(id, { el, position, shown: false });
  }

  function showLabels(ids = []) {
    for (const [id, l] of labels) {
      l.shown = ids.includes(id);
      l.el.classList.toggle('on', l.shown);
    }
  }

  /** 3D point → CSS pixels of the canvas. `behind` is true when the point lies behind the camera. */
  function project(point) {
    tmp.copy(point).project(camera);
    const r = canvas.getBoundingClientRect();
    return { x: r.left + (tmp.x + 1) / 2 * r.width, y: r.top + (1 - tmp.y) / 2 * r.height, behind: tmp.z > 1 };
  }

  function updateLabels() {
    for (const l of labels.values()) {
      if (!l.shown) continue;
      const p = project(l.position);
      l.el.style.visibility = p.behind ? 'hidden' : 'visible';
      l.el.style.transform = `translate(${p.x}px, ${p.y}px)`;
    }
  }

  // ---- Loop ---------------------------------------------------------------------------------
  const frameHooks = [];
  let paused = false;

  function resize() {
    const w = window.innerWidth, h = window.innerHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  window.addEventListener('resize', resize);
  resize();

  renderer.setAnimationLoop((now) => {
    if (flight) stepFlight(now);
    else controls.update();
    updateLabels();
    for (const hook of frameHooks) hook(now);
    if (!paused) renderer.render(scene, camera);
  });

  return {
    THREE, scene, camera, controls, renderer,
    flyTo, jumpTo, addLabel, showLabels, project,
    onFrame: (fn) => frameHooks.push(fn),
    setPaused: (value) => { paused = value; },
    isFlying: () => flight !== null,
  };
}
