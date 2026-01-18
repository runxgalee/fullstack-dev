---
description: Analyze a project directory and generate an onboarding report using dynamically selected skills based on detected technologies
---

## Task

Analyze the specified project directory and generate a comprehensive onboarding report. Dynamically detect the project type and apply relevant onboarding skills.

### Arguments

- `{{args}}` - Target directory path to analyze (defaults to current directory if not specified)

### Process

1. **Detect Project Type**

   Scan the target directory to identify technologies:

   | Detection | Files/Patterns | Applicable Skill |
   |-----------|----------------|------------------|
   | Go project | `go.mod`, `*.go` | `go-project` |
   | Go REST API | `go.mod` + Echo/Gin/Chi/Fiber imports | `go-rest-api` |
   | Go GraphQL | `go.mod` + gqlgen, `*.graphqls` | `go-graphql` |
   | Go gRPC | `go.mod` + `*.proto`, grpc imports | `go-grpc` |
   | React/Next.js | `package.json` with react/next | `react-project` |
   | Database | Migration files, schema files | `database-schema` |

2. **Apply Relevant Skills**

   For each detected technology, invoke the corresponding skill using the Task tool with the appropriate agent:

   ```
   - go-project → agent: go-specialist
   - go-rest-api → agent: go-specialist
   - go-graphql → agent: go-specialist
   - go-grpc → agent: go-specialist
   - react-project → agent: react-specialist
   - database-schema → agent: postgres-specialist
   ```

3. **Run Project Health Check**

   Always run `review-project` skill to assess:
   - Structural integrity
   - Security posture
   - Performance characteristics
   - Code stability

4. **Generate Consolidated Report**

   Combine all skill outputs into a unified onboarding report:

   ```markdown
   # Project Onboarding Report

   ## Project Overview
   - Directory: [path]
   - Detected Technologies: [list]
   - Analysis Date: [date]

   ## Technology-Specific Analysis

   ### [Technology 1]
   [Skill output]

   ### [Technology 2]
   [Skill output]

   ## Project Health
   - Health Score: XX/100
   - Risk Level: [Low/Medium/High/Critical]

   ## Key Findings
   1. [Finding 1]
   2. [Finding 2]

   ## Recommended Next Steps
   1. [Action item]
   2. [Action item]

   ## Key Files to Read
   1. [file path] - [reason]
   2. [file path] - [reason]
   ```

### Multi-Technology Projects

For projects with multiple technologies (e.g., Go backend + React frontend):

1. Run skills in parallel where possible
2. Identify integration points between technologies
3. Document cross-technology dependencies
4. Provide holistic architecture overview

### Example Usage

```bash
# Analyze current directory
/onboard-project

# Analyze specific directory
/onboard-project /path/to/project

# Analyze relative path
/onboard-project ./backend
```
