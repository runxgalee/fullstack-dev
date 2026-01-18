---
description: Interactive skill creation workflow with guided prompts, templates, and best practices enforcement. Supports context fork, allowed-tools, and agent specification.
---

## Task

Use the create-skill skill to create a new Claude Code skill with an interactive, guided workflow.

The create-skill skill provides:
- Guided prompts for skill name, description, and functionality
- Template selection based on skill complexity and purpose
- Best practices enforcement for skill structure and documentation
- Automatic plugin category determination
- File creation in appropriate plugin directories
- Symlink creation in .claude/skills/
- Comprehensive documentation with examples
- Validation of skill structure
- README.md updates
- **Advanced frontmatter support:**
  - `context: fork` - Run skill in isolated sub-agent context
  - `allowed-tools` - Restrict available tools for the skill
  - `agent` - Specify which agent type executes the skill

### Process

1. Invoke the create-skill skill using the Skill tool
2. Follow the interactive prompts to define your skill
3. **Choose advanced features if needed:**
   - Should the skill run in a forked context? (for research/exploration)
   - Should specific tools be restricted? (for security/simplicity)
   - Should a specialist agent handle this? (for domain expertise)
4. Review the generated skill structure
5. Validate and deploy the skill

### Advanced Frontmatter Reference

```yaml
---
name: my-skill
description: Skill description with trigger keywords
context: fork           # Optional: Run in isolated context
agent: react-specialist # Optional: Specify executing agent
allowed-tools:          # Optional: Restrict available tools
  - Read
  - Glob
  - Grep
---
```

### Available Agents for `agent` Field

- `react-specialist` - React/frontend development
- `typescript-specialist` - TypeScript development
- `postgres-specialist` - PostgreSQL/database
- `go-specialist` - Go development
- `graphql-architect` - GraphQL design
- `security-specialist` - Security audits
- `debug-specialist` - Debugging
- `code-reviewer` - Code review
- See `.claude/agents/` for full list

### Arguments

- `{{args}}` - Optional: Skill name or brief description to initialize the workflow

If no arguments provided, create-skill will start with interactive prompts.
