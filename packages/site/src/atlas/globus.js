// Globus im Stil einer technischen Zeichnung: Papierfarbe, Gradnetz, Tintenlinien.
// Länder mit Anteil werden wie die Bauteile der Station extrudiert, Bögen zeigen den Weg nach Deutschland.
import Globe from 'globe.gl';
import * as THREE from 'three';
import { feature } from 'topojson-client';
import { geoArea, geoCentroid } from 'd3-geo';
import welt from 'world-atlas/countries-110m.json';
import { esc, zahl, ruhig } from '../shell.js';

const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const mische = (a, b, t) => `#${new THREE.Color(a).lerp(new THREE.Color(b), t).getHexString()}`;
const DEUTSCHLAND = '276';

// Schwerpunkt der größten Teilfläche, damit z. B. Frankreich nicht im Atlantik landet
function mitte(f) {
  if (f.geometry.type !== 'MultiPolygon') return geoCentroid(f);
  const teile = f.geometry.coordinates.map((c) => ({ type: 'Feature', geometry: { type: 'Polygon', coordinates: c } }));
  return geoCentroid(teile.sort((a, b) => geoArea(b) - geoArea(a))[0]);
}

export function erzeugeGlobus(el, laender) {
  const F = { paper: css('--paper'), sheet: css('--sheet'), card: css('--card'), ink: css('--ink'), ink3: css('--ink-3'),
    rule: css('--rule'), accent: css('--accent'), soft: css('--accent-soft') };
  const zuNum = Object.fromEntries(Object.entries(laender).map(([a3, l]) => [l.num, a3]));
  const laenderGeo = feature(welt, welt.objects.countries).features.map((f) => {
    const [lng, lat] = mitte(f);
    return { ...f, a3: zuNum[f.id] ?? null, lat, lng, anteil: 0 };
  });
  const de = laenderGeo.find((f) => f.id === DEUTSCHLAND);
  let hervor = null, maxAnteil = 1;

  const hoehe = (f) => (f.anteil ? 0.012 + 0.22 * (f.anteil / 100) : f === de ? 0.012 : 0.004);
  const kappe = (f) => (f.a3 && f.a3 === hervor ? F.ink : f.anteil ? mische(F.soft, F.accent, 0.25 + 0.75 * (f.anteil / maxAnteil)) : f === de ? F.ink3 : F.sheet);

  const globus = new Globe(el, { animateIn: false })
    .backgroundColor('rgba(0,0,0,0)')
    .showAtmosphere(false)
    .showGraticules(true)
    .globeMaterial(new THREE.MeshLambertMaterial({ color: F.paper }))
    .polygonsData(laenderGeo)
    .polygonAltitude(hoehe)
    .polygonCapColor(kappe)
    .polygonSideColor((f) => (f.anteil ? mische(F.accent, F.ink, 0.35) : F.rule))
    .polygonStrokeColor(() => F.ink3)
    .polygonsTransitionDuration(ruhig ? 0 : 700)
    .polygonLabel((f) => `<div class="tip"><b>${esc(laender[f.a3]?.name ?? f.properties.name)}</b>${f.anteil ? `<small>${zahl(f.anteil, 0)} %</small>` : f === de ? '<small>hier wird der Gegenstand genutzt</small>' : ''}</div>`)
    .arcColor(() => F.accent)
    .arcStroke((a) => 0.25 + 1.1 * (a.anteil / maxAnteil))
    .arcAltitudeAutoScale(0.35)
    .arcDashLength(0.4).arcDashGap(0.2).arcDashAnimateTime(ruhig ? 0 : 2800)
    .htmlElement((d) => {
      const div = document.createElement('div');
      div.className = `globus-ballon ${d.de ? 'de' : ''}`;
      div.innerHTML = d.de ? '<b>DE</b>' : `<b>${d.nr}</b><span>${esc(d.name)} · ${zahl(d.anteil, 0)} %</span>`;
      return div;
    })
    .htmlAltitude((d) => d.alt)
    .htmlTransitionDuration(ruhig ? 0 : 500);
  globus.controls().enableZoom = true;
  globus.controls().autoRotate = false;
  globus.pointOfView({ lat: 25, lng: 15, altitude: 2.1 });
  // Graticule in Linienfarbe der Zeichnung
  globus.scene().traverse((o) => { if (o.type === 'LineSegments' && o.material?.color) { o.material.color.set(F.rule); o.material.opacity = 0.9; o.material.transparent = true; } });

  new ResizeObserver(() => { const r = el.getBoundingClientRect(); globus.width(r.width).height(r.height); }).observe(el);

  return {
    // anteile: { ISO3: Prozent } — leer = nur Deutschland zeigen
    zeige(anteile = {}, { fokus = true } = {}) {
      const werte = Object.values(anteile);
      maxAnteil = Math.max(1, ...werte);
      for (const f of laenderGeo) f.anteil = (f.a3 && anteile[f.a3]) || 0;
      const rang = laenderGeo.filter((f) => f.anteil > 0 && f !== de).sort((a, b) => b.anteil - a.anteil);
      globus.polygonsData(laenderGeo);
      globus.arcsData(rang.map((f) => ({ startLat: f.lat, startLng: f.lng, endLat: de.lat, endLng: de.lng, anteil: f.anteil })));
      globus.htmlElementsData([
        ...rang.slice(0, 3).map((f, i) => ({ lat: f.lat, lng: f.lng, alt: hoehe(f) + 0.01, nr: String(i + 1).padStart(2, '0'), name: laender[f.a3]?.name ?? f.properties.name, anteil: f.anteil })),
        { lat: de.lat, lng: de.lng, alt: 0.03, de: true },
      ]);
      if (fokus) {
        const z = rang[0] ?? de;
        globus.pointOfView({ lat: (z.lat + de.lat) / 2, lng: (z.lng + de.lng) / 2, altitude: rang.length ? 1.75 : 2.1 }, ruhig ? 0 : 1100);
      }
    },
    hebeHervor(a3) { hervor = a3; globus.polygonCapColor(kappe); },
  };
}
