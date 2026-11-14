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
// Zwischenspeicher im Browser: Bild bleibt, bis sich das Modell ändert (Kennung aus Teilezahl und Masse)
const kennung = (seed) => `${seed.parts.length}-${Math.round(seed.parts.reduce((s, p) => s + p.mass * 10 + p.w + p.h, 0))}`;
const ausSpeicher = (id) => { try { return JSON.parse(localStorage.getItem(`vorschau:${id}`)); } catch { return null; } };
for (const o of objekte) { const v = ausSpeicher(o.id); if (v?.bild) bilder.set(o.id, v.bild); }
async function male() {
  if (malt) return;
  malt = true;
  maler ??= erzeugeViewer(document.getElementById('buehne'));
  while (warte.length) {
    const id = warte.shift();
    try {
      const seed = await ladeModell(id), k = kennung(seed);
      if (ausSpeicher(id)?.k === k && bilder.get(id)) continue;   // Bild aus dem Speicher ist aktuell
      maler.nummern(false);
      maler.foto(false);                      // Zeichnungsansicht: viel schneller als die Foto-Ansicht
      maler.explosion(0, false);              // zusammengebaut, Ausschnitt passt sich an
      maler.lade(seed);
      await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
      bilder.set(id, maler.bild());
      try { localStorage.setItem(`vorschau:${id}`, JSON.stringify({ k, bild: bilder.get(id) })); } catch { /* Speicher voll: nur ohne Zwischenspeicher */ }
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
function beobachte(wurzel) { wurzel.querySelectorAll('img[data-bild]').forEach((img) => beobachter.observe(img)); }   // auch gespeicherte prüfen

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
      <div class="idee-kopf"><h2>${esc(r.titel)}</h2>${s.baubar ? `<span class="haken" title="Alles da">${icon('haken')}</span>` : ''}</div>
      <div class="uses">${s.posten.map((p) => {
        const n = postenName(p, teile, name), k = `${r.id}:${p.component_id}`;
        return `<div class="use ${p.ok ? 'da' : 'fehlt'}"><i></i><span title="${esc(n.alle)}">${esc(n.text)}${n.mehr ? ` <small>+${n.mehr}</small>` : ''}</span>
          <span class="q">${p.soll > 1 ? `${Math.min(p.da, p.soll)}/${geschaetzt(p) ? '≈' : ''}${p.soll}` : ''}</span>
          <span></span></div>
          ${p.ok ? '' : `<details class="wb-wo" data-k="${k}" ${offen.has(k) ? 'open' : ''}><summary>Wo finde ich das?</summary><div class="wb-quellen">${p.ids.flatMap((id) => K[id]?.in ?? []).filter((v, j, a) => a.indexOf(v) === j).slice(0, 6).map((oid) => `
            <div>${bild(oid, 'mini')}<a href="../atlas/#kat=${oid}">${esc(objektVon.get(oid)?.name ?? oid)}</a><button data-id="${oid}" data-d="1" aria-label="hinzufügen">+</button></div>`).join('')}</div></details>`}`;
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

});
document.getElementById('suche').addEventListener('input', () => { if (ansicht !== 'sammeln') { ansicht = 'sammeln'; zeige(); } else zeigeRaster(); });
// Offene „Wo finde ich das?“ merken, damit sie nach dem Hinzufügen offen bleiben
app.addEventListener('toggle', (e) => { const k = e.target.dataset?.k; if (k) { if (e.target.open) offen.add(k); else offen.delete(k); } }, true);
addEventListener('werkbank', zeige);
addEventListener('storage', zeige);
zeige();
