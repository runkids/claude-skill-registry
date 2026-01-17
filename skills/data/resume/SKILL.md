---
description: Resume session with orchestration and memory (workspace-aware)
invokes: orchestration
---

# Resume Session

You are tasked with resuming work from a previous session.

## Process

### Step 0: Load Orchestration First (MANDATORY)

**Before doing anything else, invoke the `/orchestration` skill.**

```
Use Skill tool: skill="orchestration"
```

This ensures:
- Post-compact memory recovery is handled
- Session memory system is active
- All orchestration rules and patterns are loaded
- Worker agent templates are available

**Only proceed to Step 1 AFTER orchestration is loaded.**

### Step 0.5: Display Welcome Banner

```
   ─────────────────◆─────────────────
           ░█████╗░██╗░░░░░░█████╗░██████╗░░█████╗░██╗░░██╗
           ██╔══██╗██║░░░░░██╔══██╗██╔══██╗██╔══██╗██║░░██║
           ██║░░╚═╝██║░░░░░██║░░██║██████╔╝██║░░╚═╝███████║
           ██║░░██╗██║░░░░░██║░░██║██╔══██╗██║░░██╗██╔══██║
           ╚█████╔╝███████╗╚█████╔╝██║░░██║╚█████╔╝██║░░██║
           ░╚════╝░╚══════╝░╚════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
   ─────────────────◆─────────────────

         Resuming session...

   ─────────────────◆─────────────────
```

---

### Step 1: Detect Resume Context

Run these checks in parallel to find handoffs.

1. **Check for structured handoffs** (check both local and Clorch root):
   ```bash
   # Check local first, then parent (for ~/.claude/opc case)
   (find thoughts/shared/handoffs -name "*.yaml" -o -name "*.md" 2>/dev/null; \
    find ../thoughts/shared/handoffs -name "*.yaml" -o -name "*.md" 2>/dev/null) | \
    sort -u | head -10
   ```

2. **Check for simple handoff**:
   ```bash
   cat .claude/memory/handoff.md 2>/dev/null | head -20 || \
   cat ../memory/handoff.md 2>/dev/null | head -20
   ```

3. **Recall handoff-specific memory** (if opc exists):
   ```bash
   # Note: General session memory is handled by /orchestration
   # This is specifically for handoff/open-thread context
   if [ -d "opc" ]; then
     cd opc && PYTHONPATH=. uv run python scripts/core/recall_learnings.py --query "recent session open threads handoff" --k 3 --text-only 2>/dev/null
   elif [ -f "scripts/core/recall_learnings.py" ]; then
     PYTHONPATH=. uv run python scripts/core/recall_learnings.py --query "recent session open threads handoff" --k 3 --text-only 2>/dev/null
   fi
   ```

### Step 2: Present Findings

Based on what you find:

#### If structured handoffs exist:
```
Found structured handoff(s):
- {path1} ({date})
- {path2} ({date})

Would you like to:
1. Resume from most recent handoff: {path}
2. Choose a different handoff
3. Start fresh (ignore handoffs)
```

If user chooses to resume from a handoff, proceed with full handoff analysis:
- Read the handoff document completely
- Read any linked plans/research documents
- Verify current state vs handoff state
- Present analysis and recommended next actions
- Use TodoWrite to create task list from action items

#### If only simple handoff exists:
Present the handoff summary:
```
Last session handoff (from memory/handoff.md):

{handoff content summary}

Memory recalls:
{any relevant learnings from opc}

What would you like to work on?
```

#### If no handoffs found:
```
No handoffs found. Starting fresh session.

Memory recalls:
{any relevant learnings from opc, or "No prior learnings found"}

What would you like to work on?
```

### Step 3: If Resuming Structured Handoff

Follow the full handoff resume process:

1. **Read handoff document completely** (no limit/offset)

2. **Extract and verify**:
   - Tasks and their statuses
   - Recent changes (verify they still exist)
   - Learnings and decisions
   - Artifacts and file references
   - Action items and next steps
   - Chain history (if `prior_handoff:` exists)

3. **Present analysis**:
   ```
   Analyzed handoff from {date}:

   **Completed:**
   - {task 1}
   - {task 2}

   **Key Decisions:**
   - {decision}: {rationale}

   **What Worked / What Failed:**
   - Worked: {approaches}
   - Failed: {approaches to avoid}

   **History Chain:** (if prior_handoff exists)
   - Previous: {prior_handoff path} - {prior goal}
   - [View full chain history]

   **Recommended Next Actions:**
   1. {from handoff's `now:` field or `next:` list}
   2. {additional actions}

   Shall I proceed with action 1?
   ```

#### Chain Traversal (if prior_handoff exists)

If the handoff has a `prior_handoff:` field, offer chain exploration:

```
This handoff chains to: {prior_handoff}
Chain options:
1. Continue with current handoff (recommended)
2. Show chain history (list all linked handoffs)
3. Jump to earlier handoff in chain
```

To show full chain:
```bash
# Read prior_handoff field, follow links recursively
# Build chain: current -> prior -> prior's prior -> ...
# Present as timeline
```

**Chain Display Format:**
```
Handoff Chain (newest first):
├─ 2026-01-14_skill-loading.yaml (current)
│  Goal: Dynamic skill loading system
│
├─ 2026-01-13_context-rotation.yaml
│  Goal: Context rotation improvements
│
└─ 2026-01-12_clorch-improvements.yaml
   Goal: General Clorch enhancements
```

4. **Use TodoWrite** to track the action items

5. **Route to specialist agent** based on task type:
   - Bug fix → `spark` or `sleuth`
   - Feature → `kraken` or `architect`
   - Research → `scout` or `oracle`
   - Tests → `arbiter` or `atlas`

## Parameters

If invoked with a path or ticket number:
- `/resume path/to/handoff.yaml` → Resume from that specific handoff
- `/resume ENG-1234` → Find and resume from most recent handoff for that ticket

Look for handoffs in (priority order):
1. `thoughts/shared/handoffs/` (current directory)
2. `../thoughts/shared/handoffs/` (parent - for ~/.claude/opc case)
3. `.claude/memory/handoff.md` (simple handoff)

## Guidelines

1. **Be thorough**: Read entire handoff, verify all references
2. **Be interactive**: Present findings, get confirmation before acting
3. **Leverage wisdom**: Apply learnings, avoid documented failures
4. **Track progress**: Use TodoWrite for task continuity
5. **Validate state**: Never assume handoff matches current codebase

## Clorch Workspace Structure

Clorch development uses `~/.claude/` as the root workspace:

| Path | Purpose |
|------|---------|
| `~/.claude/thoughts/shared/handoffs/` | Clorch handoffs |
| `~/.claude/opc/` | OPC tools and scripts |
| `~/.claude/hooks/` | Clorch hooks |
| `~/.claude/commands/` | Clorch skills/commands |

When running from `~/.claude/opc/`, handoffs are at `../thoughts/shared/handoffs/`
