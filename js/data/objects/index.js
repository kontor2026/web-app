// Registry aller bekannten Objekte. Ein neues Objekt = eine neue Datei + Import und Eintrag hier.
// Später liefert das Backend (KI) diese Daten als JSON, der Renderer bleibt gleich.
import smartphone from './smartphone.js';

export const OBJECTS = [
  smartphone,
];
export const getObject = (id) => OBJECTS.find((o) => o.id === id);
