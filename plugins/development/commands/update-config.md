---
description: Update Claude Code configuration files (agents, skills, commands, hooks) based on their descriptions
---

## Task

Analyze and modify Claude Code configuration files to ensure they match their stated descriptions.

### Process

1. **Identify target files**
   - Read the arguments to determine which files to update
   - If no specific files mentioned, ask which configuration type to analyze (agents/skills/commands/hooks)

2. **Analyze descriptions**
   - Read each configuration file
   - Extract the description from the frontmatter or header
   - Compare the description with the actual implementation

3. **Apply modifications**
   - Update the file content to align with the description
   - Ensure consistency in:
     - Tool usage matches stated capabilities
     - Instructions reflect the described behavior
     - Examples align with the description
     - Triggers (for skills) match the description

4. **Maintain structure**
   - Preserve existing frontmatter format
   - Keep the overall file structure intact
   - Follow plugin organization rules

### Arguments
- File paths or patterns to update (optional)
- Configuration type: agents, skills, commands, or hooks (optional)
- If no arguments provided, prompt the user to specify

### Example Usage
```
/update-config plugins/development/agents/*.md
/update-config --type skills
/update-config .claude/agents/backend:postgres-specialist.md
```
