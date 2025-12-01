# Brainstorming Skill mit Ollama Integration

Dieses Projekt enthält einen Brainstorming-Skill, der auf den Algorithmen Tree-of-Thoughts (ToT) und Graph-of-Thoughts (GoT) basiert und mit einem lokalen Ollama-Modell arbeitet.

## Voraussetzungen

- Python 3.8+
- Ollama (https://ollama.ai/)
- Ein installiertes Ollama-Modell (z.B. `llama3.2:8b`)

## Installation

1. Installiere die Python-Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

2. Installiere oder stelle sicher, dass ein Ollama-Modell verfügbar ist:
   ```bash
   ollama pull llama3.2:8b
   ```

3. Starte den Ollama-Server:
   ```bash
   ollama serve
   ```

## Konfiguration

Kopiere die Beispielkonfiguration und passe sie an:

```bash
cp .env.example .env
```

In der `.env`-Datei stelle sicher, dass die Ollama-spezifischen Einstellungen korrekt sind:

```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2:8b
OLLAMA_URL=http://localhost:11434
```

## Verwendung

### Als eigenständiges Modul

```python
from brainstorming_skill.src.skill import execute_brainstorm_skill

inputs = {
    "idea": "Eine App, die Pflanzen anhand von Fotos erkennt und Pflegetipps gibt",
    "context": "Mobile Anwendung für Hobbygärtner",
    # ... weitere Eingaben
}

result = execute_brainstorm_skill(inputs, use_mock=False)
print(result)
```

### Mit OllamaClient direkt

```python
from brainstorming_skill.src.ollama_integration import OllamaClient

client = OllamaClient()
client.set_model("llama3.2:8b")

# Generiere Gedanken direkt mit Ollama
thoughts = client.generate_initial_thoughts("Erstelle eine E-Learning-Plattform")
print(thoughts)
```

## Tests

Führe den Ollama-Test aus, um die Integration zu überprüfen:

```bash
python test_ollama.py
```

## Architektur

- `tree_of_thoughts.py`: Implementiert den Tree-of-Thoughts-Algorithmus
- `graph_of_thoughts.py`: Implementiert den Graph-of-Thoughts-Algorithmus
- `scoring.py`: Bewertungssystem für Gedanken basierend auf 10 Kriterien
- `llm.py`: Abstraktion für verschiedene LLM-Anbieter (inkl. Ollama)
- `ollama_integration.py`: Ollama-spezifische Implementierung
- `skill.py`: Haupt-Skill-Schnittstelle
- `visualization.py`: Erstellung von Visualisierungen (z.B. Mermaid-Diagramme)

## Lizenzen und Referenzen

Diese Implementation basiert auf den Forschungsergebnissen zu Tree-of-Thoughts und Graph-of-Thoughts:
- Yao et al., 2024 – "Tree of Thoughts: Thorough Reasoning with Large Language Models"
- Yao et al., 2024 – "Graph of Thoughts: Solving Elaborate Problems with Large Language Models"