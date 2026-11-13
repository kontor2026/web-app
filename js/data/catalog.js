// Gemeinsamer Katalog: Materialklassen, Materialien, Elemente.
// Objekte referenzieren nur IDs. Ein neues Objekt braucht daher meist
// keine neuen Materialien, sondern nur eine neue Bauteilliste.
// Alle Werte sind Richtwerte für das Mockup und noch nicht verifiziert.

export const CLASSES = {
  metall:     { label: 'Metall',          color: '#AEB5B9' },
  kunststoff: { label: 'Kunststoff',      color: '#E3D2AE' },
  glas:       { label: 'Glas',            color: '#C4DADB' },
  elektronik: { label: 'Elektronik',      color: '#8AA58E' },
  akku:       { label: 'Akku / Chemie',   color: '#9C97B5' },
  magnet:     { label: 'Magnet / Ferrit', color: '#7F8489' },
  papier:     { label: 'Druck / Faser',   color: '#D6C3AE' },
};

