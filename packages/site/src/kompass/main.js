// KI-Kompass: vier Richtungen für verantwortungsvollen Umgang mit KI, belegt aus dem Code (inhalt.js).
// Links eine Kompassrose als technische Zeichnung, darunter der Ablauf; rechts das Datenblatt wie im Steckbrief.
import { shell, esc, repoLink } from '../shell.js';
import { KOMPASS } from './inhalt.js';
import './kompass.css';

const WINKEL = { N: 0, O: 90, S: 180, W: 270 };
const NAME = { N: 'Norden', O: 'Osten', S: 'Süden', W: 'Westen' };
const WER = { Mensch: 'mensch', KI: 'ki', Datenbank: 'db' };
const zaehle = (w) => KOMPASS.ablauf.filter((a) => a.wer === w).length;

const app = shell('kompass', '../', `<span class="stock">Offene Punkte <b>${KOMPASS.richtungen.reduce((s, r) => s + r.offen.length, 0)}</b></span>`);

// Kompassrose: Kreise, Teilstriche alle 10°, vier Richtungen als Positionsnummern-Ballons
const striche = Array.from({ length: 36 }, (_, i) => {
  const a = (i * 10 * Math.PI) / 180, lang = i % 9 === 0 ? 16 : i % 3 === 0 ? 10 : 5;
  return `<line x1="${Math.sin(a) * 150}" y1="${-Math.cos(a) * 150}" x2="${Math.sin(a) * (150 - lang)}" y2="${-Math.cos(a) * (150 - lang)}"/>`;
}).join('');
const richtungen = KOMPASS.richtungen.map((r) => {
  const a = (WINKEL[r.himmelsrichtung] * Math.PI) / 180, x = Math.sin(a) * 178, y = -Math.cos(a) * 178;
  const lx = Math.sin(a) * 216, ly = -Math.cos(a) * 216 + (r.himmelsrichtung === 'S' ? 6 : r.himmelsrichtung === 'N' ? -2 : 4);
  const anker = r.himmelsrichtung === 'O' ? 'start' : r.himmelsrichtung === 'W' ? 'end' : 'middle';
  const lxx = r.himmelsrichtung === 'O' ? x + 30 : r.himmelsrichtung === 'W' ? x - 30 : lx;
  const lyy = r.himmelsrichtung === 'O' || r.himmelsrichtung === 'W' ? y + 5 : ly;
  return `<g class="richtung" data-id="${r.id}" tabindex="0" role="button" aria-label="${esc(r.titel)}: ${esc(r.frage)}">
    <circle class="ballon-k" cx="${x}" cy="${y}" r="20"/><text class="num" x="${x}" y="${y}">${r.himmelsrichtung}</text>
    <text class="lbl" x="${lxx}" y="${lyy}" text-anchor="${anker}">${esc(r.titel)}</text></g>`;
}).join('');

app.innerHTML = `
<section class="view sheet kompass">
  <div class="canvas">
    <div class="canvas-head">
      <div><h2>${esc(KOMPASS.titel)}</h2><p>Tippe eine Himmelsrichtung oder einen Schritt an</p></div>
    </div>
    <div class="rose-flaeche">
      <svg class="rose" viewBox="-300 -250 600 500" role="group" aria-label="Kompassrose mit vier Richtungen">
        <circle class="ring" r="150"/><circle class="ring2" r="120"/><circle class="ring2" r="60"/>
        <g class="striche">${striche}</g>
        <line class="achse" x1="-150" y1="0" x2="150" y2="0"/><line class="achse" x1="0" y1="-150" x2="0" y2="150"/>
        <g class="nadel" id="nadel"><polygon class="nord" points="0,-112 13,0 -13,0"/><polygon class="sued" points="0,112 13,0 -13,0"/><circle r="5"/></g>
        ${richtungen}
      </svg>
    </div>
    <div class="ablauf">
      <div class="eyebrow">Ablauf in der Station · wer macht was?</div>
      <ol>${KOMPASS.ablauf.map((a, i) => `<li><button data-schritt="${i}" class="schritt ${WER[a.wer]}">
        <span class="nr">${String(i + 1).padStart(2, '0')}</span><b>${esc(a.schritt)}</b><span class="wer">${esc(a.wer)}</span></button></li>`).join('')}</ol>
    </div>
  </div>
  <aside class="panel" id="panel"></aside>
  <div class="actionbar">
    <div class="q">Wer entscheidet? <span>Mensch ${zaehle('Mensch')} · KI ${zaehle('KI')} · Datenbank ${zaehle('Datenbank')} Schritte</span></div>
    <button class="btn ghost" id="zurueck">← Richtung</button>
    <button class="btn" id="weiter">Richtung →</button>
  </div>
</section>`;

const panel = document.getElementById('panel');
function setzePanel(html, crumbs) {
  panel.innerHTML = `<div class="panel-inner">${crumbs ? `<nav class="crumbs">${crumbs.map((c, i) => (i < crumbs.length - 1
    ? `<button data-c="${i}">${esc(c.label)}</button><span></span>` : `<b style="font-weight:500;color:var(--ink)">${esc(c.label)}</b>`)).join('')}</nav>` : ''}${html}</div>`;
  panel.querySelectorAll('.crumbs button').forEach((b) => b.addEventListener('click', () => crumbs[+b.dataset.c].go()));
  panel.querySelectorAll('[data-r]').forEach((b) => b.addEventListener('click', () => (location.hash = b.dataset.r)));
  panel.scrollTop = 0;
}
const beleg = (b) => `<span class="beleg">${repoLink(b)}</span>`;
const start = { label: 'KI-Kompass', go: () => (location.hash = '') };

function uebersicht() {
  markiere(null);
  setzePanel(`
    <div><div class="eyebrow">Verantwortungsvoller Umgang mit KI</div><h1 style="margin-top:8px">${esc(KOMPASS.frage)}</h1>
      <p class="sub">${esc(KOMPASS.einleitung)}</p></div>
    <div><h3>Vier Richtungen · tippe eine an</h3><div class="plist">${KOMPASS.richtungen.map((r) => `
      <button class="prow" data-r="${r.id}"><span class="n">${r.himmelsrichtung}</span>
        <span>${esc(r.titel)}<small>${esc(r.frage)}</small></span><span class="m">${r.offen.length} offen →</span></button>`).join('')}</div></div>
    <div><h3>Bevor du selbst KI nutzt</h3><ol class="howto">${KOMPASS.checkliste.map((c) => `<li>${esc(c)}</li>`).join('')}</ol></div>
    <div><h3>Zum Nachlesen</h3><div class="quellen">${KOMPASS.quellen.map((q) => `<a href="${esc(q.url)}" target="_blank" rel="noopener">${esc(q.titel)} →</a>`).join('')}</div></div>
    <p class="source">Jede Aussage im Kompass ist mit der Datei belegt, aus der sie stammt.</p>`, null);
}

function richtung(r) {
  markiere(r);
  setzePanel(`
    <div><div class="eyebrow">${r.himmelsrichtung} · ${NAME[r.himmelsrichtung]}</div><h1 style="margin-top:8px">${esc(r.titel)}</h1>
      <p class="sub">${esc(r.frage)}</p></div>
    <div><h3>So machen wir es</h3><dl class="belege">${r.so_machen_wirs.map((s) => `<div><dd>${esc(s.text)}</dd>${beleg(s.beleg)}</div>`).join('')}</dl></div>
    <div><h3>Noch offen</h3><div class="pruef">${r.offen.map((o) => `<p class="note warn">${esc(o)}</p>`).join('')}</div></div>
    <div class="goal"><small>Tipp für dich</small>${esc(r.tipp_fuer_dich)}</div>`, [start, { label: r.titel, go: () => richtung(r) }]);
}

function schritt(i) {
  const a = KOMPASS.ablauf[i];
  markiere(null, i);
  setzePanel(`
    <div><div class="eyebrow">Schritt ${String(i + 1).padStart(2, '0')} von ${KOMPASS.ablauf.length}</div><h1 style="margin-top:8px">${esc(a.schritt)}</h1>
      <p class="sub"><span class="schritt-wer ${WER[a.wer]}">${esc(a.wer)}</span></p></div>
    <p>${esc(a.text)}</p>
    <p class="source">Beleg: ${beleg(a.beleg)}</p>
    <div class="row-knoepfe">
      ${i > 0 ? `<button class="btn ghost" data-s="${i - 1}">← ${esc(KOMPASS.ablauf[i - 1].schritt)}</button>` : ''}
      ${i < KOMPASS.ablauf.length - 1 ? `<button class="btn" data-s="${i + 1}">${esc(KOMPASS.ablauf[i + 1].schritt)} →</button>` : ''}
    </div>`, [start, { label: `Schritt ${i + 1}`, go: () => schritt(i) }]);
  panel.querySelectorAll('[data-s]').forEach((b) => b.addEventListener('click', () => (location.hash = `schritt-${+b.dataset.s + 1}`)));
}

function markiere(r, s = null) {
  document.getElementById('nadel').style.transform = `rotate(${r ? WINKEL[r.himmelsrichtung] : 0}deg)`;
  document.querySelectorAll('.richtung').forEach((g) => g.classList.toggle('sel', g.dataset.id === r?.id));
  document.querySelector('.rose').classList.toggle('has-sel', !!r);
  document.querySelectorAll('.schritt').forEach((b) => b.classList.toggle('sel', +b.dataset.schritt === s));
}

document.querySelectorAll('.richtung').forEach((g) => {
  const los = () => (location.hash = g.dataset.id);
  g.addEventListener('click', los);
  g.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); los(); } });
});
document.querySelectorAll('.schritt').forEach((b) => b.addEventListener('click', () => (location.hash = `schritt-${+b.dataset.schritt + 1}`)));
const ids = KOMPASS.richtungen.map((r) => r.id);
const dreh = (d) => { const i = ids.indexOf(location.hash.slice(1)); location.hash = ids[(i + d + ids.length) % ids.length]; };
document.getElementById('zurueck').addEventListener('click', () => dreh(-1));
document.getElementById('weiter').addEventListener('click', () => dreh(1));

function ausHash() {
  const h = location.hash.slice(1), r = KOMPASS.richtungen.find((x) => x.id === h), s = h.match(/^schritt-(\d+)$/);
  if (r) richtung(r); else if (s && KOMPASS.ablauf[s[1] - 1]) schritt(s[1] - 1); else uebersicht();
}
addEventListener('hashchange', ausHash);
ausHash();
