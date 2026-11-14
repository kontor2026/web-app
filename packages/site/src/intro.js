// Rundgang mit Mo, dem Holz-Mannequin. Sechs Schritte, ein Durchgang über Start und Lebensweg:
// Mo fragt, erzählt die Eckdaten (echte Zahlen aus der Datenbank) und lässt dich dann selbst tippen:
// Das Ziel leuchtet, alles andere ist gesperrt. Der Schritt wird in sessionStorage gemerkt und überlebt den Seitenwechsel.
import { ruhig } from './shell.js';
import { moSvg } from './mo.js';

const GESEHEN = 'intro-gesehen', LAUFT = 'rundgang-schritt';
const z = (n) => n.toLocaleString('de-DE');
// seite: auf welcher Seite der Schritt läuft; ziel: Selektor, auf den getippt werden muss (tap) oder der nur leuchtet
const SCHRITTE = [
  { seite: 'start', frage: true, text: () => 'Hey! Dich hab ich hier noch nicht gesehen. Schön, dass dich Nachhaltigkeit interessiert. Soll ich dir kurz zeigen, wie das hier geht?' },
  { seite: 'start', weiter: true, text: (d) => `Ich bin Mo. Das hier ist eine Datenbank für einen Hackathon: ${z(d.objekte)} Alltagsgegenstände, ${z(d.rohstoffe)} Rohstoffe, ${z(d.rezepte)} Bauideen. Jede Zahl hat eine Quelle.` },
  { seite: 'start', tap: true, ziel: '.beispiel[href*="smartphone"]', text: () => 'Probieren wir’s aus: Tipp auf das Smartphone. Ich zeig dir, wo es herkommt.' },
  { seite: 'atlas', tap: true, ziel: '.lw-schritte a:nth-child(4)', text: () => 'Das ist sein Lebensweg in sieben Stationen, vom Rohstoff bis zum Recycling. Tipp oben aufs Würfel-Symbol: Woraus besteht es?' },
  { seite: 'atlas', tap: true, ziel: '.menue-knopf', text: () => 'So sieht er zerlegt aus. Jede Zahl hat einen Quellen-Link, alles mit › klappt auf. Jetzt tipp aufs Menü.' },
  { seite: 'atlas', weiter: true, ende: true, ziel: '.steps a:nth-child(5)', verzoegert: 400, text: (d) => `Die Werkbank sammelt deine Gegenstände und zeigt, was du daraus bauen kannst (${z(d.rezepte)} Bauideen). Der Rest ist deins. Viel Spaß!` },
];

export function zeigeIntro({ seite, zahlen, erzwingen = false }) {
  const gespeichert = sessionStorage.getItem(LAUFT);
  let i = gespeichert == null ? null : +gespeichert;
  if (i == null) {
    if (seite !== 'start' || (!erzwingen && localStorage.getItem(GESEHEN))) return;
    i = 0;
  }
  if (!SCHRITTE[i] || SCHRITTE[i].seite !== seite) { sessionStorage.removeItem(LAUFT); return; }

  let tipper = 0, suche = 0, zielEl = null;
  const el = document.createElement('div');
  el.className = 'rundgang';
  el.setAttribute('role', 'dialog');
  el.setAttribute('aria-label', 'Rundgang mit Mo');
  el.innerHTML = `<div class="rg-block"></div><div class="rg-spot"></div>
    <div class="rg-karte">
      <div class="rg-mo">${moSvg()}</div>
      <div class="rg-blase"><p class="rg-text" aria-live="polite"></p><div class="rg-punkte">${SCHRITTE.slice(1).map((_, n) => `<i data-n="${n + 1}"></i>`).join('')}</div><div class="rg-knoepfe"></div></div>
    </div>`;
  document.body.append(el);
  const [block, spot, mo, text, knoepfe, blase] = ['.rg-block', '.rg-spot', '.mo', '.rg-text', '.rg-knoepfe', '.rg-blase'].map((s) => el.querySelector(s));

  const ende = () => {
    sessionStorage.removeItem(LAUFT);
    localStorage.setItem(GESEHEN, '1');
    clearInterval(tipper); clearInterval(suche);
    document.removeEventListener('click', beiTipp, true);
    removeEventListener('resize', ausrichten);
    document.body.classList.remove('menue-offen');
    el.classList.add('weg');
    setTimeout(() => el.remove(), ruhig ? 0 : 300);
  };

  const sprich = (s) => {
    clearInterval(tipper);
    text.textContent = '';
    if (ruhig) { text.textContent = s; return; }
    mo.classList.add('spricht');
    let n = 0;
    tipper = setInterval(() => { n += 2; text.textContent = s.slice(0, n); if (n >= s.length) { clearInterval(tipper); mo.classList.remove('spricht'); } }, 20);
    blase.onclick = () => { clearInterval(tipper); text.textContent = s; mo.classList.remove('spricht'); };
  };

  // Loch in der Sperrschicht genau über dem Ziel: nur dort kommen Tipps durch
  const ausrichten = () => {
    const s = SCHRITTE[i];
    mo.style.setProperty('--arm-l', '0deg'); mo.style.setProperty('--arm-r', '0deg');
    if (!zielEl?.isConnected) {
      Object.assign(spot.style, { width: '0px', height: '0px', transform: `translate(${innerWidth / 2}px, ${innerHeight / 2}px)` });
      block.style.clipPath = 'none';
      el.classList.remove('oben', 'leuchtet');
      return;
    }
    const r = zielEl.getBoundingClientRect(), p = 8, x = r.left - p, y = r.top - p, w = r.width + 2 * p, h = r.height + 2 * p;
    Object.assign(spot.style, { width: `${w}px`, height: `${h}px`, transform: `translate(${x}px, ${y}px)` });
    block.style.clipPath = s.tap ? `polygon(evenodd, 0 0, 100% 0, 100% 100%, 0 100%, 0 0, ${x}px ${y}px, ${x}px ${y + h}px, ${x + w}px ${y + h}px, ${x + w}px ${y}px, ${x}px ${y}px)` : 'none';
    el.classList.toggle('leuchtet', !!s.tap);
    el.classList.toggle('oben', r.top + r.height / 2 > innerHeight * 0.5);
    requestAnimationFrame(() => {
      const m = mo.getBoundingClientRect(), links = r.left + r.width / 2 < m.left + m.width / 2;
      const sx = m.left + ((links ? 29 : 71) / 100) * m.width, sy = m.top + (52 / 112) * m.height;
      const winkel = (Math.atan2(r.top + r.height / 2 - sy, r.left + r.width / 2 - sx) * 180) / Math.PI - 90;
      mo.style.setProperty(links ? '--arm-l' : '--arm-r', `${winkel.toFixed(0)}deg`);
    });
  };

  // Tipp aufs Ziel: Schritt merken (die Seite kann gleich wechseln), danach weiter
  const beiTipp = (e) => {
    const s = SCHRITTE[i];
    if (!s.tap || !zielEl || !zielEl.contains(e.target)) return;
    sessionStorage.setItem(LAUFT, String(i + 1));
    setTimeout(() => { if (el.isConnected) gehe(i + 1); }, 60);
  };
  document.addEventListener('click', beiTipp, true);

  function gehe(n) {
    if (n >= SCHRITTE.length) return ende();
    i = n;
    sessionStorage.setItem(LAUFT, String(i));
    if (SCHRITTE[i].seite !== seite) {  // läuft auf der nächsten Seite weiter (dort liest zeigeIntro den gemerkten Schritt)
      clearInterval(tipper); clearInterval(suche); document.removeEventListener('click', beiTipp, true); removeEventListener('resize', ausrichten); el.remove(); return;
    }
    const s = SCHRITTE[i];
    zielEl = null;
    el.querySelectorAll('.rg-punkte i').forEach((p) => p.classList.toggle('on', +p.dataset.n <= i));
    el.classList.toggle('frage', !!s.frage);
    mo.classList.toggle('winkt', !!s.frage || !!s.ende);
    knoepfe.innerHTML = s.frage ? '<button class="btn primary" data-ja>Ja, zeig’s mir<span class="pfeil">→</span></button><button class="btn ghost" data-nein>Nein, danke</button>'
      : s.tap ? '<p class="rg-hinweis"><i></i>Tipp auf das leuchtende Feld</p><button class="btn ghost" data-weg>Beenden</button>'
      : `<button class="btn primary" data-weiter>${s.ende ? 'Los geht’s' : 'Weiter'}<span class="pfeil">→</span></button>${s.ende ? '' : '<button class="btn ghost" data-weg>Beenden</button>'}`;
    knoepfe.querySelector('.primary')?.focus({ preventScroll: true });
    sprich(s.text(zahlen));
    ausrichten();
    clearInterval(suche);
    if (s.ziel) {
      let versuche = 0;
      suche = setInterval(() => {
        const t = document.querySelector(s.ziel);
        if (t && t.getBoundingClientRect().width > 0) { clearInterval(suche); setTimeout(() => { zielEl = t; ausrichten(); }, s.verzoegert ?? 0); }
        else if (++versuche > 40) { clearInterval(suche); ende(); }
      }, 120);
      if (s.ende) document.body.classList.add('menue-offen');
    }
  }

  knoepfe.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b) return;
    if (b.hasAttribute('data-ja') || b.hasAttribute('data-weiter')) gehe(i + 1);
    else if (b.hasAttribute('data-weg')) ende();
    else if (b.hasAttribute('data-nein')) {
      knoepfe.innerHTML = ''; mo.classList.remove('winkt');
      sprich('Alles klar! Du findest mich jederzeit im Menü oben links.');
      setTimeout(ende, 2600);
    }
  });
  addEventListener('resize', ausrichten);
  gehe(i);
}
