package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc"
	pb2 "lGo/rpc/grpc/hello/proto/pb"
	"net"
)

type Server struct {
	pb2.UnimplementedHelloServiceServer //把接口里面的方法全部实现一遍
}

func (s *Server) SayHello(ctx context.Context, req *pb2.HelloRequest) (*pb2.HelloReply, error) {
	return &pb2.HelloReply{Message: "Hello, " + req.Name}, nil
}

func main() {
	listen, err := net.Listen("tcp", ":50051") //监听端口
	if err != nil {
		fmt.Println("failed to listen:", err)
	}
	s := grpc.NewServer()                        //创建grpc服务
	pb2.RegisterHelloServiceServer(s, &Server{}) //注册服务
	fmt.Println("gRPC server listening on :50051")
	if err := s.Serve(listen); err != nil { //启动服务
		fmt.Println("failed to serve:", err)
	}
}
