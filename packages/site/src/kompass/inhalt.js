// Inhalt der Seite „KI-Kompass“ (Wettbewerbskategorie „Verantwortungsvoller Umgang mit KI“).
// Nur Daten. Jede Aussage hat in `beleg` die Datei, aus der sie stammt (Pfade relativ zum Repo web-app;
// `deployment/…` liegt im Nachbar-Repo deployment). Was noch fehlt, steht ehrlich unter `offen`.
// Sprache: einfach, für 12-Jährige und eine Jury ohne Technik-Wissen.

export const KOMPASS = {
  titel: 'KI-Kompass',
  frage: 'Wie gehen wir verantwortungsvoll mit KI um?',
  einleitung: 'Die Station nutzt KI an drei Stellen: beim Erkennen, beim Steckbrief und bei Bauideen.',

  richtungen: [
    {
      id: 'transparenz',
      himmelsrichtung: 'N',
      titel: 'Transparenz',
      frage: 'Weiß ich, wann eine KI arbeitet?',
      so_machen_wirs: [
        {
          text: 'Oben auf dem Bildschirm steht immer, ob gerade eine KI arbeitet.',
          beleg: 'js/main.js',
        },
        {
          text: 'Bei jedem Ergebnis steht, ob es vom Foto-Vergleich oder von der KI kommt.',
          beleg: 'js/main.js',
        },
        {
          text: 'Steckbriefe von der KI sind als „KI-Entwurf · ungeprüft“ markiert.',
          beleg: 'docs/backend.md',
        },
        {
          text: 'Rohstoffwerte und CO₂ bekannter Gegenstände kommen nicht von der KI, sondern aus Tabellen mit Quellen.',
          beleg: 'data/rohstoffe/README.md',
        },
      ],
      offen: [
        'Wie oft die KI richtig erkennt, haben wir noch nicht genau getestet.',
        'Ob die KI unsichere Werte immer kennzeichnet, prüft noch niemand nach.',
      ],
      tipp_fuer_dich: 'Frag dich immer: Kommt das von einer KI, und woher weiß sie das?',
    },

    {
      id: 'datenschutz',
      himmelsrichtung: 'O',
      titel: 'Datenschutz',
      frage: 'Wohin gehen meine Fotos und Daten?',
      so_machen_wirs: [
        {
          text: 'Normalerweise arbeitet die KI auf dem Gerät hier, und dein Foto bleibt in der Station.',
          beleg: 'docs/backend.md',
        },
        {
          text: 'Man kann auch eine KI im Internet einschalten, dann geht das Foto an eine Firma.',
          beleg: 'backend/app/llm_claude.py',
        },
        {
          text: 'Die KI sieht nur den ausgeschnittenen Gegenstand, nicht den Tisch oder den Hintergrund.',
          beleg: 'backend/app/pipeline.py',
        },
        {
          text: 'Die KI im Internet bekommt nur Bild und Text und darf sonst nichts tun.',
          beleg: 'docs/claude-sdk.md',
        },
      ],
      offen: [
        'Die Station speichert jedes Foto, aber einen Knopf zum Löschen gibt es noch nicht.',
        'Vor dem Foto sagt dir die Station noch nicht, wohin das Bild geht.',
      ],
      tipp_fuer_dich: 'Zeig einer KI nur Fotos, auf denen nichts Privates zu sehen ist.',
    },

    {
      id: 'kontrolle',
      himmelsrichtung: 'S',
      titel: 'Der Mensch entscheidet',
      frage: 'Wer hat das letzte Wort?',
      so_machen_wirs: [
        {
          text: 'Die KI macht bis zu drei Vorschläge, und du wählst den richtigen aus.',
          beleg: 'js/main.js',
        },
        {
          text: 'Materialien darf die KI nur aus einer festen Liste auswählen.',
          beleg: 'docs/backend.md',
        },
        {
          text: 'Passt eine Antwort nicht, bekommt die KI einen zweiten Versuch, sonst kommt eine Fehlermeldung.',
          beleg: 'backend/app/pipeline.py',
        },
        {
          text: 'Die KI soll keine Bauideen mit Akkus oder Strom aus der Steckdose vorschlagen.',
          beleg: 'backend/app/pipeline.py',
        },
      ],
      offen: [
        'Ob eine Bauidee gefährlich ist, prüft kein Programm, deshalb sollte eine Lehrkraft sie ansehen.',
        'Die Werkstatt kann KI-Entwürfe noch nicht direkt in der Station freigeben.',
      ],
      tipp_fuer_dich: 'Prüf die Antwort der KI und entscheide dann selbst.',
    },

    {
      id: 'ressourcen',
      himmelsrichtung: 'W',
      titel: 'Ressourcen',
      frage: 'Brauche ich hier überhaupt eine KI?',
      so_machen_wirs: [
        {
          text: 'Die 3D-Modelle wurden einmal vorab gebaut, die KI muss sie nicht neu erzeugen.',
          beleg: 'docs/3d-modelle.md',
        },
        {
          text: 'Ein bekanntes Foto erkennt die Station ohne KI, in etwa einer Zehntelsekunde.',
          beleg: 'docs/backend.md',
        },
        {
          text: 'Die KI auf dem Gerät hier ist klein und läuft auch auf einem normalen Computer.',
          beleg: 'docs/backend.md',
        },
        {
          text: 'Bei unserer Vorführung ist die KI ganz aus, und das Wichtigste läuft trotzdem.',
          beleg: 'docs/claude-sdk.md',
        },
      ],
      offen: [
        'Wie viel Strom die KI verbraucht, haben wir noch nicht gemessen.',
        'Der CO₂-Wert zählt nur die Materialien, nicht Zusammenbau und Transport.',
      ],
      tipp_fuer_dich: 'Wenn ein Buch oder eine Lehrkraft es weiß, brauchst du keine KI.',
    },
  ],

  ablauf: [
    {
      schritt: 'Foto',
      wer: 'Mensch',
      text: 'Du machst ein Foto vom Gegenstand oder lädst ein Bild hoch.',
      beleg: 'README.md',
    },
    {
      schritt: 'Foto-Vergleich',
      wer: 'Datenbank',
      text: 'Ohne KI vergleicht die Station dein Foto mit bekannten Fotos.',
      beleg: 'backend/app/pipeline.py',
    },
    {
      schritt: 'Erkennung',
      wer: 'KI',
      text: 'Gibt es keinen Treffer, macht die KI bis zu drei Vorschläge.',
      beleg: 'backend/app/pipeline.py',
    },
    {
      schritt: 'Bestätigen',
      wer: 'Mensch',
      text: 'Du wählst den richtigen Gegenstand oder sagst „weiß ich nicht“.',
      beleg: 'js/main.js',
    },
    {
      schritt: 'Fertiger Steckbrief',
      wer: 'Datenbank',
      text: 'Für bekannte Gegenstände gibt es schon einen Steckbrief mit Quellen.',
      beleg: 'backend/app/db.py',
    },
    {
      schritt: 'Neuer Steckbrief',
      wer: 'KI',
      text: 'Für neue Gegenstände schreibt die KI einen Entwurf, markiert als ungeprüft.',
      beleg: 'docs/backend.md',
    },
    {
      schritt: 'Bauideen',
      wer: 'KI',
      text: 'Die KI schlägt drei Projekte mit Material aus dem Lager vor.',
      beleg: 'backend/app/pipeline.py',
    },
    {
      schritt: 'Du entscheidest',
      wer: 'Mensch',
      text: 'Du baust ein Projekt oder legst den Gegenstand ins Lager.',
      beleg: 'docs/backend.md',
    },
    {
      schritt: 'Freigabe',
      wer: 'Mensch',
      text: 'Die Werkstatt prüft KI-Entwürfe, aber noch nicht direkt in der Station.',
      beleg: 'backend/app/main.py',
    },
  ],

  checkliste: [
    'Brauche ich hier wirklich eine KI?',
    'Ist auf meinem Foto etwas Privates, und wohin geht es?',
    'Wie kann ich die Antwort prüfen?',
    'Könnte es gefährlich sein? Dann frage ich eine Lehrkraft.',
    'Sage ich anderen, dass ich KI benutzt habe?',
  ],

  quellen: [
    {
      titel: 'EU-Gesetz über KI (KI-Verordnung)',
      url: 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj',
    },
    {
      titel: 'EU-Gesetz zum Datenschutz (DSGVO)',
      url: 'https://eur-lex.europa.eu/eli/reg/2016/679/oj',
    },
    {
      titel: 'UNESCO: Empfehlung für einen guten Umgang mit KI (2021)',
      url: 'https://www.unesco.org/en/artificial-intelligence/recommendation-ethics',
    },
  ],
};
