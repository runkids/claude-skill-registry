---
name: docs-updater
description: Expert assistant for keeping documentation synchronized with code changes in the KR92 Bible Voice project. Use when updating API docs, maintaining architecture diagrams, syncing README, updating CLAUDE.MD, or generating documentation from code.
invocable: true
cron: true
---

# Docs Updater

Keep documentation in sync with code. Generates concise, user-friendly summaries.

## Context Files (Read First)

For current state, read from `Docs/context/`:
- `Docs/context/conventions.md` - Documentation standards
- `Docs/context/repo-structure.md` - File organization
- `Docs/ai/CHANGELOG.md` - Recent changes to sync

## Quick Summary Format

Every doc should start with a **TL;DR section** for human readers:

```markdown
# Document Title

> **TL;DR:** [1-2 sentence summary of what this covers]
>
> **Key Points:**
> - [Most important fact 1]
> - [Most important fact 2]
> - [Most important fact 3]
>
> **Quick Links:** [Table](#tables) | [RPC](#rpc-functions) | [Edge Functions](#edge-functions)
```

## Documentation Files

| Doc | Purpose | Update Trigger |
|-----|---------|----------------|
| `CLAUDE.MD` | AI context | Architecture changes |
| `README.md` | Project overview | Feature/setup changes |
| `Docs/01-PRD.md` | Requirements | Vision changes |
| `Docs/02-DESIGN.md` | Architecture | System design changes |
| `Docs/03-API.md` | API contracts | DB/RPC/Edge changes |
| `Docs/06-AI-ARCHITECTURE.md` | AI system | AI feature changes |
| `Docs/07-ADMIN-GUIDE.md` | Admin panel | Admin changes |
| `Docs/13-SUBSCRIPTION-SYSTEM.md` | Plans/quotas | Subscription changes |

## Cron/Scheduled Invocation

This skill supports automated execution for documentation audits.

### Invocation Modes

**Manual:** `claude /docs-updater "check api docs are current"`

**Scheduled (cron):** Set up with CI/CD or cron job:
```bash
# Weekly docs audit (Sundays at midnight)
0 0 * * 0 claude --skill docs-updater --task "audit" --output report.md

# Pre-release docs check
claude --skill docs-updater --task "release-check" --output docs-status.md
```

### Supported Tasks

| Task | Description | Output |
|------|-------------|--------|
| `audit` | Check all docs for staleness | Markdown report |
| `release-check` | Pre-release documentation verification | Pass/fail + issues |
| `sync-schemas` | Update docs from database schema | Updated doc files |
| `generate-api` | Generate API docs from Edge Functions | API documentation |

### Audit Report Format

```markdown
# Documentation Audit Report
Generated: 2026-01-08

## Summary
- Total docs: 15
- Up-to-date: 12
- Needs update: 3
- Critical: 1

## Issues Found

### Critical
- [ ] `03-API.md`: Missing `token_pools` table (added 2026-01-07)

### Warnings
- [ ] `02-DESIGN.md`: Edge Function list outdated
- [ ] `07-ADMIN-GUIDE.md`: Missing Subscriptions page section

## Recommendations
1. Run `sync-schemas` to update API docs
2. Add new admin page to guide
```

## Writing User-Friendly Summaries

### Good Summary (DO)
```markdown
> **TL;DR:** Token-based quota system limits AI usage per subscription plan.
>
> **Key Points:**
> - Users get tokens per 6-hour window (Guest: 50, Pro: 500)
> - Each AI operation costs fixed tokens (Search: 20, Study: 100)
> - Admin can adjust all limits via `/admin/subscriptions`
```

### Bad Summary (DON'T)
```markdown
## Overview
This document describes the token pool subscription system architecture
which was redesigned from a complex per-feature quota model...
```

## Update Workflow

1. **Identify change type** → Which docs affected?
2. **Update TL;DR first** → Most critical information
3. **Update details** → Tables, examples, diagrams
4. **Cross-reference** → Update related docs
5. **Validate** → Run audit task

## References

- **Update examples**: See [references/examples.md](references/examples.md)
- **Doc templates**: See [references/templates.md](references/templates.md)
- **Quality checklist**: See [references/checklist.md](references/checklist.md)
