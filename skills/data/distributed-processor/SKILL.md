---
name: distributed-processor
description: "Coordinate distributed processing. Use when: You need parallel execution, forked skills, or isolated work units. Not for: Sequential tasks or single-threaded workflows."
context: fork
---

# Distributed Data Processing

Coordinate distributed data processing using TaskList with forked skills.

## Processing Architecture

**Three-component system:**
- **Coordinator** uses TaskList to track all processing tasks
- **Region processors** are forked skills with complete isolation
- **Results flow back** to coordinator for aggregation

## Processing Tasks

**Parallel, independent execution:**

1. **process-region-a** - Process data from Region A
   - Forked skill processes in isolation

2. **process-region-b** - Process data from Region B
   - Forked skill processes in isolation

3. **process-region-c** - Process data from Region C
   - Forked skill processes in isolation

4. **aggregate-results** - Combine all processed outputs
   - Wait for all region processors to complete
   - Aggregate results into final dataset

## Execution Workflow

**Execute autonomously:**

1. **Create TaskList** with all tasks
2. **Use Skill tool** with context: fork for each region processor
3. **Monitor task completion**
4. **Aggregate results** when all processors complete
5. **Return aggregated dataset**

**Recognition test:** Each region processor runs in complete isolation with no shared state.

## Expected Output

```
Distributed Processing: COORDINATING
[task-id] process-region-a: IN_PROGRESS -> COMPLETE
[task-id] process-region-b: IN_PROGRESS -> COMPLETE
[task-id] process-region-c: IN_PROGRESS -> COMPLETE
[task-id] aggregate-results: BLOCKED -> IN_PROGRESS -> COMPLETE

=== AGGREGATED RESULTS ===
Region A: [records processed, summary]
Region B: [records processed, summary]
Region C: [records processed, summary]

Total: [combined statistics]
```

## Validation Criteria

- Parallel execution of regions
- Results aggregation after completion

**Binary check:** "Proper distributed processing?" → Both criteria must pass.
