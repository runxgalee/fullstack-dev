# gRPC Streaming Patterns

## Streaming Types Overview

| Type | Client | Server | Use Case |
|------|--------|--------|----------|
| Unary | Single request | Single response | Simple CRUD operations |
| Server Streaming | Single request | Multiple responses | List operations, real-time updates |
| Client Streaming | Multiple requests | Single response | File upload, batch processing |
| Bidirectional | Multiple requests | Multiple responses | Chat, live collaboration |

## Proto Definitions

```protobuf
service StreamService {
  // Server streaming: Client sends one request, server sends multiple responses
  rpc ListItems(ListItemsRequest) returns (stream Item);

  // Client streaming: Client sends multiple requests, server sends one response
  rpc UploadItems(stream Item) returns (UploadResponse);

  // Bidirectional streaming: Both sides send multiple messages
  rpc Chat(stream ChatMessage) returns (stream ChatMessage);
}
```

## Server Streaming Implementation

### Server Side

```go
// ListItems implements server-side streaming
func (s *streamServer) ListItems(req *pb.ListItemsRequest, stream pb.StreamService_ListItemsServer) error {
    ctx := stream.Context()

    // Simulate fetching items in batches
    cursor := ""
    for {
        // Check for cancellation
        select {
        case <-ctx.Done():
            return status.Error(codes.Canceled, "client cancelled")
        default:
        }

        // Fetch batch
        items, nextCursor, err := s.itemService.ListBatch(ctx, cursor, 100)
        if err != nil {
            return status.Errorf(codes.Internal, "failed to fetch items: %v", err)
        }

        // Send each item
        for _, item := range items {
            if err := stream.Send(toProtoItem(item)); err != nil {
                return status.Errorf(codes.Internal, "failed to send: %v", err)
            }
        }

        // Check if done
        if nextCursor == "" {
            break
        }
        cursor = nextCursor
    }

    return nil
}
```

### Client Side

```go
// Client consuming server stream
func listItems(ctx context.Context, client pb.StreamServiceClient) error {
    stream, err := client.ListItems(ctx, &pb.ListItemsRequest{})
    if err != nil {
        return err
    }

    for {
        item, err := stream.Recv()
        if err == io.EOF {
            // Stream finished
            break
        }
        if err != nil {
            return err
        }

        // Process item
        fmt.Printf("Received: %v\n", item)
    }

    return nil
}
```

## Client Streaming Implementation

### Server Side

```go
// UploadItems implements client-side streaming
func (s *streamServer) UploadItems(stream pb.StreamService_UploadItemsServer) error {
    var items []*pb.Item
    var totalSize int64

    for {
        item, err := stream.Recv()
        if err == io.EOF {
            // Client finished sending
            // Process all items and send response
            count, err := s.itemService.BulkCreate(stream.Context(), items)
            if err != nil {
                return status.Errorf(codes.Internal, "failed to save items: %v", err)
            }

            return stream.SendAndClose(&pb.UploadResponse{
                ItemCount: int32(count),
                TotalSize: totalSize,
            })
        }
        if err != nil {
            return status.Errorf(codes.Internal, "failed to receive: %v", err)
        }

        items = append(items, item)
        totalSize += int64(len(item.GetData()))
    }
}
```

### Client Side

```go
// Client sending stream
func uploadItems(ctx context.Context, client pb.StreamServiceClient, items []*pb.Item) (*pb.UploadResponse, error) {
    stream, err := client.UploadItems(ctx)
    if err != nil {
        return nil, err
    }

    for _, item := range items {
        if err := stream.Send(item); err != nil {
            return nil, err
        }
    }

    // Close send and receive response
    return stream.CloseAndRecv()
}
```

## Bidirectional Streaming Implementation

### Server Side

```go
// Chat implements bidirectional streaming
func (s *chatServer) Chat(stream pb.ChatService_ChatServer) error {
    // Create channels for managing the connection
    errCh := make(chan error, 1)

    // Handle incoming messages in goroutine
    go func() {
        for {
            msg, err := stream.Recv()
            if err == io.EOF {
                errCh <- nil
                return
            }
            if err != nil {
                errCh <- err
                return
            }

            // Broadcast message to other clients
            s.hub.Broadcast(msg)
        }
    }()

    // Send messages to this client
    msgCh := s.hub.Subscribe(stream.Context())
    for {
        select {
        case <-stream.Context().Done():
            return status.Error(codes.Canceled, "client disconnected")
        case err := <-errCh:
            return err
        case msg := <-msgCh:
            if err := stream.Send(msg); err != nil {
                return err
            }
        }
    }
}
```

### Client Side

```go
// Bidirectional client
func chat(ctx context.Context, client pb.ChatServiceClient) error {
    stream, err := client.Chat(ctx)
    if err != nil {
        return err
    }

    // Receive messages in goroutine
    go func() {
        for {
            msg, err := stream.Recv()
            if err == io.EOF {
                return
            }
            if err != nil {
                log.Printf("receive error: %v", err)
                return
            }
            fmt.Printf("Received: %s\n", msg.GetContent())
        }
    }()

    // Send messages
    scanner := bufio.NewScanner(os.Stdin)
    for scanner.Scan() {
        if err := stream.Send(&pb.ChatMessage{
            Content: scanner.Text(),
        }); err != nil {
            return err
        }
    }

    return stream.CloseSend()
}
```

## Streaming Best Practices

### Context Handling

```go
func (s *server) StreamMethod(stream pb.Service_StreamMethodServer) error {
    ctx := stream.Context()

    for {
        // Always check context
        select {
        case <-ctx.Done():
            return status.FromContextError(ctx.Err()).Err()
        default:
        }

        // Process stream...
    }
}
```

### Flow Control

```go
// Use buffered channels for flow control
func (s *server) StreamWithBackpressure(stream pb.Service_StreamServer) error {
    buffer := make(chan *pb.Item, 100) // Buffer size controls backpressure

    // Producer
    go func() {
        defer close(buffer)
        for item := range s.items {
            select {
            case buffer <- item:
            case <-stream.Context().Done():
                return
            }
        }
    }()

    // Consumer
    for item := range buffer {
        if err := stream.Send(item); err != nil {
            return err
        }
    }
    return nil
}
```

## Key Detection Patterns

```bash
# Find streaming proto definitions
grep -rn "stream " --include="*.proto"

# Find server streaming implementations
grep -rn "_Server\)" --include="*.go"

# Find stream.Send/Recv calls
grep -rn "\.Send\|\.Recv\|\.SendAndClose\|\.CloseAndRecv" --include="*.go"

# Find bidirectional patterns
grep -rn "go func.*Recv\|go func.*stream" --include="*.go"
```
