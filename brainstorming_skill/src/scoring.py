from dataclasses import dataclass
from typing import Dict

@dataclass
class Thought:
    id: str
    summary: str
    criteria_scores: Dict[str, float]  # 10 Kriterien
    total_score: float

# Weight distribution based on the original Brainstorm_LLM project
WEIGHTS = {
    "Zielerreichung": 0.15,      # Goal achievement
    "Machbarkeit": 0.12,          # Feasibility
    "Aufwand": 0.12,              # Effort
    "Wartbarkeit": 0.11,          # Maintainability
    "Risiko": 0.11,               # Risk
    "ROI": 0.10,                  # Return on Investment
    "Innovation": 0.08,           # Innovation
    "Sicherheit": 0.08,           # Security
    "Team-Fit": 0.07,             # Team fit
    "UX": 0.06,                   # User Experience
}

def calculate_total_score(thought: Thought) -> float:
    """
    Calculate the total score for a thought based on weighted criteria.
    """
    return sum(
        score * WEIGHTS.get(name, 0.0) 
        for name, score in thought.criteria_scores.items()
    )

def validate_criteria_scores(scores: Dict[str, float]) -> bool:
    """
    Validate that all required criteria are present and scores are within range.
    """
    required_criteria = set(WEIGHTS.keys())
    provided_criteria = set(scores.keys())
    
    if required_criteria != provided_criteria:
        missing = required_criteria - provided_criteria
        extra = provided_criteria - required_criteria
        if missing or extra:
            print(f"Warning: Missing criteria: {missing}, Extra criteria: {extra}")
            return False
    
    for name, score in scores.items():
        if not 1 <= score <= 10:
            print(f"Warning: Score for {name} is out of range [1,10]: {score}")
            return False
    
    return True