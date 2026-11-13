import { animate, stagger } from '../vendor/anime.esm.min.js';
import { OBJECTS, getObject } from './data/objects/index.js';
import { CLASSES, MATERIALS, ELEMENTS } from './data/catalog.js';
import { INVENTORY, byId } from './data/inventory.js';
import { ExplodedView, partColor } from './iso.js';

const app = document.getElementById('app');
const modalRoot = document.getElementById('modal-root');
const tip = document.getElementById('tip');

// Position der Objekte auf den Beispielfotos (Anteil der Bildfläche), nur für die Scan-Animation.
const SAMPLE_BBOX = {
  smartphone: [0.10, 0.33, 0.70, 0.28],
  flasche: [0.31, 0.23, 0.37, 0.42],
  laptop: [0.22, 0.23, 0.57, 0.52],
  netzteil: [0.08, 0.15, 0.81, 0.50],
};
const NEW_FACH = 'E-12';

const state = {
  obj: null,
  model: null,
  stock: INVENTORY.filter((i) => i.einheit === 'Stk').reduce((a, i) => a + i.menge, 0),
  view: null,
  explode: null,
  stream: null,
};

const h = (html) => {
  const t = document.createElement('template');
  t.innerHTML = html.trim();
  return t.content.firstElementChild;
};
const pct = (v) => `${Math.round(v * 100)} %`;
const fmt = (n) => String(n).replace('.', ',');

function setStep(step) {
  const order = ['scan', 'sheet', 'craft'];
  document.querySelectorAll('#steps span').forEach((s) => {
    const i = order.indexOf(s.dataset.step), cur = order.indexOf(step);
    s.classList.toggle('active', i === cur);
    s.classList.toggle('done', i < cur);
  });
  document.getElementById('stock-count').textContent = state.stock;
}

function show(viewEl, step) {
  const old = state.view;
  state.explode?.destroy();
  state.explode = null;
  stopCamera();
  app.appendChild(viewEl);
  state.view = viewEl;
  setStep(step);
  if (old) {
    animate(old, { opacity: [1, 0], translateY: [0, -12], duration: 260, ease: 'inQuad', onComplete: () => old.remove() });
  }
  animate(viewEl, { opacity: [0, 1], translateY: [16, 0], duration: 420, delay: old ? 140 : 0, ease: 'outCubic' });
}

