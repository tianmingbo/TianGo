package main

import (
	"context"
	"fmt"
	"os"
	"strconv"

	"github.com/apache/rocketmq-client-go/v2"
	"github.com/apache/rocketmq-client-go/v2/primitive"
	"github.com/apache/rocketmq-client-go/v2/producer"
)

type myManualQueueSelector struct{}

func newMyQueueSelector() producer.QueueSelector {
	return new(myManualQueueSelector)
}

func (myManualQueueSelector) Select(message *primitive.Message, queues []*primitive.MessageQueue, lastBrokerName string) *primitive.MessageQueue {
	message.Queue.BrokerName = queues[0].BrokerName
	fmt.Println("指定queueId=", message.Queue.QueueId)
	return message.Queue
}

// Package main implements a simple producer to send message.
func main() {
	p, _ := rocketmq.NewProducer(
		producer.WithNsResolver(primitive.NewPassthroughResolver([]string{"10.6.64.191:9876"})),
		producer.WithRetry(2),
		producer.WithQueueSelector(newMyQueueSelector()),
	)

	err := p.Start()
	if err != nil {
		fmt.Printf("start producer error: %s", err.Error())
		os.Exit(1)
	}
	topic := "test"
	//指定queueId
	for i := 0; i < 100; i++ {
		msg := &primitive.Message{
			Topic: topic,
			Body:  []byte("Hello RocketMQ Go Client! " + strconv.Itoa(i)),
			Queue: &primitive.MessageQueue{Topic: topic, QueueId: 1},
		}
		res, err := p.SendSync(context.Background(), msg)

		if err != nil {
			fmt.Printf("send message error: %s\n", err)
		} else {
			fmt.Printf("send message success: result=%s\n", res.String())
		}
	}
	err = p.Shutdown()
	if err != nil {
		fmt.Printf("shutdown producer error: %s", err.Error())
	}
}
