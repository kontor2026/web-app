// QR-Codes: links Etiketten zum Ausdrucken (ein Code je Kategorie, führt auf ihr 3D-Modell),
// rechts ein Scanner. Der Scanner nutzt BarcodeDetector des Browsers; wo es den nicht gibt,
// liest die normale Handykamera die Codes ohnehin und öffnet den Link.
import { shell, esc } from '../shell.js';
import index from '../../../../backend/seed/kategorien/index.json';
import { qrSvg } from './qrcode.js';
import './qr.css';

// Codes zeigen immer auf die veröffentlichte Seite, auch wenn lokal gebaut wird
const PAGES = 'https://kontor2026.github.io/web-app/';
const lokal = location.protocol !== 'https:' || /^(localhost|127\.|\[::1\])/.test(location.hostname);
const ROOT = lokal ? PAGES : new URL('../', location.href).href;
const ziel = (id) => (id ? `${ROOT}modelle/#kat=${id}` : ROOT);

// Nur Kategorien mit Modelldatei (Schlüssel reichen, geladen wird nichts)
const MODELLE = import.meta.glob('../../../../backend/seed/kategorien/*.json');
const liste = index.filter((k) => `../../../../backend/seed/kategorien/${k.id}.json` in MODELLE);
const app = shell('qr', '../');
app.innerHTML = `
<section class="view craft qrseite">
  <div class="craft-main">
    <div class="craft-head">
      <div>
        <h1>QR-Codes</h1>
        <p>Ein Code je Gegenstand. Aufkleben, scannen, und das 3D-Modell mit Steckbrief öffnet sich.</p>
      </div>
      <div class="row"><button class="btn" id="drucken">Drucken</button></div>
    </div>
    <div>
      <div class="qr-filter">
        <input class="suche-feld" id="suche" type="search" placeholder="Gegenstand suchen" aria-label="Gegenstand suchen" autocomplete="off">
        <span class="qr-anzahl" id="anzahl"></span>
      </div>
      <ul class="qr-etiketten" id="etiketten"></ul>
    </div>
  </div>
  <aside class="inv qr-scanner">
    <h2 class="qr-titel">Scannen</h2>
    <div class="qr-video" id="sucher"><video id="video" playsinline muted></video><i class="qr-rahmen"></i></div>
    <button class="btn" id="kamera">Kamera starten</button>
    <p class="qr-hinweis" id="hinweis"></p>
    <div class="qr-treffer" id="treffer" hidden></div>
    <h2 class="qr-titel">Diese Seite</h2>
    <a class="qr-start" href="${esc(ROOT)}">${qrSvg(ROOT, { titel: 'Startseite der Kreislauf-Station' })}<span>${esc(ROOT.replace(/^https:\/\//, ''))}</span></a>
  </aside>
</section>`;

// ---------- Etiketten ----------
const etiketten = document.getElementById('etiketten');
const svgCache = new Map();
const svg = (k) => svgCache.get(k.id) ?? svgCache.set(k.id, qrSvg(ziel(k.id), { titel: k.name })).get(k.id);
const normal = (s) => s.toLowerCase().normalize('NFD').replace(/\p{M}/gu, '');
function zeige() {
  const q = normal(document.getElementById('suche').value.trim());
  const treffer = liste.filter((k) => !q || normal(`${k.name} ${k.name_en} ${k.id}`).includes(q));
  etiketten.innerHTML = treffer.map((k) => `
    <li class="qr-etikett">
      <a href="${esc(ziel(k.id))}">${svg(k)}</a>
      <b>${esc(k.name)}</b>
      <span>${esc(k.klasse ?? '')}</span>
    </li>`).join('') || '<li class="qr-leer">Nichts gefunden.</li>';
  document.getElementById('anzahl').textContent = `${treffer.length} von ${liste.length}`;
}
document.getElementById('suche').addEventListener('input', zeige);
document.getElementById('drucken').addEventListener('click', () => print());
zeige();

// ---------- Scanner ----------
const video = document.getElementById('video');
const hinweis = document.getElementById('hinweis');
const knopf = document.getElementById('kamera');
const kannLesen = 'BarcodeDetector' in window;
const kannKamera = !!navigator.mediaDevices?.getUserMedia && isSecureContext;
let strom = null, detektor = null, laeuft = false;

if (!kannKamera || !kannLesen) {
  knopf.hidden = true;
  document.getElementById('sucher').hidden = true;
  hinweis.innerHTML = 'Dieser Browser kann QR-Codes nicht selbst lesen. Einfach die <b>Kamera-App</b> des Handys auf einen Code halten: Sie erkennt ihn und öffnet das Modell.';
} else {
  hinweis.textContent = 'Kamera auf einen Code halten. Codes dieser Seite öffnen sich sofort.';
}

// Eigene Links direkt öffnen, fremde nur anzeigen
const eigen = (url) => { try { const u = new URL(url); return [PAGES, ROOT].some((r) => u.href.startsWith(r)); } catch { return false; } };
function gefunden(text) {
  const box = document.getElementById('treffer');
  if (eigen(text)) {
    stopp();
    const id = new URL(text).hash.match(/kat=([\w-]+)/)?.[1];
    box.hidden = false;
    box.innerHTML = `<b>${esc(liste.find((k) => k.id === id)?.name ?? 'Kreislauf-Station')}</b> wird geöffnet …`;
    location.href = lokal ? text.replace(PAGES, new URL('../', location.href).href) : text;
    return;
  }
  box.hidden = false;
  box.innerHTML = /^https?:\/\//.test(text)
    ? `Fremder Link, nicht automatisch geöffnet:<br><a href="${esc(text)}" rel="noopener noreferrer" target="_blank">${esc(text)}</a>`
    : `Kein Link: <code>${esc(text)}</code>`;
}

async function lies() {
  if (!laeuft) return;
  if (video.readyState >= 2) {
    try { const [c] = await detektor.detect(video); if (c?.rawValue) gefunden(c.rawValue); } catch { /* nächstes Bild */ }
  }
  if (laeuft) setTimeout(lies, 150);
}
async function start() {
  try {
    detektor ??= new BarcodeDetector({ formats: ['qr_code'] });
    strom = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false });
    video.srcObject = strom;
    await video.play();
    laeuft = true;
    knopf.textContent = 'Kamera stoppen';
    document.getElementById('sucher').classList.add('an');
    lies();
  } catch (e) {
    hinweis.textContent = e.name === 'NotAllowedError' ? 'Kamera nicht erlaubt. In den Browser-Einstellungen freigeben und neu laden.' : `Kamera nicht verfügbar: ${e.message}`;
  }
}
function stopp() {
  laeuft = false;
  strom?.getTracks().forEach((t) => t.stop());
  strom = null;
  knopf.textContent = 'Kamera starten';
  document.getElementById('sucher').classList.remove('an');
}
knopf.addEventListener('click', () => (laeuft ? stopp() : start()));
addEventListener('pagehide', stopp);
