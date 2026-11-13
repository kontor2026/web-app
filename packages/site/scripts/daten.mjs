// Erzeugt src/daten/atlas.json (läuft vor dev und build, nur Node, keine Abhängigkeiten).
//   backend/seed/kategorien/<id>.json  Bauteile mit Masse und material_id, Rohstoffe (metalle_mg, materialien_g)
//   tools/kategorien/kategorien.csv    deutscher Name, Entsorgungsweg, Gewicht
//   data/classifier.json               Bauteile und Materialien
//   data/rohstoffe/herkunft.json       Länderanteile je Rohstoff (Abbau, Verarbeitung) mit Quelle
//   data/rohstoffe/laender.json        deutsche Ländernamen und ISO-Nummern
//   data/rohstoffe/quellen.json        Zitate
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';

const root = new URL('../../../', import.meta.url);
const da = (p) => existsSync(new URL(p, root));
const json = (p, leer) => (da(p) ? JSON.parse(readFileSync(new URL(p, root), 'utf8')) : leer);

const cls = json('data/classifier.json');
const herkunft = json('data/rohstoffe/herkunft.json', {});
const laender = json('data/rohstoffe/laender.json', {});
const quellen = json('data/rohstoffe/quellen.json', {});
const zeilen = readFileSync(new URL('tools/kategorien/kategorien.csv', root), 'utf8').trim().split('\n').map((z) => z.split(';'));
const kopf = zeilen.shift();
const csv = Object.fromEntries(zeilen.map((z) => [z[0], Object.fromEntries(kopf.map((k, i) => [k, z[i]]))]));

// Rohstoffe: Anzeige, Farbklasse (wie CLASSES in js/data/catalog.js) und Artikel für die Frage „Woher kommt …?“
const R = (name, sym, art, artikel = 'das') => ({ name, sym, art, artikel });
const ROHSTOFF = {
  Fe: R('Eisen', 'Fe', 'metall'), Cu: R('Kupfer', 'Cu', 'metall'), Al: R('Aluminium', 'Al', 'metall'),
  Ni: R('Nickel', 'Ni', 'metall'), Cr: R('Chrom', 'Cr', 'metall'), Zn: R('Zink', 'Zn', 'metall'),
  Mn: R('Mangan', 'Mn', 'metall'), Sn: R('Zinn', 'Sn', 'metall'),
  Au: R('Gold', 'Au', 'elektronik'), Ag: R('Silber', 'Ag', 'elektronik'), Pd: R('Palladium', 'Pd', 'elektronik'),
  Pt: R('Platin', 'Pt', 'elektronik'), In: R('Indium', 'In', 'elektronik'), Ga: R('Gallium', 'Ga', 'elektronik'),
  Ta: R('Tantal', 'Ta', 'elektronik'), Y: R('Yttrium', 'Y', 'elektronik'),
  Co: R('Kobalt', 'Co', 'akku'), Li: R('Lithium', 'Li', 'akku'), graphit: R('Graphit', 'C', 'akku'),
  Nd: R('Neodym', 'Nd', 'magnet'), Pr: R('Praseodym', 'Pr', 'magnet'), Dy: R('Dysprosium', 'Dy', 'magnet'),
  erdoel: R('Erdöl', 'Öl', 'kunststoff'), naturkautschuk: R('Naturkautschuk', 'Kt', 'kunststoff', 'der'),
  holz: R('Holz', 'Hz', 'papier'), baumwolle: R('Baumwolle', 'Bw', 'papier', 'die'), wolle: R('Wolle', 'Wo', 'papier', 'die'),
  leder: R('Leder', 'Le', 'papier'), kork: R('Kork', 'Ko', 'papier', 'der'), quarzsand: R('Quarzsand', 'Sd', 'glas', 'der'),
};
const Z = { Fe: 26, Cu: 29, Al: 13, Ni: 28, Cr: 24, Zn: 30, Mn: 25, Sn: 50, Au: 79, Ag: 47, Pd: 46, Pt: 78, In: 49, Ga: 31,
  Ta: 73, Y: 39, Co: 27, Li: 3, graphit: 6, Nd: 60, Pr: 59, Dy: 66 };

// Nichtmetalle: Material → Primärrohstoff (ganze Materialmasse)
const AUS = {
  pp: 'erdoel', pe: 'erdoel', hdpe: 'erdoel', ldpe: 'erdoel', pet: 'erdoel', pvc: 'erdoel', ps: 'erdoel', eps: 'erdoel',
  abs: 'erdoel', pc: 'erdoel', nylon: 'erdoel', polyester: 'erdoel', pu_foam: 'erdoel', eva_foam: 'erdoel',
  polyurethane: 'erdoel', multilayer_plastic: 'erdoel', phenolic_resin: 'erdoel', paraffin_wax: 'erdoel',
  rubber: 'naturkautschuk', paper: 'holz', cardboard: 'holz', wood: 'holz', paper_plastic_composite: 'holz',
  composite_carton: 'holz', cotton: 'baumwolle', wool: 'wolle', leather: 'leder', cork: 'kork',
  glass: 'quarzsand', special_glass: 'quarzsand',
};
// Metalle: aus welchen Materialien sie kommen (wie METALLANTEIL in tools/kategorien/rohstoffe.py)
const METALL_IN = {
  Cu: { copper: 1, pcb: 0.2, li_ion: 0.1, mixed_electronics: 0.3 }, Al: { aluminium: 1, li_ion: 0.15 },
  Fe: { steel: 0.98, mixed_electronics: 0.15 }, Ni: { nickel_chrome: 0.8 },
};
const SPUR_IN = { Au: ['pcb', 'mixed_electronics'], Ag: ['pcb', 'mixed_electronics'], Pd: ['pcb', 'mixed_electronics'],
  Pt: ['pcb', 'mixed_electronics'], Ta: ['pcb', 'mixed_electronics'], Ga: ['pcb', 'mixed_electronics'],
  In: ['special_glass', 'pcb'], Y: ['special_glass', 'mixed_electronics'], Co: ['li_ion', 'mixed_electronics'],
  Nd: ['mixed_electronics'], Pr: ['mixed_electronics'], Dy: ['mixed_electronics'] };

const GRUPPE = { EK: 'Elektro', EB: 'Elektro', EG: 'Elektro', BAT: 'Elektro', LM: 'Elektro',
  VK: 'Verpackung', VG: 'Verpackung', VP: 'Verpackung', PF: 'Verpackung', TX: 'Textil' };

const objekte = [], katalogVon = {};   // classifier-Material → häufigste Katalog-ID (deutscher Name, Farbklasse)
for (const [oid, o] of Object.entries(cls.objects)) {
  const pfad = `backend/seed/kategorien/${oid}.json`;
  if (!da(pfad)) continue;
  const seed = json(pfad);
  // Bauteile: Masse je component_id, Name des schwersten Teils (handgebaut: deutsch)
  const teile = new Map();
  for (const p of seed.parts) {
    const cid = p.component_id ?? p.id;
    const mid = p.material_id ?? cls.components[cid]?.material_id ?? 'mixed_electronics';
    const kid = p.materials?.[0]?.[0];
    if (kid) (katalogVon[mid] ??= {})[kid] = (katalogVon[mid][kid] ?? 0) + 1;
    const t = teile.get(cid) ?? { cid, name: cls.components[cid]?.name ?? p.name, mid, g: 0, max: 0 };
    t.g += p.mass;
    if (p.mass > t.max && !seed.platzhalter) { t.max = p.mass; t.name = p.name; }
    teile.set(cid, t);
  }
  const bm = new Map();                                  // Bauteil → Material
  for (const t of teile.values()) bm.set(`${t.cid}|${t.mid}`, (bm.get(`${t.cid}|${t.mid}`) ?? 0) + t.g);
  const matG = seed.rohstoffe?.materialien_g ?? {};
  const mr = new Map(), roh = new Map();                // Material → Rohstoff, Rohstoff gesamt
  const fluss = (mid, key, g) => {
    if (!(g > 0)) return;
    mr.set(`${mid}|${key}`, (mr.get(`${mid}|${key}`) ?? 0) + g);
    roh.set(key, (roh.get(key) ?? 0) + g);
  };
  for (const [mid, g] of Object.entries(matG)) if (AUS[mid]) fluss(mid, AUS[mid], g);
  for (const [el, mg] of Object.entries(seed.rohstoffe?.metalle_mg ?? {})) {
    const g = mg / 1000;
    if (METALL_IN[el]) {
      const quellen = Object.entries(METALL_IN[el]).map(([mid, a]) => [mid, (matG[mid] ?? 0) * a]).filter(([, x]) => x > 0);
      const summe = quellen.reduce((s, [, x]) => s + x, 0);
      if (summe) quellen.forEach(([mid, x]) => fluss(mid, el, (g * x) / summe));
      else fluss(Object.keys(matG)[0], el, g);
    } else {
      const mid = (SPUR_IN[el] ?? []).find((m) => matG[m]) ?? Object.keys(matG)[0];
      fluss(mid, el, g);
    }
  }
  const z = csv[oid] ?? {};
  objekte.push({
    id: oid, name: z.name ?? o.name, gruppe: GRUPPE[z.entsorgung] ?? 'Alltag', gramm: Number(z.gramm) || 0,
    handgebaut: !seed.platzhalter, klasse: seed.klasse,
    teile: [...teile.values()].map(({ cid, name, mid, g }) => ({ cid, name, mid, g: +g.toFixed(3) })).sort((a, b) => b.g - a.g),
    materialien: Object.entries(matG).map(([mid, g]) => ({ mid, g })).sort((a, b) => b.g - a.g),
    rohstoffe: [...roh].map(([key, g]) => ({ key, g: +g.toFixed(4) })).sort((a, b) => b.g - a.g),
    bm: [...bm].map(([k, g]) => [...k.split('|'), +g.toFixed(3)]),
    mr: [...mr].map(([k, g]) => [...k.split('|'), +g.toFixed(4)]),
  });
}

const rohstoffe = {};
for (const [key, r] of Object.entries(ROHSTOFF)) {
  const h = herkunft[key] ?? {};
  rohstoffe[key] = { ...r, z: Z[key] ?? null, kritisch: h.kritisch ?? null, abbau: h.abbau ?? null, verarbeitung: h.verarbeitung ?? null };
}
const haeufigste = (o) => Object.entries(o ?? {}).sort((a, b) => b[1] - a[1])[0]?.[0] ?? null;
const materialien = Object.fromEntries(Object.keys(cls.materials).map((mid) => [mid, { en: cls.materials[mid].name ?? mid, kat: haeufigste(katalogVon[mid]) }]));

mkdirSync(new URL('../src/daten/', import.meta.url), { recursive: true });
writeFileSync(new URL('../src/daten/atlas.json', import.meta.url), JSON.stringify({ objekte, rohstoffe, materialien, laender, quellen }));
const mitHerkunft = Object.values(rohstoffe).filter((r) => r.abbau || r.verarbeitung).length;
console.log(`atlas.json: ${objekte.length} Gegenstände, ${Object.keys(rohstoffe).length} Rohstoffe (${mitHerkunft} mit Herkunftsdaten)`);
