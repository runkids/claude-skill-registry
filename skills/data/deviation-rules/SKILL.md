---
name: deviation-rules
description: "Handle unexpected work during execution. Use when: You encounter bugs, missing critical features, blockers, or potential architectural changes while executing a plan. Not for: Initial planning or non-execution contexts."
disable-model-invocation: false
allowed-tools: ["Read", "Write", "Edit", "Bash", "AskUserQuestion"]
---

# Deviation Rules Engine

Automatic handling of discovered work during plan execution with clear rules and full transparency.

## What This Skill Does

Apply deviation rules when encountering unexpected work during plan execution:

1. **Auto-fix bugs** - Fix bugs discovered during implementation
2. **Add missing critical** - Add critical functionality that was overlooked
3. **Fix blockers** - Resolve blocking issues preventing completion
4. **Ask about architectural changes** - Stop and ask for major structural changes
5. **Log enhancements** - Log non-critical improvements for later

**Key Innovation**: Handle real-world complexity automatically while maintaining full transparency.

## When to Use

Use deviation rules when:
- Executing plans and discovering additional work
- Encountering bugs in existing code
- Finding missing critical functionality
- Facing blocking issues
- Considering architectural changes

## The 5 Deviation Rules

### Rule 1: Auto-Fix Bugs

**Definition**: Fix any bugs discovered during implementation without asking.

**What counts as a bug**:
- Logic errors in existing code
- Syntax errors that prevent execution
- Type errors that would cause runtime failures
- Security vulnerabilities in existing implementations
- Performance issues in critical paths

**When to apply**:
- Bug is discovered while implementing plan
- Bug fix doesn't change architecture
- Bug fix is unambiguous (clear solution exists)

**Example**:
```
Plan: "Add user authentication"
Discovery: Existing password hashing uses MD5 (insecure)
Action: Fix to use bcrypt without asking
Reason: Security fix, unambiguous solution
```

**Recognition**: "Is this a bug with a clear fix that doesn't change architecture?"

### Rule 2: Add Missing Critical

**Definition**: Add critical functionality that was clearly overlooked in planning.

**What counts as missing critical**:
- Error handling that would cause crashes
- Input validation required for security
- Logging needed for debugging
- Configuration for required functionality
- Dependencies required for operation

**When to apply**:
- Functionality is essential for task completion
- Not adding it would make the implementation non-functional
- Solution is straightforward and unambiguous

**Example**:
```
Plan: "Create API endpoint"
Discovery: No error handling for database failures
Action: Add error handling middleware without asking
Reason: Critical for operation, unambiguous implementation
```

**Recognition**: "Is this essential for functionality that was clearly overlooked?"

### Rule 3: Fix Blockers

**Definition**: Resolve any blocking issues that prevent task completion.

**What counts as a blocker**:
- Missing dependencies that prevent execution
- Configuration issues preventing testing
- Environment setup problems
- File permissions blocking operations
- Network/connectivity issues for required services

**When to apply**:
- Issue blocks progress on planned work
- Resolution is necessary to continue
- Solution doesn't require architectural decision

**Example**:
```
Plan: "Deploy to production"
Discovery: Environment variables not set in production
Action: Set environment variables from documentation
Reason: Blocks deployment, required configuration
```

**Recognition**: "Does this block progress and have an unambiguous fix?"

### Rule 4: Ask About Architectural Changes

**Definition**: STOP and ask user before making any architectural changes.

**What counts as architectural**:
- Changing file/folder structure
- Adding/removing major components
- Changing data models or schemas
- Modifying system boundaries
- Changing patterns or frameworks
- Altering deployment architecture

**When to apply**:
- Change affects system structure
- Change has multiple valid approaches
- Change would require updating other components
- Change conflicts with existing patterns

**Example**:
```
Plan: "Add user preferences"
Discovery: Current data model doesn't support user-specific settings
Action: STOP and ask user about data model approach
Reason: Architectural decision, multiple valid options
```

**Recognition**: "Does this change the system structure or have multiple valid approaches?"

### Rule 5: Log Enhancements

**Definition**: Log non-critical improvements for later consideration.

**What counts as enhancements**:
- Code refactoring for clarity
- Adding convenience features
- Performance optimizations (non-critical)
- Documentation improvements
- Test coverage expansions

**When to apply**:
- Improvement is valuable but not essential
- Enhancement doesn't block current work
- Can be deferred without impact

**Example**:
```
Plan: "Add payment processing"
Discovery: Error messages could be more user-friendly
Action: Log to SUMMARY.md as enhancement
Reason: Nice to have, not essential for completion
```

**Recognition**: "Is this valuable but not essential for current task?"

## SUMMARY.md Documentation

All deviations are documented in `SUMMARY.md`:

```markdown
# Execution Summary

## Original Plan
[Original plan description]

## Deviations Log

### Auto-Fixed Bugs
- [Bug description] → [Fix applied]
- [Bug description] → [Fix applied]

### Added Missing Critical
- [Missing functionality] → [What was added]

### Fixed Blockers
- [Blocker] → [Resolution]

### Logged Enhancements
- [Enhancement idea] (deferred)
- [Enhancement idea] (deferred)

## Architectural Decisions
[Only if Rule 4 was triggered]
- [Decision point] → [User's decision]
```

**Recognition**: "Is every deviation documented for transparency?"

## Application Workflow

### During Execution

When encountering unexpected work:

<router>
flowchart TD
    Start([Unexpected Work]) --> Type{Classify Type}
    Type -- Bug --> Rule1[Rule 1: Auto-Fix]
    Type -- Missing Critical --> Rule2[Rule 2: Add Critical]
    Type -- Blocker --> Rule3[Rule 3: Fix Blocker]
    Type -- Architectural --> Rule4[Rule 4: Ask User]
    Type -- Enhancement --> Rule5[Rule 5: Log It]
    
    Rule1 --> Doc[Document in SUMMARY.md]
    Rule2 --> Doc
    Rule3 --> Doc
    Rule4 --> Wait[Wait for Decision]
    Rule5 --> Doc
    
    Doc --> Continue[Continue Execution]
    Wait --> Continue
</router>

1. **Classify the deviation type**

2. **Apply the appropriate rule**
   - Execute the rule's action
   - Document in SUMMARY.md
   - Continue execution (or wait for user if Rule 4)

3. **Continue with plan**
   - Return to planned work
   - Update task status if needed

### Example Execution

```
Original Plan: Add JWT authentication to API

During Implementation:
1. Discovery: Password hashing uses MD5
   → Rule 1 (Bug): Fix to bcrypt
   → Document: Fixed insecure MD5 hashing

2. Discovery: No error handling for database failures
   → Rule 2 (Missing Critical): Add error handling
   → Document: Added error handling for database operations

3. Discovery: User model doesn't have email field
   → Rule 4 (Architectural): STOP and ask user
   → Wait for user decision on data model

4. Discovery: Token expiration check could be more efficient
   → Rule 5 (Enhancement): Log for later
   → Document: Deferred: Optimize token validation

Result: Authentication complete with documented deviations
```

## Recognition Questions

Before applying any rule, ask:

**Rule 1 (Bugs)**:
- "Is this a bug with a clear, unambiguous fix?"
- "Does the fix preserve the intended architecture?"

**Rule 2 (Missing Critical)**:
- "Is this essential for functionality?"
- "Was this clearly overlooked, not a new feature?"
- "Is the implementation straightforward?"

**Rule 3 (Blockers)**:
- "Does this block progress?"
- "Is there an unambiguous resolution?"

**Rule 4 (Architectural)**:
- "Does this change system structure?"
- "Are there multiple valid approaches?"
- "Would other components be affected?"

**Rule 5 (Enhancements)**:
- "Is this valuable but not essential?"
- "Can this be deferred without impact?"

## Best Practices

### Transparency
- Document EVERY deviation in SUMMARY.md
- Explain WHY each deviation was necessary
- Note what was done vs what was planned

### Judgement
- Be conservative with Rule 4 (when in doubt, ask)
- Be generous with Rule 2 (err on side of completeness)
- Be honest with Rule 5 (log real improvements, don't ignore)

### Context
- Consider project size and complexity
- Consider team practices and standards
- Consider long-term maintenance impact

## Common Mistakes

**❌ Wrong**: Treating every unexpected item as architectural (Rule 4)
**✅ Correct**: Only Rule 4 for structural changes with multiple valid approaches

**❌ Wrong**: Ignoring enhancements because they're not in the plan
**✅ Correct**: Log enhancements (Rule 5) for future consideration

**❌ Wrong**: Not documenting deviations
**✅ Correct**: Always document to SUMMARY.md for transparency

**❌ Wrong**: Making architectural assumptions without asking
**✅ Correct**: Rule 4 triggers user consultation for architecture decisions

## Integration with Planning

Deviation rules integrate with planning systems:

- **TDD Workflow**: Handle bugs found during test writing
- **Component Creation**: Add missing critical during implementation
- **Ralph/Orchestrate**: Automatic deviation handling during execution

## Related Skills

This skill integrates with:
- `tdd-workflow` - Test-driven development with deviation handling
- `skill-development` - Component creation with automatic fixes
- `/orchestrate` - Native orchestration with deviation rules

## Arguments

This skill is loaded automatically during plan execution. No direct invocation needed.

**Manual invocation** (for reference/testing):
```
Skill: deviation-rules
Args: [deviation description] [rule to apply]
```

## Example Use Cases

### Use Case 1: API Development
```
Plan: "Add user profile endpoint"
Deviation 1: No input validation → Rule 2 (add validation)
Deviation 2: Database query vulnerable to SQL injection → Rule 1 (fix bug)
Deviation 3: Response format inconsistent → Rule 4 (ask about standard)
```

### Use Case 2: Frontend Component
```
Plan: "Create dashboard widget"
Deviation 1: Missing loading state → Rule 2 (add critical)
Deviation 2: Could use animations → Rule 5 (log enhancement)
Deviation 3: Color system doesn't support theme → Rule 4 (ask about theming)
```

### Use Case 3: Infrastructure
```
Plan: "Set up CI/CD pipeline"
Deviation 1: Docker build fails → Rule 3 (fix blocker)
Deviation 2: No test coverage reporting → Rule 2 (add critical)
Deviation 3: Could add deployment previews → Rule 5 (log enhancement)
```

**Trust intelligence** - Deviation rules enable automatic handling of real-world complexity while maintaining transparency and architectural integrity.
