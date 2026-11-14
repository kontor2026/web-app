// Werkbank: links die Bauideen (wie „Bauen“ in der Station), rechts was ich habe (wie das Lager).
// Ganz baubar = alles da. Teilweise = fehlende Bauteile grau, mit „Wo finde ich das?“ und Link zum Gegenstand.
import { shell, esc, chip, repoUrl } from '../shell.js';
import daten from '../daten/atlas.json';
import { bestand, setze, plus, bauteile, stand, postenName, geschaetzt } from '../werkbank.js';
import './werkbank.css';

const { objekte, komponenten: K, rezepte: REZEPTE } = daten;
const objektVon = new Map(objekte.map((o) => [o.id, o]));
const WERKZEUG = {
  shredding_bike_shredder: 'Fahrrad-Schredder', shredding_granulator: 'Granulator', injection_molding: 'Spritzguss', extrusion: 'Extruder',
  '3d_printing': '3D-Drucker', laser_processing: 'Laser', cad: 'CAD', photogrammetry: 'Fotogrammetrie', drilling: 'Bohren', sawing: 'Sägen',
  filing: 'Feilen', milling: 'Fräsen', turning: 'Drehen', screwing: 'Schrauben', riveting: 'Nieten', soldering: 'Löten', welding: 'Schweißen',
  angle_grinding: 'Winkelschleifer', cut_off_grinding: 'Trennschleifer', rough_grinding: 'Schleifen', solvent_welding: 'Kleben (Lösemittel)',
  gluing_hot_glue: 'Heißkleber', gluing_super_glue: 'Sekundenkleber', gluing_two_component: '2K-Kleber', gluing_wood_glue: 'Holzleim',
  gluing_contact_adhesive: 'Kontaktkleber', gluing_double_sided_tape: 'Doppelseitiges Klebeband',
};
const name = (cid) => K[cid]?.name ?? cid;
let filter = 'alle', offen = new Set();

const app = shell('werkbank', '../');
app.innerHTML = `
<section class="view craft werkbank">
  <div class="craft-main">
    <div class="craft-head">
      <div><h1>Was kannst du bauen?</h1><p id="zusammenfassung"></p></div>
      <div class="seg" id="filter" role="group" aria-label="Filter"></div>
    </div>
    <div class="ideas" id="ideen"></div>
  </div>
  <aside class="inv">
    <h3>Deine Werkbank</h3>
    <p>Was du zuhause hast.</p>
    <div class="wb-suche"><input class="suche-feld" id="suche" type="search" placeholder="Gegenstand hinzufügen" autocomplete="off" aria-label="Gegenstand hinzufügen"><ul id="treffer" hidden></ul></div>
    <div id="liste"></div>
  </aside>
</section>`;

// ---------- Bestand rechts ----------
function zeigeBestand() {
  const b = bestand(), ids = Object.keys(b);
  const teile = bauteile(objektVon);
  document.getElementById('liste').innerHTML = ids.length ? `
    ${ids.map((id) => `<div class="irow wb-zeile"><a class="f" href="../atlas/#kat=${id}" title="Lebensweg">${esc(objektVon.get(id)?.name ?? id)}</a>
      <span class="wb-stepper"><button data-id="${id}" data-d="-1" aria-label="weniger">−</button><b>${b[id]}</b><button data-id="${id}" data-d="1" aria-label="mehr">+</button></span></div>`).join('')}
    <details class="wb-teile"><summary>${Object.keys(teile).length} Bauteile</summary>
      ${Object.entries(teile).sort((x, y) => name(x[0]).localeCompare(name(y[0]), 'de')).map(([cid, n]) => `<div class="irow"><span>${esc(name(cid))}</span><span class="q">${n}×</span></div>`).join('')}</details>
    <button class="btn ghost wb-leeren" id="leeren">Leeren</button>`
    : '<p class="leer">Noch leer. Suche oben einen Gegenstand.</p>';
  document.querySelectorAll('.wb-stepper button').forEach((x) => x.addEventListener('click', () => setze(x.dataset.id, (bestand()[x.dataset.id] ?? 0) + +x.dataset.d)));
  document.getElementById('leeren')?.addEventListener('click', () => { for (const id of Object.keys(bestand())) setze(id, 0); });
}

const suche = document.getElementById('suche'), treffer = document.getElementById('treffer');
suche.addEventListener('input', () => {
  const q = suche.value.trim().toLowerCase();
  const liste = q ? objekte.filter((o) => o.name.toLowerCase().includes(q)).slice(0, 8) : [];
  treffer.hidden = !liste.length;
  treffer.innerHTML = liste.map((o) => `<li><button data-id="${o.id}">${esc(o.name)}<span>+</span></button></li>`).join('');
  treffer.querySelectorAll('button').forEach((x) => x.addEventListener('click', () => { plus(x.dataset.id); suche.value = ''; treffer.hidden = true; suche.focus(); }));
});
suche.addEventListener('keydown', (e) => { if (e.key === 'Enter') treffer.querySelector('button')?.click(); });

// ---------- Bauideen links ----------
function zeigeIdeen() {
  const teile = bauteile(objektVon), leer = !Object.keys(bestand()).length;
  const alle = (REZEPTE ?? []).map((r) => ({ r, s: stand(r, teile) }))
    .sort((a, b) => b.s.baubar - a.s.baubar || b.s.ok / b.s.alle - a.s.ok / a.s.alle || a.r.titel.localeCompare(b.r.titel, 'de'));
  const zahl = { baubar: alle.filter((x) => x.s.baubar).length, fast: alle.filter((x) => !x.s.baubar && x.s.teilweise).length, alle: alle.length };
  if (filter !== 'alle' && !zahl[filter]) filter = 'alle';
  document.getElementById('filter').innerHTML = [['baubar', 'Baubar'], ['fast', 'Fast'], ['alle', 'Alle']]
    .map(([k, t]) => `<button data-f="${k}" class="${filter === k ? 'on' : ''}" ${zahl[k] ? '' : 'disabled'}>${t} ${zahl[k]}</button>`).join('');
  document.querySelectorAll('#filter button').forEach((x) => x.addEventListener('click', () => { filter = x.dataset.f; zeigeIdeen(); }));
  document.getElementById('zusammenfassung').textContent = !alle.length ? 'Die Bauideen werden gerade geschrieben.'
    : leer ? 'Füge rechts hinzu, was du hast.' : `${zahl.baubar} baubar, bei ${zahl.fast} fehlt noch etwas.`;
  const sichtbar = alle.filter((x) => filter === 'alle' || (filter === 'baubar' ? x.s.baubar : !x.s.baubar && x.s.teilweise));
  document.getElementById('ideen').innerHTML = sichtbar.map(({ r, s }, i) => `
    <article class="idea wb-idee ${s.baubar ? 'baubar' : ''}" id="r-${r.id}">
      <div class="wb-kopf"><span class="letter">${String.fromCharCode(65 + (i % 26))}</span>
        <span class="wb-status">${s.baubar ? 'Baubar' : `${s.ok} von ${s.alle}`}</span></div>
      <div><h2>${esc(r.titel)}</h2><p class="kurz">${esc(r.kurz ?? '')}</p></div>
      <div class="meta"><span>${esc(r.dauer ?? '')}</span><span class="dots">${'●'.repeat(r.stufe ?? 1)}${'○'.repeat(3 - (r.stufe ?? 1))}</span></div>
      <div><h4>Du brauchst</h4><div class="uses">${s.posten.map((p) => `
        <div class="use ${p.ok ? 'da' : 'fehlt'}"><i></i><span title="${esc(postenName(p, teile, name).alle)}">${esc(postenName(p, teile, name).text)}${postenName(p, teile, name).mehr ? ` <small>+${postenName(p, teile, name).mehr}</small>` : ''}${p.hinweis ? `<small class="wb-hinweis">${esc(p.hinweis)}</small>` : ''}</span><span class="q">${Math.min(p.da, p.soll)}/${geschaetzt(p) ? '≈' : ''}${p.soll}</span>
          ${p.ok ? '<span></span>' : `<button class="wb-wo" data-k="${r.id}:${p.component_id}" aria-expanded="${offen.has(`${r.id}:${p.component_id}`)}">Wo?</button>`}</div>
        ${!p.ok && offen.has(`${r.id}:${p.component_id}`) ? `<div class="wb-quellen">${p.ids.flatMap((id) => K[id]?.in ?? []).filter((v, j, a) => a.indexOf(v) === j).slice(0, 8).map((oid) => `
          <div><a href="../atlas/#kat=${oid}">${esc(objektVon.get(oid)?.name ?? oid)}</a><button data-plus="${oid}" aria-label="Hab ich">+ Hab ich</button></div>`).join('')}</div>` : ''}`).join('')}</div></div>
      <div class="tools">${(r.werkzeug ?? []).map((w) => `<span class="tag">${esc(WERKZEUG[w] ?? w)}</span>`).join('')}</div>
      <details class="wb-anleitung"><summary>Anleitung</summary><ol class="steps-list">${(r.schritte ?? []).map((x) => `<li>${esc(x)}</li>`).join('')}</ol>
        ${r.sicherheit ? `<p class="note warn">${esc(r.sicherheit)}</p>` : ''}</details>
      <p class="wb-quelle">${esc(r.quelle?.titel ?? '')}${chip(r.quelle?.url, r.quelle?.titel)}${s.posten.some(geschaetzt) ? `<a class="chip-q schaetzung" href="${esc(repoUrl(`data/rezepte/${r.id}.json`))}" target="_blank" rel="noopener" title="Mengen mit ≈ sind geschätzt">≈ Schätzung</a>` : ''}</p>
    </article>`).join('') || '<p class="leer">Keine Bauideen in dieser Auswahl.</p>';
  document.querySelectorAll('.wb-wo').forEach((x) => x.addEventListener('click', () => { offen.has(x.dataset.k) ? offen.delete(x.dataset.k) : offen.add(x.dataset.k); zeigeIdeen(); }));
  document.querySelectorAll('[data-plus]').forEach((x) => x.addEventListener('click', () => plus(x.dataset.plus)));
}

function alles() { zeigeBestand(); zeigeIdeen(); }
addEventListener('werkbank', alles);
addEventListener('storage', alles);       // andere Tabs
alles();
