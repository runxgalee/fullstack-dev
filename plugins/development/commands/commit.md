---
description: Create git commits with smart grouping and conventional commit format
---

## Task

Create git commits following Conventional Commits format with smart grouping. **This command only works with staged files** (files that have been `git add`ed).

### Arguments
If an issue number is provided (e.g., `/commit 123` or `/commit #123`), include it in the commit message format: `<type>: <description> (#<issue-number>)`

1. **Analyze staged changes**:
   - Run `git status` to see staged and unstaged changes
   - Run `git diff --cached --stat` to see only staged changes
   - Run `git diff --cached` to see detailed staged changes
   - Run `git log --oneline -5` to understand existing commit style
   - **IMPORTANT**: If there are no staged changes, inform the user and exit

2. **Group staged changes by type**:
   - Analyze only the staged changes
   - Group them into logical commits
   - Each commit should be focused and atomic
   - Group related files together (e.g., a feature with its tests, a bug fix with its affected files)
   - Separate different types of changes (features, fixes, refactors, docs, etc.)
   - If there are too many unrelated changes, split into multiple commits

3. **Determine commit type prefix**:
   - `feat:` - New features or functionality
   - `fix:` - Bug fixes
   - `refactor:` - Code refactoring without changing behavior
   - `docs:` - Documentation changes
   - `test:` - Adding or updating tests
   - `style:` - Code style/formatting changes
   - `chore:` - Maintenance tasks, dependencies, config
   - `perf:` - Performance improvements
   - `ci:` - CI/CD changes
   - `build:` - Build system changes

4. **Create commits from staged files**:
   - For each logical group, use `git reset HEAD <files>` to unstage files not in the current group
   - After unstaging unwanted files, the remaining staged files will be committed
   - Create commit with format: `<type>: <description>`
   - Use a heredoc for proper formatting:
     ```bash
     git commit -m "$(cat <<'EOF'
     feat: add user authentication system
     EOF
     )"
     ```
   - Re-stage the unstaged files for the next commit: `git add <previously-unstaged-files>`
   - Run `git status` after each commit to verify

5. **Commit message guidelines**:
   - Start with the type prefix (e.g., `feat:`, `fix:`)
   - Keep the description concise and clear
   - Focus on "what" and "why", not "how"
   - Use present tense
   - Don't end with a period
   - **If issue number provided**: append it in format `(#<number>)`
   - Example: `feat: add password reset functionality`
   - Example: `fix: prevent race condition in user login`
   - Example: `refactor: simplify database query logic`
   - Example with issue: `feat: add password reset functionality (#123)`
   - Example with issue: `fix: prevent race condition in user login (#456)`

## Important Notes

- **Only staged files**: This command only works with files that have already been staged with `git add`
- **Check for staged changes first**: Always verify there are staged changes before proceeding
- **Smart grouping**: If there are 5+ unrelated staged files, propose splitting into multiple focused commits
- **Do not commit everything at once** unless all changes are truly related
- Do not push to remote unless explicitly requested
- Do not commit files with secrets (.env, credentials.json, etc.)
- If pre-commit hook fails:
  - If commit was REJECTED: fix the issue and create a NEW commit
  - If commit SUCCEEDED but files were auto-modified: may amend ONLY if HEAD was created by you and not pushed
- Never use `git commit --amend` unless explicitly requested and safe to do so
- Never use flags like `--no-verify` or `--no-gpg-sign` unless explicitly requested
