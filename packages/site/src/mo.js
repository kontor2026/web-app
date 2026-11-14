// Mo, das Holz-Mannequin: Führer durch die Seite. Reines SVG, keine Abhängigkeiten.
// Die Arme drehen sich um die Schultern (CSS-Variablen --arm-l / --arm-r in Grad, 0 = hängt nach unten).
// Kein sichtbares Gelenk: der Ärmel geht fließend in den Unterarm über, der Ellbogen knickt nur leicht.
const HOLZ = '#EDD2AB', HOLZ2 = '#D9B685', LINIE = '#3B2D20';

export const moSvg = ({ klasse = '', nurKopf = false } = {}) => nurKopf
  ? `<svg class="mo mo-kopf ${klasse}" viewBox="26 2 48 44" aria-hidden="true">${defs()}${kopf()}</svg>`
  : `<svg class="mo ${klasse}" viewBox="0 0 100 112" aria-hidden="true">${defs()}
  <g class="mo-koerper">
    ${arm('l', 29)}${arm('r', 71)}
    <path d="M28 54c0-6 5-10 11-10h22c6 0 11 4 11 10l2 38H26Z" fill="url(#mo-hemd)" stroke="${LINIE}" stroke-width="1.4" stroke-linejoin="round"/>
    <path d="M43 44.5c2 3.5 12 3.5 14 0" fill="none" stroke="${LINIE}" stroke-opacity=".55" stroke-width="1.2" stroke-linecap="round"/>
    <path d="M45 40h10v6c-3 2-7 2-10 0Z" fill="${HOLZ2}" stroke="${LINIE}" stroke-width="1.2"/>
    <g class="mo-hals">${kopf()}</g>
  </g></svg>`;

const defs = () => `<defs>
  <linearGradient id="mo-hemd" x1="0" x2="1"><stop offset="0" stop-color="var(--accent)"/><stop offset="1" stop-color="var(--accent-hover)"/></linearGradient>
  <radialGradient id="mo-holz" cx=".4" cy=".35" r=".75"><stop offset="0" stop-color="#F6E2C3"/><stop offset="1" stop-color="${HOLZ}"/></radialGradient></defs>`;

function kopf() {
  return `<ellipse cx="50" cy="24" rx="14" ry="16.5" fill="url(#mo-holz)" stroke="${LINIE}" stroke-width="1.4"/>
    <path d="M39.5 16.5c3-4.5 7.5-6.5 10.5-6.5s7.500 2 10.500 6.500" fill="none" stroke="${HOLZ2}" stroke-width="2" stroke-linecap="round" opacity=".7"/>
    <path d="M40.500 20.200q3.500-2 6.500-.5M53 19.700q3-1.500 6.500.5" fill="none" stroke="${LINIE}" stroke-width="1.100" stroke-linecap="round" opacity=".75"/>
    <g class="mo-augen"><ellipse cx="44" cy="25" rx="1.800" ry="2.300" fill="${LINIE}"/><ellipse cx="56" cy="25" rx="1.800" ry="2.300" fill="${LINIE}"/></g>
    <ellipse cx="40" cy="30" rx="2.600" ry="1.600" fill="var(--accent)" opacity=".22"/><ellipse cx="60" cy="30" rx="2.600" ry="1.600" fill="var(--accent)" opacity=".22"/>
    <path d="M45 31.500c2.500 2.800 7.500 2.800 10 0" fill="none" stroke="${LINIE}" stroke-width="1.500" stroke-linecap="round"/>`;
}

// Arm: Oberarm im Hemdsärmel (orange), Unterarm aus Holz mit rundlicher Hand. Pivot = Schulter, Ellbogen = (x, 68).
function arm(seite, x) {
  return `<g class="mo-arm ${seite}" style="transform-origin:${x}px 52px;transform:rotate(var(--arm-${seite},0deg))">
    <g class="mo-unter" style="transform-origin:${x}px 68px">
      <rect x="${x - 3.200}" y="64" width="6.400" height="21" rx="3.200" fill="${HOLZ}" stroke="${LINIE}" stroke-width="1.200"/>
      <ellipse cx="${x}" cy="87.500" rx="4.300" ry="5" fill="url(#mo-holz)" stroke="${LINIE}" stroke-width="1.200"/></g>
    <rect x="${x - 5.200}" y="46" width="10.400" height="24" rx="5.200" fill="var(--accent)" stroke="${LINIE}" stroke-width="1.300"/></g>`;
}
