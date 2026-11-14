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

// Umschalter in der Kopfzeile: 'souveraen' = lokales Modell, nichts verlässt die Station; 'cloud' = Claude.
const MODUS_KEY = 'station-modus';

export const api = {
  online: false,
  info: null,
  modus: localStorage.getItem(MODUS_KEY) ?? null,   // null: Standard des Backends

  setModus(m) { this.modus = m; localStorage.setItem(MODUS_KEY, m); },
  // Stand des gewählten Modus (Modell, bereit, Hinweis), sonst der Standard des Backends.
  get mode() { return this.info?.modi?.[this.modus] ?? this.info; },

  async init() {
    try {
      // Großzügig: Während einer Generierung antwortet der Modellserver langsamer.
      const r = await fetch('/api/health', { signal: AbortSignal.timeout(8000) });
      if (r.ok) {
        this.info = await r.json(); this.online = true;
        this.modus ??= this.info.standard ?? 'souveraen';
      }
    } catch { /* kein Backend: Demo-Modus */ }
    return this.online;
  },

  scan(image, signal) { return req('/api/scan', { body: { image, modus: this.modus }, signal }); },
  steckbrief(body, signal) { return req('/api/steckbrief', { body: { ...body, modus: this.modus }, signal }); },
  jobs: (scanId) => req(`/api/scans/${scanId}/jobs`),
  ideen(id, neu, signal) {
    const q = new URLSearchParams({ ...(neu && { neu: 'true' }), ...(this.modus && { modus: this.modus }) });
    return req(`/api/objects/${encodeURIComponent(id)}/ideen?${q}`, { method: 'POST', signal });
  },
  inventory: () => req('/api/inventory'),
  kategorien: () => req('/api/kategorien'),
  objekt: (id) => req(`/api/objects/${encodeURIComponent(id)}`),
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
