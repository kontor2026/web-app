// Navigation, Overlay-Text und die eingebettete Web-App.
// Die App liegt als iframe über dem Monitor: Jeden Frame werden die vier Bildschirmecken projiziert und das iframe
// per Homografie (CSS matrix3d) perspektivisch genau darauf abgebildet. Am Ende der Fahrt in den Bildschirm ist die
// Abbildung die Identität, dann wird das iframe ohne Transformation gezeigt (gestochen scharf) und die 3D-Welt pausiert.
import { createEngine, clamp01, lerp } from './engine.js';
import { buildWorld } from './world.js';
import { slides, STEPS, stepIndex, APP_URL, PRODUKTNAME, SCHLUSSSATZ, QR_URL, QR_TEXT, MITBRINGEN } from './content.js';

const $ = (s) => document.querySelector(s);
const engine = createEngine($('#world'));
const frame = $('#app');
const LIVE = stepIndex('live'), MONITOR = stepIndex('monitor');
const BACK_T = 60;                       // rückwärts angekommen: Schritt im Endzustand zeigen

const state = { k: -1, enteredAt: 0, token: 0, appFull: false, returnTo: null, black: false, lastNav: 0, appOp: 0, ready: false };
let world = null;

// ---- Start: Modelle laden, Shader kompilieren, jede Station einmal vorrendern -------------------
(async () => {
  try {
    world = await buildWorld(engine);
  } catch (e) {
    $('#loader').classList.add('error');
    $('#loader .msg').textContent = `Fehler beim Laden: ${e.message}`;
    throw e;
  }
  const k0 = fromHash() ?? 0;
  frame.src = APP_URL;
  $('#loader .msg').textContent = 'Bereite Szenen vor';
  await new Promise((r) => setTimeout(r, 30));
  world.allVisible(() => engine.renderer.compile(engine.scene, engine.camera));
  for (let k = 0; k < STEPS.length; k++) {
    world.update(k, BACK_T, 0, 100);
    engine.jumpTo(world.shot(STEPS[k].id));
    engine.renderOnce();
    await new Promise((r) => setTimeout(r, 0));
  }
  buildFooter();
  // Das iframe einmal kurz (fast unsichtbar) zeichnen lassen, damit sein erstes Erscheinen nicht hakt
  frame.style.visibility = 'visible';
  frame.style.opacity = '0.01';
  await new Promise((r) => setTimeout(r, 200));     // kein requestAnimationFrame: lädt auch in einem Hintergrund-Tab fertig
  frame.style.visibility = 'hidden';
  frame.style.opacity = '0';
  go(k0, { instant: true });
  world.update(k0, 0, 0, 100);
  engine.onFrame(frameHook);
  engine.start();
  state.ready = true;
  document.body.classList.add('ready');
})();

function fromHash() {
  const n = parseInt(location.hash.slice(1), 10);
  if (Number.isFinite(n) && n >= 1 && n <= STEPS.length) return n - 1;
  const i = stepIndex(location.hash.slice(1));
  return i >= 0 ? i : null;
}

// ---- Schritte -------------------------------------------------------------------------------------
function stepTime() { return (performance.now() - state.enteredAt) / 1000; }

function go(k, { instant = false, backwards = false, replay = false } = {}) {
  k = Math.max(0, Math.min(STEPS.length - 1, k));
  if (k === state.k && !replay) return;
  const step = STEPS[k];
  const prevK = state.k;
  state.k = k;
  state.enteredAt = performance.now() - (backwards ? BACK_T * 1000 : 0);
  if (state.appFull && !step.app) exitFull();
  history.replaceState(null, '', `#${k + 1}`);

  const shot = world.shot(step.id);
  const token = ++state.token;
  let delay = 0;
  if (instant) {
    engine.jumpTo(shot, { noDrift: shot.noDrift });
    if (step.app) enterFull();
  } else {
    const dist = engine.camera.position.distanceTo(shot.pos);
    let dur = Math.min(3.4, Math.max(1.4, 1.15 + dist * 0.15));
    if (step.app && prevK === MONITOR) dur = 1.7;
    delay = Math.min(dur * 0.55, 1.4);
    engine.flyTo(shot, dur, { arc: shot.arc ?? 0, noDrift: shot.noDrift }).then((arrived) => {
      if (arrived && token === state.token && STEPS[state.k].app) enterFull();
    });
  }
  setCaption(step, delay);
  updateFooter();
  $('#notes').innerHTML = notesHtml(k);
  setModeText();
}

const next = () => go(state.k + 1);
const prev = () => go(state.k - 1, { backwards: true });

function toggleApp() {
  if (state.k === LIVE) {
    if (state.returnTo != null) { const r = state.returnTo; state.returnTo = null; go(r, { backwards: true }); }
    else go(LIVE + 1);
  } else {
    state.returnTo = state.k === MONITOR ? null : state.k;
    go(LIVE);
  }
}

// ---- Text auf dem Bild ------------------------------------------------------------------------------
let captionTimer = 0, finaleTimers = [];
function setCaption(step, delay) {
  const el = $('#caption');
  el.classList.remove('in', 'finale', 'kipp');
  if (!step.qr) $('#qr').classList.remove('in');
  if (!step.messwerte) $('#messwerte').classList.remove('in');
  clearTimeout(captionTimer);
  finaleTimers.forEach(clearTimeout);
  finaleTimers = [];
  captionTimer = setTimeout(() => {
    if (step.qr) $('#qr').classList.add('in');
    if (step.messwerte) finaleTimers.push(setTimeout(() => $('#messwerte').classList.add('in'), 1200));
    if (step.finale) return finale(el);
    el.innerHTML = step.caption ? `<h2>${step.caption}</h2>${step.sub ? `<p class="sub">${step.sub}</p>` : ''}` : '';
    if (step.caption) requestAnimationFrame(() => el.classList.add('in'));
  }, Math.max(320, delay * 1000));
}

// Letzte Folie: „Bring … mit.“ kippt durch mehrere Gegenstände, dann kippt alles zum Namen, dazu der QR-Code
function finale(el) {
  el.classList.add('finale');
  el.innerHTML = `<div class="rad">${MITBRINGEN.map((w) => `<h2>Bring ${w} mit.</h2>`).join('')}</div><div class="name"><h1>${SCHLUSSSATZ}</h1><p>${PRODUKTNAME}</p></div>`;
  const zeilen = [...el.querySelectorAll('.rad h2')];
  const zeige = (i) => zeilen.forEach((z, j) => { z.classList.toggle('an', j === i); z.classList.toggle('weg', j < i); });
  requestAnimationFrame(() => { el.classList.add('in'); zeige(0); });
  const T = 1500;
  zeilen.forEach((_, i) => { if (i) finaleTimers.push(setTimeout(() => zeige(i), 900 + i * T)); });
  const ende = 900 + zeilen.length * T + 300;
  finaleTimers.push(setTimeout(() => el.classList.add('kipp'), ende));
}

// ---- Eingebettete App -----------------------------------------------------------------------------
function homography(w, h, p) {
  // Einheitsquadrat → Viereck (p0 oben links, p1 oben rechts, p2 unten rechts, p3 unten links), dann auf w × h skaliert
  const [x0, y0] = [p[0].x, p[0].y], [x1, y1] = [p[1].x, p[1].y], [x2, y2] = [p[2].x, p[2].y], [x3, y3] = [p[3].x, p[3].y];
  const dx1 = x1 - x2, dx2 = x3 - x2, dx3 = x0 - x1 + x2 - x3, dy1 = y1 - y2, dy2 = y3 - y2, dy3 = y0 - y1 + y2 - y3;
  let a, b, c, d, e, f, g, hh;
  if (Math.abs(dx3) < 1e-9 && Math.abs(dy3) < 1e-9) {
    a = x1 - x0; b = x2 - x1; c = x0; d = y1 - y0; e = y2 - y1; f = y0; g = 0; hh = 0;
  } else {
    const det = dx1 * dy2 - dx2 * dy1;
    g = (dx3 * dy2 - dx2 * dy3) / det;
    hh = (dx1 * dy3 - dx3 * dy1) / det;
    a = x1 - x0 + g * x1; b = x3 - x0 + hh * x3; c = x0;
    d = y1 - y0 + g * y1; e = y3 - y0 + hh * y3; f = y0;
  }
  return `matrix3d(${a / w},${d / w},0,${g / w},${b / h},${e / h},0,${hh / h},0,0,1,0,${c},${f},0,1)`;
}

const projected = [0, 1, 2, 3].map(() => ({ x: 0, y: 0, behind: false }));
let lastTransform = '';
function updateApp(dt) {
  if (state.appFull) return;
  const allowed = state.k === MONITOR || state.k === LIVE;
  let target = 0;
  if (allowed) {
    const n = world.screenNormal(), c = world.screenPos();
    const to = engine.camera.position.clone().sub(c);
    const dist = to.length();
    const facing = to.normalize().dot(n);
    target = clamp01((facing - 0.72) / 0.2) * clamp01((3.4 - dist) / 1.4) * clamp01((stepTime() - 0.2) / 0.6 + (state.k === LIVE ? 1 : 0));
  }
  state.appOp = lerp(state.appOp, target, 1 - Math.exp(-dt * 7));
  if (state.appOp < 0.004) { if (frame.style.visibility !== 'hidden') frame.style.visibility = 'hidden'; return; }
  const corners = world.screenCorners();
  let behind = false;
  corners.forEach((cw, i) => { engine.project(cw, projected[i]); behind ||= projected[i].behind; });
  if (behind) { frame.style.visibility = 'hidden'; return; }
  const t = homography(innerWidth, innerHeight, projected);
  if (t !== lastTransform) { frame.style.transform = t; lastTransform = t; }
  frame.style.visibility = 'visible';
  frame.style.opacity = state.appOp.toFixed(3);
}

function enterFull() {
  state.appFull = true;
  state.appOp = 1;
  frame.style.transform = 'none';
  lastTransform = 'none';
  frame.style.opacity = '1';
  frame.style.visibility = 'visible';
  document.body.dataset.app = 'full';
  setModeText();
  // Die App deckt alles ab: 3D-Welt anhalten, die GPU gehört der App
  setTimeout(() => { if (state.appFull) engine.setPaused(true); }, 350);
}
function exitFull() {
  state.appFull = false;
  engine.setPaused(false);
  document.body.dataset.app = '';
  if (document.activeElement === frame) frame.blur();
  window.focus();
  setModeText();
}

// Tasten aus der App (gleicher Ursprung) an die Präsentation weiterreichen, außer beim Tippen
const APP_KEYS = new Set(['x', 'X', 'f', 'F', 'PageDown', 'PageUp', 'b', 'B', 'h', 'H', 't', 'T']);
frame.addEventListener('load', () => {
  try {
    frame.contentWindow.addEventListener('keydown', (e) => {
      const el = e.target;
      if (el && (/^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName) || el.isContentEditable)) return;
      if (APP_KEYS.has(e.key)) { e.preventDefault(); onKey(e); }
    });
  } catch { /* andere Herkunft: die App kann postMessage({ type: 'praesi-key', key }) schicken */ }
});
addEventListener('message', (e) => {
  if (e.data?.type === 'praesi-key' && APP_KEYS.has(e.data.key)) onKey({ key: e.data.key, repeat: false, preventDefault() {} });
});
$('#apphint').addEventListener('click', () => toggleApp());

// ---- Pro Frame ----------------------------------------------------------------------------------------
function frameHook(dt, now) {
  world.update(state.k, stepTime(), now / 1000, dt);
  updateApp(dt);
}

// ---- Footer, Hilfe, Sprechertext ------------------------------------------------------------------------
function buildFooter() {
  $('#dots').innerHTML = slides.map((s, si) => `<span class="grp" title="${s.aida} · ${s.title}"><em>${s.aida[0]}</em>${s.steps
    .map((st) => `<i data-k="${STEPS.findIndex((x) => x.id === st.id)}"></i>`).join('')}</span>`).join('');
  $('#dots').addEventListener('click', (e) => { const k = e.target.dataset?.k; if (k != null) go(Number(k)); });
}
function updateFooter() {
  document.querySelectorAll('#dots i').forEach((el) => {
    const k = Number(el.dataset.k);
    el.classList.toggle('on', k === state.k);
    el.classList.toggle('done', k < state.k);
  });
}
function setModeText() {
  const step = STEPS[state.k];
  const slide = slides[step?.slide];
  let mode = 'Präsentation';
  if (state.appFull) mode = 'App live · X zurück';
  else if (engine.isFree()) mode = 'Freie Kamera · R zurück';
  $('#mode').textContent = slide ? `${slide.aida} · ${step.name} · ${mode}` : mode;
}
engine.onFree(() => setModeText());
function notesHtml(k) {
  const s = STEPS[k], n = STEPS[k + 1];
  return `<p class="kicker">${slides[s.slide].aida} · ${k + 1}/${STEPS.length} · ${s.name}</p><p>${s.notes ?? ''}</p>${n ? `<p class="nexts">Danach: ${n.name}</p>` : ''}`;
}

function toggleFullscreen() {
  if (document.fullscreenElement) document.exitFullscreen();
  else document.documentElement.requestFullscreen({ navigationUI: 'hide' }).catch(() => {});
}
function setBlack(on) { state.black = on; document.body.classList.toggle('black', on); }

function resetCamera() {
  const s = world.shot(STEPS[state.k].id);
  engine.flyTo(s, 0.9, { noDrift: s.noDrift }).then(() => setModeText());
}

// ---- Tasten ---------------------------------------------------------------------------------------------
function onKey(e) {
  if (!state.ready || e.repeat || e.metaKey || e.ctrlKey || e.altKey) return;
  const key = e.key;
  if (state.black) { if (!['b', 'B', '.'].includes(key)) { e.preventDefault(); } setBlack(false); return; }
  const nav = (fn) => { e.preventDefault(); const now = performance.now(); if (now - state.lastNav < 280) return; state.lastNav = now; fn(); };
  // In der laufenden App nur die Tasten, die die App nicht selbst braucht
  if (state.appFull && ['ArrowRight', 'ArrowLeft', 'ArrowUp', 'ArrowDown', ' '].includes(key)) return;
  if (['ArrowRight', 'ArrowDown', ' ', 'PageDown', 'Enter'].includes(key)) nav(next);
  else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(key)) nav(prev);
  else if (key === 'x' || key === 'X') nav(toggleApp);
  else if (/^[1-9]$/.test(key)) { const s = slides[Number(key) - 1]; if (s) nav(() => go(STEPS.findIndex((x) => x.id === s.steps[0].id))); }
  else if (key === 'f' || key === 'F') toggleFullscreen();
  else if (key === 'h' || key === 'H') $('#help').hidden = !$('#help').hidden;
  else if (key === 't' || key === 'T') $('#notes').hidden = !$('#notes').hidden;
  else if (key === 'r' || key === 'R') resetCamera();
  else if (key === 'z' || key === 'Z') go(state.k, { replay: true });
  else if (key === 'b' || key === 'B' || key === '.') setBlack(true);
  else if (key === 'Escape') { $('#help').hidden = true; $('#notes').hidden = true; }
}
addEventListener('keydown', onKey);

$('#qr .url').textContent = QR_URL;
document.querySelectorAll('.produktname').forEach((el) => { el.textContent = PRODUKTNAME; });
document.title = PRODUKTNAME;
$('#qr .text').textContent = QR_TEXT;

// Für Prüfskripte: direkt zu einem Schritt springen (Endzustand) und warten, bis die Kamera steht
window.__praesi = {
  steps: STEPS.map((s) => s.id),
  go: (k, t = BACK_T) => { go(k, { instant: true, backwards: t >= BACK_T, replay: true }); if (t < BACK_T) state.enteredAt = performance.now() - t * 1000; },
  state,
  engine,
  // Für Prüfungen in gedrosselten Fenstern: n Bilder mit je 50 ms rechnen und zeichnen
  tick: (n = 40) => { for (let i = 0; i < n; i++) frameHook(0.05, performance.now()); engine.renderOnce(); },
};
