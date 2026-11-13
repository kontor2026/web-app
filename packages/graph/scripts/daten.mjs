// Erzeugt src/daten.json für den Graphen aus den Daten im Projekt (läuft vor dev und build).
//   data/classifier.json              Gegenstände, Bauteile, Materialien
//   tools/kategorien/kategorien.csv   deutscher Name, Entsorgungsweg, Gewicht
//   backend/seed/kategorien/<id>.json Bauteil-Massen aus den 3D-Modellen
//   backend/seed/catalog.json         deutsche Materialnamen und Farben der Materialklassen
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const root = new URL('../../../', import.meta.url);
const lies = (p) => readFileSync(new URL(p, root), 'utf8');
const json = (p) => JSON.parse(lies(p));

const cls = json('data/classifier.json');
const katalog = json('backend/seed/catalog.json');
const csv = lies('tools/kategorien/kategorien.csv').trim().split('\n').map((z) => z.split(';'));
const kopf = csv.shift();
const zeilen = Object.fromEntries(csv.map((z) => [z[0], Object.fromEntries(kopf.map((k, i) => [k, z[i]]))]));

const GRUPPE = { EK: 'elektro', EB: 'elektro', EG: 'elektro', BAT: 'elektro', LM: 'elektro',
  VK: 'verpackung', VG: 'verpackung', VP: 'verpackung', PF: 'verpackung', TX: 'textil' };

// Bauteil-Massen je Gegenstand und Katalog-Material je classifier-Material aus den erzeugten Modellen
const masse = {}, katalogVon = {};
for (const oid of Object.keys(cls.objects)) {
  const pfad = `backend/seed/kategorien/${oid}.json`;
  if (!existsSync(new URL(pfad, root))) continue;
  const obj = json(pfad);
  masse[oid] = { handgebaut: !obj.platzhalter, teile: {} };
  for (const p of obj.parts) {
    if (!p.component_id) continue;
    masse[oid].teile[p.component_id] = (masse[oid].teile[p.component_id] ?? 0) + p.mass;
    const mid = p.material_id ?? cls.components[p.component_id]?.material_id;
    const kid = p.materials?.[0]?.[0];
    if (mid && kid) (katalogVon[mid] ??= {})[kid] = (katalogVon[mid][kid] ?? 0) + 1;
  }
}
const haeufigste = (o) => Object.entries(o ?? {}).sort((a, b) => b[1] - a[1])[0]?.[0];

const nodes = [], links = [];
for (const [mid, m] of Object.entries(cls.materials)) {
  const kat = katalog.materials[haeufigste(katalogVon[mid])];
  const klasse = katalog.classes[kat?.cls] ?? { label: 'Sonstiges', color: '#B8B4A8' };
  nodes.push({ id: `m:${mid}`, typ: 'material', key: mid, name: kat?.name ?? m.name ?? mid, en: m.name ?? mid,
    klasse: klasse.label, farbe: klasse.color, text: kat?.text ?? '', recycling: kat?.recycling ?? '' });
}
for (const [cid, c] of Object.entries(cls.components)) {
  nodes.push({ id: `c:${cid}`, typ: 'bauteil', key: cid, name: c.name, hint: c.hint, material: c.material_id });
  links.push({ source: `c:${cid}`, target: `m:${c.material_id}`, typ: 'material' });
}
for (const [oid, o] of Object.entries(cls.objects)) {
  const z = zeilen[oid] ?? {};
  nodes.push({ id: `o:${oid}`, typ: 'objekt', key: oid, name: z.name ?? o.name, en: o.name,
    gruppe: GRUPPE[z.entsorgung] ?? 'alltag', gramm: Number(z.gramm) || 0, handgebaut: masse[oid]?.handgebaut ?? false });
  for (const cid of o.components)
    links.push({ source: `o:${oid}`, target: `c:${cid}`, typ: 'bauteil', gramm: Math.round((masse[oid]?.teile[cid] ?? 0) * 10) / 10 });
}

const ziel = fileURLToPath(new URL('../src/daten.json', import.meta.url));
writeFileSync(ziel, JSON.stringify({ nodes, links }));
console.log(`daten.json: ${nodes.length} Knoten, ${links.length} Kanten`);
