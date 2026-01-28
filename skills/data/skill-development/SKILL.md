---
name: skill-development
description: "Create portable, self-sufficient skills. Use when: You need to create a new reusable capability or specialized knowledge block. Not for: One-off scripts, user-triggered commands (use command-development), or single-session fixes."
---

# Skill Development

Skills are reusable capabilities that provide domain-specific knowledge and logic. Unlike commands (which are human-triggered), skills are contextually invoked by Claude to perform specific tasks.

**Core principle**: Skills must be self-contained and work in isolation without external dependencies.

---

## What Skills Are

Skills provide:

- Reusable logic blocks
- Domain-specific knowledge
- Contextual capabilities
- Compositional building blocks

### Skill vs Command

- **Skills**: Model-invoked capabilities (contextual use)
- **Commands**: Human-invoked orchestrators (explicit triggers)

---

## Core Structure

### Frontmatter

```yaml
---
name: skill-name
description: Clear, actionable description
---
```

### Skill Body

- **Trigger phrases**: When to use this skill
- **Core instructions**: How to apply the skill
- **Examples**: Concrete usage patterns
- **Integration**: How it works with other components

---

## Best Practices

### Portability

- Self-contained (no external dependencies)
- Include all necessary context
- Work in isolation

### Autonomy

- 80-95% autonomy (0-5 questions)
- Clear triggering conditions
- Progressive disclosure

### Quality

- Imperative form
- Clear examples
- Single source of truth

### Advanced Logic: Diagrams > Tables

For complex conditional logic or state machines, diagrams are unambiguous and token-efficient.

**A. Semantic Routing (Mermaid)**
Use inside `<router>` tags when decisions depend on natural language analysis.

```markdown
<router>
flowchart TD
    Input --> Analyze{Category?}
    Analyze -- Bug --> FixPath
    Analyze -- Feature --> PlanPath
    FixPath --> Test
</router>
```

**B. Strict State Machines (DOT/Graphviz)**
Use inside `<logic_flow>` tags for strict loops, retries, and error handling. **Preferred for high density.**

```markdown
<logic_flow>
digraph RetryLogic {
Start -> Attempt;
Attempt -> Success [label="200 OK"];
Attempt -> Backoff [label="5xx"];
Backoff -> Attempt;
}
</logic_flow>
```

### Persuasion Principles for Critical Skills

**CRITICAL**: Skills that enforce discipline require strong psychological enforcement to ensure compliance.

**Use authority language for non-negotiables:**

- MANDATORY: Must follow this workflow
- NEVER: Prohibited actions
- ALWAYS: Required steps

**Apply commitment techniques for multi-step workflows:**

- Require explicit user acknowledgment
- Force choices between approaches
- Create psychological barriers to shortcuts

**Examples:**

❌ Weak language (easily skipped):

```
"It's good to write tests first"
"You should probably use TDD"
"Maybe run the tests"
```

✅ Strong language (enforces compliance):

```
MANDATORY: Complete RED phase before GREEN
NEVER skip verification before completion
ALWAYS provide evidence for claims
```

**Red Flag Recognition**: If skill content is critical for quality or compliance, use absolute language to prevent rationalization and skipping.

---

## Navigation

| If you need...         | Reference                              |
| ---------------------- | -------------------------------------- |
| Description guidelines | `references/description-guidelines.md` |
| Progressive disclosure | `references/progressive-disclosure.md` |
| Autonomy design        | `references/autonomy-design.md`        |
| Orchestration patterns | `references/orchestration-patterns.md` |
| Anti-patterns          | `references/anti-patterns.md`          |
| Quality framework      | `references/quality-framework.md`      |
| Advanced execution     | `references/advanced-execution.md`     |
