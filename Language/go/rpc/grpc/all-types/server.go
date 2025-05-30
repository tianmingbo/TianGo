// server/types_service.go
package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc"
	"google.golang.org/protobuf/types/known/durationpb"
	"google.golang.org/protobuf/types/known/timestamppb"
	"net"
	"time"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"lGo/rpc/grpc/all-types/pb"
)

type server struct {
	pb.UnimplementedTypesServiceServer
}

func (s *server) TestAllTypes(ctx context.Context, req *pb.AllTypes) (*pb.AllTypes, error) {
	if req == nil {
		return nil, status.Errorf(codes.InvalidArgument, "invalid request")
	}

	//处理特殊类型
	if req.Special != nil {
		req.Special.Timestamp = &timestamppb.Timestamp{
			Seconds: time.Now().Unix(),
			Nanos:   int32(time.Now().Nanosecond()),
		}

		req.Special.Duration = &durationpb.Duration{
			Seconds: 10,
			Nanos:   0,
		}
	}
	return req, nil
}

func main() {
	listen, err := net.Listen("tcp", ":50051")
	if err != nil {
		fmt.Println("failed to listen:", err)
	}
	s := grpc.NewServer()
	pb.RegisterTypesServiceServer(s, &server{})
	fmt.Println("gRPC server listening on :50051")
	if err := s.Serve(listen); err != nil {
		fmt.Println("failed to serve:", err)
	}
}
