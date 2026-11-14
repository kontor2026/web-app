// Gemeinsame Bausteine aller Seiten: Kopfzeile wie die Station (index.html: header.topbar),
// Lebensweg-Schritte mit Symbolen, Quellen-Chips, Formatierung.
import '../../../css/app.css';
import './site.css';
import { anzahl } from './werkbank.js';

export const SEITEN = [
  { id: 'start', pfad: '', name: 'Start' },
  { id: 'atlas', pfad: 'atlas/', name: 'Lebensweg' },
  { id: 'modelle', pfad: 'modelle/', name: '3D-Modelle' },
  { id: 'werkbank', pfad: 'werkbank/', name: 'Werkbank' },
  { id: 'kompass', pfad: 'kompass/', name: 'KI-Kompass' },
];

// root: relativer Weg zur Startseite ('./' auf der Startseite, '../' in den Unterseiten)
export function shell(aktiv, root) {
  document.body.insertAdjacentHTML('afterbegin', `
  <header class="topbar">
    <a class="brand" href="${root}">
      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M12 3.5v4M20.5 12h-4M12 20.5v-4M3.5 12h4"/></svg>
      <span>Kreislauf-Station</span>
    </a>
    <nav class="steps" aria-label="Bereiche">
      ${SEITEN.map((s, i) => `<a href="${root}${s.pfad}" class="${s.id === aktiv ? 'active' : ''}" ${s.id === aktiv ? 'aria-current="page"' : ''}><b>0${i}</b>${s.name}${s.id === 'werkbank' ? `<span class="zaehler" ${anzahl() ? '' : 'hidden'}>${anzahl()}</span>` : ''}</a>`).join('')}
    </nav>
    <div class="status"></div>
  </header>`);
  addEventListener('werkbank', () => { const z = document.querySelector('.steps .zaehler'); z.textContent = anzahl(); z.hidden = !anzahl(); });
  return document.getElementById('app');
}

// Der Lebensweg eines Gegenstands: sieben Stationen, überall gleich benannt und gleich gezeichnet
const ICON = {
  abbau: '<path d="M3 19 9 9l4 6 3-4 5 8Z"/>',
  verarbeitung: '<path d="M12 3c3 4 5 6.5 5 10a5 5 0 0 1-10 0c0-3 2-5.5 5-10Z"/><path d="M12 14a2 2 0 0 0 2-2"/>',
  herstellung: '<path d="M3 20V10l5 3v-3l5 3V6h5v14Z"/><path d="M7 17h2M12 17h2"/>',
  gegenstand: '<path d="m12 3 8 4.5v9L12 21l-8-4.5v-9Z"/><path d="m4 7.5 8 4.5 8-4.5M12 12v9"/>',
  werkbank: '<path d="M3 10h18v3H3zM5 13v7M19 13v7M8 10V6h8v4"/>',
  upcycling: '<path d="M14.5 5.5 18.5 9.5 9 19H5v-4Z"/><path d="m12.5 7.5 4 4"/>',
  entsorgung: '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/><path d="M10 11v6M14 11v6"/>',
  verwertung: '<path d="M20 12a8 8 0 1 1-2.3-5.7"/><path d="M20 4v4h-4"/>',
};
export const SCHRITTE = [
  { id: 'abbau', name: 'Abbau', frage: 'Woher kommen die Rohstoffe?' },
  { id: 'verarbeitung', name: 'Verarbeitung', frage: 'Wo werden sie verarbeitet?' },
  { id: 'herstellung', name: 'Herstellung', frage: 'Woher kommt das fertige Produkt?' },
  { id: 'gegenstand', name: 'Gegenstand', frage: 'Woraus besteht er?' },
  { id: 'upcycling', name: 'Upcycling', frage: 'Was kann ich daraus bauen?' },
  { id: 'entsorgung', name: 'Entsorgung', frage: 'Wohin damit?' },
  { id: 'verwertung', name: 'Verwertung', frage: 'Was passiert danach?' },
];
export const icon = (id, k = '') => `<svg class="icon ${k}" viewBox="0 0 24 24" aria-hidden="true">${ICON[id] ?? ''}</svg>`;

export const zahl = (v, s = 1) => Number(v).toLocaleString('de-DE', { maximumFractionDigits: s });
export const gramm = (g) => (g >= 1000 ? `${zahl(g / 1000)} kg` : g >= 10 ? `${zahl(g, 0)} g` : g >= 0.1 ? `${zahl(g)} g` : `${zahl(g * 1000, 0)} mg`);
export const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
export const datum = (iso) => (/^\d{4}-\d{2}-\d{2}$/.test(iso ?? '') ? iso.split('-').reverse().join('.') : iso ?? '');
export const ruhig = matchMedia('(prefers-reduced-motion: reduce)').matches || new URLSearchParams(location.search).has('static');

// ---------- Belege: jede Zahl und jede Aussage verweist auf ihre Fundstelle ----------
const REPO = 'https://github.com/kontor2026';
export const repoUrl = (pfad) => (pfad.startsWith('deployment/') ? `${REPO}/deployment/blob/main/${pfad.slice(11)}` : `${REPO}/web-app/blob/main/${pfad}`);
export const repoLink = (pfad, text = pfad) => `<a class="ql" href="${esc(repoUrl(pfad))}" target="_blank" rel="noopener">${esc(text)} →</a>`;
export const quelleUrl = (quellen, key, seite) => {
  const q = quellen[key];
  const url = q?.url ?? q?.landingpage;
  if (!url) return null;
  return seite && /\.pdf($|[?#])|format=pdf/i.test(url) ? `${url.split('#')[0]}#page=${seite}` : url;
};
export const quelleA = (quellen, key, text) => {
  const url = quelleUrl(quellen, key);
  const t = text ?? quellen[key]?.titel ?? key;
  return url ? `<a class="ql" href="${esc(url)}" target="_blank" rel="noopener">${esc(t)} →</a>` : esc(t);
};
// Kleiner Chip direkt an der Zahl: „Quelle“ (belegt) oder „Schätzung“ (eigene Annahme, mit Link auf die Datei)
export const chip = (url, titel, text = 'Quelle') =>
  url ? `<a class="chip-q" href="${esc(url)}" target="_blank" rel="noopener" title="${esc(titel ?? '')}">${esc(text)}</a>` : '';
export const schaetzung = (pfad, titel = 'Eigene Schätzung, siehe Datei') =>
  `<a class="chip-q schaetzung" href="${esc(repoUrl(pfad))}" target="_blank" rel="noopener" title="${esc(titel)}">Schätzung</a>`;
