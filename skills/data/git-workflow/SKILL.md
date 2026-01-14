---
name: git-workflow
description: "Auto-load for git operations. Provides branching strategy, commit conventions, and PR workflow."
---

# Git Workflow

## Branch Naming

```
feat/     - New features (feat/user-auth)
fix/      - Bug fixes (fix/login-redirect)
refactor/ - Code refactoring (refactor/api-client)
docs/     - Documentation (docs/api-readme)
test/     - Test additions (test/user-service)
chore/    - Maintenance (chore/update-deps)
```

## Commit Message Format (Conventional Commits)

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change (no feature/fix)
- `docs`: Documentation only
- `test`: Adding tests
- `chore`: Maintenance tasks
- `perf`: Performance improvement

### Examples
```
feat(auth): add OAuth2 login flow

fix(api): resolve race condition in data fetch

refactor(utils): extract validation logic

docs(readme): update installation steps

test(user): add integration tests for signup
```

## PR Workflow

### Creating PRs
```bash
# Create feature branch
git checkout -b feat/my-feature

# Make changes, commit
git add .
git commit -m "feat: add new feature"

# Push and create PR
git push -u origin feat/my-feature
gh pr create --title "feat: add new feature" --body "Description"
```

### PR Description Template
```markdown
## Summary
Brief description of changes

## Changes
- Change 1
- Change 2

## Testing
How to test these changes

## Screenshots (if UI)
```

## Common Operations

```bash
# View status
git status

# Stage changes
git add .                    # All
git add path/to/file         # Specific

# Commit
git commit -m "type: message"

# View history
git log --oneline -20

# See who changed a line
git blame path/to/file

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Stash changes
git stash
git stash pop

# Rebase on main
git fetch origin
git rebase origin/main
```

## Golden Rules
- Never commit directly to main
- Keep commits atomic (one logical change)
- Write meaningful commit messages
- Review diff before committing
- Pull/rebase before pushing
