---
name: testing-strategy
description: Testing strategy for backend use-cases and frontend hooks/UI
compatibility: opencode
license: MIT
metadata:
  stack: node-react-next
  style: solid-clean-code
---
## What I do

Je propose une stratégie de tests cohérente full-stack.

## Backend
- Domain : tests purs.
- Use-cases : tests unitaires avec ports mockés.
- Infra : intégration ciblée.

## Frontend
- Hooks : tests avec QueryClient isolé + mocks services.
- UI : tests d'interaction et accessibilité.

## Mock philosophy
- Préférer des fakes typés (implémentations d'interface) plutôt que des mocks dynamiques.
