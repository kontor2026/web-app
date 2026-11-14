// Rundgang mit Mo, dem Holz-Mannequin. Erscheint beim ersten Besuch auf der Startseite (und über das Menü erneut).
// Kurz halten: eine Frage, dann vier Sprechblasen. Ein Spotlight hebt hervor, worauf Mo mit dem Arm zeigt.
import { ruhig } from './shell.js';
import { moSvg } from './mo.js';

const SCHLUESSEL = 'intro-gesehen';
// ziel: CSS-Selektor des Elements, auf das Mo zeigt (null = nichts hervorheben)
const SCHRITTE = [
  { frage: true, text: 'Hey! Dich hab ich hier noch nicht gesehen. Schön, dass dich Nachhaltigkeit interessiert. Soll ich dir kurz zeigen, wie das hier geht?' },
  { text: 'Ich bin Mo. Das hier ist eine Datenbank, die wir für einen Hackathon gebaut haben: Woraus besteht ein Gegenstand, woher kommt er, wohin geht er? Jede Zahl hat eine Quelle.', ziel: null },
  { text: 'Such dir einen Gegenstand aus. Ein Tipp auf die Karte, und du folgst seinem Weg.', ziel: '.waehler' },
  { text: 'Hier öffnest du das Menü: Lebensweg, 3D-Modelle, Werkbank und KI-Kompass.', ziel: '.menue-knopf' },
  { text: 'Alles mit › lässt sich aufklappen. „Weiter“ führt dich immer zum nächsten Schritt. Tief gehen kannst du, musst du aber nicht.', ziel: null, ende: true },
];

export function zeigeIntro({ erzwingen = false } = {}) {
  if (!erzwingen && localStorage.getItem(SCHLUESSEL)) return;
  let i = 0, tipper = 0;
  const el = document.createElement('div');
  el.className = 'rundgang';
  el.setAttribute('role', 'dialog');
  el.setAttribute('aria-modal', 'true');
  el.setAttribute('aria-label', 'Rundgang mit Mo');
  el.innerHTML = `<div class="rg-spot"></div>
    <div class="rg-karte">
      <div class="rg-mo">${moSvg()}</div>
      <div class="rg-blase">
        <p class="rg-text" aria-live="polite"></p>
        <div class="rg-punkte">${SCHRITTE.slice(1).map((_, n) => `<i data-n="${n + 1}"></i>`).join('')}</div>
        <div class="rg-knoepfe"></div>
      </div>
    </div>`;
  document.body.append(el);
  const spot = el.querySelector('.rg-spot'), karte = el.querySelector('.rg-karte'), mo = el.querySelector('.mo'), text = el.querySelector('.rg-text');
  const knoepfe = el.querySelector('.rg-knoepfe');

  const schliesse = () => {
    localStorage.setItem(SCHLUESSEL, '1');
    clearInterval(tipper);
    el.classList.add('weg');
    removeEventListener('resize', zeigeZiel);
    setTimeout(() => el.remove(), ruhig ? 0 : 300);
    document.querySelector('.beispiel')?.focus({ preventScroll: true });
  };

  // Schreibmaschine: Text erscheint Zeichen für Zeichen, Tippen auf die Blase zeigt ihn sofort ganz
  const sprich = (s) => {
    clearInterval(tipper);
    text.textContent = '';
    mo.classList.add('spricht');
    if (ruhig) { text.textContent = s; mo.classList.remove('spricht'); return; }
    let n = 0;
    tipper = setInterval(() => {
      n += 2;
      text.textContent = s.slice(0, n);
      if (n >= s.length) { clearInterval(tipper); mo.classList.remove('spricht'); }
    }, 22);
    el.querySelector('.rg-blase').onclick = () => { clearInterval(tipper); text.textContent = s; mo.classList.remove('spricht'); };
  };

  // Spotlight auf das Ziel, Arm zeigt hin, Karte liegt auf der anderen Bildschirmhälfte
  const zeigeZiel = () => {
    const s = SCHRITTE[i], ziel = s.ziel ? document.querySelector(s.ziel) : null;
    mo.style.setProperty('--arm-l', '0deg');
    mo.style.setProperty('--arm-r', '0deg');
    mo.classList.toggle('winkt', i === 0 || !!s.ende);
    if (!ziel) {
      Object.assign(spot.style, { width: '0px', height: '0px', transform: `translate(${innerWidth / 2}px, ${innerHeight / 2}px)`, opacity: '1' });
      el.classList.remove('oben');
      return;
    }
    const r = ziel.getBoundingClientRect(), pad = 8;
    Object.assign(spot.style, { width: `${r.width + 2 * pad}px`, height: `${r.height + 2 * pad}px`, transform: `translate(${r.left - pad}px, ${r.top - pad}px)`, opacity: '1' });
    el.classList.toggle('oben', r.top + r.height / 2 > innerHeight * 0.5);
    // Arm nach dem Umlegen der Karte ausrichten
    requestAnimationFrame(() => {
      const m = mo.getBoundingClientRect(), links = r.left + r.width / 2 < m.left + m.width / 2;
      const sx = m.left + ((links ? 28 : 72) / 100) * m.width, sy = m.top + (50 / 112) * m.height;
      const winkel = (Math.atan2(r.top + r.height / 2 - sy, r.left + r.width / 2 - sx) * 180) / Math.PI - 90;
      mo.style.setProperty(links ? '--arm-l' : '--arm-r', `${winkel.toFixed(0)}deg`);
    });
  };

  const zeige = () => {
    const s = SCHRITTE[i];
    el.querySelectorAll('.rg-punkte i').forEach((p) => p.classList.toggle('on', +p.dataset.n <= i));
    el.classList.toggle('frage', !!s.frage);
    knoepfe.innerHTML = s.frage
      ? '<button class="btn primary" data-ja>Ja, zeig’s mir<span class="pfeil">→</span></button><button class="btn ghost" data-nein>Nein, danke</button>'
      : `<button class="btn primary" data-weiter>${s.ende ? 'Los geht’s' : 'Weiter'}<span class="pfeil">→</span></button>${s.ende ? '' : '<button class="btn ghost" data-weg>Überspringen</button>'}`;
    knoepfe.querySelector('.primary').focus({ preventScroll: true });
    zeigeZiel();
    sprich(s.text);
  };
  const weiter = () => { if (i + 1 >= SCHRITTE.length) return schliesse(); i += 1; zeige(); };

  knoepfe.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b) return;
    if (b.hasAttribute('data-ja') || b.hasAttribute('data-weiter')) weiter();
    else if (b.hasAttribute('data-weg')) schliesse();
    else if (b.hasAttribute('data-nein')) {
      knoepfe.innerHTML = '';
      el.classList.remove('frage');
      mo.classList.remove('winkt');
      sprich('Alles klar! Du findest mich jederzeit im Menü oben links.');
      setTimeout(schliesse, 2600);
    }
  });
  addEventListener('resize', zeigeZiel);
  addEventListener('keydown', function taste(e) {
    if (!el.isConnected) return removeEventListener('keydown', taste);
    if (e.key === 'Escape') schliesse();
  });
  zeige();
}
