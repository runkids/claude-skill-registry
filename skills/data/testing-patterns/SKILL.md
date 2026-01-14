---
name: testing-patterns
description: "Auto-load when writing tests. Provides TDD workflow, test structure patterns, and common testing idioms."
---

# Testing Patterns

## TDD Workflow (RED-GREEN-REFACTOR)

### 1. RED: Write Failing Test First
```typescript
describe('Calculator', () => {
  it('should add two numbers', () => {
    const calc = new Calculator();
    expect(calc.add(2, 3)).toBe(5);
  });
});
```
Run test - verify it FAILS for the right reason.

### 2. GREEN: Minimal Implementation
```typescript
class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }
}
```
Run test - verify it PASSES.

### 3. REFACTOR: Clean Up
Improve code while keeping tests green.

## Test Structure (AAA Pattern)

```typescript
it('should transfer money between accounts', () => {
  // Arrange - Set up test data
  const source = new Account(100);
  const target = new Account(0);

  // Act - Perform the action
  source.transfer(50, target);

  // Assert - Verify results
  expect(source.balance).toBe(50);
  expect(target.balance).toBe(50);
});
```

## What to Test

### DO Test
- Business logic and calculations
- Edge cases and boundaries
- Error handling paths
- State transitions
- Integration points

### DON'T Test
- Framework code (React, Express)
- Third-party libraries
- Simple getters/setters
- Implementation details

## Mocking Guidelines

```typescript
// Mock external dependencies
jest.mock('./api', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: 1, name: 'Test' }),
}));

// Prefer dependency injection over mocking
class UserService {
  constructor(private api: ApiClient) {}

  async getUser(id: number) {
    return this.api.fetchUser(id);
  }
}

// In tests - inject mock
const mockApi = { fetchUser: jest.fn() };
const service = new UserService(mockApi);
```

## Test Naming Convention

```typescript
describe('[Unit Under Test]', () => {
  describe('[Method/Scenario]', () => {
    it('should [expected behavior] when [condition]', () => {
      // test
    });
  });
});
```

## Async Testing

```typescript
// Async/await (preferred)
it('should fetch user', async () => {
  const user = await fetchUser(1);
  expect(user.name).toBe('Test');
});

// Testing rejections
it('should throw on invalid id', async () => {
  await expect(fetchUser(-1)).rejects.toThrow('Invalid ID');
});
```

## Coverage Targets
- Aim for 80% coverage on business logic
- 100% coverage on critical paths (auth, payments)
- Don't chase 100% everywhere - diminishing returns
