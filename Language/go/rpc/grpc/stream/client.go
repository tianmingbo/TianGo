package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"io"
	"lGo/rpc/grpc/stream/pb"
	"log"
	"strconv"
	"sync"
	"time"
)

func testSimpleRpc(client pb.ChatServiceClient) error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	response, err := client.SendMessage(ctx, &pb.MessageRequest{Content: "hello", Sender: "tian"})
	if err != nil {
		fmt.Println("testSimpleRpc err:", err)
		return err
	}
	log.Printf("Response from server: %v\n", response)
	return nil
}

/*
*
stream.Send() 发送多条消息
CloseAndRecv() 关闭流并接收响应
*/
func testClientStream(client pb.ChatServiceClient) error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	stream, err := client.SendStream(ctx) // 创建客户端流
	if err != nil {
		log.Println("创建客户端流失败:", err)
	}
	for i := 0; i < 5; i++ {
		if err := stream.Send(&pb.MessageRequest{Content: strconv.Itoa(i), Sender: "client"}); err != nil {
			log.Println("发送数据失败:", err)
		}
	}
	response, err := stream.CloseAndRecv()
	if err != nil {
		log.Println("接收数据失败:", err)
	}
	log.Printf("Response from server: %v\n", response)
	return nil
}

func testServerStream(client pb.ChatServiceClient) error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	req := &pb.MessageRequest{Content: "hello", Sender: "tian"}
	stream, err := client.ReceiveStream(ctx, req)
	if err != nil {
		log.Println("创建服务端流失败:", err)
	}
	for {
		resp, err := stream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Println("接收数据失败:", err)
		}
		log.Printf("Response from server: %v\n", resp)
	}
	return nil
}

func TestBidirectionalStream(client pb.ChatServiceClient) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	stream, err := client.BiStream(ctx)
	if err != nil {
		return fmt.Errorf("创建双向流失败: %v", err)
	}

	var wg sync.WaitGroup

	// 发送消息的 goroutine
	wg.Add(1)
	go func() {
		defer wg.Done()

		messages := []string{"双向流消息1", "双向流消息2", "双向流消息3", "双向流消息4", "双向流消息5"}
		for _, msg := range messages {
			err := stream.Send(&pb.MessageRequest{
				Content: msg,
				Sender:  "客户端",
			})

			if err != nil {
				log.Printf("发送双向流消息失败: %v", err)
				return
			}

			log.Printf("已发送双向流消息: %s", msg)
			time.Sleep(500 * time.Millisecond)
		}

		// 发送完毕，关闭发送端
		stream.CloseSend()
	}()

	// 接收响应的 goroutine
	wg.Add(1)
	go func() {
		defer wg.Done()

		for {
			resp, err := stream.Recv()
			if err == io.EOF {
				break // 流结束
			}

			if err != nil {
				log.Printf("接收双向流响应失败: %v", err)
				break
			}

			log.Printf("收到双向流响应 #%d: %s", resp.Seq, resp.Content)
		}
	}()

	// 等待两个 goroutine 完成
	wg.Wait()
	return nil
}

func main() {
	conn, err := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Printf("did not connect:%v", err)
	}
	defer conn.Close()
	client := pb.NewChatServiceClient(conn)
	fmt.Println("*************testSimpleRpc*****************")
	if err := testSimpleRpc(client); err != nil {
		log.Println("简单RPC err:", err)
	}

	fmt.Println("*************testClientStream*****************")
	if err := testClientStream(client); err != nil {
		log.Println("client stream RPC err:", err)
	}

	fmt.Println("*************testServerStream*****************")
	if err := testServerStream(client); err != nil {
		log.Println("server stream RPC err:", err)
	}

	fmt.Println("*************TestBidirectionalStream*****************")
	if err := TestBidirectionalStream(client); err != nil {
		log.Println("bi_direction stream RPC err:", err)
	}
}
