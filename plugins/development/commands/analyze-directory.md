---
description: Analyze code and documentation within a specified directory to generate a comprehensive report explaining what the code does, its purpose, and behavior. Scans files to identify functionality, architecture patterns, entry points, dependencies, and workflows.
---

## Task

Generate a comprehensive analysis report for the specified directory.

### Process

1. **Accept directory path argument** - Use `{{ARGS}}` as the target directory path (default to current directory if not specified)

2. **Launch exploration** - Use the Task tool with subagent_type='Explore' and thoroughness='very thorough' to analyze:
   - File structure and organization
   - Code functionality and purpose
   - Architecture patterns and design decisions
   - Entry points and main workflows
   - Dependencies and integrations
   - Configuration files and settings

3. **Generate structured report** including:
   - **Overview**: Directory purpose and high-level functionality
   - **Architecture**: Design patterns, structure, and organization
   - **Entry Points**: Main files, functions, or classes that serve as starting points
   - **Key Components**: Important modules, functions, and their purposes
   - **Dependencies**: External libraries, frameworks, and internal dependencies
   - **Data Flow**: How data moves through the system
   - **Configuration**: Environment variables, config files, and settings
   - **Workflows**: Common operations and processes

4. **Output format** - Present the report in clear markdown format with sections and subsections

### Arguments

- `{{ARGS}}` - Directory path to analyze (optional, defaults to current directory)

### Example Usage

```
/analyze-directory src/services
/analyze-directory .
/analyze-directory ../backend/api
```
