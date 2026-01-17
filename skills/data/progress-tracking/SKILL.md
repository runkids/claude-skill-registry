# 📊 Progress Tracking Skill

---
name: progress-tracking
description: Track task progress, visualize completion status, and maintain project momentum
---

## 🎯 Purpose

Track and visualize progress on tasks, features, and projects to maintain momentum and transparency.

## 📋 When to Use

- Starting a new task/project
- During long-running tasks
- Reporting progress to stakeholders
- Managing multiple parallel tasks

## 📝 Progress Format

### Task Checklist
```markdown
## Task: [Task Name]

### Progress: ████████░░ 80%

- [x] Step 1: Setup
- [x] Step 2: Implementation
- [x] Step 3: Testing
- [ ] Step 4: Documentation
- [ ] Step 5: Deploy
```

### Visual Progress Bar
```
Empty:    ░░░░░░░░░░  0%
Quarter:  ███░░░░░░░  25%
Half:     █████░░░░░  50%
3/4:      ████████░░  75%
Complete: ██████████  100%
```

## 📊 Progress Indicators

### Status Emoji
| Status | Emoji | Meaning |
|--------|-------|---------|
| Not Started | ⚪ | Waiting |
| In Progress | 🔵 | Working |
| Blocked | 🔴 | Needs help |
| Review | 🟡 | Pending review |
| Complete | 🟢 | Done |

### Priority Markers
| Priority | Marker | Urgency |
|----------|--------|---------|
| Critical | 🔴 P0 | Immediate |
| High | 🟠 P1 | This sprint |
| Medium | 🟡 P2 | Soon |
| Low | 🟢 P3 | Eventually |

## 🗂️ Project Progress Template

```markdown
# Project: [Name]

## Overall Progress: ██████░░░░ 60%

### Milestones

| Milestone | Status | Due | Progress |
|-----------|--------|-----|----------|
| MVP | 🔵 In Progress | Jan 20 | 75% |
| Beta | ⚪ Not Started | Feb 1 | 0% |
| Launch | ⚪ Not Started | Feb 15 | 0% |

### Current Sprint
- [x] 🟢 Feature A - Complete
- [x] 🟢 Feature B - Complete  
- [ ] 🔵 Feature C - In Progress (80%)
- [ ] ⚪ Feature D - Not Started

### Blockers
- 🔴 Waiting for API credentials
- 🔴 Design review pending
```

## 📈 Metrics to Track

| Metric | Description | Example |
|--------|-------------|---------|
| Completion % | Tasks done / Total | 8/10 = 80% |
| Velocity | Tasks per day | 3 tasks/day |
| Blockers | Number of blocks | 2 blockers |
| Time remaining | Est. time to complete | 2 hours |

## 🔄 Update Workflow

```
Start Task
    │
    ▼
Mark as 🔵 In Progress
    │
    ▼
Update progress % periodically
    │
    ▼
Hit blocker? → Mark 🔴 Blocked
    │
    ▼
Complete → Mark 🟢 Done
    │
    ▼
Update overall project %
```

## 📋 Daily Progress Report

```markdown
## 📅 Daily Progress - [Date]

### Completed Today ✅
- [Task 1]
- [Task 2]

### In Progress 🔵
- [Task 3] - 60% done
- [Task 4] - Started

### Blocked 🔴
- [Issue description]

### Tomorrow's Plan 📋
- [ ] Task 5
- [ ] Task 6
```

## 🔗 Related Skills

- `documentation` - Document progress
- `project-setup` - Define project scope
- `memory-system` - Persist progress state
