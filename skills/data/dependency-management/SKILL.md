---
name: dependency-management
description: Manage NuGet/.NET dependencies with enterprise-grade safety: versioning strategy, vulnerability awareness, licensing awareness, and minimizing supply-chain risk. Use when adding/updating packages or changing restore/build behavior.
---

# Dependency Management

## Overview

Dependencies are production code you did not write. Treat them as part of your threat and reliability surface.

## When to use

- Adding or upgrading any NuGet package
- Changing target frameworks or runtime settings
- Introducing SDKs (telemetry, auth, storage, sync)

## Definition of done (DoD)

- The dependency change is justified (why needed, why this package)
- Version choice is intentional (no accidental floating versions)
- No secrets/keys are introduced via packages or config templates
- Tests/builds still pass, and the change is scoped to the minimal set of packages

## Practical checklist

### Selection

- Prefer well-maintained packages with clear ownership and release cadence
- Avoid bringing in “kitchen sink” packages when a smaller one suffices
- Prefer official Microsoft packages for platform primitives when available

### Versioning

- Avoid floating versions unless there’s an explicit policy
- Keep transitive upgrades understandable (review `dotnet list package --include-transitive` when needed)

### Vulnerability and supply-chain awareness

- For package upgrades/additions, run `dotnet list package --vulnerable` (or CI equivalent) when feasible
- Avoid packages that require unsafe deserialization or reflection-heavy dynamic execution unless required

### Licensing (lightweight)

- For new dependencies, do a quick license sanity check (at least “is it permissive?”)

## Common anti-patterns

- Adding a package to solve a problem that can be solved in BCL
- Upgrading a large package graph without tests/verification
- Relying on transitive dependencies without understanding who pulls them in
