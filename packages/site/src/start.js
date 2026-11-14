// Start: Der Kreislauf als Bild, darunter sofort die Wahl des Gegenstands. Wenig Text, eine Hauptaktion.
import { shell, SCHRITTE, icon, ruhig } from './shell.js';
import { waehlerHtml, verbindeWaehler } from './waehler.js';
import atlas from './daten/atlas.json';

const app = shell('start', './');

// Kreis mit den sieben Stationen, Uhrzeigersinn ab oben
const R = 150;
const punkte = SCHRITTE.map((s, i) => {
  const a = (i / SCHRITTE.length) * Math.PI * 2 - Math.PI / 2;
  return { ...s, x: Math.cos(a) * R, y: Math.sin(a) * R, cx: Math.cos(a), cy: Math.sin(a) };
});

app.innerHTML = `
<section class="view start">
  <div class="start-inhalt">
    <div class="wechsel" id="wechsel" aria-roledescription="Bilderwechsel">
    <figure class="kreis wechsel-bild on" data-n="0" aria-label="Der Lebensweg eines Gegenstands in sieben Stationen">
      <svg viewBox="-290 -215 580 430" class="kreis-svg">
        <circle class="kreis-ring" r="${R}" pathLength="1" transform="rotate(-90)"/>
        ${punkte.map((p, i) => `<g transform="translate(${p.x.toFixed(1)} ${p.y.toFixed(1)})"><g class="kreis-punkt" style="--i:${i}">
          <circle r="30" class="${p.id === 'gegenstand' ? 'mitte' : ''}"/>
          <g transform="translate(-13 -13) scale(1.0833)">${icon(p.id).replace('<svg class="icon "', '<svg width="24" height="24" class="icon"')}</g>
          <text x="${(p.cx * 46).toFixed(1)}" y="${(p.cy * 46 + 4.5).toFixed(1)}" text-anchor="${p.cx > 0.3 ? 'start' : p.cx < -0.3 ? 'end' : 'middle'}">${p.name}</text></g></g>`).join('')}
      </svg>
    </figure>
    <figure class="wechsel-bild" data-n="1" aria-label="Woher Kobalt im Smartphone kommt"><div class="wechsel-flaeche" id="start-globus"></div></figure>
    <figure class="wechsel-bild" data-n="2" aria-label="Smartphone in Einzelteilen"><div class="wechsel-flaeche" id="start-modell"></div></figure>
    </div>
    <div class="start-text">
      <h1>Wo kommt es her?<br>Wo geht es hin?</h1>
      <p class="lead">Wähle einen Gegenstand und folge seinem Weg.</p>
      ${waehlerHtml(atlas.objekte, (id) => `atlas/#kat=${id}`, { alle: false })}
    </div>
  </div>
</section>`;
if (ruhig) document.querySelector('.kreis').classList.add('ruhig');

// ---------- Kreis in Bewegung: die hervorgehobene Station wandert weiter ----------
let station = SCHRITTE.findIndex((x) => x.id === 'gegenstand');
if (!ruhig) setInterval(() => {
  if (document.hidden) return;
  const kreise = document.querySelectorAll('.kreis-punkt > circle');
  kreise[station]?.classList.remove('mitte');
  station = (station + 1) % kreise.length;
  kreise[station]?.classList.add('mitte');
}, 2600);

// ---------- Bilderwechsel: Kreislauf → Weltkarte → 3D-Modell ----------
// Globus und 3D laden erst, wenn sie gezeigt werden. Stopp bei Berührung, ohne Automatik bei reduzierter Bewegung.
let aktiv = 0, globus = null, modell = null, pause = false, atmen = null;
const fertig = {};
function bereite(n) { return (fertig[n] ??= lade(n)); }
async function lade(n) {
  if (n === 1 && !globus) {
    const { erzeugeGlobus } = await import('./atlas/globus.js');
    globus = erzeugeGlobus(document.getElementById('start-globus'), atlas.laender);
    globus.zeige(atlas.rohstoffe.Co?.abbau?.anteile ?? {}, { namen: false });
  }
  if (n === 2 && !modell) {
    const { erzeugeViewer, ladeModell } = await import('./viewer.js');
    modell = erzeugeViewer(document.getElementById('start-modell'));
    modell.nummern(false);
    modell.explosion(0, false);                       // startet zusammengebaut
    modell.lade(await ladeModell('smartphone'));
    modell.drehen?.(true);
  }
}
// 3D-Modell im Wechsel: zusammenbauen und zerlegen, solange es zu sehen ist
function atme(n) {
  clearInterval(atmen);
  if (n === 2 && modell && !ruhig) { let zu = true; modell.explosion(0, false); atmen = setInterval(() => { zu = !zu; modell.explosion(zu ? 0 : 1); }, 2000); }
}
async function zeigeBild(n) {
  aktiv = n;
  await bereite(n);              // erst wechseln, wenn das Bild fertig geladen ist
  if (aktiv !== n) return;
  atme(n);
  document.querySelectorAll('.wechsel-bild').forEach((f) => f.classList.toggle('on', +f.dataset.n === n));
}
// Weltkarte und 3D-Modell schon im Hintergrund laden, damit der Wechsel ohne Warten klappt
(window.requestIdleCallback ?? ((f) => setTimeout(f, 800)))(() => { bereite(1).then(() => bereite(2)); });
if (!ruhig) setInterval(() => { if (!pause && !document.hidden) zeigeBild((aktiv + 1) % 3); }, 5000);
verbindeWaehler(app.querySelector('.waehler'));
