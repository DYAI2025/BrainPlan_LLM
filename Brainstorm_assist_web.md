# Brainstorming Assistant Web Interface

## Beschreibung
Diese Web-Oberfläche ermöglicht eine einfache Interaktion mit dem Brainstorming-Skill unter Verwendung der Tree-of-Thoughts (ToT) und Graph-of-Thoughts (GoT) Algorithmen. Die Anwendung akzeptiert Ideen, optionalen Kontext und Dokumente, die als Input für den KI-gestützten Brainstorming-Prozess dienen.

## Funktionen

### Hauptfunktionen
- **Idee-Eingabe**: Haupt-Idee oder Anforderung, die brainstormed werden soll
- **Kontext-Eingabe**: Zusätzlicher Kontext wie bestehende Systeme, Technologie-Stack, Einschränkungen
- **Fokus-Auswahl**: Auswahl eines spezifischen Bereichs (Allgemein, Architektur, Tests, Datenmodell, Planung)
- **Dokumenten-Upload**: Unterstützung für verschiedene Dateiformate (TXT, PDF, DOCX, MD, CSV, JSON) zum Einbeziehen in den Kontext

### Ergebnisvisualisierung
- Strukturierte Darstellung aller Brainstorming-Komponenten:
  - Problem Statement
  - Ziele & KPIs
  - Funktionale und nicht-funktionale Anforderungen
  - Risiken & Annahmen
  - Umsetzungspotenzial
  - Task-Liste
  - Test-Ideen
  - Prompts für nachgelagerte Skills

## Installation

### Voraussetzungen
- Python 3.8+
- Ollama
- Ein installiertes Ollama-Modell (z.B. `llama3.2:latest`)

### Setup-Schritte
1. Stelle sicher, dass Ollama läuft:
   ```bash
   ollama serve
   ```

2. Klone oder lade das Projekt herunter

3. Erstelle eine virtuelle Umgebung:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # oder myenv\Scripts\activate auf Windows
   ```

4. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

5. Starte die Web-Oberfläche:
   ```bash
   python3 brainstorming_ui.py
   ```

## Verwendung

### Starten der Anwendung
1. Stelle sicher, dass Ollama läuft
2. Aktiviere deine virtuelle Umgebung
3. Führe `python3 brainstorming_ui.py` aus
4. Öffne http://localhost:5000 in deinem Browser

### Interaktion mit der Oberfläche
1. **Idee eingeben**: Beschreibe deine Haupt-Idee oder das zu lösende Problem
2. **Kontext hinzufügen**: Optional zusätzlicher Kontext wie bestehende Systeme, Einschränkungen, Stakeholder-Anforderungen
3. **Fokus-Bereich wählen**: Wähle einen spezifischen Bereich (z.B. Architektur, Tests)
4. **Dokumente hochladen**: Lade relevante Dokumente hoch, die als zusätzlicher Kontext verwendet werden sollen
5. **"Brainstorming durchführen" klicken**: Startet den Prozess mit der KI

### Unterstützte Dateiformate
- **Textdateien** (`.txt`): Einfacher Textinhalt
- **PDF-Dokumente** (`.pdf`): Strukturierte Dokumente mit Textextraktion
- **Word-Dokumente** (`.docx`): Text aus Microsoft Word-Dokumenten
- **Markdown-Dateien** (`.md`): Formatierter Text
- **CSV-Dateien** (`.csv`): Strukturierte Tabellen-Daten
- **JSON-Dateien** (`.json`): Strukturierte Datensätze

## Architektur

### Technologien
- **Backend**: Flask-Web-Framework
- **KI-Integration**: Ollama API
- **Frontend**: HTML/CSS/JavaScript
- **Brainstorming-Engine**: Tree-of-Thoughts und Graph-of-Thoughts Algorithmen

### Dateistruktur
```
brainstorming_ui.py          # Haupt-Flask-Anwendung
templates/
├── index.html              # Hauptseite mit Eingabeformular
└── result.html             # Ergebnisanzeige
```

## Konfiguration

### Umgebungsvariablen
Erstelle eine `.env`-Datei in `/brainstorming_skill/.env` mit:
```
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2:latest
OLLAMA_URL=http://localhost:11434
```

## API

Die Web-Oberfläche bietet auch einen API-Endpunkt für direkte Integration:
- **POST** `/api/brainstorm`
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "idea": "Deine Idee hier",
    "context": "Optionaler Kontext",
    "focus": "allgemein",
    "round_info": "Optionale Rundeninfo"
  }
  ```

## Fehlerbehebung

### Häufige Probleme
- **"Ollama server not accessible"**: Stelle sicher, dass `ollama serve` läuft
- **"Model not found"**: Überprüfe, ob das in der Konfiguration genannte Modell installiert ist
- **"File upload failed"**: Überprüfe die Dateierweiterung und die maximale Dateigröße

### Logs
Überprüfe die Terminal-Ausgabe für detaillierte Fehlerinformationen.

## Lizenz
Diese Software basiert auf Brainstorming- und Reasoning-Algorithmen (Tree-of-Thoughts, Graph-of-Thoughts) und ist für Forschungs- und Entwicklungsziele gedacht.