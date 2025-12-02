"""
Constraint-Analyzer für den erweiterten Brainstorming-Skill
"""
from typing import Dict, Any, List
import re

class ConstraintAnalyzer:
    """
    Analysiert Ressourcen und Einschränkungen für Projekte und Anforderungen
    """
    
    def __init__(self):
        # Basisschätzungen für verschiedene Aufgabentypen
        self.time_multipliers = {
            "datenintegration": 1.5,
            "künstliche_intelligenz": 1.8,
            "wissenschaftliche_analyse": 2.2,
            "visualisierung": 1.2,
            "schnittstelle": 1.0,
            "dokumentation": 0.5
        }
        
        self.resource_requirements = {
            "datenintegration": {"personal": 1, "rechenzeit": 2, "speicher": 2},
            "künstliche_intelligenz": {"personal": 2, "rechenzeit": 5, "speicher": 4},
            "wissenschaftliche_analyse": {"personal": 1, "rechenzeit": 3, "speicher": 3},
            "visualisierung": {"personal": 1, "rechenzeit": 1, "speicher": 1},
            "schnittstelle": {"personal": 1, "rechenzeit": 0.5, "speicher": 0.5}
        }
    
    def analyze_resources(self, task_description: str) -> Dict[str, Any]:
        """
        Schätzt benötigte Ressourcen basierend auf der Aufgabenbeschreibung
        """
        # Klassifiziere die Aufgaben nach Typ
        task_types = self._classify_task_types(task_description)
        
        # Schätze Ressourcen basierend auf Aufgabentypen
        resources = {
            "time_estimate": self.estimate_time(task_description, task_types),
            "budget_estimate": self.estimate_budget(task_description, task_types),
            "technical_resources": self.estimate_technical_resources(task_description, task_types),
            "personnel": self.estimate_personnel(task_description, task_types)
        }
        
        return resources
    
    def _classify_task_types(self, description: str) -> List[str]:
        """
        Klassifiziert die Aufgaben in verschiedene Typen basierend auf der Beschreibung
        """
        description_lower = description.lower()
        task_types = []
        
        # Muster für verschiedene Aufgabentypen
        patterns = {
            "datenintegration": [
                "daten", "integration", "import", "export", "schnittstelle", "api", 
                "quelle", "transformation", "migration", "kuration"
            ],
            "künstliche_intelligenz": [
                "künstliche intelligenz", "ki", "ai", "ml", "machine learning", 
                "lernen", "model", "algorithmus", "training", "predict", "vorhersage"
            ],
            "wissenschaftliche_analyse": [
                "wissenschaftlich", "forschung", "analyse", "studie", "kennzahl", 
                "theorie", "modell", "framework", "methodik", "statistik", "benchmark"
            ],
            "visualisierung": [
                "visualisierung", "grafik", "anzeige", "heatmap", "diagramm", 
                "interface", "ui", "ux", "chart", "darstellung", "grafisch"
            ],
            "schnittstelle": [
                "schnittstelle", "interface", "verbindung", "kommunikation", 
                "integration", "anbindung", "verknüpfung"
            ],
            "dokumentation": [
                "dokumentation", "doku", "anleitung", "handbuch", "erklärung", 
                "spezifikation", "beschreibung"
            ]
        }
        
        for task_type, keywords in patterns.items():
            for keyword in keywords:
                if keyword in description_lower:
                    if task_type not in task_types:
                        task_types.append(task_type)
                    break
        
        return task_types
    
    def estimate_time(self, description: str, task_types: List[str]) -> Dict[str, float]:
        """
        Schätzt die benötigte Zeit basierend auf Aufgabentypen
        """
        base_time = 2.0  # Basiszeit in Wochen
        complexity_factor = 1.0
        
        for task_type in task_types:
            if task_type in self.time_multipliers:
                complexity_factor *= self.time_multipliers[task_type]
        
        # Berücksichtige Komplexitätswörter
        complexity_indicators = ["mehrere", "kombiniert", "integration", "vielfältig", "komplex"]
        for indicator in complexity_indicators:
            if indicator in description.lower():
                complexity_factor *= 1.3
        
        final_time = base_time * complexity_factor
        
        # Erstelle detaillierte Zeitschätzung
        time_breakdown = {
            "research": final_time * 0.3,  # 30% Forschung/Analyse
            "development": final_time * 0.5,  # 50% Entwicklung
            "testing": final_time * 0.2,  # 20% Testen
            "total": final_time
        }
        
        return time_breakdown
    
    def estimate_budget(self, description: str, task_types: List[str]) -> float:
        """
        Schätzt den Budgetbedarf in EUR
        """
        # Basisbudget pro Woche
        base_weekly_budget = 8000  # EUR für 1 Entwickler
        
        time_estimate = self.estimate_time(description, task_types)
        total_time = time_estimate["total"]
        
        # Berücksichtige besondere Ressourcen
        special_resources = 0
        if "künstliche_intelligenz" in task_types:
            special_resources += 5000  # Zusätzliche Kosten für GPU-Zeit
        if "wissenschaftliche_analyse" in task_types:
            special_resources += 3000  # Zusätzliche Kosten für externe Expertise
        
        return (total_time * base_weekly_budget) + special_resources
    
    def estimate_technical_resources(self, description: str, task_types: List[str]) -> Dict[str, Any]:
        """
        Schätzt technische Ressourcen wie Rechenleistung, Speicher, etc.
        """
        resources = {
            "cpu": 0,
            "memory": 0,
            "storage": 0,
            "gpu": 0,
            "network": 0
        }
        
        # Summiere Anforderungen basierend auf Aufgabentypen
        for task_type in task_types:
            if task_type in self.resource_requirements:
                reqs = self.resource_requirements[task_type]
                for resource, value in reqs.items():
                    if resource in resources:
                        resources[resource] += value
        
        # Skaliere Werte auf realistische Größen
        resources["cpu"] = max(1, resources["cpu"])  # Mindestens 1 CPU
        resources["memory"] = resources["memory"] * 4  # in GB
        resources["storage"] = resources["storage"] * 10  # in GB
        resources["gpu"] = 1 if "künstliche_intelligenz" in task_types else 0
        resources["network"] = 1  # Basis-Netzwerkzugang
        
        return resources
    
    def estimate_personnel(self, description: str, task_types: List[str]) -> Dict[str, int]:
        """
        Schätzt den Personalbedarf
        """
        personnel = {
            "developers": 1,  # Mindestens 1 Entwickler
            "researchers": 0,
            "designers": 0,
            "testers": 0,
            "project_managers": 1
        }
        
        if "wissenschaftliche_analyse" in task_types:
            personnel["researchers"] = 1
        
        if "visualisierung" in task_types:
            personnel["designers"] = 1
        
        if "künstliche_intelligenz" in task_types:
            personnel["researchers"] = max(1, personnel["researchers"])
        
        # Schätzung der Gesamtstunden
        time_estimate = self.estimate_time(description, task_types)
        total_weeks = time_estimate["total"]
        
        total_personnel_hours = sum(personnel.values()) * total_weeks * 40  # 40h/Woche
        
        personnel["total_personnel_hours"] = total_personnel_hours
        
        return personnel

# Beispiel für die Verwendung
if __name__ == "__main__":
    analyzer = ConstraintAnalyzer()
    
    task = "Integration von mehreren wissenschaftlichen Modellen (Hall, GLOBE, Hofstede) mit visueller Darstellung als Heatmap"
    
    resources = analyzer.analyze_resources(task)
    
    print("Ressourcenanalyse:")
    print(f"Zeitschätzung: {resources['time_estimate']}")
    print(f"Budgetschätzung: {resources['budget_estimate']:.2f} EUR")
    print(f"Technische Ressourcen: {resources['technical_resources']}")
    print(f"Personalbedarf: {resources['personnel']}")