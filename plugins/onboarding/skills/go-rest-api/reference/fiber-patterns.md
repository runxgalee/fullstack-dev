# Fiber Framework Patterns

## Basic Setup

```go
package main

import (
    "github.com/gofiber/fiber/v2"
    "github.com/gofiber/fiber/v2/middleware/cors"
    "github.com/gofiber/fiber/v2/middleware/logger"
    "github.com/gofiber/fiber/v2/middleware/recover"
)

func main() {
    app := fiber.New(fiber.Config{
        ErrorHandler: customErrorHandler,
    })

    // Global middleware
    app.Use(logger.New())
    app.Use(recover.New())
    app.Use(cors.New())

    // Routes
    app.Get("/health", healthHandler)

    // API group with auth
    api := app.Group("/api/v1")
    api.Use(authMiddleware)

    api.Get("/users", getUsers)
    api.Post("/users", createUser)
    api.Get("/users/:id", getUser)
    api.Put("/users/:id", updateUser)
    api.Delete("/users/:id", deleteUser)

    app.Listen(":8080")
}
```

## Handler Pattern

```go
func getUser(c *fiber.Ctx) error {
    id := c.Params("id")

    user, err := userService.GetByID(id)
    if err != nil {
        return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
            "error": "user not found",
        })
    }

    return c.JSON(user)
}
```

## Request Binding

```go
type CreateUserRequest struct {
    Name  string `json:"name"`
    Email string `json:"email"`
}

func createUser(c *fiber.Ctx) error {
    req := new(CreateUserRequest)
    if err := c.BodyParser(req); err != nil {
        return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
            "error": err.Error(),
        })
    }
    // Validate...
    // ...
    return c.Status(fiber.StatusCreated).JSON(user)
}
```

## Middleware Pattern

```go
func authMiddleware(c *fiber.Ctx) error {
    token := c.Get("Authorization")
    if token == "" {
        return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
            "error": "missing token",
        })
    }
    // Validate token...
    c.Locals("userID", userID)
    return c.Next()
}
```

## Context Locals

```go
// Setting locals
c.Locals("userID", userID)

// Getting locals
userID := c.Locals("userID").(string)
```

## Query Parameters

```go
func listUsers(c *fiber.Ctx) error {
    page := c.QueryInt("page", 1)
    limit := c.QueryInt("limit", 10)
    search := c.Query("search", "")
    // ...
}
```

## Error Handler

```go
func customErrorHandler(c *fiber.Ctx, err error) error {
    code := fiber.StatusInternalServerError
    message := "internal server error"

    if e, ok := err.(*fiber.Error); ok {
        code = e.Code
        message = e.Message
    }

    return c.Status(code).JSON(fiber.Map{
        "error": message,
    })
}
```

## Static Files

```go
// Serve static files
app.Static("/", "./public")

// Serve single file
app.Get("/favicon.ico", func(c *fiber.Ctx) error {
    return c.SendFile("./public/favicon.ico")
})
```

## Key Detection Patterns

```bash
# Find Fiber initialization
grep -rn "fiber.New" --include="*.go"

# Find route registrations
grep -rn "app\.Get\|app\.Post\|app\.Put\|app\.Delete\|\.Get\|\.Post" --include="*.go"

# Find middleware usage
grep -rn "app\.Use\|\.Use(" --include="*.go"

# Find groups
grep -rn "\.Group(" --include="*.go"

# Find handlers
grep -rn "func.*\*fiber\.Ctx" --include="*.go"

# Find body parsing
grep -rn "BodyParser\|c\.Body" --include="*.go"
```
