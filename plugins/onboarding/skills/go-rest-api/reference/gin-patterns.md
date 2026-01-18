# Gin Framework Patterns

## Basic Setup

```go
package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default() // Includes Logger and Recovery middleware

    // Custom middleware
    r.Use(corsMiddleware())

    // Routes
    r.GET("/health", healthHandler)

    // API group with auth
    api := r.Group("/api/v1")
    api.Use(authMiddleware())
    {
        api.GET("/users", getUsers)
        api.POST("/users", createUser)
        api.GET("/users/:id", getUser)
        api.PUT("/users/:id", updateUser)
        api.DELETE("/users/:id", deleteUser)
    }

    r.Run(":8080")
}
```

## Handler Pattern

```go
func getUser(c *gin.Context) {
    id := c.Param("id")

    user, err := userService.GetByID(id)
    if err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "user not found"})
        return
    }

    c.JSON(http.StatusOK, user)
}
```

## Request Binding

```go
type CreateUserRequest struct {
    Name  string `json:"name" binding:"required"`
    Email string `json:"email" binding:"required,email"`
}

func createUser(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    // ...
}
```

## Middleware Pattern

```go
func authMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{
                "error": "missing token",
            })
            return
        }
        // Validate token...
        c.Set("userID", userID) // Store in context
        c.Next()
    }
}
```

## Error Handling

```go
// Centralized error handling
func errorHandler() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()

        if len(c.Errors) > 0 {
            err := c.Errors.Last()
            c.JSON(http.StatusInternalServerError, gin.H{
                "error": err.Error(),
            })
        }
    }
}
```

## Query Parameters

```go
func listUsers(c *gin.Context) {
    page := c.DefaultQuery("page", "1")
    limit := c.DefaultQuery("limit", "10")
    search := c.Query("search") // Returns "" if not present
    // ...
}
```

## Key Detection Patterns

```bash
# Find Gin initialization
grep -rn "gin.Default\|gin.New" --include="*.go"

# Find route registrations
grep -rn "r\.GET\|r\.POST\|r\.PUT\|r\.DELETE\|\.GET\|\.POST" --include="*.go"

# Find middleware usage
grep -rn "\.Use(" --include="*.go"

# Find groups
grep -rn "\.Group(" --include="*.go"

# Find handlers
grep -rn "func.*\*gin\.Context" --include="*.go"

# Find binding
grep -rn "ShouldBind\|ShouldBindJSON\|Bind" --include="*.go"
```
