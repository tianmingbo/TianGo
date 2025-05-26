package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"io"
	"lGo/rpc/grpc/stream/pb"
	"log"
	"net"
	"time"
)

type server struct {
	pb.UnimplementedChatServiceServer
	counter int32 //消息计数器
}

func (s *server) SendMessage(ctx context.Context, req *pb.MessageRequest) (*pb.MessageResponse, error) {
	fmt.Printf("received %s from %s", req.Content, req.Sender)
	time.Sleep(100 * time.Millisecond)

	return &pb.MessageResponse{
		Content:  "received: " + req.Content,
		Receiver: req.Sender,
		Seq:      1,
	}, nil
}

// 客户端流
func (s *server) SendStream(stream pb.ChatService_SendStreamServer) error {
	var (
		totalMessages int32
		totalBytes    int32
	)
	for {
		req, err := stream.Recv()
		if err == io.EOF {
			return stream.SendAndClose(&pb.StatsResponse{TotalMessages: totalMessages, TotalBytes: totalBytes})
		}
		if err != nil {
			log.Printf("receive message err,%v", err)
			return status.Errorf(codes.Internal, "receive message err,%v", err)
		}
		log.Printf("received message #%d: %s from %s", totalMessages+1, req.Content, req.Sender)
		totalMessages++
		totalBytes += int32(len(req.Content))
	}
}

// 服务端流
func (s *server) ReceiveStream(req *pb.MessageRequest, stream pb.ChatService_ReceiveStreamServer) error {
	fmt.Printf("ReceiveStream : %s from %s", req.Content, req.Sender)
	for i := 0; i < 10; i++ {
		time.Sleep(100 * time.Millisecond)
		if err := stream.Send(&pb.MessageResponse{
			Content:  fmt.Sprintf("服务器消息 #%d: %s", i+1, req.Content),
			Receiver: req.Sender,
			Seq:      int32(i + 1),
		}); err != nil {
			return err
		}
	}
	return nil
}
func (s *server) BiStream(stream pb.ChatService_BiStreamServer) error {
	return status.Errorf(codes.Unimplemented, "method BiStream not implemented")
}

func main() {
	listen, err := net.Listen("tcp", ":50051") //监听端口
	if err != nil {
		fmt.Println("failed to listen:", err)
	}
	s := grpc.NewServer() //创建grpc服务
	pb.RegisterChatServiceServer(s, &server{})
	fmt.Println("gRPC server listening on :50051")
	if err := s.Serve(listen); err != nil { //启动服务
		fmt.Println("failed to serve:", err)
	}
}
