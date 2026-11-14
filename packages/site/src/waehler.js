// Gegenstand wählen: Suche, sechs Beispiele, alle 201 nach Gruppe. Gleich auf Start und Lebensweg.
import { esc, gramm, icon } from './shell.js';

export const BEISPIELE = ['smartphone', 'pet_bottle', 'laptop', 't_shirt', 'aluminium_can', 'hair_dryer'];

// Karte mit Piktogramm: eigenes, sonst das der Gruppe
const GRUPPE_ICON = { Elektro: 'gruppe_elektro', Verpackung: 'gruppe_verpackung', Textil: 'gruppe_textil', Alltag: 'gruppe_alltag' };
const karte = (o, href) => `<a class="beispiel" href="${href(o.id)}">${icon(BEISPIELE.includes(o.id) ? o.id : GRUPPE_ICON[o.gruppe] ?? 'gruppe_alltag', 'gross')}<b>${esc(o.name)}</b><span>${gramm(o.gramm)}</span></a>`;

export function waehlerHtml(objekte, href, { alle = true } = {}) {
  const gruppen = new Map();
  for (const o of [...objekte].sort((a, b) => a.name.localeCompare(b.name, 'de')))
    (gruppen.get(o.gruppe) ?? gruppen.set(o.gruppe, []).get(o.gruppe)).push(o);
  const von = new Map(objekte.map((o) => [o.id, o]));
  return `<div class="waehler" data-objekte='${alle ? '[]' : esc(JSON.stringify(objekte.map((o) => ({ id: o.id, name: o.name, gruppe: o.gruppe, gramm: o.gramm, h: href(o.id) })))).replace(/'/g, '&#39;')}'>
    <div class="suche-zeile"><input class="suche-feld" type="search" placeholder="Gegenstand suchen" autocomplete="off" aria-label="Gegenstand suchen">${alle ? '' : `<button class="wuerfel" type="button" aria-label="Andere Vorschläge" title="Andere Vorschläge">${icon('wuerfeln')}</button>`}</div>
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
  if (!alle) return verbindeSuche(el, suche);
  suche.addEventListener('input', () => {
    const q = suche.value.trim().toLowerCase();
    alle.open = !!q || alle.open;
    el.querySelectorAll('.kat-list a').forEach((a) => { a.hidden = !!q && !a.dataset.name.includes(q); });
    el.querySelectorAll('.gruppe').forEach((g) => { g.hidden = ![...g.querySelectorAll('a')].some((a) => !a.hidden); });
  });
  suche.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter') return;
    const a = el.querySelector('.kat-list a:not([hidden])');
    if (a && suche.value.trim()) location.href = a.href;
  });
}

// Ohne Liste (Start): Suche zeigt Treffer direkt als Karten unter dem Feld
function verbindeSuche(el, suche) {
  const beispiele = el.querySelector('.beispiele'), alle = JSON.parse(el.dataset.objekte ?? '[]');
  const zeige = (liste) => { beispiele.innerHTML = liste.map((o) => karte(o, () => o.h)).join('') || '<p class="leer">Nichts gefunden.</p>'; };
  suche.addEventListener('input', () => {
    const q = suche.value.trim().toLowerCase();
    if (q) zeige(alle.filter((o) => o.name.toLowerCase().includes(q)).slice(0, 2));
  });
  suche.addEventListener('keydown', (e) => { if (e.key === 'Enter') beispiele.querySelector('a')?.click(); });
  el.querySelector('.wuerfel')?.addEventListener('click', () => {
    suche.value = '';
    const zufall = [...alle].sort(() => Math.random() - 0.5).slice(0, 2);
    zeige(zufall);
  });
}
