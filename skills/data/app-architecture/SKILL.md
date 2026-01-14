---
name: app-architecture
description: Define and maintain clean architecture for the .NET 8 WPF widget host app. Use when shaping solution structure, layer boundaries, dependency rules, DI wiring, and project layout to keep UI, application, domain, and infrastructure separated.
---

# App Architecture

## Overview

Keep a clean, scalable structure that supports a widget host with a single shell and optional secondary windows.

## Constraints

- .NET 8
- WPF UI layer with MVVM
- Clean architecture boundaries

## Layering rules

- Domain: entities, value objects, invariants, domain services.
- Application: use cases, DTOs, interfaces, orchestration.
- Infrastructure: persistence, external services, OS integration.
- UI: WPF views, view models, shell, resources.

## Dependency rules

- Dependencies flow inward only.
- Domain has no dependencies on UI or infrastructure.
- Application depends on domain.
- Infrastructure depends on application/domain.
- UI depends on application/domain (and optionally infrastructure via DI).

## Project layout (suggested)

- `3SC.Domain`
- `3SC.Application`
- `3SC.Infrastructure`
- `3SC.UI`

## Definition of done (DoD)

- Dependencies flow inward only (verified via project references)
- Domain has zero external NuGet references (except test frameworks in test projects)
- Interfaces live in Application/Domain; implementations in Infrastructure/UI
- DI wiring is explicit in composition root (App.xaml.cs or equivalent)
- No "shortcut" references that bypass layers

## Workflow

1. Identify the change scope (UI, application, domain, infrastructure).
2. Create or move types into the correct layer.
3. Define interfaces in Application/Domain, implement in Infrastructure.
4. Wire DI at the composition root (UI startup).
5. Validate boundaries before adding new references.

## References

- `references/layering.md` for boundary and dependency rules.
- `references/solution-structure.md` for project layout guidance.
- `references/di-composition.md` for DI setup and module wiring.
