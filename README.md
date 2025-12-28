# Claude Code Plugin Management Project

This repository manages custom plugins for Claude Code.

## 📁 Project Structure

```
fullstack-dev/
├── .claude/
│   └── settings.json          # Claude Code configuration
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

### 3. Development Plugin

Comprehensive plugin supporting overall development workflows.

**Components:**
- **Agents** - Specialized agents
  - `code-reviewer` - Code review expert
  - `debug-specialist` - Debugging expert
  - `documentation-architect` - Documentation expert
  - `context-orchestrator` - Context management expert

- **Commands** - Custom commands
  - `/code-explain` - Code explanation
  - `/dev-docs` - Generate development documentation
  - `/dev-docs-update` - Update documentation
  - `/create-command` - Create new command
  - `/create-agent` - Create new agent

- **Hooks** - Event hooks
  - `post-tool-use-tracker` - Post-tool usage tracking

- **Skills** - Reusable skills
  - Writing skills - Writing assistance skills

## 🚀 Usage

### Enabling Plugins

1. Enable plugins in Claude Code settings file (`.claude/settings.json`)
2. Each plugin directory can be managed independently

### Plugin Development

Recommended directory structure for each plugin:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json           # Plugin metadata
├── agents/                   # Agent definitions (.md files)
├── commands/                 # Command definitions (.md files)
├── hooks/                    # Event hooks (.sh files)
└── skills/                   # Skill definitions (.md files)
```

## 📝 Adding New Plugins

1. Create a new directory under `plugins/`
2. Create `.claude-plugin/plugin.json` and define metadata
3. Add `agents/`, `commands/`, `hooks/`, `skills/` as needed
4. Create markdown/shell script files for each component

### Example plugin.json

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": "Author name"
}
```

## 🛠️ Templates

Agent creation templates are available in each plugin's `agents/templates/` directory:

- `specialist-agent-template.md` - For specialist agents
- `task-agent-template.md` - For task execution agents

## 📚 References

- [Claude Code Official Documentation](https://github.com/anthropics/claude-code)
- For plugin development details, refer to `/create-agent` and `/create-command` commands

