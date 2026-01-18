# gRPC Server Patterns

## Basic Server Setup

### Main Entry Point

```go
// cmd/server/main.go
package main

import (
    "log"
    "net"

    "google.golang.org/grpc"
    "google.golang.org/grpc/reflection"

    pb "myapp/gen/go/user/v1"
    "myapp/internal/server"
    "myapp/internal/interceptor"
)

func main() {
    lis, err := net.Listen("tcp", ":50051")
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }

    // Create server with interceptors
    s := grpc.NewServer(
        grpc.ChainUnaryInterceptor(
            interceptor.Recovery(),
            interceptor.Logging(),
            interceptor.Auth(),
        ),
        grpc.ChainStreamInterceptor(
            interceptor.StreamRecovery(),
            interceptor.StreamLogging(),
        ),
    )

    // Register services
    pb.RegisterUserServiceServer(s, server.NewUserServer())

    // Enable reflection for debugging
    reflection.Register(s)

    log.Printf("server listening at %v", lis.Addr())
    if err := s.Serve(lis); err != nil {
        log.Fatalf("failed to serve: %v", err)
    }
}
```

## Service Implementation

### Unary RPC

```go
// internal/server/user_server.go
package server

import (
    "context"

    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"

    pb "myapp/gen/go/user/v1"
    "myapp/internal/service"
)

type userServer struct {
    pb.UnimplementedUserServiceServer
    userService *service.UserService
}

func NewUserServer(userSvc *service.UserService) pb.UserServiceServer {
    return &userServer{userService: userSvc}
}

// GetUser implements the GetUser RPC
func (s *userServer) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.GetUserResponse, error) {
    // Validate request
    if req.GetId() == "" {
        return nil, status.Error(codes.InvalidArgument, "id is required")
    }

    // Call service layer
    user, err := s.userService.GetByID(ctx, req.GetId())
    if err != nil {
        if errors.Is(err, service.ErrNotFound) {
            return nil, status.Errorf(codes.NotFound, "user %s not found", req.GetId())
        }
        return nil, status.Errorf(codes.Internal, "failed to get user: %v", err)
    }

    return &pb.GetUserResponse{
        User: toProtoUser(user),
    }, nil
}

// CreateUser implements the CreateUser RPC
func (s *userServer) CreateUser(ctx context.Context, req *pb.CreateUserRequest) (*pb.CreateUserResponse, error) {
    user, err := s.userService.Create(ctx, &service.CreateUserParams{
        Email: req.GetEmail(),
        Name:  req.GetName(),
    })
    if err != nil {
        if errors.Is(err, service.ErrDuplicate) {
            return nil, status.Error(codes.AlreadyExists, "user already exists")
        }
        return nil, status.Errorf(codes.Internal, "failed to create user: %v", err)
    }

    return &pb.CreateUserResponse{User: toProtoUser(user)}, nil
}
```

### Server Streaming

```go
// ListUsers implements server streaming
func (s *userServer) ListUsers(req *pb.ListUsersRequest, stream pb.UserService_ListUsersServer) error {
    ctx := stream.Context()

    // Get users from service
    users, err := s.userService.List(ctx, int(req.GetPageSize()))
    if err != nil {
        return status.Errorf(codes.Internal, "failed to list users: %v", err)
    }

    // Stream each user
    for _, user := range users {
        // Check if client cancelled
        if ctx.Err() != nil {
            return status.Error(codes.Canceled, "client cancelled")
        }

        if err := stream.Send(toProtoUser(user)); err != nil {
            return status.Errorf(codes.Internal, "failed to send user: %v", err)
        }
    }

    return nil
}
```

### Client Streaming

```go
// CreateUsers implements client streaming
func (s *userServer) CreateUsers(stream pb.UserService_CreateUsersServer) error {
    var created int32

    for {
        req, err := stream.Recv()
        if err == io.EOF {
            // Client finished sending
            return stream.SendAndClose(&pb.CreateUsersResponse{
                CreatedCount: created,
            })
        }
        if err != nil {
            return status.Errorf(codes.Internal, "failed to receive: %v", err)
        }

        // Create user
        _, err = s.userService.Create(stream.Context(), &service.CreateUserParams{
            Email: req.GetEmail(),
            Name:  req.GetName(),
        })
        if err != nil {
            // Log error but continue processing
            continue
        }
        created++
    }
}
```

### Bidirectional Streaming

```go
// Chat implements bidirectional streaming
func (s *chatServer) Chat(stream pb.ChatService_ChatServer) error {
    for {
        msg, err := stream.Recv()
        if err == io.EOF {
            return nil
        }
        if err != nil {
            return status.Errorf(codes.Internal, "failed to receive: %v", err)
        }

        // Process message and send response
        response := &pb.ChatMessage{
            UserId:  msg.GetUserId(),
            Content: fmt.Sprintf("Echo: %s", msg.GetContent()),
        }

        if err := stream.Send(response); err != nil {
            return status.Errorf(codes.Internal, "failed to send: %v", err)
        }
    }
}
```

## Proto to Domain Conversion

```go
// Conversion helpers
func toProtoUser(u *domain.User) *pb.User {
    return &pb.User{
        Id:        u.ID,
        Email:     u.Email,
        Name:      u.Name,
        CreatedAt: timestamppb.New(u.CreatedAt),
    }
}

func toDomainUser(u *pb.User) *domain.User {
    return &domain.User{
        ID:        u.GetId(),
        Email:     u.GetEmail(),
        Name:      u.GetName(),
        CreatedAt: u.GetCreatedAt().AsTime(),
    }
}
```

## Key Detection Patterns

```bash
# Find server structs
grep -rn "type.*Server struct" --include="*.go"

# Find service implementations
grep -rn "func.*Server\).*context.Context" --include="*.go"

# Find server registration
grep -rn "Register.*Server" --include="*.go"

# Find stream handlers
grep -rn "func.*Server\).*stream\|_Server\)" --include="*.go"

# Find grpc.NewServer
grep -rn "grpc.NewServer" --include="*.go"
```
