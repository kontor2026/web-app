// Inhalt der Seite „KI-Kompass“ (Wettbewerbskategorie „Verantwortungsvoller Umgang mit KI“).
// Nur Daten. Jede Aussage hat in `beleg` die Datei, aus der sie stammt (Pfade relativ zum Repo web-app;
// `deployment/…` liegt im Nachbar-Repo deployment). Was noch fehlt, steht ehrlich unter `offen`.

export const KOMPASS = {
  titel: 'KI-Kompass',
  frage: 'Wie gehen wir verantwortungsvoll mit KI um?',
  einleitung:
    'Die Kreislauf-Station nutzt KI an drei Stellen: zum Erkennen des Gegenstands, für einen Entwurf des Material-Steckbriefs und für Bauideen. ' +
    'Hier zeigen wir, wo die KI arbeitet, wer am Ende entscheidet und was wir noch nicht gelöst haben.',

  richtungen: [
    {
      id: 'transparenz',
      himmelsrichtung: 'N',
      titel: 'Transparenz',
      frage: 'Weiß ich, wann eine KI arbeitet?',
      so_machen_wirs: [
        {
          text: 'In der Kopfzeile steht immer, welche KI gerade läuft, zum Beispiel „KI lokal · station-vl“. Ist die KI abgeschaltet, steht dort „KI aus (Mock)“.',
          beleg: 'js/main.js',
        },
        {
          text: 'Beim Ergebnis steht, woher es kommt: aus dem Foto-Abgleich mit bekannten Gegenständen oder von der KI.',
          beleg: 'js/main.js',
        },
        {
          text: 'Steckbriefe von der KI tragen den Status „Entwurf“. In der App steht dann „KI-Entwurf · ungeprüft“.',
          beleg: 'docs/backend.md',
        },
        {
          text: 'Im Entwurf steht auch, welches Modell ihn geschrieben hat und dass die Werte Schätzungen sind.',
          beleg: 'backend/app/pipeline.py',
        },
        {
          text: 'Die KI soll Schätzungen mit „≈“ kennzeichnen und sagen, wenn sie etwas nicht sicher weiß. Das steht in der Anweisung an die KI (dem „Prompt“).',
          beleg: 'backend/app/pipeline.py',
        },
        {
          text: 'Die Prozentzahl bei der Erkennung ist eine Selbsteinschätzung der KI. Das sagt die App auch so: „Bitte prüfen.“',
          beleg: 'backend/app/pipeline.py',
        },
        {
          text: 'Rohstoffwert und CO₂ der vorgebauten Kategorien kommen nicht von der KI, sondern aus einer eigenen Datenbank mit Quellen. Jeder Wert nennt seine Herkunft.',
          beleg: 'data/rohstoffe/README.md',
        },
      ],
      offen: [
        'Die Selbsteinschätzung der KI (z. B. „87 %“) ist keine gemessene Trefferquote. Wie oft die Erkennung wirklich stimmt, haben wir noch nicht systematisch getestet.',
        'Die Hinweise zu „≈“ und „nicht sicher“ stehen nur in der Anweisung an die KI. Ob sie sich immer daran hält, prüft kein Programm.',
        'Die Rohstoffdaten für Elektronik stammen aus einer Studie von 2012. Neuere Geräte enthalten oft weniger Gold und Silber.',
        'Palladium, Kobalt und Platin haben noch keinen Preis und fehlen im Rohstoffwert.',
      ],
      tipp_fuer_dich: 'Frag bei jeder Antwort: Kommt das von einer KI, und woher hat sie das?',
    },

    {
      id: 'datenschutz',
      himmelsrichtung: 'O',
      titel: 'Datenschutz',
      frage: 'Wohin gehen meine Fotos und Daten?',
      so_machen_wirs: [
        {
          text: 'Standard ist eine lokale KI: Das Modell Qwen3-VL läuft in einem eigenen Container auf der Station. Das Foto verlässt dann nicht die Station.',
          beleg: 'docs/backend.md',
        },
        {
          text: 'Wer will, kann auf Claude umschalten. Dann geht das Bild über das Internet an die Firma Anthropic. Das ist eine Cloud-KI, also eine KI auf fremden Servern.',
          beleg: 'backend/app/llm_claude.py',
        },
        {
          text: 'Vor der Erkennung schneidet die Station den Gegenstand aus. Die KI sieht dann nur den Gegenstand, nicht Tisch oder Hintergrund.',
          beleg: 'backend/app/pipeline.py',
        },
        {
          text: 'Das Bild für die KI wird auf höchstens 896 Pixel verkleinert.',
          beleg: 'backend/app/config.py',
        },
        {
          text: 'Zugangsschlüssel für Claude gehören nicht in den Code. Die App liest sie aus einer geschützten Datei oder einer Umgebungsvariable.',
          beleg: 'backend/app/config.py',
        },
        {
          text: 'Beim Claude-Abo bekommt Claude nur Bild, Text und eine Vorgabe für die Antwort. Alle Werkzeuge wie Dateien, Shell und Web sind abgeschaltet.',
          beleg: 'docs/claude-sdk.md',
        },
      ],
      offen: [
        'Die Station speichert jedes Scan-Foto auf dem eigenen Speicher (Ordner „scans“). Eine Löschfrist oder einen Knopf „Foto löschen“ gibt es noch nicht.',
        'Es gibt noch keinen Hinweis vor dem Foto, der erklärt, wo das Bild landet. Das wäre besonders wichtig, wenn Claude eingeschaltet ist.',
        'Personen oder Namen auf dem Foto erkennt die Station nicht gezielt. Der Ausschnitt um den Gegenstand hilft, ist aber kein Schutz.',
        'Die Docker-Anleitung empfiehlt geheime Dateien für Schlüssel. Die Deployment-Datei übergibt Schlüssel aber noch als Umgebungsvariable.',
      ],
      tipp_fuer_dich: 'Bevor du ein Foto in eine KI lädst: Ist darauf etwas, das niemand anderes sehen soll?',
    },

    {
      id: 'kontrolle',
      himmelsrichtung: 'S',
      titel: 'Der Mensch entscheidet',
      frage: 'Wer hat das letzte Wort?',
      so_machen_wirs: [
        {
          text: 'Die KI nennt bis zu drei mögliche Gegenstände. Du wählst den richtigen aus oder klickst „Anderes Modell / weiß ich nicht“.',
          beleg: 'js/main.js',
        },
        {
          text: 'Exakte Modelle (z. B. welches Smartphone genau) sind aus einem Foto unsicher. Deshalb gibt es eine Liste zum Bestätigen statt einer festen Antwort.',
          beleg: 'docs/machbarkeit.md',
        },
        {
          text: 'Die Antwort der KI muss in ein festes Formular passen (ein „Schema“). Materialien und Lagerartikel darf sie nur aus einer festen Liste wählen.',
          beleg: 'docs/backend.md',
        },
        {
          text: 'Das Programm prüft die Antwort. Bei Fehlern bekommt die KI eine zweite Chance mit Hinweisen. Scheitert auch die, gibt es eine Fehlermeldung statt einer erfundenen Antwort.',
          beleg: 'backend/app/pipeline.py',
        },
        {
          text: 'Die KI beschreibt nur Bauteile und grobe Anteile. Die Zeichnung rechnet das Programm selbst.',
          beleg: 'docs/backend.md',
        },
        {
          text: 'Die Werkstatt kann einen KI-Entwurf freigeben oder verwerfen. Geprüfte Gegenstände können nicht mehr aus Versehen gelöscht werden.',
          beleg: 'backend/app/main.py',
        },
        {
          text: 'Für Bauideen gilt: keine Projekte, bei denen Akkus geöffnet werden oder an Netzspannung gearbeitet wird.',
          beleg: 'backend/app/pipeline.py',
        },
      ],
      offen: [
        'Freigeben und Verwerfen gehen bisher nur über die Schnittstelle des Backends. In der App gibt es dafür noch keine Ansicht für die Werkstatt.',
        'Die Sicherheitsregeln für Bauideen stehen nur in der Anweisung an die KI. Das Programm prüft nicht nach, ob eine Idee gefährlich ist. Eine Lehrkraft sollte jede neue Idee ansehen.',
        'Die Bauideen werden nicht automatisch als Entwurf markiert wie der Steckbrief.',
      ],
      tipp_fuer_dich: 'Nimm die erste Antwort der KI nicht einfach hin: Prüf sie und entscheide selbst.',
    },

    {
      id: 'ressourcen',
      himmelsrichtung: 'W',
      titel: 'Ressourcen',
      frage: 'Brauche ich hier überhaupt eine KI?',
      so_machen_wirs: [
        {
          text: 'Für 201 Gegenstands-Kategorien gibt es 3D-Modelle, die einmal vorab gebaut wurden. Zur Laufzeit werden sie nur geladen, die KI erzeugt dafür nichts.',
          beleg: 'docs/3d-modelle.md',
        },
        {
          text: 'Ein schon bekanntes Foto erkennt die Station ohne KI über einen Foto-Abgleich, in etwa 0,1 Sekunden.',
          beleg: 'docs/backend.md',
        },
        {
          text: 'Bestätigte Steckbriefe werden gespeichert. Der nächste Scan desselben Gegenstands braucht keine KI.',
          beleg: 'docs/backend.md',
        },
        {
          text: 'Die lokale KI ist ein kleines Modell mit 4 Milliarden Parametern (Qwen3-VL 4B). Es läuft auch ohne Grafikkarte.',
          beleg: 'docs/backend.md',
        },
        {
          text: 'Das „Nachdenken“ der lokalen KI ist abgeschaltet. Auf dem Prozessor ist sie so 5- bis 10-mal schneller.',
          beleg: 'backend/app/config.py',
        },
        {
          text: 'Mit Claude denkt die KI je Schritt nur so viel wie nötig: wenig bei Erkennung und Bauideen, mittel beim Steckbrief.',
          beleg: 'backend/app/llm_claude.py',
        },
        {
          text: 'Die KI lässt sich ganz abschalten. Kategorien, Steckbriefe, Rohstoffwerte und Foto-Abgleich laufen dann weiter. Für unsere Präsentation ist sie abgeschaltet.',
          beleg: 'docs/claude-sdk.md',
        },
      ],
      offen: [
        'Den Stromverbrauch der KI haben wir nicht gemessen. Wir kennen nur Rechenzeiten und grob geschätzte Kosten pro Gegenstand.',
        'Auf einem Laptop ohne Grafikkarte brauchen neue Steckbriefe und Bauideen mehrere Minuten.',
        'Der CO₂-Wert im Steckbrief zählt nur die Materialien, nicht Montage, Chips und Transport.',
        'Mit Claude rechnet die Station Steckbrief und Bauideen schon beim Hochladen voraus. Das spart Wartezeit, kostet aber Rechenleistung, wenn du danach einen anderen Gegenstand wählst.',
      ],
      tipp_fuer_dich: 'Wenn eine Tabelle, ein Buch oder eine Lehrkraft die Antwort schon kennt, brauchst du keine KI.',
    },
  ],

  ablauf: [
    {
      schritt: 'Foto',
      wer: 'Mensch',
      text: 'Du legst den Gegenstand auf die Station und machst ein Foto, lädst ein Bild hoch oder nimmst ein Beispielfoto.',
      beleg: 'README.md',
    },
    {
      schritt: 'Foto-Abgleich',
      wer: 'Datenbank',
      text: 'Ohne KI: Das Programm prüft Helligkeit und Schärfe, schneidet den Gegenstand aus und vergleicht das Foto mit bekannten Fotos. Gibt es einen Treffer, ist die Erkennung schon fertig.',
      beleg: 'backend/app/pipeline.py',
    },
    {
      schritt: 'Erkennung',
      wer: 'KI',
      text: 'Sonst schaut die KI auf das Bild. Sie nennt bis zu drei mögliche Gegenstände mit ihrer geschätzten Sicherheit, gelesenen Text und vermutete Materialien.',
      beleg: 'backend/app/pipeline.py',
    },
    {
      schritt: 'Bestätigen',
      wer: 'Mensch',
      text: 'Du wählst den passenden Gegenstand aus der Liste oder sagst „weiß ich nicht“.',
      beleg: 'js/main.js',
    },
    {
      schritt: 'Steckbrief aus dem Speicher',
      wer: 'Datenbank',
      text: 'Ist der Gegenstand bekannt, kommt der Steckbrief mit 3D-Modell aus dem Speicher. Rohstoffwerte und CO₂ der Kategorien stammen aus der Rohstoff-Datenbank mit Quellen.',
      beleg: 'backend/app/db.py',
    },
    {
      schritt: 'Steckbrief-Entwurf',
      wer: 'KI',
      text: 'Ist er neu, schreibt die KI einen Entwurf: Bauteile, Materialien, Entsorgung. Das Programm prüft ihn und zeichnet daraus die Explosionszeichnung. Er ist als „KI-Entwurf · ungeprüft“ markiert.',
      beleg: 'docs/backend.md',
    },
    {
      schritt: 'Bauideen',
      wer: 'KI',
      text: 'Die KI schlägt drei Projekte vor. Sie darf nur Material nehmen, das wirklich im Lager liegt, höchstens 10 Stück je Artikel.',
      beleg: 'backend/app/pipeline.py',
    },
    {
      schritt: 'Bauen oder einlagern',
      wer: 'Mensch',
      text: 'Du entscheidest, ob du ein Projekt startest oder den Gegenstand einlagerst. Reicht der Bestand nicht, bricht die Station ab.',
      beleg: 'docs/backend.md',
    },
    {
      schritt: 'Freigabe',
      wer: 'Mensch',
      text: 'Die Werkstatt prüft KI-Entwürfe und gibt sie frei oder verwirft sie. Bisher nur über die Schnittstelle, noch nicht in der App.',
      beleg: 'backend/app/main.py',
    },
  ],

  checkliste: [
    'Brauche ich hier wirklich eine KI, oder finde ich die Antwort auch ohne?',
    'Was gebe ich der KI: Ist auf dem Foto oder im Text etwas Privates?',
    'Läuft die KI bei mir vor Ort oder schicke ich meine Daten an eine Firma?',
    'Woran erkenne ich, welcher Teil der Antwort von der KI stammt?',
    'Wie kann ich die Antwort prüfen: mit einer Quelle, einem Messwert oder einer Person, die sich auskennt?',
    'Könnte die Antwort gefährlich sein, zum Beispiel bei Akkus oder Strom? Dann frage ich eine Lehrkraft.',
    'Sage ich anderen, dass ich KI benutzt habe?',
  ],

  quellen: [
    {
      titel: 'EU-Verordnung über künstliche Intelligenz (KI-Verordnung, Verordnung (EU) 2024/1689)',
      url: 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj',
    },
    {
      titel: 'Datenschutz-Grundverordnung (DSGVO, Verordnung (EU) 2016/679)',
      url: 'https://eur-lex.europa.eu/eli/reg/2016/679/oj',
    },
    {
      titel: 'UNESCO: Empfehlung zur Ethik der künstlichen Intelligenz (2021)',
      url: 'https://www.unesco.org/en/artificial-intelligence/recommendation-ethics',
    },
  ],
};
