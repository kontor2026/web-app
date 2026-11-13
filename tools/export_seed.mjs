// Exportiert die Frontend-Daten (JS-Module) als JSON-Seed für das Backend.
// Aufruf aus dem Projektordner:  node tools/export_seed.mjs
// Nach jeder Änderung an js/data/* erneut ausführen.
import { writeFileSync, mkdirSync } from 'node:fs';
import { CLASSES, MATERIALS, ELEMENTS } from '../js/data/catalog.js';
import { INVENTORY } from '../js/data/inventory.js';
import { OBJECTS } from '../js/data/objects/index.js';

const out = new URL('../backend/seed/', import.meta.url);
mkdirSync(new URL('objects/', out), { recursive: true });
const write = (name, data) => writeFileSync(new URL(name, out), JSON.stringify(data, null, 2) + '\n');

write('catalog.json', { classes: CLASSES, materials: MATERIALS, elements: ELEMENTS });
write('inventory.json', INVENTORY);
for (const o of OBJECTS) write(`objects/${o.id}.json`, o);
console.log(`Export: Katalog, ${INVENTORY.length} Lagerposten, ${OBJECTS.length} Objekte`);
