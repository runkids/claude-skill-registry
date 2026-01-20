---
description: Resume session with orchestration, memory, and handoff analysis (workspace-aware)
invokes: orchestration
---

# Resume Session

You are tasked with resuming work from a previous session.

## Invocation Modes

- `/resume` - Discover handoffs, show options, let user choose
- `/resume path/to/handoff.yaml` - Jump directly to that handoff
- `/resume ENG-1234` - Find and resume by ticket number

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

**Only proceed to Step 0.5 AFTER orchestration is loaded.**

### Step 0.5: Display Welcome Banner

```
   -----------------*-----------------
           CLAUDE
   -----------------*-----------------

         Resuming session...

   -----------------*-----------------
```

### Step 1: Check for Direct Path or Ticket

1. **If a handoff document path was provided**:
   - Skip discovery, go directly to Step 3 (handoff analysis)
   - Read the handoff document FULLY (no limit/offset)

2. **If a ticket number (like ENG-XXXX) was provided**:
   - Locate handoffs in `thoughts/shared/handoffs/ENG-XXXX/`
   - **If zero files or directory missing**: "I can't find that handoff. Please provide a path."
   - **If one file**: proceed with that handoff
   - **If multiple files**: use the most recent (by `YYYY-MM-DD_HH-MM-SS` in filename)
   - Go directly to Step 3 (handoff analysis)

3. **If no parameters provided**: continue to Step 2 (discovery)

---

### Step 2: Discover Available Handoffs

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

**Present Findings:**

#### If structured handoffs exist:
```
Found structured handoff(s):
- {path1} ({date})
- {path2} ({date})

Would you like to:
1. Resume from most recent handoff: {path}
2. Choose a different handoff
3. Start fresh (ignore handoffs)

Tip: You can invoke directly: `/resume thoughts/shared/handoffs/ENG-XXXX/file.yaml`
or by ticket: `/resume ENG-XXXX`
```

If user chooses to resume from a handoff, proceed to Step 3.

#### If only simple handoff exists:
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

---

### Step 3: Full Handoff Analysis and Validation

**CRITICAL: This is where deep analysis happens. Do NOT use sub-agents to read critical files.**

1. **Read handoff document completely** (no limit/offset)

2. **Read linked documents immediately**:
   - Read any research or plan documents linked under `thoughts/shared/plans` or `thoughts/shared/research`
   - Do NOT use a sub-agent for these critical files

3. **Extract and verify**:
   - Tasks and their statuses
   - Recent changes (verify they still exist in codebase)
   - Learnings and decisions
   - Artifacts and file references
   - Action items and next steps
   - Chain history (if `prior_handoff:` exists)

4. **Spawn focused research tasks** for verification:
   Based on the handoff content, spawn parallel research tasks to verify current state:

   ```
   Task - Gather artifact context:
   Read all artifacts mentioned in the handoff.
   1. Read feature documents listed in "Artifacts"
   2. Read implementation plans referenced
   3. Read any research documents mentioned
   4. Extract key requirements and decisions
   Use tools: Read
   Return: Summary of artifact contents and key decisions
   ```

5. **Wait for ALL sub-tasks to complete** before presenting

6. **Present comprehensive analysis**:
   ```
   I've analyzed the handoff from {date}:

   **Original Tasks:**
   - [Task 1]: [Status from handoff] -> [Current verification]
   - [Task 2]: [Status from handoff] -> [Current verification]

   **Key Learnings Validated:**
   - [Learning with file:line reference] - [Still valid/Changed]
   - [Pattern discovered] - [Still applicable/Modified]

   **Recent Changes Status:**
   - [Change 1] - [Verified present/Missing/Modified]
   - [Change 2] - [Verified present/Missing/Modified]

   **What Worked / What Failed:**
   - Worked: {approaches from handoff}
   - Failed: {approaches to avoid}

   **History Chain:** (if prior_handoff exists)
   - Previous: {prior_handoff path} - {prior goal}
   - [View full chain history]

   **Recommended Next Actions:**
   Based on the handoff's `now:` field or `next:` list:
   1. {Most logical next step}
   2. {Second priority action}
   3. {Additional tasks discovered}

   **Potential Issues Identified:**
   - {Any conflicts or regressions found}
   - {Missing dependencies or broken code}

   Shall I proceed with action 1?
   ```

---

### Step 4: Chain Traversal (if prior_handoff exists)

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
|- 2026-01-14_skill-loading.yaml (current)
|  Goal: Dynamic skill loading system
|
|- 2026-01-13_context-rotation.yaml
|  Goal: Context rotation improvements
|
+- 2026-01-12_clorch-improvements.yaml
   Goal: General Clorch enhancements
```

---

### Step 5: Create Action Plan

1. **Use TodoWrite to create task list**:
   - Convert action items from handoff into todos
   - Add any new tasks discovered during analysis
   - Prioritize based on dependencies and handoff guidance

2. **Present the plan**:
   ```
   I've created a task list based on the handoff and current analysis:

   [Show todo list]

   Ready to begin with the first task: [task description]?
   ```

---

### Step 6: Route to Specialist Agent

**CRITICAL: Do NOT implement directly. Always spawn via Task tool.**

1. **Analyze task type and select specialist agent**:

   **Leads (can spawn workers):**
   | Agent | Domain | Use For |
   |-------|--------|---------|
   | `kraken` | implement | Large features, new systems, major components |
   | `architect` | plan | Feature design, system architecture, implementation planning |
   | `phoenix` | plan | Refactoring plans, migrations, codebase restructuring |
   | `herald` | deploy | Releases, deployments, publishing |
   | `maestro` | orchestrate | Complex multi-agent workflows |

   **Workers (focused specialists):**
   | Agent | Domain | Use For |
   |-------|--------|---------|
   | `spark` | implement | Quick fixes, patches, minor tweaks |
   | `scribe` | document | Documentation, guides, explanations |
   | `sleuth` | debug | Bug investigation, tracing, root cause analysis |
   | `aegis` | debug | Security audits, vulnerability scanning |
   | `profiler` | debug | Performance optimization, bottleneck analysis |
   | `arbiter` | validate | Unit tests |
   | `atlas` | validate | E2E/integration tests |
   | `oracle` | research | External docs, best practices, how-to |
   | `scout` | research | Codebase exploration, finding existing code |
   | `pathfinder` | research | Repository structure analysis |
   | `plan-reviewer` | review | Feature plan review, design validation |
   | `chronicler` | session | Session analysis, history summaries |

2. **Spawn the specialist via Task tool**:
   ```
   Use Task tool with:
   - subagent_type: [selected agent from above]
   - prompt: [task description + relevant handoff context + learnings]
   ```

3. **Include handoff context in the prompt**:
   - Key learnings from the handoff
   - File references with line numbers
   - Patterns to follow
   - Pitfalls to avoid

4. **Wait for agent completion**, then proceed to next task

---

## Guidelines

1. **Be Thorough in Analysis**:
   - Read the entire handoff document first
   - Verify ALL mentioned changes still exist
   - Check for any regressions or conflicts
   - Read all referenced artifacts

2. **Be Interactive**:
   - Present findings before starting work
   - Get buy-in on the approach
   - Allow for course corrections
   - Adapt based on current state vs handoff state

3. **Leverage Handoff Wisdom**:
   - Pay special attention to "Learnings" section
   - Apply documented patterns and approaches
   - Avoid repeating mistakes mentioned
   - Build on discovered solutions

4. **Track Continuity**:
   - Use TodoWrite to maintain task continuity
   - Reference the handoff document in commits
   - Document any deviations from original plan
   - Consider creating a new handoff when done

5. **Validate Before Acting**:
   - Never assume handoff state matches current state
   - Verify all file references still exist
   - Check for breaking changes since handoff
   - Confirm patterns are still valid

---

## Common Scenarios

### Scenario 1: Clean Continuation
- All changes from handoff are present
- No conflicts or regressions
- Clear next steps in action items
- Proceed with recommended actions

### Scenario 2: Diverged Codebase
- Some changes missing or modified
- New related code added since handoff
- Need to reconcile differences
- Adapt plan based on current state

### Scenario 3: Incomplete Handoff Work
- Tasks marked as "in_progress" in handoff
- Need to complete unfinished work first
- May need to re-understand partial implementations
- Focus on completing before new work

### Scenario 4: Stale Handoff
- Significant time has passed
- Major refactoring has occurred
- Original approach may no longer apply
- Need to re-evaluate strategy

---

## Clorch Workspace Structure

Clorch development uses `~/.claude/` as the root workspace:

| Path | Purpose |
|------|---------|
| `~/.claude/thoughts/shared/handoffs/` | Clorch handoffs |
| `~/.claude/opc/` | OPC tools and scripts |
| `~/.claude/hooks/` | Clorch hooks |
| `~/.claude/commands/` | Clorch skills/commands |

When running from `~/.claude/opc/`, handoffs are at `../thoughts/shared/handoffs/`

Look for handoffs in (priority order):
1. `thoughts/shared/handoffs/` (current directory)
2. `../thoughts/shared/handoffs/` (parent - for ~/.claude/opc case)
3. `.claude/memory/handoff.md` (simple handoff)
