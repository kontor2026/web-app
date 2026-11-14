#!/usr/bin/env node
'use strict';

// Statischer Server für die Präsentation. Liefert das ganze Repo aus, weil die Präsentation die Kategorie-Modelle
// (backend/seed/kategorien) und die Material-Funktionen der App (packages/site/src/foto.js, js/data/catalog.js) lädt.
//   node tools/serve.cjs [port]            nur dieser Rechner: http://localhost:5181/
//   node tools/serve.cjs [port] --tunnel   zusätzlich öffentlich per HTTPS (Cloudflare Quick Tunnel)
//   node tools/serve.cjs [port] --public   im Netz erreichbar (0.0.0.0)
// "/" leitet auf /praesentation/ weiter, die Stations-App liegt unter /index.html.
// Requests to /api/ are forwarded to the backend (API_URL, default http://127.0.0.1:8000). Presentation, app and
// API share one origin, so a single tunnel covers everything and the presentation can read keys inside the app iframe.
// Without a running backend /api answers 502 and the app falls back to its demo mode.
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { spawn } = require('node:child_process');

const root = path.join(__dirname, '..');
const args = process.argv.slice(2);
const port = Number(args.find((a) => /^\d+$/.test(a)) || process.env.PORT || 5181);
const host = args.includes('--public') ? '0.0.0.0' : (process.env.HOST || '127.0.0.1');
const api = new URL(process.env.API_URL || 'http://127.0.0.1:8000');
const types = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.txt': 'text/plain; charset=utf-8',
  '.woff2': 'font/woff2', '.glb': 'model/gltf-binary', '.ico': 'image/x-icon',
};
// Nichts ausliefern, was nicht in eine öffentliche Präsentation gehört.
// backend/data holds the local database and every scanned photo, it is only reachable through the API.
const blocked = /(^|[\\/])(\.git|\.env|secrets|node_modules|\.claude|\.venv|__pycache__)([\\/]|$)|^backend[\\/]data([\\/]|$)/;

function proxyApi(req, res) {
  const upstream = http.request({
    hostname: api.hostname, port: api.port || 80, path: req.url, method: req.method,
    headers: { ...req.headers, host: api.host },
    timeout: 900_000,                      // a new data sheet with a local model on CPU takes minutes
  }, (r) => {
    res.writeHead(r.statusCode, r.headers);
    r.pipe(res);
  });
  upstream.on('timeout', () => upstream.destroy(new Error('timeout')));
  upstream.on('error', () => {
    if (!res.headersSent) res.writeHead(502, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ detail: 'Backend nicht erreichbar' }));
  });
  req.pipe(upstream);
}

http.createServer((req, res) => {
  let pathname;
  try { pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname); } catch { res.writeHead(400); res.end(); return; }
  if (pathname.startsWith('/api/')) { proxyApi(req, res); return; }
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
}).listen(port, host, () => {
  console.log(`Präsentation: http://localhost:${port}/  (${host === '0.0.0.0' ? 'im Netz erreichbar' : 'nur lokal'})`);
  console.log(`App:          http://localhost:${port}/index.html  (Backend ${api.origin}, ohne Backend Demo-Modus)`);
  if (args.includes('--tunnel')) startTunnel();
});

// Cloudflare Quick Tunnel: no account needed, prints a random https://*.trycloudflare.com address.
function startTunnel() {
  const cf = spawn('cloudflared', ['tunnel', '--no-autoupdate', '--url', `http://127.0.0.1:${port}`], { stdio: ['ignore', 'pipe', 'pipe'] });
  let shown = false;
  const scan = (chunk) => {
    const m = !shown && /https:\/\/[a-z0-9-]+\.trycloudflare\.com/.exec(String(chunk));
    if (!m) return;
    shown = true;
    console.log(`\nÖffentlich (HTTPS): ${m[0]}/`);
    console.log(`  Präsentation ${m[0]}/praesentation/`);
    console.log(`  App          ${m[0]}/index.html`);
    console.log('Alles im Repo außer .git, .env, secrets/, backend/data/ ist darüber lesbar, solange der Server läuft.\n');
  };
  cf.stdout.on('data', scan);
  cf.stderr.on('data', scan);
  cf.on('error', () => {
    console.error('cloudflared nicht gefunden. Installieren: brew install cloudflared (macOS) oder winget install Cloudflare.cloudflared (Windows)');
    process.exit(1);
  });
  cf.on('exit', (code) => { console.error(`cloudflared beendet (Code ${code})`); process.exit(1); });
  const stop = () => { cf.kill(); process.exit(0); };
  process.on('SIGINT', stop);
  process.on('SIGTERM', stop);
}
