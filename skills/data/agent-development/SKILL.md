---
name: agent-development
description: "Create autonomous agents. Use when: You need an isolated subprocess with its own context and philosophy for distributed execution. Not for: Simple logic reuse (use skill-development) or human-orchestrated workflows (use command-development)."
---

# Agent Development

Agents are specialized autonomous subprocesses that execute tasks independently with isolated context. Unlike skills (which are invoked within the same conversation), agents run in separate processes with their own conversation context.

**Core principle**: Agents must be autonomous, isolated, and carry their own philosophy for self-guided execution.

---

## What Agents Are

Agents provide:

- **Autonomous execution**: Run independently without supervision
- **Isolated context**: Separate conversation and memory
- **Distributed processing**: Parallel task execution
- **Specialized capabilities**: Domain-specific functionality
- **Bundled philosophy**: Self-contained behavioral guidance

### Agent vs Skill vs Command

- **Agents**: Autonomous subprocesses (isolated execution)
- **Skills**: Contextual capabilities (in-conversation use)
- **Commands**: Human-invoked orchestrators (explicit triggers)

---

## Core Structure

### Frontmatter

```yaml
---
name: agent-name
description: Autonomous agent for specific task domain
mode: default
team_name: team-context
---
```

### Agent Body

- **Autonomous capability**: What the agent does independently
- **Isolation requirements**: What context it needs
- **Trigger conditions**: When to spawn this agent
- **Communication patterns**: How it reports progress
- **Philosophy bundle**: Behavioral guidance for isolation

### Critical Fields

**mode**: Execution mode

- `default`: Standard autonomous execution
- `plan`: Requires plan approval before execution
- `delegate`: Accepts delegated tasks
- `bypassPermissions`: Skips permission checks (dangerous)

**team_name**: Context identifier for multi-agent coordination

---

## Best Practices

### Autonomy

- Self-contained decision making
- No dependency on caller for implementation details
- Autonomous error handling and recovery
- Independent progress reporting

### Isolation

- Bundle all necessary context (no external references)
- Include philosophy for self-guidance
- Provide success criteria for validation
- Ensure portable operation

### Spawning Decisions

**Use agents when:**

- Task requires isolation (untrusted code, parallel execution)
- Long-running operations (>30 minutes)
- Independent subprocess needed
- Context fork required for safety

**Use skills when:**

- Same-conversation execution is sufficient
- Quick task (<5 minutes)
- No isolation needed
- Context sharing is beneficial

### Quality

- Imperative form for instructions
- Clear autonomous capabilities
- Progressive disclosure (core → details)
- Self-validation mechanisms

### Agent Communication

- Report progress to parent context
- Provide completion status
- Share errors and blockers
- Enable parent oversight

---

## Navigation

| If you need...       | Reference                                    |
| -------------------- | -------------------------------------------- |
| System prompt design | `references/system-prompt-design.md`         |
| Triggering examples  | `references/triggering-examples.md`          |
| Agent orchestration  | `references/agent-orchestration.md`          |
| Iterative retrieval  | `references/iterative-retrieval.md`          |
| Creation workflow    | `references/agent-creation-system-prompt.md` |
