#!/usr/bin/env python3
"""
Simple test script for the brainstorming skill.
"""
import sys
import os

# Add the project root to the path so we can import the skill
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Import the skill function
from brainstorming_skill.src.skill import execute_brainstorm_skill

def test_brainstorm_skill():
    """
    Test the brainstorming skill with a simple input.
    """
    # Sample input based on the skill specification
    inputs = {
        "idea": "Eine App, die Pflanzen anhand von Fotos erkennt und Pflegetipps gibt",
        "context": "Mobile Anwendung für Hobbygärtner, React Native, Offline-First Ansatz",
        "focus": "allgemein",
        "round_info": "Erste Iteration"
    }

    print("Testing brainstorming skill...")
    print(f"Input: {inputs}")

    try:
        outputs = execute_brainstorm_skill(inputs, use_mock=True)

        print("\nOutput:")
        print(f"Problem Statement: {outputs['problem_statement'][:100]}...")
        print(f"Goals & KPIs: {outputs['goals_kpis'][:100]}...")
        print(f"Functional Requirements: {outputs['functional_requirements'][:100]}...")
        print(f"Non-functional Requirements: {outputs['nonfunctional_requirements'][:100]}...")
        print(f"Risks & Assumptions: {outputs['risks_assumptions'][:100]}...")
        print(f"Implementation Potential: {outputs['implementation_potential'][:100]}...")
        print(f"Task List: {outputs['task_list'][:100]}...")
        print(f"Test Ideas: {outputs['test_ideas'][:100]}...")
        print(f"Planner Prompt: {outputs['followup_prompts']['prompt_planner'][:100]}...")
        print(f"Architect Prompt: {outputs['followup_prompts']['prompt_architect'][:100]}...")
        print(f"Dev Prompt: {outputs['followup_prompts']['prompt_dev'][:100]}...")

        print("\nSkill executed successfully!")
        return True

    except Exception as e:
        print(f"Error executing skill: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_brainstorm_skill()
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")
        sys.exit(1)