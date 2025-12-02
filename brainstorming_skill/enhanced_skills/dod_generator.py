"""
DefinitionOfDoneGenerator für den erweiterten Brainstorming-Skill
Erstellt klare Abnahmekriterien für Features und Anforderungen
"""
from typing import Dict, Any, List
import re

class DefinitionOfDoneGenerator:
    """
    Erstellt Definition of Done (DoD) für Features und Anforderungen
    """
    
    def __init__(self):
        # Kriterien-Kategorien für verschiedene Arten von Features
        self.feature_categories = {
            "visualisierung": {
                "functional_criteria": [
                    "Darstellung funktioniert für alle unterstützten Datenformate",
                    "Benutzer kann Daten visualisieren",
                    "Benutzer kann Visualisierung exportieren (PNG, SVG, PDF)"
                ],
                "performance_criteria": [
                    "Visualisierung lädt in < 100ms",
                    "Interaktion (Zoom, Pan) erfolgt in < 50ms",
                    "Speicherbedarf < 100MB für typische Datensätze"
                ],
                "quality_criteria": [
                    "Farbcodierung ist konsistent und barrierefrei",
                    "Tooltip-Informationen sind korrekt und vollständig",
                    "Visualisierung ist responsive auf verschiedenen Bildschirmgrößen"
                ],
                "acceptance_tests": [
                    "Visualisierung zeigt korrekt für Testdatensatz an",
                    "Interaktive Elemente reagieren korrekt auf Benutzereingaben",
                    "Exportfunktion erstellt Datei im korrekten Format"
                ]
            },
            "datenverarbeitung": {
                "functional_criteria": [
                    "Daten werden korrekt eingelesen",
                    "Daten werden korrekt transformiert",
                    "Daten werden korrekt aggregiert/analysiert"
                ],
                "performance_criteria": [
                    "Datenverarbeitung erfolgt in akzeptabler Zeit",
                    "Speicherbedarf ist effizient",
                    "CPU-Nutzung ist angemessen"
                ],
                "quality_criteria": [
                    "Validierung der Eingabedaten",
                    "Fehlerbehandlung bei ungültigen Daten",
                    "Logging relevanter Verarbeitungsschritte"
                ],
                "acceptance_tests": [
                    "Verarbeitung verschiedener gültiger Datensätze erfolgreich",
                    "Fehler werden korrekt bei ungültigen Datensätzen erkannt",
                    "Ergebnisse sind konsistent mit Testdatensätzen"
                ]
            },
            "künstliche_intelligenz": {
                "functional_criteria": [
                    "Modell macht Vorhersagen/Vorhersagen korrekt",
                    "Modell ist in der Anwendung integriert",
                    "Modell kann mit verschiedenen Datentypen arbeiten"
                ],
                "performance_criteria": [
                    "Vorhersage erfolgt in < 200ms",
                    "Modell verbraucht akzeptable Ressourcen",
                    "Modell kann in akzeptabler Zeit trainiert werden"
                ],
                "quality_criteria": [
                    "Modellqualität ist ausreichend (Metriken definiert)",
                    "Modell ist reproduzierbar",
                    "Modell ist dokumentiert"
                ],
                "acceptance_tests": [
                    "Modell macht korrekte Vorhersagen für Testdatensatz",
                    "Modell zeigt akzeptable Metriken (Accuracy, Precision, etc.)",
                    "Modell funktioniert mit verschiedenen Eingabedaten"
                ]
            },
            "schnittstelle": {
                "functional_criteria": [
                    "Schnittstelle implementiert definierte Endpunkte",
                    "Schnittstelle verarbeitet Eingaben korrekt",
                    "Schnittstelle gibt korrekte Antworten zurück"
                ],
                "performance_criteria": [
                    "Antwortzeit < 100ms für 95% der Anfragen",
                    "Schnittstelle kann 100+ Anfragen/Minute verarbeiten",
                    "Datenübertragung ist effizient"
                ],
                "quality_criteria": [
                    "API-Dokumentation ist vollständig",
                    "Fehlerbehandlung ist implementiert",
                    "Authentifizierung/Authorisierung ist implementiert"
                ],
                "acceptance_tests": [
                    "Alle Endpunkte funktionieren wie definiert",
                    "Fehlerfälle werden korrekt behandelt",
                    "Authentifizierung funktioniert wie erwartet"
                ]
            }
        }
    
    def generate_dod(self, feature_description: str) -> Dict[str, Any]:
        """
        Erstellt eine Definition of Done für ein Feature
        """
        # Klassifiziere das Feature
        feature_type = self._classify_feature(feature_description)
        
        # Extrahiere spezifische Details aus der Beschreibung
        feature_details = self._extract_feature_details(feature_description)
        
        # Generiere DoD basierend auf Feature-Typ und Details
        dod = {
            "feature_name": feature_details.get("name", "Unbenanntes Feature"),
            "functional_criteria": self._generate_functional_criteria(feature_description, feature_type),
            "performance_criteria": self._generate_performance_criteria(feature_description, feature_type),
            "quality_criteria": self._generate_quality_criteria(feature_description, feature_type),
            "acceptance_tests": self._generate_acceptance_tests(feature_description, feature_type),
            "additional_criteria": feature_details.get("additional_criteria", [])
        }
        
        return dod
    
    def _classify_feature(self, description: str) -> str:
        """
        Klassifiziert das Feature basierend auf der Beschreibung
        """
        desc_lower = description.lower()
        
        # Suchmuster für verschiedene Feature-Typen
        patterns = {
            "visualisierung": [
                "visualisierung", "grafik", "anzeige", "heatmap", "diagramm", 
                "chart", "darstellung", "grafisch", "plot", "tabelle", "karte"
            ],
            "datenverarbeitung": [
                "daten", "verarbeitung", "aggregierung", "analyse", "filterung", 
                "transformation", "kalkulation", "berechnung", "algorithmen"
            ],
            "künstliche_intelligenz": [
                "ki", "künstliche", "intelligenz", "ai", "ml", "machine", 
                "lernen", "model", "vorhersage", "prediction", "algorithmus"
            ],
            "schnittstelle": [
                "schnittstelle", "api", "interface", "endpunkt", "request", 
                "response", "kommunikation", "integration", "anbindung"
            ]
        }
        
        for feature_type, keywords in patterns.items():
            for keyword in keywords:
                if keyword in desc_lower:
                    return feature_type
        
        # Standard-Typ, wenn keine Kategorisierung möglich
        return "schnittstelle"  # Standard ist eine allgemeine Schnittstelle
    
    def _extract_feature_details(self, description: str) -> Dict[str, Any]:
        """
        Extrahiert spezifische Details aus der Feature-Beschreibung
        """
        # Versuche, den Feature-Namen zu extrahieren
        # Muster: "Feature-name" oder "Komponente X" oder "...funktion"
        name_patterns = [
            r'"([^"]+)"',  # Text in Anführungszeichen
            r"'([^']+)'",  # Text in einfachen Anführungszeichen
            r'(\w+)\s*[.-]?\s*(komponente|funktion|modul|seite|seite)',  # "X Komponente/Funktion"
        ]
        
        feature_name = "Unbenanntes Feature"
        for pattern in name_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                feature_name = match.group(1)
                break
        
        # Extrahiere spezifische Anforderungen
        additional_criteria = []
        specific_reqs = [
            r"(<\s*\d+\s*ms)",  # Performance-Anforderungen
            r"(<\s*\d+\s*s)",   # Zeitangaben
            r"(>\s*\d+%)",     # Prozentangaben
            r"(>\s*\d+\s*MB)", # Speicherangaben
            r"(<\s*\d+\s*MB)", # Speicherangaben
            r"(>\s*\d+\s*GB)", # Speicherangaben
            r"(<\s*\d+\s*GB)", # Speicherangaben
        ]
        
        for req_pattern in specific_reqs:
            matches = re.findall(req_pattern, description, re.IGNORECASE)
            for match in matches:
                additional_criteria.append(f"Leistungsanforderung: {match.strip()}")
        
        return {
            "name": feature_name,
            "additional_criteria": additional_criteria
        }
    
    def _generate_functional_criteria(self, description: str, feature_type: str) -> List[str]:
        """
        Generiert funktionale Kriterien für das Feature
        """
        criteria = []
        
        if feature_type in self.feature_categories:
            criteria.extend(self.feature_categories[feature_type]["functional_criteria"])
        
        # Füge spezifische Kriterien basierend auf der Beschreibung hinzu
        desc_lower = description.lower()
        
        # Muster für spezifische funktionale Anforderungen
        if "export" in desc_lower or "datei" in desc_lower:
            criteria.append("Exportfunktion ist verfügbar")
        
        if "import" in desc_lower:
            criteria.append("Importfunktion ist verfügbar")
        
        if "benutzer" in desc_lower or "nutzer" in desc_lower:
            criteria.append("Benutzer kann Feature korrekt verwenden")
        
        if "admin" in desc_lower:
            criteria.append("Administrationsfunktionen sind verfügbar")
        
        # Entferne Duplikate
        return list(set(criteria))
    
    def _generate_performance_criteria(self, description: str, feature_type: str) -> List[str]:
        """
        Generiert Leistungs-Kriterien für das Feature
        """
        criteria = []
        
        if feature_type in self.feature_categories:
            criteria.extend(self.feature_categories[feature_type]["performance_criteria"])
        
        # Füge spezifische Performance-Kriterien hinzu, wenn sie in der Beschreibung erwähnt werden
        desc_lower = description.lower()
        
        if "schnell" in desc_lower or "performance" in desc_lower:
            criteria.append("Ladezeit ist akzeptabel (< 500ms)")
        
        if "skalier" in desc_lower:
            criteria.append("Funktion skaliert mit wachsenden Datenvolumen")
        
        # Entferne Duplikate
        return list(set(criteria))
    
    def _generate_quality_criteria(self, description: str, feature_type: str) -> List[str]:
        """
        Generiert Qualitäts-Kriterien für das Feature
        """
        criteria = []
        
        if feature_type in self.feature_categories:
            criteria.extend(self.feature_categories[feature_type]["quality_criteria"])
        
        # Füge spezifische Qualitätskriterien hinzu
        desc_lower = description.lower()
        
        if "test" in desc_lower:
            criteria.append("Unit-Tests sind vorhanden und bestehen")
        
        if "doku" in desc_lower or "dokumentation" in desc_lower:
            criteria.append("Funktion ist dokumentiert")
        
        # Entferne Duplikate
        return list(set(criteria))
    
    def _generate_acceptance_tests(self, description: str, feature_type: str) -> List[str]:
        """
        Generiert Akzeptanztests für das Feature
        """
        tests = []
        
        if feature_type in self.feature_categories:
            tests.extend(self.feature_categories[feature_type]["acceptance_tests"])
        
        # Entferne Duplikate
        return list(set(tests))

class DoDFormatter:
    """
    Formatierer für Definition of Done gemäß Formatierungskonventionen
    """
    
    @staticmethod
    def format_dod(dod: Dict[str, Any]) -> str:
        """
        Formatierung der Definition of Done im Standardformat
        """
        formatted_output = f"## Definition of Done für: {dod['feature_name']}\n\n"
        
        formatted_output += "### Funktionale Kriterien:\n"
        for criterion in dod["functional_criteria"]:
            formatted_output += f"- {criterion}\n"
        formatted_output += "\n"
        
        formatted_output += "### Leistungs-Kriterien:\n"
        for criterion in dod["performance_criteria"]:
            formatted_output += f"- {criterion}\n"
        formatted_output += "\n"
        
        formatted_output += "### Qualitäts-Kriterien:\n"
        for criterion in dod["quality_criteria"]:
            formatted_output += f"- {criterion}\n"
        formatted_output += "\n"
        
        formatted_output += "### Akzeptanztests:\n"
        for test in dod["acceptance_tests"]:
            formatted_output += f"- {test}\n"
        formatted_output += "\n"
        
        if dod["additional_criteria"]:
            formatted_output += "### Zusätzliche Kriterien:\n"
            for criterion in dod["additional_criteria"]:
                formatted_output += f"- {criterion}\n"
            formatted_output += "\n"
        
        return formatted_output

# Beispiel für die Verwendung
if __name__ == "__main__":
    generator = DefinitionOfDoneGenerator()
    formatter = DoDFormatter()
    
    # Beispiel-Feature-Beschreibung
    feature_desc = 'BiasHeatmap.jsx: Eine Komponente, die grafisch anzeigt, ' \
                   'wo im Modell Bias-Werte > 0.5 auftreten. Sollte in < 100ms laden ' \
                   'und interaktive Tooltips für spezifische Bias-Werte anzeigen.'
    
    dod = generator.generate_dod(feature_desc)
    formatted_dod = formatter.format_dod(dod)
    
    print("Definition of Done:")
    print(formatted_dod)