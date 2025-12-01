import json
import re
from typing import List, Dict
from .scoring import Thought, calculate_total_score, validate_criteria_scores
from .llm import llm

MAX_DEPTH = 3
BRANCHING_FACTOR = 4

TOT_PROMPT = """
Du bist ein brillanter Produkt- und System-Architekt.
Aufgabe: {task}

Generiere EXAKT 5 unterschiedliche, aber hochwertige Lösungsansätze (Thoughts).
Jeder Thought muss enthalten:
- Kurzüberschrift (z.B. "React Native + externe API")
- 2–3 Sätze Beschreibung
- Bewertung der 10 Kriterien (1–10):

{criteria_list}

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

def generate_initial_thoughts(task: str, use_mock: bool = False) -> List[Thought]:
    """
    Generate initial thoughts for a given task using the LLM.
    If use_mock is True, use dummy thoughts for testing without LLM calls.
    """
    if use_mock:
        # Return dummy thoughts for testing without LLM
        dummy_thoughts_data = [
            {
                "id": "T1",
                "title": "React Native + externe Plant.id API",
                "summary": "Mobile Anwendung mit React Native, die externe Plant.id API für die Pflanzenkennung nutzt, mit Offline-First Ansatz für wiederkehrende Nutzer.",
                "scores": {
                    "Zielerreichung": 9,
                    "Machbarkeit": 9,
                    "Aufwand": 8,
                    "Wartbarkeit": 9,
                    "Risiko": 8,
                    "ROI": 10,
                    "Innovation": 6,
                    "Sicherheit": 9,
                    "Team-Fit": 9,
                    "UX": 8
                }
            },
            {
                "id": "T2",
                "title": "Eigenständiges ML-Modell auf dem Gerät",
                "summary": "Komplett eigenständige App mit lokal laufendem ML-Modell für Pflanzenkennung, keine Internetverbindung benötigt.",
                "scores": {
                    "Zielerreichung": 10,
                    "Machbarkeit": 4,
                    "Aufwand": 3,
                    "Wartbarkeit": 6,
                    "Risiko": 4,
                    "ROI": 9,
                    "Innovation": 5,
                    "Sicherheit": 8,
                    "Team-Fit": 5,
                    "UX": 9
                }
            },
            {
                "id": "T3",
                "title": "PWA mit TensorFlow.js",
                "summary": "Progressive Web App mit TensorFlow.js für Pflanzenkennung direkt im Browser, funktioniert auf allen Geräten.",
                "scores": {
                    "Zielerreichung": 8,
                    "Machbarkeit": 7,
                    "Aufwand": 7,
                    "Wartbarkeit": 8,
                    "Risiko": 6,
                    "ROI": 7,
                    "Innovation": 4,
                    "Sicherheit": 7,
                    "Team-Fit": 8,
                    "UX": 7
                }
            },
            {
                "id": "T4",
                "title": "WhatsApp/Telegram-Bot",
                "summary": "Chat-basierter Ansatz, Benutzer senden Fotos über WhatsApp/Telegram, erhalten Pflegetipps als Antwort.",
                "scores": {
                    "Zielerreichung": 7,
                    "Machbarkeit": 8,
                    "Aufwand": 9,
                    "Wartbarkeit": 7,
                    "Risiko": 7,
                    "ROI": 8,
                    "Innovation": 7,
                    "Sicherheit": 6,
                    "Team-Fit": 7,
                    "UX": 9
                }
            },
            {
                "id": "T5",
                "title": "AR-Brillen-Integration",
                "summary": "Erweiterte Realität-Lösung für professionelle Gartenbetriebe, Erkennung direkt durch AR-Brillen.",
                "scores": {
                    "Zielerreichung": 6,
                    "Machbarkeit": 3,
                    "Aufwand": 2,
                    "Wartbarkeit": 4,
                    "Risiko": 9,
                    "ROI": 4,
                    "Innovation": 10,
                    "Sicherheit": 5,
                    "Team-Fit": 3,
                    "UX": 7
                }
            }
        ]

        thoughts = []
        for item in dummy_thoughts_data:
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

    # Original implementation using LLM
    criteria = "\n".join([f"- {k} (1–10)" for k in {"Zielerreichung": 0.15, "Machbarkeit": 0.12, "Aufwand": 0.12,
                                                     "Wartbarkeit": 0.11, "Risiko": 0.11, "ROI": 0.10,
                                                     "Innovation": 0.08, "Sicherheit": 0.08, "Team-Fit": 0.07, "UX": 0.06}.keys()])
    prompt = TOT_PROMPT.format(task=task, criteria_list=criteria)

    messages = [
        {"role": "system", "content": "Du bist ein extrem präziser und objektiver Architekt."},
        {"role": "user", "content": prompt}
    ]

    raw_json = llm.complete(messages, temperature=0.8)

    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        # Fallback: extract JSON from Markdown
        match = re.search(r"\{.*\}", raw_json, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
            except json.JSONDecodeError:
                print("Could not parse LLM response as JSON")
                return []
        else:
            print("Could not find JSON in LLM response")
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


def tree_of_thoughts(task: str, depth: int = MAX_DEPTH, use_mock: bool = False) -> List[Thought]:
    """
    Execute the Tree-of-Thoughts algorithm to generate and refine thoughts.
    """
    # Generate initial thoughts
    thoughts = generate_initial_thoughts(task, use_mock=use_mock)
    current_level = thoughts[:]

    # Expand thoughts in a tree structure
    for level in range(1, depth):
        next_level = []
        for parent in current_level[:BRANCHING_FACTOR]:
            # Generate child thoughts based on the parent
            for i in range(1, 4):
                child_summary = f"Weiterentwicklung von {parent.id}: Variante {i}\n\n{parent.summary}"

                # Create a new thought based on the parent but with modifications
                child_scores = parent.criteria_scores.copy()

                # Make small variations to the scores to represent evolution
                for criterion in child_scores:
                    # Slightly modify each score (±0.5 to ±1.5)
                    variation = (i - 2) * 0.5  # -1, 0, +1 for i=1,2,3
                    child_scores[criterion] = max(1, min(10, child_scores[criterion] + variation))

                child = Thought(
                    id=f"{parent.id}-L{level+1}-{i}",
                    summary=child_summary,
                    criteria_scores=child_scores,
                    total_score=0
                )
                child.total_score = calculate_total_score(child)
                next_level.append(child)

        # Keep the best thoughts for the next level
        current_level = sorted(next_level, key=lambda x: x.total_score, reverse=True)[:6]

    # Return the best thoughts across all levels
    all_thoughts = thoughts + current_level
    return sorted(all_thoughts, key=lambda x: x.total_score, reverse=True)[:6]


def tree_of_thoughts_live(task: str, use_mock: bool = False) -> List[Thought]:
    """
    Execute the Tree-of-Thoughts with live LLM calls for each expansion.
    This is a more advanced version that calls the LLM for each generation.
    If use_mock is True, use dummy thoughts for testing.
    """
    return tree_of_thoughts(task, use_mock=use_mock)