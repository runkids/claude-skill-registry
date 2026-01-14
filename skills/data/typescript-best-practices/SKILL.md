---
name: typescript-best-practices
description: "Auto-load when writing TypeScript code. Provides patterns for type safety, async handling, and modern TypeScript idioms."
---

# TypeScript Best Practices

## Type Safety

### Strict Types
```typescript
// Use strict null checks
function process(value: string | null): string {
  if (value === null) return 'default';
  return value.toUpperCase();
}

// Use unknown over any
function parseJSON(input: string): unknown {
  return JSON.parse(input);
}

// Type guards for narrowing
function isUser(obj: unknown): obj is User {
  return typeof obj === 'object' && obj !== null && 'id' in obj;
}
```

### Const Assertions
```typescript
const CONFIG = {
  api: 'https://api.example.com',
  timeout: 5000,
} as const;

const ROLES = ['admin', 'user', 'guest'] as const;
type Role = typeof ROLES[number]; // 'admin' | 'user' | 'guest'
```

## Async Patterns

### Error Handling
```typescript
type Result<T, E> =
  | { success: true; data: T }
  | { success: false; error: E };

async function fetchData(): Promise<Result<Data, Error>> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      return { success: false, error: new Error(`HTTP ${response.status}`) };
    }
    return { success: true, data: await response.json() };
  } catch (error) {
    return { success: false, error: error instanceof Error ? error : new Error(String(error)) };
  }
}
```

### Parallel Operations
```typescript
// Parallel with Promise.all
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
]);

// With error handling
const results = await Promise.allSettled([fetchUsers(), fetchPosts()]);
const successful = results
  .filter((r): r is PromiseFulfilledResult<Data> => r.status === 'fulfilled')
  .map(r => r.value);
```

## Common Patterns

### Discriminated Unions
```typescript
type State =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: Data }
  | { status: 'error'; error: Error };

function render(state: State) {
  switch (state.status) {
    case 'idle': return <Idle />;
    case 'loading': return <Loading />;
    case 'success': return <Success data={state.data} />;
    case 'error': return <Error error={state.error} />;
  }
}
```

### Utility Types
```typescript
Partial<T>      // All props optional
Required<T>     // All props required
Readonly<T>     // All props readonly
Pick<T, K>      // Subset of props
Omit<T, K>      // Exclude props
Record<K, V>    // Object with K keys and V values
```

## Anti-Patterns to Avoid
- `any` - use `unknown` instead
- Non-null assertion abuse (`value!.prop`)
- Type assertions when type guards work
- Implicit any in callbacks
- Barrel files with circular deps
