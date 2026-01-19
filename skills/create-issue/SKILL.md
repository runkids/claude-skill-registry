---
name: create-issue
description: Create well-structured GitHub issues following best practices and conventions. Use when the user asks to create an issue or needs to track work.
allowed-tools: Bash(gh issue create:*), Bash(gh issue view:*), Bash(gh issue list:*), Bash(gh label list:*), AskUserQuestion
---

# Create Issue Skill

This skill helps you create clear, actionable GitHub issues that follow best practices.

## Instructions

When the user asks to create an issue, follow these steps:

### 1. Gather Issue Information

If the user provides a clear title, use it. Otherwise, use AskUserQuestion to ask:
- What is the issue about?
- What type of issue is this? (bug, feature, enhancement, etc.)

### 2. Determine Issue Type

Analyze the description to determine the appropriate type:

- **bug**: Something isn't working correctly
  - Keywords: "fix", "bug", "error", "crash", "broken", "not working"
  - Labels: `bug`

- **feature**: New functionality to be added
  - Keywords: "add", "create", "implement", "new"
  - Labels: `enhancement`, `feature`

- **enhancement**: Improvement to existing feature
  - Keywords: "improve", "enhance", "update", "optimize"
  - Labels: `enhancement`

- **documentation**: Documentation updates
  - Keywords: "docs", "documentation", "readme", "guide"
  - Labels: `documentation`

- **chore**: Maintenance, dependencies, tooling
  - Keywords: "update dependencies", "configure", "setup", "maintain"
  - Labels: `chore`

- **refactor**: Code restructuring
  - Keywords: "refactor", "restructure", "reorganize"
  - Labels: `refactor`

- **performance**: Speed or efficiency improvements
  - Keywords: "slow", "performance", "optimize", "speed up"
  - Labels: `performance`

- **security**: Security-related issues
  - Keywords: "security", "vulnerability", "exploit", "auth"
  - Labels: `security`

### 3. Structure the Issue

Create a well-structured issue description with these sections:

**For Bugs:**
```markdown
## Problem
[Clear description of what's broken]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Observe error]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Additional Context
[Environment, versions, screenshots, etc.]
```

**For Features/Enhancements:**
```markdown
## Need
[What problem does this solve? Why is it needed?]

## Proposed Solution
[How should this be implemented?]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Additional Context
[Examples, mockups, related issues, technical details]
```

**For Documentation:**
```markdown
## What Needs Documentation
[What needs to be documented]

## Current State
[What exists now, if anything]

## Proposed Documentation
[What should be added/updated]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

**For Chores:**
```markdown
## Task
[What needs to be done]

## Reason
[Why this is needed]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Additional Context
[Dependencies, impact, etc.]
```

### 4. Create the Issue

Use GitHub CLI to create the issue:
```bash
gh issue create --title "<title>" --body "$(cat <<'EOF'
<issue-description>
EOF
)" --label "<labels>"
```

**Title Format**: Clear, imperative mood, specific

Examples:
- "Fix memory leak in WebSocket handler"
- "Add user authentication with JWT"
- "Update API documentation for v2 endpoints"
- "Refactor error handling in parser"

**Labels**: Add appropriate labels based on issue type (see step 2)

### 5. Confirm and Share

After creating the issue:
1. Show the issue number and URL
2. Display the title and summary
3. Confirm the labels applied

## Best Practices

### Title Guidelines

**Good Titles:**
- "Add JWT authentication to API"
- "Fix memory leak in WebSocket handler"
- "Update README with installation instructions"
- "Refactor database connection pooling"
- "Improve search performance with indexing"

**Bad Titles:**
- "Fix bug" (too vague)
- "Update stuff" (not specific)
- "Help needed" (not descriptive)
- "Adding authentication feature to the app" (not concise)

### Description Guidelines

**Be Specific:**
- Include concrete examples
- Provide relevant context
- Reference related issues/PRs
- Add error messages, logs, screenshots

**Be Actionable:**
- Clear acceptance criteria
- Specific tasks to complete
- Measurable outcomes

**Be Concise:**
- Skip unnecessary details
- Use bullet points
- Focus on what matters

### Acceptance Criteria

Always include clear, testable acceptance criteria:

**Good Criteria:**
- [ ] User can log in with email and password
- [ ] JWT token expires after 24 hours
- [ ] Invalid credentials show error message
- [ ] Tests pass for all auth flows

**Bad Criteria:**
- [ ] Authentication works (too vague)
- [ ] Make it better (not measurable)
- [ ] Fix the issue (not specific)

## Examples

### Example 1: Bug Issue

**Title**: `Fix memory leak in WebSocket connection handler`

**Labels**: `bug`

**Description**:
```markdown
## Problem
Server crashes after sustained load with ~1000 concurrent WebSocket connections. Memory profiling shows connections aren't being properly cleaned up on disconnect.

## Steps to Reproduce
1. Start server with `npm start`
2. Run load test: `node scripts/load-test.js --connections=1000`
3. Disconnect all clients
4. Observe memory usage remains high (>2GB)
5. After ~2 hours, server crashes with OOM error

## Expected Behavior
Memory should be released when connections close. Steady-state memory should be <500MB.

## Actual Behavior
Memory usage grows with each connection and never decreases, even after disconnects.

## Acceptance Criteria
- [ ] Connections properly cleaned up on disconnect
- [ ] Memory usage returns to baseline after disconnects
- [ ] Load test passes: 2000 concurrent connections for 1 hour
- [ ] No memory leaks detected by profiler

## Additional Context
- Node.js v20.10.0
- ws library v8.14.2
- Profiling shows event listeners not being removed
```

### Example 2: Feature Issue

**Title**: `Add branch protection and safe-push workflow`

**Labels**: `enhancement`, `feature`

**Description**:
```markdown
## Need
Prevent accidental direct pushes to protected branches (main, production, testing) that should go through PR workflows. Currently, devs can accidentally push to main, bypassing code review.

## Proposed Solution
- Create `.claude/protected-branches.json` configuration file
- Add `safe-push` skill that checks current branch before pushing
- Warn users when attempting to push to protected branches
- Suggest creating feature branch or PR instead
- Allow emergency override with explicit confirmation

## Acceptance Criteria
- [ ] Protected branches config file created
- [ ] Safe-push skill intercepts push attempts
- [ ] Warning shown for protected branch pushes
- [ ] Alternatives suggested (feature branch, PR)
- [ ] Emergency override available with confirmation
- [ ] Documentation added for configuration
- [ ] Commit skill references safe-push for post-commit workflow

## Additional Context
Should support various protected branch patterns:
- Deployment: main, master, production, prod, staging, stage
- Development: dev, develop, development
- Testing: test, testing, integration, e2e
- QA: qa, uat

Related to issue #42 (branching workflow improvements).
```

### Example 3: Documentation Issue

**Title**: `Add documentation for create-pr workflow`

**Labels**: `documentation`

**Description**:
```markdown
## What Needs Documentation
The new create-pr command and skill need user-facing documentation explaining the PR creation workflow, conventions, and best practices.

## Current State
No documentation exists for the PR workflow. Users may not know:
- How to use /create-pr command
- PR title format requirements (emoji + conventional commits + scoped issues)
- PR template structure
- Required issues linking

## Proposed Documentation
Add documentation covering:
- `/create-pr` command usage
- PR title format: `emoji type(#issue1, #issue2): description`
- PR template sections (Summary, Issues, Key Changes, Testing, etc.)
- Examples of good vs bad PRs
- Integration with commit and safe-push skills

## Acceptance Criteria
- [ ] Documentation added to README or docs/
- [ ] Examples provided for common scenarios
- [ ] Screenshots or demos included
- [ ] Links to related skills (commit, checkout-branch)

## Additional Context
Documentation should be concise and example-driven. Target audience is developers using Claude Code for development workflows.
```

### Example 4: Chore Issue

**Title**: `Remove docs app from monorepo`

**Labels**: `chore`

**Description**:
```markdown
## Task
Remove the `apps/docs` directory and all associated files from the monorepo.

## Reason
The docs app is no longer needed as documentation has moved to the main README. Keeping it adds maintenance overhead and confusion.

## Acceptance Criteria
- [ ] Delete `apps/docs` directory
- [ ] Verify build still works for remaining apps
- [ ] Update workspace configuration if needed
- [ ] Commit changes with appropriate message

## Additional Context
This is a cleanup task. No functionality is being removed, just unused code.
```

## Error Handling

- **gh not installed**: Inform user to install GitHub CLI
- **Not authenticated**: Prompt to run `gh auth login`
- **Not a GitHub repo**: Inform user this only works with GitHub repos
- **Missing required info**: Ask user for details

## Integration

Works with other skills:
- **create-pr skill**: Link issues to PRs
- **checkout-branch skill**: Create branches for issue work
- **commit skill**: Reference issues in commit messages

## After Creating Issue

Ask the user:
- "Would you like to create a branch for this issue?"
- "Should I start working on this issue?"
- Don't automatically start work without user confirmation
