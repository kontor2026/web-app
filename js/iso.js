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

