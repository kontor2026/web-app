// KI-Kompass: vier Richtungen für verantwortungsvollen Umgang mit KI, belegt aus dem Code (inhalt.js).
// Links eine Kompassrose als technische Zeichnung, darunter der Ablauf; rechts das Datenblatt wie im Steckbrief.
import { shell, esc, chip, repoUrl } from '../shell.js';
import { KOMPASS } from './inhalt.js';
import './kompass.css';

const WINKEL = { N: 0, O: 90, S: 180, W: 270 };
const NAME = { N: 'Norden', O: 'Osten', S: 'Süden', W: 'Westen' };
const WER = { Mensch: 'mensch', KI: 'ki', Datenbank: 'db' };
const zaehle = (w) => KOMPASS.ablauf.filter((a) => a.wer === w).length;

const app = shell('kompass', '../');

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
    <nav class="lw-schritte kompass-schritte" aria-label="Richtungen">${KOMPASS.richtungen.map((r) => `
      <a href="#${r.id}" data-id="${r.id}" title="${esc(r.titel)}"><span class="lw-nr">${r.himmelsrichtung}</span><span class="lw-name">${esc(r.titel)}</span></a>`).join('')}</nav>
    <h1 class="lw-frage" id="frage"></h1>
    <div class="rose-flaeche">
      <svg class="rose" viewBox="-300 -250 600 500" role="group" aria-label="Kompassrose mit vier Richtungen">
        <circle class="ring" r="150"/><circle class="ring2" r="120"/><circle class="ring2" r="60"/>
        <g class="striche">${striche}</g>
        <line class="achse" x1="-150" y1="0" x2="150" y2="0"/><line class="achse" x1="0" y1="-150" x2="0" y2="150"/>
        <g class="nadel" id="nadel" style="transform: rotate(45deg)"><polygon class="nord" points="0,-112 13,0 -13,0"/><polygon class="sued" points="0,112 13,0 -13,0"/><circle r="5"/></g>
        ${richtungen}
      </svg>
    </div>
    <details class="ablauf lw-block" id="ablauf"><summary>Ablauf</summary>
      <ol>${KOMPASS.ablauf.map((a, i) => `<li><button data-schritt="${i}" class="schritt ${WER[a.wer]}">
        <span class="nr">${String(i + 1).padStart(2, '0')}</span><b>${esc(a.schritt)}</b><span class="wer">${esc(a.wer)}</span></button></li>`).join('')}</ol>
    </details>
  </div>
  <aside class="panel" id="panel"></aside>
</section>`;

const panel = document.getElementById('panel');
if (matchMedia('(min-width: 901px)').matches) document.getElementById('ablauf').open = true;
function setzePanel(html, crumbs) {
  panel.innerHTML = `<div class="panel-inner">${crumbs ? `<nav class="crumbs">${crumbs.map((c, i) => (i < crumbs.length - 1
    ? `<button data-c="${i}">${esc(c.label)}</button><span></span>` : `<b style="font-weight:500;color:var(--ink)">${esc(c.label)}</b>`)).join('')}</nav>` : ''}${html}</div>`;
  panel.querySelectorAll('.crumbs button').forEach((b) => b.addEventListener('click', () => crumbs[+b.dataset.c].go()));
  panel.querySelectorAll('[data-r]').forEach((b) => b.addEventListener('click', () => (location.hash = b.dataset.r)));
  panel.scrollTop = 0;
}
const beleg = () => '';   // Belege bleiben in inhalt.js nachvollziehbar, werden aber nicht angezeigt
const start = { label: 'KI-Kompass', go: () => (location.hash = '') };

function uebersicht() {
  markiere(null);
  setzePanel(`
    <div><h3>Vier Richtungen</h3><div class="plist">${KOMPASS.richtungen.map((r) => `
      <button class="prow" data-r="${r.id}"><span class="n">${r.himmelsrichtung}</span>
        <span>${esc(r.titel)}<small>${esc(r.frage)}</small></span><span class="m">→</span></button>`).join('')}</div></div>
    <p class="kompass-quellen">${KOMPASS.quellen.map((q) => chip(q.url, q.titel, q.titel.split(' (')[0].replace('EU-Gesetz über KI', 'KI-Verordnung').replace('EU-Gesetz zum Datenschutz', 'DSGVO').split(':')[0], { was: q.titel })).join('')}</p>
`, null);
}

function richtung(r) {
  markiere(r);
  setzePanel(`
    <p class="kompass-kern">${esc(r.so_machen_wirs[0]?.text ?? '')}</p>
    <p class="goal">${esc(r.tipp_fuer_dich)}</p>`, null);
}

function schritt(i) {
  const a = KOMPASS.ablauf[i];
  markiere(null, i);
  setzePanel(`
    <div><div class="eyebrow">Schritt ${String(i + 1).padStart(2, '0')} von ${KOMPASS.ablauf.length}</div><h1 style="margin-top:8px">${esc(a.schritt)}</h1>
      <p class="sub"><span class="schritt-wer ${WER[a.wer]}">${esc(a.wer)}</span></p></div>
    <p>${esc(a.text)}</p>
    <p class="source">${beleg(a.beleg)}</p>
    <div class="row-knoepfe">
      ${i > 0 ? `<button class="btn ghost" data-s="${i - 1}">← ${esc(KOMPASS.ablauf[i - 1].schritt)}</button>` : ''}
      ${i < KOMPASS.ablauf.length - 1 ? `<button class="btn" data-s="${i + 1}">${esc(KOMPASS.ablauf[i + 1].schritt)} →</button>` : ''}
    </div>`, [start, { label: `Schritt ${i + 1}`, go: () => schritt(i) }]);
  panel.querySelectorAll('[data-s]').forEach((b) => b.addEventListener('click', () => (location.hash = `schritt-${+b.dataset.s + 1}`)));
}

let nadelWinkel = 45;
function markiere(r, s = null) {
  // Nadel dreht immer auf kürzestem Weg; ohne Auswahl zeigt sie zwischen zwei Richtungen (45°), damit jede Wahl sichtbar ausschlägt
  const ziel = r ? WINKEL[r.himmelsrichtung] : 45;
  nadelWinkel += ((((ziel - nadelWinkel) % 360) + 540) % 360) - 180;
  document.getElementById('nadel').style.transform = `rotate(${nadelWinkel}deg)`;
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


// Oben Ort und Frage, unten nur „Weiter“ zur nächsten Richtung (wie im Lebensweg)
function fuss() {
  const i = ids.indexOf(location.hash.slice(1)), n = ids.length;
  document.querySelectorAll('.kompass-schritte a').forEach((a) => { const on = a.dataset.id === ids[i]; a.classList.toggle('on', on); a.toggleAttribute('aria-current', on); });
  document.getElementById('frage').textContent = i < 0 ? KOMPASS.frage : KOMPASS.richtungen[i].frage;
  const nach = KOMPASS.richtungen[(i + 1) % n];
  document.querySelector('#panel .panel-inner')?.insertAdjacentHTML('beforeend',
    `<a class="lw-weiter" href="#${nach.id}"><span class="lw-nr">${nach.himmelsrichtung}</span><span>Weiter: ${esc(nach.titel)}</span><span class="pfeil">→</span></a>`);
}
function ausHash() {
  const h = location.hash.slice(1), r = KOMPASS.richtungen.find((x) => x.id === h), s = h.match(/^schritt-(\d+)$/);
  if (r) richtung(r); else if (s && KOMPASS.ablauf[s[1] - 1]) schritt(s[1] - 1); else uebersicht();
  fuss();   // nach dem Datenblatt, damit „Weiter“ angehängt wird
}
addEventListener('hashchange', ausHash);
ausHash();
