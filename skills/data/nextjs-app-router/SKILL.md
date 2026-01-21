---
name: nextjs-app-router
description: Guía para desarrollo frontend con Next.js 15, App Router, Server Actions y React Query.
trigger: frontend OR dashboard-admin OR nextjs OR react
scope: dashboard-admin
---

# Next.js 15 App Router Skill

## Description

Guía para el desarrollo frontend utilizando Next.js 15, App Router y Server Actions.

## Trigger

- Cuando se editen archivos en `/dashboard-admin/src/app`.
- Cuando se generen nuevos layouts, páginas o componentes.
- Cuando se discuta sobre data fetching o mutaciones.

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)

## Best Practices

1.  **Server Components by Default:**
    - Todo componente es Server Component a menos que tenga `"use client"`.
    - Mantener la lógica de servidor (acceso a DB, secrets) fuera del cliente.

2.  **Server Actions para Mutaciones:**
    - No usar API Routes (`/pages/api`) para mutaciones simples.
    - Definir acciones en archivos `actions.ts` con `"use server"`.
    - Invocar acciones directamente desde `<form>` o `onClick` (con `startTransition`).

3.  **Data Fetching:**
    - Usar `src/lib/api.ts` o llamadas directas a DB (Prisma) en Server Components.
    - Para cliente, usar **React Query** (`@tanstack/react-query`) para cache y revalidación.

4.  **Estilos (Tailwind + Shadcn):**
    - No crear clases CSS custom. Usar utilidades de Tailwind.
    - Usar componentes de `src/components/ui` (Shadcn) para consistencia.

## Code Snippets

### Server Action Pattern

```typescript
"use server";

import { revalidatePath } from "next/cache";
import { db } from "@/lib/db";

export async function createItem(formData: FormData) {
  const name = formData.get("name");

  await db.item.create({ data: { name } });
  revalidatePath("/items");
}
```

### Client Component Pattern

```typescript
'use client'

import { useTransition } from 'react'
import { createItem } from './actions'

export function ItemForm() {
  const [isPending, startTransition] = useTransition()

  return (
    <button
      onClick={() => startTransition(() => createItem(new FormData()))}
      disabled={isPending}
    >
      {isPending ? 'Saving...' : 'Save'}
    </button>
  )
}
```
