# Echo Framework Patterns

## Basic Setup

```go
package main

import (
    "github.com/labstack/echo/v4"
    "github.com/labstack/echo/v4/middleware"
)

func main() {
    e := echo.New()

    // Global middleware
    e.Use(middleware.Logger())
    e.Use(middleware.Recover())
    e.Use(middleware.CORS())

    // Routes
    e.GET("/health", healthHandler)

    // API group with auth
    api := e.Group("/api/v1")
    api.Use(authMiddleware)

    api.GET("/users", getUsers)
    api.POST("/users", createUser)
    api.GET("/users/:id", getUser)

    e.Logger.Fatal(e.Start(":8080"))
}
```

## Handler Pattern

```go
func getUser(c echo.Context) error {
    id := c.Param("id")

    user, err := userService.GetByID(id)
    if err != nil {
        return echo.NewHTTPError(http.StatusNotFound, "user not found")
    }

    return c.JSON(http.StatusOK, user)
}
```

## Request Binding

```go
type CreateUserRequest struct {
    Name  string `json:"name" validate:"required"`
    Email string `json:"email" validate:"required,email"`
}

func createUser(c echo.Context) error {
    req := new(CreateUserRequest)
    if err := c.Bind(req); err != nil {
        return echo.NewHTTPError(http.StatusBadRequest, err.Error())
    }
    if err := c.Validate(req); err != nil {
        return echo.NewHTTPError(http.StatusBadRequest, err.Error())
    }
    // ...
}
```

## Middleware Pattern

```go
func authMiddleware(next echo.HandlerFunc) echo.HandlerFunc {
    return func(c echo.Context) error {
        token := c.Request().Header.Get("Authorization")
        if token == "" {
            return echo.NewHTTPError(http.StatusUnauthorized, "missing token")
        }
        // Validate token...
        return next(c)
    }
}
```

## Error Handling

```go
// Custom error handler
e.HTTPErrorHandler = func(err error, c echo.Context) {
    code := http.StatusInternalServerError
    message := "internal server error"

    if he, ok := err.(*echo.HTTPError); ok {
        code = he.Code
        message = he.Message.(string)
    }

    c.JSON(code, map[string]string{"error": message})
}
```

## Key Detection Patterns

```bash
# Find Echo initialization
grep -rn "echo.New()" --include="*.go"

# Find route registrations
grep -rn "e\.GET\|e\.POST\|e\.PUT\|e\.DELETE" --include="*.go"

# Find middleware usage
grep -rn "e\.Use\|\.Use(" --include="*.go"

# Find groups
grep -rn "\.Group(" --include="*.go"

# Find handlers
grep -rn "func.*echo\.Context" --include="*.go"
```
