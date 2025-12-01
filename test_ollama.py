#!/usr/bin/env python3
"""
Test script for Ollama integration with the brainstorming skill.
"""
import sys
import os

# Add the project root to the path so we can import the skill
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from brainstorming_skill.config.ollama_config import validate_ollama_config
from brainstorming_skill.src.skill import execute_brainstorm_skill
import requests

def test_ollama_connection():
    """
    Test if Ollama server is accessible.
    """
    try:
        # Try to get the list of models
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            print("✓ Ollama server is accessible")
            models = response.json().get("models", [])
            model_names = [model.get("name", "") for model in models]
            print(f"Available models: {model_names[:5]}...")  # Show first 5 models
            return True
        else:
            print(f"✗ Ollama server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to Ollama server at http://localhost:11434")
        print("Please make sure Ollama is running with 'ollama serve'")
        return False
    except Exception as e:
        print(f"✗ Error connecting to Ollama: {e}")
        return False

def test_brainstorm_skill_with_ollama():
    """
    Test the brainstorming skill with Ollama as the LLM provider.
    """
    # Check if Ollama server is running
    if not test_ollama_connection():
        print("Cannot test Ollama integration - server not accessible")
        return False

    # Sample input based on the skill specification
    inputs = {
        "idea": "Eine App, die Pflanzen anhand von Fotos erkennt und Pflegetipps gibt",
        "context": "Mobile Anwendung für Hobbygärtner, React Native, Offline-First Ansatz",
        "focus": "allgemein",
        "round_info": "Erste Iteration"
    }
    
    print("\nTesting brainstorming skill with Ollama...")
    print(f"Input: {inputs}")
    
    try:
        # Set environment to use Ollama (these are now loaded from .env file)
        # Execute the skill with Ollama (not using mock)
        outputs = execute_brainstorm_skill(inputs, use_mock=False)

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

        print("\nSkill executed successfully with Ollama!")
        return True
        
    except Exception as e:
        print(f"Error executing skill with Ollama: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Ollama Integration...")
    
    # Validate the Ollama configuration
    import os
    from dotenv import load_dotenv
    load_dotenv("/home/dyai/Dokumente/DYAI_home/DEV/GIT_repos/Brainstorm_LLM/brainstorming_skill/.env")

    # Now check the model from environment
    model = os.getenv("LLM_MODEL", "llama3.2:latest")
    print(f"Using model from environment: {model}")

    # Validate the Ollama configuration
    from brainstorming_skill.config.ollama_config import validate_ollama_config
    config_valid = validate_ollama_config()

    if config_valid:
        success = test_brainstorm_skill_with_ollama()
        if success:
            print("\nOllama integration test completed successfully!")
        else:
            print("\nOllama integration test failed!")
            sys.exit(1)
    else:
        print("\nOllama configuration is not valid!")
        sys.exit(1)