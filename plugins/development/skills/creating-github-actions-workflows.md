---
name: creating-github-actions-workflows
description: Use when setting up CI/CD pipelines, automating testing and deployment, or needing production-ready GitHub Actions workflows with concurrency control, caching, security, and proper error handling
---

# Creating GitHub Actions Workflows

## Overview

Production-ready GitHub Actions workflows require more than basic trigger-test-deploy patterns. Missing concurrency control causes overlapping deployments. Skipping quality gates allows broken code through. No timeout limits means hanging jobs burn credits indefinitely.

**Core principle:** Build workflows that are secure, efficient, and production-ready from the start.

## When to Use

**Use this skill when:**
- Setting up CI/CD for any application
- Automating testing, building, or deployment
- Creating reusable workflow templates
- Converting from other CI systems (Jenkins, GitLab CI, CircleCI)
- Workflows need to handle production deployments

**Don't use when:**
- Using other CI/CD platforms (adapt patterns, but GitHub Actions specifics won't apply)
- Project has no automated testing needs

## Critical Non-Negotiables

**These MUST be in every workflow. No exceptions:**

1. **Concurrency control** - Prevents race conditions, state corruption, overlapping deploys
   ```yaml
   concurrency:
     group: ${{ github.workflow }}-${{ github.ref }}
     cancel-in-progress: true  # or false for deploys
   ```

2. **Timeout on every job** - Prevents infinite runner usage
   ```yaml
   jobs:
     build:
       timeout-minutes: 15  # Adjust based on job
   ```

3. **Explicit minimal permissions** - Security best practice
   ```yaml
   permissions:
     contents: read  # Only what's needed
   ```

**Missing ANY of these = workflow is not production-ready. Go back and add them.**

## Red Flags - STOP and Fix

If you're creating a workflow and ANY of these are true, STOP and fix them:

- ❌ No `concurrency` block at workflow level
- ❌ Any job without `timeout-minutes`
- ❌ Using default permissions (no `permissions` declared)
- ❌ Running `npm install` instead of `npm ci`
- ❌ No caching for dependencies
- ❌ Deployment job rebuilds instead of using artifacts
- ❌ Secrets hardcoded in workflow file
- ❌ Matrix testing without `fail-fast: false`
- ❌ "It's just a simple workflow" - Simple workflows still need these basics

**All of these mean: Go back and add the missing pieces. Every workflow needs the fundamentals.**

## Essential Components Checklist

Every production workflow should include:

- [ ] **Concurrency control** - Prevent overlapping runs
- [ ] **Timeout limits** - Stop runaway jobs
- [ ] **Explicit permissions** - Least privilege principle
- [ ] **Caching strategy** - Speed up builds
- [ ] **Quality gates** - Lint/type-check before tests
- [ ] **Matrix testing** (if needed) - Test across versions/platforms
- [ ] **Artifact management** - Preserve test reports, coverage
- [ ] **Environment protection** - Manual approvals for production
- [ ] **Error handling** - Fail fast or continue as appropriate

## Quick Reference

| Pattern | YAML Syntax | Purpose |
|---------|-------------|---------|
| Concurrency control | `concurrency: group: ${{ github.workflow }}-${{ github.ref }}` | Prevent overlapping runs per branch |
| Cancel in-progress | `concurrency: cancel-in-progress: true` | Cancel old runs when new one starts |
| Job timeout | `jobs: build: timeout-minutes: 15` | Stop job after time limit |
| Minimal permissions | `permissions: contents: read` | Restrict GITHUB_TOKEN access |
| Dependency caching | `uses: actions/setup-node@v4 with: cache: 'npm'` | Cache dependencies |
| Job dependency | `jobs: deploy: needs: [test, build]` | Run jobs sequentially |
| Conditional execution | `if: github.ref == 'refs/heads/main'` | Run only on specific conditions |
| Matrix testing | `strategy: matrix: node-version: [18, 20, 22]` | Test across multiple versions |
| Continue on error | `strategy: fail-fast: false` | See all matrix failures |
| Environment | `environment: name: production` | Use environment protection rules |
| Manual approval | `environment: name: production` (+ settings) | Require approval in repo settings |
| Artifact upload | `uses: actions/upload-artifact@v4` | Preserve files between jobs |
| Artifact download | `uses: actions/download-artifact@v4` | Use files from previous jobs |

## Production-Ready Workflow Structure

```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# CRITICAL: Add concurrency control
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # Cancel old runs on new push

# Minimal permissions by default
permissions:
  contents: read

jobs:
  quality:
    name: Code Quality
    runs-on: ubuntu-latest
    timeout-minutes: 10  # Always set timeout

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'  # Enable caching

      - run: npm ci

      # Quality gates BEFORE tests
      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run type-check

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: quality  # Run after quality passes
    timeout-minutes: 15

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - run: npm ci

      - name: Run tests
        run: npm test -- --coverage

      # Preserve test results
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/
          retention-days: 30

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: test
    timeout-minutes: 10

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - run: npm ci

      - name: Build
        run: npm run build

      # Share build output with deploy job
      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/

  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    timeout-minutes: 10
    # Only deploy on main branch pushes
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'

    # Use environment for protection rules
    environment:
      name: production
      url: https://myapp.com

    # Deployment needs id-token for OIDC
    permissions:
      id-token: write
      contents: read

    steps:
      - uses: actions/checkout@v4

      # Download build from previous job
      - name: Download build
        uses: actions/download-artifact@v4
        with:
          name: build
          path: dist/

      - name: Deploy
        run: |
          echo "Deploying to production..."
          # Your deployment commands here
```

## Matrix Testing Pattern

```yaml
jobs:
  test:
    name: Test (${{ matrix.os }}, Node ${{ matrix.node }})
    runs-on: ${{ matrix.os }}
    timeout-minutes: 15

    strategy:
      # Don't cancel all jobs if one fails
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [18, 20, 22]
        # Optionally test experimental versions
        include:
          - os: ubuntu-latest
            node: 23
            experimental: true

    # Allow experimental to fail
    continue-on-error: ${{ matrix.experimental == true }}

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'

      - run: npm ci
      - run: npm test

      # Only upload coverage once (not 9 times)
      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.node == 22
        uses: codecov/codecov-action@v4
```

## Language-Specific Patterns

### Node.js

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'npm'  # or 'yarn', 'pnpm'

- run: npm ci  # Use ci for reproducible builds, not npm install
```

### Python

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'

- run: pip install -r requirements.txt
```

### Go

```yaml
- uses: actions/setup-go@v5
  with:
    go-version: '1.23'
    cache: true  # Caches Go modules automatically

# CRITICAL: Always verify go.mod/go.sum integrity
- run: go mod verify
- run: go mod tidy -diff  # Verify no missing/extra deps

- run: go build -v ./...
- run: go test -v -race ./...  # -race detects race conditions
```

**Go-specific best practices:**
- Always include `go mod verify` before build/test
- Use `-race` flag in tests to catch concurrency issues
- Consider `golangci-lint` for code quality checks

### Docker

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: ${{ github.ref == 'refs/heads/main' }}
    tags: myapp:latest
    cache-from: type=gha  # GitHub Actions cache
    cache-to: type=gha,mode=max
```

## Secrets and Security

### Use OIDC Instead of Long-Lived Credentials

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - name: Configure AWS credentials
    uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/GitHubActions
      aws-region: us-east-1

  # Now AWS CLI commands work without storing credentials
```

### Never Hardcode Secrets

```yaml
# ❌ BAD
env:
  API_KEY: sk_live_abc123

# ✅ GOOD
env:
  API_KEY: ${{ secrets.API_KEY }}
```

### Minimize Permissions

```yaml
# ❌ BAD: Uses default permissions (read/write to many things)
jobs:
  build:
    runs-on: ubuntu-latest

# ✅ GOOD: Explicit minimal permissions
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read  # Only what's needed
```

## Deployment Patterns

### With Environment Protection

```yaml
deploy:
  environment:
    name: production
    url: https://myapp.com
  # In repo settings, configure:
  # - Required reviewers
  # - Wait timer
  # - Deployment branches
```

### With Rollback Capability

```yaml
deploy:
  steps:
    - name: Get current version
      id: current
      run: |
        CURRENT=$(curl https://myapp.com/version)
        echo "version=$CURRENT" >> $GITHUB_OUTPUT

    - name: Deploy new version
      id: deploy
      run: ./deploy.sh

    - name: Health check
      id: health
      run: |
        for i in {1..5}; do
          if curl -f https://myapp.com/health; then
            echo "Health check passed"
            exit 0
          fi
          sleep 10
        done
        echo "Health check failed"
        exit 1

    - name: Rollback on failure
      if: failure()
      run: ./deploy.sh ${{ steps.current.outputs.version }}
```

## Common Mistakes

| Mistake | Why It's Bad | Fix |
|---------|--------------|-----|
| No concurrency control | Multiple deploys conflict, corrupt state | Add `concurrency` group with `cancel-in-progress` |
| No timeout | Hanging jobs waste runner minutes | Always set `timeout-minutes` on jobs |
| Using `npm install` | Non-reproducible builds | Use `npm ci` in CI |
| Installing deps in every job | Wastes time and money | Use caching or artifacts between jobs |
| Running tests twice | Test once in test job, coverage in same run | Combine: `npm test -- --coverage` |
| Quality checks after tests | Waste time running tests on broken code | Lint and type-check BEFORE tests |
| Default permissions | Gives GITHUB_TOKEN too much access | Set minimal `permissions` explicitly |
| Secrets in code | Security vulnerability | Always use `${{ secrets.NAME }}` |
| No fail-fast: false in matrix | One failure hides others | Set `fail-fast: false` to see all failures |
| Re-building in deploy job | Deploy what was tested, not new build | Use artifacts to pass build between jobs |
| No environment protection | Direct to prod without approval | Use `environment` with protection rules |
| Coverage on all matrix combos | 9x uploads of same coverage | Use `if: matrix.os == 'ubuntu-latest' && matrix.node == 22` |

## Monitoring and Debugging

### Add Status Badges

```markdown
![CI Status](https://github.com/user/repo/actions/workflows/ci.yml/badge.svg)
```

### Enable Debug Logging

```yaml
# In workflow file
- name: Debug
  run: echo "::debug::Detailed debug message"

# Or set in repo secrets:
# ACTIONS_RUNNER_DEBUG = true
# ACTIONS_STEP_DEBUG = true
```

### Failure Notifications

```yaml
notify:
  if: failure()
  runs-on: ubuntu-latest
  steps:
    - uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## Performance Optimization

### Cache Dependencies

```yaml
# Automatic for most setup actions
- uses: actions/setup-node@v4
  with:
    cache: 'npm'

# Manual caching
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### Use Artifacts for Build Outputs

```yaml
# Build job
- uses: actions/upload-artifact@v4
  with:
    name: build
    path: dist/

# Deploy job (don't rebuild!)
- uses: actions/download-artifact@v4
  with:
    name: build
    path: dist/
```

### Self-Hosted Runners for Heavy Workloads

```yaml
jobs:
  build:
    runs-on: self-hosted  # Your own infrastructure
```

## Workflow Checklist

Before committing a new workflow:

- [ ] Concurrency control configured
- [ ] All jobs have timeout-minutes
- [ ] Permissions explicitly set (minimal)
- [ ] Caching enabled for dependencies
- [ ] Quality gates (lint, type-check) run first
- [ ] Tests run before build
- [ ] Build artifacts uploaded
- [ ] Deploy uses artifacts (doesn't rebuild)
- [ ] Environment protection for production
- [ ] Secrets use `${{ secrets.NAME }}`
- [ ] Matrix includes `fail-fast: false`
- [ ] Coverage uploads only once per run
- [ ] Status badge added to README
- [ ] Deployment has health checks

## Further Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Action Marketplace](https://github.com/marketplace?type=actions)
- [Security Hardening Guide](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [OIDC with Cloud Providers](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-cloud-providers)
