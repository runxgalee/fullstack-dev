---
description: Estimate agent types, task breakdown, tools, agent interactions, parallelization opportunities, and execution flow with visual diagrams
---

## Task

Given a task description (provided as arguments or interactively), analyze and provide comprehensive task estimation including:

1. **Agent Types Needed**: Identify which specialized agents would be best suited
2. **Agent Execution Flow**: Visual Mermaid diagram showing agent sequence, parallel execution, and decision points
3. **Agent Interaction Matrix**: Table showing data flow, tools, and dependencies between agents
4. **Task Breakdown**: Detailed phases with agent assignments and dependencies
5. **Parallelization Analysis**: Identify which agents can run in parallel vs sequential
6. **Decision Points**: Conditional logic showing when agents trigger based on conditions
7. **Timeline Estimation**: Compare sequential vs parallel execution times
8. **Tool Estimation**: List tools used across all phases
9. **Expected Output Files**: Comprehensive list of all files each agent will generate, organized by agent with file paths, types, and purposes

## Agent Capability Database

Use these patterns to select appropriate agents based on task requirements:

### Development & Quality Agents

**code-reviewer** (Always include for implementation tasks)
- Inputs: All implementation files, changed files
- Outputs: review-report.md, quality-metrics
- Tools: Read, Grep, Glob
- Domain: Quality assurance
- Phase: Final validation (sequential, must wait for implementation)
- Estimated Time: 4-6 minutes

**debug-specialist** (Conditional: errors/test failures)
- Inputs: Error logs, stack traces, test failures
- Outputs: debug-report.md, fix suggestions
- Tools: Read, Grep, Bash, Task
- Domain: Cross-cutting
- Conditional: Only if tests fail or errors occur
- Estimated Time: 5-15 minutes

**context-orchestrator** (Complex tasks)
- Inputs: Project structure, task description
- Outputs: Context analysis, execution plan
- Tools: Read, Grep, Glob, Task
- Domain: Orchestration
- Phase: Initial analysis
- Estimated Time: 3-5 minutes

**claude-code-architect** (Very complex/unclear tasks)
- Inputs: Task description, codebase structure
- Outputs: Architecture plan, agent recommendations
- Tools: All tools
- Domain: Meta-planning
- Phase: Initial planning
- Estimated Time: 5-10 minutes

**documentation-architect**
- Inputs: Codebase, existing docs
- Outputs: Technical documentation, architecture guides
- Tools: Read, Grep, Glob, Write
- Domain: Documentation
- Estimated Time: 10-20 minutes

### Frontend Agents

**react-specialist**
- Inputs: Requirements, API spec, design mockups
- Outputs: components/*.tsx, hooks/*.ts, styles/*.css
- Tools: Write, Edit, Read, Bash (npm)
- Domain: Frontend
- Can Parallelize With: Backend agents, database agents (if no shared file conflicts)
- Estimated Time: 8-15 minutes

**typescript-specialist**
- Inputs: Requirements, existing types
- Outputs: types/*.ts, *.d.ts, tsconfig updates
- Tools: Write, Edit, Read
- Domain: Type systems
- Can Parallelize With: Other implementation agents
- Estimated Time: 5-10 minutes

**tailwind-specialist**
- Inputs: Design requirements, component structure
- Outputs: Tailwind configs, styled components
- Tools: Write, Edit, Read
- Domain: Styling
- Can Parallelize With: Component implementation
- Estimated Time: 4-8 minutes

### Backend Agents

**backend-architect**
- Inputs: Requirements, data model, API requirements
- Outputs: api-spec.yaml, service-design.md, *.ts, *.go
- Tools: Write, Edit, Read, Bash, Task
- Domain: Backend
- Can Parallelize With: Frontend agents, database agents (different files)
- Estimated Time: 10-20 minutes

**go-specialist**
- Inputs: Requirements, API spec
- Outputs: *.go, go.mod updates
- Tools: Write, Edit, Read, Bash
- Domain: Backend (Go)
- Can Parallelize With: Frontend, database, other backend if different services
- Estimated Time: 10-18 minutes

**grpc-specialist**
- Inputs: Service requirements, proto schemas
- Outputs: *.proto, gRPC services
- Tools: Write, Edit, Read, Bash
- Domain: RPC/microservices
- Can Parallelize With: Other implementation agents
- Estimated Time: 8-15 minutes

### Database Agents

**postgres-specialist**
- Inputs: Data model, requirements
- Outputs: migrations/*.sql, schema definitions
- Tools: Write, Edit, Bash (psql)
- Domain: Database
- Can Parallelize With: Backend API, frontend (usually different files)
- Estimated Time: 6-12 minutes

**sql-specialist**
- Inputs: Query requirements, schema
- Outputs: Optimized queries, indexes
- Tools: Write, Edit, Read, Bash
- Domain: Database optimization
- Can Parallelize With: Application code development
- Estimated Time: 5-10 minutes

**database-architect**
- Inputs: Requirements, data model
- Outputs: Schema design, migration strategy
- Tools: Write, Read
- Domain: Database design
- Phase: Early design phase (sequential)
- Estimated Time: 8-15 minutes

### Infrastructure & Operations Agents

**cloud-architect**
- Inputs: Requirements, infrastructure needs
- Outputs: IaC files (Terraform/CDK), architecture diagrams
- Tools: Write, Edit, Read
- Domain: Cloud infrastructure
- Estimated Time: 15-30 minutes

**k8s-specialist**
- Inputs: Application requirements, cluster config
- Outputs: Kubernetes manifests, Helm charts
- Tools: Write, Edit, Bash
- Domain: Container orchestration
- Estimated Time: 10-20 minutes

**terraform-specialist**
- Inputs: Infrastructure requirements
- Outputs: *.tf files, modules
- Tools: Write, Edit, Bash
- Domain: Infrastructure as Code
- Estimated Time: 12-25 minutes

**cicd-specialist**
- Inputs: Deployment requirements, test strategy
- Outputs: Pipeline configs (.github/workflows/*, .gitlab-ci.yml)
- Tools: Write, Edit, Bash
- Domain: CI/CD
- Estimated Time: 8-15 minutes

**sre-specialist**
- Inputs: Service requirements, SLOs
- Outputs: Monitoring configs, dashboards, alerts
- Tools: Write, Edit, Read
- Domain: Observability
- Estimated Time: 10-18 minutes

### Security Agents

**security-specialist** (Conditional: security-critical features)
- Inputs: Architecture design, implementation files
- Outputs: security-checklist.md, vulnerability report
- Tools: Read, Grep, Write
- Domain: Security
- Conditional: Always for auth/payments/sensitive data; optional otherwise
- Phase: After design, before implementation
- Estimated Time: 5-10 minutes

## Process

### 1. Parse Task Description

If arguments provided: Use them as task description
If no arguments: Ask user to describe the task

### 2. Analyze Task Requirements

Extract from task description:
- **Keywords**: auth, database, API, frontend, UI, deploy, test, performance, etc.
- **Technical Domain**: frontend, backend, database, fullstack, infrastructure, security
- **Complexity**: Simple (1-2 files), Medium (3-10 files), Complex (system-wide, multiple domains)
- **Scope**: Single component, feature addition, system refactor, new architecture

### 3. Select Agents

Based on keyword matching:

**Authentication/Security keywords**: `auth`, `login`, `jwt`, `oauth`, `security`, `encryption`
→ security-specialist, backend-architect, postgres-specialist (users table)

**Frontend/UI keywords**: `component`, `UI`, `frontend`, `react`, `page`, `form`, `button`
→ react-specialist, typescript-specialist, tailwind-specialist

**Backend/API keywords**: `API`, `endpoint`, `service`, `backend`, `server`, `microservice`
→ backend-architect, go-specialist, grpc-specialist

**Database keywords**: `database`, `schema`, `migration`, `query`, `SQL`, `postgres`
→ postgres-specialist, sql-specialist, database-architect

**Infrastructure keywords**: `deploy`, `cloud`, `AWS`, `kubernetes`, `infrastructure`, `terraform`
→ cloud-architect, k8s-specialist, terraform-specialist, cicd-specialist

**Performance/Debugging keywords**: `bug`, `error`, `slow`, `optimize`, `debug`, `performance`
→ debug-specialist, sre-specialist

**Quality keywords**: Always include `code-reviewer` for implementation tasks

**Complexity-based**:
- Complex or unclear tasks → claude-code-architect for planning
- Multi-domain tasks → context-orchestrator for coordination

### 4. Build Dependency Graph

For each selected agent:
1. Identify **inputs** (what artifacts/files it needs)
2. Identify **outputs** (what artifacts/files it produces)
3. Determine **dependencies**:
   - Agent B depends on Agent A if B needs A's output
   - Example: react-specialist depends on backend-architect's api-spec.yaml
4. Detect **file conflicts**:
   - Agents writing to same files cannot parallelize
   - Agents writing to different files can parallelize
5. Identify **phase**:
   - Analysis/Planning phase (sequential)
   - Implementation phase (can parallelize)
   - Integration/Testing phase (sequential)
   - Review phase (sequential)

### 5. Determine Parallelization

**Rules for parallel execution**:
- ✅ Agents with no data dependencies can run in parallel
- ✅ Agents writing to different files can run in parallel
- ✅ Multiple Read-only agents can always parallelize
- ⛔ Sequential if Agent B needs Agent A's output
- ⛔ Sequential if both modify the same files
- ⛔ Sequential for validation phases (review, testing)
- ⛔ Sequential for git operations (commits must be ordered)

**Group into phases**:
1. **Phase 1: Analysis** (Sequential)
   - context-orchestrator, claude-code-architect, database-architect
2. **Phase 2: Design Validation** (Sequential)
   - security-specialist (for security-critical features)
3. **Phase 3: Implementation** (Can parallelize)
   - Frontend: react-specialist, typescript-specialist, tailwind-specialist
   - Backend: backend-architect, go-specialist, grpc-specialist
   - Database: postgres-specialist, sql-specialist
   - Rule: Parallel if different file scopes, sequential if dependencies exist
4. **Phase 4: Integration** (Sequential)
   - backend-architect for connecting components, running integration tests
5. **Phase 5: Debugging** (Conditional, Sequential)
   - debug-specialist if tests fail
6. **Phase 6: Review** (Sequential)
   - code-reviewer for final quality check

### 6. Identify Decision Points

**Common decision patterns**:

1. **Security Review Decision** (After design)
   - Condition: Is this a security-critical feature? (auth, payments, user data)
   - If YES → security-specialist validates design
   - If NO → proceed to implementation

2. **Test Results Decision** (After integration)
   - Condition: Do all tests pass?
   - If NO → debug-specialist investigates → loop back to fixes
   - If YES → proceed to review

3. **Code Review Decision** (After review)
   - Condition: Any critical issues found?
   - If YES → loop back to implementation with fixes
   - If NO → task complete

4. **Complexity Decision** (Initial)
   - Condition: Is task very complex or unclear?
   - If YES → claude-code-architect creates detailed plan first
   - If NO → proceed with direct implementation

### 7. Generate Mermaid Diagram

Create a flowchart showing:
- **Start node**: `([Task: {task_name}])`
- **Agent nodes**: `[agent-name: action]`
- **Decision nodes**: `{Condition?}`
- **Parallel split**: `{Parallel Split}`
- **Sync points**: `((Sync Point))`
- **End node**: `([Complete])`
- **Connections**: ` --> |produces: artifact|` or `-->|condition|`

**Color coding (use style directives)**:
- Analysis/Planning agents: `fill:#E8F4F8,stroke:#0066CC`
- Implementation agents (can parallelize): `fill:#90EE90,stroke:#228B22`
- Decision points: `fill:#FFD700,stroke:#FF8C00`
- Parallel splits: `fill:#87CEEB,stroke:#4682B4`
- Sync points: `fill:#DDA0DD,stroke:#9370DB`
- Error/Debug agents: `fill:#FFB6C1,stroke:#DC143C`
- Review/Validation agents: `fill:#F0E68C,stroke:#DAA520`

**Output the Mermaid diagram to a separate file**:
- Create file: `docs/task-flow-{sanitized-task-name}.mmd` (sanitize task name: lowercase, replace spaces with hyphens, remove special chars)
- Example: For "GraphQL User Registration API" → `docs/task-flow-graphql-user-registration-api.mmd`
- If `docs/` directory doesn't exist, create it first
- Write the complete Mermaid flowchart to this file (without markdown code fences)
- In the main output, include a link to this file

**Template**:
```mermaid
flowchart TD
    Start([Task: {TASK_NAME}])

    %% Analysis Phase
    A1[agent1: Analyze Requirements]
    Start --> A1
    A1 --> |produces: requirements.md| Decision1{Decision Point}

    %% Decision Branch
    Decision1 -->|condition met| A2[agent2: Conditional Action]
    Decision1 -->|condition not met| Parallel1{Parallel Split}

    %% Parallel Implementation
    Parallel1 -->|branch 1| A3[agent3: Build Component A]
    Parallel1 -->|branch 2| A4[agent4: Build Component B]
    Parallel1 -->|branch 3| A5[agent5: Build Component C]

    A3 --> |produces: output1| Sync1((Sync Point 1))
    A4 --> |produces: output2| Sync1
    A5 --> |produces: output3| Sync1

    %% Integration & Testing
    Sync1 --> A6[agent6: Integration Tests]
    A6 --> |runs tests| Decision2{Tests Pass?}

    %% Conditional Debug Loop
    Decision2 -->|No| A7[debug-specialist: Investigate]
    A7 --> |produces: fixes| A3
    Decision2 -->|Yes| A8[code-reviewer: Final Review]

    %% Final Decision
    A8 --> |produces: review| Decision3{Critical Issues?}
    Decision3 -->|Yes| A3
    Decision3 -->|No| End([Complete])

    %% Styling
    style A1 fill:#E8F4F8,stroke:#0066CC
    style A3 fill:#90EE90,stroke:#228B22
    style A4 fill:#90EE90,stroke:#228B22
    style A5 fill:#90EE90,stroke:#228B22
    style A6 fill:#E8F4F8,stroke:#0066CC
    style A7 fill:#FFB6C1,stroke:#DC143C
    style A8 fill:#F0E68C,stroke:#DAA520
    style Decision1 fill:#FFD700,stroke:#FF8C00
    style Decision2 fill:#FFD700,stroke:#FF8C00
    style Decision3 fill:#FFD700,stroke:#FF8C00
    style Parallel1 fill:#87CEEB,stroke:#4682B4
    style Sync1 fill:#DDA0DD,stroke:#9370DB
```

### 8. Create Agent Interaction Matrix

Build a table with columns:
- **Agent**: Agent name
- **Phase**: Phase number
- **Input Dependencies**: What files/artifacts it needs (from which agents)
- **Tools Used**: List of tools (Read, Write, Edit, Bash, etc.)
- **Output Artifacts**: What files/artifacts it produces
- **Can Parallelize With**: Which other agents can run simultaneously

Example row:
| Agent | Phase | Input Dependencies | Tools Used | Output Artifacts | Can Parallelize With |
|-------|-------|-------------------|------------|------------------|---------------------|
| **backend-architect** | 3 | `requirements.md` (context-orchestrator), `security-checklist.md` (security-specialist) | Write, Edit, Bash, Task | `api-spec.yaml`, `auth-service.ts`, `tests/*.test.ts` | postgres-specialist, react-specialist |

### 9. Create Detailed Task Breakdown

For each phase:
- List phase name and type (Sequential/Parallel)
- For each step in phase:
  - **Step number and name**
  - **Agent**: Which agent handles this
  - **Input**: Dependencies and required artifacts
  - **Actions**: Bulleted list of what agent will do
  - **Tools**: Specific tools used
  - **Output**: Artifacts produced
  - **Can Parallel With**: Other steps (if applicable)
  - **Estimated Time**: Time range in minutes
  - **Blocking**: Whether this blocks other steps

### 10. List Decision Points & Conditional Flows

For each decision point:
- **Decision ID**: After which agent/phase
- **Condition**: What determines the path
- **True Path**: What happens if condition is met
- **False Path**: What happens if condition is not met
- **Trigger Type**: Always, Conditional, Loop-back

Example:
```
1. **After Phase 1 (Always triggers)**
   - Decision: Security review required?
   - Action: Always invoke security-specialist for auth/payment features
   - Rationale: Security-critical features require expert validation

2. **After Phase 4 (Conditional)**
   - Decision: Are all tests passing?
   - If NO: Invoke debug-specialist → Fix → Re-test (loop)
   - If YES: Proceed to code review
```

### 11. Calculate Timeline Estimates

**Per-agent estimates**: Use ranges from agent capability database

**Sequential execution**: Sum of all agent times
- Formula: `sum(all agent times)`

**Parallel execution**: Max of parallel branches + sequential phases
- Formula: `sum(sequential phases) + max(parallel branch times)`

**Optimization percentage**:
- Formula: `((sequential - parallel) / sequential) * 100`

**Critical path**: Longest dependency chain from start to finish

**Blocking dependencies**: Count of sync points where parallel work must converge

### 12. List Tools Required

Group tools by phase and purpose:
- **Read**: Which phases use for what purpose
- **Write**: New file creation (list estimated file count)
- **Edit**: Existing file modification
- **Grep/Glob**: Code discovery and pattern matching
- **Bash**: Commands (npm, psql, testing, git)
- **Task**: Sub-agent orchestration

Include estimated frequency for each tool.

### 13. Document Expected Output Files

Create a comprehensive list of all files that will be generated during task execution:

**File Categories**:
1. **Analysis & Planning Documents** (`.md` reports, design docs)
2. **Implementation Code** (`.ts`, `.tsx`, `.go`, `.sql`, etc.)
3. **Configuration Files** (`.yaml`, `.json`, config files)
4. **Test Files** (`.test.ts`, `.spec.ts`, integration tests)
5. **Generated Assets** (types, schemas, migrations)

**For each agent**, list:
- **Agent name**
- **Output files** with full relative paths from project root
- **File type** (Report, Code, Config, Test, Generated)
- **Purpose** of each file

**Format as a table**:
| Agent | File Path | Type | Purpose |
|-------|-----------|------|---------|
| agent-name | `path/to/file.ext` | Report/Code/Config/Test/Generated | Brief description |

**Grouping**:
- Group files by agent
- Within each agent, order by creation sequence
- Mark conditional files (e.g., debug-specialist outputs only if tests fail)

**Example**:
```markdown
### Expected Output Files

| Agent | File Path | Type | Purpose |
|-------|-----------|------|---------|
| **graphql-architect** | `docs/schema-analysis.md` | Report | GraphQL schema design and mutation specifications |
| **graphql-architect** | `schema/user.graphql` | Code | User registration GraphQL schema definitions |
| **postgres-specialist** | `docs/users-schema.sql` | Report | Database schema design document |
| **postgres-specialist** | `migrations/20260108_create_users_table.sql` | Code | Users table creation migration |
| **security-specialist** | `docs/security-checklist.md` | Report | Security validation and requirements |
| **backend-architect** | `resolvers/user.ts` | Code | User registration resolver implementation |
| **backend-architect** | `tests/user.test.ts` | Test | Unit tests for user registration |
| **code-reviewer** | `docs/review-report.md` | Report | Final code quality and security review |
| **debug-specialist** | `docs/debug-report.md` | Report | Debugging analysis (conditional - only if tests fail) |
```

This section provides:
- A complete checklist of expected deliverables
- Clear file organization structure
- Easy verification of task completion
- Input for subsequent automation (e.g., checking if all files were created)

### 14. Output Results to Files

After generating the complete analysis:

#### Step 14.1: Create Output Directory
- Check if `docs/` exists, create if needed using mkdir

#### Step 14.2: Sanitize Task Name
Convert task name to filename-safe format:
- Lowercase all characters
- Replace spaces with hyphens
- Remove special characters (keep only alphanumeric and hyphens)
- Truncate to 50 characters max
- Example: "GraphQL User Registration API" → "graphql-user-registration-api"

#### Step 14.3: Write Mermaid Diagram File
Save the complete Mermaid flowchart to `docs/task-flow-{sanitized-name}.mmd`:
- Do NOT include markdown code fences (```mermaid)
- Write raw Mermaid syntax only
- Include all style directives

#### Step 14.4: Write Complete Estimation Report
Save the complete estimation analysis to `docs/task-estimate-{sanitized-name}.md`:
- Include all sections: Complexity Assessment, Recommended Agents, Agent Execution Flow, Agent Interaction Matrix, Detailed Task Breakdown, Decision Points, Tools Required, Expected Output Files, Estimated Timeline, Parallelization Summary
- For the "Agent Execution Flow" section, include BOTH:
  - Link to the separate `.mmd` file
  - Inline mermaid diagram with code fences
- Use full markdown formatting
- This file serves as a permanent record of the estimation

#### Step 14.5: Provide Summary to User
After writing both files, provide a concise summary to the user:
```
✅ Task estimation complete!

📊 **Full Report**: [docs/task-estimate-{sanitized-name}.md](./docs/task-estimate-{sanitized-name}.md)
📈 **Flow Diagram**: [docs/task-flow-{sanitized-name}.mmd](./docs/task-flow-{sanitized-name}.mmd)

**Quick Summary**:
- Complexity: [Simple/Medium/Complex]
- Agents Required: [count] agents
- Estimated Time: [X-Y] minutes (optimized with parallelization)
- Key Phases: [brief list]
```

Do NOT output the full estimation report inline to the user - only output the summary above. The full report is in the saved file.

## Output Format

**IMPORTANT**: Write the complete estimation to `docs/task-estimate-{sanitized-task-name}.md` file, then provide only a summary to the user.

The complete estimation file should follow this structured format:

````markdown
## Task Analysis: [Task Name]

### Complexity Assessment
**[Simple/Medium/Complex]** - [Brief reasoning about scope, domains involved, and technical challenges]

### Recommended Agents
- **agent-name** (Model: sonnet/opus/haiku): [Why this agent is suitable, what it will handle]
- **agent-name** (Model: sonnet/opus/haiku): [Reasoning]
- ...

[Include 3-8 agents typically, with conditional agents marked]

### Agent Execution Flow

**Mermaid Diagram**: [View flow diagram](./docs/task-flow-{sanitized-task-name}.mmd)

<details>
<summary>Click to view inline diagram</summary>

```mermaid
[Generate flowchart diagram as specified in step 7]
```

</details>

### Agent Interaction Matrix

| Agent | Phase | Input Dependencies | Tools Used | Output Artifacts | Can Parallelize With |
|-------|-------|-------------------|------------|------------------|---------------------|
| **agent1** | 1 | Task description | Read, Grep | requirements.md | None (Sequential) |
| **agent2** | 3 | requirements.md | Write, Edit | component.tsx | agent3, agent4 |
| ... | ... | ... | ... | ... | ... |

### Detailed Task Breakdown

#### Phase 1: [Phase Name] (Sequential/Parallel - XX-YY minutes)

**Step 1.1** - Agent: `agent-name`
- **Input**: [Dependencies]
- **Actions**:
  - Action item 1
  - Action item 2
- **Tools**: [Tools used]
- **Output**: [Artifacts produced]
- **Can Parallel With**: [Other steps or None]
- **Estimated Time**: X-Y minutes

[Continue for all phases and steps]

**Synchronization Point N**: [Description of what must complete before proceeding]

### Decision Points & Conditional Flows

1. **After [Phase/Agent] ([Always/Conditional])**
   - **Decision**: [Condition to evaluate]
   - **If YES**: [Action taken]
   - **If NO**: [Alternative action]
   - **Rationale**: [Why this decision point exists]

[List all decision points]

### Tools Required

| Tool | Usage Phase | Purpose | Estimated Frequency |
|------|-------------|---------|---------------------|
| **Read** | All | Read existing code, configs | High (50+ files) |
| **Write** | 3 | Create new components | Medium (10-15 files) |
| ... | ... | ... | ... |

### Expected Output Files

| Agent | File Path | Type | Purpose |
|-------|-----------|------|---------|
| **agent-name** | `path/to/output.md` | Report | Description of the file's purpose |
| **agent-name** | `src/component.tsx` | Code | Implementation file description |
| **agent-name** | `tests/component.test.ts` | Test | Test file description |
| ... | ... | ... | ... |

[Include all files that will be generated during task execution, organized by agent]

### Estimated Timeline

**Without Parallelization** (Sequential execution):
- Phase 1: X-Y minutes
- Phase 2: X-Y minutes
- ...
- **Total: XX-YY minutes**

**With Parallelization** (Optimized):
- Phase 1: X-Y minutes (sequential)
- Phase 2: X-Y minutes (max of parallel branches)
- ...
- **Total: XX-YY minutes**

**Optimization Gain**: ~XX-YY% faster with parallel execution

**Critical Path**: [Longest dependency chain]

**Blocking Dependencies**: N synchronization points (after Phase X, Y, Z)

### Parallelization Summary

**Parallel Opportunities**:
- ✅ Phase X: [Agent A + Agent B + Agent C can run in parallel]
- ✅ [Other parallel opportunities]

**Sequential Requirements**:
- ⛔ Phase X must complete before Phase Y ([reason])
- ⛔ [Other sequential requirements]

**Conditional Branches**:
- 🔀 [Conditional flow description]
````

## Important Notes

1. **Simple tasks** (1-2 agents, single file): Skip complex diagram, provide simplified output
2. **Complex tasks** (6+ agents, multi-domain): Full visualization with all sections
3. **Edge cases**:
   - If circular dependencies detected: Warn user and suggest refactoring
   - If too many agents (>10): Group similar agents and simplify diagram
   - If unclear task: Recommend using claude-code-architect first
4. **Always include**:
   - code-reviewer for implementation tasks
   - debug-specialist marked as conditional
   - Realistic time estimates with ranges
5. **Model selection**:
   - opus for complex architecture/design agents
   - sonnet for most implementation and analysis
   - haiku for simple, straightforward tasks

## Example Keywords for Agent Selection

- **auth, login, signup, jwt, oauth, session**: → security-specialist, backend-architect, postgres-specialist
- **component, react, tsx, ui, page, form**: → react-specialist, typescript-specialist
- **api, endpoint, rest, graphql, grpc**: → backend-architect, grpc-specialist
- **database, schema, migration, sql, query**: → postgres-specialist, sql-specialist, database-architect
- **deploy, cloud, aws, k8s, terraform**: → cloud-architect, k8s-specialist, terraform-specialist
- **test, ci/cd, pipeline, github actions**: → cicd-specialist
- **monitor, metrics, logs, alerts**: → sre-specialist
- **bug, error, debug, fix, failing**: → debug-specialist
- **performance, slow, optimize**: → sre-specialist, sql-specialist (for DB), react-specialist (for frontend)
- **security, vulnerability, encrypt**: → security-specialist
- **docs, documentation, readme**: → documentation-architect
