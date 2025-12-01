# Qwen Code Context - Brainstorm LLM Project

## Project Overview

The Brainstorm_LLM project is an advanced AI-driven brainstorming and planning orchestrator that uses sophisticated reasoning techniques to transform vague ideas into structured requirements, tasks, and implementation plans. It implements state-of-the-art approaches including Tree-of-Thoughts (ToT), Graph-of-Thoughts (GoT), and ensemble refinement to generate comprehensive development plans.

## Key Features

1. **Tree-of-Thoughts (ToT) Implementation**: Generates multiple solution approaches hierarchically and evaluates them against 10 criteria
2. **Graph-of-Thoughts (GoT) Integration**: Creates a graph of solution approaches, identifies relationships (complementary, contradictory, dependent), and synthesizes hybrid solutions
3. **LLM Integration**: Connects to various LLM providers (OpenAI, Anthropic, Ollama) for dynamic reasoning
4. **Functional Enhancements**: Includes blindspot detection, constraint-impact matrix, premortem analysis, and calibration questions
5. **Skill Framework**: Integrates with an agentic system with structured input/output definitions

## Architecture & Components

### Core Reasoning Pipeline
- **Phase 2a**: Tree-of-Thoughts generation with 6 solution approaches scored on 10 criteria
- **Phase 2b**: Graph-of-Thoughts processing to find clusters, bridge thoughts, and create hybrid solutions
- **Phase 3**: Ensemble refinement to produce the final development plan

### File Structure
- `got/` - Python implementation of the reasoning pipeline
  - `tree_of_thoughts.py` - Tree-of-Thoughts implementation
  - `graph_of_thoughts.py` - Graph-of-Thoughts implementation  
  - `llm.py` - LLM client for various providers
  - `scoring.py` - Scoring system for solution evaluation
  - `visualization.py` - Mermaid diagram generation
- `references/` - Documentation and examples
- `assets/` - Evaluation questions and resources

### Scoring Criteria
The system evaluates each thought against 10 criteria:
1. Zielerreichung (Goal achievement) - 15%
2. Machbarkeit (Feasibility) - 12%
3. Aufwand (Effort) - 12%
4. Wartbarkeit (Maintainability) - 11%
5. Risiko (Risk) - 11%
6. ROI - 10%
7. Innovation - 8%
8. Sicherheit (Security) - 8%
9. Team-Fit - 7%
10. UX - 6%

## Development Workflow

### Setup & Installation
1. Install dependencies from `requirements.txt`:
```
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-2024-11-20
OPENAI_API_KEY=your-key-here
```

3. Test the installation:
```
python -c "from got import run_full_tot_then_got; print('ToT→GoT Pipeline ready')"
```

### LLM Integration
The system supports multiple LLM providers:
- OpenAI (GPT models)
- Anthropic (Claude models)
- Ollama (local models)

## AI Agent Implementation Plan

The project also includes an implementation plan for an AI agent that creates system prompts and skill definitions. The primary goal is to convert vague ideas into structured technical requirements, risks, assumptions, implementation potential, and prompts for downstream LLM skills.

### Skill Definition
The `brainstorm_llm` skill accepts inputs like:
- Idea/feature description
- Context (existing system, constraints)
- Focus area (architecture, tests, data model)
- Iteration information

It outputs structured content including:
- Problem statement
- Goals and KPIs
- Functional and non-functional requirements
- Risks and assumptions
- Implementation potential
- Task and test lists
- Prompts for downstream skills

## Usage

The system can be used as:
1. A standalone brainstorming orchestrator (`run_full_tot_then_got`)
2. An integrated skill in a larger agentic system
3. A requirement generation tool for software projects

## Testing & Validation

The system includes built-in evaluation questions and follows test-driven development principles. Each enhancement has a corresponding test to ensure functionality.

## Technical Implementation Status

The project is fully implemented with executable Python code. It represents the state-of-the-art in prompt engineering for 2025, combining multiple advanced reasoning techniques in a single pipeline.