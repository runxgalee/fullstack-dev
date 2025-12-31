---
description: Create a GitHub issue with structured planning documentation using a template that organizes task information into background, approach, and task breakdown sections
---

## Task

Create a comprehensive GitHub issue with structured planning documentation for the given task description.

### Process

1. **Analyze the task description** provided by the user
   - Extract key requirements and objectives
   - Identify scope and complexity

2. **Generate an issue template** with the following sections:
   - **Background/Context**: Why this task is needed, problem statement, current state
   - **Approach/Strategy**: Proposed solution, technical approach, key decisions
   - **Task Breakdown**: Detailed step-by-step plan with sub-tasks and dependencies

3. **Create the template file** (if not exists):
   - Location: `.github/ISSUE_TEMPLATE/planning-task.md`
   - Use GitHub issue template format
   - Include all planning sections

4. **Populate the issue** with analyzed content:
   - Fill in background based on task context
   - Outline strategic approach
   - Break down into actionable tasks with checkboxes

5. **Submit the GitHub issue**:
   - Use `gh issue create` command
   - Apply appropriate labels (e.g., `planning`, `task-breakdown`)
   - Include the populated template content
   - Return the issue URL

### Arguments

- `{{task_description}}` - Description of the task to create an issue for

### Optional Flags

When calling this command, users may include:
- `--labels` - Additional labels to apply (comma-separated)
- `--assignee` - GitHub username to assign
- `--milestone` - Milestone to link to
- `--project` - Project board to add issue to

### Example Usage

```
/create-issue Implement user authentication system with JWT tokens
/create-issue "Add dark mode support to the application" --labels "enhancement,ui" --assignee username
```

### Template Structure

The generated issue should follow this structure:

```markdown
## Background/Context

[Why is this task needed? What problem does it solve? What is the current state?]

## Approach/Strategy

[What is the proposed solution? What technical approach will be used? What are the key decisions?]

## Task Breakdown

- [ ] Task 1: [Description]
  - [ ] Subtask 1.1
  - [ ] Subtask 1.2
- [ ] Task 2: [Description]
- [ ] Task 3: [Description]

## Acceptance Criteria

[What defines completion? How will we verify success?]

## Notes

[Any additional context, dependencies, or considerations]
```
