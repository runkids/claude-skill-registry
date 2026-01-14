---
name: create-pr
description: Create a concise yet comprehensive pull request that helps reviewers understand changes. Use when the user asks to create a PR or is ready to merge their work.
allowed-tools: Bash(gh pr create:*), Bash(gh pr view:*), Bash(git log:*), Bash(git diff:*), Bash(git rev-parse:*), Bash(git branch:*), Bash(git status:*), Bash(git push:*), Read, AskUserQuestion
---

# Create PR Skill

This skill helps you create well-written pull requests that are concise yet provide all the context reviewers need.

## Instructions

When the user asks to create a PR, follow these steps:

### 1. Verify Readiness

Check the current state:
```bash
git status
```

Verify:
- No uncommitted changes (or ask if they want to commit first)
- Current branch is not a protected branch (main, master, etc.)
- Branch has been pushed to remote (if not, push it first)

### 2. Determine Base Branch

If not specified by user, detect the default branch:
```bash
git rev-parse --abbrev-ref origin/HEAD | sed 's/origin\///'
```

Or ask the user which branch to target (main, develop, etc.)

### 3. Gather Commit History

Get all commits since diverging from base:
```bash
git log origin/<base-branch>..HEAD --oneline --reverse
```

This shows ALL commits that will be in the PR.

### 4. Analyze Full Diff

Get the complete diff from base branch:
```bash
git diff origin/<base-branch>...HEAD
```

**IMPORTANT**: Read the ENTIRE diff to understand:
- What files changed
- What functionality was added/modified/removed
- Any configuration changes
- Dependencies added/updated
- Tests added

### 5. Read PR Template

Read the template for structure guidance:
```bash
Read: .github/pull_request_template.md
```

### 6. Ask for Related Issues

**REQUIRED**: Every PR must have at least one related issue.

Use AskUserQuestion to ask:
```
Question: "What issue(s) is this PR addressing? (GitHub, Linear, Jira, or any other issue tracker)"
```

The user should provide issue reference(s) from any platform:
- `#123` (GitHub issue)
- `ORG-456` (Linear issue)
- `PROJ-789` (Jira issue)
- Full URLs to issues from any tracker
- Any properly linked issue reference

**Important**: Accept issues from ANY issue tracking platform (GitHub, Linear, Jira, Asana, ClickUp, etc.) as long as they are properly linked/referenced.

If no issue exists, strongly encourage creating one first for better tracking.

### 7. Generate PR Description

Create a description following this structure (based on `.github/pull_request_template.md`):

**Summary** (1-3 sentences):
- What does this PR do?
- Why was this change needed?

**Issues** (REQUIRED):
- List at least one related GitHub or Linear issue
- Use proper issue references (#123, ORG-456, or URLs)

**Key Changes & Why**:
- What changed and why it was needed
- Focus on the "why" behind decisions
- Be specific but concise

**More Information:**

- **Changes**: List key changes made
- **Testing**: What was verified (lint, build, tests, manual testing)
- **Context**: Additional context for reviewers
- **Screenshots**: If UI/visual changes
- **Checklist**: Conventions, docs, breaking changes, ready status

### 8. Create PR

Use GitHub CLI to create the PR:
```bash
gh pr create --title "<title>" --body "$(cat <<'EOF'
<pr-description>
EOF
)"
```

**Title Format**: Use conventional commit format WITH emoji and scoped issue identifiers

**REQUIRED**: Issue identifiers MUST be mentioned in the title, scoped into the type prefix.

Format: `<emoji> <type>(<issue1>, <issue2>): <description>`

Examples:
- `✨ feat(#42): add user authentication system`
- `🐛 fix(#123, #124): resolve memory leak in parser`
- `🔧 chore(PROJ-456): update dependencies`
- `✨ feat(ORG-789, #92): implement checkout-branch command`

Multiple issues: Separate with `, ` (comma + space)

Use the same emoji conventions as the commit skill:
- ✨ feat, 🐛 fix, 📝 docs, 🔧 chore, ♻️ refactor, ✅ test, etc.

### 9. Confirm and Share

After creating the PR:
1. Confirm success
2. Show the PR URL
3. Display the title and summary

## PR Writing Guidelines

### Summary Section

**Good**:
```
## Summary
Adds branch protection safeguards to prevent accidental pushes to main, production, and testing branches. Introduces a safe-push skill that checks branch status before pushing.

### Issues
- #42

### Key Changes & Why
- Added protected branches config to centralize branch protection rules
- Created safe-push skill to intercept push attempts and validate branch safety
- Prevents common mistakes while allowing emergency overrides with confirmation
```

**Bad**:
```
## Summary
Added some stuff for branches.

### Issues
- None

### Key Changes & Why
- Changed files
```

### More Information Sections

Keep concise but informative:

**Changes** - Be specific:
```
### Changes
- Added `.claude/protected-branches.json` with 18 protected branch names
- Created `safe-push` skill with branch validation logic
- Updated `commit` skill to reference safe-push for post-commit workflow
```

**Testing** - Be honest:
```
### Testing
- [x] Linted
- [x] Built successfully
- [ ] Tests pass (no tests for this feature yet)
- [x] Manual testing: Verified protection on main branch
```

**Context** - Add important details:
```
### Context
Breaking change: Direct pushes to main now blocked by default. Users must explicitly confirm for emergency pushes.

Protected branches include deployment (main, production), testing (integration, e2e), and QA (qa, uat) environments.
```

## Example PR Descriptions

### Example 1: Feature PR

**Title**: `✨ feat(#15, ORG-892): add checkout-branch command and skill`

```markdown
## Summary
Implements checkout-branch command and skill for creating git branches with conventional naming. Automatically determines branch type (feat, fix, chore) from task description.

### Issues
- #15 - Need standardized branch naming
- ORG-892

### Key Changes & Why
- Needed consistent branch naming across team to improve workflow visibility
- Automation reduces typos and ensures conventions are followed
- Supports 10 branch types covering all common development scenarios

## More Information

### Changes
- Added `/checkout-branch <description>` command
- Created `checkout-branch` skill with branch name generation logic
- Handles uncommitted changes, existing branches, invalid characters
- Supports: feat, fix, chore, docs, refactor, test, style, perf, ci, security

### Testing
- [x] Linted
- [x] Built successfully
- [x] Manual testing: Created branches with various descriptions
- [x] Manual testing: Verified kebab-case conversion and special char handling

### Context
Users can still manually create branches, but this provides guided approach. Branch names follow pattern: `type/description-in-kebab-case`.

### Checklist
- [x] Code follows project conventions
- [x] Documentation updated (command and skill docs)
- [x] No breaking changes
- [x] Ready for review
```

### Example 2: Bug Fix PR

**Title**: `🐛 fix(#892): resolve memory leak in websocket handler`

```markdown
## Summary
Fixes memory leak in WebSocket handler causing server crashes after sustained load.

### Issues
- #892 - Production incident: server crash at 1000+ connections

### Key Changes & Why
- Root cause: Event listeners weren't removed on disconnect
- Added explicit cleanup in disconnect handler
- Connection pool prevents unbounded growth as additional safety

## More Information

### Changes
- Added cleanup logic in `WebSocketHandler.disconnect()`
- Moved event listener removal to cleanup phase
- Added connection pool with configurable max size

### Testing
- [x] Linted
- [x] Built successfully
- [x] Tests pass (added leak detection test)
- [x] Load testing: Sustained 2000 concurrent connections for 1 hour

### Context
This was causing production outages. Connection pool config defaults to 5000 max connections (adjustable via env var).

### Checklist
- [x] Code follows project conventions
- [x] Documentation updated (added connection pool config docs)
- [x] No breaking changes
- [x] Ready for review
```

## Error Handling

- **No commits ahead**: Inform user there's nothing to create a PR for
- **Not pushed**: Push the branch first (with safe-push skill)
- **Already has PR**: Show existing PR URL
- **No base branch**: Ask user which branch to target
- **No issues provided**: Strongly encourage creating an issue first
- **gh not installed**: Inform user to install GitHub CLI
- **Not authenticated**: Prompt to run `gh auth login`

## Best Practices

1. **Always ask for issues**: Every PR needs at least one related issue
2. **Read all commits**: Don't just read latest, read ALL commits in the PR
3. **Read full diff**: Understand complete scope of changes
4. **Be specific**: Name files, functions, components changed
5. **Focus on "why"**: Explain reasoning behind decisions
6. **Honest testing**: Mark what was actually verified
7. **Highlight risks**: Call out breaking changes or risky areas

## Integration

Works with other skills:
- **commit skill**: Natural next step after committing
- **checkout-branch skill**: Completes workflow (branch → code → commit → PR)
- **safe-push skill**: Ensures branch is pushed before creating PR

## After Creating PR

Ask the user:
- "Would you like me to help with anything else?"
- Don't auto-merge or make additional changes without asking
