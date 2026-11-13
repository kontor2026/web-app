// Generischer Renderer für isometrische Explosionszeichnungen.
// Eingabe: ein Objekt nach docs/objekt-schema.md. Ausgabe: interaktives SVG.
// Jedes Bauteil ist ein extrudierter Grundriss (abgerundetes Rechteck oder
// Ellipse). Dadurch kann eine KI neue Objekte als reine Daten liefern.

import { animate, stagger, svg } from '../vendor/anime.esm.min.js';
import { CLASSES, MATERIALS } from './data/catalog.js';

const NS = 'http://www.w3.org/2000/svg';
const C30 = Math.cos(Math.PI / 6);
const S30 = 0.5;
const project = (x, y, z) => [(x - y) * C30, (x + y) * S30 - z];

function outline(s) {
  const pts = [];
  if (s.shape === 'cyl') {
    const rx = s.w / 2, ry = (s.d ?? s.w) / 2, cx = s.x + rx, cy = s.y + ry;
    for (let i = 0; i < 48; i++) {
      const a = (i / 48) * Math.PI * 2;
      pts.push([cx + Math.cos(a) * rx, cy + Math.sin(a) * ry]);
    }
    return pts;
  }
  const r = Math.min(s.r || 0, s.w / 2, s.d / 2);
  if (!r) return [[s.x, s.y], [s.x + s.w, s.y], [s.x + s.w, s.y + s.d], [s.x, s.y + s.d]];
  const corners = [
    [s.x + s.w - r, s.y + r, -90], [s.x + s.w - r, s.y + s.d - r, 0],
    [s.x + r, s.y + s.d - r, 90], [s.x + r, s.y + r, 180],
  ];
  for (const [cx, cy, a0] of corners) {
    for (let i = 0; i <= 6; i++) {
      const a = ((a0 + i * 15) * Math.PI) / 180;
      pts.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]);
    }
  }
  return pts;
}

function hull(points) {
  const p = points.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  const cross = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  const lower = [], upper = [];
  for (const q of p) {
    while (lower.length >= 2 && cross(lower.at(-2), lower.at(-1), q) <= 0) lower.pop();
    lower.push(q);
  }
  for (const q of p.reverse()) {
    while (upper.length >= 2 && cross(upper.at(-2), upper.at(-1), q) <= 0) upper.pop();
    upper.push(q);
  }
  return lower.slice(0, -1).concat(upper.slice(0, -1));
}

function shade(hex, f) {
  const n = parseInt(hex.slice(1), 16);
  const c = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => Math.round(v * (1 - f)));
  return `rgb(${c.join(',')})`;
}

const el = (tag, attrs = {}, parent) => {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
};

export function partColor(part) {
  if (part.color) return part.color;
  const m = MATERIALS[part.materials?.[0]?.[0]];
  return CLASSES[m?.cls]?.color ?? '#cccccc';
}

export class ExplodedView {
  constructor(container, obj, { onHover, onSelect } = {}) {
    this.container = container;
    this.obj = obj;
    this.onHover = onHover;
    this.onSelect = onSelect;
    this.exploded = false;
    this.labeled = obj.parts.filter((p) => p.label !== false);
    this.states = obj.parts.map((p) => ({ id: p.id, t: 0 }));
    this.selected = null;
    this.ro = new ResizeObserver(() => this.render(true));
  }

  mount() {
    this.svg = el('svg', { class: 'iso' });
    this.container.appendChild(this.svg);
    this.render(false);
    this.ro.observe(this.container);
  }

  destroy() {
    this.ro.disconnect();
    this.container.innerHTML = '';
  }

  // Geometrie in Bildschirmpixel umrechnen und SVG neu aufbauen.
  render(keepState) {
    const W = this.container.clientWidth, H = this.container.clientHeight;
    if (!W || !H) return;
    const parts = this.obj.parts;
    const geo = parts.map((p) => {
      const ex = p.explode ?? [0, 0, 0];
      const o = outline(p);
      const top = o.map(([x, y]) => project(x, y, p.z + p.h));
      const bot = o.map(([x, y]) => project(x, y, p.z));
      const marks = (p.marks ?? []).map((m) => ({
        ...m,
        pts: outline({ ...m, x: p.x + m.x, y: p.y + m.y }).map(([x, y]) => project(x, y, p.z + p.h + (m.lift ?? 0))),
      }));
      const off = project(ex[0], ex[1], ex[2]);
      return {
        p, top, side: hull(top.concat(bot)), marks, off,
        // Zeichenreihenfolge (Maleralgorithmus) getrennt für zusammengebaut und explodiert.
        keyA: p.z + p.h + (p.sortBias ?? 0),
        keyB: p.z + ex[2] + (ex[0] + ex[1]) * 0.5 + (p.sortBias ?? 0),
        depth: p.x + p.y + p.w / 2 + (p.d ?? p.w) / 2,
      };
    });

    // Bounding Box über zusammengebauten und explodierten Zustand.
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const g of geo) for (const t of [0, 1]) for (const [x, y] of g.side) {
      const X = x + g.off[0] * t, Y = y + g.off[1] * t;
      minX = Math.min(minX, X); maxX = Math.max(maxX, X); minY = Math.min(minY, Y); maxY = Math.max(maxY, Y);
    }
    // Auf schmalen Bildschirmen nur Positionsnummern ohne Beschriftung.
    this.compact = W < 640;
    const gutter = this.compact ? 34 : Math.min(175, W * 0.16);
    const s = Math.min((W - gutter * 2) / (maxX - minX), (H - 70) / (maxY - minY));
    const ox = (W - (maxX - minX) * s) / 2 - minX * s;
    const oy = (H - (maxY - minY) * s) / 2 - minY * s;
    const tx = ([x, y]) => [x * s + ox, y * s + oy];
    const str = (pts) => pts.map((q) => tx(q).map((n) => n.toFixed(1)).join(',')).join(' ');
    this.scale = s;

    this.svg.innerHTML = '';
    this.svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    const partsLayer = el('g', { class: 'parts' }, this.svg);
    this.calloutLayer = el('g', { class: 'callouts' }, this.svg);

    this.nodes = new Map();
    const sortBy = (k) => geo.map((g, i) => i).sort((a, b) => geo[a][k] - geo[b][k] || geo[a].depth - geo[b].depth).map((i) => geo[i].p.id);
    this.orders = { A: sortBy('keyA'), B: sortBy('keyB') };
    this.partsLayer = partsLayer;
    this.phase = null;
    for (const i of geo.keys()) {
      const { p, top, side, marks, off } = geo[i];
      const color = partColor(p);
      const g = el('g', { class: 'part', 'data-id': p.id }, partsLayer);
      el('polygon', { class: 'side', points: str(side), fill: shade(color, 0.22), 'fill-opacity': p.opacity ?? 1 }, g);
      el('polygon', { class: 'top', points: str(top), fill: color, 'fill-opacity': p.opacity ?? 1 }, g);
      for (const m of marks) {
        el('polygon', { class: 'mark', points: str(m.pts), fill: m.fill ?? 'none' }, g);
      }
      this.nodes.set(p.id, { g, off: [off[0] * s, off[1] * s], top: top.map(tx) });
    }

    this.buildCallouts(W, H, gutter);
    if (keepState) {
      for (const st of this.states) st.t = this.exploded ? 1 : 0;
      this.apply();
      this.calloutLayer.style.opacity = this.exploded ? 1 : 0;
    } else {
      this.apply();
    }
  }

  // Nummerierte Positionsnummern mit Hinweislinien, links und rechts gestapelt.
  buildCallouts(W, H, gutter) {
    const items = this.labeled.map((p, i) => {
      const n = this.nodes.get(p.id);
      const cx = n.top.reduce((a, q) => a + q[0], 0) / n.top.length + n.off[0];
      const cy = n.top.reduce((a, q) => a + q[1], 0) / n.top.length + n.off[1];
      return { p, num: String(i + 1).padStart(2, '0'), ax: cx, ay: cy };
    });
    const mid = W / 2;
    const sides = { L: items.filter((it) => it.ax < mid), R: items.filter((it) => it.ax >= mid) };
    const gap = 30;
    for (const [side, list] of Object.entries(sides)) {
      list.sort((a, b) => a.ay - b.ay);
      let y = 24;
      for (const it of list) { it.by = Math.max(it.ay, y); y = it.by + gap; }
      const overflow = y - gap - (H - 24);
      if (overflow > 0) list.forEach((it) => (it.by -= overflow));
      const bx = this.compact ? (side === 'L' ? 14 : W - 14) : (side === 'L' ? gutter - 30 : W - gutter + 30);
      for (const it of list) {
        const g = el('g', { class: 'callout', 'data-id': it.p.id }, this.calloutLayer);
        const elbow = side === 'L' ? bx + 22 : bx - 22;
        el('polyline', { class: 'leader', points: `${it.ax},${it.ay} ${elbow},${it.by} ${bx + (side === 'L' ? 11 : -11)},${it.by}` }, g);
        el('circle', { class: 'anchor', cx: it.ax, cy: it.ay, r: 2.5 }, g);
        el('circle', { class: 'balloon', cx: bx, cy: it.by, r: 11 }, g);
        const t = el('text', { class: 'num', x: bx, y: it.by + 0.5 }, g);
        t.textContent = it.num;
        if (!this.compact) {
        const lbl = el('text', { class: 'lbl', x: side === 'L' ? bx - 18 : bx + 18, y: it.by + 0.5, 'text-anchor': side === 'L' ? 'end' : 'start' }, g);
        lbl.textContent = it.p.short ?? it.p.name;
        }
        g.addEventListener('pointerenter', (e) => this.hover(it.p.id, e));
        g.addEventListener('pointerleave', () => this.hover(null));
        g.addEventListener('click', () => this.onSelect?.(it.p.id));
      }
    }
    this.numbers = new Map(items.map((it) => [it.p.id, it.num]));
  }

  apply() {
    // Ab halber Strecke auf die Reihenfolge des Zielzustands umschalten.
    const avg = this.states.reduce((a, s) => a + s.t, 0) / this.states.length;
    const phase = avg > 0.5 ? 'B' : 'A';
    if (phase !== this.phase) {
      this.phase = phase;
      for (const id of this.orders[phase]) this.partsLayer.appendChild(this.nodes.get(id).g);
    }
    for (const st of this.states) {
      const n = this.nodes.get(st.id);
      n.g.setAttribute('transform', `translate(${(n.off[0] * st.t).toFixed(2)},${(n.off[1] * st.t).toFixed(2)})`);
    }
  }
}
