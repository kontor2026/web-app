// Mo, das Holz-Mannequin: Führer durch die Seite. Reines SVG, keine Abhängigkeiten.
// Brustbild, das von unten ins Bild schaut. Gesteuert wird nur über CSS-Variablen am <svg>:
//   --arm-l / --arm-r  Drehung an der Schulter (0 = hängt, positiv = Hand wandert nach links)
//   --ell-l / --ell-r  Knick im Ellbogen
//   --kopf             Neigung des Kopfes, --blick-x / --blick-y  wohin die Augen schauen
// Keine sichtbaren Gelenke: jeder Arm ist zweimal gezeichnet, erst alle Umrisse, darüber alle Flächen.
// So verschmelzen Oberarm, Unterarm und Hand zu einer Form, egal wie sie gerade gedreht sind.
const HOLZ = '#EDD2AB', HOLZ2 = '#D9B685', LINIE = '#3B2D20';
export const SCHULTER = { l: [43, 71], r: [77, 71] };
const OBER = 23, UNTER = 20;
let nr = 0;

export function moSvg({ klasse = '', nurKopf = false } = {}) {
  const id = `mo${++nr}`;
  if (nurKopf) return `<svg class="mo mo-kopf ${klasse}" viewBox="39 11 42 46" aria-hidden="true">${defs(id)}${kopf(id)}</svg>`;
  return `<svg class="mo ${klasse}" viewBox="0 0 120 130" aria-hidden="true">${defs(id)}
  <g class="mo-koerper">
    <ellipse class="mo-schatten" cx="60" cy="128" rx="28" ry="5" fill="#000" opacity=".25"/>
    <g class="mo-arme-umriss">${arm('l', 'umriss', id)}${arm('r', 'umriss', id)}</g>
    <g class="mo-arme">${arm('l', 'flaeche', id)}${arm('r', 'flaeche', id)}</g>
    <path d="M53 50h14v12c-4 3-10 3-14 0Z" fill="${HOLZ2}" stroke="${LINIE}" stroke-width="1.3"/>
    <path d="M40.5 78c0-12 6-19 15-19h9c9 0 15 7 15 19l2 56H38.5Z" fill="url(#${id}-hemd)" stroke="${LINIE}" stroke-width="1.5" stroke-linejoin="round"/>
    <path d="M53.5 59.5c2 4.6 11 4.6 13 0" fill="none" stroke="${LINIE}" stroke-opacity=".5" stroke-width="1.3" stroke-linecap="round"/>
    <path d="M47 88c4 1.6 22 1.6 26 0" fill="none" stroke="#000" stroke-opacity=".08" stroke-width="5" stroke-linecap="round"/>
    <g class="mo-hals">${kopf(id)}</g>
  </g></svg>`;
}

const defs = (id) => `<defs>
  <linearGradient id="${id}-hemd" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="var(--accent)"/><stop offset="1" stop-color="var(--accent-hover)"/></linearGradient>
  <radialGradient id="${id}-holz" cx=".38" cy=".32" r=".8"><stop offset="0" stop-color="#F8E7CC"/><stop offset=".7" stop-color="${HOLZ}"/><stop offset="1" stop-color="${HOLZ2}"/></radialGradient></defs>`;

function kopf(id) {
  return `<g class="mo-kopf-neigung"><g class="mo-kopf-ruhe">
    <ellipse cx="60" cy="33" rx="17" ry="19.5" fill="url(#${id}-holz)" stroke="${LINIE}" stroke-width="1.5"/>
    <path d="M47 23c4-6 9-8 13-8s9 2 13 8" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" opacity=".35"/>
    <g class="mo-brauen"><path d="M48.5 27.5q4-2.6 7.5-.8M64 26.7q3.5-1.8 7.5.8" fill="none" stroke="${LINIE}" stroke-width="1.3" stroke-linecap="round" opacity=".8"/></g>
    <g class="mo-blick"><g class="mo-augen">
      <ellipse cx="53" cy="33.5" rx="2.2" ry="2.8" fill="${LINIE}"/><ellipse cx="67" cy="33.5" rx="2.2" ry="2.8" fill="${LINIE}"/>
      <circle cx="53.8" cy="32.4" r=".75" fill="#fff"/><circle cx="67.8" cy="32.4" r=".75" fill="#fff"/></g></g>
    <ellipse cx="48" cy="40" rx="3.2" ry="1.9" fill="var(--accent)" opacity=".25"/><ellipse cx="72" cy="40" rx="3.2" ry="1.9" fill="var(--accent)" opacity=".25"/>
    <path class="mo-mund-zu" d="M54.5 41.5c3 3.2 8 3.2 11 0" fill="none" stroke="${LINIE}" stroke-width="1.6" stroke-linecap="round"/>
    <g class="mo-mund-auf"><path d="M55 41c1.5 4.6 8.5 4.6 10 0Z" fill="${LINIE}"/><path d="M57.5 43.6q2.5 1.2 5 0" fill="none" stroke="#C9655A" stroke-width="1.2" stroke-linecap="round"/></g>
  </g></g>`;
}

// Ein Arm, an der Schulter drehbar; darin der Unterarm, am Ellbogen drehbar. Der Ärmel liegt über dem Ellbogen.
function arm(seite, art, id) {
  const [x, y] = SCHULTER[seite], ex = y + OBER, hy = ex + UNTER + 3;
  const umriss = art === 'umriss';
  const strich = (breite, farbe) => `fill="none" stroke="${farbe}" stroke-width="${breite}" stroke-linecap="round"`;
  return `<g class="mo-arm ${seite}" style="transform-origin:${x}px ${y}px">
    <g class="mo-unter" style="transform-origin:${x}px ${ex}px">
      <path d="M${x} ${ex}V${ex + UNTER}" ${umriss ? strich(10.6, LINIE) : strich(8, HOLZ)}/>
      <g class="mo-hand" style="transform-origin:${x}px ${ex + UNTER}px">
        <ellipse cx="${x}" cy="${hy}" rx="${umriss ? 7.1 : 5.8}" ry="${umriss ? 7.9 : 6.6}" fill="${umriss ? LINIE : `url(#${id}-holz)`}"/>
        ${umriss ? '' : `<path d="M${x - (seite === 'l' ? -4.6 : 4.6)} ${hy - 3}q${seite === 'l' ? 3 : -3} 1 ${seite === 'l' ? 3.4 : -3.4} 4" fill="none" stroke="${LINIE}" stroke-width="1" stroke-linecap="round" opacity=".55"/>`}
      </g>
    </g>
    <path d="M${x} ${y}V${ex}" ${umriss ? strich(15.4, LINIE) : strich(12.6, 'var(--accent)')}/>
  </g>`;
}
