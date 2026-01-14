---
name: dialogue-log-decision
description: Log an operational or tactical decision. Use when recording a decision made by human or AI, capturing rationale, outcome, and context. Triggers on "log decision", "record decision", "document choice".
allowed-tools: Bash
---

# Dialogue: Decision Logger

Log an operational or tactical decision to the decision log.

## When to Use

Use this skill when you need to record:
- A decision you (AI) made during task execution
- A decision the user made that you should capture
- A tactical choice affecting approach or method

**Do NOT use for architecture decisions** — those should be ADRs.

## How to Log a Decision

Execute the following bash command:

```bash
.claude/skills/dialogue-log-decision/scripts/log-decision.sh <type> <actor> <subject> <outcome> <rationale> [context] [tags]
```

### Required Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `type` | `OPERATIONAL` or `TACTICAL` | OPERATIONAL for routine choices; TACTICAL for approach changes |
| `actor` | `ai:claude` or `human:<id>` | Who made the decision |
| `subject` | text | Brief description of what the decision concerns |
| `outcome` | text | What was decided or done |
| `rationale` | text | Single-line reasoning (why this choice) |

### Optional Parameters

| Parameter | Description |
|-----------|-------------|
| `context` | Additional surrounding situation |
| `tags` | Comma-separated categorisation tags |

## Examples

### AI Operational Decision
```bash
.claude/skills/dialogue-log-decision/scripts/log-decision.sh OPERATIONAL "ai:claude" "Test failure response" "Added null check to validateInput()" "TypeError indicated undefined parameter" "During PR #47 review" "fix,validation"
```

### Human Tactical Decision
```bash
.claude/skills/dialogue-log-decision/scripts/log-decision.sh TACTICAL "human:pidster" "Refactoring approach" "Refactor auth module before adding feature" "Reduce complexity before extending" "" "refactor,auth"
```

## Output

The script returns the generated decision ID (e.g., `DEC-20260113-143215`).

## Granularity Guidelines

### One Decision Per Distinct Choice

Log **one decision entry per distinct choice**. Do not batch multiple decisions into a single entry, even if they seem related.

**Correct** — separate entries for each pattern:
```bash
# PA-1 pattern
.claude/skills/dialogue-log-decision/scripts/log-decision.sh OPERATIONAL "ai:claude" "PA-1 pattern" "Partnership" "Both actors essential for context gathering" "Process design" "pattern"

# PA-2 pattern
.claude/skills/dialogue-log-decision/scripts/log-decision.sh OPERATIONAL "ai:claude" "PA-2 pattern" "AI-Only" "Document review is mechanical" "Process design" "pattern"
```

**Incorrect** — batched into single entry:
```bash
# Don't do this
.claude/skills/dialogue-log-decision/scripts/log-decision.sh OPERATIONAL "ai:claude" "PA-1 through PA-5 patterns" "Partnership, AI-Only, AI-Led, Partnership, AI-Led" "Various rationales" "Process design" "pattern"
```

### Why Granularity Matters

- **Audit trail**: Each decision can be reviewed independently
- **Traceability**: Specific rationale for each choice is preserved
- **Search**: Can find all decisions about a specific step
- **Compliance verification**: Can count decisions against expected count

### When Batching Is Acceptable

Batch only when:
- The decisions are truly identical (same rationale applies to all)
- The items being decided have no individual identity
- Example: "Applied consistent formatting to all 15 files" (one formatting decision, multiple files)
