---
name: instrumentation-planning
description: Plan what to measure in AI agent systems using tiered approach
triggers:
  - "what should I measure"
  - "planning agent telemetry"
  - "observability strategy"
  - "what to instrument"
priority: 1
---

# Instrumentation Planning for Agents

Plan agent observability using a tiered, outcome-focused approach.

## Core Principle

Every metric and span should answer one of these questions:
1. **Did the agent complete its task?** (success/failure)
2. **How long did it take?** (latency)
3. **How much did it cost?** (tokens/money)
4. **Why did it fail?** (error context)
5. **What decisions did it make?** (reasoning trace)

## 5-Tier Implementation Framework

### Tier 0: Foundation (Day 1)
Essential observability to ship any agent:
- SDK initialization
- Root span for agent runs
- Unhandled error capture
- Basic success/failure status

### Tier 1: Core Tracing (Week 1)
Understand agent execution:
- LLM call spans (model, latency)
- Tool execution spans (name, result)
- Agent loop iterations
- Retry attempts

### Tier 2: Context & Attribution (Week 2)
Track costs and ownership:
- Token counts (input/output/total)
- Cost per call (USD)
- User/session context
- Feature/workflow attribution

### Tier 3: Multi-Agent Coordination (Week 3)
For multi-agent systems:
- Parent-child span relationships
- Agent handoff tracking
- Delegation reasoning
- Supervisor decisions

### Tier 4: Evaluation & Quality (Month 1)
Measure agent quality:
- Response quality scores
- Human feedback capture
- Automated eval results
- Hallucination detection signals

## What NOT to Instrument

- Full prompt/response content (PII, storage cost)
- Every intermediate thought (noise)
- Timestamps as attributes (use span timing)
- User-provided secrets

## Span Naming Convention

Use semantic, hierarchical names:
```
agent.run              # Root agent execution
agent.think            # Reasoning step
llm.call               # LLM API call
llm.stream             # Streaming LLM call
tool.execute           # Tool execution
tool.validate          # Tool input validation
retrieval.search       # RAG retrieval
retrieval.rerank       # Reranking step
memory.read            # Memory fetch
memory.write           # Memory store
handoff.delegate       # Agent delegation
handoff.receive        # Receiving delegation
human.request          # Human approval request
human.response         # Human response received
eval.score             # Evaluation scoring
```

## Attribute Naming Convention

Use dot-notation, consistent types:
```
# Agent context
agent.name             # string: "researcher"
agent.type             # string: "langgraph"
agent.run_id           # string: UUID

# LLM context
llm.model              # string: "claude-3-opus"
llm.provider           # string: "anthropic"
llm.temperature        # float: 0.7
llm.tokens.input       # int: 1500
llm.tokens.output      # int: 350
llm.tokens.total       # int: 1850
llm.cost_usd           # float: 0.025
llm.latency_ms         # int: 2340

# Tool context
tool.name              # string: "web_search"
tool.success           # bool: true
tool.error             # string: error message
tool.latency_ms        # int: 450

# User context
user.id                # string: hash or ID
session.id             # string: session UUID
```

## Sampling Strategy

For high-volume agents:
- **100%**: Errors, slow requests (>P95), human escalations
- **10-25%**: Normal successful runs
- **1%**: High-frequency background tasks

Configure sampling at SDK level, not in code.

## Related Skills
- `llm-call-tracing` - LLM instrumentation details
- `tool-call-tracking` - Tool execution patterns
- `token-cost-tracking` - Cost calculation methods
