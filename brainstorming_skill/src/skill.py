import json
from typing import Dict, Any, List

def execute_brainstorm_skill(inputs: Dict[str, Any], use_mock: bool = False) -> Dict[str, Any]:
    """
    Execute the brainstorming skill with the given inputs.
    This function now uses the enhanced version with project management features.
    """
    # Import and use the enhanced version
    from ..enhanced_skills.integration import execute_brainstorm_skill_with_enhancements
    return execute_brainstorm_skill_with_enhancements(inputs, use_mock)

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

def format_output_for_response(outputs: Dict[str, Any]) -> str:
    """
    Format the outputs into a readable response.
    """
    response = "# Brainstorming Ergebnis\n\n"
    
    response += "## 1. Problem Statement\n"
    response += f"{outputs['problem_statement']}\n\n"
    
    response += "## 2. Ziele & KPIs\n"
    response += f"{outputs['goals_kpis']}\n\n"
    
    response += "## 3. Funktionale Anforderungen\n"
    response += f"{outputs['functional_requirements']}\n\n"
    
    response += "## 4. Nicht-funktionale Anforderungen\n"
    response += f"{outputs['nonfunctional_requirements']}\n\n"
    
    response += "## 5. Risiken & Annahmen\n"
    response += f"{outputs['risks_assumptions']}\n\n"
    
    response += "## 6. Umsetzungspotenzial\n"
    response += f"{outputs['implementation_potential']}\n\n"
    
    response += "## 7. Task-Liste\n"
    response += f"{outputs['task_list']}\n\n"
    
    response += "## 8. Test-Ideen\n"
    response += f"{outputs['test_ideas']}\n\n"
    
    response += "## 9. Prompts für nachgelagerte Skills\n"
    response += "### Planner Prompt\n"
    response += f"{outputs['followup_prompts']['prompt_planner']}\n\n"
    response += "### Architect Prompt\n"
    response += f"{outputs['followup_prompts']['prompt_architect']}\n\n"
    response += "### Dev Prompt\n"
    response += f"{outputs['followup_prompts']['prompt_dev']}\n\n"
    
    return response