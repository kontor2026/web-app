// Verbindung zum Backend (backend/app/main.py). Läuft die Seite ohne Backend
// (statischer Server, Claude-Artefakt), bleibt api.online = false und die App nutzt die Demo-Daten.

async function req(path, { body, method = body ? 'POST' : 'GET', signal } = {}) {
  const r = await fetch(path, {
    method, signal,
    headers: body ? { 'Content-Type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.detail || `Fehler ${r.status}`);
  return data;
}

export const api = {
  online: false,
  info: null,

  async init() {
    try {
      // Großzügig: Während einer Generierung antwortet der Modellserver langsamer.
      const r = await fetch('/api/health', { signal: AbortSignal.timeout(8000) });
      if (r.ok) { this.info = await r.json(); this.online = true; }
    } catch { /* kein Backend: Demo-Modus */ }
    return this.online;
  },

  scan: (image, signal) => req('/api/scan', { body: { image }, signal }),
  steckbrief: (body, signal) => req('/api/steckbrief', { body, signal }),
  jobs: (scanId) => req(`/api/scans/${scanId}/jobs`),
  ideen: (id, neu, signal) => req(`/api/objects/${encodeURIComponent(id)}/ideen${neu ? '?neu=true' : ''}`, { method: 'POST', signal }),
  inventory: () => req('/api/inventory'),
  einlagern: (object_id, modell) => req('/api/inventory/einlagern', { body: { object_id, modell } }),
  start: (object_id, projekt) => req('/api/projekte/start', { body: { object_id, projekt } }),
};

// Bild (Pfad oder data:-URL) als data:-URL für den Upload.
export async function toDataUrl(src) {
  if (src.startsWith('data:')) return src;
  const blob = await (await fetch(src)).blob();
  return new Promise((ok, fail) => {
    const r = new FileReader();
    r.onload = () => ok(r.result);
    r.onerror = fail;
    r.readAsDataURL(blob);
  });
}
