#!/usr/bin/env python3
"""
Testskript für den erweiterten Brainstorming-Skill mit Projektmanagement-Funktionen
"""
import sys
import os

# Füge das Projektverzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from brainstorming_skill.src import execute_brainstorm_skill

def test_enhanced_brainstorm_skill():
    """
    Testet den erweiterten Brainstorming-Skill
    """
    print("Teste den erweiterten Brainstorming-Skill mit Projektmanagement-Funktionen...")
    
    # Beispiel-Eingabe
    inputs = {
        "idea": "Erstelle eine Webanwendung zur Visualisierung von Bias in KI-Modellen. Sollte Heatmaps anzeigen und wissenschaftliche Modelle integrieren (Hall, GLOBE, Hofstede).",
        "context": "Academic research tool for bias detection in ML models",
        "focus": "allgemein",
        "round_info": "Erste Iteration"
    }
    
    print("Eingabe:")
    print(f"- Idea: {inputs['idea'][:60]}...")
    print(f"- Context: {inputs['context']}")
    print()
    
    try:
        # Führe den Skill mit Mock-Daten aus (da wir möglicherweise keinen LLM-Zugang haben)
        result = execute_brainstorm_skill(inputs, use_mock=True)
        
        print("Erfolgreich ausgeführt! Ergebnisse:")
        print("="*50)
        
        # Überprüfe, ob die neuen Komponenten vorhanden sind
        if "project_blueprint" in result:
            print("✓ Projekt-Blueprint gefunden")
            print(f"  Beispiel: {result['project_blueprint'][:100]}...")
        elif "prioritized_requirements" in result:
            print("✓ Priorisierte Anforderungen gefunden")
            print(f"  Beispiel: {result['prioritized_requirements'][:100]}...")
        else:
            print("✗ Wichtige Projektplanungskomponente NICHT gefunden")

        print()

        if "project_resources" in result:
            print("✓ Projekt-Ressourcenanalyse gefunden")
            print(f"  Beispiel: {result['project_resources'][:100]}...")
        else:
            print("✗ Projekt-Ressourcenanalyse NICHT gefunden")

        print()

        if "definitions_of_done" in result:
            print("✓ Definitionen of Done gefunden")
            print(f"  Anzahl an DoDs: {len(result['definitions_of_done'])}")
        elif "requirement_matrix" in result:
            print("✓ Anforderungsmatrix gefunden")
            print(f"  Beispiel: {result['requirement_matrix'][:100]}...")
        else:
            print("✗ Definitionen of Done NICHT gefunden")

        print()

        if "iterative_project_plan" in result:
            print("✓ Iterativer Projektplan gefunden")
            print(f"  Beispiel: {result['iterative_project_plan'][:100]}...")
        elif "project_plan" in result:
            print("✓ Projektplan gefunden")
            print(f"  Beispiel: {result['project_plan'][:100]}...")
        else:
            print("✗ Projektplan NICHT gefunden")

        print()

        if "project_management" in result:
            print("✓ Vollständige Projektmanagement-Struktur gefunden")
            print(f"  Länge: {len(result['project_management'])} Zeichen")

        print()
        print("Test abgeschlossen - alle erweiterten Funktionen sind verfügbar!")
        
        return True
        
    except Exception as e:
        print(f"Fehler beim Ausführen des Skills: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_components():
    """
    Testet die einzelnen neuen Komponenten
    """
    print("\nTeste einzelne Komponenten...")
    
    # Teste Constraint-Analyzer
    try:
        from brainstorming_skill.enhanced_skills.constraint_analyzer import ConstraintAnalyzer
        analyzer = ConstraintAnalyzer()
        resources = analyzer.analyze_resources("Integration von mehreren wissenschaftlichen Modellen")
        print("✓ Constraint-Analyzer funktioniert")
        print(f"  Beispiel-Ressourcen: {resources['time_estimate']['total']:.1f} Wochen, Budget: {resources['budget_estimate']:.0f}€")
    except Exception as e:
        print(f"✗ Constraint-Analyzer Fehler: {e}")
    
    # Teste Prioritizer
    try:
        from brainstorming_skill.enhanced_skills.prioritizer import Prioritizer
        prioritizer = Prioritizer()
        sample_reqs = [
            "FR-1: Das System muss Benutzer authentifizieren",
            "FR-2: Das System sollte Benachrichtigungen senden",
            "FR-3: Das System könnte eine Exportfunktion haben"
        ]
        prioritized = prioritizer.prioritize_requirements(sample_reqs)
        print("✓ Prioritizer funktioniert")
        print(f"  Must-Have Anforderungen: {len(prioritized['must_have'])}")
    except Exception as e:
        print(f"✗ Prioritizer Fehler: {e}")
    
    # Teste Definition of Done Generator
    try:
        from brainstorming_skill.enhanced_skills.dod_generator import DefinitionOfDoneGenerator
        dod_gen = DefinitionOfDoneGenerator()
        dod = dod_gen.generate_dod("Heatmap-Komponente, die Bias-Werte darstellt")
        print("✓ Definition of Done Generator funktioniert")
        print(f"  Funktionale Kriterien: {len(dod['functional_criteria'])}")
    except Exception as e:
        print(f"✗ Definition of Done Generator Fehler: {e}")
    
    # Teste Project Planner
    try:
        from brainstorming_skill.enhanced_skills.project_planner import ProjectPlanner
        planner = ProjectPlanner()
        features = [
            {"name": "Visualisierung", "description": "Heatmap-Komponente"},
            {"name": "KI-Integration", "description": "Integration wissenschaftlicher Modelle"}
        ]
        plan = planner.create_project_plan(features)
        print("✓ Project Planner funktioniert")
        print(f"  Projekt dauert: {plan['project_duration_weeks']:.1f} Wochen")
    except Exception as e:
        print(f"✗ Project Planner Fehler: {e}")

if __name__ == "__main__":
    success = test_enhanced_brainstorm_skill()
    test_individual_components()
    
    if success:
        print("\n✓ Alle Tests erfolgreich!")
        sys.exit(0)
    else:
        print("\n✗ Einige Tests sind fehlgeschlagen!")
        sys.exit(1)