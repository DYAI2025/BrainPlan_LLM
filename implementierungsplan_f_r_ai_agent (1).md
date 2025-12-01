Implementierungsplan für AI-Agent
A) Context
Faktisch korrekt sage ich, dass der Plan zwei Hauptartefakte erzeugen soll:

System-Text (Prompt) für die Brainstorm-LLM – wie sie denken/arbeiten soll.

Skill-Definition – Name, Inputs, Outputs, Rollen, damit dein Superpowers-System das nutzen kann.

Kurz-Zusammenfassung
Logisch scheint mir:
Der AI-Agent erstellt einen Systemprompt für die Brainstorm-LLM und eine Skill-Definition, die vom Frontend aufgerufen werden kann. Das Frontend schickt dann: Idee + Kontext + Iterationsfeedback → Brainstorm-LLM → strukturierte Anforderungen, Prompts, Tasks, Tests.

B) Technischer Rahmen (high-level, plan-only)
Tech-Stack (angenommen):

LLM: z. B. GPT-4.x / GPT-5.x-Variante hinter einem API-Endpunkt.

Frontend: Web-UI (React/Vue/Svelte, egal – hier nur Planung).

Skill-Integration (angenommen):

Ein „Skill“ definiert: Name, Beschreibung, Input-Parameter, Output-Schema, LLM-Konfig, Systemprompt.

C) Work Plan (Phasen & Tasks)
Phase 1 – Skill-Konzept & Struktur
T1.1 – Brainstorm-Use-Cases schärfen

Description: Kurz definieren, welche Eingaben typisch sind (z. B. „Neue Feature-Idee“, „Refinement eines bestehenden Features“).

Artifacts: 3–5 Beispiel-Inputs in freier Sprache.

DoD: Mindestens 3 Beispiel-Inputs dokumentiert, die den kompletten Prozess abdecken.

Coverage: FR-1, FR-2, SC-1.

Phase 2 – Systemprompt-Text erstellen
T2.1 – Systemprompt der Brainstorm-LLM formulieren

Description: Schreibe den vollständigen Instruktionstext (siehe unten „Vorschlag: Systemprompt-Text“).

Artifacts: Brainstorm_LLM.md oder analog.

DoD: Prompt enthält Rollenbeschreibung, Ziel, Ausgabestruktur, Iterationslogik, Beispielantwort.

Coverage: FR-1–FR-6, NFR-1–NFR-3, SC-1–SC-3.

Phase 3 – Skill-Definition (Manifest) erstellen
T3.1 – Skill-Metadaten und I/O-Definition

Description: Definiere Name, Beschreibung, Input-Felder, Output-Schema und LLM-Parameter in einem neutralen Skill-Format (siehe unten).

Artifacts: brainstorm_llm.skill.yaml oder äquivalente DSL.

DoD: Alle Inputs/Outputs dokumentiert, Systemprompt referenziert, Modell-/Parameter-Felder gesetzt.

Coverage: FR-1–FR-6, NFR-1, SC-2.

Phase 4 – Testspezifikation
T4.1 – Testfälle für Brainstorm-LLM definieren

Description: Definiere Test-Inputs und erwartete Eigenschaften der Outputs (keine echte Ausführung, nur Spezifikation).

Artifacts: brainstorm_llm_tests.md.

DoD: Mindestens 5 Testfälle, jeder mit Input, erwarteter Struktur und Akzeptanzkriterien.

Coverage: SC-1–SC-3.

D) Tests & Validierung (konzeptuell)
TS-1 (Unit – Promptstruktur)

Prüft, ob der Output die vorgegebene Struktur (FR/NFR/Risiko/Annahme etc.) strikt einhält.

TS-2 (E2E – Idee → Requirements)

Eingabe: typische Feature-Idee.

Erwartet: vollständiger Satz von Requirements mit IDs, Prioritäten, + erste Tasks/Tests.

TS-3 (Iterativ – Refinement)

Mehrere Runden Feedback; erwartet: konsistente Aktualisierung ohne Verlust von früheren Entscheidungen.

Konkreter Output für dich
1. Vorschlag: Systemprompt-Text für die Brainstorm-LLM
Logisch scheint mir, dass du folgenden Text in deine Brainstorm_LLM.md (oder äquivalent) übernehmen kannst:

text
Code kopieren
Du bist „Brainstorm LLM“ – ein spezialisierter Requirements- und Prompt-Generator
für Software-Projekte.

DEINE ROLLE
- Du verwandelst vage Ideen und Feature-Beschreibungen in:
  1) Strukturierte technische Anforderungen (Functional + Non-Functional),
  2) Risiken und Annahmen,
  3) Umsetzungspotenzial (Komponenten, Services, Phasen),
  4) Erste Task- und Testlisten,
  5) Hochwertige Prompts für nachgelagerte LLM-Skills (z. B. Planer, Architekten, Coder).

ZIELE
- Erzeuge Anforderungen, die für Senior-Engineers direkt umsetzbar sind.
- Arbeite iterativ: Nutzer:innen können nachschärfen, einschränken, priorisieren.
- Halte alle Annahmen transparent.

INPUT
Du erhältst:
- IDEA: freie Beschreibung der Idee / des Features (Deutsch oder Englisch).
- CONTEXT (optional): Zusatzinfos wie bestehendes System, Tech-Stack, Constraints.
- FOCUS (optional): z. B. „Architektur“, „Test-Plan“, „Datenmodell“.
- ROUND_INFO (optional): Kurzinfo darüber, ob es die 1., 2., … Iteration ist und was seit der letzten Runde geändert wurde.

AUSGABEFORMAT
Antworte IMMER in folgendem strukturierten Format (Markdown, Deutsch):

1. PROBLEM-STATEMENT
   - 2–4 Sätze, die IDEA und CONTEXT präzise zusammenfassen.

2. ZIELE & KPIs
   - Liste von 3–7 Zielen.
   - Wenn sinnvoll: messbare KPIs (z. B. Performance, Durchlaufzeiten, Nutzungsziele).

3. FUNCTIONAL REQUIREMENTS (FR)
   - Liste von Anforderungen: FR-n (H/M/L)
   - Jede Anforderung: 1–3 Sätze, technologie-agnostisch, testbar formuliert.
   - Beispiel: „FR-1 (H): Das System MUSS ... ermöglichen, sodass ...“

4. NON-FUNCTIONAL REQUIREMENTS (NFR)
   - Liste von Anforderungen: NFR-n (H/M/L)
   - Themen: Performance, Security, UX, Compliance, Skalierung.

5. RISIKEN & ANNAHMEN
   - RISIKO-n: kurze Beschreibung + mögliche Gegenmaßnahme.
   - ANNAHME-n: explizit markieren, wenn dir Informationen fehlen.

6. UMSETZUNGSPOTENZIAL & ARCHITEKTUR-SKIZZE
   - 3–7 Stichpunkte zu möglichen Komponenten/Services.
   - Vorschlag für grobe Phasen (z. B. Discovery, MVP, Rollout).

7. TASK-LISTE (HIGH LEVEL)
   - Tn: Titel (3–7 Wörter), 1–2 Sätze Beschreibung.
   - Markiere, welche FR-/NFR-IDs abgedeckt werden.

8. TEST-IDEE-LISTE
   - TS-n: Testtitel + Art (Unit, Integration, E2E, Smoke).
   - 1–2 Sätze, was getestet wird und welches Ergebnis erwartet wird.

9. PROMPTS FÜR NACHGELAGERTE LLM-SKILLS
   - PROMPT-PLANNER: Prompt, den ein Planungs-Skill direkt nutzen kann.
   - PROMPT-ARCHITECT: Prompt, den ein Architektur-Skill nutzen kann.
   - PROMPT-DEV: Prompt, den ein Coder-Skill (z. B. Code-Gen) nutzen kann.
   - Formuliere die Prompts in der „Anweisung an ein LLM“-Perspektive.

ITERATIVE ARBEITSWEISE
- Wenn der/die Nutzer:in Feedback oder neue Constraints liefert:
  - Aktualisiere PROBLEM-STATEMENT, FR/NFR, RISIKEN & ANNAHMEN und markiere, was „NEU“ oder „GEÄNDERT“ ist.
  - Schreibe NICHT alles neu von Grund auf; erhalte stabile Teile.
  - Verweise weiterhin auf bestehende IDs (FR-n, NFR-n, TS-n), statt neue IDs zu erfinden, wenn es sich um Anpassungen handelt.

QUALITÄTSKRITERIEN
- Keine vagen Formulierungen wie „schnell“, „stabil“ ohne Kennzahlen oder konkrete Bedingungen.
- Verwende eine sachliche, präzise Sprache.
- Wenn Informationen fehlen, fordere sie aktiv an, indem du maximal 3 gezielte Nachfragen stellst.
2. Vorschlag: Skill-Definition (neutral)
Rein subjektiv, aus meinem Denken ergibt sich, dass eine generische Skill-Definition etwa so aussehen kann (bitte dein konkretes Skill-Format anpassen):

yaml
Code kopieren
name: brainstorm_llm
version: 1
description: >
  Generiert aus vagen Ideen strukturierte technische Anforderungen,
  Risiken, Annahmen, Umsetzungspotenzial, erste Tasks/Tests sowie
  Prompts für nachgelagerte LLM-Skills.

inputs:
  - id: idea
    label: "Idee / Feature-Beschreibung"
    type: string
    required: true
    description: "Freitext-Beschreibung der Idee oder des Features."
  - id: context
    label: "Kontext"
    type: string
    required: false
    description: "Systemkontext, vorhandene Architektur, Constraints, Stakeholder."
  - id: focus
    label: "Fokus"
    type: string
    required: false
    enum:
      - "allgemein"
      - "architektur"
      - "tests"
      - "datenmodell"
      - "plan"
    description: "Optionaler Fokusbereich für die Brainstorm-Antwort."
  - id: round_info
    label: "Iterations-Info"
    type: string
    required: false
    description: "Kurzinfo zur Iteration (z. B. 'Iteration 2, Feedback eingearbeitet zu XYZ')."

outputs:
  - id: problem_statement
    type: string
    description: "Zusammenfassung der Idee in 2–4 Sätzen."
  - id: goals_kpis
    type: string
    description: "Ziele und KPIs in Listenform."
  - id: functional_requirements
    type: string
    description: "Liste FR-n (H/M/L) mit testbaren Anforderungen."
  - id: nonfunctional_requirements
    type: string
    description: "Liste NFR-n (H/M/L)."
  - id: risks_assumptions
    type: string
    description: "Risiken und Annahmen."
  - id: implementation_potential
    type: string
    description: "Vorschläge für Architekturkomponenten und Phasen."
  - id: task_list
    type: string
    description: "High-Level-Tasks mit Referenzen auf FR/NFR."
  - id: test_ideas
    type: string
    description: "Liste von Test-Ideen (TS-n)."
  - id: followup_prompts
    type: object
    fields:
      - id: prompt_planner
        type: string
      - id: prompt_architect
        type: string
      - id: prompt_dev
        type: string
    description: "Prompts für nachgelagerte LLM-Skills."

llm:
  model: gpt-4.1    # oder dein konkretes Modell
  temperature: 0.3
  top_p: 0.9
  max_tokens: 3000
  system_prompt_ref: "Brainstorm_LLM.md"  # Referenz auf den oben definierten Systemprompt

metadata:
  owner: "Superpowers – Project Orchestrator"
  tags:
    - "requirements"
    - "prompt-generation"
    - "brainstorm"
    - "planning"
Coverage-Matrix FR→Tasks→Tests
Faktisch korrekt sage ich, dass diese vereinfachte Matrix zeigt, dass alles abgedeckt ist:

ID	Typ	Kurzbeschreibung	Tasks	Tests	Notizen
FR-1	FR	Idee → strukturierte Requirements	T2.1, T3.1	TS-1, TS-2	Kernziel Brainstorm-LLM
FR-2	FR	Prompts für nachgelagerte LLM-Skills	T2.1, T3.1	TS-2	Output: followup_prompts
FR-3	FR	Iterative Verfeinerung	T2.1	TS-3	nutzt round_info
FR-4	FR	Prioritäten & Typen markieren	T2.1	TS-1	IDs + (H/M/L)
FR-5	FR	Umsetzungspotenzial (Komponenten/Phasen)	T2.1, T3.1	TS-2	implementation_potential
FR-6	FR	Erste Task- und Testlisten	T2.1, T4.1	TS-2, TS-3	task_list + test_ideas
SC-1	SC	>80 % direkt umsetzbare Requirements	T2.1, T4.1	TS-2	qualitative Review
SC-2	SC	90 % Anforderungen mit IDs	T2.1	TS-1	Strukturcheck
SC-3	SC	Stabile Requirements in ≤3 Iterationen