// The one continuous 3D world: workshop with door, workbench and tools, shelf, and the scan station
// with overhead camera and monitor. Also defines the camera stations ("shots") the slides refer to.
import * as THREE from 'three';
import {
  palette, box, cylinder, put, table, hammer, screwdriver, saw, drill, vise, bin, shelf, monitor, cameraStand,
} from './models.js';

const v = (x, y, z) => new THREE.Vector3(x, y, z);

// Room: floor 12 m x 10 m, walls 3.2 m high, door in the front wall (z = +5) at x = 0.
const ROOM = { w: 12, d: 10, h: 3.2, doorW: 1.2, doorH: 2.2 };

/** Camera stations: where the camera stands and what it looks at. Monitor shots are added in buildWorld. */
export const shots = {
  tuer: { pos: v(0, 1.65, 8.5), target: v(0, 1.3, 0) },
  werkbank: { pos: v(-1.4, 1.95, -1.6), target: v(-3, 1.0, -4.3) },
  station: { pos: v(0.6, 1.7, -0.4), target: v(2.0, 1.2, -2.5) },
  ueberblick: { pos: v(6.5, 7.5, 7.5), target: v(-0.5, 0.6, -1.5) },
};

function room(scene) {
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(ROOM.w + 8, ROOM.d + 10), palette.floor);
  floor.rotation.x = -Math.PI / 2;
  floor.position.z = 2;
  floor.receiveShadow = true;
  scene.add(floor);

  const halfW = ROOM.w / 2, halfD = ROOM.d / 2, t = 0.1;
  put(scene, box(ROOM.w, ROOM.h, t, palette.wall, 0.005), 0, ROOM.h / 2, -halfD);
  put(scene, box(t, ROOM.h, ROOM.d, palette.wallDark, 0.005), -halfW, ROOM.h / 2, 0);
  put(scene, box(t, ROOM.h, ROOM.d, palette.wallDark, 0.005), halfW, ROOM.h / 2, 0);

  // Front wall with a door opening.
  const side = halfW - ROOM.doorW / 2;
  put(scene, box(side, ROOM.h, t, palette.wall, 0.005), -(ROOM.doorW / 2 + side / 2), ROOM.h / 2, halfD);
  put(scene, box(side, ROOM.h, t, palette.wall, 0.005), ROOM.doorW / 2 + side / 2, ROOM.h / 2, halfD);
  put(scene, box(ROOM.doorW, ROOM.h - ROOM.doorH, t, palette.wall, 0.005), 0, ROOM.doorH + (ROOM.h - ROOM.doorH) / 2, halfD);
  for (const sx of [-1, 1]) put(scene, box(0.06, ROOM.doorH, 0.16, palette.accent, 0.01), sx * (ROOM.doorW / 2 + 0.03), ROOM.doorH / 2, halfD);
  put(scene, box(ROOM.doorW + 0.12, 0.06, 0.16, palette.accent, 0.01), 0, ROOM.doorH + 0.03, halfD);
  // Door leaf, swung open outwards.
  put(scene, box(0.04, ROOM.doorH - 0.05, ROOM.doorW - 0.1, palette.woodDark, 0.01), ROOM.doorW / 2 + 0.04, (ROOM.doorH - 0.05) / 2, halfD + 0.6);
}

function workbench(scene) {
  const g = new THREE.Group();
  g.position.set(-3, 0, -4.3);
  scene.add(g);
  put(g, table(2.4, 0.8, 0.9, palette.wood, palette.metalDark));
  const top = 0.9;
  put(g, hammer(), -0.75, top, 0.1).rotation.y = 0.3;
  put(g, screwdriver(palette.accent), -0.3, top, 0.2).rotation.y = -0.2;
  put(g, screwdriver(palette.yellow), -0.25, top, 0.05).rotation.y = -0.35;
  put(g, saw(), 0.35, top, -0.1).rotation.y = 0.15;
  put(g, drill(), 0.85, top, 0.05).rotation.y = -0.5;
  put(g, vise(), -1.0, top, -0.2);
  put(g, bin(palette.blue, 0.22, 0.12, 0.3), 0.1, top, 0.22);

  // Pegboard with tool silhouettes on the back wall.
  const board = put(scene, box(2.2, 1.0, 0.03, palette.woodDark, 0.006), -3, 1.65, -4.93);
  board.receiveShadow = true;
  const tools = [[-0.8, 0.15, 0.04, 0.45], [-0.55, 0.05, 0.03, 0.35], [-0.3, 0.1, 0.25, 0.04], [0.1, -0.05, 0.05, 0.4],
    [0.35, 0.15, 0.3, 0.05], [0.7, 0, 0.06, 0.5], [0.9, 0.2, 0.18, 0.18]];
  for (const [x, y, w, h] of tools) put(scene, box(w, h, 0.03, palette.metal, 0.005), -3 + x, 1.65 + y, -4.9);
}

function storage(scene) {
  const g = new THREE.Group();
  g.position.set(-5.65, 0, -1.2);
  g.rotation.y = Math.PI / 2;
  scene.add(g);
  put(g, shelf(2.2, 1.9, 0.5, 4));
  const colors = [palette.blue, palette.accent, palette.green, palette.yellow];
  for (let level = 0; level < 4; level++) {
    for (let i = 0; i < 4; i++) {
      put(g, bin(colors[(level + i) % colors.length], 0.4, 0.22, 0.42), -0.78 + i * 0.52, 0.165 + level * 0.567, 0);
    }
  }
}

function station(scene) {
  const g = new THREE.Group();
  g.position.set(2.0, 0, -2.4);
  scene.add(g);
  put(g, table(1.6, 0.8, 0.9, palette.metalDark, palette.metalDark));
  const top = 0.9;
  put(g, box(0.5, 0.01, 0.4, palette.scanPlate, 0.004), -0.25, top + 0.005, 0.05);
  put(g, cameraStand(0.75, 0.35), -0.6, top, 0.05);
  // Something brought along, waiting on the scan plate: a bottle.
  const glass = new THREE.MeshStandardMaterial({ color: '#9fd0e8', roughness: 0.2, transparent: true, opacity: 0.75 });
  put(g, cylinder(0.035, 0.035, 0.16, glass, 20), -0.25, top + 0.09, 0.05);
  put(g, cylinder(0.014, 0.014, 0.03, palette.blue, 12), -0.25, top + 0.185, 0.05);

  const m = monitor(0.96, 0.6);
  put(g, m.group, 0.35, top + 0.59, -0.3);
  return m.screen;
}

function clutter(scene) {
  // A few brought-along things near the door: boxes and cans.
  put(scene, box(0.45, 0.32, 0.35, palette.wood, 0.01), 1.6, 0.16, 3.6).rotation.y = 0.4;
  put(scene, box(0.3, 0.22, 0.3, palette.wood, 0.01), 1.75, 0.48, 3.55).rotation.y = -0.2;
  put(scene, cylinder(0.04, 0.04, 0.12, palette.metal, 16), 1.1, 0.06, 3.9);
  put(scene, cylinder(0.04, 0.04, 0.12, palette.accent, 16), 1.2, 0.06, 4.05);
}

/**
 * Build the world into the scene. Returns label anchors and the monitor screen
 * (world corners for placing the app on top of it).
 */
export function buildWorld(scene) {
  room(scene);
  workbench(scene);
  storage(scene);
  clutter(scene);
  const screen = station(scene);
  scene.updateMatrixWorld(true);

  const { width, height } = screen.geometry.parameters;
  const local = [v(-width / 2, height / 2, 0), v(width / 2, height / 2, 0), v(width / 2, -height / 2, 0), v(-width / 2, -height / 2, 0)];
  const corners = local.map((p) => screen.localToWorld(p.clone()));
  const center = screen.localToWorld(v(0, 0, 0));
  const normal = v(0, 0, 1).transformDirection(screen.matrixWorld);

  // Camera distance at which the screen fills a given share of the view height.
  const fovRad = THREE.MathUtils.degToRad(45);
  const distanceFor = (share) => height / share / (2 * Math.tan(fovRad / 2));
  shots.monitor = { pos: center.clone().addScaledVector(normal, distanceFor(0.78)), target: center.clone() };
  shots.bildschirm = { pos: center.clone().addScaledVector(normal, distanceFor(1)), target: center.clone() };

  const anchors = {
    werkbank: v(-3, 1.2, -4.1),
    kamera: v(1.75, 1.78, -2.35),
    scanflaeche: v(1.65, 1.0, -2.2),
    monitor: v(center.x, center.y + height / 2 + 0.12, center.z),
    lager: v(-5.4, 2.05, -1.2),
  };
  return { anchors, screen: { corners, center, normal, width, height } };
}
