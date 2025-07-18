package main

import (
	"context"
	"fmt"
	"os"
	"time"

	"github.com/apache/rocketmq-client-go/v2"
	"github.com/apache/rocketmq-client-go/v2/primitive"
	"github.com/apache/rocketmq-client-go/v2/producer"
)

func main() {
	p, _ := rocketmq.NewProducer(
		producer.WithGroupName("please_rename_unique_group_name"),
		producer.WithNsResolver(primitive.NewPassthroughResolver([]string{"10.6.64.191:9876"})),
		producer.WithRetry(2),
	)
	err := p.Start()
	if err != nil {
		fmt.Printf("start producer error: %s", err.Error())
		os.Exit(1)
	}

	topic := "RequestTopic"
	ttl := 5 * time.Second
	msg := &primitive.Message{
		Topic: topic,
		Body:  []byte("Hello RPC RocketMQ Go Client!"),
	}

	now := time.Now()
	f := func(ctx context.Context, responseMsg *primitive.Message, respErr error) {
		if respErr != nil {
			fmt.Printf("request to <%s> fail, err:%v \n", topic, respErr)
			return
		}
		fmt.Printf("Requst to %s cost:%d ms responseMsg:%s\n", topic, time.Since(now)/time.Millisecond, responseMsg.String())
	}
	err = p.RequestAsync(context.Background(), ttl, f, msg)
	if err != nil {
		fmt.Printf("Request Async message error: %s\n", err)
		return
	}

	time.Sleep(time.Minute)
	err = p.Shutdown()
	if err != nil {
		fmt.Printf("shutdown producer error: %s", err.Error())
	}
}
