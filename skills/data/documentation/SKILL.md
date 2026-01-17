---
name: documentation
description: Guide for writing concise, direct documentation. Use this skill when the user asks to document code, write docstrings, create or improve READMEs, write API documentation, or add comments. Triggers on requests involving "documentation", "docs", "document this", or similar.
---

# Documentation

## Core Principles

Apply these to all documentation types:

1. **Lead with purpose.** First sentence answers "what does this do?" not "how does it work?"
2. **Skip the obvious.** If code shows it, don't document it. `getUserById(id)` doesn't need a description.
3. **Imperative voice.** "Returns X" not "This function returns X". "Creates a new user" not "This method is used to create a new user".
4. **One concept per sentence.** Break complex ideas into separate statements.
5. **Examples when essential.** Only include code examples if usage isn't clear from the signature/interface.
6. **Match docs to code.** When docs and code disagree, update the docs (unless explicitly told otherwise).
7. **Mermaid over ASCII.** Use mermaid code blocks for diagrams, not ASCII art.

## By Doc Type

### Code Docs (docstrings, inline comments)

- Document **why** and **what**, not **how**
- Skip getters, setters, and obvious CRUD methods
- Parameters: only document when type or purpose isn't obvious from name
- Returns: only document when not obvious from function name
- Inline comments: explain intent behind non-obvious logic, not what code does line-by-line

```python
# Good
def retry_with_backoff(fn, max_attempts=3):
    """Retry fn with exponential backoff. Raises last exception after max_attempts."""

# Bad
def retry_with_backoff(fn, max_attempts=3):
    """
    This function retries a given function with exponential backoff.

    Args:
        fn: The function to retry
        max_attempts: The maximum number of attempts (default 3)

    Returns:
        The result of the function call

    Raises:
        Exception: If all retry attempts fail
    """
```

### Standalone Docs (READMEs, guides, overviews)

Structure (include only sections with content):

1. **Title + one-line description**
2. **TL;DR** - Core concept or summary in 2-3 sentences
3. **Installation** - Copy-paste commands (if applicable)
4. **Usage** - Common patterns, brief
5. **Configuration** - Options that users actually change
6. **Details** - Architecture, contributing, license (at bottom)

Skip empty sections. Don't add "Contributing" if there are no contribution guidelines.

### API Documentation

- Request/response example before parameter lists
- Keep endpoint descriptions to one line when possible
- Document error responses - users need these
- Group related endpoints together

```markdown
## Create User
POST /users

Creates a new user account.

**Example:**
POST /users
{"email": "user@example.com", "name": "Jane"}

→ 201 {"id": "abc123", "email": "user@example.com", "name": "Jane"}

**Errors:**
- 400: Invalid email format
- 409: Email already registered
```

## Workflows

Reference these step-by-step workflows based on the task:

- **Writing new docs:** Read `references/writing-new-docs.md` when creating documentation from scratch
- **Updating existing docs:** Read `references/updating-docs.md` when modifying documentation that already exists

## Verification

Before finalizing documentation, review each item and ask:

1. **Does this add information beyond what the code expresses?** Remove comments that restate code (`// increment counter` above `counter++`).
2. **Is this explaining standard behavior?** Remove explanations of standard library functions the reader already knows.
3. **Is this a real concern or speculation?** Remove caveats about edge cases that don't occur in practice.
4. **Does this TODO have context?** Remove or complete TODOs lacking context or ownership.
5. **Is the length proportional to complexity?** Condense multi-paragraph descriptions of simple functions to one line.
