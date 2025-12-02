# BrainPlan_LLM: KI-gestützter Brainstorming Assistant

## Projektübersicht

BrainPlan_LLM ist ein fortgeschrittener, KI-gestützter Brainstorming- und Planungs-Orchestrator, der ausgefeilte Denktechniken verwendet, um vage Ideen in strukturierte Anforderungen, Aufgaben und Implementierungspläne umzuwandeln. Das Projekt kombiniert modernste Ansätze wie Tree-of-Thoughts (ToT), Graph-of-Thoughts (GoT) und Ensemble-Refinement, um umfassende Entwicklungspläne zu generieren.

## Hauptmerkmale

### KI-Algorithmen
1. **Tree-of-Thoughts (ToT)**: Generiert hierarchisch mehrere Lösungsansätze und bewertet sie anhand von 10 gewichteten Kriterien
2. **Graph-of-Thoughts (GoT)**: Erstellt einen Graphen von Lösungsansätzen, identifiziert Beziehungen (komplementär, widersprüchlich, abhängig) und synthetisiert hybride Lösungen
3. **Ensemble-Refinement**: Kombiniert mehrere Perspektiven für robuste Anforderungsanalyse

### Technische Features
4. **Flexible LLM-Integration**: Unterstützt OpenAI, Anthropic und Ollama (lokale Modelle)
5. **Erweiterte Funktionen**: Blindspot-Erkennung, Constraint-Impact-Matrix, Premortem-Analyse, Kalibrierungsfragen
6. **Skill Framework**: Vollständig integrierbar in Agentensysteme mit strukturierten Ein-/Ausgabedefinitionen
7. **Web-Interface**: Benutzerfreundliche Oberfläche mit Dokumentenupload und Mock-Daten-Unterstützung

## Systemarchitektur

### Hybrid-Architektur (Frontend + Backend)

```
┌─────────────────────┐      HTTP/REST API      ┌──────────────────────┐
│  Frontend (Static)  │ ◄──────────────────────► │  Backend (Flask)     │
│  - HTML/CSS/JS      │                          │  - brainstorming_ui  │
│  - GitHub Pages     │                          │  - Skill Execution   │
│  - Mock-Daten       │                          └──────────┬───────────┘
└─────────────────────┘                                     │
                                                            │
                                                            ▼
                                                  ┌──────────────────────┐
                                                  │  Brainstorming Skill │
                                                  │  - ToT/GoT Engine    │
                                                  │  - LLM Integration   │
                                                  └──────────┬───────────┘
                                                            │
                                                            ▼
                                                  ┌──────────────────────┐
                                                  │  LLM Provider        │
                                                  │  - Ollama (lokal)    │
                                                  │  - OpenAI/Anthropic  │
                                                  └──────────────────────┘
```

### Deployment-Modi

**Modus 1: Demo (GitHub Pages mit Mock-Daten)**
- Frontend wird auf GitHub Pages gehostet
- Verwendet Mock-Daten (keine Backend-Verbindung erforderlich)
- Perfekt für Präsentationen und UI-Demos

**Modus 2: Vollständig (Frontend + Backend)**
- Frontend auf GitHub Pages
- Backend auf Server (z.B. Railway, Heroku, eigener Server)
- Vollständige LLM-Integration mit echten Ergebnissen

**Modus 3: Lokal**
- Flask-App (`brainstorming_ui.py`) lokal ausführen
- Integriert Frontend und Backend in einem Server
- Beste Option für Entwicklung und Tests

### Komponenten-Details

#### Frontend (`frontend/`)
- **index.html**: Eingabeformular für Ideen, Kontext, Fokus-Bereich, Dateiuploads
- **result.html**: Strukturierte Ergebnisdarstellung
- **js/app.js**:
  - Konfigurierbare Backend-URL
  - Mock-Daten-Generator für Demo-Zwecke
  - API-Client für echte Backend-Verbindung
- **config.js**: Zentrale Konfiguration für Mock/Production-Modus

#### Backend (`brainstorming_ui.py`)
- Flask-Webserver mit Web-Interface und REST API
- Endpunkte:
  - `GET /` - Web-Interface
  - `POST /brainstorm` - Web-Form-Handler
  - `POST /api/brainstorm` - JSON REST API
- Dateiupload-Verarbeitung (PDF, DOCX, TXT, MD, CSV, JSON)

#### Brainstorming Skill (`brainstorming_skill/src/`)
- **skill.py**: Hauptorchestrator, koordiniert alle Komponenten
- **tree_of_thoughts.py**: ToT-Implementierung mit 10-Kriterien-Bewertung
- **graph_of_thoughts.py**: GoT-Implementierung mit Beziehungsanalyse
- **llm.py**: Abstraktionsschicht für verschiedene LLM-Provider
- **ollama_integration.py**: Spezielle Integration für lokale Ollama-Modelle
- **scoring.py**: Bewertungslogik für Lösungsansätze

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

## Funktionsweise: Von der Idee zum Plan

### Workflow

1. **Eingabe**: Benutzer gibt Idee, Kontext und optional Dateien ein
2. **ToT-Phase**: System generiert 3 verschiedene Lösungsansätze und bewertet sie nach 10 Kriterien
3. **GoT-Phase**: Analysiert Beziehungen zwischen Ansätzen und synthetisiert hybride Lösung
4. **Refinement**: Ensemble-Verfahren kombiniert beste Aspekte aller Ansätze
5. **Ausgabe**: Strukturiertes Ergebnis mit:
   - Problem Statement
   - Ziele & KPIs
   - Funktionale/Nicht-funktionale Anforderungen (MoSCoW-priorisiert)
   - Risiken & Annahmen
   - Implementierungspotenzial (Architektur, Technologie-Stack)
   - Phasenweise Task-Liste
   - Test-Strategie
   - Follow-up-Prompts für nachgelagerte Skills

### Bewertungskriterien (ToT)

Jeder Gedankengang wird nach 10 Kriterien bewertet:

1. **Zielerreichung** (15%): Wie gut wird das ursprüngliche Problem gelöst?
2. **Machbarkeit** (12%): Wie realistisch ist die Umsetzung?
3. **Aufwand** (12%): Wie ressourcenintensiv ist die Lösung?
4. **Wartbarkeit** (11%): Wie gut ist die langfristige Pflegbarkeit?
5. **Risiko** (11%): Wie hoch sind die technischen/geschäftlichen Risiken?
6. **ROI** (10%): Welcher Return on Investment ist zu erwarten?
7. **Innovation** (8%): Wie innovativ ist der Ansatz?
8. **Sicherheit** (8%): Wie sicher ist die Lösung?
9. **Team-Fit** (7%): Passt die Lösung zu den Team-Fähigkeiten?
10. **UX** (6%): Wie gut ist die Benutzererfahrung?

## Installation & Deployment

### Option 1: Lokale Entwicklung (Empfohlen)

#### Voraussetzungen
- Python 3.8+
- Git
- Ollama (optional, für lokale LLMs)

#### Schritte
```bash
# 1. Repository klonen
git clone https://github.com/DYAI2025/BrainPlan_LLM.git
cd BrainPlan_LLM

# 2. Abhängigkeiten installieren
cd brainstorming_skill
pip install -r requirements.txt
cd ..

# 3. (Optional) Ollama installieren und Modell laden
ollama serve
ollama pull llama3.2:latest

# 4. Flask-Anwendung starten
python brainstorming_ui.py

# 5. Browser öffnen
# Öffne http://localhost:5000
```

Die lokale Installation bietet das vollständige Interface mit echten LLM-Berechnungen.

### Option 2: Frontend-Demo (GitHub Pages)

Das Frontend kann als Demo mit Mock-Daten auf GitHub Pages gehostet werden.

#### GitHub Pages aktivieren

1. **Repository Settings** öffnen
2. **Pages** Sektion aufrufen
3. **Source**: GitHub Actions auswählen
4. Bei Push zu `main` oder `master` wird automatisch deployed

#### Workflow-Konfiguration

Der Workflow in `.github/workflows/deploy.yml`:
- Wird bei Push zu `main` oder `master` ausgelöst
- Kopiert `frontend/*` nach `dist/`
- Deployed auf GitHub Pages
- Benötigt folgende Permissions:
  - `contents: read`
  - `pages: write`
  - `id-token: write`

#### Frontend-Konfiguration anpassen

```javascript
// frontend/config.js anpassen:

// Für Demo-Modus (GitHub Pages):
window.USE_MOCK_DATA = true;

// Für Production mit Backend:
window.USE_MOCK_DATA = false;
window.BACKEND_URL = 'https://your-backend-url.com';
```

### Option 3: Production-Deployment (Frontend + Backend)

#### Frontend auf GitHub Pages
1. `frontend/config.js` anpassen:
   ```javascript
   window.USE_MOCK_DATA = false;
   window.BACKEND_URL = 'https://your-backend.com';
   ```
2. Zu `main` Branch pushen
3. GitHub Actions deployed automatisch

#### Backend auf Cloud-Plattform

**Railway:**
```bash
# 1. Railway CLI installieren
npm install -g @railway/cli

# 2. Projekt erstellen
railway init

# 3. Environment Variables setzen
railway variables set OLLAMA_URL=http://localhost:11434

# 4. Deploy
railway up
```

**Heroku:**
```bash
# 1. Procfile erstellen
echo "web: python brainstorming_ui.py" > Procfile

# 2. Deploy
heroku create your-app-name
git push heroku main
```

**Eigener Server:**
```bash
# Mit gunicorn (Production-ready)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 brainstorming_ui:app
```

## LLM-Integration

### Unterstützte Provider

Das System bietet flexible LLM-Integration:

| Provider | Modelle | Vorteile | Nachteile |
|----------|---------|----------|-----------|
| **Ollama** | llama3.2, mistral, qwen | Lokal, kostenlos, Datenschutz | Benötigt lokale Hardware |
| **OpenAI** | GPT-4, GPT-3.5 | Hohe Qualität, schnell | Kostenpflichtig, Cloud-Abhängigkeit |
| **Anthropic** | Claude 3.5 Sonnet, Claude 3 | Sehr gute Reasoning-Fähigkeiten | Kostenpflichtig |

### Empfohlene Konfiguration

**Für Entwicklung/Tests:**
```python
# Ollama mit llama3.2
ollama pull llama3.2:latest
# Schnell, kostenlos, gute Qualität
```

**Für Production:**
```python
# Claude 3.5 Sonnet oder GPT-4
# Beste Ergebnisqualität für kritische Anwendungen
```

### Konfiguration

LLM-Provider wird in `brainstorming_skill/.env` konfiguriert:

```bash
# Ollama (Standard)
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2:latest
OLLAMA_URL=http://localhost:11434

# OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4

# Anthropic
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

## API-Dokumentation

### REST API Endpunkte

#### `POST /api/brainstorm`

Führt einen vollständigen Brainstorming-Durchlauf durch.

**Request:**
```json
{
  "idea": "Entwicklung einer Fitness-Tracking-App",
  "context": "Mobile-First, Integration mit Wearables",
  "focus": "architektur",
  "round_info": "Erste Iteration"
}
```

**Response:**
```json
{
  "problem_statement": "### Situation\n...",
  "goals_kpis": "## Hauptziele\n...",
  "functional_requirements": "FR-1 (H): ...",
  "nonfunctional_requirements": "NFR-1 (H): ...",
  "risks_assumptions": "## Risiken\nRISIKO-1: ...",
  "implementation_potential": "## Architekturansatz\n...",
  "task_list": "### Phase 1\nT1.1: ...",
  "test_ideas": "TS-1: ...",
  "followup_prompts": {
    "prompt_planner": "...",
    "prompt_architect": "...",
    "prompt_dev": "..."
  }
}
```

**Fokus-Optionen:**
- `allgemein`: Ausgewogene Analyse
- `architektur`: Fokus auf System-Design
- `tests`: Fokus auf Teststrategien
- `datenmodell`: Fokus auf Datenstrukturen
- `plan`: Fokus auf Projektplanung

## Verwendungsszenarien

### 1. Standalone Brainstorming-Tool
Verwenden Sie die Web-Oberfläche für interaktive Anforderungsanalyse.

### 2. API-Integration
Integrieren Sie in bestehende Workflows:
```python
import requests

response = requests.post('http://localhost:5000/api/brainstorm', json={
    'idea': 'Ihre Idee',
    'context': 'Kontext',
    'focus': 'allgemein'
})
result = response.json()
```

### 3. Skill-Integration (Agent-Systeme)
```python
from brainstorming_skill.src.skill import execute_brainstorm_skill

inputs = {
    "idea": "...",
    "context": "...",
    "focus": "allgemein"
}
result = execute_brainstorm_skill(inputs)
```

### 4. Python-Bibliothek
```python
from brainstorming_skill.src.tree_of_thoughts import TreeOfThoughts
from brainstorming_skill.src.graph_of_thoughts import GraphOfThoughts

# Direkter Zugriff auf ToT/GoT
tot = TreeOfThoughts(llm_client)
thoughts = tot.generate_thoughts("Ihre Idee")
```

## Troubleshooting

### Frontend zeigt keine Ergebnisse
- **Prüfen**: Ist `USE_MOCK_DATA` in `frontend/config.js` korrekt gesetzt?
- **Mock-Modus**: `USE_MOCK_DATA = true` (kein Backend benötigt)
- **API-Modus**: `USE_MOCK_DATA = false` + Backend muss laufen

### Backend-Verbindungsfehler
```bash
# Prüfen ob Backend läuft:
curl http://localhost:5000/api/brainstorm -X POST -H "Content-Type: application/json" -d '{"idea": "test"}'

# CORS-Probleme? Backend braucht flask-cors:
pip install flask-cors
```

### Ollama-Fehler
```bash
# Ollama-Status prüfen:
ollama list

# Modell neu laden:
ollama pull llama3.2:latest

# Logs prüfen:
ollama serve --debug
```

### GitHub Pages Deployment schlägt fehl
- **Repository Settings → Pages**: Source auf "GitHub Actions" setzen
- **Workflow-File**: `.github/workflows/deploy.yml:5-7` prüft auf `main` oder `master` Branch
- **Permissions**: Workflow benötigt `pages: write` Permission (siehe deploy.yml:11-12)

## Projektstruktur

```
BrainPlan_LLM/
├── frontend/                      # Statisches Frontend für GitHub Pages
│   ├── index.html                 # Eingabeformular
│   ├── result.html                # Ergebnisanzeige
│   ├── config.js                  # Konfiguration (Mock/API-Modus)
│   ├── css/
│   │   └── style.css              # Styling
│   └── js/
│       └── app.js                 # Frontend-Logik
├── brainstorming_skill/           # Python-Backend & Skill
│   ├── src/
│   │   ├── skill.py               # Hauptorchestrator
│   │   ├── tree_of_thoughts.py    # ToT-Implementierung
│   │   ├── graph_of_thoughts.py   # GoT-Implementierung
│   │   ├── llm.py                 # LLM-Abstraktion
│   │   ├── ollama_integration.py  # Ollama-spezifisch
│   │   └── scoring.py             # Bewertungslogik
│   ├── config/
│   │   └── skill.yaml             # Skill-Konfiguration
│   ├── requirements.txt           # Python-Abhängigkeiten
│   └── .env.example               # Umgebungsvariablen-Vorlage
├── brainstorming_ui.py            # Flask-Webserver
├── .github/
│   └── workflows/
│       └── deploy.yml             # GitHub Actions Workflow
├── README.md                      # Diese Datei
├── LOCAL_DEPLOYMENT.md            # Lokale Deployment-Anleitung
└── github_pages_deployment.md     # GitHub Pages Setup-Guide
```

## Beiträge & Weiterentwicklung

### Geplante Features
- [ ] WebSocket-Support für Echtzeit-Updates
- [ ] Mehrsprachige Unterstützung (EN, FR, ES)
- [ ] Export-Funktionen (PDF, Markdown, JSON)
- [ ] Visualisierung des ToT/GoT-Graphen
- [ ] Benutzer-Feedback-Loop für iterative Verfeinerung
- [ ] Integration mit Projektmanagement-Tools (Jira, Linear)

### Wie Sie beitragen können
1. Fork das Repository
2. Erstellen Sie einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Committen Sie Ihre Änderungen (`git commit -m 'Add AmazingFeature'`)
4. Pushen Sie zum Branch (`git push origin feature/AmazingFeature`)
5. Öffnen Sie einen Pull Request

## Lizenz & Referenzen

### Wissenschaftliche Grundlagen

Diese Implementierung basiert auf folgenden Forschungsarbeiten:

- **Yao et al., 2024** – "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
  - [Paper](https://arxiv.org/abs/2305.10601)
  - Grundlage für unsere ToT-Implementierung

- **Besta et al., 2024** – "Graph of Thoughts: Solving Elaborate Problems with Large Language Models"
  - [Paper](https://arxiv.org/abs/2308.09687)
  - Grundlage für unsere GoT-Implementierung

### Technologie-Stack

- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Backend**: Python 3.8+, Flask
- **LLMs**: Ollama, OpenAI API, Anthropic API
- **Deployment**: GitHub Actions, GitHub Pages

## Kontakt & Support

- **Issues**: [GitHub Issues](https://github.com/DYAI2025/BrainPlan_LLM/issues)
- **Diskussionen**: [GitHub Discussions](https://github.com/DYAI2025/BrainPlan_LLM/discussions)

---

**Hinweis**: Dieses Projekt ist ein Proof-of-Concept und demonstriert die Anwendung von Tree-of-Thoughts und Graph-of-Thoughts Techniken für praktische Anforderungsanalyse. Für Production-Einsatz empfehlen wir zusätzliche Sicherheits- und Performance-Optimierungen.