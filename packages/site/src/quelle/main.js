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
  <dl class="facts">${[[ziel ? 'Quelle' : 'Art', titel], ['Belegt', was], ['Von', von], ['Jahr', jahr], ['Seite', seite], ['Ziel', sicher ? ziel.hostname : null]]
    .filter(([, v]) => v).map(([k, v]) => `<div><dt>${k}</dt><dd>${esc(v)}</dd></div>`).join('')}</dl>
  <div class="quelle-knoepfe">
    <button class="btn ghost" id="zurueck"><span class="pfeil">←</span>Zurück</button>
    ${sicher ? `<a class="btn primary" href="${esc(ziel.href)}" rel="noopener noreferrer">Zur Quelle<span class="pfeil">→</span></a>` : ''}
  </div>
</div></section>`;
document.getElementById('zurueck').addEventListener('click', () => (history.length > 1 ? history.back() : (location.href = '../')));
