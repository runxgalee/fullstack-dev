---
name: database-schema
description: Analyze database schema and migrations for onboarding. Use when exploring schema folders, understanding table structures, analyzing migration files (golang-migrate, goose, sql-migrate, atlas), reviewing foreign key relationships, identifying indexes, understanding data models, and generating database documentation. Supports SQL migration files and Go-based migration tools.
context: fork
agent: database-architect
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Task
---

## Purpose

Analyze database schemas and migration files to help developers understand the data model quickly. This skill focuses on Go-based migration tools and SQL schema files, identifying table structures, relationships, and dependencies.

## When to Use

Use this skill when you need to:

- **Understand database structure** - Get an overview of all tables and their relationships
- **Analyze migrations** - Review migration history and understand schema evolution
- **Find schema files** - Locate schema/, migrations/, or db/ directories
- **Map table relationships** - Identify foreign keys and dependencies between tables
- **Review indexes** - Understand query optimization through index analysis
- **Generate ER diagrams** - Create visual representations of the data model
- **Onboard to a database** - Learn the data model for a new project

## Key Information

### Schema Location Patterns

Common locations for schema and migration files:

```
project/
├── db/
│   ├── migrations/          # golang-migrate, goose
│   │   ├── 000001_create_users.up.sql
│   │   ├── 000001_create_users.down.sql
│   │   └── ...
│   └── schema.sql           # Full schema dump
├── migrations/              # Alternative location
├── schema/                  # Schema definitions
├── sql/
│   └── migrations/
└── internal/
    └── db/
        └── migrations/
```

### Go Migration Tools

#### 1. golang-migrate

**File Pattern:** `{version}_{name}.up.sql` / `{version}_{name}.down.sql`

```sql
-- 000001_create_users.up.sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 000001_create_users.down.sql
DROP TABLE IF EXISTS users;
```

**Commands:**
```bash
# List migrations
ls -la migrations/*.sql

# Check migration status
migrate -path ./migrations -database "postgres://..." version
```

#### 2. goose

**File Pattern:** `{version}_{name}.sql` with annotations

```sql
-- +goose Up
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE
);

-- +goose Down
DROP TABLE users;
```

**Commands:**
```bash
# List migrations
goose -dir ./migrations status

# Show migration files
ls migrations/*.sql
```

#### 3. sql-migrate

**File Pattern:** `{version}_{name}.sql` with annotations

```sql
-- +migrate Up
CREATE TABLE users (...);

-- +migrate Down
DROP TABLE users;
```

#### 4. Atlas

**File Pattern:** `schema.hcl` or `*.sql`

```hcl
table "users" {
  schema = schema.public
  column "id" {
    type = bigserial
  }
  column "email" {
    type = varchar(255)
  }
  primary_key {
    columns = [column.id]
  }
}
```

### Analysis Checklist

When analyzing a database schema:

1. **Find Schema Files**
   ```bash
   # Find migration directories
   find . -type d -name "migrations" -o -name "schema" -o -name "db"

   # Find SQL files
   find . -name "*.sql" -type f

   # Find HCL files (Atlas)
   find . -name "*.hcl" -type f
   ```

2. **Identify Tables**
   ```bash
   # Find CREATE TABLE statements
   grep -r "CREATE TABLE" --include="*.sql"

   # List all tables
   grep -rh "CREATE TABLE" --include="*.sql" | sed 's/.*CREATE TABLE \(IF NOT EXISTS \)\?//' | cut -d'(' -f1
   ```

3. **Map Relationships**
   ```bash
   # Find foreign keys
   grep -r "REFERENCES\|FOREIGN KEY" --include="*.sql"

   # Find indexes
   grep -r "CREATE INDEX\|CREATE UNIQUE INDEX" --include="*.sql"
   ```

4. **Analyze Migration Order**
   ```bash
   # List migrations in order
   ls -1 migrations/*.sql | sort -V
   ```

### Table Relationship Patterns

#### One-to-Many
```sql
CREATE TABLE posts (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    title VARCHAR(255)
);
```

#### Many-to-Many
```sql
CREATE TABLE user_roles (
    user_id BIGINT REFERENCES users(id),
    role_id BIGINT REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);
```

#### Self-Referencing
```sql
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    parent_id BIGINT REFERENCES categories(id),
    name VARCHAR(255)
);
```

### Output Format

Generate a database schema report with:

1. **Schema Overview**
   - Migration tool detected
   - Total number of tables
   - Schema version / latest migration

2. **Table Catalog**
   - Table name
   - Column definitions (name, type, constraints)
   - Primary key
   - Indexes

3. **Relationship Map**
   - Foreign key relationships
   - Dependency order (for inserts/deletes)
   - Circular dependencies (if any)

4. **ER Diagram** (Mermaid format)
   ```mermaid
   erDiagram
       users ||--o{ posts : "has many"
       users ||--o{ user_roles : "has many"
       roles ||--o{ user_roles : "has many"
   ```

5. **Migration History**
   - Chronological list of migrations
   - What each migration changes
   - Recommended reading order

### Common Column Patterns

| Pattern | Description |
|---------|-------------|
| `id BIGSERIAL PRIMARY KEY` | Auto-increment primary key |
| `created_at TIMESTAMP DEFAULT NOW()` | Creation timestamp |
| `updated_at TIMESTAMP` | Last update timestamp |
| `deleted_at TIMESTAMP` | Soft delete marker |
| `*_id BIGINT REFERENCES` | Foreign key reference |
| `status VARCHAR` / `status_enum` | State machine field |
| `metadata JSONB` | Flexible JSON storage |
