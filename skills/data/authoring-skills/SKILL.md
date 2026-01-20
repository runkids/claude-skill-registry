---
name: authoring-skills
description: Guide for writing and updating Claude Code skills. Triggers on "create skill", "new skill", "update skill", "skill structure". Enforces router pattern and concise documentation.
---

# Authoring Skills

## When to Use

- Creating a new skill
- Refactoring an existing skill
- Reviewing skill structure

## Core Principles

1. **Router pattern**: SKILL.md = TOC only (~30-50 lines)
2. **TodoWrite required**: Multi-step skills must track with TodoWrite
3. **Concise over verbose**: Sacrifice grammar for clarity

## Skill Structure

```
skill-name/
├── SKILL.md           # Router only - triggers, overview, reference links
└── references/        # All detailed content
    ├── workflows/     # Step-by-step procedures
    ├── templates/     # Reusable content blocks
    └── *.md           # Domain-specific docs
```

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Router pattern | [references/router-pattern.md](references/router-pattern.md) |
| Checklist | [references/skill-checklist.md](references/skill-checklist.md) |
| Examples | [references/examples.md](references/examples.md) |

## Anti-Pattern

Monolithic SKILL.md with 200+ lines. Split into references.
