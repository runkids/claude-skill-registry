---
name: dialogue-structured-elicit
description: Gather structured information from the user through framework-aware questioning. Use when you need to elicit process context, requirements, constraints, or decisions. Triggers on "gather requirements", "elicit context", "structured questions", "need to understand".
allowed-tools: AskUserQuestion
---

# Dialogue: Structured Elicit

Gather structured information through framework-aware questioning.

## When to Use

Use this skill when you need to:
- Gather process context before designing capability flows
- Elicit requirements or constraints from the user
- Clarify ambiguous information
- Get decisions on alternatives you've identified

## Elicitation Patterns

### Process Context Elicitation

When gathering context for process design, elicit information across six areas. Four are **mandatory**; two are **contextual**.

#### Mandatory Questions (must elicit before proceeding)

| Area | Purpose | Example Question |
|------|---------|------------------|
| **Phase** | Determine SDLC phase | "Which phase does this process belong to?" |
| **Purpose** | Understand process goal | "What should this process accomplish?" |
| **Inputs** | Identify input documents/data | "What information flows into this process?" |
| **Outputs** | Identify deliverables | "What artifacts does this process produce?" |

#### Contextual Questions (elicit when relevant)

| Area | Purpose | When to Ask |
|------|---------|-------------|
| **Actors** | Understand who's involved | When unclear who participates; multi-team processes |
| **Constraints** | Surface limitations | When regulatory, security, or technical constraints likely |

### Minimum Coverage Requirement

**Do not proceed to decomposition until all four mandatory areas have answers.**

If the user cannot answer a mandatory question:
1. Note the gap as an observation
2. Propose a reasonable default with rationale
3. Get explicit confirmation before proceeding

Example: "I don't have information about inputs yet. Based on similar Phase 3 processes, I'd expect requirements documents and stakeholder notes. Does that seem right?"

### Coverage Checklist

Before proceeding from elicitation, verify:

```
□ Phase identified
□ Purpose stated
□ Inputs defined (or default confirmed)
□ Outputs defined (or default confirmed)
□ Elicited context logged as observation
```

### Information Composition Elicitation

To estimate formal/tacit/emergent composition:

| Question | Indicates |
|----------|-----------|
| "Is there documented procedure for this?" | High formal if yes |
| "Does this require expertise that's hard to document?" | High tacit if yes |
| "Does new understanding emerge during execution?" | High emergent if yes |
| "Could someone follow written instructions to do this?" | Low tacit if yes |

### Pattern Selection Elicitation

When AI involvement is unclear:

| Question | Helps Determine |
|----------|-----------------|
| "Should a human always make this decision?" | Human-Only vs other |
| "Could AI do this entirely without human review?" | AI-Only suitability |
| "Is human judgement essential, or just review?" | Partnership vs AI-Led |

## Using AskUserQuestion

Structure questions using the AskUserQuestion tool:

```
Use AskUserQuestion with:
- question: Clear, specific question
- header: Short label (max 12 chars)
- options: 2-4 distinct choices with descriptions
- multiSelect: true if multiple answers valid
```

### Example: Phase Elicitation

```
question: "Which SDLC phase does this process belong to?"
header: "Phase"
options:
  - label: "Initiation (Phase 1)"
    description: "Project setup, feasibility, initial stakeholder engagement"
  - label: "Planning (Phase 2)"
    description: "Resource allocation, timeline, risk assessment"
  - label: "Requirements (Phase 3)"
    description: "Gathering and documenting what the system should do"
  - label: "Design (Phase 4)"
    description: "Architectural decisions, component design"
```

### Example: Collaboration Pattern

```
question: "How should humans and AI collaborate on this step?"
header: "Pattern"
options:
  - label: "Human-Only"
    description: "Human does all work; AI not involved"
  - label: "Human-Led"
    description: "Human drives; AI assists and supports"
  - label: "Partnership"
    description: "Both essential; continuous collaboration"
  - label: "AI-Led"
    description: "AI drives; human reviews and approves"
```

## Recording Elicitation Results

After eliciting information, use the **dialogue-log-observation** skill to record:
- Key requirements noted
- Constraints identified
- User preferences stated

This preserves the elicited context for future reference.

## Escalation

If the user cannot answer or indicates uncertainty:
- Note the uncertainty as an observation
- Propose reasonable defaults with rationale
- Ask if defaults are acceptable

---

*Part of the AI-Augmented SDLC Framework dialogue system*
