---
name: database-migration
description: Use when working with Supabase database schemas, migrations, RLS policies, or PostGIS features. Enforces UUID standards, timestamp columns, and security best practices.
---

# Database Migration Skill

Use this skill when working with Supabase database schemas, migrations, RLS policies, or PostGIS features.

## Critical Rules

### Never Use Service Role Keys in Client Code

**❌ DANGEROUS:**
```typescript
// NEVER expose service role keys in apps/mobile or apps/web
const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);
```

**✅ SAFE:**
```typescript
// Client apps ONLY use anonymous keys
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
```

Service role keys bypass RLS - only use in:
- Backend services
- Admin tools (apps/admin with proper auth)
- Database migrations
- Edge functions

### RLS Must Be Enabled by Default

**Every table MUST have RLS enabled:**

```sql
-- ✅ REQUIRED pattern
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- CRITICAL: Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own profile"
  ON users FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON users FOR UPDATE
  USING (auth.uid() = id);
```

### Standard Table Structure

Every table should follow this pattern:

```sql
CREATE TABLE table_name (
  -- Primary key: UUID
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Your columns here
  name TEXT NOT NULL,
  description TEXT,

  -- Audit columns (REQUIRED)
  created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- RLS (REQUIRED)
ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

-- Updated_at trigger (RECOMMENDED)
CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON table_name
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

## Migration Workflow

### Using MCP Supabase Tools

The monorepo has Supabase MCP tools available:

```typescript
// Check existing tables
mcp__supabase__list_tables({ schemas: ['public'] })

// Execute DDL (schema changes)
mcp__supabase__apply_migration({
  name: 'create_posts_table',
  query: 'CREATE TABLE posts (...)'
})

// Execute queries (data operations)
mcp__supabase__execute_sql({
  query: 'SELECT * FROM users WHERE id = $1'
})

// Get security advisors
mcp__supabase__get_advisors({ type: 'security' })
```

### Migration File Organization

**IMPORTANT**: Migrations are organized by type in folders for better maintainability:

```
supabase/migrations/
├── tables/
│   ├── 20240101120000_create_users.sql
│   ├── 20240101120100_create_profiles.sql
│   ├── 20240102120000_create_pets.sql
│   └── 20240103120000_create_posts.sql
├── views/
│   ├── 20240104120000_create_user_stats_view.sql
│   └── 20240105120000_create_pet_nearby_view.sql
├── functions/
│   ├── 20240106120000_create_update_timestamp_function.sql
│   ├── 20240107120000_create_calculate_distance_function.sql
│   └── 20240108120000_create_search_pets_function.sql
├── triggers/
│   ├── 20240109120000_add_update_timestamp_trigger_users.sql
│   └── 20240110120000_add_update_timestamp_trigger_pets.sql
├── policies/
│   ├── 20240111120000_add_rls_policies_users.sql
│   ├── 20240112120000_add_rls_policies_profiles.sql
│   └── 20240113120000_add_rls_policies_pets.sql
└── indexes/
    ├── 20240114120000_add_users_email_index.sql
    └── 20240115120000_add_pets_location_gist_index.sql
```

### Migration Organization Rules

1. **Folder Structure**:
   - `tables/` - CREATE TABLE statements, ALTER TABLE for columns
   - `views/` - CREATE VIEW, CREATE MATERIALIZED VIEW
   - `functions/` - CREATE FUNCTION, CREATE OR REPLACE FUNCTION
   - `triggers/` - CREATE TRIGGER statements
   - `policies/` - RLS policies (ALTER TABLE ... ENABLE RLS, CREATE POLICY)
   - `indexes/` - CREATE INDEX statements

2. **File Placement Logic**:
   ```
   - Creating a new table? → tables/
   - Adding RLS policies? → policies/
   - Creating helper function? → functions/
   - Adding trigger to call function? → triggers/
   - Creating spatial index? → indexes/
   - Creating view for queries? → views/
   ```

3. **Cross-Folder Dependencies**:
   - Tables must be created before policies
   - Functions must be created before triggers
   - Tables must exist before views that reference them
   - Use timestamps to enforce order across folders

4. **Example Workflow**:
   ```
   1. tables/20240101_create_users.sql
      - Create users table
      - Enable RLS (basic)

   2. functions/20240102_update_timestamp.sql
      - Create update_updated_at_column() function

   3. triggers/20240103_users_timestamp_trigger.sql
      - Add trigger to users table

   4. policies/20240104_users_rls.sql
      - Add comprehensive RLS policies to users

   5. indexes/20240105_users_email_index.sql
      - Add performance indexes

   6. views/20240106_user_stats.sql
      - Create views that depend on users table
   ```

### Migration Naming Convention

Use timestamp + descriptive name:

```
YYYYMMDDHHMMSS_description.sql

Examples:
tables/20240315120000_create_users.sql
policies/20240315120100_add_rls_users.sql
functions/20240315120200_create_distance_calc.sql
triggers/20240315120300_add_timestamp_trigger_users.sql
indexes/20240315120400_add_users_email_index.sql
views/20240315120500_create_user_stats_view.sql
```

### When to Create a New Migration

**Create separate migration files for**:
- Each new table
- Each new function
- Each set of RLS policies for a table
- Each new view
- Each new trigger
- Each new index or set of related indexes

**Combine into single file**:
- Multiple indexes for the same table (if added at once)
- Related RLS policies for the same table
- Helper functions that work together

## RLS Policy Patterns

### User-Owned Resources

```sql
-- Users can only see/modify their own data
CREATE POLICY "Users manage own data"
  ON user_profiles
  FOR ALL
  USING (auth.uid() = user_id);
```

### Public Read, Authenticated Write

```sql
-- Anyone can read, authenticated users can write
CREATE POLICY "Public read access"
  ON posts
  FOR SELECT
  USING (true);

CREATE POLICY "Authenticated write access"
  ON posts
  FOR INSERT
  WITH CHECK (auth.role() = 'authenticated');
```

### Role-Based Access

```sql
-- Admin-only access
CREATE POLICY "Admin full access"
  ON sensitive_data
  FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_id = auth.uid()
      AND role = 'admin'
    )
  );
```

### Tenant Isolation

```sql
-- Multi-tenant data isolation
CREATE POLICY "Tenant isolation"
  ON tenant_data
  FOR ALL
  USING (
    tenant_id IN (
      SELECT tenant_id FROM user_tenants
      WHERE user_id = auth.uid()
    )
  );
```

## PostGIS Integration

For location-based features (pet finding, maps):

```sql
-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Add location column
ALTER TABLE pets
ADD COLUMN location GEOGRAPHY(POINT, 4326);

-- Spatial index for performance
CREATE INDEX pets_location_idx
  ON pets
  USING GIST(location);

-- Find pets within radius (in meters)
SELECT *
FROM pets
WHERE ST_DWithin(
  location,
  ST_MakePoint(longitude, latitude)::geography,
  5000  -- 5km radius
);
```

## Foreign Key Relationships

Always use proper foreign keys with cascade rules:

```sql
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Index foreign keys for performance
CREATE INDEX posts_user_id_idx ON posts(user_id);
```

## Common Functions

### Updated At Trigger

Create once, reuse everywhere:

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to any table
CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON table_name
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

### Generate Slug

```sql
CREATE OR REPLACE FUNCTION generate_slug(text_input TEXT)
RETURNS TEXT AS $$
BEGIN
  RETURN lower(
    regexp_replace(
      regexp_replace(text_input, '[^a-zA-Z0-9\s-]', '', 'g'),
      '\s+', '-', 'g'
    )
  );
END;
$$ LANGUAGE plpgsql IMMUTABLE;
```

## Type Generation

After migrations, regenerate TypeScript types:

```bash
# Using MCP tool
mcp__supabase__generate_typescript_types()

# Or via CLI (if configured)
pnpm --filter @hounii/api gen:types
```

Update types in `packages/api/src/types/database.ts`.

## Migration Checklist

Before applying a migration:

- [ ] **Table Structure**
  - [ ] UUID primary key with `gen_random_uuid()`
  - [ ] `created_at` and `updated_at` columns
  - [ ] Proper column types and constraints
  - [ ] Foreign keys with cascade rules

- [ ] **Security**
  - [ ] RLS enabled: `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`
  - [ ] Policies defined for all operations (SELECT, INSERT, UPDATE, DELETE)
  - [ ] Policies tested for edge cases
  - [ ] No service role keys in client code

- [ ] **Performance**
  - [ ] Indexes on foreign keys
  - [ ] Indexes on frequently queried columns
  - [ ] GiST indexes for PostGIS columns

- [ ] **Functions & Triggers**
  - [ ] `updated_at` trigger added
  - [ ] Custom functions documented

- [ ] **Type Safety**
  - [ ] TypeScript types regenerated
  - [ ] Types exported from `@hounii/api`

- [ ] **Testing**
  - [ ] Test policies with different user roles
  - [ ] Verify cascade deletes work correctly
  - [ ] Check PostGIS queries return expected results

## Security Advisors

After migrations, check for security issues:

```typescript
// Run security advisors
mcp__supabase__get_advisors({ type: 'security' })

// Check for:
// - Tables without RLS
// - Missing indexes
// - Overly permissive policies
```

## Common Pitfalls

### ❌ Missing RLS

```sql
CREATE TABLE posts (...);
-- ❌ FORGOT: ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
```

Result: All data exposed to everyone!

### ❌ Wrong UUID Generation

```sql
-- ❌ WRONG: No default
id UUID PRIMARY KEY

-- ❌ WRONG: Using uuid_generate_v4() (requires extension)
id UUID PRIMARY KEY DEFAULT uuid_generate_v4()

-- ✅ CORRECT: Built-in generator
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
```

### ❌ Missing Timestamps

```sql
-- ❌ INCOMPLETE: No audit trail
CREATE TABLE posts (
  id UUID PRIMARY KEY,
  title TEXT
);

-- ✅ COMPLETE: Full audit trail
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT now() NOT NULL
);
```

### ❌ Overly Permissive RLS

```sql
-- ❌ DANGEROUS: Everyone can do everything
CREATE POLICY "Allow all"
  ON sensitive_data
  FOR ALL
  USING (true);

-- ✅ SECURE: Proper isolation
CREATE POLICY "Users own data"
  ON sensitive_data
  FOR ALL
  USING (auth.uid() = user_id);
```

## Data Migration Safety

When migrating existing data:

```sql
-- ❌ DANGEROUS: No rollback
UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';

-- ✅ SAFE: Use transactions
BEGIN;
  UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';
  -- Verify changes
  SELECT * FROM users WHERE role = 'admin';
  -- If wrong: ROLLBACK;
COMMIT;
```

**Do NOT hardcode generated IDs in data migrations** - UUIDs are non-deterministic.

## Edge Functions Integration

For complex logic, use Edge Functions:

```typescript
// supabase/functions/example/index.ts
import { createClient } from '@supabase/supabase-js';

Deno.serve(async (req) => {
  // Use service role key in Edge Functions (secure)
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  );

  // Your logic here
});
```

Deploy with MCP tools:

```typescript
mcp__supabase__deploy_edge_function({
  name: 'example',
  files: [{ name: 'index.ts', content: '...' }]
})
```

## References

- Main config: [CLAUDE.md](../../../CLAUDE.md)
- Supabase migrations: [supabase/migrations/](../../../supabase/migrations/)
- API package: [packages/api/](../../../packages/api/)
- Supabase docs: Use `mcp__supabase__search_docs` for latest info
