import json
import requests
from typing import List, Dict, Any
from .scoring import Thought

class OllamaClient:
    """
    A client specifically for interacting with Ollama models locally.
    """
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "llama3.2:8b"  # Default model, can be changed
        
    def set_model(self, model_name: str):
        """
        Set the model to use for Ollama.
        """
        self.model = model_name
    
    def complete(self, messages: List[Dict], temperature: float = 0.7) -> str:
        """
        Send a completion request to the Ollama API.
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/chat", json=payload)
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"]
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama API: {e}")
            raise
        except KeyError as e:
            print(f"Unexpected response structure from Ollama: {e}")
            print(f"Response: {response.json()}")
            raise

    def generate_initial_thoughts(self, task: str) -> List[Thought]:
        """
        Generate initial thoughts using Ollama.
        """
        from .scoring import calculate_total_score, validate_criteria_scores
        from .llm import WEIGHTS
        
        criteria = "\n".join([f"- {k} (1–10)" for k in WEIGHTS.keys()])
        prompt = f"""
Du bist ein brillanter Produkt- und System-Architekt.
Aufgabe: {task}

Generiere EXAKT 5 unterschiedliche, aber hochwertige Lösungsansätze (Thoughts).
Jeder Thought muss enthalten:
- Kurzüberschrift (z.B. "React Native + externe API")
- 2–3 Sätze Beschreibung
- Bewertung der 10 Kriterien (1–10):

{criteria}

Antworte NUR im folgenden JSON-Format:
{{
  "thoughts": [
    {{
      "id": "T1",
      "title": "...",
      "summary": "...",
      "scores": {{"Zielerreichung": 9, "Machbarkeit": 8, ...}}
    }}
  ]
}}
        """

        messages = [
            {"role": "system", "content": "Du bist ein extrem präziser und objektiver Architekt."},
            {"role": "user", "content": prompt}
        ]

        raw_json = self.complete(messages, temperature=0.8)

        try:
            data = json.loads(raw_json)
        except json.JSONDecodeError:
            # Fallback: extract JSON from Markdown or text
            import re
            match = re.search(r"\{.*\}", raw_json, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(0))
                except json.JSONDecodeError:
                    print("Could not parse Ollama response as JSON")
                    return []
            else:
                print("Could not find JSON in Ollama response")
                return []

        thoughts = []
        for item in data.get("thoughts", []):
            # Validate the scores before creating the Thought
            if not validate_criteria_scores(item["scores"]):
                print(f"Invalid scores for thought {item['id']}, skipping...")
                continue
                
            thought = Thought(
                id=item["id"],
                summary=f"{item['title']}\n\n{item.get('summary', '')}",
                criteria_scores=item["scores"],
                total_score=0
            )
            thought.total_score = calculate_total_score(thought)
            thoughts.append(thought)

        return sorted(thoughts, key=lambda x: x.total_score, reverse=True)[:6]

    def classify_relations(self, thoughts: List[Thought]) -> List[Dict]:
        """
        Classify relationships between thoughts using Ollama.
        """
        thoughts_info = []
        for thought in thoughts:
            thoughts_info.append({
                "id": thought.id,
                "summary": thought.summary[:200]  # Truncate for prompt efficiency
            })
        
        relation_prompt = f"""
Hier sind {len(thoughts_info)} Lösungsansätze:
{json.dumps(thoughts_info, indent=2, ensure_ascii=False)}

Für jedes Paar (i,j) mit i < j bestimme:
- Die Beziehung: ergänzt | widerspricht | abhängig_von | kombinierbar | besser_als
- Die Stärke: 1–5

Antworte NUR als JSON-Array von Objekten mit diesen Feldern:
- "from": ID des ersten Thoughts
- "to": ID des zweiten Thoughts
- "relation": die Beziehung
- "strength": 1-5

Format:
[
  {{
    "from": "T1",
    "to": "T2",
    "relation": "kombinierbar",
    "strength": 4
  }}
]
        """

        messages = [
            {"role": "system", "content": "Du bist ein präziser Analyst für Lösungsansätze."},
            {"role": "user", "content": relation_prompt}
        ]

        raw_json = self.complete(messages, temperature=0.3)
        
        try:
            relations = json.loads(raw_json)
        except json.JSONDecodeError:
            # Fallback: extract JSON from response
            import re
            match = re.search(r"\[.*\]", raw_json, re.DOTALL)
            if match:
                try:
                    relations = json.loads(match.group(0))
                except json.JSONDecodeError:
                    print("Could not parse relation classification as JSON")
                    return []
            else:
                print("Could not find relation classification in response")
                return []
        
        return relations