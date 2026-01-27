---
name: write-release-notes
description: Generate professional Bytebase release notes by analyzing git commits, building PR dependency graphs, checking Terraform impact, searching Linear for customer feedback, and following established conventions. Creates Linear tracking issue and owner confirmation comments (with user approval before each write operation). Use when preparing release notes for minor or patch versions.
---

# Release Notes Generator

A systematic skill for generating professional Bytebase release notes by analyzing git commits, building PR dependency graphs, checking Terraform impact, and following established conventions.

## Overview

This skill helps you create release notes for Bytebase releases by:
1. Determining release version (minor vs patch) from branch names
2. Extracting commits between versions
3. **Building PR dependency graph (DAG)** to identify related changes
4. **Identifying root cause PRs** that drive cascading changes
5. Analyzing code changes to understand impact
6. Checking Terraform configuration implications
7. Searching Linear for customer feedback
8. Learning from previous release note patterns
9. Categorizing and prioritizing changes with ownership
10. **Excluding internal follow-ups** (fixes for features in this release)
11. Writing concise, user-focused release notes (no implementation details or reasoning)
12. Saving draft to `docs/release-notes/draft-X.Y.Z.md` for iteration
13. Creating Linear issue with title `<version>-<date>_release_note` **(with user confirmation)**
14. Adding confirmation comments with proper @mentions for each owner **(with user confirmation)**

**Note**: All Linear write operations (creating issues, posting comments) require explicit user confirmation before execution.

## Step-by-Step Process

### Phase 1: Version Identification (CRITICAL)

#### 1.1 Find the Version Range

```bash
# List available tags
git tag --list "*<major>.<minor>*" | sort -V

# Check for release branches
git branch -a | grep -E "release/<major>.<minor>"

# Get the latest tag
git describe --tags --abbrev=0
```

#### 1.2 Determine Version Type

**IMPORTANT**: The version type affects what sections are allowed in the release notes.

| Version Change | Type | Example |
|----------------|------|---------|
| 3.12.x → 3.13.0 | **Minor** | Minor digit increases |
| 3.12.0 → 3.12.1 | **Patch** | Patch digit increases |

**Rules by version type:**

| Section | Minor Version | Patch Version |
|---------|--------------|---------------|
| Notable Changes | ✅ Expected | ⚠️ Unusual - confirm with user |
| Features | ✅ Expected | ⚠️ Unusual - confirm with user |
| Enhancements | ✅ Yes | ✅ Yes |
| Bug Fixes | ✅ Yes | ✅ Yes (primary focus) |

#### 1.3 Confirm Version with User

**ALWAYS confirm the version before proceeding:**

```
I've identified the following version information:
- Previous version: [X.Y.Z]
- New version: [A.B.C]
- Version type: [Minor/Patch]

Is this correct? If not, please provide the correct versions.
```

**If you cannot determine versions from branches/tags, ASK the user immediately.**

### Phase 2: Data Collection

#### 2.1 Extract All Commits

```bash
# If new version is tagged
git log <prev-version>..<new-version> --oneline --decorate

# If new version is a release branch (common case)
git log <prev-version>..origin/release/<new-version> --oneline --decorate
```

**Output**: List of all commits with their hashes and one-line messages.

#### 2.2 Create Analysis Task List

Use TodoWrite to create tasks:
- Batch commits into groups of 5-7
- One task per batch for analysis
- Task for Terraform impact check
- Task for Linear issue search
- Final task for compilation

### Phase 3: Commit Analysis & PR Dependency Graph (CRITICAL)

#### 3.1 Fetch PR Details (Not Just Commit Messages)

**IMPORTANT**: Commit messages are often insufficient. Always fetch PR descriptions:

```bash
# Get PR details including body, labels, and related issues
gh pr view <pr-number> --json title,body,labels

# Extract PR number from commit message
# Commits usually end with "(#12345)"
```

**What to extract from each PR:**
- **Title and body**: Full context of the change
- **Labels**: Look for "breaking" label
- **Linear issue references**: BYT-XXXX in body
- **"Part of" or "Closes" references**: Indicates parent feature

#### 3.2 Build PR Dependency Graph (DAG)

**CRITICAL STEP**: Before categorizing, identify how PRs relate to each other:

1. **Find root cause PRs**: Look for PRs that:
   - Reference a Linear issue with broad scope (e.g., "Separate CI and CD")
   - Have many follow-up PRs
   - Are marked with "breaking" label or `refactor!:` prefix
   - Change fundamental architecture

2. **Group related PRs**: PRs are related if they:
   - Reference the same Linear issue
   - One PR "follows" or "builds on" another
   - Fix issues introduced by another PR in this release
   - Are part of the same feature initiative

3. **Order by time**: Within a group, order PRs chronologically to understand the flow

**Example DAG:**
```
BYT-8521: Separate CI (Plan+Issue) and CD (Rollout)
├── #18610 - Core: separate rollout creation from issue creation
│   ├── #18620 - Remove pipeline table
│   │   ├── #18662 - Rollout nested under plan
│   │   └── #18663-#18668 - Follow-up refactors
│   ├── #18704 - Unified Plan/Issue page
│   │   └── #18709, #18819, #18838, #18861 - Fixes for unified page
│   └── #18698 - Webhook redesign (driven by new lifecycle)
└── #18624, #18634, #18635 - Issue API cleanup
```

#### 3.3 Identify What NOT to List

**Exclude from release notes:**
- **Fixes for features in this release**: If PR #18861 fixes PR #18704 (both in this release), don't list #18861 separately
- **Internal refactors**: PRs that prepare for a feature but have no user impact
- **Follow-up polish**: PRs that tweak a feature already listed

**Rule**: If a PR's parent feature is in this release, the PR is part of that feature, not a separate item.

#### 3.4 Examine Commits with Context

For each batch, run these in parallel:

```bash
git show --stat <commit-hash>
gh pr view <pr-number> --json title,body,labels
```

**What to extract:**
- **Files changed**: Indicates scope (frontend/backend/proto/parser)
- **Lines added/removed**: Indicates magnitude
- **PR description**: Full context and reasoning
- **Linear issue**: Customer-facing problem being solved
- **Author**: For ownership tracking

#### 3.5 Identify Change Owner

For each significant change, identify the owner:

```bash
# Get the author with most changes for a feature area
git log <prev-version>..origin/release/<new-version> --format='%an' -- <path-pattern> | sort | uniq -c | sort -rn | head -1

# For a specific commit
git show --format='%an <%ae>' -s <commit-hash>
```

**Document the owner for each release note item** - we need to confirm correctness with them.

#### 3.6 Categorize Based on DAG

Use this decision tree, but apply it to **feature groups**, not individual PRs:

```
Is it a breaking change or behavior change?
├─ YES → Notable Changes (describe the root cause, not individual PRs)
└─ NO
   ├─ Does it fix a bug that existed BEFORE this release?
   │  └─ YES → Bug Fixes
   │  └─ NO (fixes something introduced in this release) → Exclude
   └─ NO
      ├─ Is it a new capability?
      │  └─ YES → Features (combine related PRs into one entry)
      └─ Is it an improvement/optimization?
         └─ YES → Enhancements
```

**Specific patterns:**

| Commit Pattern | Category | Example |
|----------------|----------|---------|
| `fix:` prefix | Bug Fixes (if pre-existing bug) | `fix: SQL Editor tab caching` |
| `fix:` for new feature | Exclude (part of feature) | `fix: redirect to new UI` |
| `feat:` new capability | Features | `feat: IdP-initiated SSO` |
| `feat:` improvement | Enhancements | `feat: MSSQL explain visualization` |
| `refactor!:` prefix | Notable Changes | `refactor!: redesign webhook events` |
| `refactor:` with user impact | Enhancements | `refactor: webhook message` |
| `refactor:` no user impact | Omit | `refactor: internal helper` |
| `chore:` with user impact | Enhancements | `chore: optimize SQL editor tabs` |
| `chore:` no user impact | Omit | `chore: update dependencies` |

### Phase 4: Terraform Impact Check (CRITICAL)

#### 4.1 Check for Terraform-Affecting Changes

For EACH categorized change, check if it affects Terraform configuration:

```bash
# Search for changes to Terraform-related files
git show --stat <commit-hash> | grep -E "(terraform|provider|resource)"

# Check API changes that might affect Terraform
git show --stat <commit-hash> | grep -E "proto/v1/(project|database|instance|environment|setting|policy)"

# Check for resource name/field changes
git show <commit-hash> -- "proto/**/*.proto" | grep -E "(field|option|message|enum)"

# Check for removed or renamed fields in proto files
git diff <prev-version>..origin/release/<new-version> -- "proto/v1/*.proto" | grep -E "^[-+].*\b(string|int|bool|repeated|message)\b"
```

**Key areas that affect Terraform:**

| Change Area | Terraform Impact | Check Files |
|-------------|-----------------|-------------|
| API field rename/remove | **Breaking** - config update required | `proto/v1/*.proto` |
| New API field | May need config update | `proto/v1/*.proto` |
| Resource behavior change | May affect state | Backend handlers |
| Default value change | May affect plan/apply | Service layer |
| Validation rule change | May cause apply failures | Validators |
| Resource path change | **Breaking** - update resource refs | API routes |

#### 4.2 Document Terraform Impact

For changes that affect Terraform, add to the release note:

```markdown
- [Change description] (**Terraform**: [impact description, e.g., "update `bytebase_instance` resource field `x` to `y`"])
```

**Example:**
```markdown
- Rename environment resource field from `tier` to `environment_tier` (**Terraform**: update `bytebase_environment` resource configuration to use new field name)
```

#### 4.3 Create Terraform Impact Summary

In the draft metadata, include a Terraform impact table:

```markdown
## Terraform Impact
| Change | Field/Path | Impact |
|--------|------------|--------|
| Issue API | rollout, releasers, task_status_count removed | Check if provider reads these fields |
| Rollout API paths | /plans/{id}/rollout | Update resource path references |
```

### Phase 5: Linear Issue Search

#### 5.1 Search for Customer Feedback

Use Linear MCP tools to find customer-reported issues:

```
mcp__linear__list_issues with:
- query: relevant keywords from commits
- labels: "customer-feedback", "bug", "customer-reported"
- updatedAt: -P30D (last 30 days)
```

**Search strategies:**
1. Search by feature area mentioned in commits
2. Search by database engine names
3. Search by component names (SQL Editor, Schema Editor, etc.)
4. Search recent issues (last 2-4 weeks)
5. Search by PR-referenced Linear issues (BYT-XXXX found in PR bodies)

#### 5.2 Get Parent Issues for Context

When a PR references a Linear issue, fetch the issue to understand the broader context:

```
mcp__linear__get_issue with:
- id: BYT-XXXX
- includeRelations: true
```

This helps identify:
- Parent initiatives that group multiple PRs
- Related issues that should be consolidated
- Customer-reported problems being addressed

#### 5.3 Confirm Customer Issues with User

Present found Linear issues:

```
I found the following Linear issues that may be related to this release:
- [ISSUE-123]: Description (Status: Done)
- [ISSUE-456]: Description (Status: Done)

Which of these should be highlighted as customer-reported fixes in the release notes?
```

### Phase 6: Learn from Previous Releases

#### 6.1 Fetch Recent Release Notes

Visit and analyze 2-3 recent releases:
- Same major version (e.g., 3.12.1, 3.12.0 when writing 3.12.2)
- One minor release example (x.x.1 or x.x.2)

```
URL: https://github.com/bytebase/bytebase/releases
```

Use WebFetch tool to extract:
1. **Section structure**: What sections are used?
2. **Writing style**: Verb tense, length, tone
3. **Grouping patterns**: How are related items grouped?
4. **Database prefixes**: How are DB-specific features marked?
5. **Notable Changes examples**: What qualifies as notable?

### Phase 7: Prioritization

#### 7.1 Write ALL Release Notes First

**IMPORTANT**: Do NOT limit items during initial writing. Write release notes for ALL significant changes first.

For each section, compile:
- All Notable Changes (with owner)
- All Features (with owner)
- All Enhancements (with owner)
- All Bug Fixes (with owner)

**Order items by priority within each section.**

#### 7.2 Apply Priority Matrix

| Priority | Criteria | Treatment |
|----------|----------|-----------|
| P0 | Customer-reported bugs, security issues, data corruption | **Must include** in Bug Fixes, list first |
| P1 | Breaking changes, new major features, Terraform-affecting | **Must include** in Notable Changes or Features |
| P2 | User-facing improvements, performance gains | Include, order by impact |
| P3 | Internal refactors with indirect benefits | Group or omit |
| P4 | Code cleanup, internal changes | Omit |

#### 7.3 Present All Items Ordered by Priority

After writing all items, present to user with priority ordering:

```markdown
## Full Release Notes (for your review)

### Notable Changes (X total) — INCLUDE ALL
1. [Most impactful change] — Owner: [Name] | Terraform: [Yes/No]
2. [Second change] — Owner: [Name]
...

### Features (X total) — Ordered by Priority
1. [Highest priority feature] — Owner: [Name]
2. [Second priority] — Owner: [Name]
...

### Enhancements (X total) — Ordered by Priority
1. [Highest priority enhancement] — Owner: [Name]
...

### Bug Fixes (X total) — Ordered by Priority
1. [Customer-reported / most impactful] — Owner: [Name]
2. [Database-specific fixes] — Owner: [Name]
...

Please review and let me know if any items should be reordered or excluded.
```

#### 7.4 Patch Version Validation

**If this is a PATCH version and Notable Changes or Features were found:**

```
⚠️ ATTENTION: This is a patch version upgrade (X.Y.Z → X.Y.Z+1), but I found:
- [N] Notable Changes
- [N] Features

Patch versions typically should NOT contain Notable Changes or Features.
Please confirm:
1. Should these be reclassified as Enhancements?
2. Should this actually be a minor version upgrade?
3. Are these exceptions that should remain as-is?
```

### Phase 8: Writing

#### 8.1 Use This Exact Template

**Section Order**: Notable Changes → Features → Enhancements → Bug Fixes

```markdown
# X.Y.Z - Month Day, Year

## 🔔 Notable Changes

- **[Major change title]** — [Explanation of what changed and impact on users]
  - [Sub-point if needed]
  - [Migration guidance if applicable]

## 🚀 Features

1. **[Feature name]** — [What it does and benefit to users]
2. **[Database Name]** — [New capability description]
...

## 🎄 Enhancements

1. **[Enhancement area]** — [What improved]
2. [General improvement with user benefit]
...

## 🐞 Bug Fixes

1. **[Database Name]** — [What was fixed]
2. Fix [description of the problem that was fixed]
...

---

**IMPORTANT:** Before upgrading to this version, please backup the [metadata](https://www.bytebase.com/docs/administration/back-up-restore-metadata/). Bytebase doesn't support in-place downgrade. Also avoid running multiple Bytebase containers sharing the same data directory. Otherwise, it may corrupt the metadata.
```

#### 8.2 Writing Rules

**Grammar and Style:**
- **Tense**: Present tense verbs ("Add", "Fix", "Improve", "Support")
- **Voice**: Active voice, subject often implied
- **Length**: One line per item, keep it short and concise
- **Tone**: Professional, factual, user-focused

**Content Rules:**
- **Keep it concise**: Avoid overly detailed descriptions. Don't include implementation reasoning or technical details unless absolutely necessary for user understanding.
- **Lead with impact**: What changed for users, not how it was implemented
- **No reasoning**: Don't explain "why" a change was made (e.g., avoid "since labels are Issue properties"). Just state what changed.
- **Infrastructure/backend changes**: For changes to internal systems (parsers, advisors, etc.), describe the **user-facing impact** not the technical fix. Example: "Fix SQL review showing incorrect line numbers" instead of "Fix advisor line position calculation in multi-statement parsing"
- **Group related changes**: Major features with multiple PRs → single entry with sub-bullets
- **Use database prefixes**: Format as `**Database Name** —` for DB-specific features
- **Include Terraform impact**: When applicable, add (**Terraform**: [details])
- **Number items**: Use numbered lists for Features/Enhancements/Bug Fixes to show priority

**Examples:**

Good (concise, user-focused):
```markdown
- Fix rollout date filter not working
- Fix SQL review showing incorrect line numbers for multi-statement SQL
- **SQL Server** — Add visualized EXPLAIN support
```

Bad (too detailed or too vague):
```markdown
- Fix SQL Editor tab caching preventing stale database query contexts from being loaded (too long)
- Show issue labels in "Ready for Review" popover during Plan creation, making the two-step Plan → Issue workflow clearer since labels are Issue properties (includes unnecessary reasoning)
- Fix advisor line position and refactor statement text architecture (technical implementation detail instead of user impact)
```

#### 8.3 Review Checklist

Before finalizing:
- [ ] Version confirmed with user (minor vs patch)
- [ ] PR dependency graph built to identify related changes
- [ ] Fixes for features in this release excluded (not listed separately)
- [ ] Patch version has no Notable Changes/Features (or confirmed as exception)
- [ ] All customer-reported issues addressed and listed first in Bug Fixes
- [ ] Terraform impact documented for all applicable changes
- [ ] Each item uses present tense
- [ ] Database-specific items have proper prefix format
- [ ] No implementation details (unless necessary for understanding)
- [ ] Breaking changes clearly explained in Notable Changes
- [ ] Owner identified for each item (for confirmation)
- [ ] Related changes grouped to save space
- [ ] Standard warning footer included
- [ ] User benefit clear for each enhancement
- [ ] Items ordered by priority within each section
- [ ] **Owner confirmation table matches release notes 1:1** (every line item has a row with full text)

### Phase 9: Linear Issue & Owner Confirmation

**IMPORTANT**: Before each Linear write operation, you MUST confirm with the user. Never create issues or comments without explicit user approval.

#### 9.1 Create Linear Issue for Release Notes

After finalizing the release notes draft, prepare to create a Linear issue to track confirmations.

**Issue Title Format**: `<version>-<date>_release_note`
- Example: `3.14.0-20260112_release_note`

**Issue Description**: Include the full release notes content and an owner confirmation table.

**⚠️ CONFIRM WITH USER BEFORE CREATING:**

Present the issue details and ask for confirmation:

```
I'm ready to create a Linear issue to track the release notes:

**Title:** 3.14.0-20260112_release_note
**Team:** Bytebase
**Assignee:** Peter Zhu
**Priority:** High

**Description:**
[Show the full release notes content that will be included]

Should I create this Linear issue? (yes/no)
```

Only proceed with `mcp__linear__create_issue` after user confirms.

#### 9.2 Subscribe Stakeholders

After creating the issue, prepare to subscribe Danny Xu and Tianzhou Chen.

**⚠️ CONFIRM WITH USER BEFORE COMMENTING:**

```
I'll now add a comment to subscribe stakeholders (Danny and Tianzhou) to the issue.

**Comment preview:**
"[danny](https://linear.app/bytebase/profiles/danny) [tianzhou](https://linear.app/bytebase/profiles/tianzhou) FYI - subscribing you to this release note issue for visibility."

Should I post this comment? (yes/no)
```

Only proceed with `mcp__linear__create_comment` after user confirms.

#### 9.3 Build Owner Confirmation Table (CRITICAL)

**IMPORTANT**: The owner confirmation table MUST exactly match every line item in the release notes.

**Requirements:**
1. **One row per release note line item** - Every numbered item in Features, Enhancements, Bug Fixes gets a row
2. **Include full item text** - Use the exact text from the release notes, not abbreviated labels
3. **Use section numbers** - Reference items as "Features #1", "Bug Fixes #12", etc.
4. **Match 1:1** - The confirmation table is the source of truth for Linear comments

**Table Format:**
```markdown
## Owner Confirmation Status
| Section | # | Item | Owner(s) | Confirmed |
|---------|---|------|----------|-----------|
| Notable | 1 | **CI/CD workflow redesigned** — Following industry practices... | Steven Li, Danny Xu | [ ] |
| Notable | 2 | **Plan title required** — Users must provide a meaningful title... | Danny Xu | [ ] |
| Features | 1 | **High Availability (HA)** — Run multiple Bytebase instances... | Xzavier Zane, Danny Xu | [ ] |
| Features | 2 | **Skip approval for specific rules** — Add 'no approval required'... | Xzavier Zane | [ ] |
...
| Bug Fixes | 1 | **PostgreSQL** — Fix SDL rollout failures with cyclic FK... | Adrian Lam | [ ] |
| Bug Fixes | 2 | **Oracle** — Fix schema sync generating DROP+CREATE... | Adrian Lam | [ ] |
...
```

**Why this matters:**
- Linear comments are generated FROM this table
- If the table doesn't match the release notes, owners confirm wrong items
- The table serves as the checklist for owner sign-off

#### 9.4 Create Confirmation Comments with @mentions

**IMPORTANT**: Create separate comments for each owner, grouping their items together. Comments MUST use the exact text from the owner confirmation table.

**Git-to-Linear User Mapping**:
| Git Author | Linear Name | Linear displayName |
|------------|-------------|-------------------|
| boojack | Steven Li | steven |
| ecmadao | Edward Lu | ed |
| h3n4l | Adrian Lam | h3n4l |
| Danny Xu | Danny Xu | danny |
| p0ny | Xzavier Zane | p0ny |
| rebelice | Jonathan Yablonski | junyi |
| Vincent Huang | Vincent Huang | vh |
| zchpeter | Peter Zhu | pz |

**Mention Format**: To properly @mention users in Linear comments, use a markdown link to their profile:

```markdown
[displayName](https://linear.app/bytebase/profiles/displayName)
```

**Comment Format** - Include section and item number:
```markdown
[owner](https://linear.app/bytebase/profiles/owner) Please confirm the following items are accurate:

**Notable Changes:**
- [ ] #1 **CI/CD workflow redesigned** — Following industry practices (GitHub, GitLab, Argo CD), the database change workflow is now separated into distinct CI (review) and CD (deployment) phases (with Danny Xu)

**Features:**
- [ ] #10 **Release info in UI** — Display release information in task items and rollout views

**Bug Fixes:**
- [ ] #10 **Grant request panel** — Fix showing empty user selector and disabled submit button
- [ ] #11 **Issue preset buttons** — Fix not working on first click
```

**⚠️ CONFIRM WITH USER BEFORE POSTING COMMENTS:**

Present ALL owner comments at once for batch approval:

```
I'll now add confirmation comments for each owner. Here are the comments I'll post:

**Comment 1 - For Steven Li (@steven):**
[steven](https://linear.app/bytebase/profiles/steven) Please confirm the following items are accurate:

**Notable Changes:**
- [ ] #1 **CI/CD workflow redesigned** — Following industry practices...

**Bug Fixes:**
- [ ] #10 **Grant request panel** — Fix showing empty user selector...

---

**Comment 2 - For Edward Lu (@ed):**
...

Should I post these [N] owner confirmation comments? (yes/no/edit)
```

Only proceed with `mcp__linear__create_comment` for each owner after user confirms.

#### 9.5 Add Final Confirmation Comments

After adding owner-specific confirmation comments, prepare the final approval comments.

**⚠️ CONFIRM WITH USER BEFORE POSTING:**

```
Finally, I'll add comments requesting overall release note approval:

**Comment for Adela Chen (@adela):**
[adela](https://linear.app/bytebase/profiles/adela) Please review and confirm the overall release notes are ready for publication.

**Comment for Peter Zhu (@pz):**
[pz](https://linear.app/bytebase/profiles/pz) Please review and confirm the overall release notes are ready for publication.

Should I post these final approval comments? (yes/no)
```

Only proceed with `mcp__linear__create_comment` after user confirms.

### Phase 10: Write Draft to File

#### 10.1 Create Release Notes Draft File

**IMPORTANT**: Always write the release notes draft to a file for reference and iteration.

Create the draft file at:
```
docs/release-notes/draft-X.Y.Z.md
```

The file should contain:
1. The full release notes draft (formatted for GitHub release)
2. A metadata section at the bottom with:
   - Version type (minor/patch)
   - Previous version
   - Date generated
   - PR dependency graph
   - Terraform impact table
   - Owner confirmation status

**Example file structure:**
```markdown
# X.Y.Z - Month Day, Year

## 🔔 Notable Changes
...

## 🚀 Features
...

## 🎄 Enhancements
...

## 🐞 Bug Fixes
...

---

**IMPORTANT:** Before upgrading...

---
<!-- DRAFT METADATA (remove before publishing) -->
<!--
Version: X.Y.Z
Previous Version: X.Y.W
Version Type: Minor/Patch
Generated: YYYY-MM-DD
Status: Draft

## Core Architectural Change
[Describe the root cause PR that drives other changes]

## PR Dependency Graph
[Show DAG of related PRs]

## Terraform Impact
| Change | Field | Impact |
|--------|-------|--------|
...

## Owner Confirmation Status
| Section | # | Item | Owner(s) | Confirmed |
|---------|---|------|----------|-----------|
| Notable | 1 | **CI/CD workflow redesigned** — Full description from release notes... | Steven Li, Danny Xu | [ ] |
| Features | 1 | **High Availability (HA)** — Full description from release notes... | Xzavier Zane, Danny Xu | [ ] |
| Bug Fixes | 1 | **PostgreSQL** — Fix SDL rollout failures... | Adrian Lam | [ ] |
...
-->
```

#### 10.2 Update Draft on Each Iteration

When user provides feedback:
1. Update the draft file in place
2. Keep a revision history in git (user can see changes via git diff)
3. Update the confirmation status as owners confirm

### Phase 11: Iteration

If user requests changes:
1. Ask for specific feedback on what needs adjustment
2. Adjust prioritization or wording based on feedback
3. Ensure customer complaints remain prioritized
4. Re-verify Terraform impact if changes affect API/resources
5. Update the draft file in `docs/release-notes/draft-X.Y.Z.md`
6. Maintain format consistency

## Quick Command Reference

```bash
# Find versions
git tag --list "*3.12*" | sort -V
git branch -a | grep release/3.12

# Get commits
git log 3.12.1..origin/release/3.12.2 --oneline --decorate

# Get PR details (CRITICAL - don't rely only on commit messages)
gh pr view <number> --json title,body,labels

# Analyze commits with author (run in parallel)
git show --stat --format='Author: %an <%ae>' <hash1>
git show --stat --format='Author: %an <%ae>' <hash2>

# Check Terraform impact - proto changes
git diff <prev-version>..origin/release/<new-version> -- "proto/v1/*.proto" | head -100

# Find owner by file changes
git log 3.12.1..origin/release/3.12.2 --format='%an' -- backend/api/ | sort | uniq -c | sort -rn

# Research format
# Use WebFetch: https://github.com/bytebase/bytebase/releases/tag/3.12.1
```

## Common Scenarios

### Scenario 1: Large Architectural Change with Many PRs

**Situation**: One Linear issue (e.g., BYT-8521 "Separate CI and CD") spawns 50+ PRs

**Action**:
1. Identify the root cause PR (e.g., #18610 "separate rollout creation from issue creation")
2. Build dependency graph to understand what follows from it
3. Write ONE Notable Change entry describing the architectural shift
4. List user-facing implications as sub-bullets
5. Exclude all follow-up fixes/polish PRs from separate listing

**Example output:**
```markdown
## 🔔 Notable Changes

- **CI/CD workflow redesigned** — The database change workflow is now separated into distinct CI (review) and CD (deployment) phases:
  - **Unified Plan/Issue page** — Plan and Issue shown on single page
  - **Explicit rollout creation** — Rollout created separately after approval
  - **Webhook events changed** — New events: ISSUE_CREATED, PIPELINE_FAILED, etc.
  - **Issue API simplified** — rollout, releasers fields removed
```

### Scenario 2: Fix for Feature in Same Release

**Situation**: PR #18861 "fix: redirect to new UI" fixes PR #18704 "unified page" (both in this release)

**Action**:
1. Don't list #18861 as a separate bug fix
2. It's part of the #18704 feature
3. Only list #18704 in Features section

### Scenario 3: API Change Affecting Terraform

**Situation**: Proto file removes `rollout` field from Issue message

**Action**:
1. Categorize as Notable Changes
2. Add Terraform impact note
3. Include in Terraform impact table in metadata

### Scenario 4: Customer Complaints Mentioned

**Input**: "Customers complained about selector only showing 10 items"

**Action**:
1. Search Linear for related issues (BYT-8525)
2. Find the PR that fixes it (#18538)
3. Prioritize this in the Enhancements section
4. Reference the Linear issue in metadata

## Tool Usage Best Practices

1. **TodoWrite**: Create task list at start, update after each batch
2. **Bash (parallel)**: Run multiple `git show --stat` and `gh pr view` commands simultaneously
3. **gh pr view**: **ALWAYS** fetch PR details, not just commit messages
4. **Linear MCP (get_issue)**: Fetch parent issues to understand feature context
5. **WebFetch**: Fetch previous release notes to learn format
6. **Linear MCP (read)**: Search for customer-reported issues (no confirmation needed)
7. **Linear MCP (write)**: **ALWAYS confirm with user** before creating issues or comments

## Success Criteria

A good release note:
- Has confirmed version (minor vs patch) with appropriate sections
- **Builds PR dependency graph** to identify related changes
- **Excludes internal follow-ups** (fixes for features in this release)
- Addresses all customer-reported issues prominently
- Documents Terraform impact for all applicable changes
- Follows the established format exactly (Notable → Features → Enhancements → Bug Fixes)
- **Includes ALL Notable Changes** (no limit) since they affect existing customers
- Uses consistent present tense
- **Concise and user-focused**: No implementation details, no reasoning
- **Orders items by priority** within each section
- **Infrastructure changes describe user impact**: e.g., "Fix SQL review showing incorrect line numbers"
- **Consolidates related PRs**: Multiple PRs for same feature become one release note item
- Includes owner for each item (multiple owners if consolidated)
- Groups related changes effectively
- Maintains professional, concise tone
- **Draft saved to `docs/release-notes/draft-X.Y.Z.md`** with full metadata
- **Owner confirmation table matches release notes 1:1** - every line item has a row with section number, full text, and owner
- **Linear issue created** with title `<version>-<date>_release_note` (after user confirmation)
- **Confirmation comments use exact text from table** - include section + item number (e.g., "Features #1", "Bug Fixes #12")
- **All Linear write operations confirmed by user** before execution
