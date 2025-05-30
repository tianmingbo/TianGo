package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"lGo/rpc/grpc/hello/proto/pb"
	"lGo/rpc/grpc/metadata/pb"
	"log"
	"time"
)

func main() {
	conn, err := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewHelloServiceClient(conn) //  创建客户端

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	res, err := c.SayHello(ctx, &pb2.HelloRequest{Name: "Tian"}) //  调用 SayHello 方法
	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}
	fmt.Println("Response from server:", res.Message)
}
