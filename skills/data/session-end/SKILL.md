---
name: session-end
description: Generate end-of-session documentation for paleoseismic research. Use at end of work session to update SESSION_LOG.md and GAPS_AND_PRIORITIES.md. Triggers on "end session", "session summary", "wrap up", "document session".
---

# /session-end - Session Documentation Skill

## Purpose

Generate end-of-session documentation to update `memory/SESSION_LOG.md` and mark completed tasks in `GAPS_AND_PRIORITIES.md`. Ensures all work is properly recorded for continuity.

## Usage

```
/session-end [optional: brief description of session focus]
```

**Examples:**
```
/session-end                              # Auto-infer from conversation
/session-end "Brazil dark earthquake verification"
/session-end "Yok Balum 1976 validation failure analysis"
```

## Workflow

### Step 1: Gather Session Information

Review the conversation to identify:

1. **Focus**: What was the main task/question this session?
2. **Key Findings**: What discoveries, reclassifications, or insights emerged?
3. **Files Modified**: Which files were created/updated?
4. **Tasks Completed**: Which GAPS_AND_PRIORITIES.md tasks were finished?
5. **New Tasks Discovered**: What new work items emerged?
6. **Blocking Issues**: What is preventing progress?
7. **Next Priority**: What should the next session focus on?

### Step 2: Generate SESSION_LOG.md Entry

Format entry following the established pattern:

```markdown
## YYYY-MM-DD | [SHORT TITLE]: [Key Finding]

**Focus**: [What the session aimed to accomplish]

### Key Finding: [Most Important Discovery]

[1-3 paragraph description of the main finding, with tables if relevant]

| Column1 | Column2 | Column3 |
|---------|---------|---------|
| data    | data    | data    |

### [Additional Findings]

[Other significant work done]

### Files Updated

| File | Change |
|------|--------|
| `path/to/file.md` | [Brief description of change] |
| `another/file.md` | [Brief description of change] |

### Statistics Update (if applicable)

[Any changes to project statistics - detection rates, event counts, etc.]

### Next Priority

[What should be tackled next, any blocking issues]

---
```

### Step 3: Update GAPS_AND_PRIORITIES.md

For each completed task:
1. Change task line to add `✅ COMPLETE` or strikethrough `~~TaskCode~~`
2. Add completion date if relevant
3. Add pointer to created documentation

For new tasks discovered:
1. Add to appropriate section with new task code
2. Include notes and cross-references

### Step 4: Present for Approval

Show the user:
1. Proposed SESSION_LOG.md entry
2. Proposed GAPS_AND_PRIORITIES.md changes
3. Ask for approval before writing

## Entry Format Guidelines

### Title Format
```
## YYYY-MM-DD | [CODE] [STATUS]: [Key Finding]
```

**Examples:**
- `## 2026-01-03 | IC1 COMPLETE: Pallett Creek Confirms ~1285 CE SAF`
- `## 2024-12-30 | ~1075 CE RECLASSIFIED: "Drought" → SEISMIC CANDIDATE`
- `## 2024-12-30 | "RIDLEY PARADOX" RESOLVED - Maya Mountains Local Fault`

### Files Updated Table
Always include this table - it's critical for tracking changes:

```markdown
| File | Change |
|------|--------|
| `regions/italy/THE_1394_DARK_EARTHQUAKE.md` | Added DISS verification section |
| `DARK_EARTHQUAKE_AUDIT.md` | New Caribbean audit entry |
| `PAPER_2_DARK_EARTHQUAKES.md` | Section 5.2 updated with findings |
| `CLAUDE.md` | Statistics table updated |
```

### Key Finding Format
For discoveries/reclassifications:
- State the finding clearly in 1 sentence
- Provide supporting data in a table
- Explain significance in 1-2 sentences

### Next Priority Format
```markdown
### Next Priority

[Task code from GAPS]: [Brief description]

**Blocking issues** (if any):
- [Issue 1]
- [Issue 2]
```

## Output Format

The skill outputs:

1. **SESSION_LOG.md entry** (ready to prepend)
2. **GAPS_AND_PRIORITIES.md changes** (specific edits)
3. **Summary** of session statistics

Then asks for approval to:
- Write entry to SESSION_LOG.md (prepend after header)
- Edit GAPS_AND_PRIORITIES.md (mark completions, add new tasks)

## Example Output

```
📝 SESSION DOCUMENTATION

Generated entry for SESSION_LOG.md:

---
## 2026-01-03 | DARK_EARTHQUAKE_AUDIT: Global Verification Complete

**Focus**: Audit all dark earthquake claims against modern fault databases

### Key Finding: Only 4 TRUE Dark Earthquakes

| Region | Event(s) | Classification | Reason |
|--------|----------|----------------|--------|
| Italy 1394 | ~1394 CE | **TRUE DARK** | NNW/SW faults not in ANY database |
| Brazil | ~96, ~867, ~1006 CE | **TRUE DARK** | No fault databases exist |
| California | 1741, 1580, 1825 | Pre-Historical | Faults ARE mapped (SCEC CFM) |
| Caribbean | ~1400, ~1062 CE | Pre-Columbian | Faults ARE mapped (GEM CCAF-DB) |

### Files Updated

| File | Change |
|------|--------|
| `DARK_EARTHQUAKE_AUDIT.md` | Complete global audit |
| `CLAUDE.md` | Updated definitions |
| `regions/brazil/BRAZIL_FAULT_DATABASE_RESEARCH.md` | New file |

### Next Priority

MS5: Update papers with fault database verification findings

---

GAPS_AND_PRIORITIES.md changes:
- ✅ Mark MS5 as COMPLETE
- Add new task: "Update California terminology (Pre-Spanish, not dark)"

Write these updates? [Y/n]
```

## Important Notes

1. **Newest entries at top** - SESSION_LOG.md has reverse chronological order
2. **Be specific** - Include file paths, task codes, specific findings
3. **Cross-reference** - Always link to detailed documentation
4. **Don't duplicate** - Put analysis in regional files, summaries in session log
5. **Track statistics** - Note any changes to detection rates, event counts
6. **Identify blockers** - Document what's preventing progress

## Files Modified

| File | Action |
|------|--------|
| `paleoseismic_caves/memory/SESSION_LOG.md` | Prepend new entry |
| `paleoseismic_caves/GAPS_AND_PRIORITIES.md` | Mark completions, add tasks |
| `paleoseismic_caves/memory/FACTS.md` | Add new verified facts (optional) |
| `paleoseismic_caves/memory/DEAD_ENDS.md` | Add failed approaches (optional) |
