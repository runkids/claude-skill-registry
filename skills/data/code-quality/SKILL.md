---
name: code-quality
description: Establish enterprise-grade code quality baselines for the .NET solution: analyzers, nullability, formatting, complexity limits, and review-ready diffs. Use when changing production code, refactoring, or introducing new project patterns.
---

# Code Quality

## Overview

Turn “good engineering habits” into repeatable quality gates.

This skill is intentionally cross-cutting: it applies to UI, application, domain, and infrastructure code.

## When to use

- Any non-trivial code change (new feature, bug fix, refactor)
- Adding a new project, package, or architectural pattern
- Touching error-prone areas (async, threading, I/O, serialization)

## Definition of done (DoD)

- Builds cleanly locally (`dotnet build`) with no new warnings introduced
- Tests pass for the nearest scope (`dotnet test` for the affected test project(s))
- Nullability decisions are explicit (no “spray-and-pray” `!` suppression)
- Public APIs are intentional (avoid accidental `public` surface)
- Changes are small and reviewable (prefer focused commits/diffs)

## Practical checklist

### Readability and maintainability

- Prefer descriptive names over abbreviations
- Avoid deep nesting; extract methods when cognitive load increases
- Keep side effects localized (especially in constructors)

### Error handling

- Throw exceptions for programming errors; return results for expected failures
- Do not swallow exceptions; either handle and continue safely, or log/report and fail fast

### Async and threading

- Avoid blocking (`.Result`, `.Wait()`) on async paths
- Prefer `CancellationToken` for long-running/interactive operations
- Keep UI thread work minimal; offload I/O and CPU-bound work

### Analyzers/formatting (repo-level standards)

- If `.editorconfig` is missing and you’re doing broad work, consider adding one alongside the change
- Prefer enabling analyzers over suppressing them
- If a suppression is necessary, scope it narrowly and document the reason

## Common anti-patterns

- Catch-all `catch (Exception)` without a clear recovery strategy
- Logging secrets/PII or large payloads
- “Fix” via disabling warnings globally instead of addressing root cause

## Notes

This skill describes quality gates; the exact enforcement mechanism (CI pipeline, analyzers, formatting tooling) should evolve over time.
