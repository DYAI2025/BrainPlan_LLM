# GitHub Actions Workflow für Brainstorming Assistant

## Konzept

Da GitHub Pages nur statische Inhalte hosten kann, wird unser Setup folgende Architektur verwenden:

1. **Frontend**: Über GitHub Pages bereitgestellte statische Webseite (HTML, CSS, JS)
2. **Backend API**: Hosten auf einer Plattform wie Heroku, Railway, Render oder Vercel
3. **LLM-Integration**: Lokale Ollama-Instanz (kann auf demselben Backend-Server laufen)

## Verzeichnisstruktur für Frontend
```
frontend/
├── index.html
├── result.html
├── css/
│   └── style.css
├── js/
│   └── app.js
└── assets/
    └── (Bilder, Icons, etc.)
```

## GitHub Actions Workflow

Erstellen wir einen Workflow, der das Frontend nach Änderungen in den `gh-pages` Branch deployed:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install dependencies
      run: npm install
      working-directory: ./frontend

    - name: Build frontend
      run: npm run build
      working-directory: ./frontend

    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./frontend/dist
        publish_branch: gh-pages
```

## Backend-Implementierung für API

Als Alternative zu einer separaten Backend-Plattform könnten wir auch eine serverlose Lösung verwenden:

### Option 1: Backend auf separater Plattform (z.B. Railway)

Erstellen einer neuen Datei: `backend/app.py` (Flask-App für API)

```python
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

# Importiere den Skill
from brainstorming_skill.src.skill import execute_brainstorm_skill

app = Flask(__name__)

@app.route('/api/brainstorm', methods=['POST'])
def brainstorm_api():
    try:
        data = request.get_json()
        
        idea = data.get('idea', '').strip()
        context = data.get('context', '').strip()
        focus = data.get('focus', 'allgemein')
        round_info = data.get('round_info', 'Erste Iteration')
        
        if not idea:
            return jsonify({'error': 'Idee ist erforderlich'}), 400
        
        inputs = {
            "idea": idea,
            "context": context,
            "focus": focus,
            "round_info": round_info
        }
        
        # Führe den Skill aus (mit Mock-Funktion für Entwicklungsumgebung)
        # In Produktion würde hier die reale LLM-Integration genutzt
        result = execute_brainstorm_skill(inputs, use_mock=False)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

### Option 2: Serverlose Funktionen (z.B. mit Vercel)

Erstellen einer neuen Datei: `api/brainstorm.js` (für Vercel Functions)

```javascript
export default async function handler(request, response) {
  if (request.method !== 'POST') {
    return response.status(405).json({ error: 'Method not allowed' });
  }

  const { idea, context, focus = 'allgemein' } = request.body;

  if (!idea) {
    return response.status(400).json({ error: 'Idee ist erforderlich' });
  }

  try {
    // Hier würde die Kommunikation mit dem Backend/LLM stattfinden
    // In einer serverlosen Umgebung müsste dies ggf. an ein anderes Backend delegiert werden
    // oder eine serverlose LLM-Lösung (z.B. über API) verwendet werden
    
    // Platzhalter für die tatsächliche LLM-Verarbeitung
    const result = {
      problem_statement: 'Beispiel Problem Statement für: ' + idea,
      goals_kpis: 'Beispiel Ziele',
      functional_requirements: 'Beispiel funktionale Anforderungen',
      // ... weitere Ergebnisfelder
    };

    response.status(200).json(result);
  } catch (error) {
    response.status(500).json({ error: error.message });
  }
}
```

## Anpassung der Frontend-Anwendung

Die Frontend-Seiten müssen aktualisiert werden, um mit der externen API zu kommunizieren:

### Aktualisierte JavaScript-Logik in `js/app.js`:

```javascript
async function submitBrainstorm(idea, context, focus, files) {
  // Dateien verarbeiten
  let fileContent = '';
  if (files.length > 0) {
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      // Dateiinhalt lesen und an Kontext anhängen
      const text = await readFileAsText(file);
      fileContent += `\n\nInhalt aus ${file.name}:\n${text}`;
    }
  }

  const fullContext = context + fileContent;

  // API-Aufruf an externes Backend
  const response = await fetch('https://your-backend-url/api/brainstorm', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      idea: idea,
      context: fullContext,
      focus: focus,
      round_info: 'Erste Iteration'
    })
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  return await response.json();
}

function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsText(file);
  });
}

// Formular-Event-Handler
document.getElementById('brainstormForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const idea = document.getElementById('idea').value;
  const context = document.getElementById('context').value;
  const focus = document.getElementById('focus').value;
  const files = Array.from(document.getElementById('files').files);
  
  try {
    const result = await submitBrainstorm(idea, context, focus, files);
    displayResult(result, idea);
  } catch (error) {
    console.error('Fehler beim Brainstorming:', error);
    alert('Fehler beim Verarbeiten der Anfrage: ' + error.message);
  }
});
```

## LLM-Integration

Für die LLM-Integration in einer Produktionsumgebung gibt es mehrere Möglichkeiten:

1. **Lokale Ollama-Instanz**: Betrieb auf demselben Server wie das Backend
2. **Cloud-basierte LLMs**: Nutzung von OpenAI, Anthropic, Cohere APIs
3. **Spezialisierte LLM-Hosting-Plattformen**: wie Banana.dev, Replicate, Hugging Face Inference API

Für eine voll funktionsfähige LLM-Integration mit lokalen Modellen wäre eine Kombination aus:
- GitHub Pages für das Frontend
- Railway/Render/Heroku für das Backend
- Lokale Ollama-Instanz auf dem Backend-Server (oder als separater Service)

die empfohlene Architektur.

## Deployment-Schritte:

1. Implementiere das Frontend mit statischen Dateien
2. Erstelle den GitHub Actions Workflow für GitHub Pages Deployment
3. Implementiere das Backend mit API-Endpunkten
4. Deploy das Backend auf einer geeigneten Plattform
5. Passe die Frontend-Anwendung an, um mit dem Backend zu kommunizieren
6. Teste die vollständige Anwendung

Diese Architektur ermöglicht eine skalierbare und wartbare Lösung, bei der die Frontend- und Backend-Entwicklung unabhängig erfolgen kann.