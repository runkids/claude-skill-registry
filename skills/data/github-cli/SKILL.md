---
name: github-cli
description: Wrapper for GitHub CLI (gh) in Claude.ai. Covers installation, authentication, and common operations like pushing files, creating branches, PRs, issues, and releases.
---

# GitHub CLI Skill

Use the official GitHub CLI (`gh`) in Claude.ai for repository operations.

## Setup

### 1. Install (once per session)

```bash
apt-get update && apt-get install -y gh
```

### 2. Claude.ai Network Allowlist

Add `api.github.com` to your project's allowed domains:

1. Go to your Claude Project settings
2. Find **Network/Egress settings**
3. Add `api.github.com`
4. **Start a new chat** (network settings load at conversation start)

### 3. Authentication

Set your GitHub PAT as an environment variable:

```bash
export GH_TOKEN="github_pat_xxxx"
```

Create a fine-grained PAT at: https://github.com/settings/tokens?type=beta

Verify auth:
```bash
gh auth status
```

## Common Operations

### Repository

```bash
# View repo info
gh repo view owner/repo

# Create new repo
gh repo create owner/repo --private --description "My project"

# Clone repo
gh repo clone owner/repo

# List your repos
gh repo list
```

### Files & Commits

```bash
# Push a single file (create or update)
CONTENT=$(base64 -w 0 myfile.txt)
gh api -X PUT repos/owner/repo/contents/path/to/file.txt \
    -f message="Add file" \
    -f content="$CONTENT" \
    -f branch="main"

# Update existing file (need SHA)
SHA=$(gh api repos/owner/repo/contents/path/to/file.txt --jq '.sha')
gh api -X PUT repos/owner/repo/contents/path/to/file.txt \
    -f message="Update file" \
    -f content="$CONTENT" \
    -f sha="$SHA" \
    -f branch="main"

# Delete a file
SHA=$(gh api repos/owner/repo/contents/path/to/file.txt --jq '.sha')
gh api -X DELETE repos/owner/repo/contents/path/to/file.txt \
    -f message="Delete file" \
    -f sha="$SHA" \
    -f branch="main"

# List files in a directory
gh api repos/owner/repo/contents/path/to/dir
```

### Branches

```bash
# List branches
gh api repos/owner/repo/branches --jq '.[].name'

# Create branch from main
SHA=$(gh api repos/owner/repo/git/refs/heads/main --jq '.object.sha')
gh api -X POST repos/owner/repo/git/refs \
    -f ref="refs/heads/feature/new-branch" \
    -f sha="$SHA"

# Delete branch
gh api -X DELETE repos/owner/repo/git/refs/heads/feature/old-branch
```

### Pull Requests

```bash
# Create PR (from cloned repo)
gh pr create --title "My PR" --body "Description" --base main --head feature-branch

# Create PR via API (without clone)
gh api -X POST repos/owner/repo/pulls \
    -f title="My PR" \
    -f body="Description" \
    -f head="feature-branch" \
    -f base="main"

# List PRs
gh pr list --repo owner/repo

# View PR
gh pr view 123 --repo owner/repo

# Merge PR
gh pr merge 123 --repo owner/repo --squash
```

### Issues

```bash
# Create issue
gh issue create --repo owner/repo --title "Bug" --body "Description"

# List issues
gh issue list --repo owner/repo

# Close issue
gh issue close 123 --repo owner/repo
```

### Releases

```bash
# Create release
gh release create v1.0.0 --repo owner/repo --title "v1.0.0" --notes "Release notes"

# Create release with files
gh release create v1.0.0 ./dist/*.zip --repo owner/repo

# List releases
gh release list --repo owner/repo
```

### Actions / Workflows

```bash
# List workflow runs
gh run list --repo owner/repo

# View run details
gh run view 12345 --repo owner/repo

# Trigger workflow
gh workflow run build.yml --repo owner/repo
```

## Required Permissions

### Fine-grained PAT

| Permission | Level | For |
|------------|-------|-----|
| Contents | Read and write | Files, branches |
| Pull requests | Read and write | PRs |
| Issues | Read and write | Issues |
| Actions | Read and write | Workflows |
| Metadata | Read | Auto-granted |
| Workflows | Read and write | Push to `.github/workflows/` |

### Classic PAT

Use `repo` scope for full access, or specific scopes as needed.

## Tips

### Use `--jq` for JSON parsing
```bash
gh api repos/owner/repo --jq '.default_branch'
gh api repos/owner/repo/branches --jq '.[].name'
```

### Batch operations with xargs
```bash
# Delete multiple branches
echo -e "old-branch-1\nold-branch-2" | xargs -I {} gh api -X DELETE repos/owner/repo/git/refs/heads/{}
```

### Check rate limits
```bash
gh api rate_limit --jq '.resources.core'
```

## References

- [GitHub CLI Manual](https://cli.github.com/manual/)
- [GitHub REST API](https://docs.github.com/en/rest)
- [gh api command](https://cli.github.com/manual/gh_api)
