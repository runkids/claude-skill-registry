---
name: create-agent
description: Create specialized subagents for Claude Code with prompts stored in .claude/commands/agent-prompts. Use when the user wants to create a new agent, needs help structuring agents, or mentions creating subagents or specialized agents.
---

# Create Agent Skill

Generate well-structured Claude Code subagents with prompts stored in the commands directory for easy management and version control.

## Overview

This skill helps you create specialized subagents that:
- Store agent definitions in `.claude/agents/`
- Keep detailed prompts in `.claude/commands/agent-prompts/` for better organization
- Follow Claude Code best practices for agent creation
- Support dynamic prompt loading from command files

## Quick Start

To create a new agent:
1. Define the agent's purpose and required tools
2. Create a prompt file in `.claude/commands/agent-prompts/`
3. Generate the agent file that references this prompt
4. Test the agent with a sample task

## Core Instructions

### Agent Creation Workflow

When asked to create an agent, follow these steps:

#### Step 1: Gather Requirements
Ask or determine:
- **Agent name**: Lowercase with hyphens (e.g., `data-analyzer`, `test-generator`)
- **Purpose**: What specific task should this agent handle?
- **Tools needed**: Which tools should the agent have access to? (Read, Write, Bash, Grep, etc.)
- **Model preference**: sonnet (default), opus (complex tasks), or haiku (simple/fast tasks)

#### Step 2: Create the Prompt File

Create a detailed prompt file at `.claude/commands/agent-prompts/{agent-name}.md`:

```markdown
# {Agent Name} Agent

You are a specialized agent for {purpose}.

## Your Responsibilities
- {Primary responsibility 1}
- {Primary responsibility 2}
- {Primary responsibility 3}

## Guidelines
1. {Important guideline}
2. {Important guideline}
3. {Important guideline}

## Workflow
When activated, you should:
1. {Step 1}
2. {Step 2}
3. {Step 3}

## Output Format
{Describe expected output format}

## Examples
{Include relevant examples}
```

#### Step 3: Create the Agent File

Create the agent file at `.claude/agents/{agent-name}.md` that reads and executes the prompt:

```markdown
---
name: {agent-name}
description: {Clear description of when to use this agent and what it does}
tools: {comma-separated list of tools, or omit to inherit all}
model: {sonnet|opus|haiku, or omit for default}
---

# Read and Execute Prompt

Read the detailed instructions from the prompt file and execute them:

{{Read .claude/commands/agent-prompts/{agent-name}.md}}

Follow all instructions, guidelines, and workflows defined in the prompt file above.

## Context Awareness

- Stay focused on your specialized task
- Use only the tools necessary for your responsibilities
- Report back clear, actionable results
- If you encounter blockers, document them clearly
```

#### Step 4: Validate the Agent

Ensure:
- [ ] Prompt file exists in `.claude/commands/agent-prompts/`
- [ ] Agent file exists in `.claude/agents/`
- [ ] YAML frontmatter is valid
- [ ] Name uses lowercase and hyphens only
- [ ] Description clearly explains when to use the agent
- [ ] Tools list is appropriate (or omitted to inherit all)
- [ ] Agent references the correct prompt file

## Templates

### Basic Agent Template

Use for general-purpose agents:

```markdown
---
name: my-agent
description: Description of what this agent does and when to use it
tools: Read, Write, Grep, Glob
model: sonnet
---

# Read and Execute Prompt

Read the detailed instructions from the prompt file and execute them:

{{Read .claude/commands/agent-prompts/my-agent.md}}

Follow all instructions, guidelines, and workflows defined in the prompt file above.
```

### Specialized Tool Agent Template

Use for agents that need specific tools only:

```markdown
---
name: analyzer-agent
description: Analyzes code structure and generates documentation
tools: Read, Grep, Glob, Write
model: sonnet
---

# Read and Execute Prompt

Read the detailed instructions from the prompt file and execute them:

{{Read .claude/commands/agent-prompts/analyzer-agent.md}}

Follow all instructions, guidelines, and workflows defined in the prompt file above.

## Constraints

- Focus only on analysis and documentation
- Do not execute code or make system changes
- Report findings in structured markdown format
```

### Fast Execution Agent Template

Use for simple, fast tasks:

```markdown
---
name: quick-helper
description: Handles quick, straightforward tasks that don't require complex reasoning
tools: Read, Write
model: haiku
---

# Read and Execute Prompt

Read the detailed instructions from the prompt file and execute them:

{{Read .claude/commands/agent-prompts/quick-helper.md}}

Follow all instructions, guidelines, and workflows defined in the prompt file above.
```

## Examples

### Example 1: Code Review Agent

**Prompt file** (`.claude/commands/agent-prompts/code-reviewer.md`):
```markdown
# Code Review Agent

You are a specialized code review agent focused on identifying issues and suggesting improvements.

## Your Responsibilities
- Review code for bugs, security issues, and best practices
- Check for code style consistency
- Suggest performance improvements
- Identify potential edge cases

## Guidelines
1. Be constructive and specific in feedback
2. Prioritize security and correctness over style
3. Provide code examples for suggestions
4. Reference line numbers when pointing out issues

## Workflow
When activated, you should:
1. Read the specified files or changes
2. Analyze code quality, security, and patterns
3. Document findings with severity levels (critical, warning, suggestion)
4. Provide actionable recommendations

## Output Format
Provide findings in this structure:
- **File**: {file path:line}
- **Severity**: {critical|warning|suggestion}
- **Issue**: {description}
- **Recommendation**: {specific fix}
```

**Agent file** (`.claude/agents/code-reviewer.md`):
```markdown
---
name: code-reviewer
description: Reviews code for bugs, security issues, and best practices. Use when the user asks for code review, mentions reviewing changes, or needs quality assessment.
tools: Read, Grep, Glob
model: sonnet
---

# Read and Execute Prompt

Read the detailed instructions from the prompt file and execute them:

{{Read .claude/commands/agent-prompts/code-reviewer.md}}

Follow all instructions, guidelines, and workflows defined in the prompt file above.
```

### Example 2: Documentation Generator Agent

**Prompt file** (`.claude/commands/agent-prompts/doc-generator.md`):
```markdown
# Documentation Generator Agent

You are specialized in creating comprehensive technical documentation.

## Your Responsibilities
- Generate API documentation from code
- Create README files and guides
- Document code architecture and patterns
- Write inline code comments

## Guidelines
1. Use clear, concise language
2. Include code examples
3. Follow markdown best practices
4. Keep documentation up-to-date with code

## Workflow
When activated, you should:
1. Analyze the codebase structure
2. Extract key components and their purposes
3. Generate structured documentation
4. Include usage examples

## Output Format
Use standard markdown with:
- Clear headings hierarchy
- Code blocks with language tags
- Tables for reference information
- Links to related sections
```

**Agent file** (`.claude/agents/doc-generator.md`):
```markdown
---
name: doc-generator
description: Generates technical documentation from code. Use when the user asks to create docs, mentions documentation, or needs README files.
tools: Read, Write, Grep, Glob
model: sonnet
---

# Read and Execute Prompt

Read the detailed instructions from the prompt file and execute them:

{{Read .claude/commands/agent-prompts/doc-generator.md}}

Follow all instructions, guidelines, and workflows defined in the prompt file above.
```

## Advanced Usage

### Multi-Agent Workflows

Create complementary agents that work together:
1. **Analyzer Agent**: Scans code and identifies areas needing work
2. **Implementation Agent**: Makes the actual changes
3. **Testing Agent**: Validates the changes
4. **Documentation Agent**: Updates docs

### Prompt Versioning

Since prompts are in `.claude/commands/agent-prompts/`, you can:
- Version control prompt changes separately
- A/B test different prompt strategies
- Share prompts across team members
- Maintain prompt history

### Dynamic Prompt Selection

For complex agents, you can reference multiple prompt files:

```markdown
# Read and Execute Prompt

Read the base instructions:
{{Read .claude/commands/agent-prompts/my-agent-base.md}}

For specific scenarios, also reference:
- Advanced features: {{Read .claude/commands/agent-prompts/my-agent-advanced.md}}
- Error handling: {{Read .claude/commands/agent-prompts/my-agent-errors.md}}
```

## Tool Access Guidelines

### Common Tool Combinations

- **Analysis agents**: `Read, Grep, Glob`
- **Implementation agents**: `Read, Write, Edit, Bash`
- **Testing agents**: `Read, Bash, Write`
- **Documentation agents**: `Read, Write, Grep, Glob`
- **Full-access agents**: Omit tools field to inherit all tools

### Restricting Tools

Only include necessary tools to:
- Improve agent focus
- Reduce token usage
- Prevent unintended actions
- Increase execution speed

## Best Practices

1. **Clear Naming**: Use descriptive, action-oriented names (e.g., `test-generator` not `helper`)
2. **Specific Descriptions**: Explain exactly when the agent should be used
3. **Detailed Prompts**: Put comprehensive instructions in the prompt file
4. **Minimal Agent Files**: Keep agent files simple - they just load and execute the prompt
5. **Tool Selection**: Only grant tools the agent actually needs
6. **Model Selection**: Use haiku for simple tasks, sonnet for most work, opus for complex reasoning
7. **Testing**: Test agents with real tasks before deploying to team
8. **Documentation**: Document the agent's purpose in both the prompt and agent file

## Troubleshooting

### Agent Not Being Invoked

Check:
- Description clearly states when to use the agent
- Name doesn't conflict with existing agents
- Agent file is in `.claude/agents/` directory

### Prompt Not Loading

Verify:
- Prompt file path is correct in agent file
- File exists at `.claude/commands/agent-prompts/{name}.md`
- No typos in the Read command

### Agent Has Wrong Tools

- Check tools list in YAML frontmatter
- Verify tools are comma-separated
- Consider omitting tools field to inherit all tools

### Performance Issues

- Use haiku model for simple, fast tasks
- Limit tool access to what's needed
- Keep prompts focused and concise
- Break complex agents into multiple specialized agents

## Resources

See templates directory for:
- `basic-agent-template.md`: Standard agent structure
- `specialized-agent-template.md`: Restricted tool agent
- `fast-agent-template.md`: Haiku-based quick agent
- `example-prompt-template.md`: Comprehensive prompt structure

## Related Documentation

- Subagents overview: `https://code.claude.com/docs/en/sub-agents.md`
- Agent Skills: `https://code.claude.com/docs/en/skills.md`
- Tools reference: Check Claude Code documentation for available tools
