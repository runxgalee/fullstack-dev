---
name: go-rest-api
description: Analyze Go REST API projects using Echo, Gin, Chi, Fiber, or standard net/http. Use when onboarding to Go web APIs, understanding routing patterns, analyzing middleware chains, reviewing handler implementations, examining request/response handling, identifying authentication patterns, and generating API endpoint documentation.
context: fork
agent: go-specialist
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Task
  - Write
  - WebFetch
  - WebSearch
---

## Purpose

Provide comprehensive analysis of Go REST API projects to help developers quickly understand API structure, routing, middleware, and handler patterns. This skill specializes in popular Go web frameworks: Echo, Gin, Chi, Fiber, and standard library net/http.

## When to Use

Use this skill when you need to:

- **Onboard to a Go REST API** - Understand the full API structure and endpoints
- **Analyze routing patterns** - Map out all routes, groups, and URL parameters
- **Review middleware chains** - Understand request processing pipeline
- **Examine handler implementations** - Understand request/response handling
- **Identify authentication/authorization** - Find auth patterns (JWT, sessions, API keys)
- **Document API endpoints** - Generate endpoint documentation
- **Understand error handling** - Review error response patterns
- **Analyze validation** - Find request validation logic

## Framework Detection

### Identifying the Framework

Check `go.mod` for these imports:

| Framework | Import Path | Documentation |
|-----------|-------------|---------------|
| Echo | `github.com/labstack/echo/v4` | echo.labstack.com |
| Gin | `github.com/gin-gonic/gin` | gin-gonic.com |
| Chi | `github.com/go-chi/chi/v5` | go-chi.io |
| Fiber | `github.com/gofiber/fiber/v2` | gofiber.io |
| net/http | (standard library) | pkg.go.dev/net/http |

```bash
# Detect framework from go.mod
grep -E "(echo|gin-gonic|go-chi|gofiber)" go.mod
```

## Framework-Specific Patterns

### Echo Framework

See `reference/echo-patterns.md` for detailed patterns.

**Key concepts:**
- `e.GET()`, `e.POST()`, etc. for route registration
- `echo.Context` for request/response handling
- `e.Group()` for route grouping
- `e.Use()` for middleware registration

**Route detection:**
```bash
# Find Echo route registrations
grep -rn "\.GET\|\.POST\|\.PUT\|\.DELETE\|\.PATCH" --include="*.go"

# Find Echo middleware
grep -rn "\.Use(" --include="*.go"

# Find route groups
grep -rn "\.Group(" --include="*.go"
```

### Gin Framework

See `reference/gin-patterns.md` for detailed patterns.

**Key concepts:**
- `r.GET()`, `r.POST()`, etc. for route registration
- `gin.Context` for request/response handling
- `r.Group()` for route grouping
- `r.Use()` for middleware registration

**Route detection:**
```bash
# Find Gin route registrations
grep -rn "\.GET\|\.POST\|\.PUT\|\.DELETE\|\.PATCH" --include="*.go"

# Find Gin middleware
grep -rn "\.Use(" --include="*.go"

# Find route groups
grep -rn "\.Group(" --include="*.go"
```

### Chi Framework

See `reference/chi-patterns.md` for detailed patterns.

**Key concepts:**
- `r.Get()`, `r.Post()`, etc. for route registration
- Standard `http.Request` and `http.ResponseWriter`
- `r.Route()` for sub-routers
- `r.Use()` for middleware

**Route detection:**
```bash
# Find Chi route registrations
grep -rn "\.Get\|\.Post\|\.Put\|\.Delete\|\.Patch" --include="*.go"

# Find Chi middleware
grep -rn "\.Use(" --include="*.go"

# Find sub-routers
grep -rn "\.Route(" --include="*.go"
```

### Fiber Framework

See `reference/fiber-patterns.md` for detailed patterns.

**Key concepts:**
- `app.Get()`, `app.Post()`, etc. for route registration
- `fiber.Ctx` for request/response handling
- `app.Group()` for route grouping
- `app.Use()` for middleware

**Route detection:**
```bash
# Find Fiber route registrations
grep -rn "\.Get\|\.Post\|\.Put\|\.Delete\|\.Patch" --include="*.go"

# Find Fiber middleware
grep -rn "\.Use(" --include="*.go"
```

## Analysis Checklist

### 1. Entry Point Analysis

```bash
# Find main.go and server initialization
find . -name "main.go" -type f

# Find where router/engine is created
grep -rn "echo.New\|gin.Default\|gin.New\|chi.NewRouter\|fiber.New" --include="*.go"
```

### 2. Route Mapping

Generate a complete route map:

```bash
# Find all route registrations across frameworks
grep -rn "\.GET\|\.POST\|\.PUT\|\.DELETE\|\.PATCH\|\.Get\|\.Post\|\.Put\|\.Delete\|\.Patch" --include="*.go" | grep -v "_test.go"
```

### 3. Middleware Analysis

```bash
# Find middleware registrations
grep -rn "\.Use(" --include="*.go"

# Find custom middleware definitions
grep -rn "func.*Middleware\|func.*Handler.*http" --include="*.go"
```

### 4. Handler Functions

```bash
# Echo handlers (echo.Context)
grep -rn "func.*echo\.Context" --include="*.go"

# Gin handlers (gin.Context)
grep -rn "func.*gin\.Context" --include="*.go"

# Chi/net/http handlers
grep -rn "func.*http\.ResponseWriter.*http\.Request" --include="*.go"

# Fiber handlers (fiber.Ctx)
grep -rn "func.*fiber\.Ctx" --include="*.go"
```

### 5. Request/Response Patterns

```bash
# JSON binding
grep -rn "\.Bind\|\.ShouldBind\|\.BodyParser\|json\.Unmarshal" --include="*.go"

# JSON responses
grep -rn "\.JSON\|\.JSONPretty\|json\.Marshal" --include="*.go"

# Error responses
grep -rn "\.Error\|\.AbortWithError\|\.AbortWithStatusJSON" --include="*.go"
```

### 6. Authentication Patterns

```bash
# JWT related
grep -rn "jwt\|JWT\|token\|Token\|Bearer" --include="*.go"

# Session related
grep -rn "session\|Session\|cookie\|Cookie" --include="*.go"

# API key related
grep -rn "apikey\|api-key\|X-API-Key" --include="*.go"
```

### 7. Validation

```bash
# Validator usage
grep -rn "validate\|Validate\|validator" --include="*.go"

# Custom validation
grep -rn "binding:\"required\|validate:\"required" --include="*.go"
```

## Output Format

Generate an API onboarding report with:

### 1. Framework Overview
- Detected framework and version
- Server configuration (port, timeouts, TLS)
- Router setup location

### 2. Route Map (Mermaid)

Generate `docs/api-routes.md` with endpoint documentation:

```markdown
# API Routes

## Endpoints Overview

| Method | Path | Handler | Middleware |
|--------|------|---------|------------|
| GET | /api/v1/users | GetUsers | Auth, Logger |
| POST | /api/v1/users | CreateUser | Auth, Logger |
| GET | /api/v1/users/:id | GetUser | Auth, Logger |

## Route Diagram

\`\`\`mermaid
<!-- See reference/api-routes.mmd -->
\`\`\`
```

### 3. Middleware Chain

Document the middleware stack:
- Global middleware (logging, recovery, CORS)
- Group-specific middleware (auth for /api routes)
- Route-specific middleware

### 4. Handler Patterns

Document common patterns:
- Request binding approach
- Response formatting
- Error handling strategy
- Validation approach

### 5. Authentication Flow

Document auth implementation:
- Auth type (JWT, session, API key)
- Token storage/validation
- Protected routes
- Permission/role handling

### 6. Key Files

Recommended reading order:
1. `main.go` - Entry point and server setup
2. Router setup file - Route definitions
3. Middleware files - Request processing
4. Handler files - Business logic
5. Auth files - Authentication logic

## Common Project Structures

### Flat Structure
```
project/
├── main.go
├── handlers.go
├── middleware.go
├── routes.go
└── models.go
```

### Layered Structure
```
project/
├── cmd/api/main.go
├── internal/
│   ├── handler/
│   ├── middleware/
│   ├── service/
│   └── repository/
├── pkg/
│   └── response/
└── api/routes.go
```

### Domain-Driven Structure
```
project/
├── cmd/api/main.go
├── internal/
│   ├── user/
│   │   ├── handler.go
│   │   ├── service.go
│   │   └── repository.go
│   └── product/
│       ├── handler.go
│       ├── service.go
│       └── repository.go
└── pkg/
    └── middleware/
```
