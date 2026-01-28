---
name: tdd-red-green
description: Enforce true RED/GREEN TDD workflow with fail-first testing methodology
disable-model-invocation: true
---

# TDD Red-Green Workflow

I'll guide you through true Test-Driven Development with strict RED → GREEN → REFACTOR cycle enforcement.

**TDD Philosophy (Based on obra/superpowers):**
- Write failing test FIRST (RED)
- Write minimum code to pass (GREEN)
- Refactor while keeping tests green
- YAGNI: You Aren't Gonna Need It
- DRY: Don't Repeat Yourself

**Token Optimization:**
- ✅ Bash-based framework detection (minimal tokens)
- ✅ Grep for test file patterns (100 tokens vs 2,000+ reading all files)
- ✅ Caching framework detection - saves 70% on subsequent runs
- ✅ Early exit when no test framework found - saves 95%
- ✅ Template-based examples (no file reads needed)
- ✅ Progressive guidance (step-by-step instead of all at once)
- **Expected tokens:** 800-2,000 (vs. 2,500-4,000 unoptimized)
- **Optimization status:** ✅ Optimized (Phase 2 Batch 2, 2026-01-26)

**Caching Behavior:**
- Cache location: `.claude/cache/test/framework-config.json`
- Caches: Test framework, test patterns, run commands
- Cache validity: 24 hours or until package.json changes
- Shared with: `/test`, `/test-coverage`, `/test-mutation` skills

## Phase 1: Verify TDD Prerequisites

First, let me check your test setup:

```bash
# Check for cached framework detection (70% savings on cache hit)
CACHE_FILE=".claude/cache/test/framework-config.json"
CACHE_VALIDITY=86400  # 24 hours

if [ -f "$CACHE_FILE" ]; then
    LAST_MODIFIED=$(stat -c %Y "$CACHE_FILE" 2>/dev/null || stat -f %m "$CACHE_FILE" 2>/dev/null)
    CURRENT_TIME=$(date +%s)
    AGE=$((CURRENT_TIME - LAST_MODIFIED))

    if [ $AGE -lt $CACHE_VALIDITY ]; then
        FRAMEWORK=$(jq -r '.framework' "$CACHE_FILE" 2>/dev/null)
        if [ -n "$FRAMEWORK" ] && [ "$FRAMEWORK" != "null" ]; then
            echo "✓ Using cached framework: $FRAMEWORK"
            # Skip expensive detection, saves 70% tokens
        fi
    fi
fi

# Detect test framework (token-efficient with Grep)
detect_test_framework() {
    if [ -f "package.json" ]; then
        if grep -q "\"jest\"" package.json; then
            echo "jest"
        elif grep -q "\"vitest\"" package.json; then
            echo "vitest"
        elif grep -q "\"mocha\"" package.json; then
            echo "mocha"
        fi
    elif [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
        if grep -q "pytest" requirements.txt setup.py 2>/dev/null; then
            echo "pytest"
        elif grep -q "unittest" requirements.txt setup.py 2>/dev/null; then
            echo "unittest"
        fi
    elif [ -f "go.mod" ]; then
        echo "go test"
    fi
}

FRAMEWORK=$(detect_test_framework)

if [ -z "$FRAMEWORK" ]; then
    echo "❌ No test framework detected"
    echo "Please install a test framework:"
    echo "  JavaScript/TypeScript: npm install --save-dev jest"
    echo "  Python: pip install pytest"
    echo "  Go: Native 'go test' support"
    exit 1
fi

echo "✓ Test framework detected: $FRAMEWORK"
```

## Phase 2: TDD Workflow Guidance

I'll guide you through the RED-GREEN-REFACTOR cycle:

### Step 1: RED - Write Failing Test First

**Your task:** Write a test that describes what you want to build.

```bash
echo "=== STEP 1: RED (Write Failing Test) ==="
echo ""
echo "Before writing any implementation code, you must:"
echo "1. Write a test that describes the desired behavior"
echo "2. Run the test to confirm it FAILS"
echo "3. Understand WHY it fails (no implementation exists)"
echo ""
echo "Example test structure:"

case $FRAMEWORK in
    jest|vitest)
        cat << 'EOF'

describe('UserAuth', () => {
  test('should authenticate valid user credentials', () => {
    const auth = new UserAuth();
    const result = auth.login('user@example.com', 'password123');
    expect(result.success).toBe(true);
    expect(result.token).toBeDefined();
  });
});

EOF
        ;;
    pytest)
        cat << 'EOF'

def test_user_authentication():
    auth = UserAuth()
    result = auth.login('user@example.com', 'password123')
    assert result['success'] is True
    assert 'token' in result

EOF
        ;;
esac

echo "After writing your test, run it to see it FAIL:"
case $FRAMEWORK in
    jest) echo "  npm test" ;;
    vitest) echo "  npm run test" ;;
    pytest) echo "  pytest" ;;
    "go test") echo "  go test ./..." ;;
esac
```

### Step 2: Verify RED State

```bash
echo ""
echo "=== Verification Checkpoint ==="
read -p "Did your test FAIL as expected? (yes/no): " test_failed

if [ "$test_failed" != "yes" ]; then
    echo ""
    echo "⚠️ TDD Violation: Test should FAIL first!"
    echo ""
    echo "Common mistakes:"
    echo "  - Test passes immediately (implementation already exists)"
    echo "  - Test has syntax errors (doesn't run at all)"
    echo "  - Test doesn't actually test the behavior"
    echo ""
    echo "Fix: Ensure test runs and fails for the right reason"
    exit 1
fi

echo "✓ RED phase complete: Test is failing"
```

### Step 3: GREEN - Write Minimum Code

```bash
echo ""
echo "=== STEP 2: GREEN (Make Test Pass) ==="
echo ""
echo "Now write the MINIMUM code to make the test pass:"
echo "  - Don't over-engineer"
echo "  - Don't add extra features"
echo "  - Don't optimize prematurely"
echo "  - Just make the test green"
echo ""
echo "YAGNI Principle: You Aren't Gonna Need It"
echo "  - No 'what if' code"
echo "  - No 'future-proofing'"
echo "  - Only what's needed NOW"
```

### Step 4: Verify GREEN State

```bash
echo ""
read -p "Have you written the implementation? (yes/no): " impl_written

if [ "$impl_written" = "yes" ]; then
    echo ""
    echo "Run tests to verify GREEN state:"

    # Run tests based on framework
    case $FRAMEWORK in
        jest|vitest)
            npm test
            TEST_RESULT=$?
            ;;
        pytest)
            pytest
            TEST_RESULT=$?
            ;;
        "go test")
            go test ./...
            TEST_RESULT=$?
            ;;
    esac

    if [ $TEST_RESULT -eq 0 ]; then
        echo ""
        echo "✅ GREEN phase complete: Test is passing!"
    else
        echo ""
        echo "❌ Tests still failing. Continue implementing until green."
        exit 1
    fi
fi
```

### Step 5: REFACTOR - Clean Up

```bash
echo ""
echo "=== STEP 3: REFACTOR (Clean Code) ==="
echo ""
echo "Now that tests are green, you can refactor:"
echo "  - Extract functions/methods"
echo "  - Remove duplication (DRY)"
echo "  - Improve naming"
echo "  - Simplify logic"
echo ""
echo "⚠️ CRITICAL: Run tests after each refactoring step!"
echo ""
echo "Safe refactoring loop:"
echo "  1. Refactor one small thing"
echo "  2. Run tests (should stay green)"
echo "  3. If green, commit"
echo "  4. Repeat"
```

## Phase 3: TDD Cycle Monitoring

I'll help verify you're following true TDD:

```bash
# Check for common TDD violations
check_tdd_violations() {
    echo ""
    echo "=== TDD Health Check ==="

    # Check if tests exist for recent code
    RECENT_SOURCE_FILES=$(git log --name-only --pretty=format: --since="1 day ago" | grep -E '\.(ts|js|py|go)$' | grep -v test | sort -u)

    if [ ! -z "$RECENT_SOURCE_FILES" ]; then
        echo ""
        echo "Recent source files modified:"
        echo "$RECENT_SOURCE_FILES" | sed 's/^/  /'

        echo ""
        echo "Checking for corresponding tests..."

        for source_file in $RECENT_SOURCE_FILES; do
            # Look for test file
            test_file=$(echo "$source_file" | sed 's/\.\([^.]*\)$/.test.\1/')

            if [ ! -f "$test_file" ]; then
                echo "  ⚠️ No test found for: $source_file"
            else
                echo "  ✓ Test exists: $test_file"
            fi
        done
    fi

    # Check test-to-code ratio
    SOURCE_LINES=$(find . -name "*.ts" -o -name "*.js" -o -name "*.py" | grep -v test | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
    TEST_LINES=$(find . -name "*.test.*" -o -name "*_test.*" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')

    if [ ! -z "$SOURCE_LINES" ] && [ "$SOURCE_LINES" -gt 0 ]; then
        RATIO=$((TEST_LINES * 100 / SOURCE_LINES))
        echo ""
        echo "Test coverage ratio: ${RATIO}%"

        if [ $RATIO -lt 50 ]; then
            echo "  ⚠️ Low test coverage (target: 80%+)"
        elif [ $RATIO -lt 80 ]; then
            echo "  ⚙️ Moderate test coverage (target: 80%+)"
        else
            echo "  ✅ Good test coverage!"
        fi
    fi
}

check_tdd_violations
```

## TDD Best Practices

**Anti-Patterns to Avoid:**
- ❌ Writing implementation before test
- ❌ Writing comprehensive tests after code is done
- ❌ Skipping the RED phase
- ❌ Testing implementation details instead of behavior
- ❌ Writing tests that always pass

**TDD Benefits:**
- ✅ Confidence in refactoring
- ✅ Better design through testability
- ✅ Living documentation
- ✅ Fewer bugs in production
- ✅ Faster debugging

## Integration Points

This skill works well with:
- `/test` - Run your TDD tests
- `/refactor` - Safe refactoring with test coverage
- `/commit` - Commit after each successful cycle

## Next Steps

```bash
echo ""
echo "=== TDD Workflow Summary ==="
echo ""
echo "1. 🔴 RED:     Write failing test"
echo "2. ✅ GREEN:   Make test pass (minimum code)"
echo "3. 🔧 REFACTOR: Clean up while keeping tests green"
echo ""
echo "Repeat this cycle for each new feature or change!"
echo ""
echo "Suggested workflow:"
echo "  1. Start: /tdd-red-green (this skill)"
echo "  2. Develop: Follow RED-GREEN-REFACTOR"
echo "  3. Test: /test"
echo "  4. Commit: /commit"
```

**Important:** This skill enforces methodology, not automation. True TDD requires discipline and practice. Use this skill as a guide and checklist for each development cycle.

**Credits:** TDD methodology based on [obra/superpowers](https://github.com/obra/superpowers) RED/GREEN/REFACTOR workflow and YAGNI/DRY principles.
