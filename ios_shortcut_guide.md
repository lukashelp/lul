# iOS Shortcut: Dateien nach Typ sortieren

Öffne die **Kurzbefehle**-App auf dem iPhone/iPad und erstelle einen neuen Kurzbefehl.

---

## Schritt 1 — Dateien holen

**Aktion:** `Dateien abrufen`
- Ordner: `iCloud Drive/Downloads` (oder gewünschter Ordner)
- Unterordner einbeziehen: **Aus**
- Fehler anzeigen: **Ein**

---

## Schritt 2 — Über jede Datei iterieren

**Aktion:** `Jedes Element wiederholen`
- Eingabe: Ergebnis aus Schritt 1

---

## Schritt 3 — Dateiendung ermitteln

**Aktion:** `Details der Datei abrufen`
- Datei: `Wiederholungselement`
- Detail: **Dateiendung**

→ Ergebnis als Variable speichern: `Endung`

---

## Schritt 4 — Kategorie bestimmen (Wenn/Sonst)

Füge folgende **Wenn**-Blöcke nacheinander ein:

### Block A — Bilder
```
Wenn  Endung  enthält einen Wert in der Liste
  jpg, jpeg, png, gif, bmp, webp, svg, heic, tiff, raw
→ Text: "Bilder"
```

### Block B — Videos
```
Sonst wenn  Endung  enthält einen Wert in der Liste
  mp4, mkv, avi, mov, wmv, flv, m4v
→ Text: "Videos"
```

### Block C — Audio
```
Sonst wenn  Endung  enthält einen Wert in der Liste
  mp3, wav, flac, aac, ogg, m4a, opus
→ Text: "Audio"
```

### Block D — Dokumente
```
Sonst wenn  Endung  enthält einen Wert in der Liste
  pdf, doc, docx, xls, xlsx, ppt, pptx, txt, md, rtf
→ Text: "Dokumente"
```

### Block E — Archive
```
Sonst wenn  Endung  enthält einen Wert in der Liste
  zip, tar, gz, rar, 7z, dmg, ipa
→ Text: "Archive"
```

### Sonst (Fallback)
```
→ Text: "Sonstiges"
```

→ Variable speichern: `Kategorie`

---

## Schritt 5 — Zielordner anlegen (falls nicht vorhanden)

**Aktion:** `Ordner abrufen`
- Pfad: `iCloud Drive/Downloads/` + Variable `Kategorie`
- Fehler, wenn nicht vorhanden: **Aus**

Falls nicht vorhanden:

**Aktion:** `Ordner erstellen`
- Pfad: `iCloud Drive/Downloads/` + Variable `Kategorie`

---

## Schritt 6 — Datei verschieben

**Aktion:** `Datei verschieben`
- Datei: `Wiederholungselement`
- Ziel: Ergebnis aus Schritt 5 (der Ordner)
- Überschreiben: **Aus**

---

## Ergebnis-Ordnerstruktur

```
iCloud Drive/Downloads/
├── Bilder/
├── Videos/
├── Audio/
├── Dokumente/
├── Archive/
└── Sonstiges/
```

---

## Tipps

- **Zum Startbildschirm hinzufügen:** Kurzbefehl-Details → Symbol → „Zum Home-Bildschirm"
- **Automatisch ausführen:** In der Kurzbefehle-App unter „Automation" einen Auslöser einrichten (z.B. täglich um 8 Uhr)
- **Andere Ordner:** In Schritt 1 einfach einen anderen Startordner wählen (z.B. „Auf meinem iPhone")
