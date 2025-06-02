package main

import (
	"context"
	"fmt"
	"net"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
	"lGo/rpc/grpc/metadata/pb"
)

// 服务端拦截器（统一验证元数据）
func serverInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
	//metadata解析
	md, ok := metadata.FromIncomingContext(ctx)
	if !ok {
		return nil, status.Errorf(codes.Unauthenticated, "metadata is not provided")
	}
	fmt.Println("metadata: ", md) //val为[]string.  slice类型
	if auth, ok := md["authorization"]; ok {
		token := auth[0]
		if token != "Bearer your-token-123" {
			return nil, status.Errorf(codes.Unauthenticated, "token is invalid")
		}
		fmt.Println("token: ", token)
	}
	//创建响应元数据（头）
	headersMetadata := metadata.Pairs("x-response-code", "200")
	if err := grpc.SendHeader(ctx, headersMetadata); err != nil {
		return nil, err
	}
	// 创建尾随元数据（请求结束时返回）
	trailerMD := metadata.Pairs(
		"x-total-count", "100", // 统计信息
	)
	err := grpc.SetTrailer(ctx, trailerMD)
	if err != nil {
		return nil, err
	}
	return handler(ctx, req)
}

type Server struct {
	pb.UnimplementedHelloServiceServer //把接口里面的方法全部实现一遍
}

func (s *Server) SayHello(ctx context.Context, req *pb.HelloRequest) (*pb.HelloReply, error) {
	return &pb.HelloReply{Message: "Hello, " + req.Name}, nil
}

func main() {
	listen, err := net.Listen("tcp", ":50051")
	if err != nil {
		fmt.Println("failed to listen:", err)
	}
	s := grpc.NewServer(grpc.UnaryInterceptor(serverInterceptor)) //使用拦截器
	pb.RegisterHelloServiceServer(s, &Server{})
	fmt.Println("gRPC server listening on :50051")
	if err := s.Serve(listen); err != nil {
		fmt.Println("failed to serve:", err)
	}
}
