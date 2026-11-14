#!/usr/bin/env node
'use strict';

// Statischer Server für die Präsentation. Liefert das ganze Repo aus, weil die Präsentation die Kategorie-Modelle
// (backend/seed/kategorien) und die Material-Funktionen der App (packages/site/src/foto.js, js/data/catalog.js) lädt.
//   node tools/serve.cjs [port]            nur dieser Rechner: http://localhost:5181/
//   node tools/serve.cjs [port] --public   im Netz erreichbar (0.0.0.0), z. B. hinter einem Tunnel
// "/" leitet auf /praesentation/ weiter.
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const root = path.join(__dirname, '..');
const args = process.argv.slice(2);
const port = Number(args.find((a) => /^\d+$/.test(a)) || process.env.PORT || 5181);
const host = args.includes('--public') ? '0.0.0.0' : (process.env.HOST || '127.0.0.1');
const types = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.txt': 'text/plain; charset=utf-8',
  '.woff2': 'font/woff2', '.glb': 'model/gltf-binary', '.ico': 'image/x-icon',
};
// Nichts ausliefern, was nicht in eine öffentliche Präsentation gehört
const blocked = /(^|[\\/])(\.git|\.env|secrets|node_modules|\.claude)([\\/]|$)/;

http.createServer((req, res) => {
  let pathname;
  try { pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname); } catch { res.writeHead(400); res.end(); return; }
  if (pathname === '/') { res.writeHead(302, { Location: '/praesentation/' }); res.end(); return; }
  const file = path.join(root, pathname.endsWith('/') ? `${pathname}index.html` : pathname);
  if (!file.startsWith(root + path.sep) || blocked.test(path.relative(root, file))) { res.writeHead(403); res.end(); return; }
  fs.stat(file, (err, st) => {
    if (!err && st.isDirectory()) { res.writeHead(302, { Location: `${pathname}/` }); res.end(); return; }
    fs.readFile(file, (error, data) => {
      if (error) { res.writeHead(404); res.end('Not found'); return; }
      res.writeHead(200, { 'Content-Type': types[path.extname(file).toLowerCase()] || 'application/octet-stream', 'Cache-Control': 'no-cache' });
      res.end(data);
    });
  });
}).listen(port, host, () => console.log(`Präsentation: http://localhost:${port}/  (${host === '0.0.0.0' ? 'im Netz erreichbar' : 'nur lokal'})`));
