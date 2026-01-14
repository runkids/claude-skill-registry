---
name: API Design
description: REST API best practices, OpenAPI/Swagger patterns, authentication, and error response formats
keywords:
  - api
  - rest
  - openapi
  - swagger
  - authentication
  - jwt
  - oauth
---

# API Design

## When to Use

**Perfect for:**
- Designing RESTful web services
- Mobile and web client integrations
- Microservices architecture
- Public and private API development
- API documentation and schema definition

**Not ideal for:**
- Real-time communication (use WebSockets/gRPC)
- File streaming (use direct downloads)
- Complex queries (consider GraphQL or gRPC)

## Quick Reference

### REST API Principles
```
GET    /api/v1/users              - List all users
POST   /api/v1/users              - Create new user
GET    /api/v1/users/{id}         - Get specific user
PUT    /api/v1/users/{id}         - Replace user
PATCH  /api/v1/users/{id}         - Update user fields
DELETE /api/v1/users/{id}         - Delete user

GET    /api/v1/users/{id}/posts   - Get user's posts
POST   /api/v1/users/{id}/posts   - Create post for user
```

### Standard HTTP Status Codes
```
2xx Success:
  200 OK                  - Request succeeded
  201 Created             - Resource created
  202 Accepted            - Request accepted for processing
  204 No Content          - Success, no body to return

3xx Redirection:
  301 Moved Permanently   - Resource moved
  304 Not Modified        - Use cached response
  307 Temporary Redirect  - Use same method for redirect

4xx Client Error:
  400 Bad Request         - Invalid request format
  401 Unauthorized        - Authentication required
  403 Forbidden           - Authenticated but no permission
  404 Not Found           - Resource doesn't exist
  409 Conflict            - Request conflicts with current state
  422 Unprocessable       - Validation failed
  429 Too Many Requests   - Rate limit exceeded

5xx Server Error:
  500 Internal Server Error - Unexpected server error
  502 Bad Gateway           - Invalid upstream response
  503 Service Unavailable   - Server temporarily down
```

### Standard Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "status": 422,
    "timestamp": "2024-01-15T10:30:00Z",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "type": "format"
      },
      {
        "field": "age",
        "message": "Must be between 18 and 120",
        "type": "range"
      }
    ],
    "request_id": "req_12345abcde"
  }
}
```

### Success Response Format
```json
{
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "meta": {
    "request_id": "req_12345abcde",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### OpenAPI/Swagger Specification
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
  description: API for managing users
  contact:
    name: API Support
    email: support@example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /users:
    get:
      operationId: listUsers
      summary: List all users
      tags:
        - Users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
          description: Maximum number of users
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
          description: Number of users to skip
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  meta:
                    $ref: '#/components/schemas/Pagination'
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

    post:
      operationId: createUser
      summary: Create new user
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '422':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ValidationError'

  /users/{userId}:
    get:
      operationId: getUser
      summary: Get user by ID
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: User details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
      properties:
        id:
          type: integer
        name:
          type: string
          minLength: 1
          maxLength: 100
        email:
          type: string
          format: email
        age:
          type: integer
          minimum: 0
          maximum: 150
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    CreateUserRequest:
      type: object
      required:
        - email
        - name
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        email:
          type: string
          format: email
        age:
          type: integer
          minimum: 0
          maximum: 150

    Error:
      type: object
      required:
        - error
      properties:
        error:
          type: object
          required:
            - code
            - message
          properties:
            code:
              type: string
            message:
              type: string
            status:
              type: integer

    ValidationError:
      allOf:
        - $ref: '#/components/schemas/Error'
        - type: object
          properties:
            details:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                  message:
                    type: string

    Pagination:
      type: object
      properties:
        total:
          type: integer
        limit:
          type: integer
        offset:
          type: integer

security:
  - bearerAuth: []
```

### JWT Authentication Pattern
```python
from datetime import datetime, timedelta, timezone
import jwt
from typing import Optional

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Usage in API
def get_current_user(token: str) -> Optional[dict]:
    payload = verify_token(token)
    if not payload:
        raise Exception("Invalid or expired token")
    return payload
```

### OAuth 2.0 Flow Pattern
```
User -> Client App -> Authorization Server -> Client App -> Resource Server

1. User clicks "Login with Provider"
2. Client redirects to authorization endpoint:
   GET /oauth/authorize?client_id=xxx&redirect_uri=...&scope=read:user&state=random

3. User authenticates and grants permission

4. Authorization Server redirects to client with code:
   GET /callback?code=auth_code&state=random

5. Client exchanges code for token (backend):
   POST /oauth/token
   {
     "client_id": "xxx",
     "client_secret": "yyy",
     "code": "auth_code",
     "grant_type": "authorization_code"
   }

6. Server returns access token:
   {
     "access_token": "token...",
     "token_type": "Bearer",
     "expires_in": 3600,
     "refresh_token": "refresh..."
   }

7. Client uses token to access resources:
   GET /api/user
   Authorization: Bearer token...
```

## Deep Dive

### API Versioning Strategies
```
1. URL Path Versioning (Recommended):
   GET /api/v1/users
   GET /api/v2/users

2. Query Parameter:
   GET /api/users?version=1
   GET /api/users?version=2

3. Header:
   GET /api/users
   API-Version: 1

4. Content Negotiation:
   Accept: application/vnd.example.v1+json
   Accept: application/vnd.example.v2+json
```

### Pagination Patterns
```json
// Offset-based (simple, not ideal for large datasets)
{
  "data": [...],
  "pagination": {
    "offset": 0,
    "limit": 10,
    "total": 500
  }
}

// Cursor-based (efficient, good for large datasets)
{
  "data": [...],
  "pagination": {
    "cursor": "eyJpZCI6IDEwfQ==",
    "next_cursor": "eyJpZCI6IDIwfQ==",
    "has_more": true
  }
}

// Keyset pagination (best for sorted data)
{
  "data": [...],
  "links": {
    "next": "/api/users?after=123&before=456",
    "prev": "/api/users?after=890&before=901"
  }
}
```

### Caching Headers
```
# Cacheable by browser and intermediaries
Cache-Control: public, max-age=3600
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
Last-Modified: Wed, 15 Jan 2024 10:30:00 GMT

# Private, only browser cache
Cache-Control: private, max-age=600

# Not cacheable
Cache-Control: no-cache, no-store, must-revalidate

# Conditional request (client checks if unchanged)
If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"
If-Modified-Since: Wed, 15 Jan 2024 10:30:00 GMT
```

### Rate Limiting Headers
```
RateLimit-Limit: 1000
RateLimit-Remaining: 999
RateLimit-Reset: 1234567890
RateLimit-RetryAfter: 60

# Retry-After for 429 Too Many Requests
HTTP/1.1 429 Too Many Requests
Retry-After: 60
```

### GraphQL Basics
```graphql
query {
  user(id: 123) {
    id
    name
    email
    posts {
      id
      title
      created_at
    }
  }
}

mutation {
  createUser(input: {
    name: "John Doe"
    email: "john@example.com"
  }) {
    id
    name
    email
  }
}

subscription {
  userCreated {
    id
    name
    email
  }
}
```

### Request/Response Logging
```python
import logging
from functools import wraps
import json

logger = logging.getLogger(__name__)

def log_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(
            "API Request",
            extra={
                "method": request.method,
                "path": request.path,
                "query_params": dict(request.query_params),
                "request_id": request.headers.get("X-Request-ID"),
            }
        )

        try:
            response = func(*args, **kwargs)
            logger.info(
                "API Response",
                extra={
                    "status_code": response.status_code,
                    "request_id": request.headers.get("X-Request-ID"),
                }
            )
            return response
        except Exception as e:
            logger.error(
                "API Error",
                extra={
                    "error": str(e),
                    "request_id": request.headers.get("X-Request-ID"),
                },
                exc_info=True
            )
            raise
    return wrapper
```

## Anti-Patterns

### DON'T: Use GET for State-Changing Operations
```
# Bad - violates REST principles
GET /api/users/123/delete
GET /api/users/123/activate

# Good - use appropriate HTTP methods
DELETE /api/users/123
PATCH /api/users/123 { "status": "active" }
```

### DON'T: Mix Success and Error Codes
```json
// Bad - using 200 for error
{
  "status": 200,
  "error": "User not found",
  "data": null
}

// Good - use correct status code
HTTP/1.1 404 Not Found
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found"
  }
}
```

### DON'T: Return Large Nested Objects
```json
// Bad - too much data
{
  "id": 1,
  "name": "John",
  "company": {
    "id": 10,
    "name": "Acme",
    "employees": [...100+ objects...]
  }
}

// Good - minimal data, use links for expansion
{
  "id": 1,
  "name": "John",
  "company_id": 10,
  "_links": {
    "company": "/api/companies/10"
  }
}
```

### DON'T: Inconsistent Field Naming
```json
// Bad - inconsistent naming
{
  "user_id": 1,
  "firstName": "John",
  "last-name": "Doe",
  "email_address": "john@example.com"
}

// Good - consistent snake_case
{
  "user_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com"
}
```

### DON'T: Return Sensitive Data
```json
// Bad - exposing sensitive information
{
  "id": 1,
  "name": "John",
  "email": "john@example.com",
  "password_hash": "bcrypt...",
  "ssn": "123-45-6789",
  "api_key": "sk_live_..."
}

// Good - only return necessary public data
{
  "id": 1,
  "name": "John",
  "email": "john@example.com"
}
```

### DON'T: Ignore Security Headers
```
# Bad - missing security headers

# Good - include security headers
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Access-Control-Allow-Origin: https://trusted-domain.com
Access-Control-Allow-Credentials: true
```

### DON'T: Forget CORS Handling
```python
# Bad - allowing all origins (security risk)
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# Good - explicit origin whitelist
ALLOWED_ORIGINS = ['https://app.example.com', 'https://admin.example.com']

@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
    return response
```
