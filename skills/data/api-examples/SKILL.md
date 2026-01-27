---
name: api-examples
description: Generate API usage examples and tutorials from code analysis
disable-model-invocation: false
---

# API Examples & Tutorial Generator

I'll analyze your API and generate comprehensive usage examples, code snippets, and tutorials for developers.

Arguments: `$ARGUMENTS` - specific API focus or language (e.g., "REST", "GraphQL", "python", "javascript")

## Strategic Planning Process

<think>
Effective API examples require understanding:

1. **API Analysis**
   - What type of API? (REST, GraphQL, gRPC, WebSocket)
   - What endpoints/operations exist?
   - What's the authentication method?
   - What are common use cases?
   - What error handling is needed?

2. **Audience Consideration**
   - Who are the API consumers? (internal, external, partners)
   - What languages do they use?
   - What's their experience level?
   - What examples will be most valuable?

3. **Example Types**
   - Quick start / Getting started
   - Authentication examples
   - CRUD operation examples
   - Complex workflow examples
   - Error handling patterns
   - Best practices and anti-patterns

4. **Format & Organization**
   - Code snippets for common operations
   - Complete working examples
   - Interactive tutorials
   - SDK usage examples
   - cURL/HTTP examples for testing
</think>

## Phase 1: API Discovery

**MANDATORY FIRST STEPS:**
1. Detect API type and framework
2. Identify all endpoints/operations
3. Analyze request/response schemas
4. Detect authentication methods

Let me analyze your API:

```bash
# Detect API framework
echo "=== API Detection ==="

# Check for REST API frameworks
if grep -q "\"express\"" package.json 2>/dev/null; then
    echo "Framework: Express (Node.js REST)"
elif grep -q "\"fastapi\"" requirements.txt 2>/dev/null || grep -q "fastapi" pyproject.toml 2>/dev/null; then
    echo "Framework: FastAPI (Python REST)"
elif grep -q "\"flask\"" requirements.txt 2>/dev/null; then
    echo "Framework: Flask (Python REST)"
fi

# Check for GraphQL
if grep -q "\"graphql\"" package.json 2>/dev/null || grep -q "\"@apollo/server\"" package.json 2>/dev/null; then
    echo "Framework: GraphQL"
fi

# Check for gRPC
if grep -q "\"@grpc\"" package.json 2>/dev/null || grep -q "grpc" requirements.txt 2>/dev/null; then
    echo "Framework: gRPC"
fi

# Find API route definitions
echo ""
echo "Route files:"
find . -type f \( -name "*route*.js" -o -name "*route*.ts" -o -name "*api*.py" -o -name "*controller*.js" \) 2>/dev/null | head -10

# Check for OpenAPI/Swagger spec
if [ -f "openapi.yaml" ] || [ -f "swagger.yaml" ] || [ -f "openapi.json" ]; then
    echo ""
    echo "✓ OpenAPI specification found"
    ls -lh openapi.* swagger.* 2>/dev/null
fi
```

## Phase 2: Endpoint Analysis

I'll catalog all API endpoints and their characteristics:

**For Each Endpoint:**
- HTTP method (GET, POST, PUT, DELETE, PATCH)
- URL path and parameters
- Request body schema
- Response schema
- Authentication requirements
- Rate limiting rules
- Error responses

**Using Native Tools:**
- **Grep** to find route definitions
- **Read** API route files
- **Grep** for authentication decorators/middleware
- **Read** OpenAPI spec if available

I'll extract:
- All available endpoints
- Required vs optional parameters
- Request/response examples
- Common error scenarios
- Authentication requirements

## Phase 3: Example Generation

Based on API analysis, I'll generate examples for:

### Quick Start Example

**JavaScript/Node.js:**
```javascript
// Quick Start - API Client Setup
const API_BASE_URL = 'https://api.example.com/v1';
const API_KEY = 'your_api_key_here';

// Initialize API client
const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${API_KEY}`
};

// Example: Fetch user data
async function getUser(userId) {
  const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
    method: 'GET',
    headers: headers
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return data;
}

// Usage
getUser('123')
  .then(user => console.log('User:', user))
  .catch(error => console.error('Error:', error));
```

**Python:**
```python
# Quick Start - API Client Setup
import requests

API_BASE_URL = 'https://api.example.com/v1'
API_KEY = 'your_api_key_here'

# Initialize session
session = requests.Session()
session.headers.update({
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
})

# Example: Fetch user data
def get_user(user_id):
    response = session.get(f'{API_BASE_URL}/users/{user_id}')
    response.raise_for_status()  # Raise exception for bad status codes
    return response.json()

# Usage
try:
    user = get_user('123')
    print('User:', user)
except requests.exceptions.RequestException as e:
    print('Error:', e)
```

**cURL:**
```bash
# Quick Start - cURL Examples

# Fetch user data
curl -X GET "https://api.example.com/v1/users/123" \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json"
```

### Authentication Examples

**OAuth 2.0 Flow:**
```javascript
// OAuth 2.0 Authentication Example
const CLIENT_ID = 'your_client_id';
const CLIENT_SECRET = 'your_client_secret';
const REDIRECT_URI = 'https://yourapp.com/callback';

// Step 1: Get authorization URL
function getAuthorizationUrl() {
  const params = new URLSearchParams({
    client_id: CLIENT_ID,
    redirect_uri: REDIRECT_URI,
    response_type: 'code',
    scope: 'read write'
  });
  return `https://api.example.com/oauth/authorize?${params}`;
}

// Step 2: Exchange code for access token
async function getAccessToken(code) {
  const response = await fetch('https://api.example.com/oauth/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      code: code,
      redirect_uri: REDIRECT_URI,
      grant_type: 'authorization_code'
    })
  });

  const data = await response.json();
  return data.access_token;
}

// Step 3: Use access token for API calls
async function makeAuthenticatedRequest(accessToken) {
  const response = await fetch('https://api.example.com/v1/user', {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  return response.json();
}
```

### CRUD Operation Examples

**Complete CRUD Example:**
```javascript
// CRUD Operations Example

class UserAPI {
  constructor(baseUrl, apiKey) {
    this.baseUrl = baseUrl;
    this.headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    };
  }

  // CREATE - Create a new user
  async createUser(userData) {
    const response = await fetch(`${this.baseUrl}/users`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(userData)
    });
    return response.json();
  }

  // READ - Get user by ID
  async getUser(userId) {
    const response = await fetch(`${this.baseUrl}/users/${userId}`, {
      method: 'GET',
      headers: this.headers
    });
    return response.json();
  }

  // READ - List all users with pagination
  async listUsers(page = 1, limit = 10) {
    const params = new URLSearchParams({ page, limit });
    const response = await fetch(`${this.baseUrl}/users?${params}`, {
      method: 'GET',
      headers: this.headers
    });
    return response.json();
  }

  // UPDATE - Update user
  async updateUser(userId, updates) {
    const response = await fetch(`${this.baseUrl}/users/${userId}`, {
      method: 'PUT',
      headers: this.headers,
      body: JSON.stringify(updates)
    });
    return response.json();
  }

  // DELETE - Delete user
  async deleteUser(userId) {
    const response = await fetch(`${this.baseUrl}/users/${userId}`, {
      method: 'DELETE',
      headers: this.headers
    });
    return response.ok;
  }
}

// Usage Example
const api = new UserAPI('https://api.example.com/v1', 'your_api_key');

// Create user
const newUser = await api.createUser({
  name: 'John Doe',
  email: 'john@example.com'
});
console.log('Created:', newUser);

// Get user
const user = await api.getUser(newUser.id);
console.log('Retrieved:', user);

// Update user
const updated = await api.updateUser(newUser.id, {
  name: 'Jane Doe'
});
console.log('Updated:', updated);

// List users
const users = await api.listUsers(1, 10);
console.log('Users:', users);

// Delete user
const deleted = await api.deleteUser(newUser.id);
console.log('Deleted:', deleted);
```

### Error Handling Examples

**Comprehensive Error Handling:**
```javascript
// Error Handling Best Practices

class APIError extends Error {
  constructor(message, statusCode, response) {
    super(message);
    this.statusCode = statusCode;
    this.response = response;
    this.name = 'APIError';
  }
}

async function makeAPIRequest(url, options) {
  try {
    const response = await fetch(url, options);

    // Handle different error status codes
    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));

      switch (response.status) {
        case 400:
          throw new APIError(
            'Bad Request: ' + (errorBody.message || 'Invalid parameters'),
            400,
            errorBody
          );
        case 401:
          throw new APIError(
            'Unauthorized: Invalid or expired token',
            401,
            errorBody
          );
        case 403:
          throw new APIError(
            'Forbidden: Insufficient permissions',
            403,
            errorBody
          );
        case 404:
          throw new APIError(
            'Not Found: Resource does not exist',
            404,
            errorBody
          );
        case 429:
          throw new APIError(
            'Rate Limit Exceeded: Too many requests',
            429,
            errorBody
          );
        case 500:
          throw new APIError(
            'Internal Server Error: Please try again later',
            500,
            errorBody
          );
        default:
          throw new APIError(
            `HTTP Error ${response.status}`,
            response.status,
            errorBody
          );
      }
    }

    return response.json();
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    // Network errors, timeout, etc.
    throw new APIError(
      'Network Error: ' + error.message,
      0,
      null
    );
  }
}

// Usage with error handling
async function getUserSafely(userId) {
  try {
    const user = await makeAPIRequest(
      `https://api.example.com/v1/users/${userId}`,
      {
        method: 'GET',
        headers: { 'Authorization': 'Bearer token' }
      }
    );
    return user;
  } catch (error) {
    if (error instanceof APIError) {
      switch (error.statusCode) {
        case 401:
          // Redirect to login
          console.log('Please log in again');
          break;
        case 404:
          // User not found
          console.log('User not found');
          return null;
        case 429:
          // Retry with backoff
          console.log('Rate limited, retrying...');
          await new Promise(r => setTimeout(r, 5000));
          return getUserSafely(userId);
        default:
          console.error('API Error:', error.message);
      }
    } else {
      console.error('Unexpected error:', error);
    }
    throw error;
  }
}
```

### GraphQL Examples

**GraphQL Query & Mutation Examples:**
```javascript
// GraphQL API Examples

const GRAPHQL_ENDPOINT = 'https://api.example.com/graphql';

// Helper function for GraphQL requests
async function graphqlRequest(query, variables = {}) {
  const response = await fetch(GRAPHQL_ENDPOINT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer your_token_here'
    },
    body: JSON.stringify({
      query,
      variables
    })
  });

  const result = await response.json();

  if (result.errors) {
    throw new Error(result.errors[0].message);
  }

  return result.data;
}

// Query Example: Fetch user with posts
const GET_USER_QUERY = `
  query GetUser($userId: ID!) {
    user(id: $userId) {
      id
      name
      email
      posts {
        id
        title
        content
        createdAt
      }
    }
  }
`;

async function getUser(userId) {
  const data = await graphqlRequest(GET_USER_QUERY, { userId });
  return data.user;
}

// Mutation Example: Create post
const CREATE_POST_MUTATION = `
  mutation CreatePost($input: CreatePostInput!) {
    createPost(input: $input) {
      id
      title
      content
      author {
        id
        name
      }
    }
  }
`;

async function createPost(title, content, authorId) {
  const data = await graphqlRequest(CREATE_POST_MUTATION, {
    input: { title, content, authorId }
  });
  return data.createPost;
}

// Usage
const user = await getUser('123');
console.log('User:', user);

const post = await createPost('My Post', 'Content here', '123');
console.log('Created post:', post);
```

### SDK Usage Examples

**TypeScript SDK Example:**
```typescript
// TypeScript SDK Usage

import { ApiClient, User, CreateUserRequest } from '@example/api-sdk';

// Initialize client
const client = new ApiClient({
  apiKey: 'your_api_key',
  baseUrl: 'https://api.example.com/v1'
});

// Type-safe API calls
async function exampleUsage() {
  try {
    // Create user with full type safety
    const newUser: CreateUserRequest = {
      name: 'John Doe',
      email: 'john@example.com',
      role: 'admin'
    };

    const createdUser: User = await client.users.create(newUser);
    console.log('Created user:', createdUser.id);

    // Fetch user with autocomplete
    const user: User = await client.users.get(createdUser.id);
    console.log('User details:', user);

    // List users with pagination
    const users = await client.users.list({
      page: 1,
      limit: 10,
      filter: { role: 'admin' }
    });
    console.log('Found', users.total, 'users');

    // Update user
    const updated: User = await client.users.update(user.id, {
      name: 'Jane Doe'
    });

    // Delete user
    await client.users.delete(user.id);
  } catch (error) {
    if (error instanceof ApiClient.ValidationError) {
      console.error('Validation failed:', error.fields);
    } else if (error instanceof ApiClient.AuthenticationError) {
      console.error('Authentication required');
    } else {
      console.error('API error:', error);
    }
  }
}
```

## Phase 4: Tutorial Generation

I'll create complete tutorials for common workflows:

**Tutorial Structure:**
1. **Introduction**: What the tutorial covers
2. **Prerequisites**: Required setup and credentials
3. **Step-by-step guide**: Detailed instructions with code
4. **Expected output**: What success looks like
5. **Troubleshooting**: Common issues and solutions
6. **Next steps**: Advanced topics to explore

**Example Tutorial Topics:**
- Getting started with the API
- Authentication and authorization
- Implementing pagination
- File upload and download
- Webhooks integration
- Real-time updates with WebSockets
- Batch operations and bulk updates
- Advanced filtering and search

## Token Optimization Strategy

**Efficient Generation:**
- Generate examples for most common endpoints first
- Focus on requested language/framework
- Provide template examples that can be adapted
- Reference API documentation instead of repeating specs
- Group similar examples together

**Targeted Output:**
- Ask for specific use case if unclear
- Skip languages not relevant to user
- Provide quick start before comprehensive examples
- Link to full documentation for edge cases

## Integration Points

**Synergistic Skills:**
- `/api-docs-generate` - Generate OpenAPI/Swagger docs first
- `/api-test-generate` - Generate tests alongside examples
- `/docs` - Add examples to project documentation
- `/types-generate` - Generate TypeScript types for examples

Suggests `/api-docs-generate` when:
- No OpenAPI spec exists
- Need formal API documentation
- Want interactive API explorer

Suggests `/types-generate` when:
- TypeScript project detected
- Need type-safe API client
- SDK generation needed

## Output Files Created

I'll create organized example files:

**Directory Structure:**
```
docs/api-examples/
├── README.md                    # Overview and quick start
├── authentication.md            # Auth examples
├── getting-started.md          # Quick start guide
├── crud-operations.md          # Basic CRUD examples
├── advanced-examples.md        # Complex workflows
├── error-handling.md           # Error handling patterns
├── code-snippets/
│   ├── javascript/
│   │   ├── basic-example.js
│   │   ├── auth-example.js
│   │   └── complete-client.js
│   ├── python/
│   │   ├── basic_example.py
│   │   ├── auth_example.py
│   │   └── complete_client.py
│   ├── typescript/
│   │   └── sdk-usage.ts
│   └── curl/
│       └── examples.sh
└── tutorials/
    ├── tutorial-1-getting-started.md
    ├── tutorial-2-authentication.md
    └── tutorial-3-advanced-usage.md
```

## Safety Mechanisms

**Protection Measures:**
- Never include real API keys in examples
- Use placeholder credentials clearly marked
- Create examples in `docs/api-examples/` directory
- Non-destructive (only creates documentation)
- Validate code syntax before output

**Security Best Practices:**
- Show environment variable usage for secrets
- Demonstrate secure credential storage
- Include rate limiting examples
- Show proper error handling
- Warn about common security pitfalls

## Important Notes

**I will NEVER:**
- Include real API keys, tokens, or credentials
- Add AI attribution to example code
- Generate examples without analyzing actual API
- Create insecure authentication examples
- Expose sensitive endpoint information

**Best Practices:**
- Keep examples simple and focused
- Include error handling in all examples
- Show both success and error cases
- Provide working, tested code
- Document prerequisites clearly

## Credits

**Inspired by:**
- [Stripe API Documentation](https://stripe.com/docs/api) - Excellent API examples
- [Twilio API Docs](https://www.twilio.com/docs) - Comprehensive tutorials
- [GitHub REST API Docs](https://docs.github.com/en/rest) - Clear code examples
- API documentation best practices
- Developer experience research

This skill helps you create comprehensive API documentation with working examples that developers can actually use.
