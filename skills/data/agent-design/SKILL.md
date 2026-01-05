---
name: agent-design
description: AI agent design and tool-use prompting patterns
sasmp_version: "1.3.0"
bonded_agent: 04-react-pattern-agent
bond_type: PRIMARY_BOND
---

# Agent Design Skill

**Bonded to:** `react-pattern-agent`

---

## Quick Start

```bash
Skill("custom-plugin-prompt-engineering:agent-design")
```

---

## Parameter Schema

```yaml
parameters:
  agent_type:
    type: enum
    values: [react, plan_execute, reflexion, multi_agent]
    default: react

  memory_type:
    type: enum
    values: [none, short_term, long_term, episodic]
    default: short_term

  tool_count:
    type: integer
    range: [1, 20]
    default: 5
```

---

## Agent Architectures

| Architecture | Strengths | Use Case |
|-------------|-----------|----------|
| ReAct | Simple, effective | General tasks |
| Plan-Execute | Structured approach | Complex multi-step |
| Reflexion | Self-improvement | Learning tasks |
| Multi-Agent | Specialization | Large systems |

---

## Core Patterns

### ReAct Agent

```markdown
## Agent Configuration
You are an AI assistant with access to tools.

## Available Tools
[Tool list with descriptions]

## Behavior
1. Think about what to do
2. Take an action using a tool
3. Observe the result
4. Repeat until task complete
```

### Plan-Execute Agent

```markdown
## Planning Phase
1. Analyze the task
2. Break into subtasks
3. Identify tools needed
4. Create execution plan

## Execution Phase
1. Execute each step
2. Validate results
3. Adjust if needed
4. Report completion
```

---

## Tool Definition Template

```yaml
tool:
  name: "tool_name"
  description: "When and why to use this tool"
  parameters:
    param1:
      type: string
      description: "What this parameter does"
      required: true
  returns: "Description of return value"
  errors:
    - "ERROR_TYPE: How to handle"
```

---

## Memory Patterns

```yaml
memory_types:
  working_memory:
    scope: current_conversation
    implementation: context_window

  long_term_memory:
    scope: persistent
    implementation: vector_store

  episodic_memory:
    scope: experience_based
    implementation: structured_logs
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Wrong tool | Vague descriptions | Improve descriptions |
| Loops forever | No exit condition | Add max iterations |
| Forgets context | Memory overflow | Summarize periodically |
| Poor planning | Complex task | Add decomposition step |

---

## References

See agent frameworks: LangChain, AutoGen, CrewAI
