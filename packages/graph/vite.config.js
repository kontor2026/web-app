import { defineConfig } from 'vite';

// Relative Pfade: läuft unter jedem Unterpfad, z. B. GitHub Pages /web-app/graph/.
export default defineConfig({ base: './', build: { chunkSizeWarningLimit: 2000 } });
