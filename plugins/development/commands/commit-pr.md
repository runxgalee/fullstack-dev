---
description: Create commits using /commit command and draft pull request
---

## Task

Create git commits and a draft pull request following these steps:

### Arguments
Optional issue number (e.g., `/commit-pr 123` or `/commit-pr #123`) to pass to `/commit` command and include in PR title.

### Step 1: Create Commits

Use the `/commit` command to create commits:
- If issue number provided, call `/commit <issue-number>`
- Otherwise, call `/commit`

The `/commit` command will:
- Analyze and group changes into logical commits
- Apply Conventional Commits format
- Include issue number in commit messages if provided

### Step 2: Create Draft Pull Request

1. **Check branch status**:
   - Run `git status` to verify commits were created
   - Check if branch needs to be pushed: `git rev-parse --abbrev-ref --symbolic-full-name @{u}`

2. **Analyze PR scope**:
   - Run `git log main...HEAD` or `git log [base-branch]...HEAD` to see all commits in PR
   - Run `git diff main...HEAD --stat` to see all changes
   - Review ALL commits that will be included (not just the latest)

3. **Create PR summary**:
   - If issue number provided, include in title: `<type>: <description> (#<issue>)`
   - Otherwise use conventional commit format based on commits: `<type>: <description>`
   - Body format:
     ```markdown
     ## Summary
     - [Bullet points of key changes based on commits]

     ## Related Issue
     Closes #<issue-number> (if applicable)

     ## Test Plan
     - [ ] [Testing checklist items]
     ```

4. **Push and create draft PR**:
   - Push to remote if needed: `git push -u origin <branch>`
   - Create draft PR using heredoc:
     ```bash
     gh pr create --draft --title "<title>" --body "$(cat <<'EOF'
     ## Summary
     - [Changes]

     ## Related Issue
     Closes #123

     ## Test Plan
     - [ ] [Tests]
     EOF
     )"
     ```

## Important Notes

- **Use `/commit` command**: Do not manually create commits, always use `/commit` command
- **PR as draft**: Always create as draft for review before marking ready
- Return the PR URL when complete
