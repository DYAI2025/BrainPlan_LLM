# Lokale Entwicklung und Ausführung

Da das GitHub Pages Deployment aktuell Probleme hat, hier eine Anleitung, wie die Anwendung lokal ausgeführt werden kann:

## Voraussetzungen
- Python 3.8 oder höher
- Git

## Installation

1. Stellen Sie sicher, dass Sie die benötigten Python-Pakete installiert haben:

```bash
cd brainstorming_skill
pip install -r requirements.txt
```

2. Stellen Sie sicher, dass Ollama läuft:

```bash
ollama serve
```

3. Stellen Sie sicher, dass das Modell installiert ist:

```bash
ollama pull llama3.2:latest
```

## Lokale Ausführung

### Option 1: Flask-Server direkt starten

1. Wechseln Sie in das Hauptverzeichnis:

```bash
cd /home/dyai/Dokumente/DYAI_home/DEV/GIT_repos/Brainstorm_LLM
```

2. Aktivieren Sie Ihre virtuelle Umgebung:

```bash
source myenv/bin/activate
```

3. Starten Sie den Flask-Server:

```bash
python brainstorming_ui.py
```

4. Öffnen Sie Ihren Browser und navigieren Sie zu [http://localhost:5000](http://localhost:5000)

### Option 2: Verwendung der Python-Bibliothek direkt

Sie können die Funktionen auch direkt in Python-Skripten verwenden:

```python
from brainstorming_skill.src.skill import execute_brainstorm_skill

inputs = {
    "idea": "Ihre Idee oder Anforderung",
    "context": "Zusätzlicher Kontext",
    "focus": "allgemein",
    "round_info": "Erste Iteration"
}

result = execute_brainstorm_skill(inputs, use_mock=True)
print(result)
```

## Entwicklungsumgebung

Wenn Sie an der Anwendung arbeiten möchten, beachten Sie folgende Verzeichnisstruktur:

- `brainstorming_skill/src/` - Hauptimplementierung
- `frontend/` - Statische HTML/CSS/JS Dateien für die GitHub Pages (wird lokal nicht benötigt)
- `brainstorming_skill/enhanced_skills/` - Erweiterte Funktionen für Projektmanagement

## Problembehebung

Wenn Sie Probleme haben:

1. Stellen Sie sicher, dass alle Abhängigkeiten installiert sind
2. Prüfen Sie, ob Ollama läuft und das Modell verfügbar ist
3. Überprüfen Sie Ihre Umgebungsvariablen (siehe `.env` Datei)
4. Schauen Sie in die Konsole oder Logdateien nach Fehlermeldungen

## Alternativen zu GitHub Pages

Falls Sie doch eine Online-Version bereitstellen möchten, könnten Sie:

1. Einen Service wie [PythonAnywhere](https://www.pythonanywhere.com/) verwenden
2. [Heroku](https://www.heroku.com/) oder [Railway](https://railway.app/) für die Bereitstellung nutzen
3. [Vercel](https://vercel.com/) für statische Dateien verwenden (muss aber mit Backend verbunden werden)

GitHub Pages ist hierbei nur eine von mehreren Möglichkeiten zur Bereitstellung.