"""
ProjectPlanner für den erweiterten Brainstorming-Skill
Erstellt detaillierte Projektzeitpläne mit Ressourcen und Meilensteinen
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
import re

class Task:
    """
    Repräsentiert eine einzelne Projekt-Aufgabe
    """
    def __init__(self, name: str, description: str, duration: float, 
                 dependencies: List[str] = None, resources: Dict[str, Any] = None):
        self.name = name
        self.description = description
        self.duration = duration  # in Wochen
        self.dependencies = dependencies or []
        self.resources = resources or {}
        self.start_date = None
        self.end_date = None
        self.assigned_resources = {}

class ProjectPlanner:
    """
    Erstellt detaillierte Projektzeitpläne mit Ressourcen und Meilensteinen
    """
    
    def __init__(self):
        # Standarddauer für verschiedene Aufgabentypen in Wochen
        self.task_durations = {
            "forschung": 2.0,
            "analyse": 1.5,
            "design": 2.0,
            "implementierung": 3.0,
            "integration": 2.0,
            "test": 1.5,
            "dokumentation": 1.0,
            "bereitstellung": 1.0
        }
        
        # Standard-Ressourcenbedarf
        self.resource_requirements = {
            "forschung": {"researcher": 1, "developer": 0.5},
            "analyse": {"analyst": 1, "developer": 0.5},
            "design": {"designer": 1, "developer": 0.5},
            "implementierung": {"developer": 2},
            "integration": {"developer": 2, "architect": 0.5},
            "test": {"tester": 1, "developer": 0.5},
            "dokumentation": {"technical_writer": 1},
            "bereitstellung": {"devops": 1, "admin": 0.5}
        }
    
    def create_project_plan(self, features: List[Dict[str, Any]], 
                           resource_constraints: Dict[str, int] = None) -> Dict[str, Any]:
        """
        Erstellt einen Projektplan basierend auf Features und Ressourcenbeschränkungen
        """
        # Extrahiere Aufgaben aus Features
        tasks = self._extract_tasks_from_features(features)
        
        # Ordne Aufgaben zeitlich basierend auf Abhängigkeiten
        ordered_tasks = self._sequence_tasks(tasks)
        
        # Berücksichtige Ressourcenbeschränkungen
        if resource_constraints:
            scheduled_tasks = self._schedule_with_resources(ordered_tasks, resource_constraints)
        else:
            scheduled_tasks = self._assign_dates(ordered_tasks)
        
        # Erstelle Meilensteine
        milestones = self._create_milestones(scheduled_tasks)
        
        # Berechne Gesamtprojektdauer
        project_duration = self._calculate_project_duration(scheduled_tasks)
        
        return {
            "project_start_date": scheduled_tasks[0].start_date if scheduled_tasks else None,
            "project_end_date": scheduled_tasks[-1].end_date if scheduled_tasks else None,
            "project_duration_weeks": project_duration,
            "tasks": scheduled_tasks,
            "milestones": milestones,
            "resource_allocation": self._analyze_resource_allocation(scheduled_tasks)
        }
    
    def _extract_tasks_from_features(self, features: List[Dict[str, Any]]) -> List[Task]:
        """
        Extrahiert Projekt-Aufgaben aus Feature-Beschreibungen
        """
        tasks = []
        
        for feature in features:
            feature_name = feature.get("name", "Unbenanntes Feature")
            feature_description = feature.get("description", "")
            
            # Klassifiziere die Feature-Beschreibung in verschiedene Aufgabentypen
            task_types = self._classify_feature_tasks(feature_description)
            
            for i, task_type in enumerate(task_types):
                task_name = f"{feature_name} - {task_type.capitalize()}"
                task_desc = f"Aufgabe für {feature_name}: {task_type.capitalize()}"
                
                # Schätze Dauer basierend auf Aufgabentyp
                duration = self.task_durations.get(task_type, 2.0)
                
                # Schätze Ressourcenbedarf
                resources = self.resource_requirements.get(task_type, {"developer": 1})
                
                # Erstelle die Aufgabe
                task = Task(
                    name=task_name,
                    description=task_desc,
                    duration=duration,
                    resources=resources
                )
                
                tasks.append(task)
        
        return tasks
    
    def _classify_feature_tasks(self, description: str) -> List[str]:
        """
        Klassifiziert die notwendigen Aufgaben basierend auf der Feature-Beschreibung
        """
        desc_lower = description.lower()
        tasks = []
        
        # Muster für verschiedene Aufgabentypen
        if any(word in desc_lower for word in ["daten", "import", "extraktion", "kuration"]):
            if "forschung" not in tasks:
                tasks.append("forschung")
            if "analyse" not in tasks:
                tasks.append("analyse")
        
        if any(word in desc_lower for word in ["design", "ui", "ux", "schnittstelle", "anzeige"]):
            if "design" not in tasks:
                tasks.append("design")
        
        if any(word in desc_lower for word in ["implement", "entwickl", "code", "funktionalität"]):
            if "implementierung" not in tasks:
                tasks.append("implementierung")
        
        if any(word in desc_lower for word in ["integration", "kombination", "verbindung"]):
            if "integration" not in tasks:
                tasks.append("integration")
        
        if any(word in desc_lower for word in ["test", "prüfung", "validierung", "verifikation"]):
            if "test" not in tasks:
                tasks.append("test")
        
        # Jede Funktion braucht auch Dokumentation
        if "dokumentation" not in tasks:
            tasks.append("dokumentation")
        
        # Standardabschluss-Aufgabe
        if "bereitstellung" not in tasks:
            tasks.append("bereitstellung")
        
        return tasks
    
    def _sequence_tasks(self, tasks: List[Task]) -> List[Task]:
        """
        Ordnet Aufgaben zeitlich basierend auf Abhängigkeiten
        """
        # In diesem einfachen Modell: alle Aufgaben werden sequenziell abgearbeitet
        # mit minimalen Abhängigkeiten basierend auf der Namensgebung
        ordered_tasks = []
        
        # Gruppiere Aufgaben nach Feature
        feature_tasks = {}
        for task in tasks:
            feature_name = ' '.join(task.name.split(' - ')[:-1])  # Extrahiere Feature-Namen
            if feature_name not in feature_tasks:
                feature_tasks[feature_name] = []
            feature_tasks[feature_name].append(task)
        
        # Verarbeite Feature-Gruppen
        for feature_name, feature_task_list in feature_tasks.items():
            # Sortiere nach logischem Ablauf
            ordered_types = ["forschung", "analyse", "design", "implementierung", 
                            "integration", "test", "dokumentation", "bereitstellung"]
            
            sorted_tasks = []
            for task_type in ordered_types:
                for task in feature_task_list:
                    if task_type in task.name.lower():
                        sorted_tasks.append(task)
            
            # Füge sortierte Aufgaben hinzu
            ordered_tasks.extend(sorted_tasks)
        
        return ordered_tasks
    
    def _assign_dates(self, tasks: List[Task]) -> List[Task]:
        """
        Weist Aufgaben Start- und Enddaten zu
        """
        current_date = datetime.now()
        
        for task in tasks:
            task.start_date = current_date
            task.end_date = current_date + timedelta(weeks=task.duration)
            
            # Update des aktuellen Datums
            current_date = task.end_date
        
        return tasks
    
    def _schedule_with_resources(self, tasks: List[Task], 
                                resource_constraints: Dict[str, int]) -> List[Task]:
        """
        Plant Aufgaben unter Berücksichtigung von Ressourcenbeschränkungen
        """
        # In dieser Implementierung: Einfache Ressourcenplanung
        # Aktualisiert Dauer basierend auf verfügbaren Ressourcen
        scheduled_tasks = []
        current_date = datetime.now()
        
        for task in tasks:
            # Berechne benötigte verfügbare Ressourcen
            required_resources = task.resources
            
            # Prüfe, ob genügend Ressourcen verfügbar sind
            adjusted_duration = task.duration
            for resource_type, required_amount in required_resources.items():
                available = resource_constraints.get(resource_type, 0)
                if available > 0 and available < required_amount:
                    # Wenn nicht genügend Ressourcen verfügbar, verlängere die Dauer
                    adjustment_factor = required_amount / available
                    adjusted_duration = max(adjusted_duration, task.duration * adjustment_factor)
            
            # Erstelle die geplante Aufgabe mit angepasster Dauer
            scheduled_task = Task(
                name=task.name,
                description=task.description,
                duration=adjusted_duration,
                dependencies=task.dependencies,
                resources=task.resources
            )
            
            scheduled_task.start_date = current_date
            scheduled_task.end_date = current_date + timedelta(weeks=adjusted_duration)
            
            # Update des aktuellen Datums
            current_date = scheduled_task.end_date
            
            scheduled_tasks.append(scheduled_task)
        
        return scheduled_tasks
    
    def _create_milestones(self, tasks: List[Task]) -> List[Dict[str, Any]]:
        """
        Erstellt Meilensteine basierend auf den Aufgaben
        """
        milestones = []
        
        if not tasks:
            return milestones
        
        # Erster Meilenstein: Projektstart
        milestones.append({
            "name": "Projektstart",
            "date": tasks[0].start_date,
            "description": "Beginn der Projektarbeit"
        })
        
        # Meilensteine für Feature-Fertigstellung
        feature_names = set()
        for task in tasks:
            feature_name = ' '.join(task.name.split(' - ')[:-1])
            if feature_name not in feature_names:
                feature_names.add(feature_name)
                
                # Finde das Ende dieser Feature-Gruppe
                feature_end_date = task.end_date
                for future_task in tasks[tasks.index(task):]:
                    future_feature_name = ' '.join(future_task.name.split(' - ')[:-1])
                    if future_feature_name == feature_name:
                        feature_end_date = future_task.end_date
                    else:
                        break
                
                milestones.append({
                    "name": f"{feature_name} fertig",
                    "date": feature_end_date,
                    "description": f"Fertigstellung von {feature_name}"
                })
        
        # Letzter Meilenstein: Projektende
        milestones.append({
            "name": "Projektende",
            "date": tasks[-1].end_date,
            "description": "Abschluss der Projektarbeit"
        })
        
        return milestones
    
    def _calculate_project_duration(self, tasks: List[Task]) -> float:
        """
        Berechnet die Gesamtprojektdauer in Wochen
        """
        if not tasks:
            return 0.0
        
        total_duration = 0.0
        for task in tasks:
            total_duration += task.duration
        
        return total_duration
    
    def _analyze_resource_allocation(self, tasks: List[Task]) -> Dict[str, Any]:
        """
        Analysiert die Ressourcenallokation über das Projekt
        """
        resource_usage = {}
        
        for task in tasks:
            for resource_type, amount in task.resources.items():
                if resource_type not in resource_usage:
                    resource_usage[resource_type] = 0
                resource_usage[resource_type] += amount * task.duration  # Ressourcen-Wochen
        
        return {
            "total_resource_weeks": resource_usage,
            "peak_resource_needs": self._find_peak_resource_needs(tasks),
            "resource_efficiency": self._calculate_resource_efficiency(tasks)
        }
    
    def _find_peak_resource_needs(self, tasks: List[Task]) -> Dict[str, float]:
        """
        Findet den Höchststand an gleichzeitig benötigten Ressourcen
        """
        # In dieser einfachen Implementierung: Berechnung basierend auf sequenzieller Abarbeitung
        peak_needs = {}
        
        for task in tasks:
            for resource_type, amount in task.resources.items():
                if resource_type not in peak_needs or peak_needs[resource_type] < amount:
                    peak_needs[resource_type] = amount
        
        return peak_needs
    
    def _calculate_resource_efficiency(self, tasks: List[Task]) -> float:
        """
        Berechnet eine einfache Ressourceneffizienz
        """
        if not tasks:
            return 0.0
        
        total_resource_weeks = 0
        total_project_weeks = sum(task.duration for task in tasks)
        
        for task in tasks:
            for resource_type, amount in task.resources.items():
                total_resource_weeks += amount * task.duration
        
        if total_project_weeks == 0:
            return 0.0
        
        # Effizienz = Ressourcenwochen / Projektwochen
        return total_resource_weeks / total_project_weeks if total_project_weeks > 0 else 0.0

class ProjectPlanFormatter:
    """
    Formatierer für Projektplan gemäß Formatierungskonventionen
    """
    
    @staticmethod
    def format_project_plan(plan: Dict[str, Any]) -> str:
        """
        Formatierung des Projektplans im Standardformat
        """
        formatted_output = "## Projektzeitplan\n\n"
        
        formatted_output += f"**Projektstart**: {plan['project_start_date'].strftime('%d.%m.%Y') if plan['project_start_date'] else 'Nicht definiert'}\n"
        formatted_output += f"**Projektende**: {plan['project_end_date'].strftime('%d.%m.%Y') if plan['project_end_date'] else 'Nicht definiert'}\n"
        formatted_output += f"**Gesamtprojektdauer**: {plan['project_duration_weeks']:.1f} Wochen\n\n"
        
        formatted_output += "### Aufgaben:\n"
        for i, task in enumerate(plan['tasks'], 1):
            formatted_output += f"**Aufgabe {i}: {task.name}**\n"
            formatted_output += f"- Dauer: {task.duration:.1f} Wochen\n"
            formatted_output += f"- Start: {task.start_date.strftime('%d.%m.%Y') if task.start_date else 'Nicht definiert'}\n"
            formatted_output += f"- Ende: {task.end_date.strftime('%d.%m.%Y') if task.end_date else 'Nicht definiert'}\n"
            formatted_output += f"- Beschreibung: {task.description}\n"
            formatted_output += f"- Benötigte Ressourcen: {task.resources}\n\n"
        
        formatted_output += "### Meilensteine:\n"
        for milestone in plan['milestones']:
            formatted_output += f"- **{milestone['name']}** am {milestone['date'].strftime('%d.%m.%Y') if milestone['date'] else 'Nicht definiert'}: {milestone['description']}\n"
        
        formatted_output += "\n### Ressourcenanalyse:\n"
        formatted_output += f"- **Gesamt-Ressourcenwochen**: {plan['resource_allocation']['total_resource_weeks']}\n"
        formatted_output += f"- **Maximale Ressourcenbedarfe**: {plan['resource_allocation']['peak_resource_needs']}\n"
        formatted_output += f"- **Ressourceneffizienz**: {plan['resource_allocation']['resource_efficiency']:.2f}\n"
        
        return formatted_output

# Beispiel für die Verwendung
if __name__ == "__main__":
    planner = ProjectPlanner()
    formatter = ProjectPlanFormatter()
    
    # Beispiel-Features
    features = [
        {
            "name": "BiasHeatmap.jsx",
            "description": "Eine Komponente, die grafisch anzeigt, wo im Modell Bias-Werte > 0.5 auftreten. Sollte in < 100ms laden und interaktive Tooltips für spezifische Bias-Werte anzeigen."
        },
        {
            "name": "Wissenschaftliche Integration",
            "description": "Integration von mehreren wissenschaftlichen Modellen (Hall, GLOBE, Hofstede) zur umfassenden Bias-Analyse"
        }
    ]
    
    # Beispiel-Ressourcenbeschränkungen
    resource_constraints = {
        "developer": 2,
        "researcher": 1,
        "designer": 1,
        "tester": 1
    }
    
    project_plan = planner.create_project_plan(features, resource_constraints)
    formatted_plan = formatter.format_project_plan(project_plan)
    
    print("Projektplan:")
    print(formatted_plan)