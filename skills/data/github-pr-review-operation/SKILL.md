---
name: github-pr-review-operation
description: GitHub Pull Request review operations using gh CLI. Extract PR info, view diffs with line numbers, retrieve and post comments, create inline comments, and reply to comments. Use when reviewing PRs, conducting code reviews, or performing PR operations.
---

# GitHub PR Review Operation

GitHub CLI (`gh`) for PR review operations.

## Prerequisites

- `gh` installed
- `gh auth login` completed

## Parsing PR URL

Extract from PR URL `https://github.com/OWNER/REPO/pull/NUMBER`:
- `OWNER`: Repository owner
- `REPO`: Repository name
- `NUMBER`: PR number

## Operations

### 1. Retrieve PR Information

```bash
gh pr view NUMBER --repo OWNER/REPO --json title,body,author,state,baseRefName,headRefName,url
```

### 2. Retrieve Diff with Line Numbers

```bash
gh pr diff NUMBER --repo OWNER/REPO | awk '
/^@@/ {
  match($0, /-([0-9]+)/, old)
  match($0, /\+([0-9]+)/, new)
  old_line = old[1]
  new_line = new[1]
  print $0
  next
}
/^-/ { printf "L%-4d     | %s\n", old_line++, $0; next }
/^\+/ { printf "     R%-4d| %s\n", new_line++, $0; next }
/^ / { printf "L%-4d R%-4d| %s\n", old_line++, new_line++, $0; next }
{ print }
'
```

Output example:
```
@@ -46,15 +46,25 @@ jobs:
L46   R46  |            prompt: |
L49       | -            (deleted line)
     R49  | +            (added line)
L50   R50  |              # Review guidelines
```

- `L{number}`: Line number on LEFT (base) side → use with `side=LEFT` for inline comments
- `R{number}`: Line number on RIGHT (head) side → use with `side=RIGHT` for inline comments

### 3. Retrieve Comments

Issue Comments (comments on the entire PR):
```bash
gh api repos/OWNER/REPO/issues/NUMBER/comments --jq '.[] | {id, user: .user.login, created_at, body}'
```

Review Comments (comments on code lines):
```bash
gh api repos/OWNER/REPO/pulls/NUMBER/comments --jq '.[] | {id, user: .user.login, path, line, created_at, body, in_reply_to_id}'
```

### 4. Post Comment to PR

```bash
gh pr comment NUMBER --repo OWNER/REPO --body "Comment text"
```

### 5. Post Inline Comment (Code Line Specific)

First, retrieve the head commit SHA:
```bash
gh api repos/OWNER/REPO/pulls/NUMBER --jq '.head.sha'
```

Single line comment:
```bash
gh api repos/OWNER/REPO/pulls/NUMBER/comments \
  --method POST \
  -f body="Comment text" \
  -f commit_id="COMMIT_SHA" \
  -f path="src/example.py" \
  -F line=15 \
  -f side=RIGHT
```

Multi-line comment (lines 10-15):
```bash
gh api repos/OWNER/REPO/pulls/NUMBER/comments \
  --method POST \
  -f body="Comment text" \
  -f commit_id="COMMIT_SHA" \
  -f path="src/example.py" \
  -F line=15 \
  -f side=RIGHT \
  -F start_line=10 \
  -f start_side=RIGHT
```

**Important Notes:**
- Use `-F` (uppercase) for numeric parameters (`line`, `start_line`). Using `-f` will convert them to strings and cause errors.
- `side`: `RIGHT` (added lines) or `LEFT` (deleted lines)

### 6. Reply to Comment

```bash
gh api repos/OWNER/REPO/pulls/NUMBER/comments/COMMENT_ID/replies \
  --method POST \
  -f body="Reply text"
```

Use the `id` from retrieved comments as `COMMENT_ID`.

## Important Guidelines

**All review comments must be written in Japanese** to ensure consistency with team communication and maintain clarity for all team members.

Examples:
- Inline comment: `"この行でnullチェックが必要です。"`
- Review comment: `"コードレビュー完了しました。承認します。"`
- Reply: `"ご指摘ありがとうございます。修正しました。"`

## Common Workflow

```bash
# 1. Get PR info
PR_NUM=123
OWNER_REPO="owner/repo"
gh pr view $PR_NUM --repo $OWNER_REPO --json title,body

# 2. Get diff with line numbers
gh pr diff $PR_NUM --repo $OWNER_REPO | awk '...' > /tmp/diff.txt

# 3. Get existing comments
gh api repos/$OWNER_REPO/pulls/$PR_NUM/comments > /tmp/comments.json

# 4. Get commit SHA
COMMIT_SHA=$(gh api repos/$OWNER_REPO/pulls/$PR_NUM --jq '.head.sha')

# 5. Post inline comments
gh api repos/$OWNER_REPO/pulls/$PR_NUM/comments \
  --method POST \
  -f body="この部分はnullチェックが必要です。" \
  -f commit_id="$COMMIT_SHA" \
  -f path="src/file.ts" \
  -F line=42 \
  -f side=RIGHT

# 6. Submit review
gh api repos/$OWNER_REPO/pulls/$PR_NUM/reviews \
  --method POST \
  -f body="コードレビュー完了しました。承認します。" \
  -f event="APPROVE" \
  -f commit_id="$COMMIT_SHA"
```

## Troubleshooting

**Comment on wrong line**: Verify line numbers using the diff output with L/R format. Ensure `side` parameter matches (LEFT for removed, RIGHT for added).

**Reply not threaded**: Include all required fields and ensure `COMMENT_ID` is correct.

**Comments not retrieved**: Fetch both types - issue comments and review comments are separate endpoints.
