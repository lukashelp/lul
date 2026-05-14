# iOS Shortcut: Dateien nach Typ sortieren

Öffne die **Kurzbefehle**-App → neuer Kurzbefehl → Aktionen hinzufügen.

---

## Schritt 1 — Dateien aus Ordner laden

**Aktion:** `Ordnerinhalt laden`
- Ordner: `iCloud Drive/Downloads` (oder gewünschter Ordner)
- Unterordner einbeziehen: **Aus**

---

## Schritt 2 — Über jede Datei iterieren

**Aktion:** `Jedes Element wiederholen`
- Eingabe: Ergebnis aus Schritt 1

---

## Schritt 3 — Dateiendung ermitteln

**Aktion:** `Details der Datei abrufen`  
*(Suchbegriff: „Details" → Kategorie „Dokumente")*
- Datei: `Wiederholungselement`
- Detail: **Erweiterung**

→ Ergebnis als Variable speichern: `Endung`

---

## Schritt 4 — Kategorie bestimmen (Wenn/Sonst)

Füge folgende **Wenn**-Blöcke nacheinander ein:

### Bilder
```
Wenn  Endung  enthält einen Wert in der Liste
  jpg, jpeg, png, gif, bmp, webp, svg, heic, tiff, raw
→ Text: "Bilder"
```

### Videos
```
Sonst wenn  Endung  enthält einen Wert in der Liste
  mp4, mkv, avi, mov, wmv, flv, m4v
→ Text: "Videos"
```

### Audio
```
Sonst wenn  Endung  enthält einen Wert in der Liste
  mp3, wav, flac, aac, ogg, m4a, opus
→ Text: "Audio"
```

### Dokumente
```
Sonst wenn  Endung  enthält einen Wert in der Liste
  pdf, doc, docx, xls, xlsx, ppt, pptx, txt, md, rtf
→ Text: "Dokumente"
```

### Archive
```
Sonst wenn  Endung  enthält einen Wert in der Liste
  zip, tar, gz, rar, 7z, dmg, ipa
→ Text: "Archive"
```

### Fallback
```
Sonst
→ Text: "Sonstiges"
```

→ Variable speichern: `Kategorie`

---

## Schritt 5 — Zielordner erstellen (falls nicht vorhanden)

**Aktion:** `Ordner erstellen`
- Pfad: `iCloud Drive/Downloads/` + Variable `Kategorie`
- *(Ordner erstellen ist idempotent — existiert er bereits, passiert nichts)*

---

## Schritt 6 — Datei verschieben

**Aktion:** `Datei bewegen`
- Datei: `Wiederholungselement`
- Ziel: Ergebnis aus Schritt 5
- Bei Konflikt: **Umbenennen**

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

- **Zum Home-Bildschirm:** Kurzbefehl-Details → Symbol → „Zum Home-Bildschirm hinzufügen"
- **Automatisch täglich:** Kurzbefehle → Automation → Neu → Tageszeit wählen → diesen Kurzbefehl auswählen
- **Anderen Ordner sortieren:** In Schritt 1 Ordner ändern, z.B. „Auf meinem iPhone/Downloads"
