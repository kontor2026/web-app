// Werkbank: Was habe ich? Gegenstände mit Anzahl, im Browser gespeichert (localStorage).
// Daraus ergeben sich die Bauteile, die ich habe, und welche Rezepte ich ganz oder teilweise bauen kann.
const SCHLUESSEL = 'werkbank';

export function bestand() {
  try { return JSON.parse(localStorage.getItem(SCHLUESSEL)) ?? {}; } catch { return {}; }
}
function speichere(b) {
  localStorage.setItem(SCHLUESSEL, JSON.stringify(b));
  dispatchEvent(new CustomEvent('werkbank'));
}
export function setze(id, menge) {
  const b = bestand();
  if (menge > 0) b[id] = menge; else delete b[id];
  speichere(b);
}
export const plus = (id, n = 1) => setze(id, (bestand()[id] ?? 0) + n);
// Anzeigename eines Postens: das Bauteil, das ich habe, sonst das erste; weitere Alternativen als „+n“
export function postenName(p, teile, name) {
  const da = p.ids.find((id) => teile[id] > 0) ?? p.component_id;
  return { text: name(da), mehr: p.ids.length - 1, alle: p.ids.map(name).join(', ') };
}
export const geschaetzt = (p) => /geschätzt|Schätzung/i.test(p.hinweis ?? '');
export const anzahl = () => Object.values(bestand()).reduce((s, n) => s + n, 0);

// Bauteile aus den Gegenständen: jedes Bauteil eines Gegenstands zählt einmal je Stück
export function bauteile(objektVon) {
  const z = {};
  for (const [id, n] of Object.entries(bestand())) for (const t of objektVon.get(id)?.teile ?? []) z[t.cid] = (z[t.cid] ?? 0) + n;
  return z;
}

// Stand eines Rezepts: je Eintrag in „braucht“ vorhanden oder fehlend (Alternativen über „oder“)
export function stand(rezept, teile) {
  const posten = (rezept.braucht ?? []).map((b) => {
    const ids = [b.component_id, ...(b.oder ?? [])];
    const da = ids.reduce((s, id) => s + (teile[id] ?? 0), 0);
    const soll = Math.max(1, b.menge ?? 1);
    return { ...b, ids, da, soll, ok: da >= soll };
  });
  const ok = posten.filter((p) => p.ok).length;
  return { posten, ok, alle: posten.length, baubar: posten.length > 0 && ok === posten.length, teilweise: ok > 0 || posten.some((p) => p.da > 0) };
}
