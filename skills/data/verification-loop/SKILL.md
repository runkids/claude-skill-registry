---
name: verification-loop
description: "6-phase sequential verification system for quality assurance. Use when: Validating changes before commit, ensuring code quality, or running comprehensive checks. Not for: Quick smoke tests or single verification checks."
---

# Verification Loop System

Comprehensive quality assurance through 6 sequential verification gates: build → type → lint → test → security → diff.

## The 6-Phase Gate System

```
┌─────────────────────────────────────────────────────────────┐
│                    VERIFICATION LOOP                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. BUILD GATE     ──► Project builds successfully          │
│         │                                                     │
│         ▼                                                     │
│  2. TYPE GATE     ──► Type checking passes                   │
│         │                                                     │
│         ▼                                                     │
│  3. LINT GATE     ──► Code style and quality checks          │
│         │                                                     │
│         ▼                                                     │
│  4. TEST GATE     ──► Tests pass with 80%+ coverage          │
│         │                                                     │
│         ▼                                                     │
│  5. SECURITY GATE ──► No secrets, console.logs, vulnerabilities│
│         │                                                     │
│         ▼                                                     │
│  6. DIFF GATE     ──► Changes reviewed for issues            │
│         │                                                     │
│         ▼                                                     │
│    ALL PASS ──► Changes verified ✓                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Gate Descriptions

### 1. Build Gate

**Purpose**: Verify the project builds successfully.

**What it checks**:

- Compilation succeeds
- Dependencies are resolved
- Build artifacts are generated

**Commands by project type**:

- Node.js: `npm run build`, `pnpm build`, `yarn build`
- Python: `python -m build`, `pip install -e .`
- Rust: `cargo build`
- Go: `go build`
- Java: `mvn compile`, `gradle build`
- No build system: Skip (exit 0)

**Failure behavior**: Stop verification, report build errors

### 2. Type Gate

**Purpose**: Verify type safety.

**What it checks**:

- Type checking passes
- No type errors
- Type definitions are valid

**Commands by project type**:

- TypeScript: `tsc --noEmit`
- Python: `mypy` (if configured)
- Pyright: `pyright`
- Go: `go vet` (partial type checking)
- No type system: Skip (exit 0)

**Failure behavior**: Stop verification, report type errors

### 3. Lint Gate

**Purpose**: Verify code style and quality.

**What it checks**:

- Code style consistency
- Potential bugs and anti-patterns
- Code quality standards

**Commands by project type**:

- JavaScript/TypeScript: `eslint`, `prettier --check`
- Python: `pylint`, `flake8`, `black --check`
- Rust: `cargo clippy`
- Go: `gofmt`, `golint`
- No linter configured: Skip with warning

**Failure behavior**: Stop verification, report lint errors

### 4. Test Gate

**Purpose**: Verify tests pass with sufficient coverage.

**What it checks**:

- All tests pass
- Coverage meets minimum threshold (80%)
- No test failures or skips

**Commands by project type**:

- Node.js: `npm test`, `jest --coverage`
- Python: `pytest --cov`
- Rust: `cargo test`
- Go: `go test ./...`
- No tests: Warning (not failure for small changes)

**Failure behavior**: Stop verification, report test failures

### 5. Security Gate

**Purpose**: Verify no security issues.

**What it checks**:

- No hardcoded secrets (API keys, passwords)
- No debug console.log statements
- No known vulnerabilities
- File permissions are appropriate

**Commands by project type**:

- Secrets: `git diff --cached | grep -iE '(password|secret|api_key|token)'\`
- Console logs: `git diff --cached | grep -E 'console\.(log|debug|info|warn|error)'`
- Vulnerabilities: `npm audit`, `pip-audit`, `cargo audit`
- File permissions: `find . -type f -perm /o+w`

**Failure behavior**: Stop verification, report security issues

### 6. Diff Gate

**Purpose**: Review changes for potential issues.

**What it checks**:

- Changes are intentional
- No commented-out code
- No TODO/FIXME left in changes
- Files are properly formatted

**Commands**:

```bash
# Check for commented-out code
git diff --cached | grep -E '^\+.*//.*code|^\+.*#.*code'

# Check for TODO/FIXME
git diff --cached | grep -E '^\+.*TODO|^\+.*FIXME'

# Verify formatting
git diff --cached --name-only | xargs prettier --check 2>/dev/null || true
```

**Failure behavior**: Warning (doesn't block, but alerts)

## Sequential Enforcement

Gates must pass **in order**. If a gate fails:

1. Stop verification immediately
2. Report the failure with details
3. Do not run subsequent gates
4. Provide actionable error messages

**Rationale**: Later gates depend on earlier gates passing. For example:

- Can't run tests if build fails
- Can't check coverage if tests fail
- Security scan requires compiled artifacts

## Exit Codes

Each gate script uses standard exit codes:

- **0**: Gate passed
- **1**: Gate failed (stop verification)
- **2**: Gate skipped (not applicable)

## Usage Patterns

### Manual Verification

Run the full loop manually:

```bash
# Run all gates sequentially
.claude/scripts/gates/build-gate.sh && \
.claude/scripts/gates/type-gate.sh && \
.claude/scripts/gates/lint-gate.sh && \
.claude/scripts/gates/test-gate.sh && \
.claude/scripts/gates/security-gate.sh && \
.claude/scripts/gates/diff-gate.sh
```

### Pre-Commit Hook

Configure as pre-commit hook in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreCommit": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/scripts/gates/verification-loop.sh",
            "description": "Run 6-phase verification before commit"
          }
        ]
      }
    ]
  }
}
```

### Individual Gates

Run specific gates as needed:

```bash
# Quick type check
.claude/scripts/gates/type-gate.sh

# Security scan only
.claude/scripts/gates/security-gate.sh
```

## Integration with Seed System

### Verification-Before-Completion

The verification-loop enhances `verification-before-completion` with:

| Aspect      | verification-before-completion | verification-loop         |
| ----------- | ------------------------------ | ------------------------- |
| Scope       | General principle              | Specific 6-phase workflow |
| Trigger     | Manual invocation              | Automated pre-commit      |
| Feedback    | Conceptual                     | Concrete exit codes       |
| Integration | Complementary                  | Implements the principle  |

**Integration**: Use verification-loop as the implementation of verification-before-completion for automated quality gates.

### Ralph Orchestrator

Ralph uses verification-loop for component validation:

- **Test Designer hat**: Designs tests for component
- **verification-loop**: Executes 6-phase gates to validate
- **Two-stage review**: Spec compliance → Quality review

**Integration**: Ralph's validation workflow includes verification-loop as the quality enforcement phase.

### TDD-Workflow

The two systems complement each other:

- **TDD**: red → green → refactor (development cycle)
- **Verification-loop**: build → type → lint → test → security → diff (validation phase)

**Integration**: Run verification-loop after TDD cycle completes to validate the implementation.

## Verification Log

Results are logged to `~/.claude/homunculus/verification-log.jsonl`:

```jsonl
{"timestamp":"2025-01-27T10:30:00Z","gate":"build","status":"pass","duration_ms":1200}
{"timestamp":"2025-01-27T10:30:01Z","gate":"type","status":"pass","duration_ms":800}
{"timestamp":"2025-01-27T10:30:02Z","gate":"lint","status":"fail","duration_ms":500,"error":"ESLint errors in 3 files"}
```

## Best Practices

1. **Run locally first**: Don't push failing code to CI
2. **Fix in order**: Address build errors before type errors before lint errors
3. **Keep tests fast**: Verification should complete in <2 minutes
4. **Configure appropriately**: Adjust gates for your project type
5. **Automate via hooks**: Use pre-commit hooks to enforce gates

## Related Skills

- **verification-before-completion**: General principle of evidence-based completion
- **tdd-workflow**: Test-driven development methodology
- **security**: Security patterns and vulnerability scanning

## Key Principle

Sequential enforcement ensures quality at each step. Fix issues in order: build → type → lint → test → security → diff.
