---
name: ci-pipeline-manager
description: "Manage CI pipelines. Use when: Testing pipeline error handling, recovery, or complex dependencies. Not for: Simple linear scripts or unit testing individual tasks."
context: fork
---

# CI Pipeline Error Recovery Testing

Test TaskList error handling and recovery behavior with CI pipelines.

## Pipeline Architecture

<logic_flow>
digraph Pipeline {
    rankdir=LR;
    node [shape=box];
    Tests [label="1. run-tests"];
    Build [label="2. build"];
    Deploy [label="3. deploy"];
    Cleanup [label="4. cleanup-on-failure" style=filled fillcolor=lightgrey];

    Tests -> Build [label="Pass"];
    Build -> Deploy [label="Success"];
    Tests -> Cleanup [label="Fail"];
    
    {rank=same; Tests; Cleanup}
}
</logic_flow>

**Four-task pipeline with error handling:**

1. **run-tests** - Execute test suite
   - Simulates test failure for validation
   - Failure: blocks all downstream tasks
   - Output: Test results (simulated failure)

2. **build** - Compile application
   - BLOCKED by: run-tests
   - Should NOT run if tests fail
   - Output: Build artifact or "SKIPPED"

3. **deploy** - Deploy to staging
   - BLOCKED by: build
   - Should NOT run if build doesn't happen
   - Output: Deployment status or "SKIPPED"

4. **cleanup-on-failure** - Cleanup resources
   - BLOCKED by: run-tests (triggers when run-tests completes)
   - MUST execute even when tests fail
   - Output: Cleanup completion status

## Execution Workflow

**Execute autonomously:**

1. **Create TaskList** with all four tasks
2. **Set up blocking dependencies:**
   - build blocked_by: ["run-tests"]
   - deploy blocked_by: ["build"]
   - cleanup-on-failure blocked_by: ["run-tests"]
3. **Simulate test failure** in run-tests task
4. **Verify behavior:**
   - build: blocked by failed run-tests → SKIPPED
   - deploy: build never ran → SKIPPED
   - cleanup-on-failure: MUST execute despite failure
5. **Report task states** and pipeline status

**Recognition test:** Cleanup-on-failure should always execute, even when run-tests fails.

## Expected Output

```
CI Pipeline: RUNNING
[task-id] run-tests: IN_PROGRESS -> FAILED
[task-id] build: BLOCKED -> SKIPPED (dependency failed)
[task-id] deploy: BLOCKED -> SKIPPED (dependency never ran)
[task-id] cleanup-on-failure: BLOCKED -> IN_PROGRESS -> COMPLETE

Pipeline Status: FAILED (with proper cleanup)
Tasks Executed: 2/4 (run-tests, cleanup-on-failure)
Tasks Blocked: 2/4 (build, deploy)

Error Handling: PASS
Cleanup: PASS
```

## Validation Criteria

- Failed task blocked dependents
- Cleanup executed despite failure

**Binary check:** "Proper error handling?" → Both criteria must pass.
