# 📝 Commit Message Skill

---
name: commit-message
description: Generate meaningful, conventional commit messages from code changes
---

## 🎯 Purpose

สร้าง commit messages ที่มีความหมาย ตาม Conventional Commits standard จาก code changes อัตโนมัติ

## 📋 When to Use

- เมื่อ stage changes และพร้อม commit
- ต้องการ consistent commit style
- ต้องการ auto-generate changelogs
- Team ใช้ conventional commits

## 🔧 Conventional Commits Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types
| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat: add user authentication` |
| `fix` | Bug fix | `fix: resolve login redirect issue` |
| `docs` | Documentation | `docs: update API documentation` |
| `style` | Formatting (no code change) | `style: format code with prettier` |
| `refactor` | Refactoring | `refactor: extract validation logic` |
| `perf` | Performance | `perf: optimize database queries` |
| `test` | Tests | `test: add unit tests for utils` |
| `build` | Build system | `build: update webpack config` |
| `ci` | CI/CD | `ci: add GitHub Actions workflow` |
| `chore` | Maintenance | `chore: update dependencies` |
| `revert` | Revert | `revert: undo last commit` |

### Scope (Optional)
```
feat(auth): add OAuth2 support
fix(api): handle timeout errors
docs(readme): add installation guide
refactor(components): simplify Button props
```

## 📝 Generation Process

```
1. ANALYZE changes
   - git diff --staged
   - Identify changed files
   - Detect change patterns

2. DETECT type
   - New files → feat
   - Deleted code → fix or refactor
   - Test files → test
   - Config changes → build/ci

3. IDENTIFY scope
   - By folder (auth, api, ui)
   - By feature
   - By component

4. GENERATE description
   - Imperative mood
   - Clear and concise
   - Max 72 characters

5. ADD body (if needed)
   - Explain WHY
   - Reference issues
   - Breaking changes
```

## 📊 Examples by Change Type

### New Feature
```bash
# Changes: Created new UserProfile component
feat(user): add user profile component

- Display user avatar, name, and bio
- Add skeleton loading state
- Implement responsive layout
```

### Bug Fix
```bash
# Changes: Fixed null check in API
fix(api): handle null response in user fetch

The API was crashing when user data was null.
Added proper null check and fallback value.

Closes #123
```

### Refactoring
```bash
# Changes: Extracted logic to custom hook
refactor(hooks): extract useAuth from AuthContext

- Created useAuth hook for auth state
- Reduced AuthProvider complexity
- Improved testability
```

### Breaking Change
```bash
# Changes: Changed API signature
feat(api)!: change login API response format

BREAKING CHANGE: The login response now returns
{ user, token } instead of { data: { user, token } }
```

## 🔧 Auto-Generation Logic

```typescript
function generateCommitMessage(diff: string): string {
  // Analyze diff
  const files = parseChangedFiles(diff);
  const additions = countAdditions(diff);
  const deletions = countDeletions(diff);
  
  // Determine type
  let type = 'chore';
  if (files.some(f => f.includes('.test.'))) type = 'test';
  if (files.some(f => f.includes('README') || f.includes('.md'))) type = 'docs';
  if (additions > deletions * 2) type = 'feat';
  if (deletions > additions && hasFixPattern(diff)) type = 'fix';
  
  // Determine scope
  const scope = detectScope(files);
  
  // Generate description
  const description = generateDescription(diff, type);
  
  return scope 
    ? `${type}(${scope}): ${description}`
    : `${type}: ${description}`;
}
```

## 📋 Good Commit Messages

### ✅ Good
```
feat(cart): add product quantity selector
fix(auth): prevent duplicate login requests
docs(api): document rate limiting behavior
refactor(utils): simplify date formatting logic
test(user): add integration tests for signup
```

### ❌ Bad
```
fixed stuff
update
WIP
changes
asdfasdf
```

## 🛠️ Tools

### Commitizen
```bash
npm install -g commitizen
git cz  # Interactive commit
```

### Husky + Commitlint
```bash
npm install -D husky @commitlint/cli @commitlint/config-conventional
```

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional']
};
```

## ✅ Commit Message Checklist

- [ ] Type is correct
- [ ] Scope is relevant (if used)
- [ ] Description is clear
- [ ] Uses imperative mood ("add" not "added")
- [ ] Less than 72 characters
- [ ] Body explains WHY (if complex)
- [ ] References issues/PRs (if applicable)
- [ ] Breaking changes noted

## 🔗 Related Skills

- `git-workflow` - Git operations
- `changelog-generator` - Generate changelogs
- `pr-review` - Review pull requests
