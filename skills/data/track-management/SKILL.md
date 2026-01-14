---
name: track-management
description: Track lifecycle management patterns. Use when creating tracks, updating track status, generating track IDs, parsing plan files, or managing track metadata.
---

# Track Management

This skill provides patterns for managing Conductor tracks throughout their lifecycle.

## Track ID Generation

### Format
Track IDs follow the pattern: `shortname_YYYYMMDD`

### Rules
1. Derive shortname from track description (lowercase, underscores, no special characters)
2. Use current date in YYYYMMDD format
3. Keep shortname concise (2-4 words max)

### Examples
- "Add user authentication" → `user_auth_20260110`
- "Fix login page bug" → `login_bug_20260110`
- "Create dashboard UI" → `dashboard_ui_20260110`

## Status Markers

Conductor uses checkbox-style markers to track status:

| Marker | Status | Description |
|--------|--------|-------------|
| `[ ]` | Pending | Not yet started |
| `[~]` | In Progress | Currently being worked on |
| `[x]` | Completed | Finished successfully |

### Usage in tracks.md
```markdown
- [ ] **Track: Add user authentication**
- [~] **Track: Create dashboard UI**
- [x] **Track: Fix login bug**
```

### Usage in plan.md
```markdown
# Phase 1: Setup

- [x] Task: Initialize project structure
    - [x] Create directory layout
    - [x] Set up package.json
- [~] Task: Configure testing framework
    - [x] Install Jest
    - [ ] Write initial test
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Setup' (Protocol in workflow.md)
```

## Track File Structure

Each track is stored in `conductor/tracks/<track_id>/` with these files:

```
conductor/tracks/<track_id>/
├── metadata.json    # Track metadata
├── spec.md          # Feature specification
└── plan.md          # Implementation plan
```

## Metadata Schema

The `metadata.json` file contains:

```json
{
  "track_id": "user_auth_20260110",
  "type": "feature",
  "status": "new",
  "created_at": "2026-01-10T14:30:00Z",
  "updated_at": "2026-01-10T14:30:00Z",
  "description": "Add user authentication with login and registration"
}
```

### Fields

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `track_id` | string | - | Unique identifier |
| `type` | string | `feature`, `bug`, `chore`, `refactor` | Category of work |
| `status` | string | `new`, `in_progress`, `completed`, `cancelled` | Current state |
| `created_at` | string | ISO 8601 datetime | Creation timestamp |
| `updated_at` | string | ISO 8601 datetime | Last update timestamp |
| `description` | string | - | Brief description |

## Plan Parsing

### Reading Tasks
When parsing `plan.md`:

1. Look for phase headings (e.g., `# Phase 1: Setup`)
2. Find task lines matching `- [ ] Task:` or `- [~] Task:` or `- [x] Task:`
3. Find sub-tasks indented under tasks (4 spaces): `    - [ ] ...`

### Extracting Status
```
Line: "- [~] Task: Configure testing framework"
Status: in_progress
Task: "Configure testing framework"
```

### Finding Commit SHAs
Completed tasks may have commit SHAs appended:
```
- [x] Task: Initialize project (abc1234)
```
Extract SHA: `abc1234`

### Phase Checkpoints
Completed phases have checkpoint markers:
```
# Phase 1: Setup [checkpoint: def5678]
```

## tracks.md Format

The main tracks file (`conductor/tracks.md`) lists all tracks:

```markdown
# Project Tracks

This file tracks all major tracks for the project. Each track has its own detailed plan in its respective folder.

---

- [ ] **Track: Add user authentication**
  *Link: [./conductor/tracks/user_auth_20260110/](./conductor/tracks/user_auth_20260110/)*

---

- [~] **Track: Create dashboard UI**
  *Link: [./conductor/tracks/dashboard_ui_20260110/](./conductor/tracks/dashboard_ui_20260110/)*
```

### Parsing tracks.md
1. Split content by `---` separator
2. For each section, find:
   - Status marker: `- [ ]`, `- [~]`, or `- [x]`
   - Description: Text after `**Track:` and before `**`
   - Link: Path in `*Link: [...](...)*`

## Track Lifecycle

### 1. Creation
- Generate unique track ID
- Create directory structure
- Write metadata.json, spec.md, plan.md
- Add entry to tracks.md

### 2. Implementation
- Update tracks.md status to `[~]`
- Execute tasks from plan.md
- Update plan.md as tasks complete
- Commit changes with git notes

### 3. Completion
- Update tracks.md status to `[x]`
- Synchronize project documentation
- Offer archive/delete options

### 4. Archive (Optional)
- Move track folder to `conductor/archive/`
- Remove entry from tracks.md
- Commit changes

### 5. Delete (Optional)
- Permanently delete track folder
- Remove entry from tracks.md
- Commit changes

## Duplicate Prevention

Before creating a new track:

1. List existing tracks in `conductor/tracks/`
2. Extract shortnames from existing track IDs
3. If proposed shortname matches an existing one, halt and suggest alternatives

Example check:
```bash
ls conductor/tracks/
# Output: user_auth_20260108  dashboard_ui_20260109

# If user wants "user_auth", warn that it already exists
```
