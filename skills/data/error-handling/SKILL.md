---
name: error-handling
description: Design global error handling for the .NET 8 WPF widget host app: unhandled exceptions, UI error surfaces, crash reporting, and user-safe recovery. Use when wiring App.xaml.cs exception hooks, adding error boundaries in ViewModels, or integrating crash reporting services.
---

# Error Handling

## Overview

Provide consistent, user-safe error handling across the shell, widgets, and background services.

## Core coverage

- App-domain and dispatcher exception handling
- Task scheduler unobserved exception handling
- UI error surfaces (toast/banner/dialog)
- Crash reporting and diagnostics export

## Definition of done (DoD)

- Global handlers registered in App.xaml.cs for: Dispatcher, AppDomain, TaskScheduler
- All exceptions are logged with correlation IDs before any recovery
- User sees friendly error message, not stack trace
- Crash reports include app version, correlation ID, and sanitized stack
- No swallowed exceptions without explicit justification comment

## Workflow

1. Register global handlers in App startup.
2. Add VM-level error capture for commands and async operations.
3. Define a UI error surface strategy (non-blocking by default).
4. Capture crash reports with correlation IDs.
5. Persist last error state for support export.

## Guidance

- Avoid swallowing exceptions; log and report.
- Use a consistent error model for UI messaging.
- Keep crash reporting opt-in if required by policy.

## References

- `references/global-handlers.md` for exception hooks.
- `references/ui-errors.md` for UI surface patterns.
- `references/crash-reporting.md` for report capture and storage.
