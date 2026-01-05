---
name: debugging-systematic
description: Expert systematic debugging through root cause analysis. Reflects on 5-7 possible sources, distills to 1-2 most likely causes, adds strategic logging to validate assumptions, and confirms diagnosis before fixing. Uses MCP servers for database validation. Use when troubleshooting errors, debugging issues, investigating bugs, analyzing problems, or when user mentions error, bug, not working, broken, or debugging.
version: 1.0.0
---

# Systematic Debugging - Root Cause Analysis

Expert debugging approach that identifies root causes through systematic analysis before applying fixes.

## Core Philosophy

**NEVER jump to solutions. ALWAYS diagnose first.**

1. Analyze the problem thoroughly
2. Generate multiple hypotheses
3. Add strategic logging
4. Validate assumptions with data
5. Confirm diagnosis with user
6. Only then apply the fix

## Debugging Workflow

### Step 1: Understand the Problem

**Gather Information:**

1. **What is the error/issue?**
   - Exact error message
   - Stack trace
   - Console output
   - User-reported behavior

2. **When does it occur?**
   - Always or intermittently?
   - Specific conditions?
   - After what actions?
   - In what environment?

3. **What is expected vs actual?**
   - Expected behavior
   - Actual behavior
   - Differences

**Example Questions to Ask:**
```
- Can you share the exact error message?
- When did this start happening?
- Does it happen every time or randomly?
- What were you doing when it occurred?
- Are there any console errors?
```

---

### Step 2: Reflect on Possible Sources (5-7 Hypotheses)

**REQUIRED: Generate 5-7 different possible root causes**

Think through multiple categories:

1. **Data Issues**
   - Missing fields in database
   - Wrong field names
   - Incorrect data types
   - Null/undefined values
   - Data format mismatches

2. **Logic Issues**
   - Incorrect conditional logic
   - Wrong variable scope
   - Race conditions
   - Async/await problems
   - State management errors

3. **API/Integration Issues**
   - API endpoint errors
   - Authentication failures
   - Missing permissions
   - Network timeouts
   - Response format changes

4. **Database Issues**
   - Schema mismatches
   - Field name typos
   - Missing collections/tables
   - Query syntax errors
   - Index problems

5. **Configuration Issues**
   - Environment variables
   - Missing dependencies
   - Version conflicts
   - Build configuration
   - Feature flags

6. **Frontend Issues**
   - Component lifecycle
   - Props not passed correctly
   - Event handlers not firing
   - State not updating
   - Routing problems

7. **Backend Issues**
   - Server errors
   - Middleware problems
   - Request validation
   - Response handling
   - Error catching

**Format Your Analysis:**

```markdown
## Possible Root Causes (Initial Analysis)

1. **Database field mismatch**
   - The field name in code might not match Firestore schema
   - Could be using 'userId' when database has 'user_id'

2. **Null/undefined handling**
   - Data might be null when code expects object
   - Missing null checks before accessing properties

3. **Async timing issue**
   - Component rendering before data loads
   - Missing await on async operation

4. **Type mismatch**
   - Expecting string but receiving number
   - Array expected but object provided

5. **Authentication state**
   - User not authenticated when code executes
   - Token expired or invalid

6. **API response format changed**
   - Backend returning different structure
   - Missing error handling for new format

7. **Environment configuration**
   - Missing environment variable
   - Wrong API endpoint in current environment
```

---

### Step 3: Distill to 1-2 Most Likely Sources

**Analyze the hypotheses and narrow down:**

Based on:
- Error message patterns
- Stack trace location
- Recent code changes
- System behavior

**Format:**

```markdown
## Most Likely Root Causes (Narrowed Analysis)

After analyzing the error pattern and stack trace, the two most likely causes are:

### Primary Hypothesis: Database Field Mismatch
**Probability: 70%**

The error occurs when accessing `user.profileData.imageUrl` but Firestore
might store it as `user.profile_data.image_url` or `user.profileImage`.

Evidence:
- Error shows "Cannot read property 'imageUrl' of undefined"
- This happens after Firestore query
- Schema documentation is outdated

### Secondary Hypothesis: Null Data Handling
**Probability: 25%**

User document exists but `profileData` field is null for some users.

Evidence:
- Error is intermittent (some users affected, others not)
- Older user accounts more likely to hit this
- Field was added later in development

### Other possibilities: 5%
```

---

### Step 4: Use MCP Servers for Database Validation

**CRITICAL: For database-related issues, ALWAYS verify with MCP servers**

#### Firebase MCP Server

**When to use:**
- Firestore data validation
- Check actual field names
- Verify document structure
- Inspect current state
- Validate queries

**Commands:**

```javascript
// List available Firebase MCP tools
mcp__firebase-afterdark-production__firebase_query
mcp__firebase-afterdark-staging__firebase_query

// Query specific document to check structure
firebase_query({
  collection: "users",
  documentId: "user123"
})

// Query collection to check field names
firebase_query({
  collection: "users",
  limit: 5
})

// Check if field exists in documents
firebase_query({
  collection: "users",
  where: [{ field: "profileData", operator: "!=", value: null }],
  limit: 10
})
```

**What to validate:**
- ✅ Actual field names (camelCase vs snake_case)
- ✅ Data structure (nested objects, arrays)
- ✅ Field types (string, number, boolean)
- ✅ Null/undefined values
- ✅ Missing fields in some documents

#### PostgreSQL/Supabase MCP Server

**When to use:**
- SQL database validation
- Check table schema
- Verify column names
- Inspect data types
- Validate relationships

**Commands:**

```sql
-- Check table structure
mcp__supabase-minrights__query({
  query: "SELECT column_name, data_type, is_nullable
          FROM information_schema.columns
          WHERE table_name = 'users'"
})

-- Inspect actual data
mcp__aws-postgres-minrights__query({
  query: "SELECT * FROM users LIMIT 5"
})

-- Check for null values
mcp__aws-postgres-minrights__query({
  query: "SELECT COUNT(*) FROM users WHERE profile_data IS NULL"
})

-- Verify column exists
mcp__aws-postgres-minrights__query({
  query: "SELECT EXISTS (
    SELECT FROM information_schema.columns
    WHERE table_name = 'users'
    AND column_name = 'image_url'
  )"
})
```

**What to validate:**
- ✅ Table and column names
- ✅ Data types and constraints
- ✅ Null values presence
- ✅ Foreign key relationships
- ✅ Actual data samples

#### Example MCP Validation

```markdown
## Database Validation (MCP Server Check)

Using Firebase MCP to verify user document structure:

Query: Get sample user document
```javascript
firebase_query({
  collection: "users",
  documentId: "abc123"
})
```

Result:
```json
{
  "uid": "abc123",
  "email": "user@example.com",
  "profile": {
    "imageUrl": "https://...",
    "bio": "..."
  }
}
```

**Finding: Field is `profile.imageUrl` not `profileData.imageUrl`**

This confirms Primary Hypothesis: Field name mismatch.
Code uses: `user.profileData.imageUrl`
Database has: `user.profile.imageUrl`
```

---

### Step 5: Add Strategic Logging

**NEVER fix without validation. Add logging first.**

#### Logging Strategy

**Purpose:**
- Validate hypotheses with real data
- See actual values at runtime
- Confirm problem location
- Understand data flow

**Where to add logs:**

1. **Before the error point**
   - Log data before it's used
   - Check what's actually received

2. **At decision points**
   - Log conditional branches taken
   - Verify logic flow

3. **At data transformations**
   - Log input and output
   - Verify transformations correct

4. **At API boundaries**
   - Log requests and responses
   - Verify data format

#### Logging Examples

**Bad Logging:**
```typescript
console.log("here");
console.log("got data");
console.log(user);
```

**Good Logging:**
```typescript
// Validate hypothesis: Check if profileData exists
console.log("=== User Profile Debug ===");
console.log("User object:", JSON.stringify(user, null, 2));
console.log("Has profileData?", user.hasOwnProperty('profileData'));
console.log("Has profile?", user.hasOwnProperty('profile'));
console.log("ProfileData value:", user.profileData);
console.log("Profile value:", user.profile);
console.log("========================");

// Check specific field path
try {
  console.log("Attempting to access imageUrl...");
  console.log("Path 1 (profileData.imageUrl):", user.profileData?.imageUrl);
  console.log("Path 2 (profile.imageUrl):", user.profile?.imageUrl);
} catch (error) {
  console.error("Error accessing imageUrl:", error.message);
}
```

**For Database Queries:**
```typescript
// Before query
console.log("=== Firestore Query Debug ===");
console.log("Querying collection:", collectionName);
console.log("Document ID:", docId);

// After query
console.log("Query result:", querySnapshot.exists());
console.log("Document data:", querySnapshot.data());
console.log("Available fields:", Object.keys(querySnapshot.data() || {}));
console.log("============================");
```

**For API Calls:**
```typescript
// Before request
console.log("=== API Request Debug ===");
console.log("Endpoint:", endpoint);
console.log("Method:", method);
console.log("Payload:", JSON.stringify(payload, null, 2));

// After response
console.log("Response status:", response.status);
console.log("Response data:", JSON.stringify(response.data, null, 2));
console.log("========================");
```

---

### Step 6: Present Diagnosis to User

**REQUIRED: Get user confirmation before fixing**

**Format:**

```markdown
## Diagnosis Summary

Based on my analysis and validation, I've identified the root cause.

### Problem
[Clear description of what's wrong]

### Root Cause
[Specific reason why it's happening]

### Evidence
1. [Evidence point 1]
2. [Evidence point 2]
3. [Evidence point 3]

### Proposed Solution
[How to fix it]

### Logs to Add First
Before fixing, I'll add these logs to confirm:
```typescript
[Specific logging code]
```

**Next Steps:**
1. Add logging code above
2. Reproduce the issue
3. Verify logs confirm diagnosis
4. Apply the fix

**May I proceed with adding the logs to validate this diagnosis?**
```

**Wait for user confirmation before proceeding.**

---

### Step 7: Validate with Logs

After user confirms and logs are added:

1. **Ask user to reproduce issue**
2. **Review log output**
3. **Confirm hypothesis**
4. **Adjust if needed**

**Example:**

```markdown
## Log Validation

Please reproduce the error and share the console output.

Expected logs will show:
- User object structure
- Which field path exists
- Exact value at error point

This will confirm if issue is:
✅ Field name mismatch (profileData vs profile)
❌ Null value handling
❌ Something else

Once logs confirm, I'll apply the appropriate fix.
```

---

### Step 8: Apply Fix Only After Validation

**ONLY after logs confirm the diagnosis:**

1. **Implement targeted fix**
2. **Add error handling**
3. **Add validation checks**
4. **Update related code**
5. **Add tests if needed**

**Example Fix:**

```typescript
// Before (broken)
const imageUrl = user.profileData.imageUrl;

// After (fixed and defensive)
const imageUrl = user.profile?.imageUrl || user.profileData?.imageUrl || null;

if (!imageUrl) {
  console.warn("User missing profile image:", user.uid);
  // Handle missing image gracefully
}
```

---

## Database-Specific Debugging

### Firestore Issues

**Common Problems:**

1. **Field name mismatches**
   ```
   Code: user.firstName
   DB:   user.first_name or user.name.first
   ```

2. **Missing fields**
   ```
   Older documents don't have new fields
   ```

3. **Wrong collection path**
   ```
   Code: users/{uid}/profile
   DB:   users/{uid}
   ```

4. **Subcollection confusion**
   ```
   Code: accessing as field
   DB:   stored as subcollection
   ```

**Validation Process:**

```markdown
1. Use Firebase MCP to query actual document
2. Compare structure with code expectations
3. Check field names (exact match, case-sensitive)
4. Verify nested object paths
5. Look for null/missing fields
6. Check array vs object types
```

### PostgreSQL/Supabase Issues

**Common Problems:**

1. **Column name mismatches**
   ```
   Code: userId
   DB:   user_id
   ```

2. **Type mismatches**
   ```
   Code expects: string
   DB returns:   number
   ```

3. **NULL handling**
   ```
   DB has NULL values
   Code doesn't handle
   ```

4. **Join issues**
   ```
   Missing foreign keys
   Wrong table references
   ```

**Validation Process:**

```markdown
1. Use PostgreSQL MCP to check schema
2. Verify column names and types
3. Run sample query to see actual data
4. Check for NULL values
5. Validate relationships
6. Test query syntax
```

---

## MCP Server Integration

### Available MCP Servers

**Firebase:**
- `mcp__firebase-afterdark-production__firebase_query`
- `mcp__firebase-afterdark-staging__firebase_query`

**PostgreSQL:**
- `mcp__aws-postgres-minrights__query`
- `mcp__aws-postgres-minrights__execute_sql`

**Supabase:**
- `mcp__supabase-minrights__query`
- `mcp__supabase-minrights__execute_sql`

### When to Use MCP Servers

**Always use for:**
- ✅ Verifying field names
- ✅ Checking data structure
- ✅ Inspecting actual values
- ✅ Validating queries
- ✅ Understanding schema
- ✅ Finding mismatches

**Example Workflow:**

```markdown
1. User reports error accessing user.email
2. Generate hypothesis: Field might be 'emailAddress'
3. Use Firebase MCP to query user document
4. See actual structure: { email_address: "..." }
5. Confirm: Field is 'email_address' not 'email'
6. Add logs to validate
7. Apply fix: user.email_address
```

---

## Complete Example Debugging Session

### Problem Report

```
User: "Getting error: Cannot read property 'imageUrl' of undefined
       when trying to access dating features"
```

### Step 1: Understand

```markdown
Error: Cannot read property 'imageUrl' of undefined
Location: Dating discovery page
When: When user navigates to /discover
Expected: Show user profile images
Actual: Crash with error
```

### Step 2: Reflect (5-7 Hypotheses)

```markdown
1. **Field name mismatch**: Code uses different field than database
2. **Null profileData**: User has no profile data object
3. **Async timing**: Accessing data before it loads
4. **Auth state**: User not logged in when code executes
5. **Old user data**: Older accounts missing new fields
6. **Firestore query error**: Query failing silently
7. **Type error**: profileData is string not object
```

### Step 3: Distill (1-2 Most Likely)

```markdown
Primary (70%): Field name mismatch
- Error mentions 'undefined' suggesting path issue
- Likely accessing user.profileData when DB has user.profile

Secondary (25%): Null/missing data
- Some users might not have profile data
- Field added later in development
```

### Step 4: MCP Validation

```markdown
Using Firebase MCP to check structure:

firebase_query({
  collection: "users",
  limit: 3
})

Result shows:
{
  uid: "...",
  profile: {          // ← It's "profile" not "profileData"
    imageUrl: "...",
    bio: "..."
  }
}

Confirmed: Field mismatch. Database uses "profile", code uses "profileData"
```

### Step 5: Add Logging

```typescript
// Add to page component
console.log("=== Dating Profile Debug ===");
console.log("User data:", JSON.stringify(userData, null, 2));
console.log("Has profileData?", userData.hasOwnProperty('profileData'));
console.log("Has profile?", userData.hasOwnProperty('profile'));
console.log("ProfileData:", userData.profileData);
console.log("Profile:", userData.profile);
console.log("========================");
```

### Step 6: Present Diagnosis

```markdown
## Diagnosis

**Root Cause**: Field name mismatch

**Evidence**:
1. MCP query shows database uses `user.profile.imageUrl`
2. Code is accessing `user.profileData.imageUrl`
3. Error "Cannot read property 'imageUrl' of undefined" indicates profileData is undefined

**Solution**: Update code to use correct field path

**Logs to add**: [code above]

Shall I add these logs to confirm, then fix the field path?
```

### Step 7: Wait for Confirmation

User: "Yes, add the logs"

### Step 8: After Log Validation

```markdown
Logs confirmed diagnosis. Applying fix:

// Before
const imageUrl = user.profileData.imageUrl;

// After
const imageUrl = user.profile?.imageUrl;

// Add defensive check
if (!imageUrl) {
  console.warn("User missing profile image");
  // Redirect to settings
}
```

---

## Key Principles

1. **Never Skip Analysis**
   - Always generate 5-7 hypotheses
   - Always narrow to 1-2 most likely
   - Always validate with data

2. **Use MCP Servers**
   - Check actual database structure
   - Verify field names
   - Inspect real data
   - Never assume schema

3. **Add Logs First**
   - Validate hypotheses with data
   - Never fix blindly
   - Strategic, meaningful logs
   - Confirm before fixing

4. **Get User Confirmation**
   - Present diagnosis clearly
   - Wait for approval
   - Explain reasoning
   - Show evidence

5. **Fix After Validation**
   - Only apply fix when confirmed
   - Add defensive code
   - Handle edge cases
   - Prevent recurrence

## Debugging Checklist

Before any fix:

- [ ] Generated 5-7 possible root causes
- [ ] Narrowed to 1-2 most likely sources
- [ ] Used MCP server to validate (if database-related)
- [ ] Added strategic logging code
- [ ] Presented diagnosis to user
- [ ] Got user confirmation
- [ ] Validated with log output
- [ ] Applied targeted fix
- [ ] Added error handling
- [ ] Tested the fix

Remember: **Systematic debugging finds root causes. Jumping to solutions fixes symptoms.**
