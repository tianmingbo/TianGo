package main

import (
	"fmt"
	"net"

	"google.golang.org/grpc"

	"lGo/shop/handle"
	"lGo/shop/proto"
)

func main() {
	listen, err := net.Listen("tcp", ":23333") //监听端口
	if err != nil {
		fmt.Println("failed to listen:", err)
	}
	s := grpc.NewServer()                             //创建grpc服务
	proto.RegisterUserServer(s, &handle.UserServer{}) //注册服务
	fmt.Println("gRPC server listening on :23333")
	if err := s.Serve(listen); err != nil {
		fmt.Println("failed to serve:", err)
	}
}
