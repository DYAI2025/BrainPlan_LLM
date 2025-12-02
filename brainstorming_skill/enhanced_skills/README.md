# Erweiterter Brainstorming-Skill mit Projektmanagement- und Anforderungsanalyse-Funktionen

## Beschreibung
Dies ist eine erweiterte Version des Brainstorming-Skills, die spezifische Funktionen für Projektmanagement und Anforderungsanalyse enthält, insbesondere:
- Constraint-Management (Zeit, Budget, Ressourcen)
- Priorisierung nach MoSCoW-Methode
- Operationalisierung mit Definition of Done
- Integration von Planungs- und Spezifikationsfähigkeiten

## Erweiterte Funktionen

### 1. Constraint-Management
Das System berücksichtigt explizit zeitliche, finanzielle und technische Einschränkungen:

- **Zeit-Ressourcen**: Verständnis für benötigte Forschungs-, Entwicklungs- und Testphasen
- **Budget-Ressourcen**: Kostenabschätzungen für Entwicklung, Betrieb und Wartung
- **Technische Ressourcen**: CPU, Speicher, Netzwerk und andere Systemressourcen
- **Personal-Ressourcen**: Verfügbare Entwickler, Designer, Tester, Fachexperten

Beispiel: Bei der Integration mehrerer wissenschaftlicher Modelle (z.B. Hall, GLOBE, Hofstede) gibt das System explizit an:
"Die Integration erfordert 6-8 Wochen Forschungszeit für Datenkuration, 2 Wochen für Modellvalidierung und zusätzliche 3 Wochen für die technische Implementierung."

### 2. Priorisierung nach MoSCoW-Methode
Das System klassifiziert Anforderungen in:

- **Must Have**: Grundlegende Funktionalitäten, ohne die das Produkt nicht funktioniert
- **Should Have**: Wichtige Funktionen, die stark zum Wert des Produkts beitragen
- **Could Have**: Nützliche Funktionen, die eingebaut werden können, wenn genug Zeit und Budget vorhanden sind
- **Won't Have (this time)**: Funktionen, die für aktuelle Iteration nicht vorgesehen sind

### 3. Operationalisierung mit Definition of Done
Für jede Funktion wird eine klare Definition of Done (DoD) angegeben:

Beispiel für "BiasHeatmap.jsx":
- **Definition of Done**:
  - Die Heatmap zeigt grafisch an, wo im Modell Bias-Werte > 0.5 auftreten
  - Die Visualisierung lädt in < 100ms
  - Die Farbcodierung folgt einer Standard-Palette (rot für hohe Bias-Werte)
  - Tooltips zeigen spezifische Bias-Werte an, wenn der Benutzer mit der Maus darüberfährt
  - Die Heatmap ist in einem Panel integriert, das sich ein- und ausblenden lässt

## Technische Implementierung

### Neue Module
1. `constraint_analyzer.py` - Analysiert Ressourcen und Einschränkungen
2. `prioritizer.py` - Implementiert die MoSCoW-Priorisierung
3. `dod_generator.py` - Erstellt Definition of Done für Features
4. `project_planner.py` - Erstellt Projektzeitpläne mit Meilensteinen

### Integration in bestehende Pipeline
Die neuen Module werden in die bestehende ToT→GoT→Ensemble Pipeline integriert:

1. **Phase 1**: Idee und Kontext werden analysiert
2. **Phase 2a**: ToT generiert Lösungsansätze
3. **Phase 2b**: GoT verbindet Ansätze und identifiziert Hybride
4. **Phase 2c**: Neue Erweiterung - Constraint- und Ressourcenanalyse
5. **Phase 2d**: Neue Erweiterung - Priorisierung mit MoSCoW
6. **Phase 2e**: Neue Erweiterung - Operationalisierung mit DoD
7. **Phase 3**: Ensemble Refinement produziert finalen Plan

## Beispiel-Ausgabe für erweiterten Skill

### Funktionale Anforderungen (mit Priorisierung):
**Must Have:**
- FR-1 (M): Das System MUSS in der Lage sein, Bias-Werte aus dem Modell zu extrahieren
- FR-2 (M): Das System MUSS eine grafische Heatmap anzeigen

**Should Have:**
- FR-3 (S): Das System SOLL die Bias-Heatmap in < 100ms laden
- FR-4 (S): Das System SOLL interaktive Tooltips für spezifische Bias-Werte anzeigen

**Could Have:**
- FR-5 (C): Das System KANN eine Exportfunktion für die Bias-Analyse bieten
- FR-6 (C): Das System KANN ein Bookmarking-System für häufige Analyse-Punkte bieten

### Projektzeitplan:
- **Phase 1: Datenextraktion (2 Wochen)**
  - Implementierung des Bias-Extraktions-Algorithmus
  - Unit-Tests für Extraktionsfunktion

- **Phase 2: Heatmap-Visualisierung (3 Wochen)**
  - Entwicklung der Heatmap-Komponente
  - Performance-Optimierung für < 100ms Ladezeit
  - Integration in bestehende UI

- **Phase 3: Interaktive Features (1 Woche)**
  - Implementierung von Tooltips
  - Implementierung des Panel-Systems
  - End-2-End-Tests

### Ressourcenbedarf:
- 2 Entwickler für 6 Wochen
- 1 UI/UX Designer für 2 Wochen
- Zugriff auf 2 GPU-Instanzen für Testphasen
- Budget für 2 Wochen externe Beratung für wissenschaftliche Validierung

## Implementierungsdetails

### constraint_analyzer.py
```python
class ConstraintAnalyzer:
    def analyze_resources(self, task_description):
        # Schätzt benötigte Ressourcen basierend auf Aufgabenbeschreibung
        resources = {
            "time_estimate": self.estimate_time(task_description),
            "budget_estimate": self.estimate_budget(task_description),
            "technical_resources": self.estimate_tech_resources(task_description),
            "personnel": self.estimate_personnel(task_description)
        }
        return resources
    
    def estimate_time(self, task):
        # Implementierung der Zeitschätzung basierend auf ähnlichen Aufgaben
        pass
```

### prioritizer.py
```python
class Prioritizer:
    def prioritize_requirements(self, requirements_list):
        # Klassifiziert Anforderungen nach MoSCoW-Methode
        prioritized = {
            "must_have": [],
            "should_have": [],
            "could_have": [],
            "wont_have": []
        }
        
        for req in requirements_list:
            category = self.classify_requirement(req)
            prioritized[category].append(req)
        
        return prioritized
```

### dod_generator.py
```python
class DefinitionOfDoneGenerator:
    def generate_dod(self, feature_description):
        # Erstellt eine Definition of Done für eine Funktion
        dod = {
            "functional_criteria": self.extract_functional_criteria(feature_description),
            "performance_criteria": self.extract_performance_criteria(feature_description),
            "quality_criteria": self.extract_quality_criteria(feature_description),
            "acceptance_tests": self.generate_acceptance_tests(feature_description)
        }
        return dod
```

Diese Erweiterung verbessert den Brainstorming-Skill erheblich in Richtung Projektmanagement und Anforderungsanalyse, indem sie explizit Ressourcen, Prioritäten und klare Abnahmekriterien berücksichtigt.