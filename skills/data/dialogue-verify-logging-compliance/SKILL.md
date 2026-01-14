---
name: dialogue-verify-logging-compliance
description: Verify that required logging occurred during a process execution. Use before presenting work for approval to ensure decisions and observations were captured. Triggers on "verify logging", "check compliance", "validate logs".
allowed-tools: Bash, Read
---

# Dialogue: Verify Logging Compliance

Validate that required decision and observation logging occurred during process execution.

## When to Use

Use this skill:
- Before presenting work for human approval
- As a validation step in capability flows
- When auditing whether dialogue protocol was followed

## What It Checks

The verification checks for:

| Log Type | Minimum Expected | Purpose |
|----------|------------------|---------|
| **Decisions** | ≥1 per significant choice | Ensures rationale is captured |
| **Observations** | ≥1 for context elicitation | Ensures inputs are recorded |

## How to Verify

### Option 1: Quick Check (Manual)

Review the logs directly:

```bash
# Count recent decisions with a specific context/tag
grep -c "context.*<process-identifier>" .dialogue/logs/decisions.yaml

# Count recent observations with a specific context/tag
grep -c "context.*<process-identifier>" .dialogue/logs/observations.yaml
```

### Option 2: Script-Based Verification

Execute the verification script:

```bash
.claude/skills/dialogue-verify-logging-compliance/scripts/verify-logging.sh <process-identifier> <min-decisions> <min-observations>
```

#### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `process-identifier` | String to search for in context/tags | "Process Architect v2" |
| `min-decisions` | Minimum decision entries expected | 5 |
| `min-observations` | Minimum observation entries expected | 2 |

#### Example

```bash
.claude/skills/dialogue-verify-logging-compliance/scripts/verify-logging.sh "Process Architect v2 simulation" 5 2
```

## Output

The script returns:
- **PASS** if minimums are met, with counts
- **FAIL** if any minimum not met, with details

Example output:
```
Verifying logging compliance for: Process Architect v2 simulation
---
Decisions found: 5 (minimum: 5) ✓
Observations found: 2 (minimum: 2) ✓
---
PASS: Logging compliance verified
```

## Escalation

If verification fails:
1. Identify which log type is deficient
2. Return to the relevant process step to add missing entries
3. Re-run verification before proceeding

## Integration with Process Flows

Add a verification step before approval gates:

```
Step X: Verify Logging Compliance
├── Capability: Validate
├── Pattern: AI-Only
├── AI role: Run verification script; report results
├── Escalation triggers: Verification fails (missing entries)
├── Completion criteria: All minimums met
└── Validation: Script returns PASS
```

---

*Part of the AI-Augmented SDLC Framework dialogue system*
