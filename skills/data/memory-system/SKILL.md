# 🧠 Memory System Skill

---
name: memory-system
description: Manage AI context, memory persistence, and knowledge retention across sessions
---

## 🎯 Purpose

Maintain context and knowledge across conversations, enabling continuity and learning from past interactions.

## 📋 When to Use

- Starting new conversations (load context)
- Completing tasks (save learnings)
- Switching between projects
- Referencing past decisions

## 🗂️ Memory Structure

```
📁 memory/
├── 📄 active.md       ← Current task context
├── 📄 summary.md      ← Project summaries
├── 📄 decisions.md    ← Architecture decisions
├── 📄 changelog.md    ← Changes history
├── 📄 patterns.md     ← Reusable patterns
├── 📄 snippets.md     ← Code templates
└── 📄 lessons.md      ← Learnings from mistakes
```

## 📝 Memory Types

### 1. Short-term Memory (Session)
- Current task context
- Recent files edited
- Active decisions

### 2. Long-term Memory (Persistent)
- Project architecture
- Design decisions
- Lessons learned
- Code patterns

### 3. Episodic Memory (Events)
- Bug fixes and solutions
- Feature implementations
- Deployment records

## 🔧 Memory Operations

### Save Memory
```markdown
## Save Format

### Context
- Project: [name]
- Date: [ISO date]
- Task: [description]

### Key Decisions
1. [Decision 1]: [Rationale]
2. [Decision 2]: [Rationale]

### Lessons Learned
- [Lesson 1]
- [Lesson 2]

### Code Patterns Used
- [Pattern]: [File reference]
```

### Load Memory
```markdown
## Load Checklist

1. [ ] Read project context.md
2. [ ] Check active.md for ongoing tasks
3. [ ] Review recent decisions.md entries
4. [ ] Load relevant patterns
```

### Search Memory
```markdown
## Search Methods

1. Keyword search in solutions.md
2. Date-based filtering
3. Project-specific lookup
4. Tag-based retrieval
```

## 📊 Memory Metrics

| Metric | Description |
|--------|-------------|
| Context loaded | Files read at session start |
| Decisions made | Architecture choices recorded |
| Patterns saved | Reusable code patterns |
| Lessons recorded | Mistakes and learnings |

## 🔄 Memory Lifecycle

```
┌─────────────┐
│ Session     │
│ Start       │──▶ LOAD context from memory files
└─────────────┘
       │
       ▼
┌─────────────┐
│ During      │
│ Work        │──▶ UPDATE active.md with progress
└─────────────┘
       │
       ▼
┌─────────────┐
│ Task        │
│ Complete    │──▶ SAVE learnings to appropriate files
└─────────────┘
       │
       ▼
┌─────────────┐
│ Session     │
│ End         │──▶ SUMMARIZE session in summary.md
└─────────────┘
```

## 💡 Best Practices

1. **Be Specific**: Save context with enough detail to understand later
2. **Use Tags**: Add searchable tags to entries
3. **Link Related**: Reference related decisions/patterns
4. **Prune Regularly**: Archive old, irrelevant entries
5. **Keep Active Current**: Update active.md frequently

## 🔗 Related Skills

- `session-recovery` - Recover from session interruptions
- `documentation` - Document decisions properly
- `progress-tracking` - Track ongoing work
