---
name: api-endpoint-builder
description: "Build REST API endpoints. Use when: Designing or implementing API routes with security best practices. Not for: Client-side fetching or non-API logic."
context: fork
agent: Plan
allowed-tools: Read, Write, Edit, Bash
---

# API Endpoint Builder

Build REST API endpoints following security and performance best practices.

## Workflow

Execute this process for building API endpoints:

### 1. Plan the Endpoint
- Determine HTTP method (GET, POST, PUT, DELETE)
- Design path pattern following REST conventions
- Identify required input validation
- Define output format (JSON, status codes)

### 2. Validate Security
- Input validation and sanitization
- Authentication/authorization checks
- Rate limiting considerations
- SQL injection prevention
- XSS protection

### 3. Implement Structure
- Create route handler file
- Add middleware for validation
- Implement error handling
- Add request/response types
- Include logging

### 4. Add Tests
- Unit tests for handler
- Integration tests for route
- Validation test cases
- Error scenario tests

### 5. Verify Compliance
- Check error codes follow conventions
- Verify response format consistency
- Validate security headers
- Test input validation

## Example Implementation

```typescript
// POST /api/users
export async function POST(request: NextRequest) {
  try {
    // 1. Validate input
    const body = await request.json();
    const validated = CreateUserSchema.parse(body);

    // 2. Check authentication
    const user = await authenticate(request);
    if (!user || !hasPermission(user, 'create_user')) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // 3. Create user
    const newUser = await createUser(validated);

    // 4. Return response
    return NextResponse.json(
      { user: sanitizeUser(newUser) },
      { status: 201 }
    );
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Invalid input', details: error.errors },
        { status: 400 }
      );
    }

    logger.error('Create user failed', { error, userId: user?.id });
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

## Best Practices

- **Always validate input** - Use Zod or similar for schema validation
- **Use parameterized queries** - Prevent SQL injection
- **Implement rate limiting** - Protect against abuse
- **Log security events** - Track authentication failures
- **Use proper status codes** - 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 500 Internal Server Error
- **Sanitize output** - Prevent XSS attacks
- **Version your APIs** - Use /api/v1/ paths
- **Document responses** - Use OpenAPI/Swagger

## Integration

This skill integrates with:
- `security` - Security patterns and validation
- `backend-patterns` - Backend best practices
- `tdd-workflow` - Testing requirements
