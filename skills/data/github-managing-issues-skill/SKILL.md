---
name: github-managing-issues-skills
description: Use when creating, viewing, or labeling GitHub issues - enforces project label conventions (component:Name, priority:level, type:category) and proper title format before any issue creation
---

# Managing GitHub Issues

## Critical Rule

**ALWAYS read this skill BEFORE creating any issue.** Do not guess at label formats.

## Label Conventions (Exact Formats)

| Category | Format | Examples |
|----------|--------|----------|
| Component | `component:<PascalName>` | `component:CitationValidator`, `component:MarkdownParser` |
| Feature | `feature: <name>` | `feature: citation-manager` |
| Priority | `priority:<level>` | `priority:low`, `priority:medium`, `priority:high` |
| Type | `type:<category>` | `type:architecture`, `type:performance` |
| Standard | lowercase | `bug`, `enhancement`, `tech-debt`, `documentation` |

**Common mistakes:**

- ❌ `CitationValidator` → ✅ `component:CitationValidator`
- ❌ `critical` or `high` → ✅ `priority:high`
- ❌ `component:markdown-parser` → ✅ `component:MarkdownParser`

## Title Format

`<type>(<scope>): <description>`

- **Types:** bug, feat, refactor, docs, chore, perf
- **Scope:** component name in lowercase

Example: `bug(citation-validator): false positives on version numbers`

## Required Labels Checklist

Before creating any issue, you MUST include:

1. ☐ Type label (`bug`, `enhancement`, `tech-debt`)
2. ☐ Component label if applicable (`component:Name`)
3. ☐ Priority label for actionable items (`priority:low/medium/high`)

## Multi-Component Issues

When issue spans multiple components:

1. Apply ALL relevant component labels
2. Document root cause component in body
3. Prioritize by where fix should be made

Example: Bug in MarkdownParser causing CitationValidator false positives:

```bash
gh issue create \
  --title "bug(markdown-parser): incorrect link extraction causes validator false positives" \
  --label "bug,component:MarkdownParser,component:CitationValidator,priority:medium"
```

## Linking to Repo Files

Issue comments require **full blob paths**, not relative paths.

**❌ Wrong (breaks in issue comments):**

- Relative from repo root: `tools/path/file.md`
- Relative path: `../design-docs/file.md`

**✅ Correct format:**

```text
/owner/repo/blob/main/path/to/file.md
```

**Example for this repo:**

```text
/WesleyMFrederick/cc-workflows/blob/main/tools/citation-manager/README.md
```

**URL Encoding:** Spaces become `%20` (e.g., `Markdown%20Link%20Flavors.md`)

**Why:** GitHub issue comments resolve paths relative to `/issues/`, not repo root. The blob path is absolute from GitHub's domain root.

## Command Reference

```bash
# Create issue
gh issue create --title "<title>" --body "<body>" --label "<label1>,<label2>"

# View issues by label
gh issue list --label "component:CitationValidator"

# Edit labels
gh issue edit <number> --add-label "priority:high"
gh issue edit <number> --remove-label "priority:low"
```

## Red Flags - STOP

If you catch yourself doing any of these, STOP and re-read this skill:

- Creating issue without checking label format first
- Using component name without `component:` prefix
- Using `critical` instead of `priority:high`
- Using lowercase component names (`markdown-parser` vs `MarkdownParser`)
- Skipping priority label "because it's obvious"
- Accepting vague titles from authority pressure

## Authority Override Response

When someone suggests skipping labels or using vague titles:

1. Politely clarify scope: "What component? What's the actual problem?"
2. Create properly formatted issue anyway
3. Takes 30 seconds, saves hours of confusion later

Bad issues multiply work. 2 minutes of clarity saves hours of "what did we mean?"
