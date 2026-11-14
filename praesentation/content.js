// Alle Folien als Daten, in Sprecherreihenfolge (AIDA, 5 Minuten).
// Jede Folie hat Schritte. Ein Schritt = eine Kamerastation plus die Animation, die dort läuft (world.js).
// caption: der einzige Satz auf dem Bild (leer = kein Text). notes: Sprechertext, Taste T.

// Web-App im Bildschirm. Platzhalter ist die Mock-App, bis die echte App feststeht.
// Ohne Codeänderung umstellen: ?app=https://… an die URL hängen (z. B. ?app=/ für die Stations-App im Demo-Modus).
export const APP_URL = new URLSearchParams(location.search).get('app') || './mock-app/';

// Name auf der letzten Folie (steht noch nicht fest) und Ziel des QR-Codes (assets/qr-app.svg, neu erzeugen bei Änderung)
export const PRODUKTNAME = 'ReSource Scanner';
export const SCHLUSSSATZ = 'Was man versteht, wirft man nicht weg.';
export const QR_URL = 'kontor2026.github.io/web-app';
export const QR_TEXT = 'Schau nach, was bei dir noch rumliegt.';

// Letzte Folie: „Bring … mit.“ dreht sich durch diese Gegenstände, dann erscheint der Name
export const MITBRINGEN = ['dein altes Handy', 'deinen alten Laptop', 'deine alte Powerbank', 'deine alten Kopfhörer', 'dein altes Ladekabel'];

export const slides = [
  {
    id: 'schublade', aida: 'Attention', title: 'Die Schublade',
    steps: [
      {
        id: 'start', name: 'Start', caption: '',
        notes: 'Ruhiges Startbild, Schublade zu. Hier stehen, bis es losgeht. [→ öffnet die Schublade]',
      },
      {
        id: 'schublade', name: 'Schublade', caption: '',
        notes: 'Kein Hallo, keine Vorstellung, direkt rein. Die Schublade geht auf. Jeder hat so eine: alte Handys, Ladegeräte, Kopfhörer, Powerbanks. Frage ans Publikum: Wer hat zu Hause ein altes Handy in der Schublade?',
      },
      {
        id: 'inhalt', name: 'Was drin steckt', caption: '',
        notes: 'Das ist ein ganz normales Smartphone, zerlegt in seine 16 Bauteile. Auf der Platine stecken 30 Milligramm Gold und 305 Milligramm Silber, im Akku über 6 Gramm Kobalt. Quelle: Öko-Institut.',
      },
      {
        id: 'muell', name: 'Weggeworfen', caption: 'Was drin steckt, sieht man nicht.',
        notes: 'Nur: Das sieht man von außen nicht. Und was man nicht sieht, landet im Restmüll.',
      },
    ],
  },
  {
    id: 'kreislauf', aida: 'Interest', title: 'Der Kreislauf',
    steps: [
      {
        id: 'ring', name: 'Der Weg eines Gegenstands', caption: '',
        notes: 'Jeder Gegenstand hat einen Weg: Rohstoffe werden abgebaut, verarbeitet, zu einem Produkt. Wir nutzen es, und dann landet es in der Tonne. Genau da reißt der Weg ab. Zurück zur Verwertung und zu neuen Rohstoffen kommt das Wenigste.',
      },
      {
        id: 'energie', name: 'Graue Energie', caption: 'Die Energie steckt schon drin.',
        notes: 'Und mit jedem Schritt steckt mehr drin, was man nicht sieht: graue Energie. Alles, was für Abbau, Verarbeitung und Herstellung aufgewendet wurde. Allein das Material dieses Handys: rund 1,9 kg CO₂ (Idemat 2026). In der Tonne geht all das verloren, und ein neues Gerät fängt wieder bei null an.',
      },
      {
        id: 'station', name: 'Die Station', caption: 'Wir schließen die Lücke.',
        notes: 'Genau hier setzt der ReSource Scanner an. Gegenstand drauflegen, und er zeigt, was drin steckt, was es wert ist und was man daraus bauen kann. Das Handy kommt zurück in den Kreislauf, und mit ihm die graue Energie: weiternutzen, umbauen, und erst am Ende fachgerecht recyceln.',
      },
      {
        id: 'lernen', name: 'Lernkreislauf', caption: 'Aus Müll wird Wissen.',
        notes: 'Unsere These: Erst wer hautnah erlebt, was in seinen alten Geräten steckt, lässt sie nicht mehr in der Schublade vergammeln. Darum ist der Scanner ein Lernkreislauf: entdecken, was drin steckt; verstehen, woher es kommt und was es wert ist; daraus bauen; und das Wissen weitergeben. Jeder bestätigte Scan macht den Katalog für alle besser.',
      },
    ],
  },
  {
    id: 'live', aida: 'Interest', title: 'Live',
    steps: [
      {
        id: 'monitor', name: 'Die Station', caption: '',
        notes: 'Und das zeigen wir euch jetzt live.',
      },
      {
        id: 'live', name: 'Live-Demo', caption: '', app: true,
        notes: 'Live-Demo (ca. 1:10), ein Beispiel von Anfang bis Ende: Handy-Foto, Kandidat bestätigen, Explosionszeichnung, Akku antippen, Kobalt, Herkunft, Entsorgung. Offen sagen, was simuliert ist. [X] führt heraus zu den Bauideen.',
      },
      {
        id: 'projekte', name: 'Bauideen', caption: 'Aus Altem wird Neues.',
        notes: 'Und jetzt der Teil, der Spaß macht: Der Scanner schlägt drei Projekte vor, die das alte Handy plus Material aus dem Lager der Werkstatt nutzen. [Hervorgehoben ist die Auswahl; Klick auf eine Säule ändert sie, → zeigt das gewählte Projekt.]',
      },
      {
        id: 'gewaehlt', name: 'Projekt gewählt', caption: '',
        notes: 'Wir nehmen die Musik-Box: Das Handy steckt im Deckel eines Schuhkartons, der Karton verstärkt den Klang. Der Schuhkarton kommt aus dem Lager der Werkstatt.',
      },
    ],
  },
  {
    id: 'haube', aida: 'Desire', title: 'Unter der Haube',
    steps: [
      {
        id: 'haube', name: 'So arbeitet die Station', caption: 'Die KI erkennt. Die Datenbank weiß. Der Mensch entscheidet.', messwerte: true,
        notes: 'Unter der Haube: drei Container. Das Foto geht zuerst in den Foto-Abgleich. Kennen wir den Gegenstand schon, braucht es keine KI. Sonst erkennt ein Modell nur, was es ist: die Kategorie. Alles Weitere kommt aus unserer Datenbank mit 201 Gegenständen: Bauteile, Materialien, Herkunft der Rohstoffe, Entsorgung, alles mit Quellen. Was die KI neu anlegt, bleibt ein Entwurf, bis die Werkstatt es freigibt. Unser Ziel war ein Demonstrator vom realen Material bis zum Nutzungsvorschlag: 28 von 30 Testfotos erkannt, also 93 %, und höchstens 5 Sekunden bis zum Ergebnis.',
      },
      {
        id: 'wahl', name: 'Deine Wahl', caption: 'Du entscheidest, wohin dein Foto geht.',
        notes: 'Und wo die KI läuft, entscheidet ihr. Lokal auf eurem Rechner, mit Ollama oder einem anderen offenen Modell: Dann verlässt kein Foto das Haus. Oder in der Cloud mit eurem eigenen Claude- oder OpenAI-Zugang, schneller und genauer. Wir sperren niemanden ein. Der Code ist offen.',
      },
    ],
  },
  {
    id: 'ueberall', aida: 'Action', title: 'Überall',
    steps: [
      {
        id: 'bausatz', name: 'Was man braucht', caption: 'Ein Laptop. Eine Kamera. Ein Befehl.', sub: 'ca. 100 € Hardware · unter 1 € Betrieb am Tag',
        notes: 'Was braucht eine Werkstatt dafür? Einen Laptop, eine Kamera und einen Befehl. Rund 100 Euro Hardware, unter einem Euro Betrieb am Tag. Die Container sind fertig gebaut, 201 Gegenstände sind schon drin, und es läuft auch ohne Grafikkarte.',
      },
      {
        id: 'ueberall', name: 'Jede Werkstatt', caption: 'Eine Station. Dann jede Werkstatt.', qr: true,
        notes: 'Wir fangen in Lübeck an: Pilot von Dezember bis Januar mit 10 bis 15 Schülerinnen und Schülern über die AllWeShape gGmbH, Regelbetrieb ab Februar. Danach kann jede Schulwerkstatt, jedes Repair-Café, jeder Makerspace so eine Station aufstellen. Den QR-Code oben links könnt ihr jetzt schon scannen. [Punkte auf der Karte: Großstädte als Platzhalter, siehe werkstaetten.js]',
      },
      {
        id: 'ende', name: 'Bring es mit', caption: '', finale: true, qr: true,
        notes: 'Und damit zurück zur Schublade vom Anfang: Bringt mit, was bei euch noch rumliegt. Ab Ende Februar 2027 in der Schützenstraße 62 in Lübeck. [Text dreht sich durch die Gegenstände, dann der Name.] Was man versteht, wirft man nicht weg. ReSource Scanner.',
      },
    ],
  },
];

/** Alle Schritte flach, mit Folienindex. */
export const STEPS = slides.flatMap((s, si) => s.steps.map((st, j) => ({ ...st, slide: si, inSlide: j })));
export const stepIndex = (id) => STEPS.findIndex((s) => s.id === id);
