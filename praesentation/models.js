// Simple geometry building blocks for the workshop. Placeholder look on purpose: rounded boxes,
// cylinders and a shared material palette, no external model files.
import * as THREE from 'three';
import { RoundedBoxGeometry } from './assets/RoundedBoxGeometry.js';

export const palette = {
  floor: new THREE.MeshStandardMaterial({ color: '#2b2e31', roughness: 0.9 }),
  wall: new THREE.MeshStandardMaterial({ color: '#d9d4c7', roughness: 0.95 }),
  wallDark: new THREE.MeshStandardMaterial({ color: '#b9b3a5', roughness: 0.95 }),
  wood: new THREE.MeshStandardMaterial({ color: '#b07a45', roughness: 0.7 }),
  woodDark: new THREE.MeshStandardMaterial({ color: '#7a5230', roughness: 0.75 }),
  metal: new THREE.MeshStandardMaterial({ color: '#a7adb2', roughness: 0.35, metalness: 0.8 }),
  metalDark: new THREE.MeshStandardMaterial({ color: '#4a4f54', roughness: 0.45, metalness: 0.6 }),
  black: new THREE.MeshStandardMaterial({ color: '#1b1d1f', roughness: 0.5 }),
  accent: new THREE.MeshStandardMaterial({ color: '#d9480f', roughness: 0.55 }),
  blue: new THREE.MeshStandardMaterial({ color: '#2f6fb3', roughness: 0.6 }),
  green: new THREE.MeshStandardMaterial({ color: '#3d7a55', roughness: 0.6 }),
  yellow: new THREE.MeshStandardMaterial({ color: '#e0b43a', roughness: 0.6 }),
  scanPlate: new THREE.MeshStandardMaterial({ color: '#f2efe6', roughness: 0.4 }),
  screen: new THREE.MeshStandardMaterial({ color: '#0d0f10', roughness: 0.25, emissive: '#16201c', emissiveIntensity: 1 }),
};

function shadowed(mesh) {
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  return mesh;
}

/** Rounded box, positioned by its center. */
export function box(w, h, d, material, radius = 0.015) {
  const r = Math.min(radius, w / 2, h / 2, d / 2);
  return shadowed(new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 3, r), material));
}

export function cylinder(radiusTop, radiusBottom, height, material, segments = 24) {
  return shadowed(new THREE.Mesh(new THREE.CylinderGeometry(radiusTop, radiusBottom, height, segments), material));
}

/** Place a child at (x, y, z) inside a group and return the child. */
export function put(group, child, x = 0, y = 0, z = 0) {
  child.position.set(x, y, z);
  group.add(child);
  return child;
}

export function table(width, depth, height, top = palette.wood, legs = palette.metalDark) {
  const g = new THREE.Group();
  put(g, box(width, 0.05, depth, top, 0.01), 0, height - 0.025, 0);
  for (const sx of [-1, 1]) {
    for (const sz of [-1, 1]) {
      put(g, box(0.05, height - 0.05, 0.05, legs, 0.01), sx * (width / 2 - 0.06), (height - 0.05) / 2, sz * (depth / 2 - 0.06));
    }
  }
  put(g, box(width - 0.12, 0.03, 0.04, legs, 0.01), 0, 0.15, depth / 2 - 0.06);
  return g;
}

export function hammer() {
  const g = new THREE.Group();
  const handle = put(g, cylinder(0.014, 0.016, 0.32, palette.woodDark, 12), 0, 0.016, 0);
  handle.rotation.z = Math.PI / 2;
  put(g, box(0.05, 0.035, 0.11, palette.metal, 0.006), 0.15, 0.02, 0);
  return g;
}

export function screwdriver(material) {
  const g = new THREE.Group();
  const grip = put(g, cylinder(0.016, 0.016, 0.1, material, 12), 0, 0.016, 0);
  grip.rotation.z = Math.PI / 2;
  const shaft = put(g, cylinder(0.004, 0.004, 0.14, palette.metal, 8), 0.12, 0.016, 0);
  shaft.rotation.z = Math.PI / 2;
  return g;
}

export function saw() {
  const g = new THREE.Group();
  put(g, box(0.42, 0.004, 0.11, palette.metal, 0.002), 0.06, 0.004, 0);
  put(g, box(0.12, 0.03, 0.08, palette.accent, 0.012), -0.2, 0.015, 0);
  return g;
}

export function drill() {
  const g = new THREE.Group();
  put(g, box(0.2, 0.08, 0.07, palette.green, 0.02), 0, 0.2, 0);
  put(g, box(0.06, 0.16, 0.06, palette.green, 0.02), -0.04, 0.09, 0);
  put(g, box(0.08, 0.05, 0.08, palette.black, 0.015), -0.04, 0.025, 0);
  const chuck = put(g, cylinder(0.018, 0.012, 0.07, palette.metalDark, 12), 0.13, 0.2, 0);
  chuck.rotation.z = Math.PI / 2;
  return g;
}

export function vise() {
  const g = new THREE.Group();
  put(g, box(0.18, 0.06, 0.12, palette.blue, 0.01), 0, 0.03, 0);
  put(g, box(0.05, 0.08, 0.12, palette.blue, 0.01), -0.06, 0.1, 0);
  put(g, box(0.05, 0.08, 0.12, palette.blue, 0.01), 0.06, 0.1, 0);
  return g;
}

export function bin(material, w = 0.3, h = 0.18, d = 0.4) {
  const g = new THREE.Group();
  put(g, box(w, h, d, material, 0.02), 0, h / 2, 0);
  put(g, box(w * 0.5, 0.03, 0.01, palette.black, 0.005), 0, h * 0.75, d / 2);
  return g;
}

export function shelf(width, height, depth, levels = 4) {
  const g = new THREE.Group();
  for (const sx of [-1, 1]) put(g, box(0.04, height, depth, palette.metalDark, 0.008), sx * (width / 2 - 0.02), height / 2, 0);
  for (let i = 0; i < levels; i++) put(g, box(width, 0.03, depth, palette.metalDark, 0.006), 0, 0.15 + i * (height - 0.2) / (levels - 1), 0);
  return g;
}

/** Monitor facing +z. Returns the group and the screen mesh (a plane exactly the visible screen area). */
export function monitor(screenW = 0.96, screenH = 0.6) {
  const g = new THREE.Group();
  const bezel = 0.025;
  put(g, box(screenW + bezel * 2, screenH + bezel * 2, 0.04, palette.black, 0.01), 0, 0, 0);
  const screen = put(g, new THREE.Mesh(new THREE.PlaneGeometry(screenW, screenH), palette.screen), 0, 0, 0.0205);
  put(g, box(0.06, 0.32, 0.05, palette.metalDark, 0.01), 0, -screenH / 2 - 0.12, -0.05);
  put(g, box(0.3, 0.02, 0.2, palette.metalDark, 0.01), 0, -screenH / 2 - 0.28, -0.03);
  return { group: g, screen };
}

/** Overhead camera on a stand, lens pointing down. */
export function cameraStand(height = 0.75, reach = 0.35) {
  const g = new THREE.Group();
  put(g, box(0.2, 0.02, 0.16, palette.metalDark, 0.008), 0, 0.01, 0);
  put(g, cylinder(0.015, 0.015, height, palette.metal, 12), 0, height / 2, 0);
  const arm = put(g, cylinder(0.012, 0.012, reach, palette.metal, 12), reach / 2, height, 0);
  arm.rotation.z = Math.PI / 2;
  put(g, box(0.11, 0.06, 0.08, palette.black, 0.012), reach, height - 0.04, 0);
  put(g, cylinder(0.025, 0.025, 0.03, palette.metalDark, 16), reach, height - 0.085, 0);
  put(g, cylinder(0.012, 0.012, 0.005, palette.accent, 12), reach, height - 0.1, 0);
  return g;
}
