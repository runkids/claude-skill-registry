---
name: brainstorming
description: Explores user intent, requirements, and design before implementation. Use before creating features, building components, or modifying behavior to turn ideas into designs through collaborative dialogue.
---

# Brainstorming Ideas Into Designs

## When to use this skill
- When the user has a vague idea or feature request.
- Before writing any code or implementation plans.
- When you need to understand purpose, constraints, and success criteria.

## Workflow
1.  **Understand the Idea**: Ask questions one at a time to refine the user's intent.
2.  **Explore Approaches**: Propose 2-3 approaches with trade-offs.
3.  **Present Design**: Present the design in small sections (200-300 words) for validation.
4.  **Finalize**: Save the validated design to a markdown file.

## Instructions

### 1. Understanding the Idea
*   **Context First**: Check current project state (files, docs) before asking.
*   **One Question at a Time**: Never overwhelm the user; ask one focused question per turn.
*   **Multiple Choice**: When possible, offer options to choose from.
*   **Focus**: Nail down the purpose, constraints, and success criteria.

### 2. Exploring Approaches
*   **Propose Alternatives**: Always offer 2-3 different ways to solve the problem (e.g., "Option A: Quick & Dirty", "Option B: Robust & Scalable").
*   **Trade-offs**: Explain pros/cons of each.
*   **Recommendation**: State which option you recommend and why.

### 3. Presenting the Design
*   **Incremental**: Break the design into sections of 200-300 words.
*   **Validation**: Stop after each section and ask: "Does this look right so far?"
*   **Content**: Cover architecture, components, data flow, error handling, and testing.

### 4. Output
*   Once agreed, write the full design to `docs/plans/YYYY-MM-DD-<topic>-design.md`.
*   Ask the user if they are ready to proceed to the **Planning** phase.

## Resources
*   [Planning Skill](../planning/SKILL.md) - For converting the design into actionable tasks.
