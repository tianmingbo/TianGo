package main

import (
	"context"
	"fmt"
	"os"
	"sync"

	"github.com/apache/rocketmq-client-go/v2"
	"github.com/apache/rocketmq-client-go/v2/primitive"
	"github.com/apache/rocketmq-client-go/v2/producer"
)

// Package main implements a async producer to send message.
func main() {
	p, _ := rocketmq.NewProducer(
		producer.WithNsResolver(primitive.NewPassthroughResolver([]string{"10.6.64.191:9876"})),
		producer.WithRetry(2))

	err := p.Start()
	if err != nil {
		fmt.Printf("start producer error: %s", err.Error())
		os.Exit(1)
	}
	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		err := p.SendAsync(context.Background(),
			func(ctx context.Context, result *primitive.SendResult, e error) {
				if e != nil {
					fmt.Printf("receive message error: %s\n", err)
				} else {
					fmt.Printf("send message success: result=%s\n", result.String())
				}
				wg.Done()
			}, primitive.NewMessage("test", []byte("Hello RocketMQ Go Client!")))

		if err != nil {
			fmt.Printf("send message error: %s\n", err)
		}
	}
	wg.Wait()
	err = p.Shutdown()
	if err != nil {
		fmt.Printf("shutdown producer error: %s", err.Error())
	}
}
