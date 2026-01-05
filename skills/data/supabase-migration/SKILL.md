---
name: supabase-migration
description: Safe database migration creation and management for Supabase PostgreSQL
version: 1.0.0
---

# Supabase Migration Skill

## Purpose
Create, test, and apply database migrations safely following project conventions.

---

## Migration Conventions

### File Naming Pattern
```
YYYYMMDDHHMMSS_description.sql

Examples:
20251018120000_add_user_preferences.sql
20251018130000_enable_rls_on_comments.sql
```

### Location
```
 /home/sk/skybox-gamehub/supabase
```

---

## Core Principles

### 1. Idempotency (CRITICAL)
**Always use**:
- `CREATE TABLE IF NOT EXISTS`
- `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` (PostgreSQL 9.6+)
- `DROP TABLE IF EXISTS`
- `DO $$ ... END $$;` blocks for conditional logic

**Never use**:
- `CREATE TABLE` without IF NOT EXISTS
- `ALTER TABLE ADD COLUMN` without IF NOT EXISTS
- Any command that fails on re-run

### 2. RLS Security (REQUIRED)
**Every new table MUST include**:
```sql
-- Enable RLS
ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

-- Basic policy (user owns record)
CREATE POLICY "Users can manage own records"
  ON table_name
  FOR ALL
  TO authenticated
  USING (profile_id = auth.uid())
  WITH CHECK (profile_id = auth.uid());
```

### 3. Foreign Keys
**Use profile_id, NOT user_id**:
```sql
-- ✅ Correct
profile_id UUID REFERENCES profiles(id) ON DELETE CASCADE

-- ❌ Wrong
user_id UUID REFERENCES auth.users(id)
```

---

## Migration Template

```sql
-- Migration: <description>
-- Created: YYYY-MM-DD
-- Status: <pending|applied|rolled-back>

BEGIN;

-- =============================================================================
-- TABLE CREATION
-- =============================================================================

CREATE TABLE IF NOT EXISTS table_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),

  -- Additional columns
  name TEXT NOT NULL,
  status TEXT DEFAULT 'active'
);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_table_profile
  ON table_name(profile_id);

CREATE INDEX IF NOT EXISTS idx_table_created
  ON table_name(created_at DESC);

-- =============================================================================
-- RLS POLICIES
-- =============================================================================

ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

-- Drop existing policies (idempotent)
DROP POLICY IF EXISTS "policy_name" ON table_name;

-- Create new policies
CREATE POLICY "Users manage own records"
  ON table_name
  FOR ALL
  TO authenticated
  USING (profile_id = auth.uid())
  WITH CHECK (profile_id = auth.uid());

-- =============================================================================
-- TRIGGERS (if needed)
-- =============================================================================

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_updated_at ON table_name;

CREATE TRIGGER trigger_update_updated_at
  BEFORE UPDATE ON table_name
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

COMMIT;
```

---

## Workflow

### 1. Create Migration File
```bash
# Navigate to migrations folder
cd /home/sk/skybox-gamehub/supabase/migrations

# Create new migration (use current timestamp)
touch $(date +%Y%m%d%H%M%S)_description.sql

# Edit with idempotent SQL
nano <filename>.sql
```

### 2. Test Locally
```bash
# Option 1: Apply via Supabase CLI
supabase db push

# Option 2: Apply directly via MCP
# Use mcp__supabase__execute_sql with migration content
```

### 3. Verify Migration
```sql
-- Check table created
SELECT tablename FROM pg_tables
WHERE tablename = 'your_table_name';

-- Verify RLS enabled
SELECT tablename, rowsecurity
FROM pg_tables
WHERE tablename = 'your_table_name';
-- Expected: rowsecurity = true

-- Check policies exist
SELECT schemaname, tablename, policyname
FROM pg_policies
WHERE tablename = 'your_table_name';

-- Test data insertion
INSERT INTO your_table_name (profile_id, name)
VALUES (auth.uid(), 'Test record')
RETURNING *;
```

### 4. Rollback (if needed)
```bash
# Create rollback migration
touch $(date +%Y%m%d%H%M%S)_rollback_previous_migration.sql
```

**Rollback template**:
```sql
BEGIN;

DROP TABLE IF EXISTS table_name CASCADE;
-- Remove any other changes

COMMIT;
```

---

## Common Patterns

### Adding Column to Existing Table
```sql
-- Add column safely
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'presentations'
    AND column_name = 'new_column'
  ) THEN
    ALTER TABLE presentations
    ADD COLUMN new_column TEXT;
  END IF;
END $$;
```

### Creating RPC Function
```sql
CREATE OR REPLACE FUNCTION function_name(param1 TEXT)
RETURNS TABLE (id UUID, name TEXT) AS $$
BEGIN
  RETURN QUERY
  SELECT t.id, t.name
  FROM table_name t
  WHERE t.profile_id = auth.uid()
  AND t.status = param1;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### Adding Public Access Policy
```sql
-- Allow public read access to presentations
CREATE POLICY "Public presentations visible to all"
  ON presentations
  FOR SELECT
  TO anon, authenticated
  USING (is_public = true);
```

---

## Testing Checklist

### Pre-Apply
- [ ] Migration file uses timestamp naming
- [ ] SQL is idempotent (can run multiple times)
- [ ] RLS enabled on new tables
- [ ] Foreign keys use `profile_id`
- [ ] Indexes added for common queries
- [ ] No hardcoded UUIDs or sensitive data

### Post-Apply
- [ ] Table exists: `\dt table_name`
- [ ] RLS enabled: `SELECT rowsecurity FROM pg_tables`
- [ ] Policies exist: `SELECT * FROM pg_policies`
- [ ] Can insert test data
- [ ] Can query test data
- [ ] No errors in Supabase dashboard

---

## Debugging

### Check Migration Status
```bash
# List applied migrations
supabase migration list

# Check current schema
supabase db diff
```

### Common Errors

**Error: "relation already exists"**
- **Cause**: Missing `IF NOT EXISTS`
- **Fix**: Add `IF NOT EXISTS` to CREATE statements

**Error: "column already exists"**
- **Cause**: Missing conditional column check
- **Fix**: Use DO block with `information_schema` check

**Error: "violates foreign key constraint"**
- **Cause**: Referenced table doesn't exist
- **Fix**: Ensure migration order is correct

**Error: "permission denied for table"**
- **Cause**: RLS blocking query
- **Fix**: Add appropriate RLS policy

---

## Security Rules

### Always Include
1. **RLS enabled** on all tables with user data
2. **profile_id check** in policies: `profile_id = auth.uid()`
3. **CASCADE delete** on foreign keys
4. **SECURITY DEFINER** on RPC functions (when needed)

### Never Include
1. **user_id** foreign keys (use `profile_id`)
2. **auth.users** direct references
3. **Hardcoded secrets** or API keys
4. **Production user data** in migrations

---

## Quick Reference

### Create Migration
```bash
cd /home/sk/skybox-gamehub/supabase/migrations
touch $(date +%Y%m%d%H%M%S)_description.sql
```

### Apply Migration
```bash
supabase db push
```

### Check RLS Status
```sql
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public';
```

### Verify Policies
```sql
SELECT tablename, policyname, cmd
FROM pg_policies
ORDER BY tablename;
```

---

## Example: Complete Migration

**File**: `20251018120000_add_comments_table.sql`

```sql
-- Migration: Add comments table for presentations
-- Created: 2025-10-18
-- Status: pending

BEGIN;

-- Table
CREATE TABLE IF NOT EXISTS comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  presentation_id UUID NOT NULL REFERENCES presentations(id) ON DELETE CASCADE,
  profile_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_comments_presentation
  ON comments(presentation_id);
CREATE INDEX IF NOT EXISTS idx_comments_profile
  ON comments(profile_id);

-- RLS
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users manage own comments" ON comments;
CREATE POLICY "Users manage own comments"
  ON comments FOR ALL TO authenticated
  USING (profile_id = auth.uid())
  WITH CHECK (profile_id = auth.uid());

DROP POLICY IF EXISTS "Public comments visible" ON comments;
CREATE POLICY "Public comments visible"
  ON comments FOR SELECT TO anon, authenticated
  USING (
    EXISTS (
      SELECT 1 FROM presentations
      WHERE id = comments.presentation_id
      AND is_public = true
    )
  );

COMMIT;
```

---

*This skill ensures all migrations are safe, idempotent, and follow project security standards.*
