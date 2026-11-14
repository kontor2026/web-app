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
    <figure class="kreis" aria-label="Der Lebensweg eines Gegenstands in sieben Stationen">
      <svg viewBox="-290 -215 580 430" class="kreis-svg">
        <circle class="kreis-ring" r="${R}" pathLength="1" transform="rotate(-90)"/>
        ${punkte.map((p, i) => `<g transform="translate(${p.x.toFixed(1)} ${p.y.toFixed(1)})"><g class="kreis-punkt" style="--i:${i}">
          <circle r="30" class="${p.id === 'gegenstand' ? 'mitte' : ''}"/>
          <g transform="translate(-13 -13) scale(1.0833)">${icon(p.id).replace('<svg class="icon "', '<svg width="24" height="24" class="icon"')}</g>
          <text x="${(p.cx * 46).toFixed(1)}" y="${(p.cy * 46 + 4.5).toFixed(1)}" text-anchor="${p.cx > 0.3 ? 'start' : p.cx < -0.3 ? 'end' : 'middle'}">${p.name}</text></g></g>`).join('')}
      </svg>
    </figure>
    <div class="start-text">
      <h1>Wo kommt es her?<br>Wo geht es hin?</h1>
      <p class="lead">Wähle einen Gegenstand und folge seinem Weg.</p>
      ${waehlerHtml(atlas.objekte, (id) => `atlas/#kat=${id}`, { alle: false })}
    </div>
  </div>
</section>`;
if (ruhig) document.querySelector('.kreis').classList.add('ruhig');
verbindeWaehler(app.querySelector('.waehler'));
