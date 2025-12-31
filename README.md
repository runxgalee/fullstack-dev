# Claude Code Plugin Management Project

This repository manages custom plugins for Claude Code.

## Compatibility

This plugin collection is designed for **Claude Code CLI** and follows the official plugin marketplace specification. Compatible with Claude Code version 1.0.0 and above.

## 📁 Project Structure

```
fullstack-dev/
├── .claude-plugin/
│   └── marketplace.json       # Claude Code configuration
└── plugins/
    ├── frontend/              # Frontend development plugin
    ├── backend/               # Backend development plugin
    └── development/           # Development workflow plugin
```

## 🔌 Plugins Overview

### 1. Frontend Plugin

Specialized agents for frontend development and UI engineering.

**Included Agents (4):**
- `react-specialist` - React 19, Next.js 15, and modern frontend architecture expert
- `typescript-specialist` - Advanced TypeScript type system and strict type safety expert
- `tailwind-specialist` - Tailwind CSS design systems and performance optimization expert
- `graphql-architect` - GraphQL architecture, federation, and schema design expert

### 2. Backend Plugin

Specialized agents for backend development, infrastructure, and data engineering.

**Included Agents (14):**
- `backend-architect` - Backend architecture and microservices design
- `go-specialist` - Go language development with modern patterns and concurrency
- `k8s-specialist` - Kubernetes operations and cloud-native platform engineering
- `terraform-specialist` - Terraform/OpenTofu IaC automation expert
- `grpc-specialist` - gRPC service design and streaming systems
- `security-specialist` - Security, DevSecOps, and compliance frameworks
- `sql-specialist` - SQL database optimization and query tuning
- `cicd-specialist` - CI/CD pipelines and deployment automation
- `cloud-architect` - AWS/Azure/GCP multi-cloud infrastructure and FinOps
- `data-engineer` - Data pipelines, warehouses, and streaming architectures
- `postgres-specialist` - PostgreSQL database design and performance optimization
- `database-architect` - Database technology selection and schema design
- `sre-specialist` - Production monitoring, observability, and SRE practices
- `graphql-architect` - GraphQL architecture, federation, and schema design expert (also in frontend)

### 3. Development Plugin

Comprehensive plugin supporting overall development workflows, code quality, and project management.

**Components:**

- **Agents (6)** - Specialized development agents
  - `code-reviewer` - AI-powered code analysis and security scanning
  - `debug-specialist` - Error analysis and debugging expert
  - `documentation-architect` - Technical documentation and architecture guides
  - `context-orchestrator` - Context management and AI orchestration
  - `codebase-analyzer` - Architectural analysis, code redundancy, and complexity assessment
  - `project-analyzer` - Comprehensive project onboarding and architecture audits

- **Commands (16)** - Custom slash commands
  - `/code-explain` - Explain code functionality and behavior
  - `/dev-docs` - Generate comprehensive development documentation
  - `/dev-docs-update` - Update existing documentation
  - `/create-command` - Create new custom slash command
  - `/create-agent` - Create new specialized agent
  - `/create-issue` - Create GitHub issue with structured planning documentation
  - `/analyze-codebase` - Analyze architecture, redundancy, and complexity
  - `/analyze-directory` - Analyze code within a specific directory
  - `/create-skill` - Interactive skill creation workflow with guided prompts and templates
  - `/optimize-description` - Transform vague prompts into clear descriptions
  - `/review-docs` - Review documentation for format, consistency, and security
  - `/commit` - Create git commits with smart grouping and Conventional Commits format
  - `/commit-pr` - Create commits and draft pull request
  - `/onboarding-report` - Generate comprehensive project onboarding report
  - `/git-workflow` - Complete git workflow with multi-agent orchestration
  - `/plan-execution` - Create execution plans with agent selection and sequencing strategy

- **Hooks (2)** - Event hooks
  - `post-tool-use-tracker` - Post-tool usage tracking
  - `skill-activation-prompt` - Skill activation prompt handler

- **Skills (2)** - Reusable skills
  - `skill-developer` - Create and manage Claude Code skills following Anthropic best practices
  - `brainstorming` - Collaborative ideation and exploration before implementation

## 🚀 Usage

This repository is designed to work as a Claude Code plugin marketplace. Install individual plugins using the following commands:

```bash
# Install frontend development plugin
/plugin install frontend@fullstack-dev

# Install backend development plugin
/plugin install backend@fullstack-dev

# Install development workflow plugin
/plugin install development@fullstack-dev
```

## 📚 References

Comprehensive resources for Claude Code plugins and features:

- [Claude Code Plugins Documentation](https://code.claude.com/docs/en/plugins) - Plugin development guide
- [Plugin Marketplaces Guide](https://code.claude.com/docs/en/plugin-marketplaces) - Creating and managing plugin marketplaces
- [Slash Commands Reference](https://code.claude.com/docs/en/slash-commands) - Custom command creation
- [Skills Documentation](https://code.claude.com/docs/en/skills) - Building reusable skills
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide) - Event-driven hooks

## Inspired by Repositories

- https://github.com/wshobson/agents - Agent collection and patterns
- https://github.com/diet103/claude-code-infrastructure-showcase - Infrastructure automation examples
- https://github.com/davepoon/claude-code-subagents-collection - Specialized subagent implementations
