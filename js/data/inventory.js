// Lagerbestand der Werkstatt (Mock). fach = Lagerplatz-Code auf dem Etikett.
export const INVENTORY = [
  { id: 'hdpe-deckel', name: 'HDPE-Deckel, sortiert', fach: 'A-01', menge: 412, einheit: 'Stk', cls: 'kunststoff' },
  { id: 'hdpe-platte', name: 'HDPE-Platte, gepresst', fach: 'A-03', menge: 9, einheit: 'Stk', cls: 'kunststoff' },
  { id: 'pp-granulat', name: 'PP-Granulat', fach: 'A-04', menge: 2.4, einheit: 'kg', cls: 'kunststoff' },
  { id: 'holzleiste', name: 'Holzleiste Kiefer, 1 m', fach: 'B-02', menge: 18, einheit: 'Stk', cls: 'papier' },
  { id: 'rundstab', name: 'Rundstab Buche, 8 mm', fach: 'B-03', menge: 25, einheit: 'Stk', cls: 'papier' },
  { id: 'holzscheibe', name: 'Baumscheibe', fach: 'B-05', menge: 6, einheit: 'Stk', cls: 'papier' },
  { id: 'usb-kabel', name: 'USB-Kabel, geprüft', fach: 'C-01', menge: 31, einheit: 'Stk', cls: 'elektronik' },
  { id: 'led-streifen', name: 'LED-Streifen 5 V', fach: 'C-02', menge: 6, einheit: 'Stk', cls: 'elektronik' },
  { id: 'controller', name: 'Display-Controller (Spende)', fach: 'C-04', menge: 2, einheit: 'Stk', cls: 'elektronik' },
  { id: 'magnete', name: 'Neodym-Magnete', fach: 'C-06', menge: 40, einheit: 'Stk', cls: 'magnet' },
  { id: 'uhrwerk', name: 'Quarz-Uhrwerk', fach: 'C-07', menge: 3, einheit: 'Stk', cls: 'metall' },
  { id: 'draht', name: 'Bindedraht, verzinkt', fach: 'D-01', menge: 1, einheit: 'Rolle', cls: 'metall' },
  { id: 'schrauben', name: 'Schrauben-Mix aus Altgeräten', fach: 'D-02', menge: 1.1, einheit: 'kg', cls: 'metall' },
  { id: 'platinen', name: 'Leiterplatten, ausgeschlachtet', fach: 'D-04', menge: 12, einheit: 'Stk', cls: 'elektronik' },
];

export const byId = (id) => INVENTORY.find((i) => i.id === id);
