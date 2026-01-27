---
name: mock-generate
description: Generate mock data and test fixtures from schemas
disable-model-invocation: true
---

# Mock Data Generator

I'll generate realistic mock data and test fixtures based on TypeScript types, JSON schemas, database schemas, or API specifications.

**Data Sources:**
- TypeScript interfaces and types
- JSON Schema definitions
- Database schemas (Prisma, TypeORM, Drizzle)
- OpenAPI/Swagger specifications
- GraphQL schemas

**Token Optimization:**
- Uses Grep to find type definitions (150 tokens)
- Reads only schema files (600-800 tokens)
- Template-based generation (saves 600 tokens)
- Expected: 2,000-3,500 tokens total

## Phase 1: Schema Detection

```bash
#!/bin/bash
# Detect schemas for mock data generation

echo "=== Detecting Data Schemas ==="
echo ""

detect_schemas() {
    echo "Searching for schema definitions..."
    echo ""

    # TypeScript types
    TS_TYPES=$(find . -name "*.ts" -type f \
        ! -path "*/node_modules/*" \
        ! -path "*/dist/*" \
        -exec grep -l "interface\|type.*=" {} \; 2>/dev/null | head -20)

    if [ -n "$TS_TYPES" ]; then
        echo "✓ TypeScript type definitions found:"
        echo "$TS_TYPES" | sed 's/^/  /'
        echo ""
    fi

    # JSON Schemas
    JSON_SCHEMAS=$(find . -name "*.schema.json" -type f 2>/dev/null)
    if [ -n "$JSON_SCHEMAS" ]; then
        echo "✓ JSON Schema files found:"
        echo "$JSON_SCHEMAS" | sed 's/^/  /'
        echo ""
    fi

    # Prisma schema
    if [ -f "prisma/schema.prisma" ]; then
        echo "✓ Prisma schema found: prisma/schema.prisma"
        echo ""
    fi

    # OpenAPI specs
    OPENAPI_SPECS=$(find . -name "openapi*.yaml" -o -name "swagger*.json" 2>/dev/null)
    if [ -n "$OPENAPI_SPECS" ]; then
        echo "✓ OpenAPI specifications found:"
        echo "$OPENAPI_SPECS" | sed 's/^/  /'
        echo ""
    fi

    # GraphQL schemas
    GRAPHQL_SCHEMAS=$(find . -name "*.graphql" -o -name "schema.gql" 2>/dev/null)
    if [ -n "$GRAPHQL_SCHEMAS" ]; then
        echo "✓ GraphQL schemas found:"
        echo "$GRAPHQL_SCHEMAS" | sed 's/^/  /'
        echo ""
    fi
}

detect_schemas

# Check for Faker.js installation
check_faker() {
    if [ -f "package.json" ]; then
        if ! grep -q "@faker-js/faker" package.json; then
            echo "⚠️  Faker.js not installed"
            echo ""
            read -p "Install @faker-js/faker for realistic data generation? (y/n): " install
            if [ "$install" = "y" ]; then
                npm install --save-dev @faker-js/faker
                echo "✓ Faker.js installed"
            fi
        else
            echo "✓ Faker.js already installed"
        fi
    fi
}

check_faker
```

## Phase 2: Generate Mock Data from TypeScript Types

```typescript
// Generated mock data from TypeScript types
import { faker } from '@faker-js/faker';

/**
 * User interface
 */
interface User {
  id: string;
  email: string;
  name: string;
  age: number;
  role: 'admin' | 'user' | 'guest';
  isActive: boolean;
  createdAt: Date;
  profile?: UserProfile;
}

interface UserProfile {
  bio?: string;
  avatarUrl?: string;
  location?: string;
  socialLinks?: {
    twitter?: string;
    github?: string;
  };
}

/**
 * Generate a single mock user
 */
export function createMockUser(overrides?: Partial<User>): User {
  return {
    id: faker.string.uuid(),
    email: faker.internet.email(),
    name: faker.person.fullName(),
    age: faker.number.int({ min: 18, max: 80 }),
    role: faker.helpers.arrayElement(['admin', 'user', 'guest']),
    isActive: faker.datatype.boolean(),
    createdAt: faker.date.past(),
    profile: createMockUserProfile(),
    ...overrides,
  };
}

/**
 * Generate mock user profile
 */
export function createMockUserProfile(
  overrides?: Partial<UserProfile>
): UserProfile {
  return {
    bio: faker.lorem.paragraph(),
    avatarUrl: faker.image.avatar(),
    location: faker.location.city(),
    socialLinks: {
      twitter: `https://twitter.com/${faker.internet.userName()}`,
      github: `https://github.com/${faker.internet.userName()}`,
    },
    ...overrides,
  };
}

/**
 * Generate multiple mock users
 */
export function createMockUsers(count: number = 10): User[] {
  return Array.from({ length: count }, () => createMockUser());
}

/**
 * Generate users with specific characteristics
 */
export function createMockAdminUser(): User {
  return createMockUser({
    role: 'admin',
    isActive: true,
  });
}

export function createMockInactiveUser(): User {
  return createMockUser({
    isActive: false,
  });
}

/**
 * Post interface
 */
interface Post {
  id: string;
  title: string;
  content: string;
  authorId: string;
  author: User;
  tags: string[];
  published: boolean;
  viewCount: number;
  createdAt: Date;
  updatedAt: Date;
}

/**
 * Generate a single mock post
 */
export function createMockPost(overrides?: Partial<Post>): Post {
  return {
    id: faker.string.uuid(),
    title: faker.lorem.sentence(),
    content: faker.lorem.paragraphs(3),
    authorId: faker.string.uuid(),
    author: createMockUser(),
    tags: faker.helpers.arrayElements(
      ['javascript', 'typescript', 'react', 'node', 'testing'],
      { min: 1, max: 3 }
    ),
    published: faker.datatype.boolean(),
    viewCount: faker.number.int({ min: 0, max: 10000 }),
    createdAt: faker.date.past(),
    updatedAt: faker.date.recent(),
    ...overrides,
  };
}

/**
 * Generate multiple mock posts
 */
export function createMockPosts(count: number = 10): Post[] {
  return Array.from({ length: count }, () => createMockPost());
}

/**
 * API Response wrapper
 */
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
  timestamp: Date;
}

/**
 * Generate mock API response
 */
export function createMockApiResponse<T>(
  data: T,
  overrides?: Partial<ApiResponse<T>>
): ApiResponse<T> {
  return {
    data,
    status: 200,
    message: 'Success',
    timestamp: new Date(),
    ...overrides,
  };
}

/**
 * Generate mock error response
 */
export function createMockErrorResponse(
  message: string = 'An error occurred',
  status: number = 500
): ApiResponse<null> {
  return {
    data: null,
    status,
    message,
    timestamp: new Date(),
  };
}

/**
 * Paginated response
 */
interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}

/**
 * Generate mock paginated response
 */
export function createMockPaginatedResponse<T>(
  items: T[],
  page: number = 1,
  pageSize: number = 10
): PaginatedResponse<T> {
  const total = items.length;
  const start = (page - 1) * pageSize;
  const end = start + pageSize;
  const paginatedItems = items.slice(start, end);

  return {
    items: paginatedItems,
    total,
    page,
    pageSize,
    hasMore: end < total,
  };
}
```

## Phase 3: Generate Mock Data from JSON Schema

```typescript
// Generate mocks from JSON Schema
import Ajv from 'ajv';
import { faker } from '@faker-js/faker';

/**
 * JSON Schema to mock data generator
 */
export class JsonSchemaMockGenerator {
  private ajv: Ajv;

  constructor() {
    this.ajv = new Ajv();
  }

  /**
   * Generate mock data from JSON schema
   */
  generate(schema: any, count: number = 1): any[] {
    return Array.from({ length: count }, () => this.generateSingle(schema));
  }

  /**
   * Generate a single mock object from schema
   */
  private generateSingle(schema: any): any {
    if (schema.type === 'object') {
      return this.generateObject(schema);
    } else if (schema.type === 'array') {
      return this.generateArray(schema);
    } else {
      return this.generatePrimitive(schema);
    }
  }

  /**
   * Generate object from schema
   */
  private generateObject(schema: any): any {
    const obj: any = {};
    const properties = schema.properties || {};

    for (const [key, propSchema] of Object.entries(properties)) {
      // Check if property is required
      const isRequired = schema.required?.includes(key);

      if (isRequired || faker.datatype.boolean()) {
        obj[key] = this.generateSingle(propSchema);
      }
    }

    return obj;
  }

  /**
   * Generate array from schema
   */
  private generateArray(schema: any): any[] {
    const minItems = schema.minItems || 1;
    const maxItems = schema.maxItems || 5;
    const length = faker.number.int({ min: minItems, max: maxItems });

    return Array.from({ length }, () =>
      this.generateSingle(schema.items || {})
    );
  }

  /**
   * Generate primitive value from schema
   */
  private generatePrimitive(schema: any): any {
    const format = schema.format;
    const type = schema.type;

    // Handle format-specific generation
    if (format) {
      return this.generateByFormat(format, schema);
    }

    // Handle type-specific generation
    switch (type) {
      case 'string':
        if (schema.enum) {
          return faker.helpers.arrayElement(schema.enum);
        }
        return faker.lorem.word();

      case 'number':
      case 'integer':
        const min = schema.minimum || 0;
        const max = schema.maximum || 1000;
        return type === 'integer'
          ? faker.number.int({ min, max })
          : faker.number.float({ min, max, precision: 0.01 });

      case 'boolean':
        return faker.datatype.boolean();

      case 'null':
        return null;

      default:
        return null;
    }
  }

  /**
   * Generate value based on format
   */
  private generateByFormat(format: string, schema: any): any {
    switch (format) {
      case 'email':
        return faker.internet.email();
      case 'uri':
      case 'url':
        return faker.internet.url();
      case 'uuid':
        return faker.string.uuid();
      case 'date':
        return faker.date.past().toISOString().split('T')[0];
      case 'date-time':
        return faker.date.past().toISOString();
      case 'time':
        return faker.date.recent().toTimeString().split(' ')[0];
      case 'ipv4':
        return faker.internet.ipv4();
      case 'ipv6':
        return faker.internet.ipv6();
      case 'hostname':
        return faker.internet.domainName();
      default:
        return faker.lorem.word();
    }
  }
}

// Example usage
const userSchema = {
  type: 'object',
  required: ['id', 'email', 'name'],
  properties: {
    id: { type: 'string', format: 'uuid' },
    email: { type: 'string', format: 'email' },
    name: { type: 'string' },
    age: { type: 'integer', minimum: 18, maximum: 100 },
    role: { type: 'string', enum: ['admin', 'user', 'guest'] },
  },
};

const generator = new JsonSchemaMockGenerator();
const mockUsers = generator.generate(userSchema, 10);
```

## Phase 4: Generate Test Fixtures

```typescript
// Test fixtures for different test frameworks
import { faker } from '@faker-js/faker';

/**
 * Base fixture factory
 */
export abstract class FixtureFactory<T> {
  /**
   * Create a single fixture
   */
  abstract create(overrides?: Partial<T>): T;

  /**
   * Create multiple fixtures
   */
  createMany(count: number, overrides?: Partial<T>): T[] {
    return Array.from({ length: count }, () => this.create(overrides));
  }

  /**
   * Create with specific trait
   */
  createWithTrait(trait: string, overrides?: Partial<T>): T {
    const traitOverrides = this.getTraitOverrides(trait);
    return this.create({ ...traitOverrides, ...overrides });
  }

  /**
   * Get trait-specific overrides
   */
  protected getTraitOverrides(trait: string): Partial<T> {
    return {};
  }
}

/**
 * User fixture factory
 */
export class UserFixtureFactory extends FixtureFactory<User> {
  create(overrides?: Partial<User>): User {
    return {
      id: faker.string.uuid(),
      email: faker.internet.email(),
      name: faker.person.fullName(),
      age: faker.number.int({ min: 18, max: 80 }),
      role: 'user',
      isActive: true,
      createdAt: faker.date.past(),
      ...overrides,
    };
  }

  protected getTraitOverrides(trait: string): Partial<User> {
    switch (trait) {
      case 'admin':
        return { role: 'admin' };
      case 'inactive':
        return { isActive: false };
      case 'new':
        return { createdAt: faker.date.recent() };
      default:
        return {};
    }
  }
}

// Usage in tests
describe('User Service', () => {
  const userFactory = new UserFixtureFactory();

  it('should create a user', () => {
    const user = userFactory.create();
    expect(user).toHaveProperty('id');
    expect(user).toHaveProperty('email');
  });

  it('should create an admin user', () => {
    const admin = userFactory.createWithTrait('admin');
    expect(admin.role).toBe('admin');
  });

  it('should create multiple users', () => {
    const users = userFactory.createMany(5);
    expect(users).toHaveLength(5);
  });
});
```

## Phase 5: Database Seed Data

```typescript
// Database seed data generation
import { PrismaClient } from '@prisma/client';
import { faker } from '@faker-js/faker';

const prisma = new PrismaClient();

/**
 * Seed database with mock data
 */
async function seedDatabase() {
  console.log('Seeding database...');

  // Clear existing data
  await prisma.post.deleteMany();
  await prisma.user.deleteMany();

  // Create users
  const users = await Promise.all(
    Array.from({ length: 10 }, async () => {
      return prisma.user.create({
        data: {
          email: faker.internet.email(),
          name: faker.person.fullName(),
          role: faker.helpers.arrayElement(['admin', 'user', 'guest']),
        },
      });
    })
  );

  console.log(`Created ${users.length} users`);

  // Create posts
  const posts = await Promise.all(
    users.flatMap((user) =>
      Array.from({ length: 3 }, async () => {
        return prisma.post.create({
          data: {
            title: faker.lorem.sentence(),
            content: faker.lorem.paragraphs(3),
            authorId: user.id,
            published: faker.datatype.boolean(),
          },
        });
      })
    )
  );

  console.log(`Created ${posts.length} posts`);
  console.log('Seeding complete!');
}

seedDatabase()
  .catch((error) => {
    console.error('Seeding failed:', error);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

## Phase 6: Generate Mock Files

```bash
echo ""
echo "=== Generating Mock Data Files ==="
echo ""

# Create mocks directory
mkdir -p src/__mocks__
mkdir -p src/__fixtures__
mkdir -p prisma/seeds

cat > src/__mocks__/data.ts << 'EOF'
// Auto-generated mock data
// Run: npm run generate:mocks to regenerate

import { faker } from '@faker-js/faker';

// Import generated mock functions
export { createMockUser, createMockUsers } from './user.mock';
export { createMockPost, createMockPosts } from './post.mock';

/**
 * Reset faker seed for consistent mocks in tests
 */
export function resetMockSeed(seed: number = 12345) {
  faker.seed(seed);
}

/**
 * Generate complete test dataset
 */
export function generateTestDataset() {
  resetMockSeed();

  return {
    users: createMockUsers(10),
    posts: createMockPosts(30),
  };
}
EOF

echo "✓ Created src/__mocks__/data.ts"

# Add npm scripts
cat >> package.json << 'EOF'
  "scripts": {
    "generate:mocks": "ts-node scripts/generate-mocks.ts",
    "seed:db": "ts-node prisma/seeds/seed.ts"
  }
EOF

echo "✓ Added mock generation scripts"
```

## Summary

```bash
echo ""
echo "=== ✓ Mock Data Generation Complete ==="
echo ""
echo "📁 Created files:"
echo "  - src/__mocks__/data.ts         # Mock data generators"
echo "  - src/__fixtures__/             # Test fixtures"
echo "  - prisma/seeds/seed.ts          # Database seed script"
echo ""
echo "🚀 Usage:"
echo ""
echo "# In tests:"
echo "import { createMockUser } from './__mocks__/data';"
echo ""
echo "const user = createMockUser();"
echo "const users = createMockUsers(10);"
echo ""
echo "# Generate with overrides:"
echo "const admin = createMockUser({ role: 'admin' });"
echo ""
echo "# Seed database:"
echo "npm run seed:db"
echo ""
echo "💡 Integration points:"
echo "  - /test - Use mocks in test generation"
echo "  - /seed-data - Populate databases"
echo "  - /api-test-generate - Mock API responses"
```

## Best Practices

**Mock Data Quality:**
- Use realistic data from Faker.js
- Match actual data constraints
- Include edge cases
- Support deterministic generation (seeds)

**Test Fixtures:**
- Create factory functions
- Support partial overrides
- Define common traits
- Keep fixtures DRY

**Integration Points:**
- `/test` - Generate tests with mocks
- `/seed-data` - Database seeding
- `/api-test-generate` - API test mocks

## What I'll Actually Do

1. **Detect schemas** - Find type definitions
2. **Install dependencies** - Faker.js if needed
3. **Generate mock functions** - Type-safe generators
4. **Create fixtures** - Test fixture factories
5. **Database seeds** - Seed data scripts
6. **Document usage** - Examples and patterns

**Important:** I will NEVER:
- Generate invalid data for schemas
- Hardcode sensitive data
- Create non-deterministic tests without seeds
- Add AI attribution

**Credits:** Mock data patterns based on Faker.js, factory-bot patterns, test fixture best practices, and database seeding strategies from Prisma, TypeORM, and Rails communities.
