---
name: react-performance
description: React performance: memoization and virtualization guidelines
compatibility: opencode
license: MIT
metadata:
  stack: node-react-next
  style: solid-clean-code
---
## What I do

Je fournis des règles de performance pragmatiques :
- memoization sur besoin
- virtualisation pour grandes listes
- stabilité des props

## Decision checklist
Memoize seulement si au moins un de ces points est vrai :
- rendu coûteux
- liste volumineuse
- composant memoïsable (pur)
- callbacks stables nécessaires

## Examples

```ts
const derived = useMemo(() => heavy(users), [users]);
const onSelect = useCallback((id: string) => setId(id), []);
```

## Don’t
- "optimiser" avant d'avoir un problème mesurable.
