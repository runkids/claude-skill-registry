# 🔍 PR Review Skill

---
name: pr-review
description: Automatically review Pull Requests for code quality, bugs, security issues, and best practices
---

## 🎯 Purpose

Review Pull Requests อัตโนมัติ ตรวจสอบ code quality, potential bugs, security issues, และ best practices

## 📋 When to Use

- Review PRs ก่อน merge
- Assist human reviewers
- Enforce coding standards
- Catch common issues
- Improve code quality

## 🔧 Review Dimensions

### 1. Code Quality
| Check | Description |
|-------|-------------|
| Readability | Code easy to understand |
| Complexity | Functions not too complex |
| Duplication | No copy-paste code |
| Naming | Variables/functions named well |
| Comments | Complex logic documented |

### 2. Correctness
| Check | Description |
|-------|-------------|
| Logic errors | Conditions correct |
| Edge cases | Null checks, empty arrays |
| Error handling | Try-catch where needed |
| Type safety | No `any`, proper types |
| Async handling | Await, error boundaries |

### 3. Security
| Check | Description |
|-------|-------------|
| Input validation | User input sanitized |
| SQL injection | Parameterized queries |
| XSS | Output encoded |
| Secrets | No hardcoded credentials |
| CORS | Properly configured |

### 4. Performance
| Check | Description |
|-------|-------------|
| N+1 queries | Batch database calls |
| Memoization | Avoid re-computation |
| Bundle size | No large dependencies |
| Rendering | Minimize re-renders |

### 5. Testing
| Check | Description |
|-------|-------------|
| Test coverage | New code tested |
| Edge cases | Tests cover edge cases |
| Mocking | External deps mocked |

## 📝 Review Process

```
1. UNDERSTAND context
   - Read PR description
   - Check linked issues
   - Understand the goal

2. ANALYZE changes
   - File by file review
   - Check diff context
   - Identify patterns

3. CHECK each dimension
   - Quality
   - Correctness
   - Security
   - Performance
   - Testing

4. PROVIDE feedback
   - Clear comments
   - Suggest improvements
   - Explain WHY
   - Offer alternatives

5. SUMMARIZE
   - Overall assessment
   - Blocking issues
   - Nice-to-haves
```

## 📋 Review Comment Templates

### Bug Found
```markdown
🐛 **Potential Bug**

This code will throw an error when `user` is null:
```js
const name = user.name; // Error if user is null
```

**Suggestion:**
```js
const name = user?.name ?? 'Unknown';
```
```

### Security Issue
```markdown
🔐 **Security Concern**

User input is used directly in the query without sanitization:
```js
const result = db.query(`SELECT * FROM users WHERE id = ${userId}`);
```

**Suggestion:** Use parameterized queries:
```js
const result = db.query('SELECT * FROM users WHERE id = ?', [userId]);
```
```

### Performance Issue
```markdown
⚡ **Performance Improvement**

This component re-renders on every parent update:
```jsx
const result = heavyCalculation(data);
```

**Suggestion:** Use memoization:
```jsx
const result = useMemo(() => heavyCalculation(data), [data]);
```
```

### Style Suggestion
```markdown
💡 **Suggestion**

Consider extracting this logic to a custom hook for reusability:
```jsx
const [data, setData] = useState(null);
const [loading, setLoading] = useState(true);
useEffect(() => { ... }, []);
```

Could become:
```jsx
const { data, loading } = useDataFetch(url);
```
```

## 📊 Review Summary Template

```markdown
## 📋 PR Review Summary

### Overview
- **Files changed**: 12
- **Lines added**: 234
- **Lines removed**: 56

### Assessment: ✅ Approve with suggestions

### 🔴 Blocking Issues
None

### 🟡 Should Fix
1. Add null check in `UserCard.tsx` (line 45)
2. Remove console.log in `api.ts` (line 23)

### 🟢 Suggestions (Nice-to-have)
1. Consider extracting validation to separate function
2. Add loading skeleton for better UX

### 💬 Comments
Great implementation overall! The new auth flow is well-structured.
Just a few minor issues to address before merging.
```

## 🔧 Automated Checks

```yaml
# .github/workflows/pr-review.yml
name: PR Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run linter
        run: npm run lint
      - name: Run type check
        run: npm run type-check
      - name: Run tests
        run: npm test
      - name: Check bundle size
        run: npm run analyze
```

## ✅ Review Checklist

- [ ] PR description is clear
- [ ] Changes match the description
- [ ] No obvious bugs
- [ ] Error handling present
- [ ] No security vulnerabilities
- [ ] No performance issues
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console.logs or debug code
- [ ] Types are correct

## 🔗 Related Skills

- `code-review` - General code review
- `security-audit` - Security analysis
- `testing` - Test coverage
