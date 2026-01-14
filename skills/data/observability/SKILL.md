---
name: observability
description: Unified observability for the .NET 8 WPF widget host app - logging, telemetry, health checks, diagnostics exports, and operational tooling. Use when configuring Serilog, Application Insights, health checks, correlation IDs, or support tools.
---

# Observability

## Overview

Provide unified logging, telemetry, and operational tooling that helps diagnose issues in development and production.

## Core Areas

### 1. Structured Logging
- Serilog with file sink (rolling, 7-day retention)
- Application Insights for cloud telemetry
- ETW for local diagnostics
- Correlation IDs on user-initiated actions

### 2. Telemetry
- Custom events for key actions (AppStarted, WidgetCreated, SyncCompleted)
- Exception tracking with stack traces
- Performance metrics (startup time, memory, responsiveness)

### 3. Health Checks
- Database connectivity
- Sync service availability
- Configuration validity
- Widget instance integrity

### 4. Diagnostics Export
- Logs (last N days, redacted)
- Configuration (sanitized)
- Environment info (OS, .NET version, app version)
- Health check results

## Definition of Done (DoD)

- [ ] Serilog configured with file sink (7-day rolling)
- [ ] Correlation IDs present on all user-initiated actions
- [ ] No PII or secrets in logs (verified before merge)
- [ ] Structured properties used instead of string interpolation
- [ ] Application Insights wired when connection string available
- [ ] Health check for each critical subsystem (DB, sync, config)
- [ ] Diagnostics export redacts all tokens/secrets/PII
- [ ] Support tools accessible from Settings or Help menu
- [ ] Log levels appropriate (Debug for verbose, Warning+ for production)

## Key Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `LogBootstrapper` | `3SC/Logging/` | Serilog initialization |
| `CorrelationContext` | `3SC/Logging/` | Scoped correlation IDs |
| `OperationLogger` | `3SC/Logging/` | Operation logging with timing |
| `TelemetryEventSource` | `3SC/Logging/` | ETW event source |
| `HealthService` | `3SC/Observability/` | Health check orchestration |
| `DiagnosticsExportService` | `3SC/Services/` | Export bundle creation |

## Workflow

1. Use `CorrelationContext.BeginScope()` for user-initiated operations
2. Log with structured properties: `Log.Information("Widget {WidgetId} created", id)`
3. Add health checks for new subsystems in `Observability/Checks/`
4. Include new data in diagnostics export when relevant
5. Never log secrets, tokens, or PII

## Anti-Patterns

- ❌ String interpolation in logs: `Log.Information($"User {name}")`
- ❌ Swallowing exceptions without logging
- ❌ Logging sensitive data
- ❌ Missing correlation IDs on async operations

## References

- `3SC/Logging/` for logging implementation
- `3SC/Observability/` for health checks
- `3SC/Services/DiagnosticsExportService.cs` for export

