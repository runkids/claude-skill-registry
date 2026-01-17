# 🔍 Code Search Skill

---
name: code-search
description: Efficiently search through codebases to find patterns, usages, and references
---

## 🎯 Purpose

ค้นหา code patterns, usages, และ references ใน codebase อย่างมีประสิทธิภาพ

## 📋 When to Use

- หาว่า function ถูกใช้ที่ไหน
- หา pattern ที่คล้ายกัน
- Refactor และต้องหาทุกที่ที่ใช้
- หา TODO/FIXME comments
- หา import/export relationships

## 🔧 Search Methods

### 1. grep_search (Tool)
```
grep_search(
  Query="functionName",
  SearchPath="./src",
  MatchPerLine=true
)
```

### 2. PowerShell Select-String
```powershell
# ค้นหาใน file เดียว
Select-String -Path "file.ts" -Pattern "searchTerm"

# ค้นหาในหลาย files
Select-String -Path "src/*.ts" -Pattern "searchTerm" -Recurse

# Case insensitive
Select-String -Path "src/*.ts" -Pattern "searchTerm" -CaseSensitive:$false
```

### 3. ripgrep (rg)
```bash
# Basic search
rg "pattern" ./src

# With file type
rg "pattern" --type ts

# With context
rg -C 3 "pattern"

# Ignore case
rg -i "pattern"

# Fixed string (no regex)
rg -F "exact.string"
```

### 4. Git grep
```bash
# Search in tracked files
git grep "pattern"

# With line numbers
git grep -n "pattern"

# Only filenames
git grep -l "pattern"
```

## 📊 Search Patterns

### Find Function Usage
```bash
# Find function calls
rg "functionName\(" --type ts

# Find function definition
rg "function functionName|const functionName" --type ts
```

### Find Component Usage
```bash
# Find JSX usage
rg "<ComponentName" --type tsx

# Find import
rg "import.*ComponentName" --type ts
```

### Find TODOs and FIXMEs
```bash
rg "TODO:|FIXME:|HACK:|XXX:" --type ts
```

### Find Console Logs
```bash
rg "console\.(log|warn|error)" --type ts
```

### Find Hardcoded Values
```bash
# Find hardcoded URLs
rg "https?://[^\s]+" --type ts

# Find hardcoded credentials
rg "(password|secret|api_key)\s*[:=]\s*['\"]" -i --type ts
```

## 📝 Search Results Template

```markdown
## 🔍 Search Results: `{pattern}`

### Summary
- **Files matched**: 12
- **Lines matched**: 45
- **Pattern**: `{regex or string}`

### Results by File

#### `src/components/UserCard.tsx`
- Line 15: `const user = useUser(userId);`
- Line 23: `return <UserCard user={user} />;`

#### `src/hooks/useUser.ts`
- Line 8: `export function useUser(id: string) {`

### Suggestions
- Consider extracting common pattern to shared utility
- 3 instances could be simplified
```

## 🔧 Advanced Search Patterns

### Regex Patterns
| Pattern | Matches |
|---------|---------|
| `\bword\b` | Whole word only |
| `func\(.*\)` | Function calls |
| `import.*from` | Import statements |
| `useState<.*>` | Generic useState |
| `// TODO:.*` | TODO comments |

### Multi-term Search
```bash
# OR patterns
rg "pattern1|pattern2"

# AND patterns (in same file)
rg "pattern1" | xargs rg "pattern2"

# NOT pattern
rg "pattern1" --invert-match "pattern2"
```

## 📋 Common Searches

| Purpose | Pattern |
|---------|---------|
| Find imports | `import.*{name}` |
| Find exports | `export.*{name}` |
| Find hooks | `use[A-Z]\w+` |
| Find components | `<[A-Z]\w+` |
| Find API calls | `fetch\(|axios\.|api\.` |
| Find types | `interface\|type\s+\w+` |
| Find console | `console\.` |
| Find comments | `//.*\|/\*.*\*/` |

## 🛠️ IDE Search Features

### VS Code
- `Ctrl+Shift+F` - Search in files
- `Ctrl+Shift+H` - Search and replace
- `F12` - Go to definition
- `Shift+F12` - Find all references

### Antigravity
- `grep_search` - Search patterns
- `find_by_name` - Find files
- `view_file_outline` - See structure

## ✅ Search Best Practices

- [ ] Use word boundaries `\b` for precision
- [ ] Start narrow, expand if needed
- [ ] Exclude node_modules, dist
- [ ] Use file type filters
- [ ] Save common searches
- [ ] Check both singular/plural

## 🔗 Related Skills

- `codebase-understanding` - Understand project
- `refactoring` - After finding usages
- `code-review` - Review patterns
