---
name: ship
description: 変更をコミットし、Pull Requestを作成。差分を分析し、コミット→プッシュ→PR作成を一括実行する。
model: claude-sonnet-4-5-20250929
allowed-tools: Bash, Read, Glob, Grep
---

# Ship

変更をコミットし、リモートにプッシュして Pull Request を作成します。

**ベースブランチは `develop`。`main` への PR は禁止。**

## Phase 0: ブランチ確認

```bash
git branch --show-current
```

**main / master / develop にいる場合:**
1. diff から変更内容を分析
2. ブランチ名を生成（`feat/xxx`, `fix/xxx` 等）
3. `git checkout -b <ブランチ名>`

## Phase 1: Commit

### 1-1. 状態確認

以下を並列実行:

```bash
git status
git diff
git diff --cached
git log -10 --oneline --no-decorate
```

### 1-2. ステージング

```bash
git add <files>
```

**除外対象:** シークレット、一時ファイル

### 1-3. 変更内容の理解

1. `git diff --cached --name-only` で変更ファイル確認
2. 主要ファイルを Read で確認
3. 変更の目的・影響範囲を把握

### 1-4. コミット

```bash
git commit -m "$(cat <<'EOF'
<prefix>: <簡潔な説明>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet <noreply@anthropic.com>
EOF
)"
```

### 1-5. 確認

```bash
git status
git log -1 --stat
```

**コミット失敗時は Phase 2 をスキップして終了。**

## Phase 2: Create PR

### 2-1. プッシュ

```bash
git push -u origin HEAD
```

### 2-2. PR作成

```bash
gh pr create --draft --assignee @me --base develop \
  --title "<タイトル>" \
  --body "$(cat <<'EOF'
## Summary
<変更内容の要約>

## Test plan
<テスト方法>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### 2-3. ブラウザで開く

```bash
gh pr view --web
```

## 完了報告

- コミットメッセージ
- PR URL
- 次のアクション
