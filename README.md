# BrainPlan_LLM: Brainstorming Assistant with Web Interface

## Projektübersicht

BrainPlan_LLM ist ein fortgeschrittener, KI-gestützter Brainstorming- und Planungs-Orchestrator, der ausgefeilte Denktechniken verwendet, um vage Ideen in strukturierte Anforderungen, Aufgaben und Implementierungspläne umzuwandeln. Das Projekt kombiniert modernste Ansätze wie Tree-of-Thoughts (ToT), Graph-of-Thoughts (GoT) und Ensemble-Refinement, um umfassende Entwicklungspläne zu generieren.

## Hauptmerkmale

1. **Tree-of-Thoughts (ToT) Implementierung**: Generiert hierarchisch mehrere Lösungsansätze und bewertet sie anhand von 10 Kriterien
2. **Graph-of-Thoughts (GoT) Integration**: Erstellt einen Graphen von Lösungsansätzen, identifiziert Beziehungen (komplementär, widersprüchlich, abhängig) und synthetisiert hybride Lösungen
3. **LLM Integration**: Verbindet mit verschiedenen LLM-Anbietern (OpenAI, Anthropic, Ollama) für dynamisches Denken
4. **Funktionale Erweiterungen**: Enthält Blindspot-Erkennung, Constraint-Impact-Matrix, Premortem-Analyse und Kalibrierungsfragen
5. **Skill Framework**: Integriert in ein Agentensystem mit strukturierten Ein- und Ausgabedefinitionen
6. **Web-Oberfläche**: Benutzerfreundliche Oberfläche mit Dokumentenupload-Funktionalität

## Architektur & Komponenten

### Hauptanwendungsarchitektur
- **Frontend**: Über GitHub Pages bereitgestellte statische Webseite (HTML, CSS, JS)
- **Backend API**: Separater Service für die LLM-Verarbeitung
- **LLM-Integration**: Lokale Ollama-Instanz (kann auf demselben Backend-Server laufen)

### Dateistruktur
- `frontend/` - Statische Dateien für die GitHub Pages-Website
  - `index.html` - Hauptseite mit Eingabeformular
  - `result.html` - Ergebnisanzeige
  - `css/style.css` - Styling
  - `js/app.js` - Frontend-Logik
- `brainstorming_skill/` - Python-Implementierung des Brainstorming-Pipelines
  - `src/` - Hauptquellcode (ToT, GoT, LLM-Integration, etc.)
  - `config/` - Konfigurationsdateien
- `backend/` - Separater Backend-Service (nicht in diesem Repo enthalten)
- `.github/workflows/` - GitHub Actions für CI/CD

### Bewertungskriterien
Das System bewertet jeden Gedanken anhand von 10 Kriterien:
1. Zielerreichung (Goal achievement) - 15%
2. Machbarkeit (Feasibility) - 12%
3. Aufwand (Effort) - 12%
4. Wartbarkeit (Maintainability) - 11%
5. Risiko (Risk) - 11%
6. ROI - 10%
7. Innovation - 8%
8. Sicherheit (Security) - 8%
9. Team-Fit - 7%
10. UX - 6%

## Entwicklung & Deployment

### Lokale Entwicklung
1. Installiere die Abhängigkeiten:
```
cd brainstorming_skill
pip install -r requirements.txt
```

2. Stelle sicher, dass Ollama läuft:
```
ollama serve
```

3. Starte die Flask-Anwendung:
```
python brainstorming_ui.py
```

### GitHub Pages Deployment
Die Frontend-Oberfläche wird über GitHub Actions automatisch auf GitHub Pages veröffentlicht. Jeder Push in den `main`-Branch löst das Deployment aus.

So richten Sie das Deployment ein:
1. Fügen Sie Ihr GitHub Pages-Repository hinzu:
```
git remote add origin https://github.com/DEIN_USERNAME/DEIN_REPOSITORY.git
```

2. Der Workflow ist bereits in `.github/workflows/deploy.yml` konfiguriert

3. Aktivieren Sie GitHub Pages im Repository Settings (Branch: gh-pages)

## LLM-Integration

Das System unterstützt mehrere LLM-Anbieter:
- OpenAI (GPT Modelle)
- Anthropic (Claude Modelle)
- Ollama (lokale Modelle)

Für die Produktion empfehlen wir die Verwendung lokaler Ollama-Modelle für bessere Datenschutzkontrolle und geringere Latenz. Installieren Sie ein geeignetes Modell:
```
ollama pull llama3.2:latest
```

## Web-Oberfläche

Die Web-Oberfläche bietet:
- Einfaches Formular für Ideen und Kontext
- Dateiupload-Funktionalität für verschiedene Formate (PDF, DOCX, TXT, etc.)
- Auswahlmöglichkeit für Fokus-Bereich
- Klare Ergebnisdarstellung aller Brainstorming-Komponenten
- Responsives Design für verschiedene Bildschirmgrößen

## API-Integration

Die Frontend-Anwendung kommuniziert mit einem separaten Backend-Service über eine REST-API:

### Endpunkte
- `POST /api/brainstorm` - Führt einen Brainstorming-Vorgang durch

### Anfrageformat
```
{
  "idea": "Ihre Idee",
  "context": "Zusätzlicher Kontext",
  "focus": "allgemein",
  "round_info": "Optionale Rundeninfo"
}
```

### Antwortformat
Die Antwort enthält alle Brainstorming-Komponenten wie Anforderungen, Risiken, Tasks, etc.

## Verwendung

Das System kann verwendet werden als:
1. Web-basiertes Brainstorming-Tool (über GitHub Pages)
2. Integrierter Skill in einem größeren Agentensystem
3. Anforderungsgenerator für Softwareprojekte

## GitHub Actions & CI/CD

Dieses Projekt verwendet GitHub Actions für:
- Automatisches Deployment auf GitHub Pages
- Code-Qualitätsprüfungen
- Dokumentationsaktualisierungen

Der Workflow ist in `.github/workflows/deploy.yml` definiert und wird bei jedem Push in den `main`-Branch ausgeführt.

## Lizenzen und Referenzen

Diese Implementierung basiert auf Forschungsergebnissen zu Tree-of-Thoughts und Graph-of-Thoughts:
- Yao et al., 2024 – "Tree of Thoughts: Thorough Reasoning with Large Language Models"
- Yao et al., 2024 – "Graph of Thoughts: Solving Elaborate Problems with Large Language Models"