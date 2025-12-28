---
description: Review and validate documentation for format compliance, contextual consistency, editorial quality, and sensitive information leakage
---

## Task

Perform comprehensive documentation review and validation on the specified file or directory.

### Review Checklist

1. **Format Validation**
   - Markdown syntax correctness
   - Heading hierarchy and structure
   - Code block formatting and language tags
   - Link integrity (internal and external)
   - List formatting consistency
   - Table structure validity

2. **Consistency Analysis**
   - Terminology usage consistency
   - Tone and voice alignment
   - Cross-reference accuracy
   - Version information alignment
   - Naming convention adherence

3. **Editorial Quality**
   - Grammar and spelling
   - Clarity and readability
   - Technical accuracy
   - Completeness of information
   - Code example correctness
   - Proper use of technical terms

4. **Security Scan**
   - API keys and tokens
   - Database credentials
   - Authentication secrets
   - PII (Personally Identifiable Information)
   - Internal URLs and endpoints
   - Confidential business information
   - Environment-specific details

### Arguments

- `{{target}}` - File path or directory to review (defaults to current directory)
- `--format-only` - Only perform format validation
- `--security-only` - Only perform security scan
- `--consistency-only` - Only perform consistency analysis
- `--editorial-only` - Only perform editorial review
- `--fix-auto` - Automatically fix formatting issues where possible
- `--report <path>` - Generate detailed report and save to specified path

### Output

Provide a structured report with:
- **Summary**: Overall assessment and key findings count
- **Critical Issues**: Security concerns and broken links
- **Format Issues**: Syntax errors and structural problems
- **Consistency Issues**: Terminology conflicts and cross-reference errors
- **Editorial Suggestions**: Grammar, clarity, and completeness improvements
- **Recommendations**: Prioritized action items with severity levels (Critical/High/Medium/Low)

### Process

1. Read the target documentation file(s)
2. Run applicable validation checks based on flags
3. Categorize findings by severity
4. If `--fix-auto` is specified, apply automatic fixes to formatting issues
5. Generate comprehensive report with actionable feedback
6. If `--report` is specified, save the report to the designated path
