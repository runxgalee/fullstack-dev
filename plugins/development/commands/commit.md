---
description: Create git commits with smart grouping and conventional commit format
---

## Task

Create git commits following Conventional Commits format with smart grouping.

### Arguments
If an issue number is provided (e.g., `/commit 123` or `/commit #123`), include it in the commit message format: `<type>: <description> (#<issue-number>)`

1. **Analyze changes**:
   - Run `git status` and `git diff --stat` to see all changes
   - Run `git diff` to see detailed changes
   - Run `git log --oneline -5` to understand existing commit style

2. **Group changes by type**:
   - Analyze the changes and group them into logical commits
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

4. **Create commits**:
   - For each logical group, stage only those files using `git add <files>`
   - Create commit with format: `<type>: <description>`
   - Use a heredoc for proper formatting:
     ```bash
     git commit -m "$(cat <<'EOF'
     feat: add user authentication system
     EOF
     )"
     ```
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

- **Smart grouping**: If there are 5+ unrelated files, propose splitting into multiple focused commits
- **Do not commit everything at once** unless all changes are truly related
- Do not push to remote unless explicitly requested
- Do not commit files with secrets (.env, credentials.json, etc.)
- If pre-commit hook fails:
  - If commit was REJECTED: fix the issue and create a NEW commit
  - If commit SUCCEEDED but files were auto-modified: may amend ONLY if HEAD was created by you and not pushed
- Never use `git commit --amend` unless explicitly requested and safe to do so
- Never use flags like `--no-verify` or `--no-gpg-sign` unless explicitly requested
