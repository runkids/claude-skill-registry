---
description: Save session and exit gracefully (unified approach)
---

# Graceful Session Exit

When the user invokes `/bye`, you should:

## Step 1: Save Session

**Spawn the `session-saver` agent** to create:
1. YAML handoff at `thoughts/shared/handoffs/{date}_{topic}.yaml`
2. Quick state files in `.claude/memory/`

This is the unified save mechanism - one source of truth for all hooks.

## Step 2: Confirm with User

After saving, show:

```
Session saved to: thoughts/shared/handoffs/{date}_{topic}.yaml

Summary:
- Goal: [what you were working on]
- Done: [key accomplishments]
- Next: [first action item]

Ready to exit? Type 'exit' or just close the terminal.
```

## Usage

- `/bye` - full save + exit prompt
- `/bye quick` - minimal save (goal/now/done/next only)

## Quick Mode

If `/bye quick`, tell session-saver to create minimal handoff:
```yaml
goal: [1-line summary]
outcome: IN_PROGRESS
now: [immediate next action]
done_this_session:
  - [1-2 key items]
next:
  - priority: P0
    task: [most important next step]
```

## Migration Note

This replaces the old dual-system where `/create_handoff` wrote Markdown and `session-saver` wrote separate state files. Now everything goes through session-saver for consistency.
