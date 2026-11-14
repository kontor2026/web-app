// Zwischenseite für Quellen: zeigt vor dem Verlassen, wohin der Link führt und was er belegt.
import { shell, esc, icon } from '../shell.js';
import './quelle.css';

const p = new URLSearchParams(location.search);
const url = p.get('u'), titel = p.get('t') ?? 'Quelle', was = p.get('w'), von = p.get('h'), jahr = p.get('j'), seite = p.get('s');
let ziel = null;
try { ziel = url ? new URL(url) : null; } catch { ziel = null; }
const sicher = ziel && ziel.protocol === 'https:';   // nur https-Ziele werden verlinkt

const app = shell('', '../');
app.innerHTML = `
<section class="view quelle-seite"><div class="quelle-karte">
  <p class="eyebrow">${icon(ziel ? 'beleg' : 'schaetzung')}${ziel ? 'Quelle prüfen' : 'Eigene Schätzung'}</p>
  <h1>${esc(titel)}</h1>
  ${was ? `<p class="quelle-was">${esc(was)}</p>` : ''}
  <dl class="facts">
    ${von ? `<div><dt>Von</dt><dd>${esc(von)}</dd></div>` : ''}
    ${jahr ? `<div><dt>Jahr</dt><dd>${esc(jahr)}</dd></div>` : ''}
    ${seite ? `<div><dt>Seite</dt><dd>${esc(seite)}</dd></div>` : ''}
    ${sicher ? `<div><dt>Du landest auf</dt><dd class="quelle-ziel">${esc(ziel.hostname)}</dd></div>` : ''}
  </dl>
  <div class="quelle-knoepfe">
    <button class="btn ghost" id="zurueck"><span class="pfeil">←</span>Zurück</button>
    ${sicher ? `<a class="btn primary" href="${esc(ziel.href)}" rel="noopener noreferrer">Zur Quelle<span class="pfeil">→</span></a>` : ''}
  </div>
</div></section>`;
document.getElementById('zurueck').addEventListener('click', () => (history.length > 1 ? history.back() : (location.href = '../')));
