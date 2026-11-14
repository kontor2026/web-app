// Lebensweg: ein Gegenstand, sieben Stationen. Links das Bild (Globus, 3D-Modell, Balken), rechts das Datenblatt.
// Regel: Jede Zahl trägt einen Beleg (Chip „Quelle“) oder ist als „Schätzung“ markiert.
import { shell, esc, zahl, gramm, datum, SCHRITTE, icon, chip, schaetzung, quelleUrl, repoUrl } from '../shell.js';
import { CLASSES, MATERIALS } from '../../../../js/data/catalog.js';
import daten from '../daten/atlas.json';
import { waehlerHtml, verbindeWaehler } from '../waehler.js';
import { zeichneStoffstrom } from './stoffstrom.js';
import { erzeugeGlobus } from './globus.js';
import { erzeugeViewer, ladeModell, materialVon } from '../viewer.js';
import './atlas.css';

const { objekte, rohstoffe: ROH, materialien: MAT, laender: LAND, quellen: QUELLE, awsh: AWSH, verwertung: VW, importe: IMP, rezepte: REZEPTE } = daten;
const objektVon = new Map(objekte.map((o) => [o.id, o]));
const IDS = SCHRITTE.map((s) => s.id);

const material = (mid) => {
  const k = MATERIALS[MAT[mid]?.kat];
  return { name: k?.name ?? MAT[mid]?.en ?? mid, farbe: CLASSES[k?.cls]?.color ?? '#cccccc', cls: k?.cls };
};
const rohstoff = (key) => ({ ...ROH[key], key, farbe: CLASSES[ROH[key]?.art]?.color ?? '#cccccc' });
const land = (a3) => LAND[a3]?.name ?? a3;
const stufeDaten = (key, stufe) => ROH[key]?.[stufe] ?? null;
const belegStufe = (st) => chip(quelleUrl(QUELLE, st.quelle, st.pdf_seite), `${QUELLE[st.quelle]?.titel ?? st.quelle}${st.seite ? `, ${st.seite}` : ''}`);
const CSV = 'tools/kategorien/kategorien.csv';

// Farben der Entsorgungswege: nur zur Unterscheidung im Bild, keine Tonnenfarben
const WEG_FARBE = { wertstofftonne: '#E3C14A', papier: '#7FA3C8', glas: '#8DB89A', bio: '#A88B5E', restmuell: '#8D918A', elektro: '#5B8C99',
  lampen: '#E38B5A', batterie: '#9C97B5', schadstoff: '#B5473A', sperrmuell: '#6E7378', textil: '#C9A3B9', pfand: '#5E9C8F', recyclinghof: '#4F5A66' };
// Entsorgungsweg → Datenreihe zur Verwertung (bei Wertstofftonne und Pfand nach Hauptmaterial)
function verwertungsStrom(weg, o) {
  const cls = material(o.materialien[0]?.mid).cls, mid = o.materialien[0]?.mid;
  const nachMaterial = mid === 'aluminium' ? 'verpackung_alu' : mid === 'steel' ? 'verpackung_stahl' : cls === 'glas' ? 'verpackung_glas' : 'verpackung_kunststoff';
  return { wertstofftonne: nachMaterial, pfand: nachMaterial, papier: 'verpackung_papier', glas: 'verpackung_glas', elektro: 'elektro', lampen: 'elektro',
    batterie: 'batterie', restmuell: 'restmuell', bio: 'bio', sperrmuell: 'sperrmuell', textil: 'textil' }[weg] ?? null;
}

const app = shell('atlas', '../');
let obj = null, schritt = 'gegenstand', gewaehlt = null, globus = null, viewer = null, strom = null, seed = null;

// ---------- Ohne Gegenstand: wählen ----------
function zeigeWahl() {
  obj = null;
  document.title = 'Lebensweg · Kreislauf-Station';
  app.innerHTML = `<section class="view lw-wahl"><div class="lw-wahl-inhalt">
    <h1>Welchen Gegenstand?</h1>${waehlerHtml(objekte, (id) => `#kat=${id}`)}</div></section>`;
  verbindeWaehler(app.querySelector('.waehler'));
}

// ---------- Gerüst der Ansicht ----------
function baueGeruest() {
  app.innerHTML = `
  <section class="view sheet lw">
    <div class="canvas">
      <nav class="lw-schritte" aria-label="Lebensweg">${SCHRITTE.map((s, i) => `
        <a href="#" data-s="${s.id}" title="${s.name}" aria-label="${i + 1}. ${s.name}"><span class="lw-nr">${i + 1}</span>${icon(s.id)}<span class="lw-name">${s.name}</span></a>`).join('')}
      </nav>
      <div class="lw-buehne">
        <div class="lw-globus" id="globus"></div>
        <div class="lw-szene" id="szene"></div>
        <div class="lw-balken" id="balken"></div>
        <div class="lw-strom"><div class="strom" id="strom"></div></div>
      </div>
      <div class="legend" id="legende"></div>
    </div>
    <aside class="panel" id="panel"></aside>
    <div class="actionbar">
      <a class="btn ghost" id="zurueck" href="#">←</a>
      <div class="q" id="ort"></div>
      <a class="btn" id="weiter" href="#">→</a>
    </div>
  </section>`;
  globus = erzeugeGlobus(document.getElementById('globus'), LAND);
  viewer = erzeugeViewer(document.getElementById('szene'), {
    tip: document.getElementById('tip'),
    onHover: (i) => panelHover(i),
    onSelect: (i) => { if (schritt === 'gegenstand') zeigeTeil(i); },
  });
  new ResizeObserver(() => { if (schritt === 'abbau' || schritt === 'verarbeitung') zeichneStrom(); }).observe(document.getElementById('strom'));
}

const link = (s = schritt, r = gewaehlt) => `#kat=${obj.id}&s=${s}${r ? `&r=${r}` : ''}`;

async function zeige(o, s, r) {
  const neu = obj !== o;
  if (!document.querySelector('.lw')) baueGeruest();
  obj = o; schritt = s; gewaehlt = r;
  document.title = `${o.name} · Lebensweg`;
  const i = IDS.indexOf(s);
  document.querySelectorAll('.lw-schritte a').forEach((a, j) => {
    a.href = link(IDS[j], null); a.classList.toggle('on', j === i); a.toggleAttribute('aria-current', j === i);
  });
  document.querySelector('.lw').dataset.schritt = s;
  document.getElementById('zurueck').href = i > 0 ? link(IDS[i - 1], null) : '#';
  document.getElementById('zurueck').innerHTML = i > 0 ? `← ${SCHRITTE[i - 1].name}` : '← Gegenstand wählen';
  document.getElementById('weiter').href = i < IDS.length - 1 ? link(IDS[i + 1], null) : link(IDS[0], null);
  document.getElementById('weiter').innerHTML = i < IDS.length - 1 ? `${SCHRITTE[i + 1].name} →` : 'Von vorn →';
  document.getElementById('ort').innerHTML = `<b>${esc(o.name)}</b> <span>· ${i + 1} / ${IDS.length}</span>`;
  if (neu || !seed) { seed = await ladeModell(o.id); viewer.lade(seed); }
  viewer.nummern(s === 'gegenstand');
  ({ abbau: zeigeRohstoffe, verarbeitung: zeigeRohstoffe, herstellung: zeigeHerstellung, gegenstand: zeigeGegenstand,
    upcycling: zeigeUpcycling, entsorgung: zeigeEntsorgung, verwertung: zeigeVerwertung })[s]();
}

// ---------- Datenblatt ----------
const panel = () => document.getElementById('panel');
function setzePanel(html) {
  const s = SCHRITTE.find((x) => x.id === schritt);
  panel().innerHTML = `<div class="panel-inner"><div class="lw-kopf">
      <div class="eyebrow">${icon(schritt)}${s.name}</div><h1>${esc(s.frage)}</h1></div>${html}</div>`;
  panel().scrollTop = 0;
}
const legende = (eintraege) => { document.getElementById('legende').innerHTML = eintraege.map(([f, t]) => `<span><i style="background:${f}"></i>${esc(t)}</span>`).join(''); };
const laenderListe = (anteile, rest) => `${Object.entries(anteile).sort((a, b) => b[1] - a[1]).map(([l, p], i) => `
  <div class="lw-land" data-land="${l}"><span class="nr">${String(i + 1).padStart(2, '0')}</span><span>${esc(land(l))}</span><b>${p} %</b><div class="mbar"><b style="width:${p}%"></b></div></div>`).join('')}
  ${rest ? `<div class="lw-land rest"><span class="nr">··</span><span>Andere</span><b>${rest} %</b><div class="mbar"><b style="width:${rest}%"></b></div></div>` : ''}`;
function verbindeLaender() {
  panel().querySelectorAll('.lw-land[data-land]').forEach((z) => {
    z.addEventListener('pointerenter', () => globus.hebeHervor(z.dataset.land));
    z.addEventListener('pointerleave', () => globus.hebeHervor(null));
  });
}

// ---------- 1 + 2: Abbau und Verarbeitung ----------
function zeichneStrom() {
  strom = zeichneStoffstrom(document.getElementById('strom'), obj, {
    teilName: (t) => t.name, material, rohstoff,
    onHover: (id, typ) => { if (typ === 'rohstoff') globus.zeige(stufeDaten(id ?? gewaehlt, schritt)?.anteile ?? {}, { fokus: false }); },
    onClick: (id, typ) => { if (typ === 'rohstoff') location.hash = link(schritt, id); },
  });
  strom.markiere(gewaehlt);
}
function zeigeRohstoffe() {
  const mitDaten = obj.rohstoffe.filter((r) => stufeDaten(r.key, schritt));
  if (!gewaehlt || !obj.rohstoffe.some((r) => r.key === gewaehlt)) gewaehlt = (mitDaten[0] ?? obj.rohstoffe[0])?.key ?? null;
  zeichneStrom();
  const r = gewaehlt && rohstoff(gewaehlt), st = gewaehlt && stufeDaten(gewaehlt, schritt), menge = obj.rohstoffe.find((x) => x.key === gewaehlt)?.g;
  globus.zeige(st?.anteile ?? {});
  legende([]);
  setzePanel(`
    <div class="lw-chips">${obj.rohstoffe.map((x) => {
      const y = rohstoff(x.key), da = !!stufeDaten(x.key, schritt);
      return `<a href="${link(schritt, x.key)}" class="lw-chip ${x.key === gewaehlt ? 'on' : ''} ${da ? '' : 'leer'}" title="${da ? '' : 'Keine Länderdaten'}">
        <i style="background:${y.farbe}"></i>${esc(y.name)}</a>`;
    }).join('')}</div>
    ${r ? `<div class="lw-zahl"><b>${gramm(menge)}</b><span>${esc(r.name)} im Gegenstand${r.kritisch ? ` · <em class="krit">▲ kritisch für die EU</em>${chip(quelleUrl(QUELLE, ROH[gewaehlt].kritisch_quelle, ROH[gewaehlt].kritisch_pdf_seite), 'Verordnung (EU) 2024/1252, Anhang II')}` : ''}</span>${schaetzung('tools/kategorien/rohstoffe.py', 'Aus den Massen des 3D-Modells berechnet')}</div>` : ''}
    ${st ? `<div><h3>Nach Land ${belegStufe(st)}</h3>${laenderListe(st.anteile, st.rest)}
      <p class="lw-fuss">${esc(st.jahr ?? '')} · ${esc(QUELLE[st.quelle]?.herausgeber ?? QUELLE[st.quelle]?.titel ?? '')}</p></div>`
    : `<p class="note">Keine Länderdaten mit Quelle.</p>`}`);
  verbindeLaender();
}

// ---------- 3: Herstellung ----------
function zeigeHerstellung() {
  const im = IMP?.objekte?.[obj.id];
  globus.zeige(im?.anteile ?? {});
  legende([]);
  setzePanel(im?.anteile ? `
    <div><h3>Importe nach Deutschland ${chip(im.api_url ?? IMP.quelle?.url, `${IMP.quelle?.titel ?? 'UN Comtrade'}, HS ${im.hs}`)}</h3>${laenderListe(im.anteile, im.rest)}
      <p class="lw-fuss">${esc(im.jahr)} · nach Importwert · HS ${esc(im.hs)}</p>
      ${im.zuordnung === 'breit' ? `<p class="note">Die Zollnummer umfasst auch andere Waren. Die Länder gelten für die ganze Warengruppe.</p>` : ''}
      ${im.hinweis ? `<details class="lw-mehr"><summary>Zur Zollnummer</summary><p>${esc(im.hinweis)}</p><p>HS ${esc(im.hs)}: ${esc(im.hs_text ?? '')}</p></details>` : ''}</div>`
    : `<p class="note">${IMP ? 'Für diesen Gegenstand gibt es keine passende Zollnummer.' : 'Die Importdaten werden gerade zusammengestellt.'}</p>`);
  verbindeLaender();
}

// ---------- 4: Gegenstand ----------
function zeigeGegenstand() {
  viewer.faerbe(null);
  viewer.waehle(null);
  const klassen = [...new Set(seed.parts.map((p) => materialVon(p)?.cls).filter(Boolean))];
  legende(klassen.map((c) => [CLASSES[c].color, CLASSES[c].label]));
  const gesamt = obj.materialien.reduce((s, m) => s + m.g, 0) || 1;
  const mix = new Map();
  for (const m of obj.materialien) { const c = material(m.mid).cls ?? 'metall'; mix.set(c, (mix.get(c) ?? 0) + m.g); }
  const sortiert = [...mix].sort((a, b) => b[1] - a[1]);
  setzePanel(`
    <div class="lw-zahl"><b>${gramm(obj.gramm)}</b><span>${esc(obj.name)}</span>${schaetzung(CSV, 'Typisches Gewicht, eigene Schätzung')}</div>
    <div><div class="mix">${sortiert.map(([c, g]) => `<i style="width:${(g / gesamt) * 100}%;background:${CLASSES[c]?.color}"></i>`).join('')}</div>
      <div class="mix-legend">${sortiert.map(([c, g]) => `<span><i style="background:${CLASSES[c]?.color}"></i>${esc(CLASSES[c]?.label)}<b>${zahl((g / gesamt) * 100, 0)} %</b></span>`).join('')}</div></div>
    <div><h3>${seed.parts.length} Teile ${chip(repoUrl(`tools/kategorien/modelle/${obj.id}.json`), '3D-Modell im Repository', 'Modell')}</h3>
      <div class="plist">${viewer.teile.map((t) => `<button class="prow" data-i="${t.i}"><span class="n">${t.nr ?? '–'}</span>
        <span>${esc(t.p.name)}<small>${esc(materialVon(t.p)?.name ?? '')}</small></span><span class="m">${gramm(t.p.mass)}</span></button>`).join('')}</div></div>`);
  panel().querySelectorAll('.prow').forEach((b) => {
    b.addEventListener('pointerenter', () => viewer.markiere(+b.dataset.i));
    b.addEventListener('pointerleave', () => viewer.markiere(null));
    b.addEventListener('click', () => { viewer.waehle(+b.dataset.i); zeigeTeil(+b.dataset.i); });
  });
}
function zeigeTeil(i) {
  if (i == null) return zeigeGegenstand();
  const p = viewer.teile[i].p;
  setzePanel(`
    <nav class="crumbs"><button id="zu">${esc(obj.name)}</button><span></span><b style="font-weight:500;color:var(--ink)">${esc(p.name)}</b></nav>
    <div class="lw-zahl"><b>${gramm(p.mass)}</b><span>${esc(p.name)}</span>${chip(repoUrl(`tools/kategorien/modelle/${obj.id}.json`), '3D-Modell im Repository', 'Modell')}</div>
    <div><h3>Material</h3>${(p.materials ?? []).map(([m, a]) => `
      <div class="mrow"><i style="background:${CLASSES[MATERIALS[m]?.cls]?.color ?? '#ccc'}"></i><span>${esc(MATERIALS[m]?.name ?? m)}</span>
        <span class="pct">${a} %</span><span></span><div class="mbar"><b style="width:${a}%"></b></div></div>`).join('')}</div>`);
  document.getElementById('zu').addEventListener('click', () => zeigeGegenstand());
}
function panelHover(i) {
  panel()?.querySelectorAll('.prow').forEach((r) => r.classList.toggle('hot', +r.dataset.i === i));
}

// ---------- 5: Upcycling ----------
function zeigeUpcycling() {
  viewer.faerbe(null);
  viewer.waehle(null);
  legende([]);
  const cids = new Set(obj.teile.map((t) => t.cid)), mids = new Set(obj.materialien.map((m) => m.mid));
  const passend = (REZEPTE ?? []).filter((r) => (r.component_ids ?? []).some((c) => cids.has(c)) || (r.material_ids ?? []).some((m) => mids.has(m)));
  setzePanel(passend.length ? `<div class="lw-rezepte">${passend.map((r) => `
    <article class="lw-rezept"><h2>${esc(r.titel)}</h2>
      <div class="meta"><span>${esc(r.dauer ?? '')}</span><span class="dots">${'●'.repeat(r.stufe ?? 1)}${'○'.repeat(3 - (r.stufe ?? 1))}</span></div>
      <ol class="steps-list">${(r.schritte ?? []).map((s) => `<li>${esc(s)}</li>`).join('')}</ol>
      ${r.sicherheit ? `<p class="note warn">${esc(r.sicherheit)}</p>` : ''}
      <p class="lw-fuss">${esc(r.quelle?.titel ?? '')}${chip(r.quelle?.url, r.quelle?.titel)}</p></article>`).join('')}</div>`
    : `<p class="note">Rezepte für diesen Gegenstand werden gerade geschrieben.</p>`);
}

// ---------- 6: Entsorgung ----------
function zeigeEntsorgung() {
  const e = AWSH?.objekte?.[obj.id];
  viewer.waehle(null);
  if (!e) { viewer.faerbe(null); legende([]); setzePanel('<p class="note">Keine Daten.</p>'); return; }
  const wegVon = new Map((e.teile ?? []).map((t) => [t.component_id, t.weg]));
  viewer.faerbe((p) => WEG_FARBE[wegVon.get(p.component_id) ?? e.weg]);
  const wege = [e.weg, ...(e.teile ?? []).map((t) => t.weg)].filter((w, i, a) => a.indexOf(w) === i);
  legende(wege.map((w) => [WEG_FARBE[w], AWSH.wege[w]?.name ?? w]));
  const w = AWSH.wege[e.weg];
  const hof = ['elektro', 'lampen', 'batterie', 'schadstoff', 'sperrmuell', 'recyclinghof'].includes(e.weg);
  setzePanel(`
    <div class="lw-tonne" style="--f:${WEG_FARBE[e.weg]}"><i></i><div><b>${esc(w?.name ?? e.weg)}${chip(e.url, 'AWSH Abfall-ABC')}</b><span>${esc(w?.kurz ?? '')}</span></div></div>
    ${e.hinweis ? `<p class="lw-hinweis">${esc(e.hinweis)}</p>` : ''}
    ${(e.teile ?? []).length ? `<div><h3>Getrennt entsorgen</h3>${e.teile.map((t) => `<div class="lw-teil" style="--f:${WEG_FARBE[t.weg]}"><i></i><span>${esc(obj.teile.find((x) => x.cid === t.component_id)?.name ?? daten.komponenten?.[t.component_id]?.name ?? t.component_id)}</span><b>${esc(AWSH.wege[t.weg]?.name ?? t.weg)}</b></div>`).join('')}</div>` : ''}
    ${e.unsicher ? `<p class="note">AWSH nennt den Gegenstand nicht direkt. Zuordnung nach der Regel für sein Material.</p>` : ''}
    ${hof ? `<details class="lw-mehr lw-hof"><summary>${AWSH.recyclinghoefe.length} Recyclinghöfe ${chip('https://www.awsh.de/recyclinghoefe/uebersicht/', 'AWSH Recyclinghöfe')}</summary><div class="lw-hoefe">${AWSH.recyclinghoefe.map((h) => `
      <a href="${esc(h.lat ? `https://www.openstreetmap.org/?mlat=${h.lat}&mlon=${h.lng}#map=16/${h.lat}/${h.lng}` : h.url)}" target="_blank" rel="noopener">
        <b>${esc(h.name.replace('Recyclinghof ', ''))}</b><span>${esc(h.adresse)}</span>${h.hinweis ? `<em>${esc(h.hinweis)}</em>` : ''}</a>`).join('')}</div></details>` : ''}
    <p class="lw-fuss">${esc(AWSH.gebiet)} · Stand ${esc(datum(AWSH.stand))}</p>`);
}

// ---------- 7: Verwertung ----------
function zeigeVerwertung() {
  const e = AWSH?.objekte?.[obj.id], key = e && verwertungsStrom(e.weg, obj), s = key && VW?.stroeme?.[key];
  legende([]);
  const teile = s ? [['recycelt', 'recycelt', 'var(--good)'], ['verbrannt', 'verbrannt, mit Energie', 'var(--ink-3)'], ['deponiert', 'deponiert', 'var(--accent)']]
    .filter(([k]) => s[k] != null) : [];
  const rest = s ? Math.max(0, 100 - teile.reduce((x, [k]) => x + s[k], 0)) : 0;
  const q = s && VW.quellen?.[s.quelle];
  document.getElementById('balken').innerHTML = s ? `<div class="lw-balken-bild">
      <div class="lw-saeule">${teile.map(([k, , f]) => `<i style="flex-basis:${s[k]}%;background:${f}"></i>`).join('')}${rest > 0.5 ? `<i class="rest" style="flex-basis:${rest}%"></i>` : ''}</div>
      <div class="lw-saeule-text">${(() => { let unten = 0; return [...teile.map(([k, n, f]) => [s[k], n, f, '']), ...(rest > 0.5 ? [[rest, 'nicht ausgewiesen', 'var(--rule)', 'rest']] : [])]
        .map(([v, n, f, k]) => { const m = unten + v / 2; unten += v; return `<p class="${k}" style="--f:${f};bottom:${m}%"><b>${zahl(v)} %</b>${n}</p>`; }).join(''); })()}</div></div>`
    : '<p class="lw-leer">Keine amtliche Zahl</p>';
  setzePanel(s ? `
    <div class="lw-zahl"><b>${zahl(s.recycelt ?? s.sammelquote ?? 0)} %</b><span>${s.recycelt != null ? 'recycelt' : 'gesammelt'} · gilt für: ${esc(s.name)}</span>${chip(s.url ?? q?.url, q?.titel)}</div>
    ${e.weg === 'pfand' ? `<p class="note">Pfandflaschen und -dosen werden getrennt zurückgenommen. Eine eigene amtliche Quote dafür enthält diese Quelle nicht.</p>` : ''}
    ${s.sammelquote != null && s.recycelt != null ? `<p class="lw-hinweis">Aber nur ${zahl(s.sammelquote)} % werden überhaupt gesammelt.</p>` : ''}
    <p class="lw-fuss">Deutschland · ${esc(s.jahr)} · ${esc(q?.herausgeber ?? '')}</p>
    <details class="lw-mehr"><summary>Was genau gezählt wird</summary><p>${esc(s.was ?? '')}</p>${s.hinweis ? `<p>${esc(s.hinweis)}</p>` : ''}</details>`
    : `<p class="note">${e ? 'Für diesen Entsorgungsweg gibt es keine amtliche Zahl.' : 'Keine Daten.'}</p>`);
}

// ---------- Navigation über den Hash: #kat=<id>&s=<schritt>&r=<rohstoff> ----------
function ausHash() {
  const p = new URLSearchParams(location.hash.slice(1));
  const o = objektVon.get(p.get('kat'));
  if (!o) return zeigeWahl();
  zeige(o, IDS.includes(p.get('s')) ? p.get('s') : 'gegenstand', p.get('r'));
}
addEventListener('hashchange', ausHash);
addEventListener('keydown', (e) => {
  if (!obj || e.target.closest('input')) return;
  const i = IDS.indexOf(schritt);
  if (e.key === 'ArrowRight' && i < IDS.length - 1) location.hash = link(IDS[i + 1], null);
  if (e.key === 'ArrowLeft' && i > 0) location.hash = link(IDS[i - 1], null);
});
ausHash();
