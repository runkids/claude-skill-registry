---
name: checkpoint
description: Save session progress to Linear and generate a handoff prompt. Triggers on "checkpoint", "save progress", "hand off", "new chat", "context getting large". NOT for git operations - use /commit for that.
---

# Checkpoint Skill

Save session progress to Linear and generate a handoff prompt for continuing in a new chat.

> **⚠️ This is NOT a git commit.** Checkpoint is for **context management** - preserving session state for handoff to a new chat. Use `/commit` for git operations (staging, committing, pushing code). These are completely different workflows.

## When to Use

- Context window getting large (conversation > 50 messages)
- Switching topics or projects mid-session
- Before ending a long session
- User says "checkpoint", "save progress", "hand off"
- Proactively offer when detecting topic drift

## Invocation

```
/checkpoint                    # Auto-detect ticket, full checkpoint
/checkpoint DIS-322            # Target specific ticket
/checkpoint --no-clear         # Don't clear plan file after checkpoint
/checkpoint --slack            # Also post summary to Slack
```

---

## Workflow

### Step 1: Detect Active Ticket

See [workflows/ticket-detection.md](./workflows/ticket-detection.md) for full logic.

**Priority order:**
1. User-specified argument (e.g., `/checkpoint DIS-322`)
2. Explicit mention in conversation ("working on DIS-322")
3. Branch name pattern (`feature/dis-322-*`)
4. Most recently mentioned `DIS-XXX` in conversation
5. Fallback: Ask user with AskUserQuestion

**If multiple tickets detected:**
- List all found tickets
- Ask user which one(s) to checkpoint to

### Step 2: Gather Context

**First, check for pre-captured context from the context-decision-logger:**

```bash
# Read decisions.md if it exists (captured by background agent at 70%, 55%, 40% thresholds)
cat .claude/session/decisions.md 2>/dev/null || echo "No pre-captured decisions"
```

If `decisions.md` exists, it contains sections for:
- Decisions made
- Blockers encountered
- Files touched
- Rationale
- Next steps

**Merge pre-captured content with conversation scan** - the pre-captured content provides a foundation, then scan recent messages (since last capture) for anything new.

Scan the conversation to build the **Context Summary**:

| Field | How to Extract |
|-------|----------------|
| **Original ask** | First user message or explicit task statement |
| **Approach** | Look for "using", "chose", "going with" + rationale |
| **Remaining** | TodoWrite items not completed, or explicit "still need to" |

Then extract supporting details:

| Pattern | What to Extract |
|---------|-----------------|
| `*.ts`, `*.md`, `*.json` paths | Files touched (include what changed) |
| `DIS-XXX` | Related Linear tickets |
| "?", "unclear", "need to decide" | Open questions |
| "next", "todo", "need to", "should" | Next steps |

### Step 2.5: Detect Investigation Mode

**Trigger conditions:**
- Blocker mentioned in conversation ("blocked", "stuck", "can't figure out")
- User invoked with `--investigate` flag
- Session involved significant debugging activity

**If investigation mode detected:**

1. Scan recent Grep/Read tool calls to extract file:line references
2. Group into categories:
   - Files that were repeatedly accessed (likely relevant)
   - Files where specific lines were examined
   - Error locations mentioned
3. Present suggestions to user:

```
## Investigation Context Detected

I found these file references from the session:

**Frequently accessed:**
- `src/components/Modal.tsx:45` - read 3 times
- `src/hooks/useAuth.ts:112` - read 2 times

**Error locations:**
- `src/api/client.ts:78` - error stack trace

Include in checkpoint? [Confirm all / Select specific / Skip]
```

4. User confirms which references to include
5. Include confirmed references in Investigation section of checkpoint

**Skip if:** No debugging activity detected and no `--investigate` flag.

### Step 3: Track Decisions

See [workflows/decision-tracking.md](./workflows/decision-tracking.md) for full logic.

**Process:**
1. Scan for decision patterns: "decided", "chose", "finalized", "will use"
2. Scan for reversal patterns: "actually", "instead", "changed to", "no longer"
3. Mark decisions as `CURRENT` or `SUPERSEDED`
4. Final output: flat list of current decisions with inline rationale

**Example output:**
```markdown
### Decisions
- Using SQLite because simpler for prototype
- Component-based architecture because matches existing patterns

*2 decisions superseded during session (not shown)*
```

### Step 4: Check for Spec Changes

Compare current understanding with ticket description:

```bash
# Get current ticket description
npx tsx .claude/tools/linear-cc/src/index.ts get-issue {TICKET}
```

**If spec changed during session:**
1. Detect changes: new acceptance criteria, revised approach, updated requirements
2. Auto-update ticket description:

```bash
npx tsx .claude/tools/linear-cc/src/index.ts update-issue {TICKET} \
  --description "{updated_description}"
```

3. Note in checkpoint comment: "Ticket description updated to reflect revised approach"

**Skip if:** No meaningful spec changes detected

### Step 5: Post to Linear (Living Document Model)

**Use the Living Document approach** - maintain ONE context document per ticket that gets UPDATED rather than creating new documents each time.

See [workflows/context-document.md](./workflows/context-document.md) for full details.

#### Step 5a: Check for Existing Context Document

```bash
# Check if [CONTEXT] document already exists
npx tsx .claude/tools/linear-cc/src/index.ts list-documents \
  --issue {TICKET} \
  --title "[CONTEXT]*"
```

#### Step 5b: Fetch and Merge (if exists)

```bash
# Get existing document content
npx tsx .claude/tools/linear-cc/src/index.ts get-document \
  --issue {TICKET} \
  --title "[CONTEXT]*"
```

Parse the response and merge:
1. **Decisions** - APPEND new, preserve existing
2. **Current Session** - REPLACE with new session content
3. **Session History** - Archive old "Current Session" here

#### Step 5c: Update or Create Document

**If document exists:**
```bash
# Write merged content to temp file
cat << 'EOF' > /tmp/context-update.md
{merged_content}
EOF

# Update existing document
npx tsx .claude/tools/linear-cc/src/index.ts update-document \
  --issue {TICKET} \
  --title-pattern "[CONTEXT]*" \
  --file /tmp/context-update.md
```

**If no document exists:**
```bash
npx tsx .claude/tools/linear-cc/src/index.ts create-document \
  "[CONTEXT] {TICKET}" \
  --issue {TICKET} \
  --file /tmp/checkpoint-content.md
```

**Document structure:**
```markdown
# [CONTEXT] {TICKET}

## Decisions
> Key decisions with rationale. Append new, preserve existing.

- [YYYY-MM-DD] {Decision} because {rationale}

## Current Session
**Last Updated:** YYYY-MM-DD
**Status:** {In Progress | Blocked | Near Complete}

### Summary
{current work}

### Files Touched
- `{path}` - {what changed}

### Next Steps
1. {priority items}

## Session History
> Compressed summaries of previous sessions.

### Session {N} (YYYY-MM-DD)
- {Key accomplishment}
```

**Then post a brief comment** for timeline visibility:
```bash
npx tsx .claude/tools/linear-cc/src/index.ts create-comment {TICKET} \
  "📋 **Checkpoint updated** - context document refreshed."
```

**Error handling:** If Linear fails, warn and continue. Still generate handoff prompt.

### Step 5.5: Create Sub-Issues for Next Steps

**IMPORTANT:** Next steps should be stored as Linear sub-issues, not just in the checkpoint comment or plan file.

For each remaining task identified:
1. Create a sub-issue under the parent ticket
2. Use appropriate type prefix (`[BUG]`, `[FEAT]`, `[IMPROVE]`)
3. Include file paths and implementation hints in description
4. Link to parent ticket in description

```bash
npx tsx .claude/tools/linear-cc/src/index.ts create-issue "[TYPE] Short description" \
  --description "Details...

**Parent:** {TICKET}" \
  --label {appropriate_label}
```

**Why sub-issues over plan file:**
- Sub-issues persist across sessions
- Sub-issues are visible in Linear board
- Sub-issues can be assigned, prioritized, tracked
- Plan file is ephemeral and session-specific

**Skip if:** No meaningful next steps identified

### Step 5.6: Upload Session Transcript

Create a snapshot of the conversation transcript for reference.

```bash
npx tsx .claude/skills/checkpoint/scripts/transcript.ts \
  --session {sessionId} \
  --ticket {TICKET}
```

**Response format:**
```json
{
  "success": true,
  "documentId": "...",
  "url": "https://linear.app/...",
  "messageCount": 42
}
```

Include the transcript URL in the checkpoint comment (see template).

**Note:** The transcript includes only user/Claude text messages (no tool calls, thinking, or system messages).

**Skip if:** Linear API is unavailable (warn and continue).

### Step 6: Generate Handoff Prompt

Create a copy-paste prompt using [templates/handoff-prompt.md](./templates/handoff-prompt.md).

Output this directly to the user with:
```
## Handoff Prompt

Copy this to a new Claude Code chat:

```
{handoff_prompt_content}
```
```

### Step 6.3: RalphLoop Detection

See [workflows/ralphloop-detection.md](./workflows/ralphloop-detection.md) for full logic.

**Check if remaining work is Ralph-able** (bounded + programmatically verifiable):

1. Scan remaining work (TodoWrite items, "Next Steps" from context)
2. Match against Ralph-able patterns:
   - Type errors → `npm run typecheck`
   - Test failures → `npm run test`
   - Build errors → `npm run build`
   - Lint errors → `npm run lint`

3. If Ralph-able, append to handoff prompt:

```markdown
## Auto-Continue (RalphLoop)

Remaining work is bounded with programmatic verification.
Run in a separate terminal:

\`\`\`bash
cd {project_dir} && \
MAX_ITER=10 ITER=0 && \
while [ $ITER -lt $MAX_ITER ] && ! {verify_command}; do
  claude --print "{prompt}"
  ITER=$((ITER + 1))
done && echo "✓ Done!" || echo "⚠ Max iterations reached"
\`\`\`

**Stop condition:** `{verify_command}` returns success
**Safety:** Max 10 iterations
```

**Skip if:** Remaining work requires human judgment, is exploratory, or has no programmatic verification.

### Step 6.5: Write Handoff File for Auto-Continue

Write the handoff prompt to `/tmp/claude-handoff.md` for use with the `ce` wrapper script:

```bash
cat << 'EOF' > /tmp/claude-handoff.md
{handoff_prompt_content}
EOF
```

Then tell the user:
```
✓ Handoff file written to /tmp/claude-handoff.md

**To continue in a new session:**
1. Exit this session (Ctrl+D or /exit)
2. Run: `ce`
```

**Note:** The `ce` script lives at `~/.local/bin/ce` and reads the handoff file to start a new session with context pre-loaded.

### Step 7: Clear Plan File

Unless `--no-clear` flag is used:

1. Read current plan file path (from system context)
2. Overwrite with minimal template:

```markdown
# Active Plan

> **Last Updated**: {date}
> **Linear**: {ticket}

No active task. Previous context checkpointed to {ticket}.
```

### Step 8: Reset Context Thresholds

After checkpoint is complete, reset the context logger state:

```bash
# Reset thresholds and clear decisions.md for fresh tracking
node scripts/context-watcher.js reset
```

This clears:
- `thresholds_fired` array in `current-ticket.json`
- `last_scanned_message_count` counter
- `decisions.md` file

This ensures the next session starts with fresh threshold tracking.

---

## Templates

- [templates/linear-comment.md](./templates/linear-comment.md) - `[CHECKPOINT]` comment format
- [templates/handoff-prompt.md](./templates/handoff-prompt.md) - Knowledge transfer prompt

## Workflows

- [workflows/ticket-detection.md](./workflows/ticket-detection.md) - How to find the right ticket
- [workflows/decision-tracking.md](./workflows/decision-tracking.md) - Handle decision reversals
- [workflows/context-document.md](./workflows/context-document.md) - Living document model for context persistence
- [workflows/ralphloop-detection.md](./workflows/ralphloop-detection.md) - Auto-continue for bounded, verifiable work

---

## Integration Points

| System | Integration |
|--------|-------------|
| Linear | Use living document model (`list-documents`, `get-document`, `update-document`), post brief comment, update description, **create sub-issues for experiments** via `linear-cc` |
| Slack | (Optional) Post summary via `slack-cc` |
| Plan file | Clear after checkpoint |
| TodoWrite | Clear todos after checkpoint |
| Handoff file | Write to `/tmp/claude-handoff.md` for `claude-continue` script |
| Session file | Update `.claude/session/current-ticket.json` with context document ID |
| Context logger | Read `.claude/session/decisions.md` for pre-captured context, then `reset` via `context-watcher.js` |

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| No ticket detected | Ask user which ticket to use |
| Multiple tickets found | List them, let user choose |
| Linear API failure | Warn, still generate handoff prompt |
| Plan file doesn't exist | Skip clearing step |
| Slack failure | Warn and continue |
| Spec update fails | Warn, continue with comment only |

---

## Examples

**Basic checkpoint:**
```
User: /checkpoint
Claude: Detected DIS-322 from conversation.

Gathering context...
- Original ask: Implement user authentication
- Approach: JWT with httpOnly cookies
- 3 decisions made (1 superseded)
- 4 files touched

Posting checkpoint to Linear...
✓ Comment posted to DIS-322

## Handoff Prompt

Copy this to a new Claude Code chat:

# Context Recovery: DIS-322 User Authentication
...
```

**With spec update:**
```
User: /checkpoint DIS-360
Claude: Posting checkpoint to DIS-360...

Detected spec changes:
- Added acceptance criteria for decision tracking
- Revised approach from flag-based to automatic

Updating ticket description...
✓ Description updated
✓ Comment posted to DIS-360

## Handoff Prompt
...
```

**Keep plan file:**
```
User: /checkpoint --no-clear
Claude: Checkpointing without clearing plan file...
```
