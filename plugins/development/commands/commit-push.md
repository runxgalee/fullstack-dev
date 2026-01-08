---
description: Create git commit and push changes to remote repository
---

## Task

Create a git commit with appropriate commit message and push changes to the remote repository.

Follow this workflow:

1. **Review changes**
   - Run `git status` to see all changes
   - Run `git diff` to see unstaged changes
   - Run `git diff --staged` to see staged changes (if any)
   - Run `git log -3 --oneline` to understand commit message style

2. **Stage changes**
   - Add relevant files to staging area
   - Do not commit files that likely contain secrets (.env, credentials.json, etc.)
   - Warn user if they request to commit sensitive files

3. **Create commit**
   - Analyze all staged changes
   - Draft a concise commit message (1-2 sentences) following conventional commit format
   - Focus on "why" rather than "what"
   - Match the repository's existing commit message style
   - Use heredoc format for the commit message:
     ```bash
     git commit -m "$(cat <<'EOF'
     Commit message here.
     EOF
     )"
     ```

4. **Push to remote**
   - Check if current branch tracks a remote branch
   - If no upstream branch exists, push with `-u` flag: `git push -u origin <branch-name>`
   - If upstream exists, use: `git push`
   - Display the result to user

### Git Safety
- NEVER update git config
- NEVER run destructive commands (force push, hard reset) unless explicitly requested
- NEVER skip hooks (--no-verify) unless explicitly requested
- Avoid `git commit --amend` unless explicitly requested and safe to do so
- NEVER commit unless user explicitly asks

### Arguments
If arguments are provided, use them as the commit message directly instead of analyzing changes.
