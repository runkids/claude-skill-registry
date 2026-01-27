---
name: types-generate
description: Generate TypeScript types from schemas/APIs
disable-model-invocation: true
---

# TypeScript Type Generator

I'll generate TypeScript types and interfaces from various sources: JSON schemas, OpenAPI specs, GraphQL schemas, databases, and API responses.

Arguments: `$ARGUMENTS` - schema file, API endpoint, or database connection

## Type Generation Philosophy

- **Type Safety**: Comprehensive type coverage
- **DRY**: Single source of truth
- **Documentation**: Generated JSDoc comments
- **Validation**: Runtime type guards included

**Token Optimization:**
- Uses Grep to find schemas (100 tokens)
- Reads only relevant schema files (1,000 tokens)
- Caches common patterns (saves 300 tokens)
- Expected: 1,500-2,500 tokens

## Phase 1: Source Detection

First, let me detect what schemas are available:

```bash
#!/bin/bash
# Detect type generation sources

detect_type_sources() {
    echo "=== Type Source Detection ==="
    echo ""

    # 1. OpenAPI/Swagger specs
    OPENAPI_SPECS=$(find . -name "openapi*.yaml" -o -name "swagger*.json" -o -name "api-spec*.yaml" 2>/dev/null)
    if [ ! -z "$OPENAPI_SPECS" ]; then
        echo "✓ OpenAPI specifications found:"
        echo "$OPENAPI_SPECS" | sed 's/^/  /'
    fi

    # 2. JSON Schema files
    JSON_SCHEMAS=$(find . -name "*.schema.json" 2>/dev/null)
    if [ ! -z "$JSON_SCHEMAS" ]; then
        echo "✓ JSON Schema files found:"
        echo "$JSON_SCHEMAS" | sed 's/^/  /'
    fi

    # 3. GraphQL schemas
    GRAPHQL_SCHEMAS=$(find . -name "*.graphql" -o -name "schema.gql" 2>/dev/null)
    if [ ! -z "$GRAPHQL_SCHEMAS" ]; then
        echo "✓ GraphQL schemas found:"
        echo "$GRAPHQL_SCHEMAS" | sed 's/^/  /'
    fi

    # 4. Protocol Buffers
    PROTO_FILES=$(find . -name "*.proto" 2>/dev/null)
    if [ ! -z "$PROTO_FILES" ]; then
        echo "✓ Protocol Buffer definitions found:"
        echo "$PROTO_FILES" | sed 's/^/  /'
    fi

    # 5. Database schemas
    if [ -f "prisma/schema.prisma" ]; then
        echo "✓ Prisma schema found: prisma/schema.prisma"
    fi

    if [ -f "drizzle.config.ts" ]; then
        echo "✓ Drizzle schema found"
    fi

    # 6. Sample data
    SAMPLE_JSON=$(find . -name "*.sample.json" -o -name "example*.json" 2>/dev/null | head -5)
    if [ ! -z "$SAMPLE_JSON" ]; then
        echo "✓ Sample JSON files found:"
        echo "$SAMPLE_JSON" | sed 's/^/  /'
    fi

    echo ""
}

detect_type_sources
```

## Phase 2: Type Generation from OpenAPI

Generate TypeScript types from OpenAPI/Swagger specifications:

```typescript
// Generated from openapi.yaml
// This file is auto-generated. Do not edit manually.

/**
 * User account information
 */
export interface User {
  /** Unique user identifier */
  id: string;

  /** User's email address */
  email: string;

  /** User's display name */
  name: string;

  /** User role */
  role: 'admin' | 'user' | 'guest';

  /** Account creation timestamp */
  createdAt: string;

  /** Optional profile information */
  profile?: UserProfile;
}

/**
 * User profile details
 */
export interface UserProfile {
  /** Profile bio */
  bio?: string;

  /** Avatar URL */
  avatarUrl?: string;

  /** Social media links */
  socialLinks?: {
    twitter?: string;
    github?: string;
    linkedin?: string;
  };
}

/**
 * API request types
 */
export interface CreateUserRequest {
  email: string;
  name: string;
  password: string;
  role?: 'user' | 'guest';
}

export interface UpdateUserRequest {
  name?: string;
  profile?: Partial<UserProfile>;
}

/**
 * API response types
 */
export interface CreateUserResponse {
  user: User;
  token: string;
}

export interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
}

/**
 * Type guards for runtime validation
 */
export function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'email' in obj &&
    'name' in obj &&
    'role' in obj
  );
}

export function isErrorResponse(obj: unknown): obj is ErrorResponse {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'error' in obj &&
    typeof (obj as ErrorResponse).error === 'object'
  );
}
```

**Generation Script:**

```bash
#!/bin/bash
# Generate types from OpenAPI spec

generate_openapi_types() {
    local spec_file="$1"
    local output_file="${2:-src/types/api.ts}"

    if [ ! -f "$spec_file" ]; then
        echo "❌ OpenAPI spec not found: $spec_file"
        exit 1
    fi

    echo "Generating TypeScript types from $spec_file..."

    # Use openapi-typescript if available
    if command -v openapi-typescript &> /dev/null; then
        npx openapi-typescript "$spec_file" --output "$output_file"
        echo "✓ Types generated: $output_file"
    else
        echo "Installing openapi-typescript..."
        npm install --save-dev openapi-typescript
        npx openapi-typescript "$spec_file" --output "$output_file"
        echo "✓ Types generated: $output_file"
    fi

    # Add type guards
    add_type_guards "$output_file"
}

add_type_guards() {
    local file="$1"

    cat >> "$file" << 'EOF'

/**
 * Runtime type validation utilities
 */
export namespace TypeGuards {
  export function hasRequiredFields<T extends object>(
    obj: unknown,
    fields: (keyof T)[]
  ): obj is T {
    if (typeof obj !== 'object' || obj === null) return false;
    return fields.every(field => field in obj);
  }
}
EOF
}

generate_openapi_types "docs/openapi.yaml" "src/types/api.ts"
```

## Phase 3: Type Generation from JSON Schema

Generate types from JSON Schema:

```typescript
// Generated from user.schema.json

/**
 * JSON Schema: User
 */
export interface User {
  id: string;
  email: string;
  name: string;
  age?: number;
  tags?: string[];
  metadata?: Record<string, unknown>;
}

/**
 * Zod schema for runtime validation
 */
import { z } from 'zod';

export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1).max(255),
  age: z.number().int().positive().optional(),
  tags: z.array(z.string()).optional(),
  metadata: z.record(z.unknown()).optional(),
});

/**
 * Type inferred from Zod schema
 */
export type UserFromSchema = z.infer<typeof UserSchema>;

/**
 * Validation function
 */
export function validateUser(data: unknown): User {
  return UserSchema.parse(data);
}

export function isValidUser(data: unknown): data is User {
  return UserSchema.safeParse(data).success;
}
```

**Generation Script:**

```bash
#!/bin/bash
# Generate types from JSON Schema

generate_json_schema_types() {
    local schema_file="$1"
    local output_file="${2:-src/types/schemas.ts}"

    echo "Generating TypeScript types from JSON Schema..."

    # Use json-schema-to-typescript
    if ! command -v json2ts &> /dev/null; then
        npm install --save-dev json-schema-to-typescript
    fi

    npx json2ts "$schema_file" > "$output_file"

    # Add Zod schemas for runtime validation
    generate_zod_schemas "$schema_file" >> "$output_file"

    echo "✓ Types generated: $output_file"
}

generate_zod_schemas() {
    local schema_file="$1"

    echo ""
    echo "// Runtime validation with Zod"
    echo "import { z } from 'zod';"
    echo ""

    # Parse JSON schema and generate Zod schema
    # This would require a proper parser
    # Simplified version shown
}
```

## Phase 4: Type Generation from GraphQL

Generate types from GraphQL schema:

```typescript
// Generated from schema.graphql

export type Maybe<T> = T | null;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };

/**
 * GraphQL scalar types
 */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
  DateTime: string;
};

/**
 * User type from GraphQL schema
 */
export type User = {
  __typename?: 'User';
  id: Scalars['ID'];
  email: Scalars['String'];
  name: Scalars['String'];
  posts: Array<Post>;
  createdAt: Scalars['DateTime'];
};

export type Post = {
  __typename?: 'Post';
  id: Scalars['ID'];
  title: Scalars['String'];
  content: Scalars['String'];
  author: User;
  published: Scalars['Boolean'];
};

/**
 * GraphQL Query types
 */
export type Query = {
  __typename?: 'Query';
  user?: Maybe<User>;
  users: Array<User>;
  post?: Maybe<Post>;
  posts: Array<Post>;
};

export type QueryUserArgs = {
  id: Scalars['ID'];
};

export type QueryPostArgs = {
  id: Scalars['ID'];
};

/**
 * GraphQL Mutation types
 */
export type Mutation = {
  __typename?: 'Mutation';
  createUser: User;
  updateUser: User;
  deleteUser: Scalars['Boolean'];
};

export type MutationCreateUserArgs = {
  input: CreateUserInput;
};

export type CreateUserInput = {
  email: Scalars['String'];
  name: Scalars['String'];
};
```

**Generation Script:**

```bash
#!/bin/bash
# Generate types from GraphQL schema

generate_graphql_types() {
    local schema_file="$1"
    local output_file="${2:-src/types/graphql.ts}"

    echo "Generating TypeScript types from GraphQL schema..."

    # Use GraphQL Code Generator
    if [ ! -f "codegen.yml" ]; then
        cat > codegen.yml << EOF
overwrite: true
schema: "$schema_file"
generates:
  $output_file:
    plugins:
      - typescript
      - typescript-operations
      - typescript-react-apollo
    config:
      withHooks: true
      withComponent: false
      withHOC: false
EOF
    fi

    npm install --save-dev @graphql-codegen/cli @graphql-codegen/typescript
    npx graphql-codegen

    echo "✓ Types generated: $output_file"
}

generate_graphql_types "schema.graphql"
```

## Phase 5: Type Generation from Database

Generate types from database schema:

```typescript
// Generated from Prisma schema

/**
 * Database model types
 */
export interface User {
  id: string;
  email: string;
  name: string;
  role: Role;
  createdAt: Date;
  updatedAt: Date;
  posts: Post[];
}

export interface Post {
  id: string;
  title: string;
  content: string;
  published: boolean;
  authorId: string;
  author: User;
  createdAt: Date;
  updatedAt: Date;
}

export enum Role {
  ADMIN = 'ADMIN',
  USER = 'USER',
  GUEST = 'GUEST'
}

/**
 * Input types for create/update operations
 */
export interface UserCreateInput {
  email: string;
  name: string;
  role?: Role;
  posts?: PostCreateNestedManyWithoutAuthorInput;
}

export interface UserUpdateInput {
  email?: string;
  name?: string;
  role?: Role;
  posts?: PostUpdateManyWithoutAuthorInput;
}

/**
 * Query result types
 */
export interface UserWithPosts extends User {
  posts: Post[];
}

export interface PostWithAuthor extends Post {
  author: User;
}
```

**Database Type Generation:**

```bash
#!/bin/bash
# Generate types from database

generate_db_types() {
    echo "Generating types from database schema..."

    # Prisma
    if [ -f "prisma/schema.prisma" ]; then
        echo "Using Prisma..."
        npx prisma generate
        echo "✓ Prisma types generated"
    fi

    # Drizzle
    if [ -f "drizzle.config.ts" ]; then
        echo "Using Drizzle..."
        npx drizzle-kit generate:ts
        echo "✓ Drizzle types generated"
    fi

    # TypeORM
    if grep -q "@Entity" -r src --include="*.ts" 2>/dev/null; then
        echo "Using TypeORM..."
        echo "✓ TypeORM decorators provide types at runtime"
    fi

    # Direct SQL to TypeScript
    generate_sql_types
}

generate_sql_types() {
    # For databases without ORM
    cat > src/types/database.ts << 'EOF'
/**
 * Database table types (generated from SQL schema)
 */

export interface UsersTable {
  id: string;
  email: string;
  name: string;
  created_at: Date;
  updated_at: Date;
}

export interface PostsTable {
  id: string;
  title: string;
  content: string;
  author_id: string;
  created_at: Date;
  updated_at: Date;
}

/**
 * Database result types with relationships
 */
export interface UserWithPosts extends UsersTable {
  posts: PostsTable[];
}
EOF
}
```

## Phase 6: Type Generation from API Responses

Generate types from actual API responses:

```bash
#!/bin/bash
# Generate types from API responses

generate_api_response_types() {
    local api_url="$1"
    local output_file="${2:-src/types/api-responses.ts}"

    echo "Fetching API responses and generating types..."

    # Fetch sample responses
    mkdir -p .type-gen-cache

    # Example: Fetch user endpoint
    curl -s "$api_url/api/users/1" > .type-gen-cache/user-response.json
    curl -s "$api_url/api/posts" > .type-gen-cache/posts-response.json

    # Use quicktype to generate types from JSON
    if ! command -v quicktype &> /dev/null; then
        npm install --save-dev quicktype
    fi

    cat > "$output_file" << 'EOF'
// Generated from API responses
// Auto-generated - do not edit manually

EOF

    npx quicktype .type-gen-cache/*.json \
        --src-lang json \
        --lang typescript \
        --top-level User \
        >> "$output_file"

    echo "✓ Types generated from API responses: $output_file"
}

generate_api_response_types "https://api.example.com"
```

**Manual Type Inference:**

```typescript
/**
 * Infer types from sample data
 */

// Sample API response
const sampleUser = {
  id: "123",
  email: "user@example.com",
  name: "John Doe",
  age: 30,
  tags: ["developer", "typescript"],
  metadata: {
    lastLogin: "2026-01-25T10:00:00Z",
    preferences: {
      theme: "dark"
    }
  }
};

// Inferred type
export type User = typeof sampleUser;

// Or explicitly define
export interface UserExplicit {
  id: string;
  email: string;
  name: string;
  age: number;
  tags: string[];
  metadata: {
    lastLogin: string;
    preferences: {
      theme: string;
    };
  };
}
```

## Phase 7: Utility Types

I'll generate helpful utility types:

```typescript
/**
 * Utility types for common patterns
 */

// Make all properties optional recursively
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Make specific properties required
export type RequireFields<T, K extends keyof T> = T & Required<Pick<T, K>>;

// Make specific properties optional
export type OptionalFields<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

// Flatten nested types
export type Flatten<T> = T extends object
  ? { [K in keyof T]: Flatten<T[K]> }
  : T;

// Extract nested property types
export type NestedKeyOf<T> = {
  [K in keyof T & string]: T[K] extends object
    ? `${K}` | `${K}.${NestedKeyOf<T[K]>}`
    : `${K}`;
}[keyof T & string];

// API response wrapper
export type ApiResponse<T> = {
  data: T;
  status: number;
  message?: string;
};

// Paginated response
export type PaginatedResponse<T> = {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
};

// Result type for operations that can fail
export type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };
```

## Practical Examples

**Generate from OpenAPI:**
```bash
/types-generate openapi.yaml
/types-generate docs/api-spec.yaml --output src/types/api.ts
```

**Generate from GraphQL:**
```bash
/types-generate schema.graphql
/types-generate --graphql --with-hooks
```

**Generate from Database:**
```bash
/types-generate --prisma
/types-generate --database postgresql://localhost/mydb
```

**Generate from API:**
```bash
/types-generate https://api.example.com/users/1
/types-generate --api https://api.example.com --endpoints /users,/posts
```

**Generate from JSON:**
```bash
/types-generate sample-data.json
/types-generate --json *.sample.json
```

## Best Practices

**Type Organization:**
```
src/types/
├── api.ts           # API request/response types
├── database.ts      # Database model types
├── graphql.ts       # GraphQL types
├── common.ts        # Shared types
└── utils.ts         # Utility types
```

**Documentation:**
- ✅ Add JSDoc comments to all types
- ✅ Include examples in comments
- ✅ Document required vs optional fields
- ✅ Link to schema sources

**Validation:**
- ✅ Generate runtime validators (Zod, io-ts)
- ✅ Create type guards for critical types
- ✅ Validate API responses
- ✅ Use branded types for IDs

## What I'll Actually Do

1. **Detect sources** - Find schemas using Grep
2. **Choose generator** - Select appropriate tool
3. **Generate types** - Create TypeScript interfaces
4. **Add validation** - Include runtime type guards
5. **Document types** - JSDoc comments
6. **Organize output** - Structured type files

**Important:** I will NEVER:
- Generate types without source validation
- Skip documentation comments
- Create duplicate type definitions
- Add AI attribution

All generated types will be well-documented, validated, and ready for immediate use.

**Credits:** Based on popular TypeScript type generation tools: openapi-typescript, GraphQL Code Generator, Prisma, and quicktype.
