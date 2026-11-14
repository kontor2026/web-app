// Mo, das Holz-Mannequin: Führer durch die Seite. Reines SVG, keine Abhängigkeiten.
// Die Arme drehen sich um die Schultern (CSS-Variablen --arm-l / --arm-r in Grad, 0 = hängt nach unten),
// damit Mo beim Rundgang auf das zeigen kann, worum es gerade geht.
const HOLZ = '#EBCDA3', SCHATTEN = '#CFA471', GELENK = '#8A6440', LINIE = '#3B2D20';

export const moSvg = ({ klasse = '', nurKopf = false } = {}) => nurKopf
  ? `<svg class="mo mo-kopf ${klasse}" viewBox="26 2 48 44" aria-hidden="true">${kopf()}</svg>`
  : `<svg class="mo ${klasse}" viewBox="0 0 100 112" aria-hidden="true">
  <g class="mo-koerper">
    ${arm('l', 28)}${arm('r', 72)}
    <path d="M30 50c0-4 4-7 8-7h24c4 0 8 3 8 7l3 40H27Z" fill="var(--accent)" stroke="${LINIE}" stroke-width="1.6" stroke-linejoin="round"/>
    <path d="M44 43h12v6H44Z" fill="${SCHATTEN}" stroke="${LINIE}" stroke-width="1.4"/>
    <path d="M36 66h28M35 78h30" stroke="${LINIE}" stroke-opacity=".28" stroke-width="1.2" stroke-linecap="round"/>
    <circle cx="28" cy="50" r="5" fill="${GELENK}" stroke="${LINIE}" stroke-width="1.4"/><circle cx="72" cy="50" r="5" fill="${GELENK}" stroke="${LINIE}" stroke-width="1.4"/>
    <g class="mo-hals">${kopf()}</g>
  </g></svg>`;

function kopf() {
  return `<ellipse cx="50" cy="24" rx="14" ry="16.5" fill="${HOLZ}" stroke="${LINIE}" stroke-width="1.6"/>
    <path d="M38 17c3-5 8-7 12-7s9 2 12 7" fill="none" stroke="${SCHATTEN}" stroke-width="2" stroke-linecap="round"/>
    <g class="mo-augen"><ellipse cx="44" cy="25" rx="1.9" ry="2.4" fill="${LINIE}"/><ellipse cx="56" cy="25" rx="1.9" ry="2.4" fill="${LINIE}"/></g>
    <path d="M45 32c2.5 2.6 7.5 2.6 10 0" fill="none" stroke="${LINIE}" stroke-width="1.6" stroke-linecap="round"/>`;
}

// Arm als gerade Gliederpuppe: Oberarm, Unterarm, Hand. Pivot = Schulter.
function arm(seite, x) {
  return `<g class="mo-arm ${seite}" style="transform-origin:${x}px 50px;transform:rotate(var(--arm-${seite},0deg))">
    <path d="M${x} 50v34" stroke="${LINIE}" stroke-width="9.6" stroke-linecap="round"/>
    <path d="M${x} 50v34" stroke="${HOLZ}" stroke-width="7" stroke-linecap="round"/>
    <circle cx="${x}" cy="67" r="3.2" fill="${GELENK}"/>
    <circle cx="${x}" cy="86" r="5.2" fill="${HOLZ}" stroke="${LINIE}" stroke-width="1.5"/></g>`;
}
