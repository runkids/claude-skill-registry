---
name: naming-improve
description: Improve variable and function naming with semantic analysis
disable-model-invocation: false
---

# Naming Improvement

I'll analyze your code and suggest better, more semantic names for variables, functions, and classes.

Arguments: `$ARGUMENTS` - specific files or naming focus (e.g., "functions", "variables", "types")

## Strategic Analysis Process

<think>
Improving naming requires careful consideration:

1. **Code Understanding**
   - What does this variable/function actually do?
   - What's its purpose in the broader context?
   - How is it used throughout the codebase?
   - What domain concepts does it represent?

2. **Naming Problems to Fix**
   - Generic names (data, temp, obj, result, item)
   - Single letters (x, y, i beyond simple loops)
   - Unclear abbreviations (usr, msg, cfg)
   - Misleading names (getName that modifies state)
   - Inconsistent naming patterns
   - Hungarian notation remnants (strName, arrItems)

3. **Language Conventions**
   - JavaScript/TypeScript: camelCase for variables/functions, PascalCase for classes
   - Python: snake_case for variables/functions, PascalCase for classes
   - Go: camelCase with exported names capitalized
   - Rust: snake_case for variables/functions, PascalCase for types
   - Follow project's existing conventions

4. **Semantic Naming Principles**
   - Intention-revealing names
   - Pronounceable and searchable names
   - Avoid mental mapping
   - Use domain terminology
   - Be specific and descriptive
   - Avoid encodings and prefixes
</think>

## Phase 1: Naming Analysis

**MANDATORY FIRST STEPS:**
1. Analyze code to find poorly named identifiers
2. Understand usage context for each identifier
3. Detect language and naming conventions
4. Categorize naming issues by severity

Let me analyze naming in your code:

```bash
# Detect programming language
echo "=== Code Analysis ==="

# Find common poorly named identifiers
echo "Checking for generic/unclear names..."

# Look for single-letter variables (excluding loop counters)
# Look for generic names like data, temp, obj, result, item
# Look for unclear abbreviations

# Analyze file types
FILE_COUNT=$(find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" -o -name "*.rs" \) 2>/dev/null | wc -l)
echo "Source files to analyze: $FILE_COUNT"

# Detect primary language
if [ -f "package.json" ]; then
    if grep -q "\"typescript\"" package.json; then
        echo "Primary language: TypeScript"
    else
        echo "Primary language: JavaScript"
    fi
elif [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
    echo "Primary language: Python"
elif [ -f "go.mod" ]; then
    echo "Primary language: Go"
elif [ -f "Cargo.toml" ]; then
    echo "Primary language: Rust"
fi
```

## Phase 2: Pattern Detection

I'll identify common naming anti-patterns:

**Generic Names:**
- `data`, `info`, `obj`, `item`, `element`, `thing`
- `result`, `output`, `temp`, `tmp`
- `list`, `array`, `collection` (without context)
- `manager`, `handler`, `helper`, `util` (vague suffixes)

**Single Letter Names:**
- `x`, `y`, `z` (outside math/coordinates)
- `a`, `b`, `c` (meaningless)
- `i`, `j`, `k` (beyond simple loop counters)
- `e` (for error - should be `error`)

**Unclear Abbreviations:**
- `usr` → `user`
- `cfg` → `config`
- `msg` → `message`
- `btn` → `button`
- `arr` → `array` (or better, describe contents)
- `num` → `number` or specific quantity

**Misleading Names:**
- `getData()` that modifies state → `fetchAndStoreData()`
- `isValid()` with side effects → `validateAndLog()`
- `process()` → be specific about what's processed

**Inconsistent Patterns:**
- Mix of `getUser()` and `fetchProfile()`
- Mix of `userId` and `user_id`
- Mix of `isEnabled` and `hasAccess`

Using native tools:
- **Grep** to find generic identifiers
- **Read** files with poor naming
- **Grep** for naming pattern inconsistencies

## Phase 3: Semantic Name Suggestions

Based on context and usage, I'll suggest better names:

### Variable Naming Improvements

**Before:**
```typescript
// Generic, unclear names
const data = await fetch('/api/users');
const result = data.json();
const list = result.map(item => item.name);
const temp = list.filter(x => x.length > 5);
```

**After:**
```typescript
// Descriptive, intention-revealing names
const usersResponse = await fetch('/api/users');
const users = await usersResponse.json();
const userNames = users.map(user => user.name);
const longUserNames = userNames.filter(name => name.length > 5);
```

### Function Naming Improvements

**Before:**
```typescript
// Vague function names
function process(data) {
  const result = data.filter(x => x.active);
  return result;
}

function handle(item) {
  item.status = 'done';
  save(item);
}

function get() {
  return state.user;
}
```

**After:**
```typescript
// Specific, action-oriented names
function filterActiveUsers(users) {
  return users.filter(user => user.active);
}

function markItemAsCompleteAndSave(item) {
  item.status = 'done';
  save(item);
}

function getCurrentUser() {
  return state.user;
}
```

### Class/Type Naming Improvements

**Before:**
```typescript
// Generic, unclear class names
class Manager {
  handle(data) { }
}

class Helper {
  process(item) { }
}

interface Data {
  info: string;
  stuff: any;
}
```

**After:**
```typescript
// Specific, domain-focused names
class UserSessionManager {
  authenticateUser(credentials) { }
}

class DateFormatter {
  formatToISO(date) { }
}

interface UserProfile {
  displayName: string;
  preferences: UserPreferences;
}
```

## Phase 4: Context-Aware Renaming

I'll analyze how identifiers are used to suggest contextual names:

**Usage Analysis:**
```typescript
// Analyze this code:
const data = await fetchFromDatabase();
const filtered = data.filter(x => x.age > 18);
const sorted = filtered.sort((a, b) => a.name.localeCompare(b.name));
const result = sorted.slice(0, 10);
```

**Context Understanding:**
- `data` is fetched from database → likely users, products, etc.
- Filtered by `age > 18` → adults or eligible users
- Sorted by `name` → alphabetically ordered
- Top 10 results → limited result set

**Improved Version:**
```typescript
const allUsers = await fetchUsersFromDatabase();
const adultUsers = allUsers.filter(user => user.age > 18);
const alphabeticalUsers = adultUsers.sort((a, b) =>
  a.name.localeCompare(b.name)
);
const topTenUsers = alphabeticalUsers.slice(0, 10);

// Or with descriptive pipeline:
const topTenAdultUsersSorted = await fetchUsersFromDatabase()
  .then(users => users.filter(user => user.age > 18))
  .then(adults => adults.sort((a, b) => a.name.localeCompare(b.name)))
  .then(sorted => sorted.slice(0, 10));
```

## Phase 5: Language-Specific Conventions

I'll apply language-specific naming best practices:

### JavaScript/TypeScript

**Conventions:**
- Variables/functions: `camelCase`
- Classes/interfaces: `PascalCase`
- Constants: `UPPER_SNAKE_CASE` or `camelCase`
- Private members: `_prefixWithUnderscore` (legacy) or `#privateField` (modern)
- Boolean variables: `is`, `has`, `should` prefixes

**Examples:**
```typescript
// Variables
const userProfile = getUserProfile();
const isAuthenticated = checkAuth();
const hasPermission = user.permissions.includes('admin');

// Functions
function calculateTotalPrice(items: CartItem[]): number { }
function shouldDisplayNotification(user: User): boolean { }

// Classes
class UserAuthenticationService { }
class ProductInventoryManager { }

// Constants
const MAX_RETRY_ATTEMPTS = 3;
const API_BASE_URL = 'https://api.example.com';

// Interfaces/Types
interface UserProfile { }
type PaymentMethod = 'card' | 'paypal' | 'crypto';
```

### Python

**Conventions:**
- Variables/functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private members: `_prefix_with_underscore`
- Boolean variables: `is_`, `has_`, `should_` prefixes

**Examples:**
```python
# Variables
user_profile = get_user_profile()
is_authenticated = check_auth()
has_permission = 'admin' in user.permissions

# Functions
def calculate_total_price(items: list[CartItem]) -> float:
    pass

def should_display_notification(user: User) -> bool:
    pass

# Classes
class UserAuthenticationService:
    pass

class ProductInventoryManager:
    pass

# Constants
MAX_RETRY_ATTEMPTS = 3
API_BASE_URL = 'https://api.example.com'
```

### Go

**Conventions:**
- Exported: Capitalized (`UserService`)
- Unexported: lowercase (`userService`)
- Acronyms: All caps (`HTTPServer`, `URLParser`)
- Getters: No `Get` prefix (`user.Name()` not `user.GetName()`)

**Examples:**
```go
// Exported
type UserAuthenticationService struct {}
func (s *UserAuthenticationService) AuthenticateUser() {}

// Unexported
var maxRetryAttempts = 3
func calculateTotalPrice(items []CartItem) float64 {}

// Acronyms
type HTTPClient struct {}
type URLParser struct {}

// Getters (no Get prefix)
func (u *User) Name() string { return u.name }
```

## Phase 6: Refactoring Implementation

I'll safely rename identifiers across the codebase:

**Renaming Strategy:**
1. **Local scope first**: Rename within single functions
2. **File scope**: Rename across file
3. **Module scope**: Rename across related files
4. **Global scope**: Rename across entire codebase (most risky)

**Safety Checks:**
- Create git checkpoint before changes
- Use precise string matching (avoid partial matches)
- Verify no external references broken
- Update tests and documentation
- Run tests after each significant rename

**Example Refactoring:**
```typescript
// Before: Poor naming
function proc(d) {
  const r = d.filter(x => x.s === 'a');
  const t = r.length;
  return t > 0;
}

// After: Clear naming
function hasActiveUsers(users) {
  const activeUsers = users.filter(user => user.status === 'active');
  const activeUserCount = activeUsers.length;
  return activeUserCount > 0;
}

// Or even better (more concise):
function hasActiveUsers(users) {
  return users.some(user => user.status === 'active');
}
```

## Token Optimization Strategy

**Efficient Analysis:**
- Use Grep to find common anti-patterns quickly
- Focus on most impactful names first
- Analyze file-by-file rather than entire codebase
- Provide examples rather than exhaustive lists
- Prioritize user-specified files/areas

**Targeted Improvements:**
- Start with worst offenders (single letters, `data`, `temp`)
- Focus on public APIs and interfaces
- Prioritize frequently used identifiers
- Skip obvious loop counters (`i`, `j`, `k`)

## Integration Points

**Synergistic Skills:**
- `/make-it-pretty` - Overall code readability improvements
- `/refactor` - Broader refactoring including naming
- `/review` - Code review including naming feedback
- `/complexity-reduce` - Simplification often improves naming clarity

Suggests `/make-it-pretty` when:
- Code has other readability issues beyond naming
- Formatting and structure need attention
- Type safety improvements needed

Suggests `/refactor` when:
- Code structure needs reorganization
- Functions need extraction
- Broader refactoring needed

## Naming Guidelines Reference

**Good Naming Principles:**

1. **Intention-Revealing**: Name should explain why it exists
   - Bad: `d` (elapsed time in days)
   - Good: `elapsedTimeInDays`

2. **Avoid Disinformation**: Don't use misleading names
   - Bad: `accountList` for a Map
   - Good: `accountMap` or `accounts`

3. **Make Meaningful Distinctions**: Avoid number series or noise words
   - Bad: `data1`, `data2`, `dataInfo`
   - Good: `rawData`, `processedData`, `dataStatistics`

4. **Pronounceable Names**: Should be readable aloud
   - Bad: `genymdhms` (generation year month day hour minute second)
   - Good: `generationTimestamp`

5. **Searchable Names**: Easy to find with search
   - Bad: `7` (magic number)
   - Good: `DAYS_IN_WEEK = 7`

6. **Avoid Mental Mapping**: Don't require translation
   - Bad: `r` for URL
   - Good: `url`

7. **Class Names**: Nouns or noun phrases
   - Good: `Customer`, `WikiPage`, `Account`, `AddressParser`
   - Avoid: `Manager`, `Processor`, `Data`, `Info`

8. **Method Names**: Verbs or verb phrases
   - Good: `postPayment`, `deletePage`, `save`
   - Accessors/Mutators: `getName`, `setName`, `isPosted`

9. **Pick One Word Per Concept**: Be consistent
   - Don't mix: `fetch`, `retrieve`, `get` for same concept
   - Pick one: `get` for all similar operations

10. **Use Domain Names**: When appropriate
    - Good: `AccountVisitor`, `JobQueue`, `PriorityQueue`

## Safety Mechanisms

**Protection Measures:**
- Create git checkpoint before renaming
- Rename incrementally (local → file → module → global)
- Verify tests pass after each rename
- Use search to find all usages
- Update documentation and comments

**Validation Steps:**
1. Find all occurrences of identifier
2. Verify context matches intended rename
3. Perform rename with exact matching
4. Run linter/type checker
5. Run tests
6. Review changes

**Rollback Procedure:**
```bash
# If renaming introduces issues
git checkout HEAD -- path/to/file
# Or for entire renaming session
git reset --hard HEAD
```

## Expected Improvements

**Code Clarity:**
- 50-80% reduction in cognitive load
- Easier onboarding for new developers
- Better IDE autocomplete suggestions
- Improved searchability
- Self-documenting code

**Naming Quality Metrics:**
- Generic names eliminated
- Single-letter variables reduced to loops only
- Consistent naming patterns
- Domain-appropriate terminology
- Clear intention in all identifiers

## Error Handling

If naming improvements introduce issues:
- I'll identify which rename caused the problem
- Provide specific rollback instructions
- Suggest alternative names
- Explain naming conflicts
- Ensure code functionality preserved

## Important Notes

**I will NEVER:**
- Break working code with renames
- Add AI attribution to files
- Rename without understanding context
- Change public API names without warning
- Ignore language conventions

**Best Practices:**
- Always understand context before renaming
- Preserve functionality exactly
- Follow language-specific conventions
- Be consistent across codebase
- Update tests and documentation

## Credits

**Inspired by:**
- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) - Naming principles
- [Refactoring by Martin Fowler](https://refactoring.com/) - Rename refactoring patterns
- Language-specific style guides (Airbnb, Google, PEP 8)
- Domain-driven design naming practices
- Code review best practices

This skill helps you transform unclear, generic names into clear, intention-revealing identifiers that make code self-documenting.
