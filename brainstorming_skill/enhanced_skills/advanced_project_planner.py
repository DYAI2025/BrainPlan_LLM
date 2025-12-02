"""
Advanced Project Planner für den erweiterten Brainstorming-Skill
Implementiert die Projektmanagement-Funktionen aus dem project-resource-planner Blueprint
"""
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta
import re
from ..enhanced_skills.constraint_analyzer import ConstraintAnalyzer
from ..enhanced_skills.prioritizer import Prioritizer, RequirementsFormatter
from ..enhanced_skills.dod_generator import DefinitionOfDoneGenerator, DoDFormatter

class Project5DCanvas:
    """
    Strukturiert Projektinformationen entlang des 5D-Canvas:
    - Ziel & Outcome
    - Scope & Deliverables
    - Ressourcen
    - Zeit & Constraints
    - Risiken & Annahmen
    """
    
    def __init__(self, project_description: str):
        self.project_description = project_description
        self.goal_outcome = ""
        self.scope_deliverables = []
        self.resources = {}
        self.time_constraints = {}
        self.risks_assumptions = []
        self.open_questions = []
        
    def analyze_project_description(self):
        """
        Analysiert die Projektbeschreibung und extrahiert die 5D-Elemente
        """
        desc_lower = self.project_description.lower()
        
        # Ziel & Outcome
        goal_patterns = [
            r"ziel.*?ist es.*?([^.]+)",
            r"erfolg.*?wäre.*?([^.]+)",
            r"machen.*?wollen.*?([^.]+)",
            r"ziel.*?([^.]+?)(erfolg|scope|ressourcen|zeit|risiken|$)"
        ]
        
        for pattern in goal_patterns:
            match = re.search(pattern, self.project_description, re.IGNORECASE)
            if match:
                self.goal_outcome = match.group(1).strip()
                break
        
        if not self.goal_outcome:
            self.goal_outcome = f"Entwicklung und Implementierung von {self.project_description[:50]}{'...' if len(self.project_description) > 50 else ''}"
        
        # Scope & Deliverables
        # Extrahiere mögliche Komponenten und Funktionen
        components = re.findall(r"(\w+(?:-\w+)*)\s*(?:system|plattform|anwendung|tool|lösung)", self.project_description, re.IGNORECASE)
        features = re.findall(r"(?:eine )?(?:funktion|komponente|modul)\s+([^.]+?)(?:,|\.| und|\s+für|\s+mit)", self.project_description, re.IGNORECASE)
        
        self.scope_deliverables = []
        for comp in components:
            self.scope_deliverables.append(f"{comp.title()}-System")
        for feat in features:
            self.scope_deliverables.append(feat.strip())
        
        # Falls keine spezifischen Komponenten gefunden wurden, verwende das Projekt selbst
        if not self.scope_deliverables:
            self.scope_deliverables = [self.goal_outcome.split('.')[0] if '.' in self.goal_outcome else self.goal_outcome]
        
        # Risiken & Annahmen
        risk_keywords = ["risiko", "problem", "herausforderung", "komplikation", "hürde", "abhaengigkeit"]
        assumption_keywords = ["angenommen", "angenommen wird", "wir gehen davon aus", "unter der annahme", "wenn"]
        
        for keyword in risk_keywords:
            if keyword in desc_lower:
                self.risks_assumptions.append(f"Potenzielles Risiko identifiziert: {keyword}")
        
        for keyword in assumption_keywords:
            if keyword in desc_lower:
                self.risks_assumptions.append(f"Vor Annahme: {keyword}")
        
        # Offene Fragen
        question_keywords = ["offen", "unklar", "klären", "noch zu klären", "bedarf", "was ist mit"]
        for keyword in question_keywords:
            if keyword in desc_lower:
                self.open_questions.append(f"Offene Frage: {keyword}")
        
        # Wenn keine spezifischen Informationen gefunden wurden, fülle mit Standardwerten
        if not self.risks_assumptions:
            self.risks_assumptions = ["Technische Umsetzbarkeit kann variieren", "Abhängigkeiten von externen Systemen"]
        
        if not self.open_questions:
            self.open_questions = ["Details zur Implementierung", "Spezifikation der genauen Anforderungen"]
    
    def set_resources(self, resource_data: Dict[str, Any]):
        """
        Setzt die Ressourceninformationen
        """
        self.resources = resource_data
    
    def set_time_constraints(self, time_data: Dict[str, Any]):
        """
        Setzt die Zeitinformationen
        """
        self.time_constraints = time_data


class AdvancedProjectPlanner:
    """
    Implementiert die Projektplanungsfunktionen basierend auf dem project-resource-planner Blueprint
    """
    
    def __init__(self):
        self.constraint_analyzer = ConstraintAnalyzer()
        self.prioritizer = Prioritizer()
        self.dod_generator = DefinitionOfDoneGenerator()
        
    def create_project_blueprint(self, idea: str, context: str, requirements: List[str]) -> Dict[str, Any]:
        """
        Erstellt einen Projekt-Blueprint basierend auf dem 5D-Canvas
        """
        # 1. Analysiere Projektbeschreibung
        description = f"{idea} {context}"
        canvas = Project5DCanvas(description)
        canvas.analyze_project_description()
        
        # 2. Priorisiere Anforderungen
        prioritized_reqs = self.prioritizer.prioritize_requirements(requirements)
        
        # 3. Analysiere Ressourcen
        resources = self.constraint_analyzer.analyze_resources(description)
        
        # 4. Erstelle Projekt-Blueprint
        blueprint = {
            "project_brief": {
                "description": idea,
                "context": context,
                "goal_outcome": canvas.goal_outcome,
                "success_criteria": self._derive_success_criteria(idea),
            },
            "structured_scope": {
                "epics_workstreams": canvas.scope_deliverables,
                "delivered_by": self._organize_by_priority(prioritized_reqs),
                "out_of_scope": self._identify_out_of_scope(prioritized_reqs)
            },
            "resource_model": {
                "roles_teams": self._derive_roles(resources),
                "fte_matrix": self._create_fte_matrix(resources),
                "bottlenecks": self._identify_bottlenecks(resources)
            },
            "planning_granularity": {
                "iteration_form": "Sprints (2-wöchig)",
                "planning_horizon": f"MVP in {resources['time_estimate']['total']:.1f} Wochen"
            },
            "risks_assumptions_list": {
                "key_risks": canvas.risks_assumptions,
                "explicit_assumptions": self._derive_assumptions(resources),
                "open_questions": canvas.open_questions
            }
        }
        
        return blueprint
    
    def create_iterative_project_plan(self, blueprint: Dict[str, Any], 
                                      resource_constraints: Dict[str, int] = None) -> Dict[str, Any]:
        """
        Erstellt einen iterativen Projektplan mit Sprints/Phasen/Releases
        """
        # Extrahiere notwendige Daten aus dem Blueprint
        deliverables = blueprint['structured_scope']['delivered_by']
        resources = blueprint['resource_model']['fte_matrix']
        
        # Bestimme Iterationsstruktur (Sprints/Phasen)
        iterations = self._create_iterations(deliverables, resources)
        
        # Erstelle detaillierten Plan
        plan = {
            "iterative_project_plan": {
                "sprints_phases": iterations,
                "resource_allocation": self._create_resource_allocation(resources, iterations),
                "dependencies": self._determine_dependencies(iterations)
            }
        }
        
        return plan
    
    def _derive_success_criteria(self, idea: str) -> List[str]:
        """
        Leitet Erfolgskriterien aus der Idee ab
        """
        criteria = [
            "Anforderungen werden gemäß Spezifikation umgesetzt",
            "Lösung ist benutzerfreundlich und funktioniert zuverlässig"
        ]
        
        # Füge spezifische Kriterien basierend auf der Idee hinzu
        if "perf" in idea.lower() or "geschwindigkeit" in idea.lower():
            criteria.append("Lösung erreicht definierte Performance-Ziele")
        
        if "sicherheit" in idea.lower():
            criteria.append("Lösung erfüllt Sicherheitsanforderungen")
        
        return criteria
    
    def _organize_by_priority(self, prioritized_reqs: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[str]]:
        """
        Organisiert Anforderungen nach Priorität
        """
        organized = {}
        for priority, req_list in prioritized_reqs.items():
            organized[priority] = [item["requirement"] for item in req_list]
        return organized
    
    def _identify_out_of_scope(self, prioritized_reqs: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """
        Identifiziert Anforderungen, die out-of-scope sind
        """
        # In dieser Implementierung: Won't Have Anforderungen sind out-of-scope
        wont_have = prioritized_reqs.get("wont_have", [])
        return [item["requirement"] for item in wont_have]
    
    def _derive_roles(self, resources: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Leitet benötigte Rollen aus den Ressourcen ab
        """
        roles = []
        
        personnel = resources.get("personnel", {})
        for role, count in personnel.items():
            if count > 0:
                roles.append({
                    "name": role,
                    "count": count,
                    "fte_per_person": 1.0
                })
        
        return roles
    
    def _create_fte_matrix(self, resources: Dict[str, Any]) -> Dict[str, float]:
        """
        Erstellt eine FTE-Matrix aus den Ressourcen
        """
        personnel = resources.get("personnel", {})
        fte_matrix = {}
        
        for role, count in personnel.items():
            if count > 0:
                fte_matrix[role] = count  # Einfache Annahme: count = FTE
        
        return fte_matrix
    
    def _identify_bottlenecks(self, resources: Dict[str, Any]) -> List[str]:
        """
        Identifiziert potenzielle Engpässe in den Ressourcen
        """
        bottlenecks = []
        
        if resources.get("technical_resources", {}).get("gpu", 0) == 0:
            bottlenecks.append("Keine GPU-Ressourcen verfügbar für KI/ML-Training")
        
        if resources.get("personnel", {}).get("researchers", 0) == 0:
            bottlenecks.append("Keine Forscher für wissenschaftliche Analyse verfügbar")
        
        return bottlenecks
    
    def _derive_assumptions(self, resources: Dict[str, Any]) -> List[str]:
        """
        Leitet explizite Annahmen aus den Ressourcen ab
        """
        assumptions = []
        
        time_est = resources.get("time_estimate", {})
        assumptions.append(f"Standard-Sprintlänge 2 Wochen, Gesamtprojektzeit: {time_est.get('total', 0):.1f} Wochen")
        
        tech_res = resources.get("technical_resources", {})
        if tech_res.get("gpu", 0) == 0:
            assumptions.append("Keine GPU-Zeit verfügbar - ML-Komponenten werden auf CPU ausgeführt")
        
        return assumptions
    
    def _create_iterations(self, deliverables: Dict[str, List[str]], 
                          resources: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Erstellt Iterationen (Sprints/Phasen) basierend auf Anforderungen und Ressourcen
        """
        iterations = []
        
        # Ordne die Anforderungen nach Priorität
        all_requirements = []
        for priority, req_list in deliverables.items():
            for req in req_list:
                all_requirements.append((priority, req))
        
        # Erstelle Sprints basierend auf der Priorität
        sprint_num = 1
        current_start_date = datetime.now()
        
        # Gruppiere Anforderungen in Sprints
        for i, (priority, req) in enumerate(all_requirements):
            # Bestimme Dauer basierend auf Priorität
            duration_multiplier = 1.0
            if priority == "must_have":
                duration_multiplier = 1.0  # Hohe Priorität, volle Ressourcen
            elif priority == "should_have":
                duration_multiplier = 1.2  # Mittlere Priorität
            elif priority == "could_have":
                duration_multiplier = 1.5  # Niedrigere Priorität
            else:  # wont_have
                continue  # Diese werden ignoriert
            
            sprint_length = 2 * duration_multiplier  # Standard 2 Wochen pro Sprint
            sprint_end_date = current_start_date + timedelta(weeks=sprint_length)
            
            iteration = {
                "iteration_number": sprint_num,
                "timeframe": f"{current_start_date.strftime('%d.%m.%Y')} - {sprint_end_date.strftime('%d.%m.%Y')}",
                "duration_weeks": sprint_length,
                "goal": f"Sprint {sprint_num} - {priority.replace('_', ' ').title()} Implementierung",
                "deliverables": [req],
                "assigned_roles": list(resources.keys()) if resources else ["Developer"],
                "effort_estimate": f"{duration_multiplier * 15:.0f} Personentage"  # Schätzung
            }
            
            iterations.append(iteration)
            current_start_date = sprint_end_date
            sprint_num += 1
            
            # Gruppiere mehrere niedrigere Prioritäten in einem Sprint
            if priority in ["could_have", "wont_have"]:
                if i + 1 < len(all_requirements) and all_requirements[i+1][0] == priority:
                    # Nächste Anforderung hat gleiche Priorität, füge sie diesem Sprint hinzu
                    iterations[-1]["deliverables"].append(all_requirements[i+1][1])
        
        return iterations
    
    def _create_resource_allocation(self, resources: Dict[str, float], 
                                   iterations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Erstellt eine Ressourcenallokation für jede Iteration
        """
        allocation = []
        
        for iteration in iterations:
            iter_alloc = {
                "iteration": iteration["iteration_number"],
                "timeframe": iteration["timeframe"],
                "roles": []
            }
            
            # Berechne Kapazitäten für jede Rolle in dieser Iteration
            for role, fte in resources.items():
                role_alloc = {
                    "role": role,
                    "fte_available": fte,
                    "fte_planned": fte * 0.8,  # 80% Planung, 20% Reserve
                    "utilization": (fte * 0.8) / fte * 100 if fte > 0 else 0
                }
                iter_alloc["roles"].append(role_alloc)
            
            allocation.append(iter_alloc)
        
        return allocation
    
    def _determine_dependencies(self, iterations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Bestimmt Abhängigkeiten zwischen Iterationen
        """
        dependencies = []
        
        for i in range(1, len(iterations)):
            # Jede Iteration hängt von der vorhergehenden ab
            dependency = {
                "from_iteration": iterations[i-1]["iteration_number"],
                "to_iteration": iterations[i]["iteration_number"],
                "type": "finish_to_start",
                "description": f"Iteration {iterations[i]['iteration_number']} kann erst beginnen, wenn {iterations[i-1]['iteration_number']} abgeschlossen ist"
            }
            dependencies.append(dependency)
        
        return dependencies


class AdvancedProjectPlanFormatter:
    """
    Formatierer für den erweiterten Projektplan gemäß den Vorgaben
    """
    
    @staticmethod
    def format_project_blueprint(blueprint: Dict[str, Any]) -> str:
        """
        Formatierung des Projekt-Blueprints
        """
        formatted = "## PROJEKT-BLUEPRINT\n\n"
        
        formatted += f"**Kurzbeschreibung:** {blueprint['project_brief']['description']}\n\n"
        formatted += f"**Ziel:** {blueprint['project_brief']['goal_outcome']}\n\n"
        formatted += f"**Erfolgskriterien:**\n"
        for criterion in blueprint['project_brief']['success_criteria']:
            formatted += f"- {criterion}\n"
        formatted += "\n"
        
        formatted += "**Scope-Übersicht:**\n"
        formatted += f"- **In Scope:** {', '.join(blueprint['structured_scope']['epics_workstreams'])}\n"
        if blueprint['structured_scope']['out_of_scope']:
            formatted += f"- **Out of Scope:** {', '.join(blueprint['structured_scope']['out_of_scope'])}\n"
        formatted += "\n"
        
        formatted += f"**Planungsansatz:** {blueprint['planning_granularity']['iteration_form']}\n"
        formatted += f"**Zeithorizont:** {blueprint['planning_granularity']['planning_horizon']}\n\n"
        
        formatted += "**Wichtige Annahmen:**\n"
        for assumption in blueprint['risks_assumptions_list']['explicit_assumptions']:
            formatted += f"- {assumption}\n"
        formatted += "\n"
        
        return formatted
    
    @staticmethod
    def format_requirement_matrix(blueprint: Dict[str, Any]) -> str:
        """
        Formatierung der Anforderungsmatrix
        """
        formatted = "## ANFORDERUNGMATRIX\n\n"
        
        # Tabelle für Anforderungen
        formatted += "| ID | Kategorie | Anforderung | Priorität | Aufwand | Abhängigkeiten |\n"
        formatted += "|---|---|---|---|---|---|\n"
        
        row_id = 1
        for priority, reqs in blueprint['structured_scope']['delivered_by'].items():
            for req in reqs:
                priority_label = priority.replace('_', ' ').upper()
                formatted += f"| {row_id} | Feature | {req} | {priority_label[:1]} | TBD | - |\n"
                row_id += 1
        
        formatted += "\n"
        return formatted
    
    @staticmethod
    def format_iterative_project_plan(plan: Dict[str, Any]) -> str:
        """
        Formatierung des iterativen Projektplans
        """
        formatted = "## ITERATIVER PROJEKTPLAN\n\n"
        
        formatted += "| Sprint # | Zeitraum | Ziele & Deliverables | Beteiligte Rollen | Aufwand |\n"
        formatted += "|---|---|---|---|---|\n"
        
        for sprint in plan['iterative_project_plan']['sprints_phases']:
            deliverables_str = "; ".join(sprint['deliverables'][:2])  # Nur die ersten 2 anzeigen
            if len(sprint['deliverables']) > 2:
                deliverables_str += f" + {len(sprint['deliverables'])-2} weitere"
            
            formatted += f"| {sprint['iteration_number']} | {sprint['timeframe']} | {sprint['goal']} | {', '.join(sprint['assigned_roles'])} | {sprint['effort_estimate']} |\n"
        
        formatted += "\n"
        return formatted
    
    @staticmethod
    def format_resource_capacity_view(plan: Dict[str, Any]) -> str:
        """
        Formatierung der Ressourcen- und Kapazitätsübersicht
        """
        formatted = "## RESSOURCEN- & KAPAZITÄTSÜBERSICHT\n\n"
        
        formatted += "| Sprint | Rolle | Verfügbare Kapazität | Geplanter Aufwand | Auslastung |\n"
        formatted += "|---|---|---|---|---|\n"
        
        for alloc in plan['iterative_project_plan']['resource_allocation']:
            for role_data in alloc['roles']:
                formatted += f"| {alloc['iteration']} | {role_data['role']} | {role_data['fte_available']:.1f} FTE | {role_data['fte_planned']:.1f} FTE | {role_data['utilization']:.1f}% |\n"
        
        formatted += "\n**Interpretation:**\n"
        formatted += "- Über 100%: Überlastung, Anpassung notwendig\n"
        formatted += "- 80-100%: Gute Auslastung\n"
        formatted += "- Unter 60%: Ggf. Effizienzverluste\n\n"
        
        return formatted
    
    @staticmethod
    def format_risks_assumptions_questions(blueprint: Dict[str, Any]) -> str:
        """
        Formatierung der Risiken, Annahmen und offenen Fragen
        """
        formatted = "## RISIKEN, ANNAHMEN, OFFENE FRAGEN\n\n"
        
        formatted += "**Wichtigste Risiken:**\n"
        for risk in blueprint['risks_assumptions_list']['key_risks']:
            formatted += f"- {risk}\n"
        formatted += "\n"
        
        formatted += "**Explizite Annahmen:**\n"
        for assumption in blueprint['risks_assumptions_list']['explicit_assumptions']:
            formatted += f"- {assumption}\n"
        formatted += "\n"
        
        formatted += "**Offene Fragen:**\n"
        for question in blueprint['risks_assumptions_list']['open_questions']:
            formatted += f"- {question}\n"
        formatted += "\n"
        
        return formatted


# Integriere die neuen Funktionen in die Hauptintegration
def enhance_with_blueprint_concepts(idea: str, context: str, original_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Erweitert das Ergebnis um die Projektmanagement-Funktionen aus dem Blueprint
    """
    # Extrahiere Anforderungen aus dem Originalergebnis
    all_requirements = []
    if original_result.get("functional_requirements"):
        for line in original_result["functional_requirements"].split('\n'):
            if line.strip() and (line.startswith("FR-") or "muss" in line.lower() or 
                                "soll" in line.lower() or "kann" in line.lower()):
                all_requirements.append(line.strip())
    
    if original_result.get("nonfunctional_requirements"):
        for line in original_result["nonfunctional_requirements"].split('\n'):
            if line.strip() and (line.startswith("NFR-") or "performance" in line.lower() or 
                                "sicherheit" in line.lower()):
                all_requirements.append(line.strip())
    
    # Verwende leere Liste, falls keine Anforderungen gefunden wurden
    if not all_requirements:
        all_requirements = [
            f"Grundlegende Funktionalität für '{idea[:50]}...'",
            f"Benutzeroberfläche für '{idea[:30]}...'"
        ]
    
    # Erstelle den Projekt-Blueprint
    planner = AdvancedProjectPlanner()
    blueprint = planner.create_project_blueprint(idea, context, all_requirements)
    
    # Erstelle den iterativen Projektplan
    plan = planner.create_iterative_project_plan(blueprint)
    
    # Formatiere die Ergebnisse
    formatter = AdvancedProjectPlanFormatter()
    
    formatted_blueprint = formatter.format_project_blueprint(blueprint)
    formatted_requirements = formatter.format_requirement_matrix(blueprint)
    formatted_plan = formatter.format_iterative_project_plan(plan)
    formatted_resources = formatter.format_resource_capacity_view(plan)
    formatted_risks = formatter.format_risks_assumptions_questions(blueprint)
    
    # Kombiniere alle Ergebnisse
    enhanced_result = original_result.copy()
    
    # Aktualisiere die Hauptergebnisse mit den erweiterten Informationen
    enhanced_result["project_blueprint"] = formatted_blueprint
    enhanced_result["requirement_matrix"] = formatted_requirements
    enhanced_result["iterative_project_plan"] = formatted_plan
    enhanced_result["resource_capacity_view"] = formatted_resources
    enhanced_result["risks_assumptions_questions"] = formatted_risks
    
    # Kombiniere alle Projektmanagement-Informationen in einem Abschnitt
    enhanced_result["project_management"] = (
        formatted_blueprint + 
        formatted_requirements + 
        formatted_plan + 
        formatted_resources + 
        formatted_risks
    )
    
    # Aktualisiere Ressourcenanalyse mit den neuen detaillierten Informationen
    enhanced_result["project_resources"] = (
        f"{original_result.get('project_resources', '')}\n\n" +
        formatted_blueprint +
        formatted_resources
    )
    
    return enhanced_result