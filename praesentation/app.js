// Navigation: keys, slides and steps, overlay text, and control of the embedded web app (iframe).
import { createEngine } from './engine.js';
import { buildWorld, shots } from './world.js';
import { slides, APP_URL } from './content.js';

const $ = (selector) => document.querySelector(selector);
const canvas = $('#world');
const slideEl = $('#slide');
const frame = $('#app');
const footer = $('#footer');
const notesEl = $('#notes');
const helpEl = $('#help');

const engine = createEngine(canvas, $('#labels'));
const world = buildWorld(engine.scene);

const LABELS = { werkbank: 'Werkbank', lager: 'Lager', kamera: 'Kamera und NIR-Sensor', scanflaeche: 'Scan-Fläche', monitor: 'Monitor' };
for (const [id, position] of Object.entries(world.anchors)) engine.addLabel(id, LABELS[id] ?? id, position);

const MODES = {
  praesi: 'Präsentation',
  fahrt: 'Kamerafahrt',
  frei: 'Freie Kamera · R zurück',
  app: 'App bedienen · Klick daneben oder Weiter',
};

const state = { slide: -1, step: 0, mode: 'praesi', app: null, flight: 0 };

// ---- Slides and steps -----------------------------------------------------------------------

function renderSlide(slide) {
  slideEl.className = `slide layout-${slide.layout}`;
  slideEl.innerHTML = slide.html;
  slideEl.dataset.id = slide.id;
  notesEl.textContent = slide.notes ?? '';
  requestAnimationFrame(() => slideEl.classList.add('in'));
}

function flightDuration(shot) {
  const distance = engine.camera.position.distanceTo(shot.pos);
  return Math.min(3000, Math.max(1000, 900 + distance * 230));
}

async function go(slideIndex, stepIndex = 0, instant = false) {
  slideIndex = Math.max(0, Math.min(slides.length - 1, slideIndex));
  const slide = slides[slideIndex];
  stepIndex = Math.max(0, Math.min(slide.steps.length - 1, stepIndex));
  const step = slide.steps[stepIndex];
  if (slideIndex !== state.slide) renderSlide(slide);
  slideEl.classList.toggle('compact', stepIndex > 0);
  state.slide = slideIndex;
  state.step = stepIndex;

  // The app stays on the monitor while the camera moves in further; otherwise it hides during flights.
  const keepApp = state.app === 'monitor' && step.app === 'full';
  if (!keepApp) setApp(null);
  engine.setPaused(false);
  engine.showLabels([]);
  setMode('fahrt');
  const token = ++state.flight;
  const shot = shots[step.shot];
  if (instant) engine.jumpTo(shot);
  else await engine.flyTo(shot, flightDuration(shot));
  if (token !== state.flight) return;

  setMode('praesi');
  engine.showLabels(step.labels ?? []);
  setApp(step.app ?? null);
}

function next() {
  const slide = slides[state.slide];
  if (state.step < slide.steps.length - 1) go(state.slide, state.step + 1);
  else if (state.slide < slides.length - 1) go(state.slide + 1, 0);
}

function prev() {
  if (state.step > 0) go(state.slide, state.step - 1);
  else if (state.slide > 0) go(state.slide - 1, slides[state.slide - 1].steps.length - 1);
}

function resetCamera() {
  const step = slides[state.slide].steps[state.step];
  setMode('fahrt');
  const token = ++state.flight;
  engine.flyTo(shots[step.shot], 800).then(() => { if (token === state.flight) setMode('praesi'); });
}

// ---- Embedded app -----------------------------------------------------------------------------

frame.src = APP_URL;

function setApp(mode) {
  state.app = mode;
  document.body.dataset.app = mode ?? '';
  frame.classList.toggle('on', mode !== null);
  if (mode === 'full') {
    frame.classList.add('animate');
    Object.assign(frame.style, { left: '0px', top: '0px', width: `${innerWidth}px`, height: `${innerHeight}px`, opacity: '1' });
    // The app covers everything: stop rendering the 3D world to leave the GPU to the app.
    setTimeout(() => { if (state.app === 'full') engine.setPaused(true); }, 450);
  } else {
    frame.classList.remove('animate');
  }
  if (mode === null && document.activeElement === frame) window.focus();
}

// Place the app exactly over the monitor screen: project its corners every frame.
engine.onFrame(() => {
  if (state.app !== 'monitor') return;
  const points = world.screen.corners.map((c) => engine.project(c));
  const toCamera = engine.camera.position.clone().sub(world.screen.center).normalize();
  const facing = toCamera.dot(world.screen.normal) > 0.9 && !points.some((p) => p.behind);
  const xs = points.map((p) => p.x), ys = points.map((p) => p.y);
  const left = Math.min(...xs), top = Math.min(...ys);
  Object.assign(frame.style, {
    left: `${left}px`, top: `${top}px`,
    width: `${Math.max(...xs) - left}px`, height: `${Math.max(...ys) - top}px`,
    opacity: facing ? '1' : '0',
  });
  frame.style.pointerEvents = facing ? 'auto' : 'none';
});

window.addEventListener('resize', () => {
  if (state.app === 'full') Object.assign(frame.style, { width: `${innerWidth}px`, height: `${innerHeight}px` });
});

// Clicking into the app moves keyboard focus into the iframe: the presentation sees no keys then.
window.addEventListener('blur', () => setTimeout(() => {
  if (document.activeElement === frame) setMode('app');
}, 0));
window.addEventListener('focus', () => { if (state.mode === 'app') setMode('praesi'); });
document.addEventListener('pointerdown', (e) => {
  if (state.mode === 'app' && e.target !== frame) window.focus();
});
$('#next').addEventListener('click', () => { window.focus(); next(); });

// ---- Mode, footer, keys -------------------------------------------------------------------------

function setMode(mode) {
  state.mode = mode;
  document.body.dataset.mode = mode;
  const slide = slides[state.slide];
  const step = slide?.steps[state.step];
  footer.innerHTML = slide
    ? `<span>${state.slide + 1}/${slides.length} · ${slide.title} · ${step.name}</span><b>${MODES[mode]}</b>`
    : `<b>${MODES[mode]}</b>`;
}

engine.controls.addEventListener('start', () => { if (!engine.isFlying()) setMode('frei'); });

function toggleFullscreen() {
  if (document.fullscreenElement) document.exitFullscreen();
  else document.documentElement.requestFullscreen();
}

window.addEventListener('keydown', (e) => {
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  const key = e.key;
  if (['ArrowRight', 'ArrowDown', ' ', 'PageDown'].includes(key)) { e.preventDefault(); next(); }
  else if (['ArrowLeft', 'ArrowUp', 'PageUp'].includes(key)) { e.preventDefault(); prev(); }
  else if (/^[1-9]$/.test(key)) go(Number(key) - 1, 0);
  else if (key === 'f' || key === 'F') toggleFullscreen();
  else if (key === 'h' || key === 'H') helpEl.hidden = !helpEl.hidden;
  else if (key === 't' || key === 'T') notesEl.hidden = !notesEl.hidden;
  else if (key === 'r' || key === 'R') resetCamera();
  else if (key === 'Escape') { helpEl.hidden = true; notesEl.hidden = true; }
});

// Hook for tools/shots.cjs: jump to any station and wait until the camera has arrived.
window.__praesi = {
  slides: slides.map((s) => ({ id: s.id, steps: s.steps.map((st) => st.shot) })),
  go: (slide, step) => go(slide, step, true),
  busy: () => engine.isFlying(),
};

go(0, 0, true);
