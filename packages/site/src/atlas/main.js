// Lebensweg: ein Gegenstand, sieben Stationen. Links das Bild (Globus, 3D-Modell, Balken), rechts das Datenblatt.
// Regel: Jede Zahl trägt einen Beleg (Chip „Quelle“) oder ist als „Schätzung“ markiert.
import { shell, esc, zahl, gramm, datum, SCHRITTE, icon, chip, schaetzung, quelleUrl, WEG_ICON } from '../shell.js';
import { CLASSES, MATERIALS } from '../../../../js/data/catalog.js';
import daten from '../daten/atlas.json';
import { waehlerHtml, verbindeWaehler } from '../waehler.js';
import { zeichneStoffstrom } from './stoffstrom.js';
import { erzeugeGlobus } from './globus.js';
import { erzeugeViewer, ladeModell, materialVon } from '../viewer.js';
import { bestand, plus, bauteile, stand, postenName, geschaetzt } from '../werkbank.js';
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
const belegStufe = (st, was) => chip(quelleUrl(QUELLE, st.quelle, st.pdf_seite), QUELLE[st.quelle]?.titel ?? st.quelle, 'Quelle',
  { was, von: QUELLE[st.quelle]?.herausgeber, jahr: st.jahr, seite: st.seite });
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
      <h1 class="lw-frage" id="frage"></h1>
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
  // Wischen über dem Datenblatt wechselt die Station (das Bild darüber bleibt drehbar)
  let wisch = null;
  const pan = document.getElementById('panel');
  pan.addEventListener('touchstart', (e) => { wisch = [e.touches[0].clientX, e.touches[0].clientY]; }, { passive: true });
  pan.addEventListener('touchend', (e) => {
    if (!wisch) return;
    const dx = e.changedTouches[0].clientX - wisch[0], dy = e.changedTouches[0].clientY - wisch[1];
    wisch = null;
    if (Math.abs(dx) < 60 || Math.abs(dx) < Math.abs(dy) * 1.5) return;
    const i = IDS.indexOf(schritt), j = i + (dx < 0 ? 1 : -1);
    if (j >= 0 && j < IDS.length) location.hash = link(IDS[j], null);
  }, { passive: true });
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
  document.getElementById('zurueck').href = i > 0 ? link(IDS[i - 1], null) : '../';
  document.getElementById('zurueck').innerHTML = `<span class="pfeil">←</span>${i > 0 ? SCHRITTE[i - 1].name : 'Anderer Gegenstand'}`;
  document.getElementById('weiter').href = i < IDS.length - 1 ? link(IDS[i + 1], null) : link(IDS[0], null);
  document.getElementById('weiter').innerHTML = `${i < IDS.length - 1 ? SCHRITTE[i + 1].name : 'Von vorn'}<span class="pfeil">→</span>`;
  localStorage.setItem('lebensweg-letzt', o.id);
  document.getElementById('ort').innerHTML = `<b>${esc(o.name)}</b> <span>· ${i + 1} / ${IDS.length}</span>`;
  if (neu || !seed) { seed = await ladeModell(o.id); viewer.lade(seed); }
  viewer.nummern(s === 'gegenstand');
  ({ abbau: zeigeRohstoffe, verarbeitung: zeigeRohstoffe, herstellung: zeigeHerstellung, gegenstand: zeigeGegenstand,
    upcycling: zeigeUpcycling, entsorgung: zeigeEntsorgung, verwertung: zeigeVerwertung })[s]();
}

// ---------- Datenblatt ----------
// Aufklappbarer Block: auf dem Handy zu (nur die Antwort ist sichtbar), auf großen Bildschirmen immer offen
const breit = matchMedia('(min-width: 901px)');
const block = (titel, inhalt, k = '') => `<details class="lw-block ${k}" data-block><summary>${titel}</summary><div class="lw-block-inhalt">${inhalt}</div></details>`;
const alleLaender = (anteile, rest) => `${Object.entries(anteile).sort((a, b) => b[1] - a[1]).map(landZeile).join('')}${rest ? `<div class="lw-land rest"><span class="nr">··</span><span>Andere</span><b>${rest} %</b><div class="mbar"><b style="width:${rest}%"></b></div></div>` : ''}`;
const spitze = (anteile) => Object.entries(anteile ?? {}).sort((a, b) => b[1] - a[1])[0];
const panel = () => document.getElementById('panel');
function setzePanel(html) {
  const s = SCHRITTE.find((x) => x.id === schritt);
  document.getElementById('frage').textContent = s.frage;
  const strom = document.getElementById('strom');
  if (strom && panel().contains(strom)) document.querySelector('.lw-strom').append(strom);
  const i = IDS.indexOf(schritt), naechste = SCHRITTE[(i + 1) % IDS.length];
  panel().innerHTML = `<div class="panel-inner">${html}<a class="lw-weiter" href="${link(naechste.id, null)}">${icon(naechste.id)}<span>${i < IDS.length - 1 ? 'Weiter' : 'Von vorn'}: ${naechste.name}</span><span class="pfeil">→</span></a></div>`;
  panel().scrollTop = 0;
  if (breit.matches) panel().querySelectorAll('[data-block]').forEach((d) => { d.open = true; });
}
const legende = (eintraege) => { document.getElementById('legende').innerHTML = eintraege.map(([f, t]) => `<span><i style="background:${f}"></i>${esc(t)}</span>`).join(''); };
const landZeile = ([l, p], i) => `
  <div class="lw-land" data-land="${l}"><span class="nr">${String(i + 1).padStart(2, '0')}</span><span>${esc(land(l))}</span><b>${p} %</b><div class="mbar"><b style="width:${p}%"></b></div></div>`;
// Antwort zuerst: die drei größten Länder, der Rest aufklappbar
const laenderListe = (anteile, rest) => {
  const z = Object.entries(anteile).sort((a, b) => b[1] - a[1]);
  const restZeile = rest ? `<div class="lw-land rest"><span class="nr">··</span><span>Andere</span><b>${rest} %</b><div class="mbar"><b style="width:${rest}%"></b></div></div>` : '';
  return `${z.slice(0, 3).map(landZeile).join('')}${z.length > 3 ? `<details class="lw-alle"><summary>Alle ${z.length} Länder</summary>${z.slice(3).map((e, i) => landZeile(e, i + 3)).join('')}${restZeile}</details>` : restZeile}`;
};
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
    <label class="lw-wahl-liste"><span>Rohstoff</span><select id="rohstoff-wahl">${obj.rohstoffe.map((x) => `<option value="${x.key}" ${x.key === gewaehlt ? 'selected' : ''}>${esc(rohstoff(x.key).name)}${stufeDaten(x.key, schritt) ? '' : ' (keine Daten)'}</option>`).join('')}</select></label>
    <div class="lw-chips">${obj.rohstoffe.map((x) => {
      const y = rohstoff(x.key), da = !!stufeDaten(x.key, schritt);
      return `<a href="${link(schritt, x.key)}" class="lw-chip ${x.key === gewaehlt ? 'on' : ''} ${da ? '' : 'leer'}" title="${da ? '' : 'Keine Länderdaten'}">
        <i style="background:${y.farbe}"></i>${esc(y.name)}</a>`;
    }).join('')}</div>
    ${r ? `<div class="lw-zahl"><b>${gramm(menge)}</b><span>${esc(r.name)} im Gegenstand${st && spitze(st.anteile) ? ` · meist aus ${esc(land(spitze(st.anteile)[0]))} (${spitze(st.anteile)[1]} %)` : ''}${r.kritisch ? ` · <em class="krit">▲ kritisch für die EU</em>${chip(quelleUrl(QUELLE, ROH[gewaehlt].kritisch_quelle, ROH[gewaehlt].kritisch_pdf_seite), 'Verordnung (EU) 2024/1252, Anhang II', 'Quelle', { was: `${r.name} steht auf der EU-Liste kritischer Rohstoffe`, jahr: 2024 })}` : ''}</span>${schaetzung('tools/kategorien/rohstoffe.py', 'Aus dem 3D-Modell berechnet')}</div>` : ''}
    ${st ? block(`Länder ${belegStufe(st, `${r.name} · ${SCHRITTE.find((x) => x.id === schritt).name}: ${land(spitze(st.anteile)[0])} ${spitze(st.anteile)[1]} %`)}`, `${alleLaender(st.anteile, st.rest)}<p class="lw-fuss">${esc(st.jahr ?? '')} · ${esc(QUELLE[st.quelle]?.herausgeber ?? QUELLE[st.quelle]?.titel ?? '')}</p>`)
    : `<p class="note">Keine Länderdaten mit Quelle.</p>`}
    <details class="lw-fluss lw-block" id="fluss"><summary>Woher kommt was?</summary><div class="lw-fluss-ort"></div></details>`);
  verbindeLaender();
  document.getElementById('rohstoff-wahl').addEventListener('change', (e) => { location.hash = link(schritt, e.target.value); });
  const fluss = document.getElementById('fluss');
  fluss.addEventListener('toggle', () => {
    if (!fluss.open) return;
    fluss.querySelector('.lw-fluss-ort').append(document.getElementById('strom'));
    requestAnimationFrame(() => zeichneStrom());
  });
}

// ---------- 3: Herstellung ----------
function zeigeHerstellung() {
  const im = IMP?.objekte?.[obj.id];
  globus.zeige(im?.anteile ?? {});
  legende([]);
  setzePanel(im?.anteile ? `
    <div class="lw-zahl"><b>${spitze(im.anteile)[1]} %</b><span>aus ${esc(land(spitze(im.anteile)[0]))}, nach Wert der Importe nach Deutschland</span>${chip(im.api_url ?? IMP.quelle?.url, IMP.quelle?.titel ?? 'UN Comtrade', 'Quelle', { was: `Importe nach Deutschland: ${land(spitze(im.anteile)[0])} ${spitze(im.anteile)[1]} %`, von: IMP.quelle?.herausgeber, jahr: im.jahr })}</div>
    ${block('Länder', `${alleLaender(im.anteile, im.rest)}<p class="lw-fuss">${esc(im.jahr)} · nach Wert der Importe</p>`)}
      ${im.zuordnung === 'breit' ? `<p class="note">Die Zahlen gelten für eine größere Warengruppe, zu der dieser Gegenstand gehört.</p>` : ''}</div>`
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
    ${bestand()[obj.id] ? `<div class="lw-habich-da"><span>Auf deiner Werkbank</span><span class="wb-stepper"><button data-d="-1" aria-label="weniger">−</button><b>${bestand()[obj.id]}</b><button data-d="1" aria-label="mehr">+</button></span></div>`
      : '<button class="btn ghost lw-habich" id="habich"><span class="pfeil">+</span>Hab ich, auf die Werkbank</button>'}
    <div><div class="mix">${sortiert.map(([c, g]) => `<i style="width:${(g / gesamt) * 100}%;background:${CLASSES[c]?.color}"></i>`).join('')}</div>
      <div class="mix-legend">${sortiert.map(([c, g]) => `<span><i style="background:${CLASSES[c]?.color}"></i>${esc(CLASSES[c]?.label)}<b>${zahl((g / gesamt) * 100, 0)} %</b></span>`).join('')}</div></div>
    ${block(`${seed.parts.length} Teile`, `<div class="plist">${viewer.teile.map((t) => `<button class="prow" data-i="${t.i}"><span class="n">${t.nr ?? '–'}</span>
        <span>${esc(t.p.name)}<small>${esc(materialVon(t.p)?.name ?? '')}</small></span><span class="m">${gramm(t.p.mass)}</span></button>`).join('')}</div>`)}`);
  document.getElementById('habich')?.addEventListener('click', () => { plus(obj.id); zeigeGegenstand(); });
  panel().querySelectorAll('.lw-habich-da button').forEach((b) => b.addEventListener('click', () => { plus(obj.id, +b.dataset.d); zeigeGegenstand(); }));
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
    <div class="lw-zahl"><b>${gramm(p.mass)}</b><span>${esc(p.name)}</span></div>
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
  // Rezepte, die ein Bauteil dieses Gegenstands nutzen; Stand wie auf der Werkbank (mit diesem Gegenstand dazu)
  const cids = new Set(obj.teile.map((t) => t.cid));
  const mitDiesem = { ...bauteile(objektVon) };
  if (!bestand()[obj.id]) for (const c of cids) mitDiesem[c] = (mitDiesem[c] ?? 0) + 1;
  const passend = (REZEPTE ?? []).filter((r) => (r.braucht ?? []).some((b) => [b.component_id, ...(b.oder ?? [])].some((c) => cids.has(c))))
    .map((r) => ({ r, s: stand(r, mitDiesem) })).sort((a, b) => b.s.ok / b.s.alle - a.s.ok / a.s.alle);
  const name = (cid) => daten.komponenten?.[cid]?.name ?? cid;
  setzePanel(passend.length ? `<div class="lw-rezepte">${passend.map(({ r, s }) => `
    <article class="lw-rezept"><div class="lw-rezept-kopf"><h2>${esc(r.titel)}</h2>${s.baubar ? `<span class="haken" title="Alles da">${icon('haken')}</span>` : ''}</div>
      <div class="uses">${s.posten.map((p) => `<div class="use ${p.ok ? 'da' : 'fehlt'}"><i></i><span title="${esc(postenName(p, mitDiesem, name).alle)}">${esc(postenName(p, mitDiesem, name).text)}${postenName(p, mitDiesem, name).mehr ? ` <small>+${postenName(p, mitDiesem, name).mehr}</small>` : ''}</span><span class="q">${p.soll > 1 ? `${geschaetzt(p) ? '≈' : ''}${p.soll}×` : ''}</span></div>`).join('')}</div>
      <p class="lw-fuss">${esc(r.dauer ?? '')}${chip(r.quelle?.url, r.quelle?.titel, 'Quelle', { was: `Anleitung: ${r.titel}` })}</p></article>`).join('')}</div>
    <a class="btn ghost" href="../werkbank/#bauen">${icon('werkbank')}Werkbank<span class="pfeil">→</span></a>`
    : `<p class="note">${REZEPTE?.length ? 'Noch keine Bauidee nutzt Teile dieses Gegenstands.' : 'Die Bauideen werden gerade geschrieben.'}</p>`);
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
  // Orientierung auf der Karte (keine Daten): Lübeck und Hamburg grenzen an das AWSH-Gebiet
  globus.region(AWSH.recyclinghoefe, [{ name: 'Lübeck', lat: 53.8655, lng: 10.6866 }, { name: 'Hamburg', lat: 53.5511, lng: 9.9937 }]);
  setzePanel(`
    <div class="lw-tonne" style="--f:${WEG_FARBE[e.weg]}"><i>${icon(WEG_ICON[e.weg] ?? 'tonne')}</i><div><b>${esc(w?.name ?? e.weg)}${chip(e.url, 'AWSH Abfall-ABC', 'Quelle', { was: `${obj.name}: ${w?.name ?? e.weg}`, von: 'Abfallwirtschaft Südholstein (AWSH)' })}</b><span>${esc(w?.kurz ?? '')}</span></div></div>
    ${e.hinweis ? `<p class="lw-hinweis">${esc(e.hinweis)}</p>` : ''}
    ${(e.teile ?? []).length ? block('Getrennt entsorgen', `${e.teile.map((t) => `<div class="lw-teil" style="--f:${WEG_FARBE[t.weg]}"><i>${icon(WEG_ICON[t.weg] ?? 'tonne')}</i><span>${esc(obj.teile.find((x) => x.cid === t.component_id)?.name ?? daten.komponenten?.[t.component_id]?.name ?? t.component_id)}</span><b>${esc(AWSH.wege[t.weg]?.name ?? t.weg)}</b></div>`).join('')}`) : ''}
    ${e.unsicher ? `<p class="note">AWSH nennt den Gegenstand nicht direkt. Zuordnung nach der Regel für sein Material.</p>` : ''}
    ${hof ? `<details class="lw-block lw-hof"><summary>${AWSH.recyclinghoefe.length} Recyclinghöfe ${chip('https://www.awsh.de/recyclinghoefe/uebersicht/', 'AWSH Recyclinghöfe', 'Quelle', { was: 'Adressen der Recyclinghöfe', von: 'Abfallwirtschaft Südholstein (AWSH)' })}</summary><div class="lw-hoefe">${AWSH.recyclinghoefe.map((h) => `
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
      <div class="lw-saeule">${teile.map(([k, , f]) => `<i style="flex-basis:${s[k]}%;background:${f}"></i>`).join('')}${rest >= 0.1 ? `<i class="rest" style="flex-basis:${rest}%"></i>` : ''}</div>
      <div class="lw-saeule-text">${(() => { let unten = 0; return [...teile.map(([k, n, f]) => [s[k], n, f, '']), ...(rest >= 0.1 ? [[rest, 'sonstiges, nicht ausgewiesen', 'var(--rule)', 'rest']] : [])]
        .map(([v, n, f, k]) => { const m = unten + v / 2; unten += v; return `<p class="${k}" style="--f:${f};bottom:${m}%"><b>${zahl(v)} %</b>${n}</p>`; }).join(''); })()}</div></div>`
    : '<p class="lw-leer">Keine amtliche Zahl</p>';
  setzePanel(s ? `
    <div class="lw-zahl"><b>${zahl(s.recycelt ?? s.sammelquote ?? 0)} %</b><span>${s.recycelt != null ? 'recycelt' : 'gesammelt'} · gilt für: ${esc(s.name)}</span>${chip(s.url ?? q?.url, q?.titel, 'Quelle', { was: `${s.name}: ${zahl(s.recycelt ?? s.sammelquote ?? 0)} % ${s.recycelt != null ? 'recycelt' : 'gesammelt'}`, von: q?.herausgeber, jahr: s.jahr })}</div>
    ${e.weg === 'pfand' ? `<p class="note">Pfandflaschen und -dosen werden getrennt zurückgenommen. Eine eigene amtliche Quote dafür enthält diese Quelle nicht.</p>` : ''}
    ${s.sammelquote != null && s.recycelt != null ? `<p class="lw-hinweis">Aber nur ${zahl(s.sammelquote)} % werden überhaupt gesammelt.</p>` : ''}
    <p class="lw-fuss">Deutschland · ${esc(s.jahr)} · ${esc(q?.herausgeber ?? '')}</p>
    ${block('Was genau gezählt wird', `<p>${esc(s.was ?? '')}</p>`)}`
    : `<p class="note">${e ? 'Für diesen Entsorgungsweg gibt es keine amtliche Zahl.' : 'Keine Daten.'}</p>`);
}

// ---------- Navigation über den Hash: #kat=<id>&s=<schritt>&r=<rohstoff> ----------
function ausHash() {
  const p = new URLSearchParams(location.hash.slice(1));
  const o = objektVon.get(p.get('kat'));
  if (!o) return location.replace(`#kat=${objektVon.has(localStorage.getItem('lebensweg-letzt')) ? localStorage.getItem('lebensweg-letzt') : 'smartphone'}`);
  zeige(o, IDS.includes(p.get('s')) ? p.get('s') : 'abbau', p.get('r'));
}
addEventListener('hashchange', ausHash);
addEventListener('keydown', (e) => {
  if (!obj || e.target.closest('input')) return;
  const i = IDS.indexOf(schritt);
  if (e.key === 'ArrowRight' && i < IDS.length - 1) location.hash = link(IDS[i + 1], null);
  if (e.key === 'ArrowLeft' && i > 0) location.hash = link(IDS[i - 1], null);
});
ausHash();
