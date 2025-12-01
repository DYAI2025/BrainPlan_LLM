import json
from typing import Dict, Any, List
from .graph_of_thoughts import run_full_tot_then_got
from .visualization import render_mermaid, generate_thought_summary, generate_hybrid_summary

def execute_brainstorm_skill(inputs: Dict[str, Any], use_mock: bool = False) -> Dict[str, Any]:
    """
    Execute the brainstorming skill with the given inputs.

    Args:
        inputs: Dictionary containing the skill inputs as defined in skill.yaml
        use_mock: If True, use mock data instead of calling the LLM

    Returns:
        Dictionary containing the skill outputs as defined in skill.yaml
    """
    # Extract inputs
    idea = inputs.get("idea", "")
    context = inputs.get("context", "")
    focus = inputs.get("focus", "allgemein")
    round_info = inputs.get("round_info", "")

    # Combine idea and context for the task
    if context:
        task = f"{idea}\n\nKontext: {context}"
    else:
        task = idea

    # Run the ToT->GoT pipeline
    pipeline_result = run_full_tot_then_got(task, use_mock=use_mock)

    # Extract components
    tot_thoughts = pipeline_result["tot_thoughts"]
    got_result = pipeline_result["got_result"]
    final_hybrid = pipeline_result["final_hybrid"]

    # Generate problem statement
    problem_statement = generate_problem_statement(idea, context)

    # Generate goals and KPIs
    goals_kpis = generate_goals_and_kpis(idea)

    # Generate functional and non-functional requirements
    functional_requirements, nonfunctional_requirements = generate_requirements(tot_thoughts, final_hybrid)

    # Generate risks and assumptions
    risks_assumptions = generate_risks_and_assumptions()

    # Generate implementation potential
    implementation_potential = generate_implementation_potential(tot_thoughts, final_hybrid)

    # Generate task list
    task_list = generate_task_list(tot_thoughts, final_hybrid)

    # Generate test ideas
    test_ideas = generate_test_ideas(tot_thoughts, final_hybrid)

    # Generate follow-up prompts
    followup_prompts = generate_followup_prompts(idea, context, final_hybrid)

    # Format the response
    outputs = {
        "problem_statement": problem_statement,
        "goals_kpis": goals_kpis,
        "functional_requirements": functional_requirements,
        "nonfunctional_requirements": nonfunctional_requirements,
        "risks_assumptions": risks_assumptions,
        "implementation_potential": implementation_potential,
        "task_list": task_list,
        "test_ideas": test_ideas,
        "followup_prompts": followup_prompts
    }

    return outputs

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