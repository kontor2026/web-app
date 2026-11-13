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

// elements: [Symbol, Anteil in % des Materials]
export const MATERIALS = {
  alu:        { name: 'Aluminium', cls: 'metall', elements: [['Al', 97], ['Mg', 1], ['Si', 1]], recycling: 'hoch',
                text: 'Leicht und gut formbar. Recyceltes Aluminium braucht nur etwa 5 % der Energie von Primäraluminium.' },
  stahl:      { name: 'Edelstahl', cls: 'metall', elements: [['Fe', 70], ['Cr', 18], ['Ni', 10]], recycling: 'hoch',
                text: 'Robust und magnetisch je nach Sorte. Wird über Schrottplätze fast vollständig zurückgewonnen.' },
  kupfer:     { name: 'Kupfer', cls: 'metall', elements: [['Cu', 99]], recycling: 'hoch',
                text: 'Leitet Strom und Wärme sehr gut. Steckt in Leiterbahnen, Spulen und Kabeln.' },
  lot:        { name: 'Lötzinn (bleifrei)', cls: 'metall', elements: [['Sn', 96], ['Ag', 3], ['Cu', 1]], recycling: 'mittel',
                text: 'Verbindet Bauteile mit der Platine. Seit 2006 in der EU weitgehend bleifrei.' },
  kontakte:   { name: 'Vergoldete Kontakte', cls: 'metall', elements: [['Cu', 90], ['Ni', 8], ['Au', 2]], recycling: 'mittel',
                text: 'Eine hauchdünne Goldschicht schützt Steckkontakte vor Korrosion.' },
};

