// Stoffstrom: Bauteile → Materialien → Rohstoffe als Sankey in SVG, im Strich der Station (js/iso.js).
// Bandbreite = Gramm, alle Spalten im selben Maßstab. Sehr kleine Mengen bekommen eine Mindestbreite.
import { esc, gramm } from '../shell.js';

const NS = 'http://www.w3.org/2000/svg';
const MAX = { teil: 8, material: 8, rohstoff: 10 };

// Kleine Knoten einer Spalte zu „Weitere …“ zusammenfassen
function buendle(knoten, max, typ, name) {
  if (knoten.length <= max) return { knoten, karte: new Map(knoten.map((k) => [k.id, k.id])) };
  const behalten = knoten.slice(0, max - 1), rest = knoten.slice(max - 1);
  const weitere = { id: `weitere-${typ}`, typ, name: `${name} (${rest.length})`, g: rest.reduce((s, k) => s + k.g, 0), farbe: 'var(--rule)', weitere: true };
  return { knoten: [...behalten, weitere], karte: new Map([...behalten.map((k) => [k.id, k.id]), ...rest.map((k) => [k.id, weitere.id])]) };
}

export function zeichneStoffstrom(el, obj, { teilName, material, rohstoff, onHover, onClick }) {
  const { width: W, height: H } = el.getBoundingClientRect();
  el.innerHTML = '';
  if (W < 10 || H < 10) return { markiere() {} };
  const schmal = W < 620;
  const labelL = schmal ? 130 : 170, labelR = schmal ? 130 : 160, bar = 10, kopf = 22, luecke = 6;

  const T = buendle(obj.teile.map((t) => ({ id: t.cid, typ: 'teil', name: teilName(t), g: t.g, farbe: 'var(--ink-3)' })), MAX.teil, 'teil', 'Weitere Bauteile');
  const M = buendle(obj.materialien.map((m) => ({ id: m.mid, typ: 'material', name: material(m.mid).name, g: m.g, farbe: material(m.mid).farbe })), MAX.material, 'material', 'Weitere Materialien');
  const R = buendle(obj.rohstoffe.map((r) => ({ id: r.key, typ: 'rohstoff', name: rohstoff(r.key).name, g: r.g, farbe: rohstoff(r.key).farbe, kritisch: rohstoff(r.key).kritisch })), MAX.rohstoff, 'rohstoff', 'Weitere Rohstoffe');
  // Schmale Bildschirme: nur Materialien → Rohstoffe, damit die Beschriftungen lesbar bleiben
  const spalten = schmal ? [M.knoten, R.knoten] : [T.knoten, M.knoten, R.knoten];

  // Verbindungen, auf gebündelte Knoten umgeschrieben
  const links = new Map();
  const add = (a, b, g) => { const k = `${a}→${b}`; links.set(k, { a, b, g: (links.get(k)?.g ?? 0) + g }); };
  for (const [cid, mid, g] of obj.bm) if (T.karte.has(cid) && M.karte.has(mid)) add(T.karte.get(cid), M.karte.get(mid), g);
  for (const [mid, key, g] of obj.mr) if (M.karte.has(mid) && R.karte.has(key)) add(M.karte.get(mid), R.karte.get(key), g);

  // Maßstab: gleiche Gramm = gleiche Breite in allen Spalten
  const hoehe = H - kopf - 4;
  const summe = (s) => s.reduce((x, k) => x + k.g, 0);
  const skala = Math.min(...spalten.map((s) => (hoehe - luecke * (s.length - 1) - 2 * s.length) / Math.max(summe(s), 1e-9)));
  const xs = schmal ? [labelL, W - labelR - bar] : [labelL, (labelL + W - labelR - bar) / 2, W - labelR - bar];
  const titel = schmal ? ['Materialien', 'Rohstoffe'] : ['Bauteile', 'Materialien', 'Rohstoffe'];
  const letzte = spalten.length - 1;
  const pos = new Map();
  spalten.forEach((s, i) => {
    let y = kopf;
    for (const k of s) { const h = Math.max(2, k.g * skala); pos.set(k.id, { ...k, x: xs[i], y, h, aus: 0, ein: 0 }); y += h + luecke; }
  });

  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('class', 'strom-svg');
  svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  svg.setAttribute('role', 'img');
  svg.setAttribute('aria-label', `Stoffstrom von ${obj.name}: Bauteile, Materialien und Rohstoffe nach Gewicht`);
  let html = titel.map((t, i) =>
    `<text class="spalte" x="${i === 0 ? xs[0] + bar : i === letzte ? xs[i] : xs[i] + bar / 2}" y="11" text-anchor="${i === 0 ? 'end' : i === letzte ? 'start' : 'middle'}">${t}</text>`).join('');

  for (const [k, l] of links) if (!pos.has(l.a) || !pos.has(l.b)) links.delete(k);   // ausgeblendete Spalte
  // Bänder: Reihenfolge nach Lage der Gegenseite, damit sich wenig kreuzt
  const sortiert = [...links.values()].sort((p, q) => pos.get(p.b).y - pos.get(q.b).y || pos.get(p.a).y - pos.get(q.a).y);
  const proQuelle = new Map();
  for (const l of sortiert) (proQuelle.get(l.a) ?? proQuelle.set(l.a, []).get(l.a)).push(l);
  const bandH = (l) => Math.max(1, l.g * skala);
  for (const l of [...links.values()].sort((p, q) => pos.get(p.a).y - pos.get(q.a).y)) {
    const a = pos.get(l.a), b = pos.get(l.b), h = Math.min(bandH(l), a.h, b.h);
    const y0 = a.y + a.aus, y1 = b.y + b.ein;
    a.aus += h * (a.h > 2 ? 1 : 0); b.ein += h * (b.h > 2 ? 1 : 0);
    const x0 = a.x + bar, x1 = b.x, m = (x0 + x1) / 2;
    html += `<path class="band" data-a="${l.a}" data-b="${l.b}" style="fill:${a.farbe}" d="M${x0},${y0} C${m},${y0} ${m},${y1} ${x1},${y1} L${x1},${y1 + h} C${m},${y1 + h} ${m},${y0 + h} ${x0},${y0 + h} Z"><title>${esc(a.name)} → ${esc(b.name)}: ${gramm(l.g)}</title></path>`;
  }
  // Beschriftungen je Spalte mindestens 14 px auseinander, notfalls nach oben verschoben
  const labelY = new Map();
  for (const s of spalten) {
    const ys = s.map((k) => pos.get(k.id).y + pos.get(k.id).h / 2);
    for (let j = 1; j < ys.length; j++) ys[j] = Math.max(ys[j], ys[j - 1] + 16);
    const ueber = ys.length ? ys[ys.length - 1] - (H - 6) : 0;
    if (ueber > 0) for (let j = ys.length - 1; j >= 0; j--) ys[j] = Math.min(ys[j] - ueber, j < ys.length - 1 ? ys[j + 1] - 16 : Infinity);
    s.forEach((k, j) => labelY.set(k.id, ys[j]));
  }
  // Knoten mit Beschriftung
  spalten.forEach((s, i) => s.forEach((k) => {
    const p = pos.get(k.id), links_ = i === 0, mitte = p.y + p.h / 2, ty = labelY.get(k.id);
    const tx = links_ ? p.x - 8 : p.x + bar + 8;
    html += `<g class="knoten ${k.typ} ${k.weitere ? 'weitere' : ''}" data-id="${k.id}" data-typ="${k.typ}" tabindex="${k.typ === 'rohstoff' && !k.weitere ? 0 : -1}">
      <rect x="${p.x}" y="${p.y}" width="${bar}" height="${p.h}" style="fill:${k.farbe}"/>
      <rect class="treffer" x="${links_ ? 0 : p.x}" y="${p.y - 3}" width="${links_ ? p.x + bar : (i === letzte ? labelR + bar : 120)}" height="${p.h + 6}"/>
      ${Math.abs(ty - mitte) > 1 ? `<polyline class="fuehrung" points="${links_ ? p.x : p.x + bar},${mitte} ${links_ ? tx + 4 : tx - 4},${ty}"/>` : ''}
      <text x="${tx}" y="${ty}" text-anchor="${links_ ? 'end' : 'start'}">${esc(k.name)}<tspan class="g"> ${gramm(k.g)}</tspan>${k.kritisch ? '<tspan class="krit"> ▲</tspan>' : ''}</text></g>`;
  }));
  svg.innerHTML = html;
  el.append(svg);

  // Hervorheben: Knoten und alles, was durch ihn fließt
  const nachbarn = (id) => {
    const ids = new Set([id]), wege = new Set();
    const vor = (x) => [...links.values()].filter((l) => l.b === x), nach = (x) => [...links.values()].filter((l) => l.a === x);
    const geh = (x, f, n) => f(x).forEach((l) => { wege.add(l); const y = n(l); if (!ids.has(y)) { ids.add(y); geh(y, f, n); } });
    geh(id, vor, (l) => l.a); geh(id, nach, (l) => l.b);
    return { ids, wege };
  };
  function markiere(id) {
    svg.classList.toggle('has-hot', !!id);
    const n = id && pos.has(id) ? nachbarn(id) : null;
    svg.querySelectorAll('.knoten').forEach((g) => g.classList.toggle('hot', !!n?.ids.has(g.dataset.id)));
    svg.querySelectorAll('.band').forEach((p) => p.classList.toggle('hot', !!n && [...n.wege].some((l) => l.a === p.dataset.a && l.b === p.dataset.b)));
  }
  svg.querySelectorAll('.knoten').forEach((g) => {
    const id = g.dataset.id, typ = g.dataset.typ, echt = !id.startsWith('weitere');
    g.addEventListener('pointerenter', () => { markiere(id); onHover?.(echt ? id : null, typ); });
    g.addEventListener('pointerleave', () => { markiere(null); onHover?.(null, typ); });
    g.addEventListener('click', () => echt && onClick?.(id, typ));
    g.addEventListener('keydown', (e) => { if ((e.key === 'Enter' || e.key === ' ') && echt) { e.preventDefault(); onClick?.(id, typ); } });
  });
  return { markiere, groessterRohstoff: R.knoten.find((k) => !k.weitere)?.id };
}
