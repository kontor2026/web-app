import { defineConfig } from 'vite';
import { resolve } from 'node:path';

// Mehrseitige statische Seite. Relative Pfade: läuft unter jedem Unterpfad (GitHub Pages /web-app/).
// Die Seite liest css/app.css, js/data/catalog.js und backend/seed/ direkt aus dem Repo, nichts wird kopiert.
const seite = (p) => resolve(import.meta.dirname, p);
export default defineConfig({
  base: './',
  server: { fs: { allow: [resolve(import.meta.dirname, '../..')] } },
  build: {
    chunkSizeWarningLimit: 2500,
    rollupOptions: {
      input: { start: seite('index.html'), atlas: seite('atlas/index.html'), modelle: seite('modelle/index.html'), kompass: seite('kompass/index.html'), werkbank: seite('werkbank/index.html'), quelle: seite('quelle/index.html'), qr: seite('qr/index.html') },
    },
  },
});
