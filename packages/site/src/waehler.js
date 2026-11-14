// Gegenstand wählen: Suche, sechs Beispiele, alle 201 nach Gruppe. Gleich auf Start und Lebensweg.
import { esc, gramm, icon } from './shell.js';

export const BEISPIELE = ['smartphone', 'pet_bottle', 'laptop', 't_shirt', 'aluminium_can', 'hair_dryer'];

// Karte mit Piktogramm: eigenes, sonst das der Gruppe
const GRUPPE_ICON = { Elektro: 'gruppe_elektro', Verpackung: 'gruppe_verpackung', Textil: 'gruppe_textil', Alltag: 'gruppe_alltag' };
const karte = (o, href) => `<a class="beispiel" href="${href(o.id)}">${icon(BEISPIELE.includes(o.id) ? o.id : GRUPPE_ICON[o.gruppe] ?? 'gruppe_alltag', 'gross')}<b>${esc(o.name)}</b></a>`;

export function waehlerHtml(objekte, href, { alle = true } = {}) {
  const gruppen = new Map();
  for (const o of [...objekte].sort((a, b) => a.name.localeCompare(b.name, 'de')))
    (gruppen.get(o.gruppe) ?? gruppen.set(o.gruppe, []).get(o.gruppe)).push(o);
  const von = new Map(objekte.map((o) => [o.id, o]));
  return `<div class="waehler" data-objekte='${esc(JSON.stringify(objekte.map((o) => ({ id: o.id, name: o.name, gruppe: o.gruppe, gramm: o.gramm, h: href(o.id) })))).replace(/'/g, '&#39;')}'>
    <div class="suche-zeile"><input class="suche-feld" type="search" placeholder="Gegenstand suchen" autocomplete="off" aria-label="Gegenstand suchen" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="vorschlaege"><ul class="vorschlaege" id="vorschlaege" role="listbox" hidden></ul>${alle ? '' : `<button class="wuerfel" type="button" aria-label="Andere Vorschläge" title="Andere Vorschläge">${icon('wuerfeln')}</button>`}</div>
    <div class="beispiele">${(alle ? BEISPIELE : BEISPIELE.slice(0, 2)).filter((id) => von.has(id)).map((id) => karte(von.get(id), href)).join('')}</div>
    ${alle ? '' : '<!--'}<details class="alle"><summary>Alle ${objekte.length} Gegenstände</summary>
      <div class="katalog">${[...gruppen].map(([g, os]) => `<div class="gruppe"><h4 class="eyebrow">${esc(g)} · ${os.length}</h4>
        <div class="kat-list">${os.map((o) => `<a href="${href(o.id)}" class="tag" data-name="${esc(`${o.name} ${o.id}`.toLowerCase())}">${esc(o.name)}</a>`).join('')}</div></div>`).join('')}</div>
    </details>${alle ? '' : '-->'}
  </div>`;
}

// Suche filtert die Liste und klappt sie auf; Enter öffnet den ersten Treffer
export function verbindeWaehler(el) {
  const suche = el.querySelector('.suche-feld'), alle = el.querySelector('details.alle');
  verbindeVorschlaege(el, suche);
  if (!alle) return verbindeSuche(el, suche);
  suche.addEventListener('input', () => {
    const q = suche.value.trim().toLowerCase();
    alle.open = !!q || alle.open;
    el.querySelectorAll('.kat-list a').forEach((a) => { a.hidden = !!q && !a.dataset.name.includes(q); });
    el.querySelectorAll('.gruppe').forEach((g) => { g.hidden = ![...g.querySelectorAll('a')].some((a) => !a.hidden); });
  });
  suche.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' || e.defaultPrevented) return;
    const a = el.querySelector('.kat-list a:not([hidden])');
    if (a && suche.value.trim()) location.href = a.href;
  });
}

// Ohne Liste (Start): Suche zeigt Treffer direkt als Karten unter dem Feld
function verbindeSuche(el, suche) {
  const beispiele = el.querySelector('.beispiele'), alle = JSON.parse(el.dataset.objekte ?? '[]');
  const zeige = (liste) => { beispiele.innerHTML = liste.map((o) => karte(o, () => o.h)).join('') || '<p class="leer">Nichts gefunden.</p>'; };
  suche.addEventListener('input', () => { const q = suche.value.trim(); if (q) zeige(treffer(alle, q).slice(0, 2)); });
  suche.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.defaultPrevented) beispiele.querySelector('a')?.click(); });
  el.querySelector('.wuerfel')?.addEventListener('click', () => {
    suche.value = '';
    const zufall = [...alle].sort(() => Math.random() - 0.5).slice(0, 2);
    zeige(zufall);
  });
}

// Treffer nach Güte: Name beginnt mit der Eingabe, dann ein Wort im Namen, dann irgendwo; je Stufe alphabetisch
const klein = (t) => t.toLocaleLowerCase('de-DE');
export function treffer(objekte, eingabe) {
  const q = klein(eingabe.trim());
  if (!q) return [];
  const rang = (o) => { const n = klein(o.name); return n.startsWith(q) ? 0 : n.split(/[\s\-/(]+/).some((w) => w.startsWith(q)) ? 1 : n.includes(q) ? 2 : 3; };
  return objekte.map((o) => [rang(o), o]).filter(([r]) => r < 3)
    .sort((a, b) => a[0] - b[0] || a[1].name.localeCompare(b[1].name, 'de')).map(([, o]) => o);
}

// Vorschläge beim Tippen: Liste unter dem Feld, Pfeiltasten wählen, Enter öffnet, Escape schließt
function verbindeVorschlaege(el, suche) {
  const liste = el.querySelector('.vorschlaege'), alle = JSON.parse(el.dataset.objekte ?? '[]');
  if (!liste) return;
  let aktiv = -1;
  const zu = () => { liste.hidden = true; suche.setAttribute('aria-expanded', 'false'); aktiv = -1; };
  const markiere = (n) => {
    const li = [...liste.children]; aktiv = (n + li.length) % li.length;
    li.forEach((x, k) => x.setAttribute('aria-selected', k === aktiv));
    suche.setAttribute('aria-activedescendant', li[aktiv]?.id ?? '');
  };
  const fett = (name, q) => { const k = klein(name).indexOf(klein(q)); return k < 0 ? esc(name) : `${esc(name.slice(0, k))}<b>${esc(name.slice(k, k + q.length))}</b>${esc(name.slice(k + q.length))}`; };
  const fuelle = () => {
    const q = suche.value.trim(), t = treffer(alle, q).slice(0, 6);
    if (!q) return zu();
    liste.innerHTML = t.length ? t.map((o, k) => `<li id="vs-${k}" role="option"><a href="${o.h}">${icon(BEISPIELE.includes(o.id) ? o.id : GRUPPE_ICON[o.gruppe] ?? 'gruppe_alltag')}<span>${fett(o.name, q)}</span></a></li>`).join('')
      : '<li class="leer" role="option" aria-disabled="true">Nichts gefunden</li>';
    liste.hidden = false; suche.setAttribute('aria-expanded', 'true'); aktiv = -1;
  };
  suche.addEventListener('input', fuelle);
  suche.addEventListener('focus', () => suche.value.trim() && fuelle());
  suche.addEventListener('keydown', (e) => {
    if (liste.hidden) return;
    const n = liste.querySelectorAll('a').length;
    if (e.key === 'ArrowDown' && n) { e.preventDefault(); markiere(aktiv + 1); }
    else if (e.key === 'ArrowUp' && n) { e.preventDefault(); markiere(aktiv - 1); }
    else if (e.key === 'Escape') zu();
    else if (e.key === 'Enter' && n) { e.preventDefault(); liste.querySelectorAll('a')[Math.max(aktiv, 0)].click(); }
  });
  document.addEventListener('pointerdown', (e) => { if (!el.querySelector('.suche-zeile').contains(e.target)) zu(); });
}
