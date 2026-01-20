---
name: git-workflow
description: Create worktrees/branches, commit changes, and open PRs for CasareRPA. Use when: starting work or preparing a PR.
---

# Git Workflow (Worktree -> Branch -> Commit -> PR)

Use worktrees for parallel feature work, then open a PR with tests.

## Worktree / Branch
- Create a worktree: `python scripts/create_worktree.py <branch> [--base main] [--path <path>]`
- Or create a branch in-place: `git switch -c <branch>`

## Commit
- Check status: `git status`
- Stage: `git add -A`
- Commit: `git commit -m "[area] concise summary"`

## Tests (required)
- Run unit/regression suites: `pytest tests/ -v`
- Run e2e/Playwright when touching browser automation.
- Mirror CI checks defined in `.github/workflows` when applicable.
- If any test is skipped, document why.

## PR
- Push: `git push -u origin <branch>`
- Create PR (gh): `gh pr create --fill`
- Otherwise open a PR in the host UI with scope, tests, and risks.
