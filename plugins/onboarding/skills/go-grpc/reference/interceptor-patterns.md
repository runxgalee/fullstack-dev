# gRPC Interceptor Patterns

## Interceptor Types

### Unary Interceptor Signature

```go
type UnaryServerInterceptor func(
    ctx context.Context,
    req interface{},
    info *grpc.UnaryServerInfo,
    handler grpc.UnaryHandler,
) (interface{}, error)
```

### Stream Interceptor Signature

```go
type StreamServerInterceptor func(
    srv interface{},
    ss grpc.ServerStream,
    info *grpc.StreamServerInfo,
    handler grpc.StreamHandler,
) error
```

## Common Interceptors

### Recovery Interceptor

```go
// internal/interceptor/recovery.go
package interceptor

import (
    "context"
    "runtime/debug"

    "google.golang.org/grpc"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

func Recovery() grpc.UnaryServerInterceptor {
    return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (resp interface{}, err error) {
        defer func() {
            if r := recover(); r != nil {
                debug.PrintStack()
                err = status.Errorf(codes.Internal, "panic: %v", r)
            }
        }()
        return handler(ctx, req)
    }
}

func StreamRecovery() grpc.StreamServerInterceptor {
    return func(srv interface{}, ss grpc.ServerStream, info *grpc.StreamServerInfo, handler grpc.StreamHandler) (err error) {
        defer func() {
            if r := recover(); r != nil {
                debug.PrintStack()
                err = status.Errorf(codes.Internal, "panic: %v", r)
            }
        }()
        return handler(srv, ss)
    }
}
```

### Logging Interceptor

```go
// internal/interceptor/logging.go
package interceptor

import (
    "context"
    "time"

    "go.uber.org/zap"
    "google.golang.org/grpc"
    "google.golang.org/grpc/status"
)

func Logging(logger *zap.Logger) grpc.UnaryServerInterceptor {
    return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
        start := time.Now()

        resp, err := handler(ctx, req)

        duration := time.Since(start)
        st, _ := status.FromError(err)

        logger.Info("gRPC request",
            zap.String("method", info.FullMethod),
            zap.Duration("duration", duration),
            zap.String("code", st.Code().String()),
        )

        return resp, err
    }
}
```

### Authentication Interceptor

```go
// internal/interceptor/auth.go
package interceptor

import (
    "context"
    "strings"

    "google.golang.org/grpc"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/metadata"
    "google.golang.org/grpc/status"
)

type contextKey string

const userKey contextKey = "user"

func Auth(authService AuthService) grpc.UnaryServerInterceptor {
    return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
        // Skip auth for certain methods
        if isPublicMethod(info.FullMethod) {
            return handler(ctx, req)
        }

        // Extract metadata
        md, ok := metadata.FromIncomingContext(ctx)
        if !ok {
            return nil, status.Error(codes.Unauthenticated, "no metadata provided")
        }

        // Get authorization header
        authHeaders := md.Get("authorization")
        if len(authHeaders) == 0 {
            return nil, status.Error(codes.Unauthenticated, "no authorization header")
        }

        // Parse Bearer token
        token := strings.TrimPrefix(authHeaders[0], "Bearer ")
        if token == authHeaders[0] {
            return nil, status.Error(codes.Unauthenticated, "invalid authorization format")
        }

        // Validate token
        user, err := authService.ValidateToken(ctx, token)
        if err != nil {
            return nil, status.Error(codes.Unauthenticated, "invalid token")
        }

        // Add user to context
        ctx = context.WithValue(ctx, userKey, user)
        return handler(ctx, req)
    }
}

// Helper to get user from context
func UserFromContext(ctx context.Context) *User {
    user, _ := ctx.Value(userKey).(*User)
    return user
}

func isPublicMethod(method string) bool {
    publicMethods := []string{
        "/health.v1.HealthService/Check",
        "/auth.v1.AuthService/Login",
    }
    for _, m := range publicMethods {
        if m == method {
            return true
        }
    }
    return false
}
```

### Validation Interceptor

```go
// internal/interceptor/validation.go
package interceptor

import (
    "context"

    "google.golang.org/grpc"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

type Validator interface {
    Validate() error
}

func Validation() grpc.UnaryServerInterceptor {
    return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
        if v, ok := req.(Validator); ok {
            if err := v.Validate(); err != nil {
                return nil, status.Errorf(codes.InvalidArgument, "validation failed: %v", err)
            }
        }
        return handler(ctx, req)
    }
}
```

### Rate Limiting Interceptor

```go
// internal/interceptor/ratelimit.go
package interceptor

import (
    "context"

    "golang.org/x/time/rate"
    "google.golang.org/grpc"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

func RateLimit(limiter *rate.Limiter) grpc.UnaryServerInterceptor {
    return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
        if !limiter.Allow() {
            return nil, status.Error(codes.ResourceExhausted, "rate limit exceeded")
        }
        return handler(ctx, req)
    }
}
```

### Request ID Interceptor

```go
// internal/interceptor/requestid.go
package interceptor

import (
    "context"

    "github.com/google/uuid"
    "google.golang.org/grpc"
    "google.golang.org/grpc/metadata"
)

const requestIDKey = "x-request-id"

func RequestID() grpc.UnaryServerInterceptor {
    return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
        md, ok := metadata.FromIncomingContext(ctx)
        if !ok {
            md = metadata.New(nil)
        }

        requestID := ""
        if ids := md.Get(requestIDKey); len(ids) > 0 {
            requestID = ids[0]
        } else {
            requestID = uuid.New().String()
        }

        // Add to outgoing context
        ctx = metadata.AppendToOutgoingContext(ctx, requestIDKey, requestID)

        // Set response header
        grpc.SetHeader(ctx, metadata.Pairs(requestIDKey, requestID))

        return handler(ctx, req)
    }
}
```

## Chaining Interceptors

```go
// Order matters! Recovery should be first (outermost)
s := grpc.NewServer(
    grpc.ChainUnaryInterceptor(
        interceptor.Recovery(),      // 1. Catch panics
        interceptor.RequestID(),     // 2. Add request ID
        interceptor.Logging(logger), // 3. Log request
        interceptor.RateLimit(limiter), // 4. Rate limit
        interceptor.Auth(authSvc),   // 5. Authenticate
        interceptor.Validation(),    // 6. Validate request
    ),
)
```

## Key Detection Patterns

```bash
# Find interceptor definitions
grep -rn "func.*Interceptor\|UnaryServerInterceptor\|StreamServerInterceptor" --include="*.go"

# Find interceptor chain setup
grep -rn "ChainUnaryInterceptor\|ChainStreamInterceptor" --include="*.go"

# Find metadata usage
grep -rn "metadata.FromIncomingContext\|metadata.FromOutgoingContext" --include="*.go"

# Find status code usage
grep -rn "status.Error\|status.Errorf\|codes\." --include="*.go"
```
