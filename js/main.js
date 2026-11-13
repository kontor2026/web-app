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

/* ------------------------------------------------------------------ */
/* 01 Erfassen                                                          */
/* ------------------------------------------------------------------ */

function viewScan() {
  const v = h(`
    <section class="view scan">
      <div class="viewfinder" id="vf">
        <div class="vf-grid"></div>
        <i class="vf-corner tl"></i><i class="vf-corner tr"></i><i class="vf-corner bl"></i><i class="vf-corner br"></i>
        <div class="vf-meta"><span>Station 01 · Kamera oben</span><span id="vf-state">bereit</span></div>
        <div class="vf-idle" id="vf-idle">
          <h2>Leg deinen Gegenstand auf die Fläche</h2>
          <p>Die Kamera erkennt, was es ist. Du kannst auch ein Foto hochladen.</p>
          <div class="row">
            <button class="btn" id="cam">Kamera starten</button>
            <button class="btn" id="upl">Bild hochladen</button>
          </div>
          <input type="file" id="file" accept="image/*" hidden>
        </div>
      </div>
      <aside class="side" id="side">
        <div>
          <div class="eyebrow">Schritt 01 · Erfassen</div>
          <h1 style="margin-top:8px">Was hast du mitgebracht?</h1>
          <p class="lead" style="margin-top:10px">Die Station erkennt deinen Gegenstand, zeigt dir, was in ihm steckt, und schlägt vor, was du daraus bauen kannst.</p>
        </div>
        <ol class="howto">
          <li>Gegenstand mittig auf die Station legen</li>
          <li>Scannen und Ergebnis kurz prüfen</li>
          <li>Steckbrief ansehen, dann einlagern oder bauen</li>
        </ol>
        <div>
          <div class="eyebrow" style="margin-bottom:10px">Beispiele zum Ausprobieren</div>
          <div class="samples">
            ${OBJECTS.map((o) => `<button class="sample" data-id="${o.id}"><img src="${o.photo}" alt=""><span>${o.name}</span></button>`).join('')}
          </div>
        </div>
      </aside>
    </section>`);

  v.querySelectorAll('.sample').forEach((b) => b.addEventListener('click', () => {
    const o = getObject(b.dataset.id);
    analyze(v, o.photo, o);
  }));
  const file = v.querySelector('#file');
  v.querySelector('#upl').addEventListener('click', () => file.click());
  file.addEventListener('change', () => {
    if (!file.files[0]) return;
    const r = new FileReader();
    r.onload = () => analyze(v, r.result, null);
    r.readAsDataURL(file.files[0]);
  });
  v.querySelector('#cam').addEventListener('click', () => startCamera(v));
  show(v, 'scan');
  animate(v.querySelectorAll('.side > *'), { opacity: [0, 1], translateY: [10, 0], delay: stagger(70, { start: 200 }), duration: 500, ease: 'outCubic' });
}

async function startCamera(v) {
  const vf = v.querySelector('#vf');
  try {
    state.stream = await navigator.mediaDevices.getUserMedia({ video: { width: 1920, height: 1080 } });
  } catch {
    v.querySelector('#vf-state').textContent = 'Kamera nicht verfügbar, bitte Bild hochladen';
    return;
  }
  v.querySelector('#vf-idle').style.display = 'none';
  const video = h('<video autoplay playsinline muted></video>');
  video.srcObject = state.stream;
  vf.prepend(video);
  const shot = h('<button class="btn primary" style="position:absolute;bottom:28px;left:50%;transform:translateX(-50%)">Foto aufnehmen</button>');
  vf.appendChild(shot);
  v.querySelector('#vf-state').textContent = 'live';
  shot.addEventListener('click', () => {
    const c = document.createElement('canvas');
    c.width = video.videoWidth; c.height = video.videoHeight;
    c.getContext('2d').drawImage(video, 0, 0);
    shot.remove(); video.remove(); stopCamera();
    analyze(v, c.toDataURL('image/jpeg', 0.9), null);
  });
}

function stopCamera() {
  state.stream?.getTracks().forEach((t) => t.stop());
  state.stream = null;
}

// Simulierte Erkennung. Später: POST /api/scan mit dem Bild, Antwort = erkennung + Objekt-ID.
function analyze(v, src, obj) {
  const vf = v.querySelector('#vf');
  v.querySelector('#vf-idle').style.display = 'none';
  vf.querySelectorAll('img, .scanline, .bbox, .vf-log').forEach((n) => n.remove());
  const img = h(`<img src="${src}" alt="">`);
  vf.prepend(img);
  v.querySelector('#vf-state').textContent = 'analysiere';

  const label = obj ? `${obj.name} · ${pct(obj.erkennung.conf)}` : 'Gegenstand · unsicher';
  const lines = obj
    ? ['Bild erfasst', 'Kontur gefunden', `Objektklasse: ${obj.name}`, `Modellabgleich: ${obj.erkennung.modelle.length} Kandidaten`]
    : ['Bild erfasst', 'Kontur gefunden', 'Objektklasse unsicher', 'Bitte Auswahl bestätigen'];
  const log = h(`<div class="vf-log">${lines.map((l, i) => `<div>› ${l}<em>${(0.3 + i * 0.5).toFixed(1).replace('.', ',')} s</em></div>`).join('')}</div>`);
  const scan = h('<div class="scanline"></div>');
  const box = h(`<div class="bbox"><span>${label}</span></div>`);
  vf.append(scan, box, log);

  img.onload = () => {
    // Darstellungsrechteck des Bildes (object-fit: contain) bestimmen.
    const W = vf.clientWidth, H = vf.clientHeight, r = Math.min(W / img.naturalWidth, H / img.naturalHeight);
    const iw = img.naturalWidth * r, ih = img.naturalHeight * r, ix = (W - iw) / 2, iy = (H - ih) / 2;
    const [bx, by, bw, bh] = obj ? SAMPLE_BBOX[obj.id] : [0.25, 0.25, 0.5, 0.5];
    Object.assign(box.style, { left: `${ix + bx * iw}px`, top: `${iy + by * ih}px`, width: `${bw * iw}px`, height: `${bh * ih}px` });

    animate(scan, { top: [iy, iy + ih], opacity: [{ to: 1, duration: 100 }, { to: 1, duration: 1300 }, { to: 0, duration: 200 }], duration: 1600, ease: 'inOutSine' });
    animate(log.children, { opacity: [0, 1], translateX: [-6, 0], delay: stagger(420, { start: 200 }), duration: 300 });
    animate(box, {
      opacity: [0, 1], scale: [1.08, 1], delay: 1500, duration: 450, ease: 'outBack',
      onComplete: () => {
        v.querySelector('#vf-state').textContent = 'erkannt';
        showResult(v, obj);
      },
    });
  };
}

document.querySelector('.brand').addEventListener('click', viewScan);

// Direkteinstieg für Demo und Entwicklung: #sheet=laptop oder #craft=flasche
const [, mode, id] = location.hash.match(/^#(sheet|craft)=(\w+)/) ?? [];
if (mode && getObject(id)) {
  state.obj = getObject(id);
  state.model = state.obj.erkennung.modelle[0][0];
  mode === 'sheet' ? viewSheet() : viewCraft();
} else {
  viewScan();
}
