# Claude Code Plugin Management Project

This repository manages custom plugins for Claude Code.

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

Specialized agents for frontend development.

**Included Agents:**
- `react-specialist` - React development expert
- `typescript-specialist` - TypeScript type system expert
- `tailwind-specialist` - Tailwind CSS expert
- `graphql-architect` - GraphQL architecture expert

### 2. Backend Plugin

Specialized agents for backend development.

**Included Agents:**
- `backend-architect` - Backend architecture design
- `go-specialist` - Go language development expert
- `k8s-specialist` - Kubernetes operations expert
- `terraform-specialist` - Terraform/IaC expert
- `grpc-specialist` - gRPC service design expert
- `security-specialist` - Security and DevSecOps expert
- `sql-specialist` - SQL database expert
- `cicd-specialist` - Expert deployment engineer specializing in modern CI/CD pipelines

### 3. Development Plugin

Comprehensive plugin supporting overall development workflows.

**Components:**
- **Agents** - Specialized agents
  - `code-reviewer` - Code review expert
  - `debug-specialist` - Debugging expert
  - `documentation-architect` - Documentation expert
  - `context-orchestrator` - Context management expert
  - `codebase-analyzer` - Analyzes codebases to identify architectural issues, code redundancy, and complexity

- **Commands** - Custom commands
  - `/code-explain` - Code explanation
  - `/dev-docs` - Generate development documentation
  - `/dev-docs-update` - Update documentation
  - `/create-command` - Create new command
  - `/create-agent` - Create new agent
  - `/analyze-codebase` - Analyze codebase for architectural issues, code redundancy, complexity
  - `/analyze-directory` - Analyze code and documentation within a specified directory
  - `/create-skill` - Create a new skill with automated testing and validation
  - `/optimize-description` - Transform a brief or vague prompt into a clear, specific description

- **Hooks** - Event hooks
  - `post-tool-use-tracker` - Post-tool usage tracking

- **Skills** - Reusable skills
  - `writing-skills` - Writing assistance skills
  - `creating-github-actions-workflows` - Use when setting up CI/CD pipelines and automating testing/deployment

## 🚀 Usage

This repository is designed to work as a Claude Code plugin marketplace. 

```bash
/plugin install frontend@fullstack-dev
/plugin install backend@fullstack-dev
/plugin install development@fullstack-dev
```

## 📚 References

- [Claude Code Plugins Documentation](https://code.claude.com/docs/en/plugins)
- [Plugin Marketplaces Guide](https://code.claude.com/docs/en/plugin-marketplaces)
- [Slash Commands Reference](https://code.claude.com/docs/en/slash-commands)
- [Skills Documentation](https://code.claude.com/docs/en/skills)
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)

## Inspired By repositories

- https://github.com/wshobson/agents
- https://github.com/diet103/claude-code-infrastructure-showcase
- https://github.com/davepoon/claude-code-subagents-collection
