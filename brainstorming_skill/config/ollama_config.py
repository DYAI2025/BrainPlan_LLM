"""
Configuration for Ollama integration
"""
import os

# Ollama-specific settings
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"

# Request timeout in seconds
OLLAMA_TIMEOUT = 300  # 5 minutes

# Model parameters
OLLAMA_TEMPERATURE = 0.7
OLLAMA_TOP_P = 0.9
OLLAMA_MAX_TOKENS = 4096

# Available Ollama models for brainstorming
OLLAMA_SUPPORTED_MODELS = [
    "llama3.2:latest",
    "llama3.2:8b",
    "llama3.1:8b",
    "mistral:7b",
    "codellama:7b",
    "phi:3b"
]

def validate_ollama_config():
    """
    Validate the Ollama configuration.
    """
    if OLLAMA_MODEL not in OLLAMA_SUPPORTED_MODELS:
        print(f"Warning: {OLLAMA_MODEL} is not in the list of supported models")
        print(f"Supported models: {OLLAMA_SUPPORTED_MODELS}")

    # Test connection to Ollama server
    try:
        import requests
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model.get("name", "") for model in models]
            if OLLAMA_MODEL in model_names:
                print(f"✓ Ollama server is running and model {OLLAMA_MODEL} is available")
                return True
            else:
                print(f"⚠ Model {OLLAMA_MODEL} not found on Ollama server")
                print(f"Available models: {model_names}")
                return False
        else:
            print(f"⚠ Could not connect to Ollama server at {OLLAMA_URL}")
            return False
    except requests.RequestException as e:
        print(f"⚠ Could not connect to Ollama server at {OLLAMA_URL}: {e}")
        return False