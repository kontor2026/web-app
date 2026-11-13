// Rohstoff-Atlas: Gegenstand wählen → Stoffstrom (Bauteile → Materialien → Rohstoffe) → Herkunft auf dem Globus.
// Layout und Bausteine wie in der Station: Katalog wie #katalog, Objektansicht wie der Steckbrief (.sheet).
import { shell, esc, zahl, gramm } from '../shell.js';
import { CLASSES, MATERIALS } from '../../../../js/data/catalog.js';
import daten from '../daten/atlas.json';
import { zeichneStoffstrom } from './stoffstrom.js';
import { erzeugeGlobus } from './globus.js';
import './atlas.css';

const { objekte, rohstoffe: ROH, materialien: MAT, laender: LAND, quellen: QUELLE } = daten;
const objektVon = new Map(objekte.map((o) => [o.id, o]));
const BEISPIELE = ['smartphone', 'pet_bottle', 'laptop', 't_shirt', 'aluminium_can', 'hair_dryer'].filter((id) => objektVon.has(id));
const STUFE = {
  abbau: { name: 'Abbau', erklaert: 'wo der Rohstoff aus der Erde oder vom Feld kommt' },
  verarbeitung: { name: 'Verarbeitung', erklaert: 'wo er gereinigt und zu Metall oder Chemikalie verarbeitet wird' },
};

const material = (mid) => {
  const k = MATERIALS[MAT[mid]?.kat];
  return { name: k?.name ?? MAT[mid]?.en ?? mid, farbe: CLASSES[k?.cls]?.color ?? '#cccccc', cls: k?.cls };
};
const rohstoff = (key) => ({ ...ROH[key], key, farbe: CLASSES[ROH[key]?.art]?.color ?? '#cccccc' });
const land = (a3) => LAND[a3]?.name ?? a3;
// „aus der DR Kongo“, „aus den USA“, „aus China“
const ARTIKEL = { COD: 'der', USA: 'den', TUR: 'der', PHL: 'den', NLD: 'den', ARE: 'den', SVK: 'der', UKR: 'der', MNG: 'der', CHE: 'der', CAF: 'der', DOM: 'der' };
const ausLand = (a3) => `aus ${ARTIKEL[a3] ? ARTIKEL[a3] + ' ' : ''}${land(a3)}`;

let stufe = 'abbau';
const ankuendigung = sessionStorage.getItem('atlas-hinweis') !== 'aus';

const app = shell('atlas', '../', `<span class="stock">Gegenstände <b>${objekte.length}</b></span>`);

// ---------- 01 Gegenstand wählen ----------
function zeigeKatalog() {
  document.title = 'Rohstoff-Atlas · Kreislauf-Station';
  const gruppen = new Map();
  for (const o of [...objekte].sort((a, b) => a.name.localeCompare(b.name, 'de')))
    (gruppen.get(o.klasse) ?? gruppen.set(o.klasse, []).get(o.klasse)).push(o);
  app.innerHTML = `
  <section class="view craft atlas-katalog">
    <div class="craft-main">
      <div class="craft-head">
        <div><div class="eyebrow">Schritt 1 von 3</div>
          <h1 style="margin-top:8px">Welchen Gegenstand willst du untersuchen?</h1>
          <p class="lead">Du siehst danach, woraus er besteht und aus welchen Ländern seine Rohstoffe kommen.</p></div>
        <input id="suche" class="suche-feld" type="search" placeholder="Suchen, z. B. Wasserkocher" autocomplete="off" aria-label="Gegenstand suchen">
      </div>
      <div>
        <div class="beispiele">${BEISPIELE.map((id, i) => karte(objektVon.get(id), i)).join('')}</div>
        <div class="katalog" id="katalog" style="margin-top:32px">
          <h3 class="eyebrow">Alle ${objekte.length} Gegenstände</h3>
          ${[...gruppen].map(([g, os]) => `<div class="gruppe"><h4 class="eyebrow">${esc(g)} · ${os.length}</h4>
            <div class="kat-list">${os.map((o) => `<a href="#kat=${o.id}" class="tag" data-name="${esc(`${o.name} ${o.id}`.toLowerCase())}">${esc(o.name)}</a>`).join('')}</div></div>`).join('')}
        </div>
      </div>
    </div>
    <aside class="inv">
      <h3>So funktioniert es</h3>
      <ol class="howto" style="margin-top:12px">
        <li>Gegenstand wählen.</li>
        <li>Im Stoffstrom ablesen, woraus er besteht: links die Bauteile, in der Mitte die Materialien, rechts die Rohstoffe.</li>
        <li>Einen Rohstoff antippen. Der Globus zeigt, aus welchen Ländern er kommt.</li>
      </ol>
      <h3 style="margin-top:28px">Farben</h3>
      <div class="mix-legend einspaltig">${Object.values(CLASSES).map((c) => `<span><i style="background:${c.color}"></i>${esc(c.label)}</span>`).join('')}
        <span><i class="krit-i">▲</i>kritischer Rohstoff für die EU</span></div>
      <p class="source" style="margin-top:28px">Herkunft: ${['usgs2026', 'eucrm2023', 'usdapsd2026'].filter((q) => QUELLE[q]).map((q) => esc(QUELLE[q].titel)).join(' · ') || 'noch keine Daten'}.</p>
    </aside>
  </section>`;
  const suche = document.getElementById('suche');
  suche.addEventListener('input', () => {
    const q = suche.value.trim().toLowerCase();
    document.querySelectorAll('#katalog .tag').forEach((a) => { a.hidden = !!q && !a.dataset.name.includes(q); });
    document.querySelectorAll('#katalog .gruppe').forEach((g) => { g.hidden = ![...g.querySelectorAll('.tag')].some((a) => !a.hidden); });
  });
  suche.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') { const a = document.querySelector('#katalog .tag:not([hidden])'); if (a) location.hash = a.getAttribute('href'); }
  });
}
function karte(o, i) {
  const laender = new Set(o.rohstoffe.flatMap((r) => Object.keys(ROH[r.key]?.abbau?.anteile ?? {})));
  return `<a class="beispiel" href="#kat=${o.id}">
    <span class="letter">0${i + 1}</span><b>${esc(o.name)}</b>
    <span class="meta"><span>${gramm(o.gramm)}</span><span>${o.rohstoffe.length} ${o.rohstoffe.length === 1 ? 'Rohstoff' : 'Rohstoffe'}</span>${laender.size ? `<span>${laender.size} Länder</span>` : ''}</span></a>`;
}

// ---------- 02/03 Gegenstand: Stoffstrom, Globus, Datenblatt ----------
let obj = null, gewaehlt = null, globus = null, strom = null;

function zeigeObjekt(o, r) {
  const neu = obj !== o || !document.querySelector('.atlas-sheet');
  obj = o; gewaehlt = r ?? null;
  document.title = `${o.name} · Rohstoff-Atlas`;
  if (neu) {
    app.innerHTML = `
    <section class="view sheet atlas-sheet">
      <div class="canvas">
        <div class="canvas-head">
          <div><h2 id="globus-titel"></h2><p id="globus-unter"></p></div>
          <div class="seg" role="group" aria-label="Stufe der Wertschöpfung">
            ${Object.entries(STUFE).map(([k, s]) => `<button data-stufe="${k}" title="${esc(s.erklaert)}">${s.name}</button>`).join('')}
          </div>
        </div>
        <div class="globus" id="globus" aria-label="Globus: Herkunftsländer"></div>
        <div class="globus-legende" id="globus-legende"></div>
        <div class="strom-flaeche">
          <div class="strom-kopf"><span class="eyebrow">Stoffstrom</span><span>von links nach rechts gelesen · je breiter, desto mehr Gramm</span><span class="nur-schmal">· Bauteile siehe 3D-Modelle</span></div>
          <div class="strom" id="strom"></div>
        </div>
        <div class="hint-hover ${ankuendigung ? 'hint-puls' : ''}" id="hinweis" ${ankuendigung ? '' : 'hidden'}>Tippe einen Rohstoff an, im Stoffstrom oder rechts</div>
      </div>
      <aside class="panel" id="panel"></aside>
      <div class="actionbar">
        <div class="q">${esc(o.name)} <span>· ${gramm(o.gramm)} · ${o.rohstoffe.length} ${o.rohstoffe.length === 1 ? 'Rohstoff' : 'Rohstoffe'}</span></div>
        <a class="btn ghost" href="#">← Anderen Gegenstand wählen</a>
      </div>
    </section>`;
    document.querySelectorAll('[data-stufe]').forEach((b) => b.addEventListener('click', () => { stufe = b.dataset.stufe; aktualisiere(); }));
    globus = erzeugeGlobus(document.getElementById('globus'), LAND);
    zeichneStrom();
    new ResizeObserver(() => zeichneStrom()).observe(document.getElementById('strom'));
  }
  aktualisiere();
}

function zeichneStrom() {
  strom = zeichneStoffstrom(document.getElementById('strom'), obj, {
    teilName: (t) => t.name, material, rohstoff,
    onHover: (id, typ) => {
      if (typ !== 'rohstoff') return;
      zeigeGlobus(id ?? gewaehlt, false);
    },
    onClick: (id, typ) => { if (typ === 'rohstoff') location.hash = `kat=${obj.id}&r=${id}`; },
  });
  strom.markiere(gewaehlt);
}

// Länderanteile: ein Rohstoff, oder alle Rohstoffe des Gegenstands nach Gramm gewichtet
function anteile(key) {
  if (key) return { werte: ROH[key]?.[stufe]?.anteile ?? {}, mitDaten: !!ROH[key]?.[stufe] };
  const summe = {}; let gesamt = 0;
  for (const r of obj.rohstoffe) {
    const a = ROH[r.key]?.[stufe]?.anteile;
    if (!a) continue;
    gesamt += r.g;
    for (const [l, p] of Object.entries(a)) summe[l] = (summe[l] ?? 0) + r.g * p;
  }
  for (const l in summe) summe[l] /= gesamt || 1;
  return { werte: summe, mitDaten: gesamt > 0, anteilMitDaten: gesamt / obj.rohstoffe.reduce((s, r) => s + r.g, 0) };
}

function zeigeGlobus(key, fokus = true) {
  const { werte, mitDaten } = anteile(key);
  globus.zeige(werte, { fokus });
  const r = key && rohstoff(key);
  document.getElementById('globus-titel').textContent = r ? `Woher kommt ${r.artikel} ${r.name}?` : `Woher kommen die Rohstoffe?`;
  document.getElementById('globus-unter').textContent = !mitDaten ? `Für diese Stufe gibt es noch keine Länderdaten mit Quelle.`
    : `${STUFE[stufe].name}: ${STUFE[stufe].erklaert}${r ? '' : ' · alle Rohstoffe nach Gramm gewichtet'}`;
  const top = Object.entries(werte).sort((a, b) => b[1] - a[1]).slice(0, 5);
  document.getElementById('globus-legende').innerHTML = mitDaten ? `<div class="eyebrow">Höher und dunkler = größerer Anteil</div>
    ${top.map(([l, p], i) => `<button class="gl-zeile" data-land="${l}"><span class="nr">0${i + 1}</span>${esc(land(l))}<b>${zahl(p, 0)} %</b></button>`).join('')}
    <div class="gl-de"><i></i>DE = Deutschland: hier wird der Gegenstand genutzt</div>` : '';
  document.querySelectorAll('.gl-zeile').forEach((b) => {
    b.addEventListener('pointerenter', () => globus.hebeHervor(b.dataset.land));
    b.addEventListener('pointerleave', () => globus.hebeHervor(null));
  });
}

function aktualisiere() {
  document.querySelectorAll('[data-stufe]').forEach((b) => b.classList.toggle('on', b.dataset.stufe === stufe));
  zeigeGlobus(gewaehlt);
  strom?.markiere(gewaehlt);
  gewaehlt ? panelRohstoff(gewaehlt) : panelObjekt();
}

// ---------- Datenblatt rechts ----------
const panel = () => document.getElementById('panel');
function setzePanel(html, crumbs) {
  const p = panel();
  p.innerHTML = `<div class="panel-inner">${crumbs ? `<nav class="crumbs">${crumbs.map((c, i) => (i < crumbs.length - 1
    ? `<a href="${c.href}">${esc(c.label)}</a><span></span>` : `<b style="font-weight:500;color:var(--ink)">${esc(c.label)}</b>`)).join('')}</nav>` : ''}${html}</div>`;
  p.querySelectorAll('[data-r]').forEach((b) => {
    b.addEventListener('click', () => (location.hash = `kat=${obj.id}&r=${b.dataset.r}`));
    b.addEventListener('pointerenter', () => { strom.markiere(b.dataset.r); zeigeGlobus(b.dataset.r, false); });
    b.addEventListener('pointerleave', () => { strom.markiere(gewaehlt); zeigeGlobus(gewaehlt, false); });
  });
  p.scrollTop = 0;
}
const kachel = (r, g) => `<button class="el ${r.kritisch ? 'crit' : ''} ${r.abbau || r.verarbeitung ? '' : 'ohne'}" data-r="${r.key}" title="${esc(r.name)}${r.kritisch ? ' · kritisch für die EU' : ''}">
  <span class="z">${r.z ?? ''}</span><span class="share">${gramm(g)}</span><span class="sym">${esc(r.sym)}</span><span class="nm">${esc(r.name)}</span></button>`;

function panelObjekt() {
  const o = obj, gesamt = o.materialien.reduce((s, m) => s + m.g, 0) || 1;
  const klassen = new Map();
  for (const m of o.materialien) { const c = material(m.mid).cls ?? 'metall'; klassen.set(c, (klassen.get(c) ?? 0) + m.g); }
  const mix = [...klassen].sort((a, b) => b[1] - a[1]);
  const kritisch = o.rohstoffe.filter((r) => ROH[r.key]?.kritisch).length;
  const { werte, mitDaten, anteilMitDaten } = anteile(null);
  const top = Object.entries(werte).sort((a, b) => b[1] - a[1]);
  const meist = o.materialien[0];
  const satz = [
    `${o.name} wiegt ${gramm(o.gramm)}.`,
    meist ? `Am meisten steckt ${material(meist.mid).name} drin (${gramm(meist.g)}).` : '',
    `${o.rohstoffe.length} ${o.rohstoffe.length === 1 ? 'Rohstoff' : 'Rohstoffe'}${kritisch ? `, davon ${kritisch} kritisch für die EU` : ''}.`,
    mitDaten && top.length ? `Beim ${STUFE[stufe].name} kommt das meiste ${ausLand(top[0][0])} (${zahl(top[0][1], 0)} %).` : '',
  ].filter(Boolean).join(' ');
  setzePanel(`
    <div><div class="eyebrow">Schritt 2 von 3 · Woraus besteht dieser Gegenstand?</div>
      <h1 style="margin-top:8px">${esc(o.name)}</h1><p class="sub">${esc(satz)}</p></div>
    <div class="stats">
      <div><b>${gramm(o.gramm)}</b><span>Gewicht</span><small>laut Tabelle</small></div>
      <div><b>${o.rohstoffe.length}</b><span>Rohstoffe</span><small>${kritisch} kritisch ▲</small></div>
      <div><b>${mitDaten ? top.length : '–'}</b><span>Länder</span><small>${mitDaten ? `für ${zahl(anteilMitDaten * 100, 0)} % der Masse bekannt` : 'noch keine Daten'}</small></div>
    </div>
    <div><h3>Rohstoffe · tippe einen an</h3><div class="elements">${o.rohstoffe.map((r) => kachel(rohstoff(r.key), r.g)).join('')}</div>
      <p class="source" style="margin-top:10px">▲ Ecke: kritischer Rohstoff für die EU. Blass: noch keine Länderdaten.</p></div>
    <div><h3>Materialmix nach Gewicht</h3>
      <div class="mix">${mix.map(([c, g]) => `<i style="width:${(g / gesamt) * 100}%;background:${CLASSES[c]?.color}"></i>`).join('')}</div>
      <div class="mix-legend">${mix.map(([c, g]) => `<span><i style="background:${CLASSES[c]?.color}"></i>${esc(CLASSES[c]?.label)}<b>${zahl((g / gesamt) * 100, 0)} %</b></span>`).join('')}</div></div>
    <p class="source">Bauteile und Massen: ${o.handgebaut ? 'handgebautes 3D-Modell' : 'automatischer Platzhalter'} · Metallgehalte: Öko-Institut 2012 · Herkunft: siehe einzelne Rohstoffe.</p>`, null);
}

function panelRohstoff(key) {
  const r = rohstoff(key), menge = obj.rohstoffe.find((x) => x.key === key)?.g ?? 0;
  const st = ROH[key]?.[stufe], andere = stufe === 'abbau' ? 'verarbeitung' : 'abbau';
  const herMaterial = obj.mr.filter(([, k]) => k === key).sort((a, b) => b[2] - a[2]).map(([mid]) => material(mid).name);
  const zeilen = st ? Object.entries(st.anteile).sort((a, b) => b[1] - a[1]) : [];
  const q = st && QUELLE[st.quelle];
  setzePanel(`
    <div class="el-hero">${kachel(r, menge).replace('<button', '<div').replace('</button>', '</div>')}
      <div><div class="eyebrow">Schritt 3 von 3</div><h1 style="margin-top:6px">Woher kommt ${esc(r.artikel)} ${esc(r.name)}?</h1>
        <p class="sub">Im Gegenstand ${esc(obj.name)}: ${gramm(menge)}${herMaterial.length ? `, steckt in ${esc(herMaterial.join(', '))}` : ''}.</p></div></div>
    <div class="seg stufe-wahl" role="group" aria-label="Stufe">${Object.entries(STUFE).map(([k, s]) => `<button data-stufe2="${k}" class="${k === stufe ? 'on' : ''}">${s.name}</button>`).join('')}</div>
    <p class="erklaerung"><b>${STUFE[stufe].name}:</b> ${STUFE[stufe].erklaert}.</p>
    ${st ? `<div><h3>Länder nach Anteil</h3>
      ${zeilen.map(([l, p], i) => `<div class="mrow land" data-land="${l}"><span class="nr">${String(i + 1).padStart(2, '0')}</span><span>${esc(land(l))}</span>
        <span class="pct">${p} %</span><span></span><div class="mbar"><b style="width:${p}%"></b></div></div>`).join('')}
      ${st.rest ? `<div class="mrow land rest"><span class="nr">··</span><span>Übrige Länder</span><span class="pct">${st.rest} %</span><span></span><div class="mbar"><b style="width:${st.rest}%"></b></div></div>` : ''}</div>
      <p class="source">Quelle: ${esc(q?.titel ?? st.quelle)}${st.seite ? `, ${esc(st.seite)}` : ''}. ${esc(st.was ?? '')}${q?.url ? ` <a href="${esc(q.url)}" target="_blank" rel="noopener">Öffnen ↗</a>` : ''}</p>`
    : `<p class="note warn">Für ${esc(r.name)} haben wir beim ${STUFE[stufe].name} noch keine Länderdaten mit Quelle. Wir zeigen nichts Geschätztes.${ROH[key]?.[andere] ? ` Für die ${STUFE[andere].name} gibt es Daten.` : ''}</p>`}
    <dl class="facts">
      <div><dt>Kritisch für die EU</dt><dd class="${r.kritisch ? 'yes' : ''}">${r.kritisch ? 'ja, laut Verordnung (EU) 2024/1252' : r.kritisch === false ? 'nein' : 'unbekannt'}</dd></div>
      <div><dt>Farbe im Bild</dt><dd>${esc(CLASSES[r.art]?.label ?? '')}</dd></div>
    </dl>`, [{ label: obj.name, href: `#kat=${obj.id}` }, { label: r.name }]);
  document.querySelectorAll('[data-stufe2]').forEach((b) => b.addEventListener('click', () => { stufe = b.dataset.stufe2; aktualisiere(); }));
  document.querySelectorAll('.mrow.land[data-land]').forEach((z) => {
    z.addEventListener('pointerenter', () => globus.hebeHervor(z.dataset.land));
    z.addEventListener('pointerleave', () => globus.hebeHervor(null));
  });
  if (ankuendigung) { sessionStorage.setItem('atlas-hinweis', 'aus'); document.getElementById('hinweis').hidden = true; }
}

// ---------- Navigation über den Hash, wie die Station: #kat=<id>[&r=<rohstoff>] ----------
function ausHash() {
  const p = new URLSearchParams(location.hash.slice(1));
  const o = objektVon.get(p.get('kat'));
  const r = p.get('r');
  if (o) zeigeObjekt(o, r && o.rohstoffe.some((x) => x.key === r) ? r : null);
  else { obj = null; zeigeKatalog(); }
}
addEventListener('hashchange', ausHash);
addEventListener('keydown', (e) => { if (e.key === 'Escape' && obj) location.hash = gewaehlt ? `kat=${obj.id}` : ''; });
ausHash();
