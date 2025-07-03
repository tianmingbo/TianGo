package main

import (
	"context"
	"fmt"
	"log"

	_ "github.com/mbobakov/grpc-consul-resolver" // It's important
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	pb "lGo/shop/proto"
)

func main() {
	conn, err := grpc.NewClient(
		"consul://10.6.64.191:8500/user-service?wait=14s",
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy": "round_robin"}`),
	)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()
	cli := pb.NewUserClient(conn)
	for i := 0; i < 10; i++ {
		response, err := cli.GetUserList(context.Background(), &pb.PageInfo{Page: 1, Size: 2})
		if err != nil {
			return
		}
		fmt.Println(response)
	}

}
