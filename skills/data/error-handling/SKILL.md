---
name: error-handling
description: Guide for building resilient applications with robust error handling strategies. Use when designing APIs, debugging issues, or implementing resilience patterns like retries and circuit breakers.
---

# Error Handling Patterns

## When to use this skill
- Implementing error handling in new features
- Designing error-resilient APIs
- Debugging production issues or improving application reliability
- Creating better error messages
- Implementing resilience patterns (retry, circuit breaker)
- Handling async/concurrent errors

## Workflow
1.  **Analyze Context**: Determine the type of error (Recoverable vs Unrecoverable) and the appropriate handling philosophy (Exceptions vs Result Types).
2.  **Select Pattern**: Choose the right pattern (e.g., Retry, Circuit Breaker, Error Aggregation) based on the requirement.
3.  **Implement**: Apply the pattern using language-specific best practices.
4.  **Verify**: Ensure errors are caught, logged, and handled gracefully without crashing the application.

## Instructions

### 1. Philosophies & Categories
*   **Recoverable**: Network issues, input validation. Handle with Result types or specific exceptions.
*   **Unrecoverable**: OOM, bugs. Let it crash or catch at the top level.
*   **Exceptions**: Use for unexpected/exceptional conditions.
*   **Result Types**: Use for expected errors (validation, business logic).

### 2. Implementation by Language
*   **Python**: Use custom exception hierarchies (`ApplicationError`), context managers for cleanup, and decorators for retries.
*   **TS/JS**: Use custom `Error` classes, `Result` type pattern for explicit handling, and proper `async/await` try-catch blocks.
*   **Rust**: Use `Result` and `Option` types.
*   **Go**: Use explicit error returns and sentinel errors.

### 3. Universal Resilience Patterns
*   **Circuit Breaker**: For distributed systems to prevent cascading failures.
*   **Error Aggregation**: Collect multiple errors (e.g., validation) before failing.
*   **Graceful Degradation**: Fallback to cache or default values when primary fails.

### 4. Best Practices
*   **Fail Fast**: Validate early.
*   **Context**: Include metadata in errors.
*   **Log properly**: Don't spam logs for expected failures.
*   **Clean up**: Always release resources (finally, defer).

## Resources
*   [Exception Hierarchy Design](resources/exception-hierarchy-design.md)
*   [Error Recovery Strategies](resources/error-recovery-strategies.md)
*   [Async Error Handling](resources/async-error-handling.md)
