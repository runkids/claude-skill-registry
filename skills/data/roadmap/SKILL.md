---
name: roadmap
version: "1.0.0"
triggers: ["/roadmap", "what should I work on", "show tasks", "what's next"]
description: Display ROADMAP.md tasks and offer interactive task selection with sub-agent suggestions.
---

# Roadmap Skill

## Trigger

Use when:
- User wants to see current tasks
- Starting a work session
- Deciding what to work on next

## Process

### Step 1: Read Roadmap

Read `ROADMAP.md` from project root. Extract:
- Active tasks (🔄 or unchecked)
- Pending items (⬜)
- Bugs/blockers

### Step 2: Display Summary

Present in scannable format:

```markdown
## Active Tasks

### [Category 1]
- [ ] Task A
- [ ] Task B

### [Category 2]
- [ ] Task C
```

### Step 3: Interactive Menu

Use `AskUserQuestion` to let user choose:

```
"What would you like to work on?"

Options:
- [Task from roadmap]
- [Another task]
- [Multiple tasks] — "I'll suggest which can run in parallel"
- [Something else] — Freeform input
```

### Step 4: Sub-Agent Analysis

When user selects tasks, analyze:

| Task Type | Recommendation |
|-----------|----------------|
| Research/exploration | Can run as parallel Explore agents |
| Independent file edits | Can run as parallel general-purpose agents |
| Sequential dependencies | Run one at a time |
| Interactive (interviews, Q&A) | Dedicated session, not sub-agent |
| Builds/tests | Background task |

**Suggest parallelization when:**
- Tasks don't depend on each other
- Tasks touch different files
- Tasks are research/read-only

**Avoid sub-agents when:**
- Task requires user interaction (AskUserQuestion)
- Task has complex decision points
- Tasks share state or files

### Step 5: Execute

Based on selection:
- Single task → Start working directly
- Parallel tasks → Launch sub-agents, explain what each is doing
- Sequential tasks → Create TodoWrite list, start first one

## Output Format

```markdown
## Roadmap: [Project Name]

**Active:**
- 🔄 [Task in progress]
- ⬜ [Pending task]

**What would you like to tackle?**
[Interactive menu]

**Parallelization suggestion:**
"Tasks X and Y can run simultaneously as sub-agents while you review Z."
```

## Notes

- Always read fresh ROADMAP.md (don't cache)
- Update ROADMAP.md when tasks complete
- Respect user's choice even if sub-agents suggested
