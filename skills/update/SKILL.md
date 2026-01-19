---
description: Update Clorch to the latest version
---

# Update Clorch

Update your Clorch installation to the latest version.

## Process

### Step 1: Check Current Version

```bash
# Get current installed version
current=$(cat ~/.claude/VERSION 2>/dev/null || echo "unknown")
echo "Current version: $current"

# Get latest version from GitHub
latest=$(curl -s https://api.github.com/repos/namesreallyblank/Clorch/releases/latest 2>/dev/null | grep '"tag_name"' | sed 's/.*"v\([^"]*\)".*/\1/' || echo "unknown")
echo "Latest version: $latest"
```

### Step 2: Compare Versions

If current == latest:
```
╭─────────────────────────────────────╮
│ ✓ Clorch is up to date (v{version}) │
╰─────────────────────────────────────╯
```

If current < latest:
```
╭─────────────────────────────────────╮
│ ⚡ Update available: v{current} → v{latest}
│
│ Changes in v{latest}:
│ {changelog summary}
│
│ Update now? (y/n)
╰─────────────────────────────────────╯
```

### Step 3: Perform Update (if confirmed)

```bash
# Find Clorch installation directory
CLORCH_DIR="${CLORCH_SOURCE:-$HOME/Projects/Clorch}"

if [ -d "$CLORCH_DIR/.git" ]; then
    echo "Updating from $CLORCH_DIR..."
    cd "$CLORCH_DIR"
    git fetch origin
    git pull origin main
    ./install.sh
    echo "Update complete!"
else
    echo "Clorch source not found at $CLORCH_DIR"
    echo "Set CLORCH_SOURCE environment variable to your Clorch repo path"
    echo "Or clone fresh: git clone https://github.com/namesreallyblank/Clorch.git"
fi
```

### Step 4: Verify Update

```bash
# Confirm new version
new_version=$(cat ~/.claude/VERSION 2>/dev/null)
echo "Now running Clorch v$new_version"
```

## Parameters

- `/update` - Check and update interactively
- `/update --check` - Only check, don't update
- `/update --force` - Update without confirmation

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `CLORCH_SOURCE` | `~/Projects/Clorch` | Path to Clorch git repo |

## What Gets Updated

- Global skills in `~/.claude/skills/`
- Global agents in `~/.claude/agents/`
- Global hooks in `~/.claude/hooks/`
- Global rules in `~/.claude/rules/`
- VERSION file

**Note:** Project-specific agents in `.claude/agents/` are NOT touched. Use `/update-project` after updating to sync project agents.

## Post-Update

After updating:
1. **Restart Claude Code** - Required to load new skills/agents
2. **Run `/update-project`** - Update project-specific agents (optional)
3. **Check changelog** - See what's new in the update
