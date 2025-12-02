"""
Prioritizer für den erweiterten Brainstorming-Skill
Implementiert die MoSCoW-Methode zur Priorisierung von Anforderungen
"""
from typing import List, Dict, Any
import re

class Prioritizer:
    """
    Implementiert die MoSCoW-Methode zur Priorisierung von Anforderungen
    MoSCoW steht für:
    - M: Must have (unbedingt notwendig)
    - S: Should have (wichtig, aber nicht kritisch)
    - C: Could have (wäre schön, wenn möglich)
    - W: Won't have (this time) - nicht in dieser Iteration
    """
    
    def __init__(self):
        # Wichtige Keywords für die Kategorisierung
        self.must_keywords = [
            "muss", "notwendig", "erforderlich", "wesentlich", "grundlegend", 
            "zentral", "kern", "kritisch", "essenziell", "unbedingt", "voraussetzung",
            "rechtlich", "gesetzlich", "sicherheit", "zugänglichkeit", "kompatibilität"
        ]
        
        self.should_keywords = [
            "sollte", "wichtig", "bedeutend", "vorteilhaft", "empfehlenswert",
            "sinnvoll", "wünschenswert", "hilfreich", "nützlich", "relevant",
            "benutzerfreundlichkeit", "performance", "skalierbarkeit"
        ]
        
        self.could_keywords = [
            "könnte", "optional", "schön", "nettes", "zusätzlich", "ergänzend",
            "nice to have", "wäre toll", "wäre gut", "interessant", "kreativ",
            "innovativ", "exzellent", "perfektion", "erweiterung"
        ]
        
        self.wont_keywords = [
            "nicht jetzt", "später", "zukunft", "phase 2", "nächste iteration",
            "nicht priorisiert", "niedrige priorität", "langfristig"
        ]
    
    def prioritize_requirements(self, requirements_list: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Klassifiziert Anforderungen nach der MoSCoW-Methode
        """
        prioritized = {
            "must_have": [],
            "should_have": [],
            "could_have": [],
            "wont_have": []
        }
        
        for req in requirements_list:
            category = self.classify_requirement(req)
            prioritized[category].append({
                "requirement": req,
                "confidence": self.estimate_confidence(req, category)
            })
        
        return prioritized
    
    def classify_requirement(self, requirement: str) -> str:
        """
        Klassifiziert eine Anforderung in eine MoSCoW-Kategorie
        """
        req_lower = requirement.lower()
        
        # Zähle Keywords für jede Kategorie
        must_count = sum(1 for keyword in self.must_keywords if keyword in req_lower)
        should_count = sum(1 for keyword in self.should_keywords if keyword in req_lower)
        could_count = sum(1 for keyword in self.could_keywords if keyword in req_lower)
        wont_count = sum(1 for keyword in self.wont_keywords if keyword in req_lower)
        
        # Prüfe auch auf spezifische Muster
        if self._is_must_pattern(requirement):
            return "must_have"
        elif self._is_should_pattern(requirement):
            return "should_have"
        elif self._is_could_pattern(requirement):
            return "could_have"
        elif self._is_wont_pattern(requirement):
            return "wont_have"
        
        # Wenn keine spezifischen Muster zutreffen, verwende Keyword-Zählung
        max_count = max(must_count, should_count, could_count, wont_count)
        
        if max_count == 0:
            # Wenn keine Keywords gefunden wurden, Standardkategorisierung
            return self._default_classification(requirement)
        elif must_count == max_count:
            return "must_have"
        elif should_count == max_count:
            return "should_have"
        elif could_count == max_count:
            return "could_have"
        else:  # wont_count == max_count
            return "wont_have"
    
    def _is_must_pattern(self, req: str) -> bool:
        """
        Prüft auf spezifische Muster für "Must have"-Anforderungen
        """
        patterns = [
            r"mus[sn]\s",  # "muss", "muß"
            r"zwingend.*erforderlich",
            r"unbedingt.*notwendig",
            r"rechtliche.*anforderung",
            r"sicherheits.*anforderung",
            r"gesetzlich.*vorgeschrieben",
            r"zugänglichkeits.*anforderung",
            r"grund.*funktionalität",
            r"kern.*funktion",
            r"voraussetzung.*für"
        ]
        
        req_lower = req.lower()
        for pattern in patterns:
            if re.search(pattern, req_lower):
                return True
        return False
    
    def _is_should_pattern(self, req: str) -> bool:
        """
        Prüft auf spezifische Muster für "Should have"-Anforderungen
        """
        patterns = [
            r"sollte\s",
            r"wichtig.*funktion",
            r"bedeutend.*aspekt",
            r"performance.*anforderung",
            r"benutzerfreundlichkeit",
            r"skalierbarkeit",
            r"konsistenz.*anforderung",
            r"kommunikation.*funktion"
        ]
        
        req_lower = req.lower()
        for pattern in patterns:
            if re.search(pattern, req_lower):
                return True
        return False
    
    def _is_could_pattern(self, req: str) -> bool:
        """
        Prüft auf spezifische Muster für "Could have"-Anforderungen
        """
        patterns = [
            r"könnte\s",
            r"schön.*wenn",
            r"wäre.*toll",
            r"optionale.*funktion",
            r"zusätzliche.*funktion",
            r"nice.*to.*have",
            r"zukünftige.*erweiterung",
            r"experimentell.*feature"
        ]
        
        req_lower = req.lower()
        for pattern in patterns:
            if re.search(pattern, req_lower):
                return True
        return False
    
    def _is_wont_pattern(self, req: str) -> bool:
        """
        Prüft auf spezifische Muster für "Won't have"-Anforderungen
        """
        patterns = [
            r"nicht.*jetzt",
            r"zu.*spät.*phase",
            r"nach.*release",
            r"zukünftige.*iteration",
            r"niedrige.*priorität",
            r"nicht.*priorisiert",
            r"langfristig.*ziel"
        ]
        
        req_lower = req.lower()
        for pattern in patterns:
            if re.search(pattern, req_lower):
                return True
        return False
    
    def _default_classification(self, requirement: str) -> str:
        """
        Standard-Klassifikation, wenn keine Keywords gefunden wurden
        """
        # Verwende Heuristiken basierend auf Anforderungstyp
        req_lower = requirement.lower()
        
        # Funktionale vs. nicht-funktionale Anforderungen
        functional_indicators = [
            "funktion", "feature", "möglichkeit", "unterstützung", 
            "bereitstellung", "implementierung", "erstellung"
        ]
        
        non_functional_indicators = [
            "performance", "sicherheit", "skalierbarkeit", "benutzerfreundlichkeit",
            "zuverlässigkeit", "wartbarkeit", "zugänglichkeit", "konsistenz"
        ]
        
        # Zähle Indikatoren
        func_count = sum(1 for indicator in functional_indicators if indicator in req_lower)
        non_func_count = sum(1 for indicator in non_functional_indicators if indicator in req_lower)
        
        # Funktionale Kernfunktionen sind typischerweise "Must have"
        if func_count > non_func_count and any(kw in req_lower for kw in ["kern", "zentral", "wesentlich"]):
            return "must_have"
        
        # Nicht-funktionale Anforderungen sind oft "Should have"
        if non_func_count > func_count:
            return "should_have"
        
        # Sonstige funktionale Anforderungen sind typischerweise "Could have"
        return "could_have"
    
    def estimate_confidence(self, requirement: str, category: str) -> float:
        """
        Schätzt die Vertrauenswahrscheinlichkeit der Kategorisierung
        """
        # Basisvertrauen
        confidence = 0.7
        
        # Erhöhe Vertrauen bei spezifischen Keywords
        req_lower = requirement.lower()
        if category == "must_have":
            confidence += sum(0.1 for keyword in self.must_keywords if keyword in req_lower)
        elif category == "should_have":
            confidence += sum(0.1 for keyword in self.should_keywords if keyword in req_lower)
        elif category == "could_have":
            confidence += sum(0.1 for keyword in self.could_keywords if keyword in req_lower)
        elif category == "wont_have":
            confidence += sum(0.1 for keyword in self.wont_keywords if keyword in req_lower)
        
        # Begrenze auf maximal 1.0
        return min(1.0, confidence)

class RequirementsFormatter:
    """
    Formatierer für priorisierte Anforderungen gemäß Formatierungskonventionen
    """
    
    @staticmethod
    def format_prioritized_requirements(prioritized: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        Formatierung priorisierter Anforderungen im Standardformat des Brainstorming-Skills
        """
        formatted_output = ""
        
        # Must Have Anforderungen
        formatted_output += "## Funktionale Anforderungen (Priorisiert nach MoSCoW)\n\n"
        
        if prioritized["must_have"]:
            formatted_output += "**Must Have (unbedingt notwendig):**\n"
            for i, item in enumerate(prioritized["must_have"], 1):
                req_text = item["requirement"]
                # Extrahiere ID falls vorhanden
                if req_text.startswith("FR-") or req_text.startswith("NFR-"):
                    parts = req_text.split(":", 1)
                    if len(parts) > 1:
                        formatted_output += f"- {parts[0]} (M): {parts[1].strip()}\n"
                    else:
                        formatted_output += f"- Must-{i} (M): {req_text}\n"
                else:
                    formatted_output += f"- Must-{i} (M): {req_text}\n"
            formatted_output += "\n"
        
        # Should Have Anforderungen
        if prioritized["should_have"]:
            formatted_output += "**Should Have (wichtig aber nicht kritisch):**\n"
            for i, item in enumerate(prioritized["should_have"], 1):
                req_text = item["requirement"]
                if req_text.startswith("FR-") or req_text.startswith("NFR-"):
                    parts = req_text.split(":", 1)
                    if len(parts) > 1:
                        formatted_output += f"- {parts[0]} (S): {parts[1].strip()}\n"
                    else:
                        formatted_output += f"- Should-{i} (S): {req_text}\n"
                else:
                    formatted_output += f"- Should-{i} (S): {req_text}\n"
            formatted_output += "\n"
        
        # Could Have Anforderungen
        if prioritized["could_have"]:
            formatted_output += "**Could Have (wäre schön, wenn möglich):**\n"
            for i, item in enumerate(prioritized["could_have"], 1):
                req_text = item["requirement"]
                if req_text.startswith("FR-") or req_text.startswith("NFR-"):
                    parts = req_text.split(":", 1)
                    if len(parts) > 1:
                        formatted_output += f"- {parts[0]} (C): {parts[1].strip()}\n"
                    else:
                        formatted_output += f"- Could-{i} (C): {req_text}\n"
                else:
                    formatted_output += f"- Could-{i} (C): {req_text}\n"
            formatted_output += "\n"
        
        # Won't Have Anforderungen (optional in der Ausgabe)
        if prioritized["wont_have"]:
            formatted_output += "**Won't Have (this time - nicht in dieser Iteration):**\n"
            for i, item in enumerate(prioritized["wont_have"], 1):
                req_text = item["requirement"]
                formatted_output += f"- Won't-{i} (W): {req_text}\n"
            formatted_output += "\n"
        
        return formatted_output

# Beispiel für die Verwendung
if __name__ == "__main__":
    # Beispiel-Anforderungen
    sample_requirements = [
        "FR-1: Das System muss in der Lage sein, Bias-Werte aus dem Modell zu extrahieren",
        "FR-2: Das System sollte eine grafische Heatmap anzeigen",
        "FR-3: Das System könnte eine Exportfunktion für die Bias-Analyse bieten",
        "FR-4: Das System muss die Daten gemäß DSGVO verarbeiten",
        "FR-5: Das System könnte ein Bookmarking-System für häufige Analyse-Punkte bieten",
        "FR-6: Das System sollte interaktive Tooltips für spezifische Bias-Werte anzeigen"
    ]
    
    prioritizer = Prioritizer()
    formatter = RequirementsFormatter()
    
    prioritized = prioritizer.prioritize_requirements(sample_requirements)
    
    print("Priorisierte Anforderungen:")
    print(formatter.format_prioritized_requirements(prioritized))