---
name: "component-patterns"
description: "React component architecture and composition patterns for type-safe development. Use when designing component APIs, implementing composition patterns, or structuring component libraries."
---

# Component Architecture Patterns

## Component API Design

### Props Interface Pattern

```typescript
interface ComponentProps {
  // Required props
  children: React.ReactNode;

  // Variants (discriminated unions preferred)
  variant?: 'primary' | 'secondary' | 'danger';

  // Optional with defaults
  size?: 'sm' | 'md' | 'lg';

  // Callbacks
  onClick?: () => void;

  // Style override
  className?: string;

  // Pass-through HTML attrs
  'aria-label'?: string;
}

function Component({
  children,
  variant = 'primary',
  size = 'md',
  className,
  ...rest
}: ComponentProps) {
  return (
    <button
      className={`btn-${variant} btn-${size} ${className}`}
      {...rest}
    >
      {children}
    </button>
  );
}
```

### Extending HTML Elements

```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
}

// Gets all button attributes + custom props
```

## Composition Patterns

### Compound Components

For components with shared implicit state:

```typescript
const TabsContext = React.createContext<{
  active: string;
  setActive: (id: string) => void;
} | null>(null);

function Tabs({ children, defaultTab }: {
  children: React.ReactNode;
  defaultTab: string;
}) {
  const [active, setActive] = React.useState(defaultTab);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      {children}
    </TabsContext.Provider>
  );
}

function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const ctx = React.useContext(TabsContext);
  if (!ctx) throw new Error('Tab must be within Tabs');

  return (
    <button
      onClick={() => ctx.setActive(id)}
      aria-selected={ctx.active === id}
    >
      {children}
    </button>
  );
}

// Usage
<Tabs defaultTab="one">
  <Tab id="one">Tab 1</Tab>
  <Tab id="two">Tab 2</Tab>
</Tabs>
```

**Use when**: Components need to coordinate state implicitly.

### Render Props

For flexible rendering logic:

```typescript
function DataFetcher<T>({
  url,
  render,
}: {
  url: string;
  render: (props: {
    data: T | null;
    loading: boolean;
    error: Error | null;
  }) => React.ReactNode;
}) {
  const [data, setData] = React.useState<T | null>(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<Error | null>(null);

  // Fetch logic...

  return <>{render({ data, loading, error })}</>;
}

// Usage
<DataFetcher
  url="/api/users"
  render={({ data, loading, error }) => {
    if (loading) return <Spinner />;
    if (error) return <Error error={error} />;
    return <List items={data} />;
  }}
/>
```

**Use when**: Rendering logic varies significantly between uses.

## Custom Hooks

Extract reusable logic:

```typescript
function useLocalStorage<T>(key: string, initial: T) {
  const [value, setValue] = React.useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initial;
  });

  React.useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}

// Usage
function ThemeToggle() {
  const [theme, setTheme] = useLocalStorage('theme', 'light');
  return <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')} />;
}
```

**Extract when**: Logic is reused across 2+ components.

## Performance Patterns

### Memoization

```typescript
// Expensive computation
const processed = React.useMemo(
  () => expensiveOperation(data),
  [data]
);

// Component memoization
const Child = React.memo(function Child({ value }: { value: string }) {
  return <div>{value}</div>;
});

// Callback stability
const handleClick = React.useCallback(() => {
  doSomething(id);
}, [id]);
```

**Use when**:
- `useMemo`: Expensive computation, runs every render
- `React.memo`: Component re-renders with same props
- `useCallback`: Callback passed to memoized children

**Don't overuse**: Profile first. Premature optimization adds complexity.

## TypeScript Patterns

### Generic Components

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>
          {renderItem(item)}
        </li>
      ))}
    </ul>
  );
}

// Usage is fully typed
<List
  items={users}
  renderItem={user => <span>{user.name}</span>}
  keyExtractor={user => user.id}
/>
```

### Discriminated Union Props

```typescript
type ButtonProps =
  | { variant: 'link'; href: string; onClick?: never }
  | { variant: 'button'; onClick: () => void; href?: never };

// TypeScript enforces: link must have href, button must have onClick
```

## Accessibility Patterns

### Semantic HTML First

```typescript
// Good
<nav>
  <ul>
    <li><a href="/docs">Docs</a></li>
  </ul>
</nav>

// Avoid
<div className="nav">
  <div onClick={...}>Docs</div>
</div>
```

### ARIA When Needed

```typescript
<button
  onClick={onClose}
  aria-label="Close dialog"
  aria-describedby="dialog-description"
>
  ×
</button>
```

**When to use ARIA**:
- Non-semantic elements with semantic roles
- Additional context for screen readers
- Dynamic state (aria-expanded, aria-selected)

**When not to use**: Semantic HTML already provides meaning.

### Keyboard Navigation

```typescript
function Dropdown({ items }: { items: Item[] }) {
  const [selected, setSelected] = React.useState(0);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelected(s => Math.min(s + 1, items.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelected(s => Math.max(s - 1, 0));
        break;
      case 'Enter':
        e.preventDefault();
        handleSelect(items[selected]);
        break;
      case 'Escape':
        close();
        break;
    }
  };

  return <div onKeyDown={handleKeyDown}>...</div>;
}
```

## Error Boundaries

```typescript
class ErrorBoundary extends React.Component<
  { children: React.ReactNode; fallback: React.ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('Caught error:', error, info);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<ErrorFallback />}>
  <App />
</ErrorBoundary>
```

**Note**: Error boundaries catch rendering errors, not event handler errors.

## Component Organization

### File Structure

```
components/
  Button/
    Button.tsx
    Button.module.css
    Button.test.tsx
    index.ts          # Export
```

### Component Template

```typescript
import styles from './Component.module.css';

interface ComponentProps {
  // Props
}

/**
 * Component description
 *
 * @example
 * <Component prop="value" />
 */
export function Component({
  prop,
}: ComponentProps) {
  // Implementation

  return (
    <div className={styles.root}>
      {/* JSX */}
    </div>
  );
}
```

## Testing Patterns

### Component Testing

```typescript
import { render, screen, fireEvent } from '@testing-library/react';

describe('Button', () => {
  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    fireEvent.click(screen.getByRole('button'));

    expect(handleClick).toHaveBeenCalledOnce();
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled onClick={() => {}}>Click</Button>);

    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

**Test user behavior, not implementation.**

## Common Pitfalls

**Prop drilling** (passing props through many levels):
- Solution: Context API or state management

**Missing keys in lists**:
- Always provide stable, unique keys
- Don't use array index as key if list can reorder

**Inline function definitions**:
- Creates new function every render
- Use `useCallback` if passed to memoized children

**Mutating state**:
- Always return new objects/arrays
- Use spread syntax or immutability helpers

## Decision Checklist

When designing components:
- [ ] Props interface is clear and type-safe
- [ ] Variants use discriminated unions if mutually exclusive
- [ ] Accessibility requirements met (semantic HTML, ARIA, keyboard)
- [ ] Performance considerations addressed (memoization if needed)
- [ ] Error handling present
- [ ] Composable with other components
- [ ] Tested (key user interactions)
