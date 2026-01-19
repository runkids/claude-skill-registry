---
name: verify
description: Run project verification checks (type-check, lint, unit tests, e2e tests, build). Use this skill when the user asks to verify the project, run checks, or validate code quality.
---

# Verify Project Skill

## Purpose

Run comprehensive project verification checks including type-checking, linting, unit tests, e2e tests, and build validation.

## When to Use

- User asks to verify project
- User asks to run checks/tests
- Before committing/pushing changes
- After code changes
- Before creating a PR

## Steps

1. **Run unit tests & build verification**

   ```bash
   npm run verify
   ```

   This runs: `type-check`, `lint`, `test`, and `build`

2. **Run e2e tests** (optional, recommended before release)

   ```bash
   npm run test:e2e
   ```

3. **Report results**
   - ✅ All passed
   - ❌ Show failures and fix them

## Available Scripts

### Core Verification

- `npm run verify` - runs type-check + lint + test + build
- `npm run type-check` - TypeScript validation
- `npm run lint` - ESLint check
- `npm run lint:fix` - Auto-fix linting issues
- `npm run test` - Run Jest unit tests
- `npm run test:e2e` - Run Playwright e2e tests
- `npm run build` - Build all packages

## Quality Gates

- ✅ Type check must pass
- ✅ Linting must pass (no warnings)
- ✅ All unit tests must pass
- ✅ Build must succeed
- ✅ E2E tests should pass (before release)
