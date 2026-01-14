---
name: domain-modeling
description: Model core domain concepts for the widget host app: entities, value objects, aggregates, invariants, and domain services. Use when defining the domain layer, enforcing rules, or refactoring business logic out of UI/application layers.
---

# Domain Modeling

## Overview

Define stable domain concepts and invariants so business rules live outside the UI and infrastructure.

## Core concepts

- Entities: identity-based objects with lifecycle.
- Value objects: immutable, equality by value.
- Aggregates: consistency boundaries for changes.
- Domain services: behavior that does not belong to a single entity/value object.

## Definition of done (DoD)

- Value objects are immutable (no public setters)
- Entities validate invariants in constructors/factory methods
- Domain has no dependencies on Infrastructure or UI
- Invalid state is rejected at creation, not deferred to save
- Domain types have corresponding unit tests for invariants

## Invariants

- Keep invariants inside the aggregate root.
- Enforce invariants via constructors/factory methods.
- Reject invalid state early; do not rely on UI validation alone.

## Workflow

1. Identify domain nouns/verbs (widgets, layouts, schedules).
2. Choose entity vs value object and define invariants.
3. Group related entities into aggregates.
4. Extract domain services for cross-entity behavior.
5. Keep domain types persistence-agnostic.

## Examples

Use value objects for identities, sizes, positions, and schedule settings to keep behavior consistent.

## References

- `references/entities-and-values.md` for modeling guidelines.
- `references/aggregates.md` for aggregate boundaries.
- `references/invariants.md` for rule enforcement patterns.
