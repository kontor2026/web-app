// Werkbank als Laden: Gegenstände mit Bild aus dem 3D-Modell sammeln (Korb = was ich habe), dann sehen, was baubar ist.
import { shell, esc, chip, icon, gramm } from '../shell.js';
import daten from '../daten/atlas.json';
import { bestand, plus, bauteile, stand, postenName, geschaetzt, anzahl } from '../werkbank.js';
import { erzeugeViewer, ladeModell } from '../viewer.js';
import './werkbank.css';

const { objekte, komponenten: K, rezepte: REZEPTE } = daten;
const objektVon = new Map(objekte.map((o) => [o.id, o]));
const GRUPPEN = ['Elektro', 'Verpackung', 'Textil', 'Alltag'];
const WERKZEUG = {
  shredding_bike_shredder: 'Fahrrad-Schredder', shredding_granulator: 'Granulator', injection_molding: 'Spritzguss', extrusion: 'Extruder',
  '3d_printing': '3D-Drucker', laser_processing: 'Laser', drilling: 'Bohren', sawing: 'Sägen', filing: 'Feilen', milling: 'Fräsen',
  screwing: 'Schrauben', soldering: 'Löten', gluing_hot_glue: 'Heißkleber', gluing_super_glue: 'Sekundenkleber', gluing_two_component: '2K-Kleber',
  gluing_wood_glue: 'Holzleim', gluing_double_sided_tape: 'Klebeband',
};
const name = (cid) => K[cid]?.name ?? cid;
let ansicht = location.hash === '#bauen' ? 'bauen' : 'sammeln', gruppe = null;
const offen = new Set();

const app = shell('werkbank', '../');
app.innerHTML = `
<section class="view laden">
  <div class="laden-haupt">
    <div class="laden-kopf">
      <div class="seg" id="ansicht" role="tablist">
        <button data-a="sammeln" role="tab">Sammeln</button><button data-a="bauen" role="tab">Bauen <b id="baubar-zahl"></b></button>
      </div>
      <input class="suche-feld" id="suche" type="search" placeholder="Suchen" autocomplete="off" aria-label="Gegenstand suchen">
    </div>
    <div class="laden-chips" id="chips"></div>
    <div class="laden-raster" id="raster"></div>
    <div class="laden-ideen" id="ideen"></div>
  </div>
  <aside class="korb" id="korb" aria-label="Deine Werkbank"></aside>
</section>
<div class="vorschau-buehne" id="buehne" aria-hidden="true"></div>`;

// ---------- Bilder der Gegenstände: ein unsichtbarer 3D-Viewer zeichnet sie nacheinander ----------
const bilder = new Map(), warte = [];
let maler = null, malt = false;
async function male() {
  if (malt) return;
  malt = true;
  maler ??= erzeugeViewer(document.getElementById('buehne'));
  while (warte.length) {
    const id = warte.shift();
    if (bilder.has(id)) continue;
    try {
      maler.nummern(false);
      maler.explosion(0, false);              // zusammengebaut, Ausschnitt passt sich an
      maler.lade(await ladeModell(id));
      await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
      bilder.set(id, maler.bild());
      document.querySelectorAll(`img[data-bild="${id}"]`).forEach((img) => { img.src = bilder.get(id); img.classList.add('da'); });
    } catch { bilder.set(id, ''); }
  }
  malt = false;
}
const beobachter = new IntersectionObserver((eintraege) => {
  for (const e of eintraege) if (e.isIntersecting) { warte.push(e.target.dataset.bild); beobachter.unobserve(e.target); }
  male();
}, { rootMargin: '200px' });
const bild = (id, k = '') => `<img class="laden-bild ${k} ${bilder.get(id) ? 'da' : ''}" data-bild="${id}" alt="" ${bilder.get(id) ? `src="${bilder.get(id)}"` : ''}>`;
function beobachte(wurzel) { wurzel.querySelectorAll('img[data-bild]:not(.da)').forEach((img) => beobachter.observe(img)); }

// ---------- Sammeln: Raster aller Gegenstände ----------
function zeigeRaster() {
  const q = document.getElementById('suche').value.trim().toLowerCase(), b = bestand();
  document.getElementById('chips').innerHTML = [null, ...GRUPPEN].map((g) =>
    `<button class="lw-chip ${gruppe === g ? 'on' : ''}" data-g="${g ?? ''}">${g ?? 'Alle'}</button>`).join('');
  const liste = objekte.filter((o) => (!gruppe || o.gruppe === gruppe) && (!q || o.name.toLowerCase().includes(q)))
    .sort((a, c) => a.name.localeCompare(c.name, 'de'));
  document.getElementById('raster').innerHTML = liste.map((o) => `
    <article class="ware ${b[o.id] ? 'drin' : ''}">
      <a class="ware-bild" href="../atlas/#kat=${o.id}" title="Lebensweg ansehen">${bild(o.id)}</a>
      <div class="ware-text"><b>${esc(o.name)}</b><span>${gramm(o.gramm)}</span></div>
      ${b[o.id] ? `<span class="wb-stepper"><button data-id="${o.id}" data-d="-1" aria-label="weniger">−</button><b>${b[o.id]}</b><button data-id="${o.id}" data-d="1" aria-label="mehr">+</button></span>`
        : `<button class="ware-plus" data-id="${o.id}" data-d="1" aria-label="${esc(o.name)} hinzufügen">+</button>`}
    </article>`).join('') || '<p class="leer">Nichts gefunden.</p>';
  beobachte(document.getElementById('raster'));
}

// ---------- Korb: was ich habe ----------
function zeigeKorb() {
  const b = bestand(), ids = Object.keys(b);
  const baubar = (REZEPTE ?? []).filter((r) => stand(r, bauteile(objektVon)).baubar).length;
  document.getElementById('baubar-zahl').textContent = baubar || '';
  document.getElementById('korb').innerHTML = `
    <div class="korb-kopf">${icon('werkbank')}<b>Werkbank</b><span>${anzahl()}</span></div>
    <div class="korb-liste">${ids.map((id) => `
      <div class="korb-zeile">${bild(id, 'klein')}<span>${esc(objektVon.get(id)?.name ?? id)}</span>
        <span class="wb-stepper"><button data-id="${id}" data-d="-1" aria-label="weniger">−</button><b>${b[id]}</b><button data-id="${id}" data-d="1" aria-label="mehr">+</button></span></div>`).join('')
      || '<p class="leer">Tippe auf +, was du hast.</p>'}</div>
    ${ids.length ? `<button class="btn primary korb-los" data-a="bauen">${baubar ? `${baubar} baubar` : 'Ideen ansehen'}<span class="pfeil">→</span></button>` : ''}`;
  beobachte(document.getElementById('korb'));
}

// ---------- Bauen: Ideen nach Stand ----------
function zeigeIdeen() {
  const teile = bauteile(objektVon);
  const alle = (REZEPTE ?? []).map((r) => ({ r, s: stand(r, teile) }))
    .sort((a, b) => b.s.baubar - a.s.baubar || b.s.ok / b.s.alle - a.s.ok / a.s.alle || a.r.titel.localeCompare(b.r.titel, 'de'));
  document.getElementById('ideen').innerHTML = alle.map(({ r, s }, i) => `
    <article class="idee ${s.baubar ? 'baubar' : ''}">
      <div class="idee-kopf"><span class="lw-nr">${String(i + 1).padStart(2, '0')}</span><span class="wb-status ${s.baubar ? 'ok' : ''}">${s.baubar ? 'Baubar' : 'Fehlt noch'}</span></div>
      <h2>${esc(r.titel)}</h2>
      <div class="uses">${s.posten.map((p) => {
        const n = postenName(p, teile, name), k = `${r.id}:${p.component_id}`;
        return `<div class="use ${p.ok ? 'da' : 'fehlt'}"><i></i><span title="${esc(n.alle)}">${esc(n.text)}${n.mehr ? ` <small>+${n.mehr}</small>` : ''}</span>
          <span class="q">${Math.min(p.da, p.soll)} von ${geschaetzt(p) ? '≈' : ''}${p.soll}</span>
          ${p.ok ? '<span></span>' : `<button class="wb-wo" data-k="${k}" aria-expanded="${offen.has(k)}">Wo?</button>`}</div>
          ${!p.ok && offen.has(k) ? `<div class="wb-quellen">${p.ids.flatMap((id) => K[id]?.in ?? []).filter((v, j, a) => a.indexOf(v) === j).slice(0, 6).map((oid) => `
            <div>${bild(oid, 'mini')}<a href="../atlas/#kat=${oid}">${esc(objektVon.get(oid)?.name ?? oid)}</a><button data-id="${oid}" data-d="1" aria-label="hinzufügen">+</button></div>`).join('')}</div>` : ''}`;
      }).join('')}</div>
      <details class="wb-anleitung"><summary>Anleitung · ${esc(r.dauer ?? '')}</summary>
        <div class="tools">${(r.werkzeug ?? []).map((w) => `<span class="tag">${esc(WERKZEUG[w] ?? w)}</span>`).join('')}</div>
        <ol class="steps-list">${(r.schritte ?? []).map((x) => `<li>${esc(x)}</li>`).join('')}</ol>
        ${r.sicherheit ? `<p class="note warn">${esc(r.sicherheit)}</p>` : ''}
        <p class="wb-quelle">${chip(r.quelle?.url, r.quelle?.titel)}${s.posten.some(geschaetzt) ? '<span class="chip-q schaetzung" title="Mengen mit ≈ sind geschätzt">≈ Schätzung</span>' : ''}</p></details>
    </article>`).join('');
  beobachte(document.getElementById('ideen'));
}

// ---------- Steuerung ----------
function zeige() {
  document.querySelector('.laden').dataset.ansicht = ansicht;
  document.querySelectorAll('#ansicht button').forEach((b) => { b.classList.toggle('on', b.dataset.a === ansicht); b.setAttribute('aria-selected', String(b.dataset.a === ansicht)); });
  zeigeKorb();
  if (ansicht === 'sammeln') zeigeRaster(); else zeigeIdeen();
}
app.addEventListener('click', (e) => {
  const x = e.target.closest('button');
  if (!x) return;
  if (x.dataset.d) plus(x.dataset.id, +x.dataset.d);
  else if (x.dataset.a) { ansicht = x.dataset.a; history.replaceState(null, '', ansicht === 'bauen' ? '#bauen' : location.pathname); zeige(); scrollTo(0, 0); }
  else if (x.dataset.g !== undefined) { gruppe = x.dataset.g || null; zeigeRaster(); }
  else if (x.dataset.k) { if (offen.has(x.dataset.k)) offen.delete(x.dataset.k); else offen.add(x.dataset.k); zeigeIdeen(); }
});
document.getElementById('suche').addEventListener('input', () => { if (ansicht !== 'sammeln') { ansicht = 'sammeln'; zeige(); } else zeigeRaster(); });
addEventListener('werkbank', zeige);
addEventListener('storage', zeige);
zeige();
