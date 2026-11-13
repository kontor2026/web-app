// Übersicht: drei Bereiche als Karten, rechts der Stand der Daten. Layout wie „Bauen“ in der Station (.craft).
import { shell, esc, quelleA, repoLink } from './shell.js';
import index from '../../../backend/seed/kategorien/index.json';
import atlas from './daten/atlas.json';
import { KOMPASS } from './kompass/inhalt.js';

const app = shell('start', './');
const hand = index.filter((k) => !k.platzhalter).length;
const mitHerkunft = Object.values(atlas.rohstoffe).filter((r) => r.abbau || r.verarbeitung).length;
const offen = KOMPASS.richtungen.reduce((s, r) => s + (r.offen?.length ?? 0), 0);

const KARTEN = [
  { href: 'atlas/', titel: 'Rohstoff-Atlas', frage: 'Woraus besteht ein Gegenstand, und woher kommen seine Rohstoffe?',
    meta: [`${atlas.objekte.length} Gegenstände`, `${Object.keys(atlas.rohstoffe).length} Rohstoffe`],
    ziel: 'Vom Gegenstand über Bauteile und Materialien bis zu den Ländern, in denen die Rohstoffe abgebaut werden.', knopf: 'Gegenstand wählen' },
  { href: 'modelle/', titel: '3D-Modelle', frage: 'Stimmen die Explosionszeichnungen?',
    meta: [`${hand} von ${index.length} handgebaut`, 'drehbar in 3D'],
    ziel: 'Jedes Modell zusammengebaut und explodiert ansehen, Teile antippen, Gewicht und Prüfhinweise vergleichen.', knopf: 'Modelle prüfen' },
  { href: 'kompass/', titel: 'KI-Kompass', frage: KOMPASS.frage,
    meta: [`${KOMPASS.richtungen.length} Richtungen`, `${offen} offene Punkte`],
    ziel: 'Wo die KI in der Station arbeitet, wer entscheidet und was wir noch nicht gelöst haben.', knopf: 'Kompass öffnen' },
];

app.innerHTML = `
<section class="view craft start">
  <div class="craft-main">
    <div class="craft-head">
      <div>
        <div class="eyebrow">Übersicht</div>
        <h1 style="margin-top:8px">Was steckt in unseren Dingen?</h1>
        <p class="lead">Drei Bereiche der Kreislauf-Station zum Ansehen im Browser. Wähle einen aus.</p>
      </div>
    </div>
    <div class="ideas">
      ${KARTEN.map((k, i) => `
      <a class="idea karte-link" href="${k.href}">
        <div class="letter">0${i + 1}</div>
        <div>
          <h2>${esc(k.titel)}</h2>
          <p class="kurz">${esc(k.frage)}</p>
        </div>
        <div class="meta">${k.meta.map((m) => `<span>${esc(m)}</span>`).join('')}</div>
        <div class="goal"><small>Was du hier machst</small>${esc(k.ziel)}</div>
        <span class="btn primary">${esc(k.knopf)} →</span>
      </a>`).join('')}
    </div>
  </div>
  <aside class="inv">
    <h3>Stand der Daten</h3>
    <p>Alles auf dieser Seite kommt aus dem Repository, ohne KI und ohne Server.</p>
    <div class="irow"><span class="f">Modelle</span><span>handgebaut</span><span class="q">${hand} / ${index.length}</span></div>
    <div class="mbar fortschritt"><b style="width:${(hand / index.length) * 100}%"></b></div>
    <div class="irow"><span class="f">Herkunft</span><span>Rohstoffe mit Länderdaten</span><span class="q">${mitHerkunft} / ${Object.keys(atlas.rohstoffe).length}</span></div>
    <div class="irow"><span class="f">KI</span><span>offene Punkte im Kompass</span><span class="q">${offen}</span></div>
    <h3 style="margin-top:28px">Quellen</h3>
    <ul class="quellen-liste">
      <li>${repoLink('data/classifier.json', 'Bauteile und Materialien (data/classifier.json)')}</li>
      ${Object.keys(atlas.quellen).map((k) => `<li>${quelleA(atlas.quellen, k)}</li>`).join('')}
    </ul>
  </aside>
</section>`;
