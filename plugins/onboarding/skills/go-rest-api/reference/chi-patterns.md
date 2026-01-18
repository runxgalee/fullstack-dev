# Chi Framework Patterns

## Basic Setup

```go
package main

import (
    "net/http"
    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"
)

func main() {
    r := chi.NewRouter()

    // Global middleware
    r.Use(middleware.Logger)
    r.Use(middleware.Recoverer)
    r.Use(middleware.RequestID)

    // Routes
    r.Get("/health", healthHandler)

    // API routes with auth
    r.Route("/api/v1", func(r chi.Router) {
        r.Use(authMiddleware)

        r.Get("/users", getUsers)
        r.Post("/users", createUser)
        r.Route("/users/{id}", func(r chi.Router) {
            r.Get("/", getUser)
            r.Put("/", updateUser)
            r.Delete("/", deleteUser)
        })
    })

    http.ListenAndServe(":8080", r)
}
```

## Handler Pattern

Chi uses standard library signatures:

```go
func getUser(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")

    user, err := userService.GetByID(id)
    if err != nil {
        http.Error(w, "user not found", http.StatusNotFound)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}
```

## Request Binding

```go
type CreateUserRequest struct {
    Name  string `json:"name"`
    Email string `json:"email"`
}

func createUser(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    // Validate...
    // ...
}
```

## Middleware Pattern

```go
func authMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if token == "" {
            http.Error(w, "unauthorized", http.StatusUnauthorized)
            return
        }
        // Validate token...
        ctx := context.WithValue(r.Context(), "userID", userID)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

## Context Values

```go
// Setting context value
ctx := context.WithValue(r.Context(), "userID", userID)
r = r.WithContext(ctx)

// Getting context value
userID := r.Context().Value("userID").(string)
```

## Sub-routers

```go
r.Route("/api/v1", func(r chi.Router) {
    r.Use(authMiddleware)

    // Mount sub-router
    r.Mount("/users", userRouter())
    r.Mount("/products", productRouter())
})

func userRouter() chi.Router {
    r := chi.NewRouter()
    r.Get("/", listUsers)
    r.Post("/", createUser)
    r.Get("/{id}", getUser)
    return r
}
```

## Key Detection Patterns

```bash
# Find Chi initialization
grep -rn "chi.NewRouter" --include="*.go"

# Find route registrations
grep -rn "r\.Get\|r\.Post\|r\.Put\|r\.Delete\|r\.Patch" --include="*.go"

# Find middleware usage
grep -rn "r\.Use(" --include="*.go"

# Find route groups
grep -rn "r\.Route\|\.Route(" --include="*.go"

# Find sub-router mounts
grep -rn "\.Mount(" --include="*.go"

# Find URL params
grep -rn "chi.URLParam" --include="*.go"
```
