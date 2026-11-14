// Kategorie-Modelle aus backend/seed/kategorien als three.js-Gruppen, mit denselben Formen und Oberflächen
// wie die 3D-Ansicht der App (packages/site/src/foto.js). Die Präsentation zeigt also genau die Modelle der App.
// Einheiten: die Modelle sind in mm, die Welt in m. Station-Achsen x Breite, y Tiefe, z Höhe → three X, Z, Y.
import * as THREE from 'three';
import { stoff, koerperGeometrie, stapelSuchen, huellenMesh, eigenschaften } from '../packages/site/src/foto.js';
import { CLASSES, MATERIALS } from '../js/data/catalog.js';

const farbeVon = (p) => p.color ?? CLASSES[MATERIALS[p.materials?.[0]?.[0]]?.cls]?.color ?? '#cccccc';

export async function ladeKategorie(id) {
  const res = await fetch(new URL(`../backend/seed/kategorien/${id}.json`, import.meta.url));
  if (!res.ok) throw new Error(`Kategorie ${id} fehlt (${res.status})`);
  return res.json();
}

function grundriss(t) {
  const s = new THREE.Shape(), w = t.w, d = t.d ?? t.w;
  if (t.shape === 'cyl') { s.absellipse(t.x + w / 2, t.y + d / 2, w / 2, d / 2, 0, Math.PI * 2, false, 0); return s; }
  const r = Math.max(0, Math.min(t.r ?? 0, w / 2, d / 2)), x = t.x, y = t.y;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r); s.lineTo(x + w, y + d - r);
  s.quadraticCurveTo(x + w, y + d, x + w - r, y + d); s.lineTo(x + r, y + d); s.quadraticCurveTo(x, y + d, x, y + d - r);
  s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
  return s;
}

/**
 * Baut ein Modell. pivot 'boden': Mitte der Grundfläche im Ursprung, 'mitte': Mitte des Quaders.
 * Rückgabe: { root, teile, explode(f), teil(name) } – explode(f) schiebt jedes Teil um f × seinen Explosionsweg.
 */
export function baueModell(obj, { pivot = 'boden', schatten = true, glasEinfach = false } = {}) {
  const root = new THREE.Group();
  const inner = new THREE.Group();
  inner.scale.setScalar(0.001);
  root.add(inner);
  const teile = [];
  for (const p of obj.parts) {
    const farbe = new THREE.Color(farbeVon(p));
    const g = new THREE.Group();
    const mat = stoff(p, farbe, p.opacity ?? 1);
    // Echte Lichtbrechung kostet einen zusätzlichen Renderdurchgang pro Bild. Für die Präsentation reicht klares Glas.
    if (glasEinfach && mat.transmission > 0) {
      Object.assign(mat, { transmission: 0, transparent: true, opacity: Math.min(0.45, (p.opacity ?? 0.3) + 0.1), roughness: 0.04, envMapIntensity: 0.9, depthWrite: false });
    }
    // Jedes Teil eigener Tiefenversatz: aufeinanderliegende Flächen flimmern dann nicht gegeneinander
    mat.polygonOffset = true; mat.polygonOffsetFactor = 1; mat.polygonOffsetUnits = 1 + teile.length * 4;
    const mesh = new THREE.Mesh(koerperGeometrie(p), mat);
    mesh.castShadow = schatten;
    mesh.receiveShadow = true;
    g.add(mesh);
    for (const m of p.marks ?? []) {
      if (m.zeichnung) continue;
      const mg = new THREE.ShapeGeometry(grundriss(m), 24);
      mg.rotateX(Math.PI / 2);
      mg.translate(0, p.h + 0.04, 0);
      const e = eigenschaften(p);
      const mm = new THREE.Mesh(mg, new THREE.MeshPhysicalMaterial({
        color: new THREE.Color(m.fill ?? farbe.clone().multiplyScalar(0.78)), metalness: e.m ?? 0, roughness: Math.max(0.25, e.r),
        clearcoat: e.cc ?? 0, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1,
      }));
      mm.receiveShadow = true;
      g.add(mm);
    }
    g.position.set(p.x, p.z, p.y);
    const t = {
      p, g, mesh, name: p.name,
      basis: new THREE.Vector3(p.x, p.z, p.y),
      ex: new THREE.Vector3(p.explode?.[0] ?? 0, p.explode?.[2] ?? 0, p.explode?.[1] ?? 0),
      mitte: new THREE.Vector3(p.w / 2, p.h / 2, (p.d ?? p.w) / 2),
    };
    inner.add(g);
    teile.push(t);
  }
  // Gestapelte Scheiben wie in der App als glatte Hülle zeigen
  for (const kette of stapelSuchen(obj.parts, farbeVon)) {
    const unten = teile[kette[0]], p0 = unten.p;
    const h = huellenMesh(kette.map((i) => obj.parts[i]), unten.mesh.material.clone());
    h.geometry.translate(-p0.x, -p0.z, -p0.y);
    h.castShadow = schatten;
    unten.g.add(h);
    kette.forEach((i) => { teile[i].mesh.visible = false; });
  }
  inner.updateMatrixWorld(true);
  const box = new THREE.Box3().setFromObject(inner);
  const c = box.getCenter(new THREE.Vector3());
  inner.position.set(-c.x, pivot === 'mitte' ? -c.y : -box.min.y, -c.z);
  const groesse = box.getSize(new THREE.Vector3());

  function explode(f) {
    for (const t of teile) t.g.position.copy(t.basis).addScaledVector(t.ex, f);
  }
  const teil = (re) => teile.find((t) => re.test(t.name));
  // Weltpunkt in der Mitte eines Teils (für Beschriftungen)
  const punkt = (t, ziel = new THREE.Vector3()) => t.g.localToWorld(ziel.copy(t.mitte));
  return { root, inner, teile, explode, teil, punkt, groesse };
}
