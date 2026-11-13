// Gemeinsame Kopfzeile aller Seiten, gleiches Markup wie die Station (index.html: header.topbar).
import '../../../css/app.css';
import './site.css';

export const SEITEN = [
  { id: 'start', pfad: '', name: 'Übersicht' },
  { id: 'atlas', pfad: 'atlas/', name: 'Rohstoff-Atlas' },
  { id: 'modelle', pfad: 'modelle/', name: '3D-Modelle' },
  { id: 'kompass', pfad: 'kompass/', name: 'KI-Kompass' },
];

// root: relativer Weg zur Startseite ('./' auf der Startseite, '../' in den Unterseiten)
export function shell(aktiv, root, status = '') {
  document.body.insertAdjacentHTML('afterbegin', `
  <header class="topbar">
    <a class="brand" href="${root}">
      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M12 3.5v4M20.5 12h-4M12 20.5v-4M3.5 12h4"/></svg>
      <span>Kreislauf-Station</span>
    </a>
    <nav class="steps" aria-label="Bereiche">
      ${SEITEN.map((s, i) => `<a href="${root}${s.pfad}" class="${s.id === aktiv ? 'active' : ''}" ${s.id === aktiv ? 'aria-current="page"' : ''}><b>0${i}</b>${s.name}</a>`).join('')}
    </nav>
    <div class="status">${status}</div>
  </header>`);
  return document.getElementById('app');
}

export const zahl = (v, s = 1) => Number(v).toLocaleString('de-DE', { maximumFractionDigits: s });
export const gramm = (g) => (g >= 1000 ? `${zahl(g / 1000)} kg` : g >= 10 ? `${zahl(g, 0)} g` : g >= 0.1 ? `${zahl(g)} g` : `${zahl(g * 1000, 0)} mg`);
export const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
// Quellen immer verlinkt: Zitate aus data/rohstoffe/quellen.json und Dateien im Repo auf GitHub
const REPO = 'https://github.com/kontor2026';
export const repoLink = (pfad, text = pfad) => {
  const url = pfad.startsWith('deployment/') ? `${REPO}/deployment/blob/main/${pfad.slice(11)}` : `${REPO}/web-app/blob/main/${pfad}`;
  return `<a class="ql" href="${esc(url)}" target="_blank" rel="noopener">${esc(text)} →</a>`;
};
export const quelleA = (quellen, key, text) => {
  const q = quellen[key];
  if (!q) return esc(text ?? key);
  const url = q.url ?? q.landingpage;
  return url ? `<a class="ql" href="${esc(url)}" target="_blank" rel="noopener">${esc(text ?? q.titel)} →</a>` : esc(text ?? q.titel);
};
export const ruhig = matchMedia('(prefers-reduced-motion: reduce)').matches || new URLSearchParams(location.search).has('static');
