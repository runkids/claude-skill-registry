---
name: performance-profiling
description: Diagnose and improve WPF performance for the widget host app: UI virtualization, async usage, rendering cost, memory leaks, and profiling workflow. Use when investigating slow startup, laggy UI, or high memory usage.
---

# Performance Profiling

## Overview

Keep the shell and widgets responsive by profiling UI, async work, and memory usage.

## Definition of done (DoD)

- No `.Result` or `.Wait()` on async calls from UI thread
- Lists with >50 items use VirtualizingStackPanel
- Event handlers/timers disposed when views unload
- Startup time measured and tracked (target: <2s to usable)
- Memory usage profiled for leaks after opening/closing widgets

## Workflow

1. Reproduce the performance issue with a minimal scenario.
2. Profile UI thread usage and rendering cost.
3. Check data bindings and virtualization settings.
4. Validate async usage and background work.
5. Inspect memory growth and leaks.

## UI performance

- Use `VirtualizingStackPanel` for lists and grids.
- Disable heavy effects in scrolling regions.
- Prefer `BitmapCache` for static visuals when beneficial.

## Async guidance

- Offload IO and compute to background tasks.
- Avoid blocking the UI thread with `.Result` or `.Wait()`.
- Use cancellation tokens for long-running operations.

## Memory and leaks

- Remove event handlers and timers when views unload.
- Avoid long-lived static references to views or VMs.
- Use weak event patterns for global notifications.

## References

- `references/virtualization.md` for list and items control setup.
- `references/async-patterns.md` for UI-safe async usage.
- `references/memory-leaks.md` for leak detection tips.
