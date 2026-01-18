---
description: Create git commit and push changes to remote repository
allowedTools:
  - Command(development:commit)
  - Bash(git:*)
  - Bash(plugin:*)
---

## Task

Create git commit(s) using the /commit command and push changes to the remote repository.

Follow this workflow:

1. **Create commit(s) using /commit command**
   - If arguments are provided to this command, pass them to /commit (e.g., issue number)
   - The /commit command will handle:
     - Analyzing staged changes
     - Grouping changes intelligently
     - Creating conventional commit messages
     - Following git safety practices

2. **Push to remote**
   - After commit(s) are created successfully, push to remote
   - Check if current branch tracks a remote branch
   - If no upstream branch exists, push with `-u` flag: `git push -u origin <branch-name>`
   - If upstream exists, use: `git push`
   - Display the result to user

3. **Update plugin marketplace**
   - After successfully pushing to remote, run `/plugin marketplace update fullstack-dev`
   - This ensures plugin metadata is kept up-to-date after changes
   - Display the result to user

### Git Safety
- NEVER update git config
- NEVER run destructive commands (force push, hard reset) unless explicitly requested
- NEVER skip hooks (--no-verify) unless explicitly requested
- All commit safety is handled by the /commit command

### Arguments
If arguments are provided (e.g., issue number), pass them to the /commit command.
