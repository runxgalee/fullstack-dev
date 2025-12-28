---
description: Transform a brief or vague prompt into a clear, specific, and actionable description suitable for Claude Code execution
---

## Task

Transform the user's input prompt into a clear, specific, and actionable description optimized for Claude Code execution.

### Requirements

1. **Clarity**: Convert vague requests into specific, unambiguous instructions
2. **Actionability**: Ensure the prompt clearly describes what needs to be done
3. **Context**: Add relevant context that helps Claude Code understand the task better
4. **Structure**: Break down complex requests into logical steps when needed
5. **Language**: If input is in Japanese, translate to English while preserving intent

### Process

1. Analyze the user's input prompt
2. Identify ambiguities, missing context, or vague language
3. Enhance the prompt with:
   - Specific technical details
   - Clear success criteria
   - Relevant constraints or preferences
   - File paths or locations if applicable
4. Output the optimized prompt in a clear, structured format

### Arguments

- `{{prompt}}` - The original prompt to optimize

### Example Transformations

**Before**: "make it faster"
**After**: "Analyze the performance bottlenecks in the application and implement specific optimizations. Profile the code to identify slow functions, optimize database queries, implement caching where appropriate, and measure the performance improvements."

**Before**: "add button"
**After**: "Add a button component to [specify location]. The button should [specify functionality], use [specify styling approach], and handle [specify user interactions]. Follow the existing component patterns in the codebase."

### Output Format

**IMPORTANT**: Output must be formatted as a concise slash command description that fits within 1024 characters.

**Format Requirements**:
- Single-line or short paragraph description (max 1024 characters)
- Clear, actionable language suitable for command descriptions
- Focus on what the command does and key features
- Omit unnecessary elaboration or examples in the output
- If input is in Japanese, translate to English

**Example Output** (for creating a code analysis command):
"Analyze code in a specified directory and generate a comprehensive report explaining functionality, architecture, and behavior. Scans files to identify entry points, design patterns, dependencies, and data flow. Accepts directory path as argument with optional flags: --depth (recursion level), --format (markdown/html/json), --include/--exclude (file patterns), --output (save location). Uses Explore agent for thorough analysis. Useful for onboarding, documentation, and understanding unfamiliar codebases."

The output should be ready to use directly as a `description:` field in a slash command definition.
