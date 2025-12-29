---
description: Interactive skill creation workflow with guided prompts, templates, and best practices enforcement
---

## Task

Use the skill-developer skill to create a new Claude Code skill with an interactive, guided workflow.

The skill-developer provides:
- Guided prompts for skill name, description, and functionality
- Template selection based on skill complexity and purpose
- Best practices enforcement for skill structure and documentation
- Automatic plugin category determination
- File creation in appropriate plugin directories
- Symlink creation in .claude/skills/
- Comprehensive documentation with examples
- Validation of skill structure
- README.md updates

### Process

1. Invoke the skill-developer skill using the Skill tool
2. Follow the interactive prompts to define your skill
3. Review the generated skill structure
4. Validate and deploy the skill

### Arguments

- `{{args}}` - Optional: Skill name or brief description to initialize the workflow

If no arguments provided, skill-developer will start with interactive prompts.
