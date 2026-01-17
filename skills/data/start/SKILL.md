---
description: Initialize Clorch in a new or existing workspace
invokes: orchestration
---

# Start Clorch

Initialize Clorch in a workspace - whether empty or with existing code.

## Process

### Step 0: Load Orchestration

```
Use Skill tool: skill="orchestration"
```

### Step 1: Detect Workspace State

```bash
# Check if workspace has code
file_count=$(find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" -o -name "*.rs" -o -name "*.java" \) 2>/dev/null | head -100 | wc -l)

# Check if Clorch already initialized
has_clorch=$(ls -d .claude 2>/dev/null && echo "yes" || echo "no")

echo "Files: $file_count, Clorch: $has_clorch"
```

### Step 2: Route Based on State

#### 2a. Empty Project (no code files)

Display welcome banner and set up infrastructure:

```
   ─────────────────◆─────────────────
           ░█████╗░██╗░░░░░░█████╗░██████╗░░█████╗░██╗░░██╗
           ██╔══██╗██║░░░░░██╔══██╗██╔══██╗██╔══██╗██║░░██║
           ██║░░╚═╝██║░░░░░██║░░██║██████╔╝██║░░╚═╝███████║
           ██║░░██╗██║░░░░░██║░░██║██╔══██╗██║░░██╗██╔══██║
           ╚█████╔╝███████╗╚█████╔╝██║░░██║╚█████╔╝██║░░██║
           ░╚════╝░╚══════╝░╚════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
   ─────────────────◆─────────────────

         Parallel agent orchestration for Claude Code

   ─────────────────◆─────────────────
```

Then set up infrastructure:

```bash
# Create Clorch directories
mkdir -p .claude/agents
mkdir -p .claude/memory
mkdir -p .claude/hooks
mkdir -p thoughts/shared/handoffs
mkdir -p thoughts/shared/plans
```

Present:
```
Clorch initialized in empty workspace.

Created:
├── .claude/
│   ├── agents/      (project-specific agents - empty for now)
│   ├── memory/      (session state)
│   └── hooks/       (project hooks)
└── thoughts/
    └── shared/
        ├── handoffs/  (session handoffs)
        └── plans/     (implementation plans)

Start coding! Once you have code, run `/start` again to generate
project-specific agents based on your codebase.

What would you like to build?
```

#### 2b. Existing Codebase (has code files)

Display banner, then run project-init:

```
   ─────────────────◆─────────────────
           ░█████╗░██╗░░░░░░█████╗░██████╗░░█████╗░██╗░░██╗
           ██╔══██╗██║░░░░░██╔══██╗██╔══██╗██╔══██╗██║░░██║
           ██║░░╚═╝██║░░░░░██║░░██║██████╔╝██║░░╚═╝███████║
           ██║░░██╗██║░░░░░██║░░██║██╔══██╗██║░░██╗██╔══██║
           ╚█████╔╝███████╗╚█████╔╝██║░░██║╚█████╔╝██║░░██║
           ░╚════╝░╚══════╝░╚════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
   ─────────────────◆─────────────────

         Analyzing codebase...

   ─────────────────◆─────────────────
```

Then spawn project-init:

```python
Task(
    subagent_type="project-init",
    prompt="Analyze this codebase and generate project-specific agents in .claude/agents/",
    run_in_background=False
)
```

#### 2c. Already Initialized (has .claude/)

First, check if project-specific agents exist:

```bash
# Check for project agents
agent_count=$(ls .claude/agents/*.md 2>/dev/null | wc -l | tr -d ' ')
echo "Project agents: $agent_count"
```

**If no agents (agent_count == 0):**

```
Clorch initialized, but no project agents found.
Analyzing codebase to generate project-specific agents...
```

Then spawn project-init:

```python
Task(
    subagent_type="project-init",
    prompt="Analyze this codebase and generate project-specific agents in .claude/agents/",
    run_in_background=False
)
```

**If agents exist (agent_count > 0):**

```
Clorch already initialized in this workspace.

Project agents found: [list agent names]

Use:
- /resume      - Resume from last session
- /update-project - Update agents to latest standards
- /help        - See available commands
```

## Parameters

- `/start` - Auto-detect and initialize (runs project-init if agents missing)
- `/start --force` - Re-run project-init even if agents exist (regenerate)
- `/start --agents-only` - Skip infrastructure, just check/generate agents

## What Gets Created

### For Empty Projects
| Path | Purpose |
|------|---------|
| `.claude/agents/` | Project-specific agents (empty) |
| `.claude/memory/` | Session state files |
| `.claude/hooks/` | Project-specific hooks |
| `thoughts/shared/handoffs/` | Session handoffs |
| `thoughts/shared/plans/` | Implementation plans |

### For Existing Codebases
All of the above, plus:
- `stack-guardian.md` - Tech stack conventions
- `api-guardian.md` - API design patterns (if applicable)
- `domain-expert.md` - Business logic validation
- `test-guardian.md` - Testing patterns
- Additional agents based on codebase analysis

## Post-Start

After `/start`:
1. **Empty project**: Start coding, run `/start` again when ready for agents
2. **Existing codebase**: Restart Claude Code to load new agents, then work normally
