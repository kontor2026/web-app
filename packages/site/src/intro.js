// Rundgang mit Mo, dem Holz-Mannequin. Sechs Schritte, und ab Schritt 2 macht man alles selbst:
// Mo sagt, wohin; das Ziel pulsiert, alles andere ist gesperrt; erst der echte Tipp (oder das Drehen am Globus) führt weiter.
// Der Rundgang läuft über zwei Seiten (Start → Lebensweg); der Schritt steht in sessionStorage und überlebt den Seitenwechsel.
import { ruhig } from './shell.js';
import { moSvg, SCHULTER } from './mo.js';

const GESEHEN = 'intro-gesehen', LAUFT = 'rundgang-schritt';
const handy = matchMedia('(max-width: 900px)');
const z = (n) => Number(n).toLocaleString('de-DE');

// art: 'frage' (Ja/Nein), 'tipp' (Ziel antippen), 'wisch' (im Ziel ziehen), 'fertig' (Knopf zum Schluss)
// text(zahlen, info): info() kommt von der Seite und kennt den gewählten Gegenstand
const SCHRITTE = [
  { seite: 'start', art: 'frage',
    text: () => 'Hey, dich hab ich hier noch nie gesehen! Ich bin Mo. Das hier ist unsere Hackathon-Datenbank zum Anfassen. Kurze Tour? Dauert 30 Sekunden.' },
  { seite: 'start', art: 'tipp', ziel: '.start .beispiele', finger: '.beispiel',
    text: (d) => `Hier drin: ${z(d.objekte)} Alltagsdinge, ${z(d.rohstoffe)} Rohstoffe, ${z(d.rezepte)} Bauideen. Jede Zahl mit Quelle. Such dir eins aus!` },
  { seite: 'atlas', art: 'wisch', ziel: '.lw[data-schritt="abbau"] .lw-globus',
    text: (d, i) => i.land ? `Station 1, Abbau. ${i.rohstoff}: Top-Lieferant ist ${i.land} mit ${i.prozent} %. Dreh mal die Erde!`
      : `Station 1: Abbau. Hier siehst du, woher die Rohstoffe kommen. Dreh mal die Erde!` },
  { seite: 'atlas', art: 'tipp', ziel: '.lw-schritte a[data-s="gegenstand"]',
    text: () => 'Oben stehen alle 7 Stationen seines Lebens, vom Abbau bis zum Recycling. Tipp auf den Würfel: Da nehmen wir es auseinander.' },
  { seite: 'atlas', art: 'zeige', ziel: '.lw[data-schritt="gegenstand"] .panel-inner .lw-block > summary',
    text: (d, i) => `${i.teile ? `${i.teile} Teile, ${i.gramm}. ` : ''}Hier könntest du tippen: Alles mit dem Pfeil › klappt auf und zeigt dir mehr, z. B. jedes Teil mit Material.` },
  { seite: 'atlas', art: 'tipp', ende: true, ziel: () => (handy.matches ? '.menue-knopf' : '.steps'),
    text: () => 'Werkbank, 3D-Modelle, KI-Kompass: alles im Menü. Tipp drauf, ab jetzt gehört die Seite dir!' },
];
const ABSCHIED = 'Viel Spaß beim Stöbern!';

export function zeigeIntro({ seite, zahlen, info = () => ({}), erzwingen = false }) {
  const gespeichert = sessionStorage.getItem(LAUFT);
  let i = gespeichert == null ? null : +gespeichert;
  if (i == null) {
    if (seite !== 'start' || (!erzwingen && (localStorage.getItem(GESEHEN) || !handy.matches))) return;
    i = 0;
  }
  if (!SCHRITTE[i] || SCHRITTE[i].seite !== seite) { sessionStorage.removeItem(LAUFT); return; }

  const el = document.createElement('div');
  el.className = 'rundgang';
  el.setAttribute('role', 'dialog');
  el.setAttribute('aria-label', 'Rundgang mit Mo');
  el.innerHTML = `<div class="rg-block"></div><div class="rg-spot"></div><div class="rg-finger"><i></i></div>
    <div class="rg-karte rein">
      <div class="rg-mo">${moSvg()}</div>
      <div class="rg-blase">
        <p class="rg-text" aria-live="polite"></p>
        <div class="rg-fuss"><div class="rg-punkte">${SCHRITTE.slice(1).map((_, n) => `<i data-n="${n + 1}"></i>`).join('')}</div><button class="rg-weg" type="button">Überspringen</button></div>
        <div class="rg-knoepfe"></div>
      </div>
    </div>`;
  document.body.append(el);
  const $ = (s) => el.querySelector(s);
  const block = $('.rg-block'), spot = $('.rg-spot'), finger = $('.rg-finger'), mo = $('.mo'), text = $('.rg-text'), knoepfe = $('.rg-knoepfe'), blase = $('.rg-blase'), karte = $('.rg-karte');
  let tipper = 0, suche = 0, zielEl = null, fertigText = '';

  const aufraeumen = () => {
    clearInterval(tipper); clearInterval(suche);
    document.removeEventListener('click', beiTipp, true);
    document.removeEventListener('pointerdown', beiDruck, true);
    document.removeEventListener('pointerup', beiLos, true);
    removeEventListener('resize', ausrichten);
    removeEventListener('scroll', ausrichten, true);
  };
  const ende = (gruss) => {
    sessionStorage.removeItem(LAUFT);
    localStorage.setItem(GESEHEN, '1');
    aufraeumen();
    if (!gruss) { el.classList.add('weg'); return setTimeout(() => el.remove(), ruhig ? 0 : 320); }
    // Zum Abschied winkt Mo noch kurz, sperrt aber nichts mehr
    zielEl = null; ausrichten();
    el.classList.add('abschied'); el.classList.remove('leuchtet', 'frage');
    knoepfe.innerHTML = '';
    mo.classList.add('winkt'); setzeArme(null);
    sprich(gruss);
    setTimeout(() => { el.classList.add('weg'); setTimeout(() => el.remove(), 320); }, 2200);
  };

  // Text erscheint Buchstabe für Buchstabe, Mo bewegt dabei den Mund; Tipp auf die Blase zeigt alles sofort
  const sprich = (s) => {
    clearInterval(tipper);
    fertigText = s;
    if (ruhig) { text.textContent = s; return; }
    text.textContent = '';
    mo.classList.add('spricht');
    let n = 0;
    tipper = setInterval(() => {
      n += 1; text.textContent = s.slice(0, n);
      if (n >= s.length) { clearInterval(tipper); mo.classList.remove('spricht'); }
    }, 17);
  };
  blase.addEventListener('click', (e) => {
    if (e.target.closest('button')) return;
    clearInterval(tipper); text.textContent = fertigText; mo.classList.remove('spricht');
  });

  // Mo zeigt mit dem näheren Arm aufs Ziel, dreht den Kopf ein wenig mit und schaut hin
  const setzeArme = (r) => {
    const s = mo.style;
    ['--arm-l', '--arm-r', '--ell-l', '--ell-r', '--kopf', '--blick-x', '--blick-y'].forEach((v) => s.removeProperty(v));
    if (!r) return;
    const m = mo.getBoundingClientRect(), k = m.width / 120;
    const zx = r.left + r.width / 2, zy = r.top + r.height / 2;
    const seite = zx < m.left + 60 * k ? 'l' : 'r';
    const sx = m.left + SCHULTER[seite][0] * k, sy = m.top + SCHULTER[seite][1] * k;
    const dx = zx - sx, dy = zy - sy, laenge = Math.hypot(dx, dy) || 1;
    const winkel = (Math.atan2(-dx, dy) * 180) / Math.PI;
    s.setProperty(`--arm-${seite}`, `${winkel.toFixed(1)}deg`);
    s.setProperty(`--ell-${seite}`, `${seite === 'l' ? 8 : -8}deg`);
    s.setProperty('--kopf', `${Math.max(-9, Math.min(9, (dx / laenge) * 9)).toFixed(1)}deg`);
    s.setProperty('--blick-x', `${((dx / laenge) * 1.6).toFixed(2)}px`);
    s.setProperty('--blick-y', `${((dy / laenge) * 1.4).toFixed(2)}px`);
  };

  // Loch in der Sperrschicht genau über dem Ziel: nur dort kommen Finger durch
  function ausrichten() {
    const s = SCHRITTE[i];
    if (!zielEl?.isConnected) {
      Object.assign(spot.style, { width: '0px', height: '0px', transform: `translate(${innerWidth / 2}px, ${innerHeight / 2}px)` });
      block.style.clipPath = 'none';
      el.classList.remove('leuchtet', 'wischen');
      if (!el.classList.contains('abschied')) setzeArme(null);
      return;
    }
    const r = zielEl.getBoundingClientRect(), p = 6;
    const x = Math.max(2, r.left - p), y = Math.max(2, r.top - p);
    const w = Math.min(innerWidth - 2, r.right + p) - x, h = Math.min(innerHeight - 2, r.bottom + p) - y;
    Object.assign(spot.style, { width: `${w}px`, height: `${h}px`, transform: `translate(${x}px, ${y}px)` });
    block.style.clipPath = s.art === 'zeige' ? 'none' : `polygon(evenodd, 0 0, 100% 0, 100% 100%, 0 100%, 0 0, ${x}px ${y}px, ${x}px ${y + h}px, ${x + w}px ${y + h}px, ${x + w}px ${y}px, ${x}px ${y}px)`;
    const f = (s.finger && zielEl.querySelector(s.finger)?.getBoundingClientRect()) || { left: x, top: y, width: w, height: h };
    finger.style.transform = `translate(${f.left + f.width / 2}px, ${f.top + f.height / 2}px)`;
    el.classList.add('leuchtet');
    el.classList.toggle('wischen', s.art === 'wisch');
    el.classList.toggle('zeigen', s.art === 'zeige');
    const oben = r.top + r.height / 2 > innerHeight * 0.48;
    if (el.classList.contains('oben') !== oben) { el.classList.toggle('oben', oben); karte.classList.remove('rein'); void karte.offsetWidth; karte.classList.add('rein'); }
    requestAnimationFrame(() => setzeArme(zielEl?.getBoundingClientRect()));
  }

  // Weiter: Schritt sofort merken, denn ein Tipp auf einen Link wechselt gleich die Seite
  const weiter = () => {
    const s = SCHRITTE[i];
    if (s.ende) return ende(ABSCHIED);
    sessionStorage.setItem(LAUFT, String(i + 1));
    if (s.pause) { zielEl = null; ausrichten(); el.classList.add('pause'); }   // kurz zeigen, was aufgeklappt ist
    setTimeout(() => { el.classList.remove('pause'); if (el.isConnected) gehe(i + 1); }, s.pause ?? 80);
  };
  const imZiel = (e) => zielEl && (zielEl.contains(e.target) || (() => {
    const r = zielEl.getBoundingClientRect();
    return e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
  })());
  function beiTipp(e) { if (SCHRITTE[i].art === 'tipp' && zielEl && zielEl.contains(e.target)) weiter(); }
  // Globus: erst wenn wirklich gedreht wurde (oder beim zweiten Tipp) geht es weiter
  let druck = null, tipps = 0;
  function beiDruck(e) { if (SCHRITTE[i].art === 'wisch' && imZiel(e)) druck = [e.clientX, e.clientY]; }
  function beiLos(e) {
    if (SCHRITTE[i].art !== 'wisch' || !druck) return;
    const weg = Math.hypot(e.clientX - druck[0], e.clientY - druck[1]);
    druck = null;
    if (weg > 30 || ++tipps >= 2) { el.classList.remove('leuchtet', 'wischen'); setTimeout(weiter, 700); }
    else sprich('Nicht nur tippen: Finger drauf und ziehen!');
  }
  document.addEventListener('click', beiTipp, true);
  document.addEventListener('pointerdown', beiDruck, true);
  document.addEventListener('pointerup', beiLos, true);

  function gehe(n) {
    if (n >= SCHRITTE.length) return ende();
    i = n;
    sessionStorage.setItem(LAUFT, String(i));
    const s = SCHRITTE[i];
    if (s.seite !== seite) { aufraeumen(); el.remove(); return; }  // die nächste Seite liest den gemerkten Schritt
    zielEl = null; tipps = 0;
    el.querySelectorAll('.rg-punkte i').forEach((p) => { p.classList.toggle('on', +p.dataset.n < i); p.classList.toggle('jetzt', +p.dataset.n === i); });
    el.classList.toggle('frage', s.art === 'frage');
    mo.classList.toggle('winkt', s.art === 'frage');
    mo.classList.remove('hopst'); void mo.getBoundingClientRect(); mo.classList.add('hopst');
    knoepfe.innerHTML = s.art === 'frage'
      ? '<button class="btn primary" data-ja>Ja, zeig’s mir<span class="pfeil">→</span></button><button class="btn ghost" data-nein>Nein, danke</button>'
      : s.art === 'zeige' ? '<button class="btn primary" data-weiter>Weiter<span class="pfeil">→</span></button>'
      : `<p class="rg-hinweis"><i></i>${s.art === 'wisch' ? 'Mit dem Finger über die Erde ziehen' : 'Tipp auf das leuchtende Feld'}</p>`;
    knoepfe.querySelector('.primary')?.focus({ preventScroll: true });
    ausrichten();
    clearInterval(suche);
    if (!s.ziel) return sprich(s.text(zahlen, info()));
    // Ziel suchen (Seiten bauen sich nach und nach auf); solange denkt Mo nach
    text.innerHTML = '<span class="rg-denkt"><i></i><i></i><i></i></span>';
    const sel = typeof s.ziel === 'function' ? s.ziel() : s.ziel;
    let versuche = 0;
    suche = setInterval(() => {
      const t = document.querySelector(sel);
      const r = t?.getBoundingClientRect();
      if (t && r.width > 0 && r.height > 0) {
        clearInterval(suche);
        setTimeout(() => { zielEl = t; ausrichten(); sprich(s.text(zahlen, info())); }, 250);
      } else if (++versuche > 60) { clearInterval(suche); ende(); }
    }, 120);
  }

  knoepfe.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b) return;
    if (b.hasAttribute('data-ja')) gehe(i + 1);
    else if (b.hasAttribute('data-weiter')) weiter();
    else if (b.hasAttribute('data-nein')) {
      knoepfe.innerHTML = '';
      sprich('Alles klar! Du findest mich jederzeit im Menü oben links.');
      setTimeout(() => ende(), 2400);
    }
  });
  $('.rg-weg').addEventListener('click', () => ende());
  addEventListener('resize', ausrichten);
  addEventListener('scroll', ausrichten, true);
  gehe(i);
}
