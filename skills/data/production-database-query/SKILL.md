---
name: "production-database-query"
description: "Query production and staging Supabase databases safely using environment credentials with query approval workflow, safety checker, read-only roles, and audit logging; use when debugging production/staging data, verifying data exists, investigating bugs, checking RLS behavior, or applying hotfix migrations with approval"
version: "2.0.0"
last_updated: "2026-01-19"
---

# Production & Staging Database Query Skill

Query your Supabase production and staging databases safely using credentials from `.env.local` (with automatic secret management fallback and caching).

## When to Use This Skill

Use this skill when:
- Debugging production/staging data issues
- Verifying data exists on production or staging
- Investigating user-reported bugs that require database inspection
- Checking RLS policy behavior in production/staging
- Analyzing production data for support requests
- Applying hotfix migrations to production or staging

## Supabase Project Reference

Your application uses **two separate Supabase databases** for production and staging environments.

| Environment | Project Name | Project Reference ID | URL | Region |
|-------------|--------------|---------------------|-----|--------|
| **Production** | `your-app` | `your-prod-project-id` | `https://your-prod-project-id.supabase.co` | Your Region |
| **Staging** | `your-app-staging` | `your-staging-project-id` | `https://your-staging-project-id.supabase.co` | Your Region |

### Connection Pooler Hostnames

**Important**: Use the appropriate pooler hostname for your region.

**Production:**
- Session mode: `aws-X-region.pooler.supabase.com:5432`
- Database user: `postgres.your-prod-project-id`

**Staging:**
- Session mode: `aws-X-region.pooler.supabase.com:5432`
- Database user: `postgres.your-staging-project-id`

## Credential Management

### Environment Variables (Primary - Preferred)

Credentials are stored in `apps/web/.env.local`:

| Variable | Environment | Description |
|----------|-------------|-------------|
| `SUPABASE_DB_PASSWORD_PROD` | Production | Production database password |
| `SUPABASE_DB_PASSWORD_STAGING` | Staging | Staging database password |

### Secret Management (Fallback - Auto-cache)

If environment variables are not set, credentials can be fetched from your secret management system (e.g., 1Password, AWS Secrets Manager, Vault) and cached to `.env.local`.

Example with 1Password:
```bash
# Fetch from 1Password and cache to .env.local
SUPABASE_DB_PASSWORD_PROD="$(op item get <item-id> --fields password --reveal)"
echo "SUPABASE_DB_PASSWORD_PROD=$SUPABASE_DB_PASSWORD_PROD" >> apps/web/.env.local
```

## Prerequisites

- PostgreSQL client tools installed (`psql`)
- Credentials in `.env.local` OR secret management CLI installed and authenticated

## Quick Reference Commands

### Production Database

```bash
# Load password from .env.local (or fetch from secret manager and cache)
source apps/web/.env.local 2>/dev/null
if [ -z "$SUPABASE_DB_PASSWORD_PROD" ]; then
  # Fetch from your secret management system
  SUPABASE_DB_PASSWORD_PROD="$(your-secret-manager-command)"
  echo "SUPABASE_DB_PASSWORD_PROD=$SUPABASE_DB_PASSWORD_PROD" >> apps/web/.env.local
fi

# Connect to production
PGPASSWORD="$SUPABASE_DB_PASSWORD_PROD" psql \
  "postgresql://postgres.your-prod-project-id@aws-X-region.pooler.supabase.com:5432/postgres"

# Execute single query on production
PGPASSWORD="$SUPABASE_DB_PASSWORD_PROD" psql \
  "postgresql://postgres.your-prod-project-id@aws-X-region.pooler.supabase.com:5432/postgres" \
  -c "SELECT * FROM your_table LIMIT 5;"

# Apply migration to production
PGPASSWORD="$SUPABASE_DB_PASSWORD_PROD" psql \
  "postgresql://postgres.your-prod-project-id@aws-X-region.pooler.supabase.com:5432/postgres" \
  -f apps/web/supabase/migrations/YYYYMMDDHHMMSS_description.sql
```

### Staging Database

```bash
# Load password from .env.local (or fetch from secret manager and cache)
source apps/web/.env.local 2>/dev/null
if [ -z "$SUPABASE_DB_PASSWORD_STAGING" ]; then
  # Fetch from your secret management system
  SUPABASE_DB_PASSWORD_STAGING="$(your-secret-manager-command)"
  echo "SUPABASE_DB_PASSWORD_STAGING=$SUPABASE_DB_PASSWORD_STAGING" >> apps/web/.env.local
fi

# Connect to staging
PGPASSWORD="$SUPABASE_DB_PASSWORD_STAGING" psql \
  "postgresql://postgres.your-staging-project-id@aws-X-region.pooler.supabase.com:5432/postgres"

# Execute single query on staging
PGPASSWORD="$SUPABASE_DB_PASSWORD_STAGING" psql \
  "postgresql://postgres.your-staging-project-id@aws-X-region.pooler.supabase.com:5432/postgres" \
  -c "SELECT * FROM your_table LIMIT 5;"

# Apply migration to staging
PGPASSWORD="$SUPABASE_DB_PASSWORD_STAGING" psql \
  "postgresql://postgres.your-staging-project-id@aws-X-region.pooler.supabase.com:5432/postgres" \
  -f apps/web/supabase/migrations/YYYYMMDDHHMMSS_description.sql
```

## Dashboard SQL Editor URLs

**Production:** `https://supabase.com/dashboard/project/your-prod-project-id/sql/new`
**Staging:** `https://supabase.com/dashboard/project/your-staging-project-id/sql/new`

## Common Queries

### Check Table Data

```sql
SELECT *
FROM your_table
WHERE id = 'record-uuid'
LIMIT 10;
```

### Check RLS Policies for a Table

```sql
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE tablename = 'your_table';
```

### Check Migration Status

```sql
SELECT version, name, statements
FROM supabase_migrations.schema_migrations
ORDER BY version DESC
LIMIT 20;
```

## Recording Migrations After Manual Application

After applying a migration manually, record it in the tracking table:

```sql
INSERT INTO supabase_migrations.schema_migrations (version, name, statements)
VALUES ('YYYYMMDDHHMMSS', 'migration_name', ARRAY['SQL_STATEMENT'])
ON CONFLICT (version) DO NOTHING;
```

## Production Query Safety & Approval

**Purpose**: Prevent accidental data loss or corruption through automated safety checks, approval workflows, and audit logging.

### Why Query Safety Matters

**Common production disasters prevented**:
- ✅ DELETE without WHERE clause (loses all data)
- ✅ UPDATE without WHERE clause (corrupts all records)
- ✅ DROP TABLE or TRUNCATE (permanent data loss)
- ✅ UPDATE with wrong WHERE clause (partial corruption)
- ✅ Unauthorized schema changes

**Real impact**:
- 80% of production incidents involve database operations
- Average recovery time: 2-4 hours
- User trust damage: permanent
- Compliance violations: costly

### Query Safety Checker Script

Create `scripts/db-safety-check.sh` to validate queries before execution:

```bash
#!/usr/bin/env bash
# scripts/db-safety-check.sh
# Validates production database queries for dangerous patterns

set -euo pipefail

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Usage: ./scripts/db-safety-check.sh "SELECT * FROM users;"
# Usage: ./scripts/db-safety-check.sh -f migration.sql

QUERY=""
FILE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -f|--file)
      FILE="$2"
      shift 2
      ;;
    *)
      QUERY="$1"
      shift
      ;;
  esac
done

# Load query from file if specified
if [ -n "$FILE" ]; then
  if [ ! -f "$FILE" ]; then
    echo -e "${RED}❌ File not found: $FILE${NC}"
    exit 1
  fi
  QUERY=$(cat "$FILE")
fi

if [ -z "$QUERY" ]; then
  echo "Usage: $0 \"QUERY\" or $0 -f query.sql"
  exit 1
fi

# Convert query to uppercase for pattern matching
QUERY_UPPER=$(echo "$QUERY" | tr '[:lower:]' '[:upper:]')

echo "🔒 Analyzing query for safety..."
echo ""

ERRORS=0
WARNINGS=0

# CRITICAL: DELETE without WHERE
if echo "$QUERY_UPPER" | grep -E "DELETE\s+FROM" | grep -qv "WHERE"; then
  echo -e "${RED}❌ CRITICAL: DELETE without WHERE clause${NC}"
  echo "   This will delete ALL records from the table!"
  echo "   Add a WHERE clause or use TRUNCATE if intentional"
  ERRORS=$((ERRORS + 1))
fi

# CRITICAL: UPDATE without WHERE
if echo "$QUERY_UPPER" | grep -E "UPDATE\s+\w+" | grep -qv "WHERE"; then
  echo -e "${RED}❌ CRITICAL: UPDATE without WHERE clause${NC}"
  echo "   This will update ALL records in the table!"
  echo "   Add a WHERE clause"
  ERRORS=$((ERRORS + 1))
fi

# CRITICAL: DROP TABLE
if echo "$QUERY_UPPER" | grep -qE "DROP\s+TABLE"; then
  echo -e "${RED}❌ CRITICAL: DROP TABLE detected${NC}"
  echo "   This will permanently delete the table and all data!"
  echo "   Use migrations for schema changes"
  ERRORS=$((ERRORS + 1))
fi

# CRITICAL: DROP DATABASE
if echo "$QUERY_UPPER" | grep -qE "DROP\s+DATABASE"; then
  echo -e "${RED}❌ CRITICAL: DROP DATABASE detected${NC}"
  echo "   This will permanently delete the entire database!"
  echo "   This should NEVER be used on production"
  ERRORS=$((ERRORS + 1))
fi

# CRITICAL: TRUNCATE
if echo "$QUERY_UPPER" | grep -qE "TRUNCATE\s+TABLE"; then
  echo -e "${RED}❌ CRITICAL: TRUNCATE TABLE detected${NC}"
  echo "   This will delete ALL records from the table!"
  echo "   Use DELETE with WHERE for selective removal"
  ERRORS=$((ERRORS + 1))
fi

# CRITICAL: ALTER TABLE DROP COLUMN
if echo "$QUERY_UPPER" | grep -qE "ALTER\s+TABLE.*DROP\s+COLUMN"; then
  echo -e "${RED}❌ CRITICAL: ALTER TABLE DROP COLUMN detected${NC}"
  echo "   This will permanently delete the column and all its data!"
  echo "   Use migrations for schema changes"
  ERRORS=$((ERRORS + 1))
fi

# WARNING: ALTER TABLE without BEGIN/COMMIT
if echo "$QUERY_UPPER" | grep -qE "ALTER\s+TABLE" && ! echo "$QUERY_UPPER" | grep -qE "BEGIN|COMMIT"; then
  echo -e "${YELLOW}⚠️  WARNING: ALTER TABLE without transaction${NC}"
  echo "   Wrap schema changes in BEGIN...COMMIT for safety"
  WARNINGS=$((WARNINGS + 1))
fi

# WARNING: UPDATE with LIMIT
if echo "$QUERY_UPPER" | grep -E "UPDATE\s+\w+" | grep -qE "LIMIT"; then
  echo -e "${YELLOW}⚠️  WARNING: UPDATE with LIMIT${NC}"
  echo "   This is non-standard SQL and may not work as expected"
  WARNINGS=$((WARNINGS + 1))
fi

# WARNING: No LIMIT on SELECT
if echo "$QUERY_UPPER" | grep -qE "^SELECT" && ! echo "$QUERY_UPPER" | grep -qE "LIMIT|WHERE.*=.*'[^']*'"; then
  echo -e "${YELLOW}⚠️  WARNING: SELECT without LIMIT${NC}"
  echo "   This may return a large result set"
  echo "   Consider adding LIMIT clause"
  WARNINGS=$((WARNINGS + 1))
fi

# CRITICAL: Disabling RLS
if echo "$QUERY_UPPER" | grep -qE "DISABLE\s+ROW\s+LEVEL\s+SECURITY"; then
  echo -e "${RED}❌ CRITICAL: Disabling RLS detected${NC}"
  echo "   This removes security policies!"
  echo "   Use ENABLE ROW LEVEL SECURITY instead"
  ERRORS=$((ERRORS + 1))
fi

# WARNING: Creating policy without super admin bypass
if echo "$QUERY_UPPER" | grep -qE "CREATE\s+POLICY" && ! echo "$QUERY" | grep -qE "is_super_admin\(\)"; then
  echo -e "${YELLOW}⚠️  WARNING: CREATE POLICY without super admin bypass${NC}"
  echo "   Super admins may be blocked"
  echo "   Consider adding bypass clause to USING"
  WARNINGS=$((WARNINGS + 1))
fi

# Check for backup recommendation
if [ $ERRORS -gt 0 ]; then
  echo ""
  echo -e "${YELLOW}💾 RECOMMENDATION: Create database backup before proceeding${NC}"
  echo "   Use Supabase Dashboard > Database > Backups > Create Backup"
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
  echo -e "${GREEN}✅ Query passed all safety checks${NC}"
  exit 0
elif [ $ERRORS -eq 0 ]; then
  echo -e "${YELLOW}⚠️  Query has $WARNINGS warning(s)${NC}"
  echo "Review warnings before executing"
  exit 0
else
  echo -e "${RED}❌ Query FAILED safety checks: $ERRORS error(s), $WARNINGS warning(s)${NC}"
  echo ""
  echo "DO NOT execute this query on production!"
  echo "Fix errors or request peer review"
  exit 1
fi
```

**Usage**:

```bash
# Make script executable
chmod +x scripts/db-safety-check.sh

# Check inline query
./scripts/db-safety-check.sh "DELETE FROM users WHERE id = 'user-123';"

# Check query from file
./scripts/db-safety-check.sh -f migration.sql

# Pipe query to script
echo "UPDATE events SET status = 'cancelled';" | ./scripts/db-safety-check.sh
```

### Query Approval Workflow (Four-Eyes Principle)

**Purpose**: Require peer review for dangerous production queries.

#### When Approval is Required

| Operation | Staging | Production | Approval Required |
|-----------|---------|------------|-------------------|
| SELECT | ✅ Allowed | ✅ Allowed | ❌ No |
| INSERT (< 100 rows) | ✅ Allowed | ⚠️ Review | ❌ No |
| INSERT (> 100 rows) | ✅ Allowed | ⚠️ Review | ✅ Yes |
| UPDATE | ✅ Allowed | ⚠️ Review | ✅ Yes |
| DELETE | ✅ Allowed | ⚠️ Review | ✅ Yes |
| ALTER TABLE | ✅ Allowed | ⚠️ Review | ✅ Yes (use migrations) |
| DROP TABLE | ✅ Allowed | ❌ Blocked | ✅ Yes (extreme cases only) |
| TRUNCATE | ✅ Allowed | ❌ Blocked | ✅ Yes (extreme cases only) |

#### Approval Process

**Step 1: Requester creates approval request**

Create file: `docs/db-approvals/YYYY-MM-DD_description.md`

```markdown
# Database Query Approval Request

## Metadata
- **Date**: 2026-01-19
- **Requester**: @username
- **Environment**: Production
- **Urgency**: Normal / High / Emergency
- **Ticket**: #123 (optional)

## Context
Brief description of why this query is needed.

Example: "User reported duplicate records. Need to delete 5 duplicate records created by bug in migration."

## Query

\`\`\`sql
DELETE FROM your_table
WHERE id IN (
  'record-1-uuid',
  'record-2-uuid',
  'record-3-uuid'
);
\`\`\`

## Safety Check

\`\`\`bash
./scripts/db-safety-check.sh -f query.sql
✅ Query passed all safety checks
\`\`\`

## Expected Impact
- **Rows affected**: 3
- **Tables affected**: your_table
- **Downstream effects**: None

## Rollback Plan
No rollback needed - deleting duplicates created by bug.

## Testing on Staging
Tested on staging database:
- Query executed successfully
- 3 rows deleted
- No foreign key violations
- Application behavior unchanged

## Approval

- [ ] **Reviewer 1**: @reviewer-name (Date: YYYY-MM-DD)
- [ ] **Reviewer 2**: @reviewer-name (Date: YYYY-MM-DD) [Emergency only]

## Execution

- [ ] **Executed by**: @executor-name
- [ ] **Execution date**: YYYY-MM-DD HH:MM UTC
- [ ] **Result**: Success / Failed
- [ ] **Rows affected**: [actual count]
- [ ] **Notes**: [any observations]
```

**Step 2: Run safety checker**

```bash
./scripts/db-safety-check.sh -f query.sql
```

**Step 3: Test on staging**

```bash
# Test query on staging first
PGPASSWORD="$SUPABASE_DB_PASSWORD_STAGING" psql \
  "postgresql://postgres.your-staging-project-id@aws-X-region.pooler.supabase.com:5432/postgres" \
  -c "BEGIN; [YOUR_QUERY]; ROLLBACK;" # Use ROLLBACK to test without committing
```

**Step 4: Get peer review**

- Post approval request in your team channel
- Tag reviewer
- Wait for approval

**Step 5: Execute on production**

```bash
# ONLY after approval
PGPASSWORD="$SUPABASE_DB_PASSWORD_PROD" psql \
  "postgresql://postgres.your-prod-project-id@aws-X-region.pooler.supabase.com:5432/postgres" \
  -c "[YOUR_APPROVED_QUERY]"
```

**Step 6: Document execution**

Update approval doc with execution results and commit:

```bash
git add docs/db-approvals/YYYY-MM-DD_description.md
git commit -m "docs: executed prod query [description]"
git push
```

### Read-Only Database Roles

**Purpose**: Provide safe, read-only access for analysts and support team without risk of data modification.

#### Creating Read-Only Role

```sql
-- Create read-only role for analysts
CREATE ROLE app_readonly NOLOGIN;

-- Grant read access to all current tables
GRANT USAGE ON SCHEMA public TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO app_readonly;

-- Grant read access to future tables (auto-grant)
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT ON TABLES TO app_readonly;

-- Create readonly user
CREATE USER analyst_user WITH PASSWORD 'secure-random-password';
GRANT app_readonly TO analyst_user;

-- Verify permissions
\du analyst_user
\dp public.*
```

#### Using Read-Only Role

Store read-only credentials separately:

```bash
# apps/web/.env.local
SUPABASE_DB_PASSWORD_PROD_READONLY="readonly-password-here"
SUPABASE_DB_PASSWORD_STAGING_READONLY="readonly-password-here"
```

**Read-only connection**:

```bash
# Production read-only
PGPASSWORD="$SUPABASE_DB_PASSWORD_PROD_READONLY" psql \
  "postgresql://analyst_user@aws-X-region.pooler.supabase.com:5432/postgres"

# Staging read-only
PGPASSWORD="$SUPABASE_DB_PASSWORD_STAGING_READONLY" psql \
  "postgresql://analyst_user@aws-X-region.pooler.supabase.com:5432/postgres"
```

**Benefits**:
- ✅ Zero risk of accidental data modification
- ✅ Can share with analysts/support safely
- ✅ Faster queries (no transaction overhead)
- ✅ Compliance-friendly (audit trail)

### Query Execution Audit Log

**Purpose**: Track all production database operations for security, compliance, and debugging.

#### Audit Log Table Schema

```sql
-- Create audit log table
CREATE TABLE IF NOT EXISTS public.database_query_audit (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  executed_at timestamptz NOT NULL DEFAULT now(),
  executed_by text NOT NULL, -- user email or service name
  environment text NOT NULL CHECK (environment IN ('production', 'staging')),
  query_type text NOT NULL CHECK (query_type IN ('SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DDL', 'OTHER')),
  query_text text NOT NULL,
  query_hash text NOT NULL, -- SHA256 hash for deduplication
  rows_affected integer,
  execution_time_ms numeric,
  success boolean NOT NULL,
  error_message text,
  approval_doc_path text, -- Link to approval doc if applicable
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Index for queries
CREATE INDEX idx_query_audit_executed_at ON public.database_query_audit(executed_at DESC);
CREATE INDEX idx_query_audit_executed_by ON public.database_query_audit(executed_by);
CREATE INDEX idx_query_audit_environment ON public.database_query_audit(environment);
CREATE INDEX idx_query_audit_query_type ON public.database_query_audit(query_type);
CREATE INDEX idx_query_audit_query_hash ON public.database_query_audit(query_hash);

-- Enable RLS
ALTER TABLE public.database_query_audit ENABLE ROW LEVEL SECURITY;

-- Super admin can read all (customize based on your admin function)
CREATE POLICY query_audit_select ON public.database_query_audit
  FOR SELECT TO authenticated
  USING (auth.jwt() ->> 'role' = 'super_admin');

-- service_role can write
CREATE POLICY query_audit_insert ON public.database_query_audit
  FOR INSERT TO service_role
  WITH CHECK (true);
```

#### Audit Log Helper Script

Create `scripts/db-audit-log.sh`:

```bash
#!/usr/bin/env bash
# scripts/db-audit-log.sh
# Logs production database queries to audit table

set -euo pipefail

# Usage: ./scripts/db-audit-log.sh "production" "SELECT * FROM users LIMIT 10;" "engineer@example.com"

ENVIRONMENT="$1"
QUERY="$2"
EXECUTED_BY="$3"
APPROVAL_DOC="${4:-}"

# Determine query type
if echo "$QUERY" | grep -qiE "^\s*SELECT"; then
  QUERY_TYPE="SELECT"
elif echo "$QUERY" | grep -qiE "^\s*INSERT"; then
  QUERY_TYPE="INSERT"
elif echo "$QUERY" | grep -qiE "^\s*UPDATE"; then
  QUERY_TYPE="UPDATE"
elif echo "$QUERY" | grep -qiE "^\s*DELETE"; then
  QUERY_TYPE="DELETE"
elif echo "$QUERY" | grep -qiE "^\s*(CREATE|ALTER|DROP)"; then
  QUERY_TYPE="DDL"
else
  QUERY_TYPE="OTHER"
fi

# Generate query hash (for deduplication)
QUERY_HASH=$(echo -n "$QUERY" | shasum -a 256 | cut -d' ' -f1)

# Get current timestamp
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

# Insert audit log (using service_role client)
AUDIT_QUERY="
INSERT INTO public.database_query_audit (
  executed_at,
  executed_by,
  environment,
  query_type,
  query_text,
  query_hash,
  success,
  approval_doc_path,
  metadata
) VALUES (
  '$TIMESTAMP',
  '$EXECUTED_BY',
  '$ENVIRONMENT',
  '$QUERY_TYPE',
  \$\$$(echo "$QUERY" | sed "s/'/''/g")\$\$,
  '$QUERY_HASH',
  false, -- Will be updated after execution
  '$(echo "$APPROVAL_DOC" | sed "s/'/''/g")',
  '{\"tool\": \"claude-code\"}'::jsonb
);
"

echo "📝 Logging query to audit table..."
# Execute audit log insertion
# (Requires service_role credentials)

echo "✅ Query logged to audit table"
echo "   Environment: $ENVIRONMENT"
echo "   Query Type: $QUERY_TYPE"
echo "   Executed By: $EXECUTED_BY"
echo "   Query Hash: $QUERY_HASH"
```

#### Query History Report

```sql
-- View recent production queries
SELECT
  executed_at,
  executed_by,
  query_type,
  LEFT(query_text, 100) as query_preview,
  rows_affected,
  execution_time_ms,
  success
FROM public.database_query_audit
WHERE environment = 'production'
ORDER BY executed_at DESC
LIMIT 50;

-- Queries by user
SELECT
  executed_by,
  COUNT(*) as query_count,
  SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful_queries,
  SUM(CASE WHEN NOT success THEN 1 ELSE 0 END) as failed_queries
FROM public.database_query_audit
WHERE environment = 'production'
AND executed_at > NOW() - INTERVAL '30 days'
GROUP BY executed_by
ORDER BY query_count DESC;

-- Most common queries (by hash)
SELECT
  query_hash,
  LEFT(MIN(query_text), 100) as query_preview,
  COUNT(*) as execution_count,
  AVG(execution_time_ms) as avg_execution_time_ms
FROM public.database_query_audit
WHERE environment = 'production'
AND executed_at > NOW() - INTERVAL '30 days'
GROUP BY query_hash
ORDER BY execution_count DESC
LIMIT 20;
```

### Safety Checklist

Before executing ANY production query, verify:

- [ ] **Safety check passed**: `./scripts/db-safety-check.sh` shows ✅
- [ ] **Tested on staging**: Query executed successfully on staging database
- [ ] **Approval obtained**: For UPDATE/DELETE/DDL operations
- [ ] **Backup created**: For operations affecting > 1000 rows
- [ ] **Rollback plan**: Documented how to undo the change
- [ ] **Off-peak timing**: Scheduled during low traffic (if possible)
- [ ] **Monitoring ready**: Have dashboard open to watch for issues
- [ ] **Audit logged**: Execution recorded in audit table

## Error Handling

**Secret management not authenticated:**
```bash
# Authenticate with your secret management system
# Example for 1Password: op signin
```

**psql not installed:**
```bash
# macOS
brew install postgresql@16

# Linux
sudo apt-get install postgresql-client
```

**Connection timeout / "Tenant or user not found":**
- Verify pooler hostname for your region
- Verify credentials in secret manager
- Check network connection

## Best Practices

1. **Test on staging first**: Always test queries on staging before production
2. **Read-only by default**: Only use write operations when absolutely necessary
3. **Limit results**: Use `LIMIT` clause to avoid large result sets
4. **Use transactions**: For multiple queries, use transactions to ensure consistency
5. **Log queries**: Keep a record of production queries for audit purposes
6. **Record migrations**: After manual migration, always record in `schema_migrations`

## Customization Guide

When adopting this skill for your project:

1. **Update Supabase Project IDs**: Replace `your-prod-project-id` and `your-staging-project-id` with your actual project IDs
2. **Update Pooler Region**: Replace `aws-X-region` with your region (e.g., `aws-1-eu-central-1`)
3. **Update Environment Variables**: Adjust variable names in `.env.local` to match your naming convention
4. **Update Secret Management**: Replace 1Password commands with your secret management system (AWS Secrets Manager, Vault, etc.)
5. **Update RLS Functions**: Replace `is_super_admin()` with your actual admin check function
6. **Update File Paths**: Adjust paths to match your project structure (e.g., `apps/web/supabase/migrations/`)
7. **Update Approval Process**: Customize the approval workflow to match your team's process

## Related Documentation

- Production Database Access: Your Supabase documentation
- SQL Debugging Tool: `scripts/sql-exec.sh`
- Database Migration Manager: `.claude/skills/database-migration-manager/SKILL.md`

---

## Changelog

### v2.0.0 (2026-01-19)
- **Generalized from project-specific implementation**
  - Removed project-specific IDs, URLs, and references
  - Made credential management system-agnostic
  - Generalized RLS policy examples
  - Added comprehensive customization guide
  - Made suitable for any Supabase project

### v2.0.0 (2026-01-12) - Original
- **CRITICAL: Added comprehensive Production Query Safety & Approval section**
  - Query Safety Checker script (`scripts/db-safety-check.sh`) - Detects 10+ dangerous patterns
  - Query Approval Workflow (four-eyes principle) - Complete 6-step process with approval document template
  - Read-Only Database Roles - SQL setup for safe analyst access
  - Query Execution Audit Log - Complete audit system with table schema, helper scripts, and reporting queries
  - Safety Checklist - 8-point verification before production execution
  - Approval requirements table (when approval is needed for different operations)
- Updated skill description to include safety features
- **Impact**: Prevents accidental data loss/corruption through automated checks and peer review
