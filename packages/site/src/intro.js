// Kurze Einführung beim ersten Besuch: drei Karten, ein Satz je Karte, wischen oder „Weiter“.
// Erscheint nur einmal (localStorage); „Wie funktioniert’s?“ auf der Startseite öffnet sie wieder.
import { esc, icon, ruhig } from './shell.js';

const KARTEN = [
  { bild: 'kreis', titel: 'Jeder Gegenstand hat einen Weg.', text: 'Vom Rohstoff in der Erde bis zum Recycling.' },
  { bild: 'gegenstand', titel: 'Tippe einen Gegenstand an.', text: 'Folge ihm Schritt für Schritt. Jede Zahl hat eine Quelle.' },
  { bild: 'werkbank', titel: 'Sammle, was du hast.', text: 'Die Werkbank zeigt, was du daraus bauen kannst.' },
];
const SCHLUESSEL = 'intro-gesehen';

// Mini-Kreis mit sieben Punkten als Bild der ersten Karte
const kreisBild = () => `<svg viewBox="-60 -60 120 120" class="intro-kreis" aria-hidden="true"><circle r="44" fill="none" stroke="currentColor" stroke-width="1.2"/>
  ${Array.from({ length: 7 }, (_, i) => { const a = (i / 7) * Math.PI * 2 - Math.PI / 2; return `<circle cx="${(Math.cos(a) * 44).toFixed(1)}" cy="${(Math.sin(a) * 44).toFixed(1)}" r="7" class="${i === 3 ? 'an' : ''}"/>`; }).join('')}</svg>`;

export function zeigeIntro({ erzwingen = false } = {}) {
  if (!erzwingen && localStorage.getItem(SCHLUESSEL)) return;
  let i = 0;
  const el = document.createElement('div');
  el.className = 'intro';
  el.setAttribute('role', 'dialog');
  el.setAttribute('aria-modal', 'true');
  el.setAttribute('aria-label', 'Kurze Einführung');
  el.innerHTML = `<div class="intro-karte">
    <div class="intro-buehne">${KARTEN.map((k, n) => `<section class="intro-seite" data-n="${n}">
      <div class="intro-bild">${k.bild === 'kreis' ? kreisBild() : icon(k.bild)}</div>
      <h2>${esc(k.titel)}</h2><p>${esc(k.text)}</p></section>`).join('')}</div>
    <div class="intro-punkte">${KARTEN.map((_, n) => `<i data-n="${n}"></i>`).join('')}</div>
    <div class="intro-knoepfe"><button class="btn ghost" data-weg>Überspringen</button><button class="btn primary" data-weiter></button></div>
  </div>`;
  document.body.append(el);
  const zeige = () => {
    el.querySelectorAll('.intro-seite').forEach((s) => s.classList.toggle('on', +s.dataset.n === i));
    el.querySelectorAll('.intro-punkte i').forEach((p) => p.classList.toggle('on', +p.dataset.n === i));
    el.querySelector('[data-weiter]').innerHTML = i < KARTEN.length - 1 ? 'Weiter<span class="pfeil">→</span>' : 'Los geht’s<span class="pfeil">→</span>';
  };
  const schliesse = () => {
    localStorage.setItem(SCHLUESSEL, '1');
    el.classList.add('weg');
    setTimeout(() => el.remove(), ruhig ? 0 : 250);
    document.querySelector('.suche-feld')?.focus();
  };
  const gehe = (d) => { if (i + d >= KARTEN.length) return schliesse(); i = Math.max(0, i + d); zeige(); };
  el.querySelector('[data-weiter]').addEventListener('click', () => gehe(1));
  el.querySelector('[data-weg]').addEventListener('click', schliesse);
  addEventListener('keydown', function taste(e) {
    if (!el.isConnected) return removeEventListener('keydown', taste);
    if (e.key === 'ArrowRight' || e.key === 'Enter') gehe(1);
    if (e.key === 'ArrowLeft') gehe(-1);
    if (e.key === 'Escape') schliesse();
  });
  // Wischen
  let x0 = null;
  el.addEventListener('touchstart', (e) => { x0 = e.touches[0].clientX; }, { passive: true });
  el.addEventListener('touchend', (e) => { if (x0 == null) return; const dx = e.changedTouches[0].clientX - x0; x0 = null; if (Math.abs(dx) > 50) gehe(dx < 0 ? 1 : -1); }, { passive: true });
  zeige();
  el.querySelector('[data-weiter]').focus();
}
