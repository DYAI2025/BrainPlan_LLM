"""
Integration der erweiterten Projektmanagement-Funktionen in den Brainstorming-Skill
"""
from typing import Dict, Any, List
from .constraint_analyzer import ConstraintAnalyzer
from .prioritizer import Prioritizer, RequirementsFormatter
from .dod_generator import DefinitionOfDoneGenerator, DoDFormatter
from .project_planner import ProjectPlanner, ProjectPlanFormatter
from .advanced_project_planner import enhance_with_blueprint_concepts
# Importiere direkt die benötigten Funktionen aus der ursprünglichen Implementierung
# um die rekursive Schleife zu vermeiden
from ..src.graph_of_thoughts import run_full_tot_then_got
from ..src.visualization import render_mermaid, generate_thought_summary, generate_hybrid_summary
from ..src.tree_of_thoughts import tree_of_thoughts_live
from ..src.scoring import calculate_total_score, validate_criteria_scores, Thought
from ..src.llm import llm
import json

def execute_brainstorm_skill_with_enhancements(inputs: Dict[str, Any], use_mock: bool = False) -> Dict[str, Any]:
    """
    Erweiterte Version des Brainstorming-Skills mit Projektmanagement-Funktionen
    """
    # Extrahiere die relevanten Informationen
    idea = inputs.get("idea", "")
    context = inputs.get("context", "")
    focus = inputs.get("focus", "allgemein")
    round_info = inputs.get("round_info", "")

    # Kombiniere Idee und Kontext für die Aufgabe
    if context:
        task = f"{idea}\n\nKontext: {context}"
    else:
        task = idea

    # Führe den ToT->GoT Pipeline mit Mock-Option aus
    # Verwende direkt die Funktionen, anstatt die Skill-Funktion aufzurufen
    pipeline_result = run_full_tot_then_got(task, use_mock=use_mock)

    # Extrahiere Komponenten
    tot_thoughts = pipeline_result["tot_thoughts"]
    got_result = pipeline_result["got_result"]
    final_hybrid = pipeline_result["final_hybrid"]

    # Generiere die ursprünglichen Komponenten wie im Original
    original_result = {}

    # Generiere Problem Statement
    original_result["problem_statement"] = generate_problem_statement(idea, context)

    # Generiere Goals und KPIs
    original_result["goals_kpis"] = generate_goals_and_kpis(idea)

    # Generiere funktionale und nicht-funktionale Anforderungen
    functional_requirements, nonfunctional_requirements = generate_requirements(tot_thoughts, final_hybrid)
    original_result["functional_requirements"] = functional_requirements
    original_result["nonfunctional_requirements"] = nonfunctional_requirements

    # Generiere Risiken und Annahmen
    original_result["risks_assumptions"] = generate_risks_and_assumptions()

    # Generiere Implementierungspotential
    original_result["implementation_potential"] = generate_implementation_potential(tot_thoughts, final_hybrid)

    # Generiere Task-Liste
    original_result["task_list"] = generate_task_list(tot_thoughts, final_hybrid)

    # Generiere Test-Ideen
    original_result["test_ideas"] = generate_test_ideas(tot_thoughts, final_hybrid)

    # Generiere Follow-up Prompts
    original_result["followup_prompts"] = generate_followup_prompts(idea, context, final_hybrid)

    # Führe die erweiterten Analysen durch
    enhanced_result = perform_enhanced_analysis(idea, context, original_result)

    return enhanced_result

def generate_problem_statement(idea: str, context: str) -> str:
    """Generate the problem statement based on the idea and context."""
    statement = f"Zusammenfassung der Idee: {idea}\n"
    if context:
        statement += f"Kontext: {context}"
    return statement

def generate_goals_and_kpis(idea: str) -> str:
    """Generate goals and KPIs based on the idea."""
    # This would be enhanced with LLM calls in a real implementation
    return f"Ziele und KPIs für: {idea}\n\n- Ziel 1: Beschreibung\n- Ziel 2: Beschreibung\n- KPI 1: Metrik\n- KPI 2: Metrik"

def generate_requirements(thoughts: List, final_hybrid) -> tuple[str, str]:
    """Generate functional and non-functional requirements."""
    # Extract requirements from the thoughts and hybrid solution
    functional = "FR-1 (H): Das System SOLLTE eine intuitive Benutzeroberfläche bieten\n"
    functional += "FR-2 (M): Das System MUSS in der Lage sein, Benutzerdaten zu speichern\n"

    nonfunctional = "NFR-1 (H): Das System MUSS innerhalb von 2 Sekunden auf Benutzereingaben reagieren\n"
    nonfunctional += "NFR-2 (M): Das System SOLLTE eine Verfügbarkeit von 99.9% bieten\n"

    return functional, nonfunctional

def generate_risks_and_assumptions() -> str:
    """Generate risks and assumptions."""
    risks = "RISIKO-1: Technische Umsetzbarkeit könnte komplexer sein als ursprünglich angenommen - Gegenmaßnahme: Prototypisierung\n"
    assumptions = "ANNAHME-1: Benutzer haben Zugang zu Internet - Wird für die Umsetzung vorausgesetzt\n"

    return risks + assumptions

def generate_implementation_potential(thoughts: List, final_hybrid) -> str:
    """Generate implementation potential and architecture sketch."""
    potential = "Komponenten:\n- Frontend-Modul\n- Backend-Service\n- Datenbank\n\nPhasen:\n- Phase 1: Prototyp\n- Phase 2: MVP\n- Phase 3: Produktion\n"
    return potential

def generate_task_list(thoughts: List, final_hybrid) -> str:
    """Generate high-level task list."""
    tasks = "T1: Technologie-Research (FR-1, FR-2)\nT2: UI/UX-Design (FR-1)\nT3: Backend-Entwicklung (FR-2)\n"
    return tasks

def generate_test_ideas(thoughts: List, final_hybrid) -> str:
    """Generate test ideas."""
    tests = "TS-1: Unit-Test (Unit) - Testet die Hauptlogik\nTS-2: Integrationstest (Integration) - Testet die API-Schnittstellen\nTS-3: E2E-Test (E2E) - Testet den kompletten Workflow\n"
    return tests

def generate_followup_prompts(idea: str, context: str, final_hybrid) -> Dict[str, str]:
    """Generate prompts for follow-up skills."""
    planner_prompt = f"Erstelle einen detaillierten Entwicklungsplan für: {idea}. "
    if context:
        planner_prompt += f"Kontext: {context}. "
    if final_hybrid:
        planner_prompt += f"Beste Lösung: {final_hybrid['summary']}"

    architect_prompt = f"Entwirf die Systemarchitektur für: {idea}. "
    if context:
        architect_prompt += f"Gegeben ist folgender Kontext: {context}. "
    if final_hybrid:
        architect_prompt += f"Die bevorzugte Lösung ist: {final_hybrid['summary']}"

    dev_prompt = f"Erstelle eine Entwicklungsstrategie und erste Implementierungsschritte für: {idea}. "
    if context:
        dev_prompt += f"Kontext: {context}. "
    if final_hybrid:
        dev_prompt += f"Ausgewählte Lösung: {final_hybrid['summary']}"

    return {
        "prompt_planner": planner_prompt,
        "prompt_architect": architect_prompt,
        "prompt_dev": dev_prompt
    }

def perform_enhanced_analysis(idea: str, context: str, original_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Führt die erweiterten Analysen durch und kombiniert sie mit den Originalergebnissen
    """
    # Verwende die neue Blueprint-Integration
    enhanced_result = enhance_with_blueprint_concepts(idea, context, original_result)

    # Ergänze die traditionellen Erweiterungen
    # 1. Constraint-Analyse
    constraint_analyzer = ConstraintAnalyzer()
    resources = constraint_analyzer.analyze_resources(idea + " " + context)

    # 2. Definition of Done für wichtige Features (wenn nicht bereits erstellt)
    if not enhanced_result.get("definitions_of_done"):
        dod_generator = DefinitionOfDoneGenerator()
        dod_formatter = DoDFormatter()

        # Extrahiere wichtige Features aus der Idee
        features = extract_features_from_idea(idea)

        # Generiere Definition of Done für jedes Feature
        all_dods = []
        for feature_desc in features:
            dod = dod_generator.generate_dod(feature_desc)
            formatted_dod = dod_formatter.format_dod(dod)
            all_dods.append(formatted_dod)

        enhanced_result["definitions_of_done"] = all_dods

    # Kombiniere die Ressourcenanalyse mit dem neuen Projektmanagement
    enhanced_result["resource_analysis"] = resources

    # Ergänze die Projektressourcen-Info
    if "project_resources" in enhanced_result:
        enhanced_result["project_resources"] += f"""

## Traditionelle Ressourcenanalyse
- Geschätzte Gesamtzeit: {resources['time_estimate']['total']:.1f} Wochen
- Geschätztes Budget: {resources['budget_estimate']:.2f} EUR
- Technische Ressourcen: {resources['technical_resources']}
- Benötigtes Personal: {resources['personnel']['developers']} Entwickler,
  {resources['personnel'].get('researchers', 0)} Forscher,
  {resources['personnel'].get('designers', 0)} Designer
"""
    else:
        enhanced_result["project_resources"] = f"""
## Ressourcenanalyse
- Geschätzte Gesamtzeit: {resources['time_estimate']['total']:.1f} Wochen
- Geschätztes Budget: {resources['budget_estimate']:.2f} EUR
- Technische Ressourcen: {resources['technical_resources']}
- Benötigtes Personal: {resources['personnel']['developers']} Entwickler,
  {resources['personnel'].get('researchers', 0)} Forscher,
  {resources['personnel'].get('designers', 0)} Designer
"""

    return enhanced_result

def extract_features_from_idea(idea: str) -> List[str]:
    """
    Extrahiert mögliche Features aus der Idee
    """
    # In einer realen Implementierung würde dies eine komplexe Analyse durchführen
    # Hier eine vereinfachte Version
    
    features = []
    
    # Muster für mögliche Features
    if "heatmap" in idea.lower():
        features.append(f"Heatmap-Anzeige: Visuelle Darstellung von Daten in Form einer Heatmap")
    
    if "integration" in idea.lower() or "integrieren" in idea.lower():
        features.append(f"Datenintegration: Integration verschiedener Datenquellen und Formate")
    
    if "KI" in idea or "KI" in idea or "künstliche intelligenz" in idea.lower():
        features.append(f"KI-Modul: Integration und Nutzung von KI-Algorithmen")
    
    if "bericht" in idea.lower() or "report" in idea.lower():
        features.append(f"Berichtsmodul: Erstellung und Export von Berichten")
    
    if not features:
        # Wenn keine spezifischen Features identifiziert wurden, verwende die ganze Idee
        features.append(f"Grundfunktion: {idea[:100]}{'...' if len(idea) > 100 else ''}")
    
    return features

# Aktualisierte Version der Hauptfunktion, die alle Erweiterungen enthält
def execute_brainstorm_skill(inputs: Dict[str, Any], use_mock: bool = False) -> Dict[str, Any]:
    """
    Hauptfunktion des Brainstorming-Skills mit allen Erweiterungen
    """
    return execute_brainstorm_skill_with_enhancements(inputs, use_mock)

# Testfunktion
def test_enhanced_skill():
    """
    Testet die erweiterte Skill-Funktionalität
    """
    test_inputs = {
        "idea": "Erstelle eine Webanwendung zur Visualisierung von Bias in KI-Modellen. Sollte Heatmaps anzeigen und wissenschaftliche Modelle integrieren (Hall, GLOBE, Hofstede).",
        "context": "Academic research tool for bias detection in ML models",
        "focus": "allgemein",
        "round_info": "Erste Iteration"
    }
    
    print("Starte erweiterten Brainstorming-Skill...")
    result = execute_brainstorm_skill(test_inputs, use_mock=True)
    
    print("Ergebnisse:")
    print(f"Problem Statement: {result['problem_statement'][:100]}...")
    print(f"Priorisierte Anforderungen: {result['prioritized_requirements'][:200]}...")
    print(f"Ressourcenanalyse und Projektplan: {result['project_resources'][:200]}...")
    
    print("\nErfolgreich getestet!")

if __name__ == "__main__":
    test_enhanced_skill()