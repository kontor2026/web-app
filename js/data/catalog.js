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
  glas:       { name: 'Alumosilikatglas', cls: 'glas', elements: [['Si', 30], ['O', 50], ['Al', 10], ['K', 5]], recycling: 'gering',
                text: 'Chemisch gehärtetes Spezialglas. Kratzfest, aber wegen Beschichtungen kaum recycelbar.' },
  displayglas:{ name: 'Displayglas mit ITO', cls: 'glas', elements: [['Si', 30], ['O', 55], ['In', 0.1]], recycling: 'gering',
                text: 'Trägerglas mit einer leitfähigen Schicht aus Indiumzinnoxid. Indium ist selten.' },
  folien:     { name: 'Polymer-Folien', cls: 'kunststoff', elements: [['C', 70], ['H', 6], ['O', 24]], recycling: 'gering',
                text: 'Polarisations- und Lichtleiterfolien. Mehrlagig verklebt, daher schwer zu trennen.' },
  led:        { name: 'LED-Hintergrundlicht', cls: 'elektronik', elements: [['Ga', 40], ['In', 5], ['Y', 2]], recycling: 'gering',
                text: 'Leuchtdioden aus Galliumverbindungen. Gelbe Leuchtstoffe enthalten Seltene Erden.' },
  fr4:        { name: 'Leiterplatte (FR-4)', cls: 'elektronik', elements: [['C', 30], ['Si', 25], ['O', 30], ['Br', 5]], recycling: 'mittel',
                text: 'Glasfasergewebe mit Epoxidharz. Trägt die Leiterbahnen aus Kupfer.' },
  chip:       { name: 'Halbleiter-Chip', cls: 'elektronik', elements: [['Si', 40], ['Cu', 20], ['Au', 1], ['Ta', 1]], recycling: 'mittel',
                text: 'Siliziumkristall im Kunststoffgehäuse. Der Wert liegt in Gold, Kupfer und Tantal.' },
  lco:        { name: 'Lithium-Kobalt-Oxid', cls: 'akku', elements: [['Co', 60], ['Li', 7], ['O', 33]], recycling: 'mittel',
                text: 'Kathodenmaterial im Akku. Kobalt ist der teuerste und kritischste Bestandteil.' },
  nmc:        { name: 'NMC-Kathode', cls: 'akku', elements: [['Ni', 35], ['Mn', 12], ['Co', 12], ['Li', 7]], recycling: 'mittel',
                text: 'Nickel-Mangan-Kobalt-Mischung. Üblich in Laptop-Akkus.' },
  graphit:    { name: 'Graphit', cls: 'akku', elements: [['C', 100]], recycling: 'gering',
                text: 'Anodenmaterial im Akku. Speichert Lithium-Ionen beim Laden.' },
  elektrolyt: { name: 'Elektrolyt', cls: 'akku', elements: [['C', 40], ['Li', 2], ['F', 10]], recycling: 'gering',
                text: 'Brennbare Flüssigkeit mit Lithiumsalz. Grund, warum beschädigte Akkus brennen können.' },
  ndfeb:      { name: 'Neodym-Magnet', cls: 'magnet', elements: [['Nd', 30], ['Fe', 66], ['B', 1]], recycling: 'gering',
                text: 'Sehr starke Dauermagnete für Lautsprecher, Vibration und Kamera-Autofokus.' },
  ferrit:     { name: 'Ferrit', cls: 'magnet', elements: [['Fe', 70], ['Mn', 10], ['Zn', 8]], recycling: 'gering',
                text: 'Keramischer Magnetwerkstoff. Bündelt das Magnetfeld in Trafos und Ladespulen.' },
};

