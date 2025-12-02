# Brainstorming Skill mit erweiterten Projektmanagement-Funktionen (nach Blueprint)

## Beschreibung
Dies ist eine erweiterte Version des Brainstorming-Skills, die umfassende Projektmanagement- und Anforderungsanalyse-Funktionen enthält, inspiriert vom project-resource-planner Blueprint. Der Skill implementiert:

- **Constraint-Management** (Zeit, Budget, Ressourcen)
- **Priorisierung nach MoSCoW-Methode**
- **Operationalisierung mit Definition of Done**
- **Detaillierte Projektplanung mit Ressourcenanalyse**
- **5D-Canvas Analyse** (Ziel, Scope, Ressourcen, Zeit, Risiken)
- **Iterativer Projektplan** (Sprints/Phasen/Releases)
- **Anforderungsmatrix mit Prioritäten**
- **Ressourcen- und Kapazitätsübersicht**
- **Risiko-, Annahmen- und Offene-Fragen-Liste**

## Hauptfunktionen

### 1. Erweiterte Anforderungsanalyse
Der Skill generiert nicht nur funktionale und nicht-funktionale Anforderungen, sondern priorisiert diese auch nach der MoSCoW-Methode:
- **Must Have**: Grundlegende Funktionen, ohne die das Produkt nicht funktioniert
- **Should Have**: Wichtige Funktionen, die stark zum Wert des Produkts beitragen
- **Could Have**: Nützliche Funktionen, die eingebaut werden können, wenn genug Zeit und Budget vorhanden sind
- **Won't Have**: Funktionen, die für aktuelle Iteration nicht vorgesehen sind

### 2. 5D-Canvas Projektanalyse
Strukturiert Projektinformationen entlang fünf Dimensionen:
- **Ziel & Outcome**: Projektziel(e), Definition of Done, Erfolgskriterien
- **Scope & Deliverables**: Features, Module, Workstreams; Out-of-Scope
- **Ressourcen**: Rollen, Personen, FTE, Skills, externe Dienstleister
- **Zeit & Constraints**: Deadlines, Timeboxes (Sprints/Phasen), Abhängigkeiten
- **Risiken & Annahmen**: bekannte Risiken, Unsicherheiten, explizite Annahmen

### 3. Ressourcen- und Constraint-Management
Der Skill berücksichtigt explizit zeitliche, finanzielle und technische Einschränkungen:
- **Zeit-Ressourcen**: Schätzt benötigte Forschungs-, Entwicklungs- und Testphasen
- **Budget-Ressourcen**: Gibt grobe Kostenschätzungen für Entwicklung, Betrieb und Wartung an
- **Technische Ressourcen**: Berücksichtigt CPU, Speicher, Netzwerk und andere Systemressourcen
- **Personal-Ressourcen**: Schätzt benötigte Entwickler, Designer, Tester, Fachexperten

### 4. Operationalisierung mit Definition of Done
Für jede Funktion wird eine klare Definition of Done (DoD) erstellt, die folgende Aspekte abdeckt:
- Funktionale Kriterien
- Leistungs-Kriterien
- Qualitäts-Kriterien
- Akzeptanztests

### 5. Iterative Projektplanung
Erstellt einen iterativen Projektplan mit:
- Sprint-/Phasenzielen
- groben Tasks oder Arbeitspaketen
- verantwortlichen Rollen
- groben Aufwandsschätzungen
- Abhängigkeitsanalyse

### 6. Ressourcen- und Kapazitätsübersicht
- Tabelle Rollen × Zeitraum (z.B. Sprint/Monat)
- verfügbare Kapazität (FTE oder Personentage)
- geplanter Aufwand
- Auslastungsanalyse mit identifizierten Engpässen

## Installation

Folgen Sie den gleichen Installationsanweisungen wie für den Basis-Skill:

1. Installieren Sie die Abhängigkeiten:
```
pip install -r requirements.txt
```

2. Stellen Sie sicher, dass Ollama läuft:
```
ollama serve
```

## Verwendung

Die Benutzung erfolgt wie beim Basis-Skill, aber mit erweiterten Ergebnissen:

```python
from brainstorming_skill.src import execute_brainstorm_skill

inputs = {
    "idea": "Eine App, die Pflanzen anhand von Fotos erkennt und Pflegetipps gibt",
    "context": "Mobile Anwendung für Hobbygärtner",
    "focus": "allgemein",
    "round_info": "Erste Iteration"
}

result = execute_brainstorm_skill(inputs)
```

## Neue Ausgabekomponenten

Zusätzlich zu den ursprünglichen Komponenten (Problem Statement, Goals & KPIs, Requirements, etc.) enthält die Ausgabe jetzt:

### Projekt-Blueprint
- Kurzbeschreibung des Projekts
- Ziele & Erfolgskriterien
- Scope-Übersicht (inkl. Out-of-Scope)
- Planungsansatz (Iterationsform, Zeithorizont)
- Schlüsselannahmen

### Anforderungsmatrix
- Tabelle mit ID, Kategorie, Anforderung, Priorität, Aufwand, Abhängigkeiten

### Iterativer Projektplan
- Übersicht pro Phase/Sprint mit Zielen, Deliverables, beteiligten Rollen, Aufwand

### Ressourcen- & Kapazitätsübersicht
- Tabelle Rollen × Zeitraum mit verfügbaren/gebrauchten Kapazitäten und Auslastung

### Risiken, Annahmen, offene Fragen
- Liste der wichtigsten Risiken mit Einschätzung
- Explizite Annahmen
- Offene Fragen mit Vorschlägen für Klärung

## Architektur

### Neue Module
1. `constraint_analyzer.py` - Analysiert Ressourcen und Einschränkungen
2. `prioritizer.py` - Implementiert die MoSCoW-Priorisierung
3. `dod_generator.py` - Erstellt Definition of Done für Features
4. `project_planner.py` - Erstellt Projektzeitpläne mit Meilensteinen
5. `advanced_project_planner.py` - Implementiert den Blueprint-Projektplaner
6. `integration.py` - Integriert alle neuen Funktionen in den Hauptskill

### Integration in bestehende Pipeline
Die neuen Module werden in die bestehende ToT→GoT→Ensemble Pipeline integriert:

1. **Phase 1**: Idee und Kontext werden analysiert
2. **Phase 2a**: ToT generiert Lösungsansätze
3. **Phase 2b**: GoT verbindet Ansätze und identifiziert Hybride
4. **Phase 2c**: Neue Erweiterung - 5D-Canvas Analyse
5. **Phase 2d**: Neue Erweiterung - Projekt-Blueprint Erstellung
6. **Phase 2e**: Neue Erweiterung - Iterativer Projektplan
7. **Phase 2f**: Neue Erweiterung - Ressourcen- und Kapazitätsanalyse
8. **Phase 3**: Ensemble Refinement produziert finalen Plan

## Beispielergebnis

Ein typisches Ergebnis enthält nun alle traditionellen Brainstorming-Komponenten plus:

- **Projekt-Blueprint**: Strukturierte Projektübersicht nach 5D-Canvas
- **Anforderungsmatrix**: Priorisierte und kategorisierte Anforderungen
- **Iterativer Projektplan**: Detaillierter Plan mit Sprints/Phasen
- **Ressourcenübersicht**: Kapazitäts- und Auslastungsanalyse
- **Risikoanalyse**: Risiken, Annahmen und offene Fragen

## Lizenz und Referenzen

Diese Erweiterung baut auf den gleichen Forschungsergebnissen wie der Basis-Skill auf:
- Yao et al., 2024 – "Tree of Thoughts: Thorough Reasoning with Large Language Models"
- Yao et al., 2024 – "Graph of Thoughts: Solving Elaborate Problems with Large Language Models"

Zusätzlich implementiert sie bewährte Projektmanagement-Methoden aus dem project-resource-planner Blueprint:
- 5D-Canvas Projektanalyse
- Iterative Projektplanung
- Kapazitätsanalyse mit Self-Consistency Checks
- Risiko- und Annahmenmanagement