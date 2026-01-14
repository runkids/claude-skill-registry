---
name: tdd-workflow
description: Test-Driven Development workflow for task implementation. Use when implementing tasks that require the Red-Green-Refactor cycle, quality gates, commit guidelines, or phase verification protocols.
---

# TDD Workflow

This skill provides the Test-Driven Development methodology used by Conductor for task implementation.

## Guiding Principles

1. **The Plan is the Source of Truth:** All work must be tracked in `plan.md`
2. **The Tech Stack is Deliberate:** Changes to the tech stack must be documented in `tech-stack.md` *before* implementation
3. **Test-Driven Development:** Write unit tests before implementing functionality
4. **High Code Coverage:** Aim for >80% code coverage for all modules
5. **User Experience First:** Every decision should prioritize user experience
6. **Non-Interactive & CI-Aware:** Prefer non-interactive commands. Use `CI=true` for watch-mode tools (tests, linters) to ensure single execution.

## Standard Task Workflow

All tasks follow a strict lifecycle:

### 1. Select Task
Choose the next available task from `plan.md` in sequential order.

### 2. Mark In Progress
Before beginning work, edit `plan.md` and change the task from `[ ]` to `[~]`.

### 3. Write Failing Tests (Red Phase)
- Create a new test file for the feature or bug fix.
- Write one or more unit tests that clearly define the expected behavior and acceptance criteria for the task.
- **CRITICAL:** Run the tests and confirm that they fail as expected. This is the "Red" phase of TDD. Do not proceed until you have failing tests.

### 4. Implement to Pass Tests (Green Phase)
- Write the minimum amount of application code necessary to make the failing tests pass.
- Run the test suite again and confirm that all tests now pass. This is the "Green" phase.

### 5. Refactor (Optional but Recommended)
- With the safety of passing tests, refactor the implementation code and the test code to improve clarity, remove duplication, and enhance performance without changing the external behavior.
- Rerun tests to ensure they still pass after refactoring.

### 6. Verify Coverage
Run coverage reports using the project's chosen tools. Target: >80% coverage for new code.

Example commands by language:
- Python: `pytest --cov=app --cov-report=html`
- JavaScript/TypeScript: `npm test -- --coverage`
- Go: `go test -cover ./...`

### 7. Document Deviations
If implementation differs from tech stack:
- **STOP** implementation
- Update `tech-stack.md` with new design
- Add dated note explaining the change
- Resume implementation

### 8. Commit Code Changes
- Stage all code changes related to the task.
- Propose a clear, concise commit message (e.g., `feat(ui): Create basic HTML structure for calculator`).
- Perform the commit.

### 9. Attach Task Summary with Git Notes
- **Step 9.1:** Get the hash of the just-completed commit (`git log -1 --format="%H"`).
- **Step 9.2:** Draft note content including task name, summary of changes, files modified, and the "why".
- **Step 9.3:** Attach note: `git notes add -m "<note content>" <commit_hash>`

### 10. Get and Record Task Commit SHA
- **Step 10.1:** Read `plan.md`, find the completed task, update status from `[~]` to `[x]`, and append the first 7 characters of the commit hash.
- **Step 10.2:** Write the updated content back to `plan.md`.

### 11. Commit Plan Update
- Stage the modified `plan.md` file.
- Commit with message: `conductor(plan): Mark task '<task_name>' as complete`

## Phase Completion Verification and Checkpointing Protocol

**Trigger:** Execute immediately after completing a task that also concludes a phase in `plan.md`.

### 1. Announce Protocol Start
Inform the user that the phase is complete and verification has begun.

### 2. Ensure Test Coverage for Phase Changes
- **Step 2.1:** Find the Git commit SHA of the previous phase's checkpoint. If none exists, scope is all changes since first commit.
- **Step 2.2:** Execute `git diff --name-only <previous_checkpoint_sha> HEAD` to list files modified during this phase.
- **Step 2.3:** For each code file (excluding `.json`, `.md`, `.yaml`), verify a corresponding test file exists. If missing, create one.

### 3. Execute Automated Tests with Proactive Debugging
- Announce the exact shell command before execution (e.g., "Command: `CI=true npm test`").
- If tests fail, attempt to fix a **maximum of two times**. If still failing, stop and ask for guidance.

### 4. Propose Manual Verification Plan
Generate step-by-step instructions for the user to manually verify the phase.

**Frontend example:**
```
1. Start the development server: `npm run dev`
2. Open browser to: `http://localhost:3000`
3. Confirm you see: The new user profile page with name and email
```

**Backend example:**
```
1. Ensure the server is running
2. Execute: `curl -X POST http://localhost:8080/api/v1/users -d '{"name": "test"}'`
3. Confirm response: JSON with status `201 Created`
```

### 5. Await Explicit User Feedback
Ask: "Does this meet your expectations? Please confirm with yes or provide feedback."
**PAUSE** and await response. Do not proceed without explicit confirmation.

### 6. Create Checkpoint Commit
Stage all changes and commit: `conductor(checkpoint): Checkpoint end of Phase X`

### 7. Attach Verification Report using Git Notes
Draft and attach a detailed verification report including automated test command, manual steps, and user confirmation.

### 8. Get and Record Phase Checkpoint SHA
- Get the checkpoint commit hash.
- Update `plan.md` to append `[checkpoint: <sha>]` to the phase heading.
- Commit: `conductor(plan): Mark phase '<PHASE NAME>' as complete`

### 9. Announce Completion
Inform the user that the phase is complete with verification report attached as git note.

## Quality Gates

Before marking any task complete, verify:

- [ ] All tests pass
- [ ] Code coverage meets requirements (>80%)
- [ ] Code follows project's code style guidelines
- [ ] All public functions/methods are documented
- [ ] Type safety is enforced
- [ ] No linting or static analysis errors
- [ ] Works correctly on mobile (if applicable)
- [ ] Documentation updated if needed
- [ ] No security vulnerabilities introduced

## Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests
- `chore`: Maintenance tasks

### Examples
```bash
git commit -m "feat(auth): Add remember me functionality"
git commit -m "fix(posts): Correct excerpt generation for short posts"
git commit -m "test(comments): Add tests for emoji reaction limits"
```

## Definition of Done

A task is complete when:

1. All code implemented to specification
2. Unit tests written and passing
3. Code coverage meets project requirements
4. Documentation complete (if applicable)
5. Code passes all configured linting and static analysis checks
6. Works beautifully on mobile (if applicable)
7. Implementation notes added to `plan.md`
8. Changes committed with proper message
9. Git note with task summary attached to the commit
