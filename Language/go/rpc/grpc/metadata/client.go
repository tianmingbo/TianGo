package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/metadata"
	"lGo/rpc/grpc/metadata/pb"
	"log"
	"time"
)

// 客户端全局拦截器，统一添加metadata
func clientInterceptor(ctx context.Context, method string, req, reply interface{}, cc *grpc.ClientConn, invoker grpc.UnaryInvoker, opts ...grpc.CallOption) error {
	// 添加全局元数据（如版本号、时间戳）
	fmt.Println("method: ", method)
	md := metadata.Pairs(
		"client-version", "v1.0.0",
		"request-time", time.Now().Format(time.RFC3339),
	)
	ctx = metadata.NewOutgoingContext(ctx, md)

	// 调用原始方法
	return invoker(ctx, method, req, reply, cc, opts...)
}

func main() {
	conn, err := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithUnaryInterceptor(clientInterceptor))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	//构建metadata
	//md := metadata.Pairs(
	//	"User-agent", "grpc",
	//	"authorization", "Bearer your-token-123",
	//	"client-type", "web")
	md := metadata.New(map[string]string{
		"authorization": "Bearer your-token-123",
		"client-type":   "web"})

	c := pb.NewHelloServiceClient(conn) //  创建客户端

	ctx := metadata.NewOutgoingContext(context.Background(), md)
	var headerMD, trailerMD metadata.MD
	res, err := c.SayHello(ctx, &pb.HelloRequest{Name: "Tian"},
		grpc.Header(&headerMD),
		grpc.Trailer(&trailerMD)) //  调用 SayHello 方法
	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}
	fmt.Println("Response from server:", res.Message)
	// 处理头元数据
	log.Printf("响应头: %v", headerMD)
	// 处理尾随元数据
	log.Printf("尾随元数据: %v", trailerMD)
}
